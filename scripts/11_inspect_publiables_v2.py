"""Inspect Indicateurs publiables PDF for conventional credit time series."""
import pdfplumber
from pathlib import Path

# Find the files we just downloaded
pdfs = sorted(Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf").glob("Indicateurs*"))
print(f"Total Indicateurs PDFs: {len(pdfs)}")
print()
for fp in pdfs[:5]:
    print(f"\n========== {fp.name} ({fp.stat().st_size} bytes) ==========")
    try:
        with pdfplumber.open(fp) as pdf:
            print(f"  pages: {len(pdf.pages)}")
            for i, page in enumerate(pdf.pages[:2]):
                text = page.extract_text() or "(empty)"
                print(f"  --- Page {i+1} ---")
                print(text[:2500])
                print("...")
    except Exception as e:
        print(f"  ERROR: {e}")