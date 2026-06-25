"""
Robust parser v4 — no line joining, just look at each value line and its
immediate preceding label line(s).
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


def tokenize_line(line: str):
    stripped = line.strip()
    raw = []
    for p in stripped.split():
        if not p:
            continue
        clean = p.replace(" ", "").replace("\u00a0", "").replace(",", "")
        is_pct = clean.endswith("%")
        num_str = clean.rstrip("%")
        try:
            if is_pct:
                raw.append(("pct", float(num_str)))
            else:
                raw.append(("num", int(round(float(num_str)))))
        except ValueError:
            raw.append(("other", p))
    return raw


def is_value_line(line: str):
    """True if line has 2+ num tokens and 0-2 pct tokens at the end (in either order)."""
    tokens = tokenize_line(line)
    if not tokens:
        return False
    # Strip leading 'other' tokens
    while tokens and tokens[0][0] == "other":
        tokens.pop(0)
    if not tokens:
        return False
    n_num = sum(1 for t in tokens if t[0] == "num")
    if n_num < 2:
        return False
    return True


def parse_value_line(line: str):
    """Extract (year_ago, current, mv, av). PDF format: NUM NUM monthly% annual%
    where the FIRST big number is the YEAR-AGO value (column 1) and the SECOND
    is the CURRENT-month value (column 2, matching the PDF title date).

    Tries both possible splits for the num tokens and picks the one where
    the two resulting numbers have the smallest magnitude ratio.

    Each num token is padded to 3 digits when joined (handles French thousands
    formatting where leading zeros in groups like '055' get lost)."""
    tokens = tokenize_line(line)
    if not tokens:
        return None, None, None, None
    while tokens and tokens[0][0] == "other":
        tokens.pop(0)
    trailing_other = []
    while tokens and tokens[-1][0] == "other":
        trailing_other.append(tokens.pop())
    pcts = []
    while tokens and tokens[-1][0] == "pct":
        pcts.append(tokens.pop())
    pcts.reverse()
    mv = pcts[-2][1] if len(pcts) >= 2 else None
    av = pcts[-1][1] if len(pcts) >= 1 else None
    num_tokens = tokens
    if any(t[0] != "num" for t in num_tokens) or len(num_tokens) < 2:
        return None, None, mv, av
    n = len(num_tokens)
    padded = [str(t[1]).zfill(3) for t in num_tokens]
    candidates = []
    for k in range(1, n):
        first_str = "".join(padded[:k]).lstrip("0") or "0"
        second_str = "".join(padded[k:]).lstrip("0") or "0"
        try:
            a = int(first_str)
            b = int(second_str)
        except ValueError:
            continue
        if b <= 0:
            continue
        ratio = max(a, b) / max(min(a, b), 1)
        candidates.append((ratio, k, a, b))
    if not candidates:
        return None, None, mv, av
    candidates.sort()
    _, _, year_ago, current = candidates[0]
    return year_ago, current, mv, av


def categorize(line: str):
    """Determine which metric a value line corresponds to, from the line's own content.
    Returns (category, sub_category) where sub_category is for 'Dont : Mourabaha X'."""
    ll = line.lower()
    if "salam" in ll:
        return "Salam", None
    if "depot" in ll or "dépôt" in ll:
        if "investissement" in ll:
            return "Depot_investissement", None
        if "vue" in ll:
            return "Depot_vue", None
        return "Depot_other", None
    # Mourabaha total
    if ("financements participatifs par mourabaha" in ll or "financements participatifs par mourabaha hors" in ll) and "dont" not in ll:
        if "hors" in ll:
            return "Mourabaha_hors_marges_total", None
        return "Mourabaha_total", None
    # Don't breakdown
    m = re.search(r"dont\s*:?\s*mourabaha\s+(\w+)", ll)
    if m:
        cat = m.group(1)
        return "Mourabaha_sub", cat
    # Generic Mourabaha
    m = re.search(r"mourabaha\s+(\w+)", ll)
    if m:
        return "Mourabaha_sub", m.group(1)
    return None, None


SUB_LABELS = {
    "immobilière": "immobiliere",
    "immobiliere": "immobiliere",
    "automobile": "automobile",
    "équipement": "equipement",
    "equipement": "equipement",
    "matières": "matieres_premieres",
    "matieres": "matieres_premieres",
}


SUB_WORDS = ["immobilière", "automobile", "équipement", "matières premières"]


def normalize_wrapped(text: str) -> str:
    """Join wrapped label/value lines.

    Rules:
    1. Multiple consecutive label-only lines get joined into one combined label.
    2. A combined label line followed by a value line → join into "LABEL: VALUE" on one line.
    3. A value line followed by a single label-only line that contains a subcategory
       word (e.g. "immobilière") → join them as "VALUE: CATEGORY" so the category
       appears WITH the value line.
    """
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        # Is this a value line?
        if is_value_line(line):
            # Look ahead for any non-empty next line that could be a subcategory label
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                nxt = lines[j].strip()
                nxt_low = nxt.lower()
                is_subword = nxt_low in [w.lower() for w in SUB_WORDS]
                if is_subword:
                    out.append(f"{line} __CAT__:{nxt}")
                    i = j + 1
                    continue
            out.append(line)
            i += 1
            continue

        # Label-only line: accumulate consecutive label-only lines
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
            out.append(f"{lines[j].strip()} __LABEL__:{combined_label}")
            i = j + 1
        else:
            for p in label_parts:
                out.append(p)
            i = j
    return "\n".join(out)


def extract_table(text: str):
    rows = {}
    text = normalize_wrapped(text)
    lines = text.split("\n")
    section = "main"  # current section context

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        # Strip __LABEL__:... and __CAT__:... tags
        trailing_label = ""
        trailing_cat = ""
        m = re.search(r"\s+__LABEL__:(.*)$", line)
        if m:
            trailing_label = m.group(1)
            line = line[:m.start()]
        m2 = re.search(r"\s+__CAT__:(.*)$", line)
        if m2:
            trailing_cat = m2.group(1).lower()
            line = line[:m2.start()]

        # Update section based on trailing label (which describes the next/current value)
        if trailing_label:
            ll = trailing_label.lower()
            if "financements participatifs par mourabaha hors" in ll:
                section = "hors_marges"
            elif "financements participatifs par mourabaha" in ll:
                section = "main"

        if not is_value_line(line):
            continue

        cat, sub = categorize(line)
        # Augment with trailing_cat / trailing_label if categorize missed
        if cat is None and trailing_cat:
            cat = "Mourabaha_sub"
            sub = trailing_cat
        if cat is None and trailing_label:
            cat2, sub2 = categorize(trailing_label)
            if cat2:
                cat, sub = cat2, sub2

        if cat is None:
            continue

        year_ago, current, mv, av = parse_value_line(line)
        suffix = "_hors_marges" if section == "hors_marges" else ""

        if cat == "Salam":
            rows["Salam"] = (year_ago, current, mv, av)
        elif cat == "Depot_vue":
            rows["Depot_vue"] = (year_ago, current, mv, av)
        elif cat == "Depot_investissement":
            rows["Depot_investissement"] = (year_ago, current, mv, av)
        elif cat == "Mourabaha_total":
            key = "Mourabaha_total" if section == "main" else "Mourabaha_hors_marges_total"
            rows[key] = (year_ago, current, mv, av)
        elif cat == "Mourabaha_hors_marges_total":
            rows["Mourabaha_hors_marges_total"] = (year_ago, current, mv, av)
        elif cat == "Mourabaha_sub":
            sub_norm = SUB_LABELS.get(sub, sub)
            rows[f"Mourabaha_{sub_norm}{suffix}"] = (year_ago, current, mv, av)
    return rows


def parse_pdf(fp: Path):
    date = parse_fr_date_from_filename(fp.name)
    if date is None:
        return None
    full_text = ""
    try:
        with pdfplumber.open(fp) as pdf:
            for page in pdf.pages:
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
        for key, (year_ago, current, mv, av) in r["rows"].items():
            rows.append({
                "date": r["date"],
                "file": r["file"],
                "metric": key,
                "value_current_month_kDH": current,
                "value_year_ago_kDH": year_ago,
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
    print("\n=== Sample by year-end (Dec) ===")
    dec_rows = pivot[pivot.index.month == 12]
    print(dec_rows.to_string())

    if skipped:
        print(f"\nSkipped ({len(skipped)}):")
        for s in skipped[:15]:
            print(f"  {s}")


if __name__ == "__main__":
    main()