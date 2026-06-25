"""Debug date extraction specifically."""
from pathlib import Path
import sys
sys.path.insert(0, r"D:/ProjectforMM/IA_Finance_MA01/scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("pp", r"D:/ProjectforMM/IA_Finance_MA01/scripts/16_parse_participatives.py")
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)

for fname in [
    "Indicateurs_des_banques_participatives-Juillet_2019.pdf",
    "TDB_Indicateurs_des_banques_participatives-Janvier2020.pdf",
    "TDB_Indicateurs_des_banques_participatives-Janvier_2021.pdf",
    "TDB_Indicateurs_des_banques_participatives-Décembre_2020.pdf",
    "TDB_banques_participatives-Décembre_2019.pdf",
    "Indicateurs_des_banques_participatives-Août_2019.pdf",
    "Indicateurs_des_banques_participatives-Septembre_2019.pdf",
    "Indicateurs_des_banques_participatives-Octobre_2019.pdf",
]:
    fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf") / fname
    if not fp.exists():
        print(f"NOT FOUND: {fname}")
        continue
    d = pp.parse_fr_date_from_filename(fp.name)
    print(f"{fp.name[:60]:60} -> {d}")