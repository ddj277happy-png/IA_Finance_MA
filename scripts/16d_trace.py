"""Trace the date parser step by step."""
import re
from pathlib import Path

FR_MONTHS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5,
    "juin": 6, "juillet": 7, "août": 8, "aout": 8, "septembre": 9, "octobre": 10,
    "novembre": 11, "décembre": 12, "decembre": 12,
    "janv": 1, "févr": 2, "fevr": 2, "avr": 4, "juil": 7, "sept": 9, "oct": 10, "nov": 11, "déc": 12, "dec": 12,
}

name = "Indicateurs_des_banques_participatives-Juillet_2019.pdf"
s = name.lower()
s = (s.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
       .replace("ç", "c").replace("û", "u").replace("ù", "u").replace("ô", "o"))
print(f"s = {s!r}")

# Show all month matches
for k, v in FR_MONTHS.items():
    k2 = (k.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
            .replace("ç", "c").replace("û", "u").replace("ù", "u").replace("ô", "o"))
    if re.search(rf"\b{k2}\b", s) or re.search(rf"\b{k2}[-\.]\b", s):
        print(f"  MATCH: key={k!r}, normalized={k2!r}, val={v}")

# Find year
m = re.search(r"(20\d{2})", s)
print(f"year = {m.group(1) if m else None}")