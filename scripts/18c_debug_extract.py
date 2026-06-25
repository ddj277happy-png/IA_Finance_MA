"""Debug extract_table on a known file."""
import sys
sys.path.insert(0, r"D:/ProjectforMM/IA_Finance_MA01/scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("pp", r"D:/ProjectforMM/IA_Finance_MA01/scripts/18_parse_v3.py")
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)

import pdfplumber
from pathlib import Path

for fname in [
    "Indicateurs_des_banques_et_fenêtres_participatives_à_fin_Décembre_2025.pdf",
    "TDB_banques_participatives-Décembre_2019.pdf",
]:
    fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf") / fname
    if not fp.exists():
        continue
    with pdfplumber.open(fp) as pdf:
        text = "\n".join((p.extract_text() or "") for p in pdf.pages)
    print(f"\n=== {fname} ===")
    rows = pp.extract_table(text)
    print(f"  rows: {rows}")