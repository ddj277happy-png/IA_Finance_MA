"""Find the credit-by-sector page in the SM December 2018 PDF."""
import pdfplumber
from pathlib import Path

fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf/Pub_SM_31122018_VF.pdf")
print(f"=== {fp.name} ({fp.stat().st_size:,} bytes, {fp.pages_count if hasattr(fp, 'pages_count') else '?'} pages) ===" if False else "")

with pdfplumber.open(fp) as pdf:
    print(f"Pages: {len(pdf.pages)}")
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        # Look for tables with credit by sector / habitat breakdown
        if any(p in text for p in ["Crédits à l'habitat", "Crédits à l'équipement", "Crédits immobiliers",
                                    "Ménages", "Mourabaha"]):
            print(f"\n--- Page {i+1} (matches) ---")
            print(text[:3500])
            print("..." if len(text) > 3500 else "")
            if i >= 30:  # show first few matches
                break