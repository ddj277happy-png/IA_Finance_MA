"""Test regex."""
import re
text = """Crédit bancaire * 988,2 2,2 3,0
Total 366,8 0,2 4,6
Habitat 233,1 0,5 4,9
Mourabaha immobilière* 15,9 2,5 40,6
Consommation 55,3 -0,2 2,7
"""
label = r"Mourabaha\s+immobili[eè]re"
pat = r"\b" + label + r"\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)"
print("Pattern:", pat)
m = re.search(pat, text)
if m:
    print("Match:", m.groups())
else:
    print("No match")

# Try simpler pattern
pat2 = r"Mourabaha\s+immobili[eè]re\*?\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)"
m2 = re.search(pat2, text)
if m2:
    print("Match2:", m2.groups())