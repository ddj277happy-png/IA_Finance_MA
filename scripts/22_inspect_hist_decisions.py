"""Parse BAM 'Historique des décisions' HTML page for policy rate history."""
import re
import json
from pathlib import Path
import pandas as pd

HTML = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_html/hist_decisions.html")
OUT = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate")

html = HTML.read_text(encoding="utf-8")

# Strip script/style
body = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
body = re.sub(r"<style[\s\S]*?</style>", " ", body, flags=re.I)

# Find tables
tables = re.findall(r"<table[\s\S]*?</table>", body, flags=re.I)
print(f"Tables found: {len(tables)}")
for i, t in enumerate(tables):
    print(f"  Table {i}: {len(t)} chars")

# Show first table
if tables:
    t0 = tables[0]
    # Extract rows
    rows = re.findall(r"<tr[\s\S]*?</tr>", t0, flags=re.I)
    print(f"\nFirst table rows: {len(rows)}")
    for r in rows[:10]:
        cells = re.findall(r"<t[dh][^>]*>([\s\S]*?)</t[dh]>", r, flags=re.I)
        cells_clean = [re.sub(r"<[^>]+>", " ", c).strip() for c in cells]
        print(" | ".join(cells_clean))