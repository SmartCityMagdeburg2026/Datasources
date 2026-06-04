# Beispiele — Datasources Magdeburg

> *English version:* [README.en.md](./README.en.md).

Kleine, eigenständige Snippets als Einstieg. Bewusst **ohne** Build-Schritt und
ohne Framework — zeigen nur, wie man die aufbereiteten JSON-Daten lädt und
visualisiert.

| Snippet | Datenquelle | Was es zeigt |
|---|---|---|
| `python/steuereinnahmen.py` | `data/steuereinnahmen/json/` | Gewerbesteuer je Jahr + Veränderung zum Vorjahr (Stdlib, nur `print`) |
| `python/sensor_klima.py` | `data/sensor-data/json/` | Jahresmitteltemperatur der letzten 10 Jahre aus Monatswerten (Stdlib) |
| `web/steuereinnahmen.html` | `data/steuereinnahmen/json/` | Balkendiagramm der Gewerbesteuer (Chart.js per CDN) |

Mehr (Witterung + Mietspiegel, mit pandas/matplotlib bzw. Chart.js):
siehe [`../data/kiss-md/examples/`](../data/kiss-md/examples/README.md).

## Python-Beispiele

Keine Abhängigkeiten — Python 3 genügt:

```bash
cd examples/python
python3 steuereinnahmen.py
python3 sensor_klima.py
```

## Web-Beispiel

Statischen Server im **Repo-Root** starten, damit die relativen Pfade nach
`data/` auflösen:

```bash
python3 -m http.server 8000
# → http://localhost:8000/examples/web/steuereinnahmen.html
```
