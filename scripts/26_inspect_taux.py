"""Inspect Taux débiteurs PDF."""
import pdfplumber
from pathlib import Path
fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf/Taux_débiteurs_T4-2025.pdf")
with pdfplumber.open(fp) as pdf:
    for pn, page in enumerate(pdf.pages):
        text = page.extract_text(x_tolerance=1, y_tolerance=1) or ""
        if "habitat" in text.lower():
            print(f"--- Page {pn+1} ---")
            print(text[:2500])
            print()
            if pn >= 3:
                break