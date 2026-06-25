"""Download one sample PDF to inspect structure."""
import requests, json
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

OUT = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf")
OUT.mkdir(parents=True, exist_ok=True)

# Pick: most recent + an early one
samples = [
    "https://www.bkam.ma/content/download/8644388/12345678/Indicateurs%20des%20banques%20et%20fen%C3%AAtres%20participatives%20%C3%A0%20fin%20D%C3%A9cembre%202025.pdf",
]

# Use the actual URLs from our list
urls = json.loads(Path(r"D:/ProjectforMM/IA_Finance_MA01/data/download_urls.json").read_text(encoding="utf-8"))

# Try the most recent participatory
part = urls["participatives"][0]   # most recent
ipai = urls["ipai"][0]
print(f"Fetching sample:\n  part: {part['url']}\n  ipai: {ipai['url']}")

for src in [part, ipai]:
    url = src["url"]
    if url.startswith("/"):
        url = "https://www.bkam.ma" + url
    r = requests.get(url, headers=HEADERS, timeout=60)
    safe = src["label"].replace("/", "_").replace(" ", "_")
    fp = OUT / f"SAMPLE_{safe}"
    fp.write_bytes(r.content)
    print(f"  -> {fp.name} | {len(r.content)} bytes | {r.status_code}")