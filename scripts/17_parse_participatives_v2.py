"""
Robust parser for BAM 'Indicateurs des banques et fenêtres participatives' PDFs.

Handles two formats:
- Modern (2022+): single-line labels
- Older / wrapped (2021-Q4): labels wrap onto the line before values

Strategy: pre-process by joining a label-only line with the following value-only line.
"""
import pdfplumber
import re
from pathlib import Path
import pandas as pd
import json

PDF_DIR = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf")
OUT = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate")
OUT.mkdir(parents=True, exist_ok=True)

FR_MONTHS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5,
    "juin": 6, "juillet": 7, "août": 8, "aout": 8, "septembre": 9, "octobre": 10,
    "novembre": 11, "décembre": 12, "decembre": 12,
    "janv": 1, "févr": 2, "fevr": 2, "avr": 4, "juil": 7, "sept": 9, "oct": 10, "nov": 11, "déc": 12, "dec": 12,
}


def parse_fr_date_from_filename(name: str):
    s = name.lower()
    s = (s.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
           .replace("ç", "c").replace("û", "u").replace("ù", "u").replace("ô", "o"))
    s_norm = re.sub(r"[_\-\.]+", " ", s)
    s_concat = re.sub(r"\s+", "", s_norm)
    month = None
    for k, v in FR_MONTHS.items():
        k2 = (k.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
                .replace("ç", "c").replace("û", "u").replace("ù", "u").replace("ô", "o"))
        if re.search(rf"\b{k2}\b", s_norm) or k2 in s_concat:
            month = v
            break
    m = re.search(r"(20\d{2})", s_norm)
    if not m:
        return None
    year = int(m.group(1))
    if month is None:
        m2 = re.search(r"(?:^|\s)(\d{2})[\s\-]?(20\d{2})", s_norm)
        if m2:
            month = int(m2.group(1))
        else:
            m3 = re.search(r"(20\d{2})[\s\-](\d{2})(?:\s|$)", s_norm)
            if m3:
                month = int(m3.group(2))
    if month is None or not (1 <= month <= 12):
        return None
    return pd.Timestamp(year=year, month=month, day=1)


def join_wrapped_lines(text: str) -> str:
    """If a line has no digits and the NEXT line starts with digits, concatenate them.
    This handles wrapped labels like 'Financements participatifs' (no digits) followed by
    '13 480 352 19 256 731 ...' (digits only).
    Joins multiple consecutive label-only lines into one combined label.
    """
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        has_digits = bool(re.search(r"\d{2,}", stripped))
        if not has_digits and stripped and i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            nxt_has_digits = bool(re.search(r"\d{2,}", nxt))
            if nxt_has_digits:
                # Concatenate all consecutive label-only lines into one
                label_parts = [stripped]
                j = i + 1
                while j < len(lines) and not re.search(r"\d{2,}", lines[j].strip()) and lines[j].strip():
                    label_parts.append(lines[j].strip())
                    j += 1
                # now j points to value line
                if j < len(lines) and re.search(r"\d{2,}", lines[j].strip()):
                    combined_label = " ".join(label_parts)
                    out.append(f"{combined_label} {lines[j].strip()}")
                    i = j + 1
                    continue
        out.append(line)
        i += 1
    return "\n".join(out)


def parse_number(s: str):
    s = s.replace(" ", "").replace("\u00a0", "").replace(",", "").strip()
    if not s or s == "-":
        return None
    try:
        return int(s)
    except ValueError:
        try:
            return int(float(s))
        except ValueError:
            return None


def parse_pcts(s: str):
    nums = re.findall(r"(-?[\d,]+)\s*%?", s)
    if len(nums) >= 1:
        v1 = float(nums[0].replace(",", "."))
    else:
        v1 = None
    if len(nums) >= 2:
        v2 = float(nums[1].replace(",", "."))
    else:
        v2 = None
    return v1, v2


# Patterns (multi-line aware via pre-processing)
PAT_TOTAL = re.compile(
    r"^(?:Financements participatifs\s+)?par\s+Mourabaha\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)$",
    re.IGNORECASE,
)
PAT_TOTAL_DIRECT = re.compile(
    r"^Financements participatifs par Mourabaha\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)$",
    re.IGNORECASE,
)
PAT_DONT = re.compile(
    r"^[-\s]*Dont\s*:?\s*Mourabaha\s+(\w+)\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)$",
    re.IGNORECASE,
)
PAT_SALAM = re.compile(
    r"^Financements\s+Salam\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)$",
    re.IGNORECASE,
)


def extract_table(text: str):
    rows = {}
    text = join_wrapped_lines(text)

    # Total Mourabaha
    for m in PAT_TOTAL_DIRECT.finditer(text):
        a, b, rest = m.groups()
        v1, v2 = parse_pcts(rest)
        rows["Mourabaha_total"] = (parse_number(a), parse_number(b), v1, v2)

    # Don't-line breakdown
    for m in PAT_DONT.finditer(text):
        label, a, b, rest = m.groups()
        v1, v2 = parse_pcts(rest)
        rows[f"Mourabaha_{label.lower()}"] = (parse_number(a), parse_number(b), v1, v2)

    # Salam
    for m in PAT_SALAM.finditer(text):
        a, b, rest = m.groups()
        v1, v2 = parse_pcts(rest)
        rows["Salam"] = (parse_number(a), parse_number(b), v1, v2)

    return rows


def parse_pdf(fp: Path):
    date = parse_fr_date_from_filename(fp.name)
    if date is None:
        return None

    full_text = ""
    try:
        with pdfplumber.open(fp) as pdf:
            for page in pdf.pages:
                full_text += "\n" + (page.extract_text() or "")
    except Exception as e:
        return {"file": fp.name, "date": date, "error": str(e)}

    # Try to override date from PDF body title (more reliable than filename)
    title_m = re.search(r"INDICATEURS[^\n]*\n[^\n]*?([A-Za-zéèêàûôç]+)[-\s]+(\d{2,4})", full_text)
    if title_m:
        title_month = title_m.group(1).lower()
        title_year_raw = title_m.group(2)
        title_year = int(title_year_raw) if len(title_year_raw) == 4 else 2000 + int(title_year_raw)
        if title_month in FR_MONTHS:
            date = pd.Timestamp(year=title_year, month=FR_MONTHS[title_month], day=1)

    rows = extract_table(full_text)
    return {"file": fp.name, "date": date, "rows": rows}


def main():
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    results = []
    skipped = []
    for fp in pdfs:
        name = fp.name
        # Skip non-participative publications
        if any(x in name for x in ["Taux", "IPAI", "Flash", "Pub SM", "DERI", "DSGD"]):
            continue
        if not any(x in name for x in ["Indicateur", "TDB", "banque"]):
            continue
        r = parse_pdf(fp)
        if r is None:
            skipped.append(name)
            continue
        if "error" in r:
            print(f"  ERROR parsing {name}: {r['error']}")
            continue
        if r.get("rows"):
            results.append(r)
        else:
            skipped.append(name)

    print(f"Parsed: {len(results)} files, Skipped: {len(skipped)}")
    if skipped:
        print("Skipped files:")
        for s in skipped:
            print(f"  {s}")

    # Convert to long format
    rows = []
    for r in results:
        for key, (cur, ya, mv, av) in r["rows"].items():
            rows.append({
                "date": r["date"],
                "file": r["file"],
                "metric": key,
                "value_current_month_kDH": cur,
                "value_year_ago_kDH": ya,
                "monthly_var_pct": mv,
                "annual_var_pct": av,
            })
    df = pd.DataFrame(rows)
    print(f"\nLong format rows: {len(df)}")
    print(f"Unique dates: {df['date'].nunique()}")
    print(f"Date range: {df['date'].min()} -> {df['date'].max()}")

    # Pivot wide: take current month value
    pivot = df.pivot_table(
        index="date", columns="metric",
        values="value_current_month_kDH", aggfunc="first",
    ).sort_index()
    print(f"\nWide pivot shape: {pivot.shape}")
    print(f"Non-null counts:\n{pivot.count()}")

    # Save
    pivot.to_csv(OUT / "participatives_wide.csv")
    df.to_csv(OUT / "participatives_raw.csv", index=False)
    # Also save the metadata of parsed files
    meta = [{"date": str(r["date"]), "file": r["file"], "metrics": list(r["rows"].keys())} for r in results]
    Path(OUT / "participatives_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))

    print(f"\nSaved:\n  {OUT / 'participatives_wide.csv'}\n  {OUT / 'participatives_raw.csv'}\n  {OUT / 'participatives_meta.json'}")

    # Print sample
    print("\nSample of wide pivot:")
    print(pivot.head(10).to_string())
    print("\nLast 10 rows:")
    print(pivot.tail(10).to_string())


if __name__ == "__main__":
    main()