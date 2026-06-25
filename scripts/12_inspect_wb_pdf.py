"""Extract and search the World Bank climate risks PDF for housing credit time series."""
import pdfplumber
from pathlib import Path

fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/references/attachments/world-bank-bank-al-maghrib-climate-risks-moroccan-banking-sector-2024.pdf")
print(f"Reading {fp.name} ({fp.stat().st_size:,} bytes)")
with pdfplumber.open(fp) as pdf:
    print(f"Pages: {len(pdf.pages)}")
    # Extract text from first 10 pages to see structure
    for i in range(min(15, len(pdf.pages))):
        text = pdf.pages[i].extract_text() or ""
        # Look for housing/real estate keywords
        lines = text.split("\n")
        for j, ln in enumerate(lines):
            if any(k in ln.lower() for k in ["housing", "real estate", "immobilier", "mortgage", "credit", "prêt"]):
                print(f"  p{i+1} L{j}: {ln.strip()[:150]}")
    print("\n=== table of contents / first few pages ===")
    for i in range(3):
        print(f"\n--- Page {i+1} ---")
        print((pdf.pages[i].extract_text() or "")[:2000])