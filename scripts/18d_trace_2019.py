"""Trace 2019-07 PDF parsing step by step."""
import sys
sys.path.insert(0, r"D:/ProjectforMM/IA_Finance_MA01/scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("pp", r"D:/ProjectforMM/IA_Finance_MA01/scripts/18_parse_v3.py")
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)

import pdfplumber
from pathlib import Path
fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf/Indicateurs_des_banques_participatives-Juillet_2019.pdf")
with pdfplumber.open(fp) as pdf:
    text = "\n".join((p.extract_text(x_tolerance=1, y_tolerance=1) or "") for p in pdf.pages)

lines = text.split("\n")
print(f"Total lines: {len(lines)}")
for line in lines:
    line = line.strip()
    if not line:
        continue
    is_v = pp.is_value_line(line)
    tag = "V" if is_v else " "
    print(f"{tag} | {line!r}")