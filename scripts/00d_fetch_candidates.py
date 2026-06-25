"""Fetch all candidate BAM pages that may contain our series."""
import requests, time
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
}

URLS = [
    # Participatory finance (already have, re-fetch for cleanliness)
    ("participatives",      "https://www.bkam.ma/Statistiques/Statistiques-sur-le-secteur-bancaire/Indicateurs-des-banques-et-fenetres-participatives"),
    # Conventional banks aggregate balance sheet
    ("bilan_conventionnel", "https://www.bkam.ma/Statistiques/Statistiques-sur-le-secteur-bancaire/Bilans-agreges/Bilan-des-banques-conventionnelles"),
    # Credits and deposits time series (from calendar)
    ("credits_depots_cal",  "https://www.bkam.ma/Statistiques/Calendrier/Credits-et-depots-bancaires"),
    # Credits and deposits time series (from national key figures)
    ("credits_depots_cles", "https://www.bkam.ma/Statistiques/Chiffres-cles-de-l-economie-nationale/Credits-et-depots-bancaires"),
    # Housing price index (IPAI)
    ("ipai",                "https://www.bkam.ma/Statistiques/Prix/Indice-des-prix-des-actifs-immobiliers"),
    # Quarterly lending rate survey
    ("taux_debiteurs",      "https://www.bkam.ma/Statistiques/Enquetes/Resultats-de-l-enquete-trimestrielle-sur-les-taux-debiteurs"),
    # Policy rate decisions history
    ("hist_decisions",      "https://www.bkam.ma/Politique-monetaire/Cadre-strategique/Decision-de-la-politique-monetaire/Historique-des-decisions"),
    # Monthly monetary statistics review (might also have credit breakdown)
    ("revue_monetaire",     "https://www.bkam.ma/Statistiques/Statistiques-monetaires/Revue-statistiques-monetaires"),
]

OUT = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_html")
OUT.mkdir(parents=True, exist_ok=True)

for name, url in URLS:
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.encoding = "utf-8"
        fp = OUT / f"{name}.html"
        fp.write_text(r.text, encoding="utf-8")
        print(f"[{name:25}] {r.status_code} | {len(r.text):>8} bytes | {url}")
    except Exception as e:
        print(f"[{name:25}] ERROR {e}")
    time.sleep(0.4)

print("\nDone.")