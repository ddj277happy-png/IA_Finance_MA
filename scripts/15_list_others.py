"""List ALL PDFs in 'other' category to see monthly bulletin availability."""
import json
from pathlib import Path

urls = json.loads(Path(r"D:/ProjectforMM/IA_Finance_MA01/data/download_urls.json").read_text(encoding="utf-8"))
others = urls.get("other", [])
print(f"Total 'other': {len(others)}")
for o in others:
    print(f"  {o['label']}")