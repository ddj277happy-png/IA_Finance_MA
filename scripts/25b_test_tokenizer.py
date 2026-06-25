"""Test SM tokenizer."""
import sys
sys.path.insert(0, r"D:/ProjectforMM/IA_Finance_MA01/scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("pp", r"D:/ProjectforMM/IA_Finance_MA01/scripts/25_parse_sm_flash_v2.py")
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)

for line in [
    "Crédits à l'habitat 151 389 150 586 137 371 803 14 019 0,5 10,2",
    "Crédits immobiliers 219 487 220 037 207 431 -551 12 055 0,3 5,8",
]:
    print(f"Line: {line}")
    print(f"  Tokens: {pp.tokenize_sm_line(line)}")
    nums, pcts = pp.parse_sm_line_value(line)
    print(f"  Nums: {nums}")
    print(f"  Pcts: {pcts}")