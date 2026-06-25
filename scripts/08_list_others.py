"""List all files and check if there's a Bilan or Statistiques monétaires file."""
import requests, json, time
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0"}

# We didn't download "other" category. Let's grab the most useful:
# - Bilan des banques conventionnelles (annual or quarterly)
# - Revue statistiques monétaires monthly PDFs
urls = json.loads(Path(r"D:/ProjectforMM/IA_Finance_MA01/data/download_urls.json").read_text(encoding="utf-8"))
others = urls.get("other", [])
print(f"Total 'other' URLs: {len(others)}")
print("\nFirst 30 'other':")
for o in others[:30]:
    print(f"  {o['label']}")