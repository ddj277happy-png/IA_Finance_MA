"""
Robust parser v3 — uses line-pattern recognition instead of regex.

Strategy:
1. Walk each line of the (joined) PDF text.
2. Classify each line as either a LABEL line (no big numbers) or a VALUE line (2 big numbers + 2 percentages).
3. For each VALUE line, look at the immediately preceding label line(s) to determine category.
4. Maintain a sliding context: the most recent "Don’t : Mourabaha <category>" determines the next sub-row.
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


def parse_number(s: str):
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


# A VALUE line has 2+ big numbers (>= 4 digits each) and 2 percentages
VALUE_RE = re.compile(
    r"^(-?\d[\d\s\u00a0,]*?)\s+(-?\d[\d\s\u00a0,]*?)\s+(-?[\d,]+%?)\s+(-?[\d,]+%?)\s*$"
)


def tokenize_line(line: str):
    """Tokenize a line into ('num', int), ('pct', float), ('other', str)."""
    stripped = line.strip()
    raw_tokens = []
    parts = stripped.split()
    for p in parts:
        if not p:
            continue
        clean = p.replace(" ", "").replace("\u00a0", "").replace(",", "")
        is_pct = clean.endswith("%")
        if is_pct:
            num_str = clean.rstrip("%")
        else:
            num_str = clean
        try:
            if is_pct:
                v = float(num_str)
                raw_tokens.append(("pct", v))
            else:
                v = float(num_str)
                raw_tokens.append(("num", int(round(v))))
        except ValueError:
            raw_tokens.append(("other", p))
    return raw_tokens


def is_value_line(line: str):
    """Return True if line is: [label]? NUM(s) NUM(s) [PCT PCT]? pattern.
    Accepts both 2-pct and 1-pct and 0-pct formats (some lines have only 1 pct
    or just values with "—").
    """
    tokens = tokenize_line(line)
    if not tokens:
        return False
    # Strip leading 'other' tokens (label)
    while tokens and tokens[0][0] == "other":
        tokens.pop(0)
    if not tokens:
        return False
    # Need at least 2 num tokens (to form 2 numbers)
    n_num = sum(1 for t in tokens if t[0] == "num")
    n_pct = sum(1 for t in tokens if t[0] == "pct")
    if n_num < 2:
        return False
    # Trailing non-num/non-pct tokens (like "—") get ignored — allow trailing 'other'
    # But ALL pct must be at end
    last_pct_idx = -1
    for i, t in enumerate(tokens):
        if t[0] == "pct":
            last_pct_idx = i
    if last_pct_idx == -1:
        # No percentages — that's OK if we have lots of nums
        pass
    elif last_pct_idx < len(tokens) - 1:
        # There's something after the last pct — must be 'other' like "—" or empty
        for t in tokens[last_pct_idx + 1:]:
            if t[0] not in ("other", "pct"):
                return False
    return True


def parse_value_line(line: str):
    """Extract (a, b, mv, av) from a value line, handling French thousands separators.
    PDF format: NUM NUM monthly% annual% — so monthly var is at position -2, annual at -1.
    Tolerates 1-pct or 0-pct lines (returns None for missing vars).
    """
    tokens = tokenize_line(line)
    if not tokens:
        return None, None, None, None
    # Strip leading 'other' tokens (label)
    while tokens and tokens[0][0] == "other":
        tokens.pop(0)
    if not tokens:
        return None, None, None, None
    # Collect trailing pcts and trailing 'other' tokens
    trailing_other = []
    while tokens and tokens[-1][0] == "other":
        trailing_other.append(tokens.pop())
    # Now last 0+ tokens should be pcts
    pcts = []
    while tokens and tokens[-1][0] == "pct":
        pcts.append(tokens.pop())
    pcts.reverse()  # in original order
    mv = pcts[-2][1] if len(pcts) >= 2 else None
    av = pcts[-1][1] if len(pcts) >= 1 else None
    # The rest should be num tokens
    num_tokens = tokens
    if any(t[0] != "num" for t in num_tokens) or len(num_tokens) < 2:
        return None, None, mv, av
    n = len(num_tokens)
    half = n // 2
    if n % 2 != 0:
        first, second = num_tokens[:half+1], num_tokens[half+1:]
    else:
        first, second = num_tokens[:half], num_tokens[half:]
    a_str = "".join(str(t[1]) for t in first)
    b_str = "".join(str(t[1]) for t in second)
    try:
        a = int(a_str)
    except ValueError:
        a = None
    try:
        b = int(b_str)
    except ValueError:
        b = None
    return a, b, mv, av


# Categories we track
CATEGORIES = {
    "immobilière": "Mourabaha_immobiliere",
    "immobiliere": "Mourabaha_immobiliere",
    "automobile": "Mourabaha_automobile",
    "équipement": "Mourabaha_equipement",
    "equipement": "Mourabaha_equipement",
    "matières premières": "Mourabaha_matieres_premieres",
    "matieres premieres": "Mourabaha_matieres_premieres",
}


def extract_table(text: str):
    """Walk lines, recognize label vs value, build dict of metric -> (current, year_ago, mv, av)."""
    rows = {}

    # First: join wrapped label-only lines with the next value-only line
    lines = text.split("\n")
    joined = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        # If this line has no big number and next line does, accumulate label parts
        if not is_value_line(line):
            label_parts = [line]
            j = i + 1
            while j < len(lines):
                nxt = lines[j].strip()
                if not nxt:
                    j += 1
                    continue
                if is_value_line(nxt):
                    break
                label_parts.append(nxt)
                j += 1
            if j < len(lines) and is_value_line(lines[j].strip()):
                combined_label = " ".join(label_parts)
                joined.append(f"__LABEL__:{combined_label}")
                joined.append(f"__VALUE__:{lines[j].strip()}")
                i = j + 1
                continue
            joined.append(line)
            i += 1
        else:
            joined.append(f"__VALUE__:{line}")
            i += 1

    # Now walk joined tokens
    pending_label = ""
    pending_sous_label = ""  # for "Dont : Mourabaha xxx" trailing subcategory

    for tok in joined:
        if tok.startswith("__LABEL__:"):
            label = tok[len("__LABEL__:"):].strip()
            pending_label = label
            # If this label is a "Dont : Mourabaha <category>" pattern, remember subcategory
            m = re.search(r"Dont\s*:?\s*Mourabaha\s+(\w+)", label, re.IGNORECASE)
            if m:
                pending_sous_label = m.group(1).lower()
        elif tok.startswith("__VALUE__:"):
            val_line = tok[len("__VALUE__:"):]
            a, b, mv, av = parse_value_line(val_line)
            # Determine category from pending_label
            label = pending_label.lower()
            if "salam" in label:
                rows["Salam"] = (a, b, mv, av)
            elif "financements participatifs" in label and "mourabaha" in label and "hors marges" not in label:
                rows["Mourabaha_total"] = (a, b, mv, av)
            elif "financements participatifs" in label and "hors marges" in label:
                rows["Mourabaha_hors_marges_total"] = (a, b, mv, av)
            elif "depot" in label or "dépôt" in label:
                if "vue" in label:
                    rows["Depot_vue"] = (a, b, mv, av)
                elif "investissement" in label or "investiss" in label:
                    rows["Depot_investissement"] = (a, b, mv, av)
            elif "dont" in label and "mourabaha" in label:
                # Use subcategory
                cat = pending_sous_label
                key = CATEGORIES.get(cat, f"Mourabaha_{cat}")
                rows[key] = (a, b, mv, av)
            else:
                # Generic — try to extract category from the label
                m = re.search(r"Mourabaha\s+(\w+)", label, re.IGNORECASE)
                if m:
                    cat = m.group(1).lower()
                    key = CATEGORIES.get(cat, f"Mourabaha_{cat}")
                    rows[key] = (a, b, mv, av)
            # After consuming, only clear the short-lived pending_label/sous_label
            # Actually keep them; next VALUE will see if it's the same Dont context
            # The label reset happens when a new LABEL comes in.

    return rows


def parse_pdf(fp: Path):
    date = parse_fr_date_from_filename(fp.name)
    if date is None:
        return None
    full_text = ""
    try:
        with pdfplumber.open(fp) as pdf:
            for page in pdf.pages:
                # Use tighter tolerance so 3-digit groups like "055" keep their leading zero
                full_text += "\n" + (page.extract_text(x_tolerance=1, y_tolerance=1) or "")
    except Exception as e:
        return {"file": fp.name, "date": date, "error": str(e)}

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
    pivot = df.pivot_table(
        index="date", columns="metric",
        values="value_current_month_kDH", aggfunc="first",
    ).sort_index()

    print(f"\nWide pivot shape: {pivot.shape}")
    print(f"Date range: {pivot.index.min()} -> {pivot.index.max()}")
    print(f"\nNon-null counts:\n{pivot.count()}")

    pivot.to_csv(OUT / "participatives_wide.csv")
    df.to_csv(OUT / "participatives_raw.csv", index=False)
    meta = [{"date": str(r["date"]), "file": r["file"], "metrics": list(r["rows"].keys())} for r in results]
    Path(OUT / "participatives_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))

    print(f"\nSaved.")
    print("\nFirst 5 rows of wide pivot:")
    print(pivot.head().to_string())
    print("\nLast 5 rows:")
    print(pivot.tail().to_string())

    if skipped:
        print(f"\nSkipped ({len(skipped)}):")
        for s in skipped[:10]:
            print(f"  {s}")


if __name__ == "__main__":
    main()