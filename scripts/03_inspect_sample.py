"""Extract text from the sample participatory PDF."""
import pdfplumber
from pathlib import Path

fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf/SAMPLE_Indicateurs_des_banques_et_fenêtres_participatives_à_fin_Décembre_2025.pdf")
print(f"Reading {fp.name} ({fp.stat().st_size} bytes)\n")

with pdfplumber.open(fp) as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"\n========= PAGE {i+1} =========")
        text = page.extract_text() or "(no text)"
        print(text)