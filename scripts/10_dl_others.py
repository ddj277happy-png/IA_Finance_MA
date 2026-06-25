"""Download the 'Indicateurs publiables' (other) PDFs to check for conventional credit time series."""
import requests, json, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

OUT = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf")
urls = json.loads(Path(r"D:/ProjectforMM/IA_Finance_MA01/data/download_urls.json").read_text(encoding="utf-8"))
others = urls.get("other", [])

def safe(label):
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in label)

def fetch(src):
    url = src["url"]
    if url.startswith("/"):
        url = "https://www.bkam.ma" + url
    fp = OUT / safe(src["label"])
    if fp.exists() and fp.stat().st_size > 500:
        return ("skip", src["label"])
    try:
        r = requests.get(url, headers=HEADERS, timeout=60)
        fp.write_bytes(r.content)
        return ("ok", src["label"])
    except Exception as e:
        return ("err", src["label"], str(e))

with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(fetch, s): s["label"] for s in others}
    counts = {"ok": 0, "skip": 0, "err": 0}
    errs = []
    for f in as_completed(futs):
        r = f.result()
        if r[0] == "err":
            counts["err"] += 1
            errs.append((futs[f], r[2]))
        else:
            counts[r[0]] += 1
    print(f"Results: {counts}")
    for e in errs:
        print(f"  ERR {e[0]}: {e[1]}")