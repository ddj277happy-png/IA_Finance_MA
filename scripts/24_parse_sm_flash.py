"""Parse BAM SM (Statistiques Monétaires) + Flash Crédits/Dépôts PDFs for
Crédits à l'habitat (conventional housing credit) time series.

Each PDF gives:
- Year-end snapshot (SM): Crédits à l'habitat, Crédits aux promoteurs immobiliers, etc.
- Some SM PDFs also give intra-year quarterly snapshots (current quarter + previous)
- Flash PDFs give year-end snapshots with full sectoral breakdown
"""
import pdfplumber
import re
from pathlib import Path
import pandas as pd
from datetime import datetime

PDF_DIR = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf")
OUT = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate")

FR_MONTHS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5,
    "juin": 6, "juillet": 7, "août": 8, "aout": 8, "septembre": 9, "octobre": 10,
    "novembre": 11, "décembre": 12, "decembre": 12,
}


def parse_number(s):
    s = s.replace(" ", "").replace("\u00a0", "").replace(",", "").strip()
    if not s or s == "-":
        return None
    try:
        return int(s)
    except ValueError:
        try:
            return int(round(float(s)))
        except ValueError:
            return None


def parse_date_from_filename(name):
    """Parse date from filename patterns like 'Pub SM dec-17.pdf' or 'Flash crédits dépôts Déc 2021.pdf'."""
    s = name.lower()
    # remove accents
    s = (s.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
           .replace("ç", "c").replace("û", "u").replace("ù", "u").replace("ô", "o"))
    # Find year
    m = re.search(r"(20\d{2})", s)
    if not m:
        return None
    year = int(m.group(1))
    # Find month
    month = None
    for k, v in FR_MONTHS.items():
        if k in s:
            month = v
            break
    if month is None:
        # "dec-17" → 12 + 17 → year 2017
        m2 = re.search(r"dec[-\s]+(\d{2})$", s)
        if m2:
            y2 = int(m2.group(1))
            year = 2000 + y2
            month = 12
    if month is None:
        # If year found but no month, default to December
        month = 12
    return pd.Timestamp(year=year, month=month, day=1)


def parse_page_for_habitat(text):
    """Find Crédits à l'habitat and related series in a page of text.

    Returns dict with keys:
        credits_immobiliers_MDH, credits_habitat_MDH, credits_promoteurs_MDH,
        credits_equipement_MDH, credits_consommation_MDH, etc.
    Values are dicts with 'current' and 'year_ago' (when applicable).
    """
    results = {}

    # The relevant section is "TABLEAU 3.1 : Ventilation du crédit bancaire par objet économique"
    # or similar. Look for known patterns.

    # Pattern: "Crédits immobiliers  XXX XXX" (totals)
    #          "Dont : Crédits à l'habitat  XXX XXX"
    #          "Crédits aux promoteurs immobiliers  XXX XXX"

    # Try several patterns
    patterns = [
        ("credits_immobiliers_MDH",
         r"Cr[eé]dits\s+immobiliers\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)"),
        ("credits_habitat_MDH",
         r"Cr[eé]dits\s+(?:à\s+)?l['']habitat\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)"),
        ("credits_habitat_financement_participatif_MDH",
         r"(?:Dont\s*:?\s*)?Financement\s+participatif\s+à\s+l['']habitat\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)"),
        ("credits_promoteurs_MDH",
         r"Cr[eé]dits\s+aux\s+promoteurs\s+immobiliers\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)"),
        ("credits_equipement_MDH",
         r"Cr[eé]dits\s+(?:à\s+)?l['']\u00e9quipement\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)"),
        ("credits_consommation_MDH",
         r"Cr[eé]dits\s+(?:à\s+)?la\s+consommation\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)"),
        ("credits_treso_consommation_MDH",
         r"Comptes\s+d[eé]biteurs\s+et\s+cr[eé]dits\s+de\s+tr[eé]sorerie\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)"),
        ("credits_bancaire_total_MDH",
         r"Cr[eé]dit\s+bancaire(?:\s+\(3\))?\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)"),
        ("credits_divers_MDH",
         r"Cr[eé]ances\s+diverses\s+sur\s+la\s+client[eè]le\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)"),
        ("credits_souffrance_MDH",
         r"Cr[eé]ances\s+en\s+souffrance\s+([\d\s\u00a0]+)\s+([\d\s\u00a0]+)\s+([\d,%\-\s]+)"),
    ]
    for key, pat in patterns:
        m = re.search(pat, text)
        if m:
            a, b, rest = m.groups()
            # Pad leading zeros (French thousands)
            a_clean = a.replace(" ", "").replace("\u00a0", "")
            b_clean = b.replace(" ", "").replace("\u00a0", "")
            try:
                av = int(a_clean) if a_clean.isdigit() else int(a_clean) if a_clean.lstrip("-").isdigit() else None
            except ValueError:
                av = None
            try:
                bv = int(b_clean) if b_clean.isdigit() else int(b_clean) if b_clean.lstrip("-").isdigit() else None
            except ValueError:
                bv = None
            results[key] = {"year_ago": av, "current": bv}

    # Also extract policy rate info if available in title
    return results


def parse_sm_pdf(fp):
    """Parse a SM PDF — extract credit by objet économique series."""
    text = ""
    try:
        with pdfplumber.open(fp) as pdf:
            for page in pdf.pages:
                text += "\n" + (page.extract_text(x_tolerance=1, y_tolerance=1) or "")
    except Exception as e:
        return {"file": fp.name, "error": str(e)}

    date = parse_date_from_filename(fp.name)
    if date is None:
        return {"file": fp.name, "error": "no date"}

    data = parse_page_for_habitat(text)
    data["date"] = date
    data["file"] = fp.name
    return data


def parse_flash_pdf(fp):
    """Parse Flash Crédits/Dépôts PDF."""
    text = ""
    try:
        with pdfplumber.open(fp) as pdf:
            for page in pdf.pages:
                text += "\n" + (page.extract_text(x_tolerance=1, y_tolerance=1) or "")
    except Exception as e:
        return {"file": fp.name, "error": str(e)}

    date = parse_date_from_filename(fp.name)
    if date is None:
        return {"file": fp.name, "error": "no date"}

    data = parse_page_for_habitat(text)
    # Flash PDFs may have different patterns. Try to grab Habitat from text.
    # In Flash PDF we saw earlier:
    # "Crédit bancaire aux ménages par nature de crédit ... Habitat 256,2 ... Mourabaha immobilière 29,7"
    # Different patterns needed
    m = re.search(r"Habitat\s+([\d,]+)\s+([\d,]+)\s+([\d,%\-\s]+)", text)
    if m:
        try:
            habitat_current = float(m.group(1).replace(",", ".")) * 1000  # MMDH → MDH
            habitat_ya = float(m.group(2).replace(",", ".")) * 1000
            data["credits_habitat_MMDH"] = {"year_ago": habitat_ya, "current": habitat_current}
        except ValueError:
            pass

    m = re.search(r"Mourabaha\s+immobili[eè]re\*?\s+([\d,]+)\s+([\d,]+)", text)
    if m:
        try:
            mb_current = float(m.group(1).replace(",", ".")) * 1000
            mb_ya = float(m.group(2).replace(",", ".")) * 1000
            data["murabaha_habitat_MMDH"] = {"year_ago": mb_ya, "current": mb_current}
        except ValueError:
            pass

    data["date"] = date
    data["file"] = fp.name
    return data


def main():
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    sm_records = []
    flash_records = []

    for fp in pdfs:
        name = fp.name
        if "Flash" in name and "credits" in name.lower() or "Flash" in name and "dép" in name.lower():
            r = parse_flash_pdf(fp)
            if "error" not in r:
                flash_records.append(r)
                print(f"  FLASH: {fp.name[:50]:50} | {r['date']} | keys={list(r.keys())}")
        elif "Pub SM" in name or "DERI" in name or "DSGD" in name and "SM" in name:
            r = parse_sm_pdf(fp)
            if "error" not in r and len(r) > 2:
                sm_records.append(r)
                print(f"  SM:    {fp.name[:50]:50} | {r['date']} | keys={list(r.keys())}")

    print(f"\nSM records: {len(sm_records)}, Flash records: {len(flash_records)}")

    # Save raw extracted data as JSON for inspection
    import json
    Path(OUT / "sm_flash_raw.json").write_text(
        json.dumps({"sm": sm_records, "flash": flash_records}, ensure_ascii=False, indent=2, default=str)
    )
    print(f"\nSaved: {OUT / 'sm_flash_raw.json'}")

    # Build a DataFrame from SM records
    sm_df_rows = []
    for r in sm_records:
        if "date" not in r:
            continue
        row = {"date": r["date"], "source": r["file"]}
        for k, v in r.items():
            if isinstance(v, dict) and "current" in v:
                row[k] = v["current"]
                row[f"{k}_yago"] = v.get("year_ago")
        sm_df_rows.append(row)
    sm_df = pd.DataFrame(sm_df_rows).set_index("date").sort_index()
    sm_df.to_csv(OUT / "sm_credit_series.csv")
    print(f"\nSM CSV: {sm_df.shape}")
    print(sm_df.tail(10))

    # Flash
    flash_df_rows = []
    for r in flash_records:
        if "date" not in r:
            continue
        row = {"date": r["date"], "source": r["file"]}
        for k, v in r.items():
            if isinstance(v, dict) and "current" in v:
                row[k] = v["current"]
                row[f"{k}_yago"] = v.get("year_ago")
        flash_df_rows.append(row)
    flash_df = pd.DataFrame(flash_df_rows).set_index("date").sort_index()
    flash_df.to_csv(OUT / "flash_credit_series.csv")
    print(f"\nFlash CSV: {flash_df.shape}")
    print(flash_df.tail(10))


if __name__ == "__main__":
    main()