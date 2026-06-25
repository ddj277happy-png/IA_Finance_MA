"""Inspect Bilan and Crédits pages HTML for tables and downloadable data."""
import pdfplumber, re
from pathlib import Path

# Look at the Bilan page HTML
bilan = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_html/bilan_conventionnel.html").read_text(encoding="utf-8")
body = re.sub(r"<script[\s\S]*?</script>", " ", bilan, flags=re.I)
body = re.sub(r"<style[\s\S]*?</style>", " ", body, flags=re.I)

# Find tables
tables = re.findall(r"<table[\s\S]*?</table>", body, flags=re.I)
print(f"=== Bilan page tables: {len(tables)} ===")
for i, t in enumerate(tables):
    print(f"\n--- TABLE {i} (len={len(t)}) ---")
    print(t[:5000])

# Crédits et dépôts calendar page
print("\n\n\n========== Credits_depots_cal page ==========")
cpage = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_html/credits_depots_cal.html").read_text(encoding="utf-8")
body2 = re.sub(r"<script[\s\S]*?</script>", " ", cpage, flags=re.I)
body2 = re.sub(r"<style[\s\S]*?</style>", " ", body2, flags=re.I)
tables2 = re.findall(r"<table[\s\S]*?</table>", body2, flags=re.I)
print(f"Tables: {len(tables2)}")
for i, t in enumerate(tables2):
    print(f"\n--- TABLE {i} (len={len(t)}) ---")
    print(t[:3000])