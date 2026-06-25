"""Scan fetched pages for actual data tables and data URLs."""
import re
from pathlib import Path

RAW = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_html")

for html_file in sorted(RAW.glob("*.html")):
    html = html_file.read_text(encoding="utf-8")
    # Strip scripts/styles
    body = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    body = re.sub(r"<style[\s\S]*?</style>", " ", body, flags=re.I)
    # Count tables and table rows
    n_tables = len(re.findall(r"<table[\s\S]*?</table>", body, flags=re.I))
    n_tr = len(re.findall(r"<tr[\s\S]*?</tr>", body, flags=re.I))
    n_td = len(re.findall(r"<td[^>]*>", body, flags=re.I))
    # Look for downloadable files
    n_xlsx = len(re.findall(r"\.(?:xls|xlsx|csv)(?:[\"'\?\#]|$)", html, flags=re.I))
    n_json = len(re.findall(r"\.(?:json)(?:[\"'\?\#]|$)", html, flags=re.I))
    # Look for digit sequences that look like data values (years, big numbers)
    big_nums = len(re.findall(r">\s*[\d\s]{6,}\s*<", body))
    print(f"{html_file.name:30} | tables={n_tables:>3} tr={n_tr:>4} td={n_td:>5} | xlsx={n_xlsx} json={n_json} big_nums={big_nums}")