"""Debug is_value_line and extract_table on a known file."""
import sys
sys.path.insert(0, r"D:/ProjectforMM/IA_Finance_MA01/scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("pp", r"D:/ProjectforMM/IA_Finance_MA01/scripts/18_parse_v3.py")
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)

import pdfplumber
from pathlib import Path

for fname in [
    "Indicateurs_publiables_12_2021.pdf",
    "TDB_Indicateurs_des_banques_participatives-Décembre_2020.pdf",
    "Indicateurs_des_banques_et_fenêtres_participatives_à_fin_Décembre_2025.pdf",
]:
    fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf") / fname
    if not fp.exists():
        print(f"NOT FOUND: {fname}")
        continue
    with pdfplumber.open(fp) as pdf:
        text = "\n".join((p.extract_text() or "") for p in pdf.pages)
    print(f"\n=== {fname} ===")
    # Check is_value_line on each line
    lines = text.split("\n")
    n_value = sum(1 for l in lines if pp.is_value_line(l.strip()))
    n_label = sum(1 for l in lines if l.strip() and not pp.is_value_line(l.strip()))
    print(f"  total lines: {len(lines)}, value lines: {n_value}, label lines: {n_label}")
    # First few value lines
    vals = [l.strip() for l in lines if pp.is_value_line(l.strip())][:6]
    for v in vals:
        print(f"    VAL: {v!r}")
        a, b, mv, av = pp.parse_value_line(v)
        print(f"      parsed: a={a}, b={b}, mv={mv}, av={av}")
    # Run extract_table
    rows = pp.extract_table(text)
    print(f"  rows found: {len(rows)}")
    for k, v in rows.items():
        print(f"    {k}: {v}")