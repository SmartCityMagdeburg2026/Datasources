#!/usr/bin/env python3
"""Mini-Beispiel: Steuereinnahmen Magdeburg laden und auswerten — nur Stdlib.

Zeigt die Gewerbesteuer-Einnahmen je Jahr und die Veränderung zum Vorjahr.
Datenquelle: ../../data/steuereinnahmen/json/steuereinnahmen-2010-2025.json
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / ".." / ".." / "data" / "steuereinnahmen" / "json" / "steuereinnahmen-2010-2025.json"

ds = json.loads(DATA.read_text(encoding="utf-8"))

# Zeilen nach Jahr aufsteigend sortieren
rows = sorted(ds["rows"], key=lambda r: r["jahr"])

print(f"{ds['title']}\n")
print(f"{'Jahr':<6}{'Gewerbesteuer (EUR)':>22}{'Δ Vorjahr':>14}")
prev = None
for r in rows:
    val = r["gewerbesteuer"]
    delta = "" if prev is None or val is None else f"{(val - prev) / prev * 100:+.1f} %"
    print(f"{r['jahr']:<6}{val:>22,.2f}{delta:>14}")
    if val is not None:
        prev = val
