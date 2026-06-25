"""Parse Taux débiteurs quarterly PDFs into a quarterly series of lending rates."""
import pdfplumber
import re
from pathlib import Path
import pandas as pd
import json

PDF_DIR = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf")
OUT = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate")

FR_TO_MONTH = {"T1": 1, "T2": 4, "T3": 7, "T4": 10}


def parse_quarter(s):
    """Parse 'T4-2025' → Timestamp(2025-10-01)."""
    m = re.match(r"T\s*([1-4])\s*[- ]?\s*(\d{4})", s)
    if not m:
        return None
    q, y = int(m.group(1)), int(m.group(2))
    return pd.Timestamp(year=y, month=FR_TO_MONTH[f"T{q}"], day=1)


def parse_taux_pdf(fp):
    """Parse one Taux débiteurs PDF. Returns dict of quarter -> {metric: rate}."""
    text = ""
    try:
        with pdfplumber.open(fp) as pdf:
            for page in pdf.pages:
                text += "\n" + (page.extract_text(x_tolerance=1, y_tolerance=1) or "")
    except Exception:
        return {}

    # Find the header line with quarter labels
    header = None
    header_line = None
    for line in text.split("\n"):
        # Look for "T?-YYYY T?-YYYY ..."
        quarters = re.findall(r"T\s*[1-4]\s*[- ]?\s*20\d{2}", line)
        if len(quarters) >= 4:
            header = [parse_quarter(q) for q in quarters]
            header_line = line
            break

    if not header:
        return {}

    results = {}
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Match "Label  num num num ..."
        # Find numeric tokens (comma decimal, no %)
        m = re.match(r"^(.+?)\s+([\d,\s]+)$", line)
        if not m:
            continue
        label, nums_str = m.groups()
        nums = []
        for n in nums_str.split():
            try:
                # French decimal with comma
                v = float(n.replace(",", "."))
                nums.append(v)
            except ValueError:
                continue
        if len(nums) != len(header):
            continue
        label_clean = label.strip()
        for date, val in zip(header, nums):
            results.setdefault(date, {})[label_clean] = val

    return results


def main():
    pdfs = sorted(PDF_DIR.glob("Taux*.pdf")) + sorted(PDF_DIR.glob("Publication*taux*.pdf"))
    all_records = {}

    for fp in pdfs:
        rec = parse_taux_pdf(fp)
        if rec:
            for date, metrics in rec.items():
                all_records.setdefault(date, {}).update(metrics)
            print(f"  {fp.name[:50]:50} | {len(rec)} quarters")
        else:
            print(f"  {fp.name[:50]:50} | NO DATA")

    print(f"\nTotal unique quarters: {len(all_records)}")
    print(f"Date range: {min(all_records)} -> {max(all_records)}")

    # Build DataFrame
    rows = []
    for date, metrics in sorted(all_records.items()):
        for label, val in metrics.items():
            rows.append({"date": date, "metric": label, "rate_pct": val})

    df = pd.DataFrame(rows)
    pivot = df.pivot_table(index="date", columns="metric", values="rate_pct", aggfunc="first").sort_index()
    print(f"\nShape: {pivot.shape}")
    print(pivot.to_string())

    pivot.to_csv(OUT / "taux_debiteurs_quarterly.csv")
    df.to_csv(OUT / "taux_debiteurs_long.csv", index=False)
    print(f"\nSaved: {OUT / 'taux_debiteurs_quarterly.csv'}")


if __name__ == "__main__":
    main()