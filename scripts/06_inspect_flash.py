"""Inspect Flash crédits dépôts to see conventional credit structure."""
import pdfplumber
from pathlib import Path

fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf/Flash_crédits_dépôts_déc_2025.pdf")
print(f"=== {fp.name} ===")
with pdfplumber.open(fp) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or "(empty)"
        print(f"\n--- Page {i+1} ---")
        print(text[:3500])