# Datasources — Smart City Hackathon Magdeburg 2026

Daten, Dokumentation und ein Deploy-Starter für den Smart-City-Hackathon
Magdeburg (5.–6. Juni 2026), im Zuge der [Tomorrow Labs](https://tomorrowlabs.magdeburg.de/).
Bereitgestellt von der Landeshauptstadt Magdeburg und der
Otto-von-Guericke-Universität.

Data, documentation and a deploy starter for the Magdeburg Smart City Hackathon
(June 5–6, 2026). Every dataset ships prepared **JSON** next to its original
source files (`.xlsx` / `.csv` / DWD-`.txt`); each folder has its own README
(`README.md` / `README.en.md`).

> ⚠️ **Nur öffentliche Daten / Open Data mit Quellenangabe — keine
> personenbezogenen Daten** (DSGVO Art. 4). · **Use only public / open data with
> attribution — no personal data** (GDPR Art. 4). Die vollständigen offiziellen
> Hinweise der Stadt / the city's full official notes are below:
> [DE](#offizielle-hinweise-der-stadt-magdeburg) · [EN](#official-notes-city-of-magdeburg).

---

## Deutsch — Entwickler-Leitfaden

### Überblick · Datensätze & Doku

| Verzeichnis | Inhalt | Doku |
|---|---|---|
| [`data/kiss-md/`](data/kiss-md/) | **322 Stadtstatistik-Datensätze** (KISS-MD), 13 Kategorien — als JSON (`json/`) **und** Original-`xlsx` (`xlsx/`), inkl. Manifest + Beispielen | [DE](data/kiss-md/README.md) · [EN](data/kiss-md/README.en.md) |
| [`data/sensor-data/`](data/sensor-data/) | **DWD-Klimastation 03126 Magdeburg** — durchgehende Tages- (1881→) und Monatsreihen (1834→) | [DE](data/sensor-data/README.md) · [EN](data/sensor-data/README.en.md) |
| [`data/steuereinnahmen/`](data/steuereinnahmen/) | **Steuereinnahmen** (2010–2025) und **Steuersätze/Hebesätze** (1991–2026) der Stadt | [DE](data/steuereinnahmen/README.md) · [EN](data/steuereinnahmen/README.en.md) |
| [`data/mietspiegel-2024/`](data/mietspiegel-2024/) | **Mietspiegel 2024** — Nettokaltmieten je Stadtteil, nach Baualter & Wohnfläche | [DE](data/mietspiegel-2024/README.md) · [EN](data/mietspiegel-2024/README.en.md) |
| [`data/rag/`](data/rag/) | **Vorgebaute RAG-Wissensbasis** zu Magdeburg (54 Quellen → ~3.000 Chunks, Qdrant + `bge-m3` via Ollama), startklar per `docker compose` | [Quickstart](data/rag/HACKATHON_README.md) · [DE](data/rag/README.md) · [EN](data/rag/README.en.md) |
| [`live-sources/`](live-sources/) | **Katalog der Live-APIs** (Wetter, Elbe-Pegel, ÖPNV/GTFS, Luftqualität …) mit Endpunkten, Response-Formen und Integrationsmustern | [DE](live-sources/DATENQUELLEN.md) · [EN](live-sources/DATENQUELLEN.en.md) |
| [`deploy/`](deploy/) | **Deploy-Starter** (FastAPI) für die bereitgestellte IBM-Cloud-Code-Engine-Infrastruktur | [DE](deploy/README.md) · [EN](deploy/README.en.md) |
| [`examples/`](examples/) | **Kleine Snippets** (Python + Web) als Einstieg | [DE](examples/README.md) · [EN](examples/README.en.md) |

### Schnellstart

**Datensätze ansehen** — alles statisch, kein Build:

```bash
python3 -m http.server 8000        # im Repo-Root
# → http://localhost:8000/examples/web/steuereinnahmen.html
```

```bash
cd examples/python && python3 steuereinnahmen.py   # nur Python-Stdlib
```

**Eigene App deployen** — siehe [`deploy/`](deploy/): FastAPI-Starter lokal mit
`uv run uvicorn app.main:app --reload`, Deployment per Push auf `main`.

**RAG-Wissensbasis** — siehe [`data/rag/HACKATHON_README.md`](data/rag/HACKATHON_README.md):
`docker compose up -d`, Snapshot restoren, per Python abfragen.

### Aufbereitung & Reproduzierbarkeit

Die JSON-Dateien sind eingecheckt — nichts muss neu erzeugt werden. Zum
Aktualisieren liegt bei den konvertierten Quellen je ein eigenständiges
Python-Skript (nur Stdlib):

- `data/sensor-data/convert.py` — DWD-`.txt` → `json/`
- `data/steuereinnahmen/convert.py` — `.csv` (Latin-1) → `json/`

Die KISS-MD-JSONs tragen je Datensatz `labelSource`/`labelNotice`: Spalten-Labels
wurden zunächst per Sprachmodell erzeugt und anschließend manuell geprüft
(unsichere Labels = `null`). Details im [KISS-MD-README](data/kiss-md/README.md).

### Datenformate auf einen Blick

| Quelle | Original | Aufbereitet |
|---|---|---|
| KISS-MD | `xlsx` (Spalten `var1…`) | `json` mit `columns[].label`/`unit`/`role` + `rows[]` |
| Sensor (DWD) | `.txt` (`;`-getrennt, `-999`) | `json` mit Labels/Einheiten, `null` für Fehlwerte |
| Steuern | `.csv` (Latin-1, `1.234,56`) | `json` (UTF-8, echte Zahlen) |
| Mietspiegel | — | `json` |

---

## English — developer guide

### Overview · datasets & docs

| Directory | Contents | Docs |
|---|---|---|
| [`data/kiss-md/`](data/kiss-md/) | **322 city-statistics datasets** (KISS-MD), 13 categories — as JSON (`json/`) **and** original `xlsx` (`xlsx/`), incl. manifest + examples | [DE](data/kiss-md/README.md) · [EN](data/kiss-md/README.en.md) |
| [`data/sensor-data/`](data/sensor-data/) | **DWD climate station 03126 Magdeburg** — continuous daily (1881→) and monthly (1834→) series | [DE](data/sensor-data/README.md) · [EN](data/sensor-data/README.en.md) |
| [`data/steuereinnahmen/`](data/steuereinnahmen/) | **Tax revenue** (2010–2025) and **tax rates/multipliers** (1991–2026) of the city | [DE](data/steuereinnahmen/README.md) · [EN](data/steuereinnahmen/README.en.md) |
| [`data/mietspiegel-2024/`](data/mietspiegel-2024/) | **Rent index 2024** — net cold rents per district, by construction age & floor area | [DE](data/mietspiegel-2024/README.md) · [EN](data/mietspiegel-2024/README.en.md) |
| [`data/rag/`](data/rag/) | **Prebuilt RAG knowledge base** for Magdeburg (54 sources → ~3,000 chunks, Qdrant + `bge-m3` via Ollama), ready via `docker compose` | [Quickstart](data/rag/HACKATHON_README.md) · [DE](data/rag/README.md) · [EN](data/rag/README.en.md) |
| [`live-sources/`](live-sources/) | **Catalogue of live APIs** (weather, Elbe level, transit/GTFS, air quality …) with endpoints, response shapes and integration patterns | [DE](live-sources/DATENQUELLEN.md) · [EN](live-sources/DATENQUELLEN.en.md) |
| [`deploy/`](deploy/) | **Deploy starter** (FastAPI) for the provided IBM Cloud Code Engine infrastructure | [DE](deploy/README.md) · [EN](deploy/README.en.md) |
| [`examples/`](examples/) | **Small snippets** (Python + web) to get started | [DE](examples/README.md) · [EN](examples/README.en.md) |

### Quickstart

**Browse datasets** — all static, no build:

```bash
python3 -m http.server 8000        # in the repo root
# → http://localhost:8000/examples/web/steuereinnahmen.html
```

```bash
cd examples/python && python3 steuereinnahmen.py   # Python stdlib only
```

**Deploy your app** — see [`deploy/`](deploy/): run the FastAPI starter locally
with `uv run uvicorn app.main:app --reload`, deploy by pushing to `main`.

**RAG knowledge base** — see [`data/rag/HACKATHON_README.md`](data/rag/HACKATHON_README.md):
`docker compose up -d`, restore the snapshot, query from Python.

### Regeneration & reproducibility

The JSON files are committed — nothing needs to be regenerated. To update, each
converted source has a standalone Python script (stdlib only):

- `data/sensor-data/convert.py` — DWD `.txt` → `json/`
- `data/steuereinnahmen/convert.py` — `.csv` (Latin-1) → `json/`

Each KISS-MD JSON carries `labelSource`/`labelNotice`: column labels were first
generated by a language model, then manually reviewed (uncertain labels = `null`).
Details in the [KISS-MD README](data/kiss-md/README.en.md).

### Data formats at a glance

| Source | Original | Prepared |
|---|---|---|
| KISS-MD | `xlsx` (columns `var1…`) | `json` with `columns[].label`/`unit`/`role` + `rows[]` |
| Sensor (DWD) | `.txt` (`;`-separated, `-999`) | `json` with labels/units, `null` for missing |
| Taxes | `.csv` (Latin-1, `1.234,56`) | `json` (UTF-8, real numbers) |
| Rent index | — | `json` |

---

## Offizielle Hinweise der Stadt Magdeburg

> Offizieller Text der Landeshauptstadt Magdeburg — bitte unverändert beachten.

Hackathon "Smart City Magdeburg" am 5. - 6. Juni 2026 Im Zuge der
https://tomorrowlabs.magdeburg.de/

Veranstaltungsanmeldung:
https://beteiligung.sachsen-anhalt.de/portal/magdeburg/beteiligung/themen/1003460

Bitte nur öffentliche Daten/open data unter Angabe der Quelle verwenden.
- Magdeburg Mietdaten: Eigene Berechnung, Datenquelle value-marktdatenbank.
- Statisikdaten aus KISS-MD: https://statistik.magdeburg.de/KISS-MD/

**Hinweise zum Datenschutz:**
Die Verwendung von Daten im Rahmen des Smart City Hackathons ist beschränkt auf
Daten, die keinen Personenbezug enthalten nach der Definition der DSGVO (Artikel 4
DSGVO). Personenbezogene Daten sind Daten die Rückschlüsse auf eine natürliche
Person zulassen oder ermöglichen.
Der Veranstalter haftet nicht für fehlende Datenschutzkonformität etwaiger
Drittquellen.
Alle Daten aus Quellen bei denen nicht ausgeschlossen werden kann, dass ein
Personenbezug hergestellt werden kann, dürfen nicht verwendet werden. Die
Verwendung von personenbezogenen Daten und die Verwendung von Daten die
möglicherweise Personenbezug aufweisen können, ist zu unterlassen.

Ziel des Hackathons ist die Entwicklung eines Prototypen eines „Smart City"
Dashboards für die Stadt Magdeburg.
Bitte beachtet, dass ihr eure Prototypen mit Upload in das Github zur Nachnutzung
durch die Landeshauotstadt Magdeburg und weitere freigibt.

---

## Official notes (City of Magdeburg)

> Official text of the City of Magdeburg — please observe as written.

"Smart City Magdeburg" Hackathon on June 5–6, 2026, as part of the
"https://tomorrowlabs.magdeburg.de/"

Event registration:
https://beteiligung.sachsen-anhalt.de/portal/magdeburg/beteiligung/themen/1003460

Please use only public data/open data, citing the source.
- Magdeburg rental data: Own calculation, data source value-marktdatenbank.
- Statistical data from KISS-MD: https://statistik.magdeburg.de/KISS-MD/

**Data Protection Notes:**
The use of data within the scope of the Smart City Hackathon is limited to data
that does not contain any personal references as defined by the GDPR (Article 4
GDPR). Personal data is data that allows or enables conclusions to be drawn about
an individual person.
The organizer is not liable for any lack of data protection compliance by
third-party sources.
Any data from sources where it cannot be ruled out that a personal reference can
be established shall not be used. The use of personal data and the use of data
that may potentially contain personal references is not allowed.

The goal of the hackathon is to develop a prototype of a "Smart City" dashboard
for the city of Magdeburg.
Please note that by uploading your prototypes to GitHub, you are granting the City
of Magdeburg and others permission to reuse them.

---

## Lizenz & Quellen · License & sources

- KISS-MD: Stadt Magdeburg, Amt für Statistik — <https://statistik.magdeburg.de/KISS-MD/>
- Klimadaten / climate data: Deutscher Wetterdienst (DWD), frei nutzbar mit Quellenangabe (GeoNutzV)
- Steuerdaten / tax data: Landeshauptstadt Magdeburg
- Mietdaten / rent data: Eigene Berechnung, Datenquelle value-marktdatenbank
- Live-APIs: jeweilige Anbieter / respective providers (siehe [`live-sources/DATENQUELLEN.md`](live-sources/DATENQUELLEN.md))

Siehe [`LICENSE`](LICENSE) für die Lizenz dieses Repositories. Mit dem Upload eurer
Prototypen ins GitHub gebt ihr sie zur Nachnutzung frei. · See [`LICENSE`](LICENSE)
for the repository licence; uploading your prototypes to GitHub releases them for
reuse by the City of Magdeburg and others.
