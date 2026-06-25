"""Check raw word extraction from PDF."""
import pdfplumber
from pathlib import Path
fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf/Indicateurs_des_banques_participatives-Juillet_2019.pdf")
with pdfplumber.open(fp) as pdf:
    page = pdf.pages[0]
    text = page.extract_text(x_tolerance=1, y_tolerance=1)
    print("Lines with Depos:")
    for line in text.split("\n"):
        if "Dépôts" in line or "2055" in line or "055" in line:
            print(repr(line))
    print()
    print("=== Words in the relevant rows ===")
    words = page.extract_words(x_tolerance=1, y_tolerance=1, keep_blank_chars=False)
    for w in words:
        if "Dépôts" in w["text"] or "vue" in w["text"]:
            print(f"  text={w['text']!r:15} x0={w['x0']:.1f} x1={w['x1']:.1f} top={w['top']:.1f}")
        # Words with multiple digits around the deposits area
        if w["text"].replace(" ", "").isdigit() and 50 < w["top"] < 200:
            print(f"  num word: text={w['text']!r:12} x0={w['x0']:.1f} x1={w['x1']:.1f} top={w['top']:.1f}")