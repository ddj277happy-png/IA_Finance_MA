"""Parse BAM 'Historique des décisions' HTML → policy rate CSV."""
import re
from pathlib import Path
import pandas as pd

HTML = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_html/hist_decisions.html")
OUT = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_intermediate")

html = HTML.read_text(encoding="utf-8")
body = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
body = re.sub(r"<style[\s\S]*?</style>", " ", body, flags=re.I)

tables = re.findall(r"<table[\s\S]*?</table>", body, flags=re.I)
t0 = tables[0]
rows = re.findall(r"<tr[\s\S]*?</tr>", t0, flags=re.I)

records = []
for r in rows:
    cells = re.findall(r"<t[dh][^>]*>([\s\S]*?)</t[dh]>", r, flags=re.I)
    cells_clean = [re.sub(r"<[^>]+>", " ", c).strip().replace("&nbsp;", "").replace("\xa0", "") for c in cells]
    if len(cells_clean) < 4:
        continue
    date_str, taux_str, reserve_str, remu_str = cells_clean[:4]
    if not date_str or "/" not in date_str:
        continue
    # Parse date dd/mm/yyyy
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", date_str)
    if not m:
        continue
    d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
    # Parse rate
    def parse_pct(s):
        s = s.replace(",", ".").replace("%", "").strip()
        try:
            return float(s)
        except ValueError:
            return None
    records.append({
        "date": pd.Timestamp(year=y, month=mo, day=d),
        "taux_directeur_pct": parse_pct(taux_str),
        "reserve_obligatoire_pct": parse_pct(reserve_str),
        "remuneration_reserve_pct": parse_pct(remu_str),
    })

df = pd.DataFrame(records).set_index("date").sort_index()
print(f"Shape: {df.shape}")
print(f"Range: {df.index.min()} -> {df.index.max()}")
print(df.head(15))
print("...")
print(df.tail(15))

df.to_csv(OUT / "policy_rate_history.csv")
print(f"\nSaved: {OUT / 'policy_rate_history.csv'}")