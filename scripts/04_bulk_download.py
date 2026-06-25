"""Download all PDFs and Excel files we found."""
import requests, json, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

OUT = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf")
OUT.mkdir(parents=True, exist_ok=True)

urls = json.loads(Path(r"D:/ProjectforMM/IA_Finance_MA01/data/download_urls.json").read_text(encoding="utf-8"))

# Kinds we want
KEEP_KINDS = {"participatives", "ipai", "taux", "credits_depots"}

def safe(label):
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in label)

def fetch_one(src):
    url = src["url"]
    if url.startswith("/"):
        url = "https://www.bkam.ma" + url
    fp = OUT / safe(src["label"])
    if fp.exists() and fp.stat().st_size > 500:
        return ("skip", src["label"], fp.stat().st_size)
    try:
        r = requests.get(url, headers=HEADERS, timeout=60)
        fp.write_bytes(r.content)
        return ("ok", src["label"], len(r.content))
    except Exception as e:
        return ("err", src["label"], str(e))

# Build flat list
tasks = []
for kind in KEEP_KINDS:
    for src in urls.get(kind, []):
        tasks.append((kind, src))

print(f"Total tasks: {len(tasks)}")

with ThreadPoolExecutor(max_workers=6) as ex:
    futures = {ex.submit(fetch_one, s): (k, s["label"]) for k, s in tasks}
    counts = {"ok": 0, "skip": 0, "err": 0}
    errs = []
    for f in as_completed(futures):
        status, label, size = f.result()
        counts[status] += 1
        if status == "err":
            errs.append((futures[f][0], label, size))
    print(f"\nResults: {counts}")
    if errs:
        print("\nErrors:")
        for k, l, e in errs:
            print(f"  [{k}] {l}: {e}")

print(f"\nFiles in {OUT}:")
for fp in sorted(OUT.glob("*")):
    print(f"  {fp.name} ({fp.stat().st_size} bytes)")