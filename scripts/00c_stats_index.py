"""Find subpage links from BAM stats index page."""
import re
from pathlib import Path

html = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_html/stats_index.html").read_text(encoding="utf-8")
body = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
body = re.sub(r"<style[\s\S]*?</style>", " ", body, flags=re.I)

tables = re.findall(r"<table[\s\S]*?</table>", body, flags=re.I)
print(f"Tables in stats_index: {len(tables)}")

links = re.findall(r'href=["\']([^"\']+)["\']', html, flags=re.I)
stat_links = sorted({l for l in links if "Statistiques" in l or "statistique" in l.lower()})
print(f"\nStatistiques/* links: {len(stat_links)}")
for l in stat_links:
    print(" -", l)

# also links mentioning 'habitat', 'cr', 'financ'
print("\nOther potentially relevant links:")
for l in sorted(set(links)):
    if any(k in l.lower() for k in ["habitat", "credit", "interet", "taux"]):
        print(" -", l)