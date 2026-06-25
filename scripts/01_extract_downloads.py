"""Find all monthly PDF download URLs on each page."""
import re
from pathlib import Path

RAW = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_html")
files = ["participatives.html", "bilan_conventionnel.html",
         "credits_depots_cal.html", "credits_depots_cles.html",
         "ipai.html", "taux_debiteurs.html", "revue_monetaire.html"]

all_urls = {}  # kind -> list of (url, label)
for f in files:
    p = RAW / f
    if not p.exists():
        continue
    html = p.read_text(encoding="utf-8")
    # find all /content/download/...pdf and xlsx
    downloads = re.findall(r'href=["\']([^"\']*\/content\/download\/[^"\']*\.(?:pdf|xlsx?|csv))["\']', html, flags=re.I)
    for d in downloads:
        # extract a label from URL fragment
        label = d.rsplit("/", 1)[-1]
        # bucket
        if "banques participat" in d.lower() or "fen" in d.lower() and "participat" in d.lower():
            kind = "participatives"
        elif "bilan" in d.lower():
            kind = "bilan"
        elif "cr" in d.lower() and "dit" in d.lower() or "depot" in d.lower():
            kind = "credits_depots"
        elif "ipai" in d.lower() or "actifs immobiliers" in d.lower():
            kind = "ipai"
        elif "taux" in d.lower():
            kind = "taux"
        else:
            kind = "other"
        all_urls.setdefault(kind, []).append((d, label))

for k, urls in all_urls.items():
    print(f"\n=== {k} ({len(urls)} files) ===")
    seen = set()
    for url, label in urls:
        if label in seen: continue
        seen.add(label)
        print(f"  {label}")

# Save the URL list
import json
out = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/download_urls.json")
data = {k: [{"url": u, "label": l} for u, l in v] for k, v in all_urls.items()}
out.write_text(json.dumps(data, ensure_ascii=False, indent=2))
print(f"\nSaved to {out}")