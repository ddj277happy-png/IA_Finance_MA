"""Parse BAM SM + Flash Crédits/Dépôts PDFs for conventional housing credit."""
import pdfplumber
import re
from pathlib import Path
import pandas as pd
import json

PDF_DIR = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf")
OUT = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate")

FR_MONTHS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5,
    "juin": 6, "juillet": 7, "août": 8, "aout": 8, "septembre": 9, "octobre": 10,
    "novembre": 11, "décembre": 12, "decembre": 12,
}


def parse_date_from_filename(name):
    s = name.lower()
    s = (s.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
           .replace("ç", "c").replace("û", "u").replace("ù", "u").replace("ô", "o"))
    m = re.search(r"(20\d{2})", s)
    if not m:
        return None
    year = int(m.group(1))
    month = None
    for k, v in FR_MONTHS.items():
        if k in s:
            month = v
            break
    if month is None:
        m2 = re.search(r"dec[-\s]+(\d{2})$", s)
        if m2:
            year = 2000 + int(m2.group(1))
            month = 12
    if month is None:
        month = 12
    return pd.Timestamp(year=year, month=month, day=1)


def parse_number_md(s):
    """Parse a number possibly followed by unit (MDH, MMDH, etc.). Returns int DH if numeric."""
    s = s.replace(" ", "").replace("\u00a0", "").replace(",", "").strip()
    try:
        return int(s)
    except ValueError:
        return None


def tokenize_sm_line(line: str):
    """Tokenize a SM table line. Numbers may be split across space-separated tokens
    (French thousands). Decimal values (e.g. 0,5 or 2,1) are treated as percentages.
    Each non-decimal num token is padded to 3 digits when joining (preserves leading zeros)."""
    stripped = line.strip()
    raw = []
    for p in stripped.split():
        if not p:
            continue
        clean = p.replace("\u00a0", "")
        is_pct = clean.endswith("%")
        is_decimal = re.search(r"^\d+,\d+$", clean) is not None
        if is_pct or is_decimal:
            num_str = clean.rstrip("%").replace(",", ".")
            try:
                raw.append((float(num_str), "pct", False, ""))
            except ValueError:
                raw.append((p, "other", False, ""))
            continue
        is_neg = clean.startswith("-")
        num_str = clean.replace(",", "")
        try:
            v = float(num_str)
            raw.append((v, "num", v < 0, num_str))
        except ValueError:
            raw.append((p, "other", False, ""))
    # Combine consecutive non-negative num tokens, padding each to 3 digits
    merged = []
    buf = ""
    for entry in raw:
        val, kind, is_neg, raw_str = entry
        if kind == "num" and not is_neg:
            # Pad token string to 3 digits
            buf += raw_str.zfill(3)
        else:
            if buf:
                merged.append((int(buf), "num"))
                buf = ""
            merged.append((val, kind))
    if buf:
        merged.append((int(buf), "num"))
    return merged


def parse_sm_line_value(line: str):
    """Return (numbers, percentages) extracted from a line.

    Numbers = MDH outstanding amounts (integer)
    Percentages = variation percentages (may or may not have % sign)"""
    tokens = tokenize_sm_line(line)
    nums = [(t[0], t[1]) for t in tokens if t[1] in ("num", "pct")]
    return [n for n, k in nums if k == "num"], [n for n, k in nums if k == "pct"]


def parse_sm_table_3_1(text):
    """SM PDF table 3.1 has lines with 7 columns:
    'Crédits à l'habitat 151 389 150 586 137 371 803 14 019 0,5 10,2'
    = current, prev, year-ago, monthly_var_amount, annual_var_amount, monthly_var%, annual_var%

    The 3 large numbers (current/prev/year-ago) each have 2-3 digit groups separated by space.
    The 2 small variation amounts and 2 percentages follow.

    Strategy: tokenize, identify the 3 large numbers by position, return the FIRST one (current)."""
    results = {}

    def parse_first_number(line):
        """Extract the FIRST big number (current outstanding) from a table line.
        The line has the format: 'Label  G1 G2 G3  G4  G5  G6 G7' where G1-G3 are 1-3 digit
        groups each forming one big number, G4 is the monthly variation (often 1-2 tokens),
        G5 the annual variation (often 1-2 tokens), G6-G7 are percentages.

        We collect tokens until we see a pattern change: small number followed by 2 small
        numbers (variation + pcts)."""
        stripped = line.strip()
        # Tokenize: keep only numeric tokens
        nums = []
        for p in stripped.split():
            clean = p.replace("\u00a0", "")
            is_pct = clean.endswith("%")
            is_decimal = re.search(r"^\d+,\d+$", clean) is not None
            is_neg = clean.startswith("-")
            num_str = clean.rstrip("%").replace(",", "")
            try:
                v = float(num_str)
            except ValueError:
                continue
            nums.append((v, is_pct or is_decimal, is_neg))

        # First, strip trailing percentage and negative-amount tokens
        # Group tokens into "big numbers" by sequence of non-negative, non-pct ints
        # The big numbers are: 3 sequences of positive ints, then 2 small variation ints (1 may be negative), then 2 pcts
        big_groups = []
        cur_group = []
        for v, is_pct, is_neg in nums:
            if is_pct:
                break
            if is_neg:
                # Signifies end of large numbers, this is a variation amount
                big_groups.append(("variation", cur_group))
                cur_group = [("neg", v)]
                big_groups.append(("variation", cur_group))
                cur_group = []
            else:
                cur_group.append(int(round(v)))
                # If we've collected 3 groups of large numbers, the next ones go to variations
                if len([g for g in big_groups if g[0] == "large"]) == 3 and len(cur_group) > 0:
                    # this might be a variation — close the previous group and start new
                    # Actually if we have 3 groups of large numbers and then more positive ints,
                    # the next group is a variation amount
                    pass

        # Simpler approach: just take the first 3 "large" positive num tokens and assume
        # they're current/prev/year-ago. We have to determine the grouping.
        # If we see a signed number (-X), that's the end of large numbers.
        # If we see a percentage, that's the end.

        # Just collect positive numbers until we hit pct or negative.
        # Then assume the first 3 big groups are cols 1-3.
        big_positive = []
        for v, is_pct, is_neg in nums:
            if is_pct or is_neg:
                break
            big_positive.append(int(round(v)))

        # Now group them. Each group is separated when we see a small number (< 1000) followed by another small number.
        # Heuristic: big numbers tend to be 100k+, variations are 0-50k.
        # Split: keep accumulating until next token makes the running sum exceed some threshold? No, too fragile.

        # Simplest heuristic: the 3 big numbers each have 1-3 digit groups.
        # If we have N tokens, distribute them as 2+2+2+N-6 where N-6 are variations+pcts.
        # Variations usually have 1-2 tokens each, pcts are 1 token each.

        # Actually the simplest: assume each big number has 2-3 tokens.
        # For "151 389 150 586 137 371 803 14 019 0,5 10,2" (9 nums total):
        # Big: 151 389 | 150 586 | 137 371 = 2+2+2 = 6 tokens
        # Var: 803 | 14 019 = 1+2 = 3 tokens  (oh wait that's wrong, 14 019 is 2 tokens for one var)
        # Hmm not consistent.

        # Best heuristic: count tokens and try different splits.
        # For 7+ positive tokens before pct/neg: assume cols 1, 2, 3 each took K tokens.
        # Try K = (total - 2 small variations) / 3 = approx 2-3 each.
        # For 9 nums: (9-2-2)/3 = 1.67. Hmm.

        # Let me try: assume first number has 2 tokens, second 2, third 2, then variations.
        # If remaining is 3, it's [monthly_var_amt, annual_var_amt, monthly_var_pct] wait that's only 3 pcts...
        # Actually: 9 nums = 2+2+2+1+2+0+0? Doesn't match pcts.

        # Let me try: split big_positive into groups based on token count.
        # Common patterns:
        # 5 nums: [2, 2, 1, 0, 0] or [2, 1, 2, 0, 0] - but no pcts, only 2 cols
        # 6 nums: [2, 2, 2, 0, 0] - 3 big numbers, no variations or pcts
        # 7 nums: [2, 2, 2, 1, 0] - 3 big + 1 var + 1 pct (need 2 pcts)
        # 8 nums: [2, 2, 2, 1, 1] - 3 big + 1 var + 1 pct + 1 missing pct (or var)
        # 9 nums: [2, 2, 2, 1, 2] - 3 big + 1 var + 1 var + 2 missing pcts
        # 10 nums: [2, 2, 2, 1, 1, 1, 1] - full: 3 big + 2 var + 2 pcts (when pcts have %)

        # So a robust heuristic: the FIRST number always has at least 2 tokens (6+ digit total).
        # The 2nd and 3rd numbers also have 2 tokens each typically.
        # After the 3 big numbers (6 tokens), remaining are variations + pcts.

        if len(big_positive) >= 6:
            # First 6 tokens = 3 numbers of 2 tokens each
            a_str = str(big_positive[0]).zfill(3) + str(big_positive[1]).zfill(3)
            return int(a_str)
        elif len(big_positive) >= 3:
            # Fewer tokens, take what we have
            a_str = "".join(str(t).zfill(3) for t in big_positive[:3])
            return int(a_str)
        elif len(big_positive) >= 1:
            return big_positive[0]
        return None

    def find_line(label_pattern):
        for line in text.split("\n"):
            stripped = line.strip()
            if re.match(label_pattern, stripped, flags=re.IGNORECASE):
                return parse_first_number(stripped)
        return None

    def find_dont_line(label_pattern):
        for line in text.split("\n"):
            stripped = line.strip()
            if re.match(r"Dont\s*:?\s*" + label_pattern, stripped, flags=re.IGNORECASE):
                return parse_first_number(stripped)
        return None

    results["credits_immobiliers_MDH"] = find_line(r"Cr[eé]dits\s+immobiliers")
    results["credits_habitat_MDH"] = find_line(r"Cr[eé]dits\s+(?:à\s+)?l['']habitat")
    results["credits_promoteurs_MDH"] = find_line(r"Cr[eé]dits\s+aux\s+promoteurs\s+immobiliers")
    results["credits_equipement_MDH"] = find_line(r"Cr[eé]dits\s+(?:à\s+)?l['']\u00e9quipement")
    results["credits_consommation_MDH"] = find_line(r"Cr[eé]dits\s+(?:à\s+)?la\s+consommation")
    results["credits_treso_MDH"] = find_line(r"Comptes\s+d[eé]biteurs\s+et\s+cr[eé]dits\s+de\s+tr[eé]sorerie")
    results["credits_divers_MDH"] = find_line(r"Cr[eé]ances\s+diverses\s+sur\s+la\s+client[eè]le")
    results["credits_souffrance_MDH"] = find_line(r"Cr[eé]ances\s+en\s+souffrance")
    results["credits_bancaire_total_MDH"] = find_line(r"Cr[eé]dit\s+bancaire")
    results["credits_habitat_financement_participatif_MDH"] = find_dont_line(r"Financement\s+participatif\s+à\s+l['']habitat")
    return results


def parse_flash_pdf(text):
    """Flash PDF: 'Crédit bancaire aux ménages par nature de crédit' section.
    Format: 'Total 395,6 0,1 3,6' (current MMDH, monthly_var, annual_var)
    """
    results = {}

    def find_flash_row(label):
        # 'Habitat 256,2 0,2 3,3' (current MMDH, monthly var, annual var)
        pat = r"\b" + label + r"\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)"
        m = re.search(pat, text)
        if m:
            try:
                return float(m.group(1).replace(",", ".")) * 1000  # MMDH → MDH
            except ValueError:
                return None
        return None

    results["credits_habitat_MMDH"] = find_flash_row(r"Habitat")
    results["credits_consommation_MMDH"] = find_flash_row(r"Consommation")
    results["murabaha_habitat_MMDH"] = find_flash_row(r"Mourabaha\s+immobili[eè]re")
    results["credits_menages_total_MMDH"] = find_flash_row(r"Total\b")

    # Also try to get "Crédit bancaire" total in MMDH
    m = re.search(r"Cr[eé]dit\s+bancaire\s+\*\s+([\d,]+)", text)
    if m:
        try:
            results["credit_bancaire_total_MMDH"] = float(m.group(1).replace(",", ".")) * 1000
        except ValueError:
            pass

    return results


def main():
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    all_records = []

    for fp in pdfs:
        name = fp.name
        # Parse SM (Statistiques Monétaires) PDFs
        if any(x in name for x in ["Pub SM", "DERI_SM", "DSGD_SM", "DSGD-MSM"]):
            text = ""
            try:
                with pdfplumber.open(fp) as pdf:
                    for page in pdf.pages:
                        text += "\n" + (page.extract_text(x_tolerance=1, y_tolerance=1) or "")
            except Exception as e:
                print(f"  ERR {name}: {e}")
                continue
            date = parse_date_from_filename(name)
            data = parse_sm_table_3_1(text)
            data["date"] = date
            data["source"] = name
            data["type"] = "SM"
            all_records.append(data)
            print(f"  SM: {name[:50]:50} | {date} | habitat={data.get('credits_habitat_MDH')}")

        # Parse Flash Crédits/Dépôts PDFs
        elif "Flash" in name and ("credit" in name.lower() or "cr" in name.lower() and "dit" in name.lower()):
            text = ""
            try:
                with pdfplumber.open(fp) as pdf:
                    for page in pdf.pages:
                        text += "\n" + (page.extract_text(x_tolerance=1, y_tolerance=1) or "")
            except Exception as e:
                print(f"  ERR {name}: {e}")
                continue
            date = parse_date_from_filename(name)
            data = parse_flash_pdf(text)
            data["date"] = date
            data["source"] = name
            data["type"] = "Flash"
            all_records.append(data)
            print(f"  FLASH: {name[:50]:50} | {date} | habitat={data.get('credits_habitat_MMDH')}")

    # Save
    Path(OUT / "sm_flash_raw.json").write_text(
        json.dumps(all_records, ensure_ascii=False, indent=2, default=str)
    )
    df = pd.DataFrame(all_records).set_index("date").sort_index()
    df.to_csv(OUT / "sm_flash_credit_series.csv")
    print(f"\nSaved: {df.shape}")
    print(df[["type", "source", "credits_habitat_MDH", "credits_habitat_MMDH",
              "credits_habitat_financement_participatif_MDH", "murabaha_habitat_MMDH"]].to_string())


if __name__ == "__main__":
    main()