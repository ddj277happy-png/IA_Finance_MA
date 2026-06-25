"""Inspect Indicateurs publiables monthly bulletin and Bilan des banques conventionnelles."""
import pdfplumber
from pathlib import Path

for fp in [
    Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf/Indicateurs__janvier_2023.pdf"),
    Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf/Indicateurs_publiables_12_2021.pdf"),
    Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf/SM_DECEMBRE__2021.pdf"),
]:
    print(f"\n========== {fp.name} ==========")
    if not fp.exists():
        print("NOT FOUND")
        continue
    with pdfplumber.open(fp) as pdf:
        for i, page in enumerate(pdf.pages[:3]):
            text = page.extract_text() or "(empty)"
            print(f"\n--- Page {i+1} ---")
            print(text[:3000])