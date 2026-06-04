#!/usr/bin/env python3
"""Mini-Beispiel: DWD-Klimadaten Magdeburg auswerten — nur Stdlib.

Berechnet die jährliche Durchschnittstemperatur der letzten 10 Jahre aus den
Monatswerten. Datenquelle: ../../data/sensor-data/json/klima-monat.json
(Spalte MO_TT = Monatsmittel der Lufttemperatur).
"""
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / ".." / ".." / "data" / "sensor-data" / "json" / "klima-monat.json"

ds = json.loads(DATA.read_text(encoding="utf-8"))

by_year = defaultdict(list)
for r in ds["rows"]:
    year = int(r["date"][:4])
    if r.get("MO_TT") is not None:
        by_year[year].append(r["MO_TT"])

print("Jahresmitteltemperatur Magdeburg (DWD-Station 03126)\n")
print(f"{'Jahr':<6}{'Ø Temperatur (°C)':>20}{'Monate':>8}")
for year in sorted(by_year)[-10:]:
    vals = by_year[year]
    print(f"{year:<6}{sum(vals) / len(vals):>20.2f}{len(vals):>8}")
