"""Debug: try the parser on the 2019-07 PDF specifically."""
import sys
sys.path.insert(0, r"D:/ProjectforMM/IA_Finance_MA01/scripts")
from importlib import import_module
import importlib.util
spec = importlib.util.spec_from_file_location("pp", r"D:/ProjectforMM/IA_Finance_MA01/scripts/16_parse_participatives.py")
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)

from pathlib import Path
fp = Path(r"D:/ProjectforMM/IA_Finance_MA01/data/_raw_pdf/Indicateurs_des_banques_participatives-Juillet_2019.pdf")
r = pp.parse_pdf(fp)
print("Date from filename:", r["date"])
print("Keys:", list(r["rows"].keys()))
for k, v in r["rows"].items():
    print(f"  {k}: {v}")