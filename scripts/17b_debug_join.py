"""Debug join_wrapped_lines on a 2021-12 PDF."""
import sys
sys.path.insert(0, r"D:/ProjectforMM/IA_Finance_MA01/scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("pp", r"D:/ProjectforMM/IA_Finance_MA01/scripts/17_parse_participatives_v2.py")
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)

import pdfplumber
from pathlib import Path

fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf/Indicateurs_publiables_12_2021.pdf")
with pdfplumber.open(fp) as pdf:
    text = "\n".join((p.extract_text() or "") for p in pdf.pages)

print("=== ORIGINAL (last 20 lines) ===")
for line in text.split("\n")[-25:]:
    print(repr(line))

print("\n=== AFTER JOIN ===")
joined = pp.join_wrapped_lines(text)
for line in joined.split("\n")[-25:]:
    print(repr(line))