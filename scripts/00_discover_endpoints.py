"""
Discover the data endpoint behind BAM participatory banks page.
BKAM uses an eZ Publish / Drupal-style stack; data likely loaded via AJAX.
"""
import requests
import re
import json
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
}

URLS = {
    "participatives": "https://www.bkam.ma/Statistiques/Statistiques-sur-le-secteur-bancaire/Indicateurs-des-banques-et-fenetres-participatives",
    "credit_habitat":  "https://www.bkam.ma/Statistiques/Statistiques-sur-le-secteur-bancaire/Credit-a-l-habitat",
    "stats_index":     "https://www.bkam.ma/Statistiques/Statistiques-sur-le-secteur-bancaire",
}

OUT = Path("D:/ProjectforMM/IA_Finance_MA01/data/_raw_html")
OUT.mkdir(parents=True, exist_ok=True)


def fetch(name, url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.encoding = "utf-8"
    print(f"[{name}] {r.status_code} | bytes={len(r.text)} | {url}")
    fp = OUT / f"{name}.html"
    fp.write_text(r.text, encoding="utf-8")
    # Look for AJAX endpoints, table fragments, json data sources
    ajax = re.findall(r'(?:url|href|src|action|endpoint)\s*[:=]\s*["\']([^"\']+(?:\.json|\.xls|\.xlsx|/api/|/ajax|/load|/content|/fetch)[^"\']*)["\']', r.text, flags=re.I)
    if ajax:
        print(f"  candidate AJAX endpoints ({len(ajax)}):")
        for a in ajax[:20]:
            print(f"    - {a}")
    else:
        # try generic JSON-looking paths
        generic = re.findall(r'["\']([^"\']*(?:participat|indicateur|cr[ée]dit|stat)[^"\']*\.(?:json|xls|xlsx|csv))["\']', r.text, flags=re.I)
        if generic:
            print("  generic JSON/XLS hits:")
            for g in generic[:20]:
                print(f"    - {g}")
    return r.text


if __name__ == "__main__":
    for k, v in URLS.items():
        fetch(k, v)
    print("\nDONE. Inspect _raw_html/*.html for data tables.")