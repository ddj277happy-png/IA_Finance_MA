"""Inspect an old participatory PDF (Jul 2019) to verify format consistency."""
import pdfplumber
from pathlib import Path

fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf/Indicateurs_des_banques_participatives-Juillet_2019.pdf")
print(f"=== {fp.name} ===")
with pdfplumber.open(fp) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or "(empty)"
        print(f"\n--- Page {i+1} ---")
        print(text[:2500])