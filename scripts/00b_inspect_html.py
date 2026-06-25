"""Inspect BAM page HTML to find real data source."""
import re
from pathlib import Path

html = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_html/participatives.html").read_text(encoding="utf-8")

# Strip scripts/styles
body = re.sub(r"<script[\s\S]*?</script>", "", html, flags=re.I)
body = re.sub(r"<style[\s\S]*?</style>", "", body, flags=re.I)

# All href values
links = re.findall(r'href=["\']([^"\']+)["\']', html, flags=re.I)
keywords = ["particip", "credit", "habitat", "indic", "stat", "secteur",
            "banqu", "financ", "immob", "monetair", "taux", "encours", "xls", "xlsx", "csv"]
relevant = sorted({l for l in links if any(k in l.lower() for k in keywords)})
print(f"=== relevant hrefs ({len(relevant)}) ===")
for l in relevant:
    print(" -", l)

# Look for table-related structures
print("\n=== table tags ===")
tables = re.findall(r"<table[^>]*>", body, flags=re.I)
print(f"count: {len(tables)}")
for t in tables[:5]:
    print(" ", t[:200])

# Look for any data URLs
print("\n=== data/file URLs ===")
data_urls = re.findall(r'(?:src|href|data-src)\s*=\s*["\']([^"\']*(?:\.xls|\.xlsx|\.csv|\.json|/api/|/export|/download)[^"\']*)["\']', html, flags=re.I)
for u in set(data_urls):
    print(" -", u)

# Also look for siteaccess content fetch URLs (eZ publish pattern)
print("\n=== eZ content URLs ===")
ez = re.findall(r'["\']([^"\']*/content/view/[^"\']+)["\']', html)
for u in sorted(set(ez))[:30]:
    print(" -", u)

# Look for <a> with "Cr&#233;dit" or "habitat"
print("\n=== links containing Cr\u00e9dit/habitat ===")
for l in links:
    if "habitat" in l.lower() or "cr" in l.lower():
        print(" -", l)