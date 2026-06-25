"""Trace the join phase."""
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

# Manually do the join
lines = text.split("\n")
joined = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    if not line:
        i += 1
        continue
    if not pp.is_value_line(line):
        label_parts = [line]
        j = i + 1
        while j < len(lines):
            nxt = lines[j].strip()
            if not nxt:
                j += 1
                continue
            if pp.is_value_line(nxt):
                break
            label_parts.append(nxt)
            j += 1
        if j < len(lines) and pp.is_value_line(lines[j].strip()):
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

print("=== JOINED TOKENS ===")
for tok in joined:
    print(repr(tok))