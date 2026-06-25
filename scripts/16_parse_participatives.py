"""
Parse all participatory bank monthly PDFs into a single dataset.

Each PDF has the same structure:
  INDICATEURS DES BANQUES ET FENETRES PARTICIPATIVES
  <Month-YY>
  NOMBRE D'AGENCES ET DE COMPTES A VUE
  ...
  ENCOURS DES FINANCEMENTS PARTICIPATIFS
  (Montant en milliers de dhs)
  ...
  Financements participatifs par Mourabaha  XX XXX XXX  YY YYY YYY  ZZ%  WW%
  Dont : Mourabaha immobilière  XX XXX XXX  YY YYY YYY  ZZ%  WW%
  Dont : Mourabaha automobile
  Dont : Mourabaha équipement
  Dont : Mourabaha matières premières
  Financements Salam  ...

Format: 2 numbers (current, year-ago) + 2 percentages (monthly var, annual var)
"""
import pdfplumber
import re
from pathlib import Path
import pandas as pd

PDF_DIR = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf")
OUT = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate/participatives_raw.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

FR_MONTHS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5,
    "juin": 6, "juillet": 7, "août": 8, "aout": 8, "septembre": 9, "octobre": 10,
    "novembre": 11, "décembre": 12, "decembre": 12,
    "janv": 1, "févr": 2, "fevr": 2, "avr": 4, "juil": 7, "sept": 9, "oct": 10, "nov": 11, "déc": 12, "dec": 12,
}


def parse_fr_date_from_filename(name: str):
    """Best-effort date from filename like 'TDB Indicateurs des banques participatives-Janvier 2020.pdf'."""
    s = name.lower()
    # remove accents
    s = (s.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
           .replace("ç", "c").replace("û", "u").replace("ù", "u").replace("ô", "o"))
    # Replace separators with spaces (so word boundaries work — _ is a word char in regex)
    s_norm = re.sub(r"[_\-\.]+", " ", s)
    # find month token (handle concatenated "Janvier2020" by also checking without space)
    s_concat = re.sub(r"\s+", "", s_norm)
    month = None
    for k, v in FR_MONTHS.items():
        k2 = (k.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
                .replace("ç", "c").replace("û", "u").replace("ù", "u").replace("ô", "o"))
        if re.search(rf"\b{k2}\b", s_norm) or k2 in s_concat:
            month = v
            break
    # find 4-digit year
    m = re.search(r"(20\d{2})", s_norm)
    if not m:
        return None
    year = int(m.group(1))
    if month is None:
        # try numeric "MM YYYY" or "YYYY MM" patterns
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


def parse_number(s: str):
    """Parse '33 738 808' style numbers to int."""
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


def extract_table(text: str):
    """Find lines that have label followed by 2 big numbers + 2 percentages.
    Returns dict: label -> (current, year_ago, monthly_var, annual_var)
    """
    rows = {}
    # The Mourabaha section: lines like 'Financements participatifs par Mourabaha  33 738 808  42 841 377  2,8%  27,0%'
    # 'Dont : Mourabaha immobilière  27 690 629  33 669 356  2,0%  21,6%'
    # We want: Murabaha totale, Mourabaha immobiliere, automobile, equipement, matieres premieres, Salam
    pat = re.compile(
        r"^(?:Financements participatifs par )?Mourabaha(?:\s+hors\s+marges\s+constatées\s+d'avance)?\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)$",
        re.MULTILINE | re.IGNORECASE,
    )
    for m in pat.finditer(text):
        a, b, rest = m.groups()
        # parse the trailing percentages
        rest = rest.strip()
        nums = re.findall(r"(-?[\d,]+)\s*%?", rest)
        rows["Mourabaha_total"] = (parse_number(a), parse_number(b),
                                   float(nums[0].replace(",", ".")) if len(nums) > 0 else None,
                                   float(nums[1].replace(",", ".")) if len(nums) > 1 else None)

    # 'Dont : Mourabaha xxx  val1 val2 var% annual%'
    pat2 = re.compile(
        r"^[-\s]*Dont\s*:?\s*Mourabaha\s+(\w+)\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)$",
        re.MULTILINE | re.IGNORECASE,
    )
    for m in pat2.finditer(text):
        label, a, b, rest = m.groups()
        rest = rest.strip()
        nums = re.findall(r"(-?[\d,]+)\s*%?", rest)
        rows[f"Mourabaha_{label.lower()}"] = (
            parse_number(a), parse_number(b),
            float(nums[0].replace(",", ".")) if len(nums) > 0 else None,
            float(nums[1].replace(",", ".")) if len(nums) > 1 else None,
        )

    # Salam: 'Financements Salam  254 493  467 963  9,5%  84%'
    pat3 = re.compile(
        r"^Financements\s+Salam\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)$",
        re.MULTILINE | re.IGNORECASE,
    )
    for m in pat3.finditer(text):
        a, b, rest = m.groups()
        rest = rest.strip()
        nums = re.findall(r"(-?[\d,]+)\s*%?", rest)
        rows["Salam"] = (parse_number(a), parse_number(b),
                        float(nums[0].replace(",", ".")) if len(nums) > 0 else None,
                        float(nums[1].replace(",", ".")) if len(nums) > 1 else None)

    # Also parse deposits: 'Dépôts à vue' and 'Dépôts d'investissement'
    pat4 = re.compile(
        r"^Dépôts\s+(à\s+vue|d[''']investissement)\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)$",
        re.MULTILINE | re.IGNORECASE,
    )
    for m in pat4.finditer(text):
        kind, a, b, rest = m.groups()
        rest = rest.strip()
        nums = re.findall(r"(-?[\d,]+)\s*%?", rest)
        rows[f"Depot_{kind.replace(' ', '_')}"] = (
            parse_number(a), parse_number(b),
            float(nums[0].replace(",", ".")) if len(nums) > 0 else None,
            float(nums[1].replace(",", ".")) if len(nums) > 1 else None,
        )

    return rows


def parse_pdf(fp: Path):
    """Parse one PDF. Returns dict {date, label, raw_values: {key: (current, year_ago)}}"""
    date = parse_fr_date_from_filename(fp.name)
    if date is None:
        return None

    full_text = ""
    try:
        with pdfplumber.open(fp) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                full_text += "\n" + t
    except Exception as e:
        return {"file": fp.name, "date": date, "error": str(e)}

    # Extract "Title" line e.g. "INDICATEURS DES BANQUES ET FENETRES PARTICIPATIVES\ndécembre-25"
    title_m = re.search(r"INDICATEURS[^\n]*\n[^\n]*?(\w+)[-\s]+(\d{2,4})", full_text)
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
    # Use all PDFs that mention participative OR banks in title
    results = []
    for fp in pdfs:
        # skip if it's clearly a different publication (taux, flash, IPAI)
        name = fp.name
        if "Taux" in name or "IPAI" in name or "Flash" in name or "Pub SM" in name or "DERI" in name or "DSGD" in name:
            continue
        if "Indicateur" not in name and "TDB" not in name and "banque" not in name.lower():
            continue
        r = parse_pdf(fp)
        if r and r.get("rows"):
            results.append(r)
            print(f"  {fp.name[:60]:60} | {r['date']} | keys={list(r['rows'].keys())}")

    print(f"\nTotal parsed: {len(results)}")

    # Convert to DataFrame
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
    print(df.head(20))

    # Pivot to wide
    pivot = df.pivot_table(
        index="date",
        columns="metric",
        values="value_current_month_kDH",
        aggfunc="first",
    )
    pivot = pivot.sort_index()
    print(f"\nWide pivot shape: {pivot.shape}")
    print(pivot.head())

    pivot.to_csv(OUT.parent / "participatives_wide.csv")
    df.to_csv(OUT, index=False)
    print(f"\nSaved:\n  {OUT}\n  {OUT.parent / 'participatives_wide.csv'}")


if __name__ == "__main__":
    main()