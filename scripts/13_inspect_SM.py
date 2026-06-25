"""Inspect 'SM' (Revue Statistiques Monétaires) PDFs for credit time series."""
import pdfplumber
from pathlib import Path

pdfs = sorted(Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf").glob("SM*"))
pdfs += sorted(Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf").glob("Pub*"))
pdfs += sorted(Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf").glob("DSGD*"))
print(f"Total candidate PDFs: {len(pdfs)}")
for fp in pdfs[:5]:
    print(f"\n========== {fp.name} ({fp.stat().st_size:,} bytes) ==========")
    try:
        with pdfplumber.open(fp) as pdf:
            print(f"  pages: {len(pdf.pages)}")
            # Show page 1 and find any page mentioning 'habitat' or 'immobilier'
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                if any(k in text.lower() for k in ["habitat", "immobilier", "crédit"]):
                    print(f"\n  --- Page {i+1} (mentions habitat/immobilier/crédit) ---")
                    print(text[:3000])
                    if i >= 2:
                        break
    except Exception as e:
        print(f"  ERROR: {e}")