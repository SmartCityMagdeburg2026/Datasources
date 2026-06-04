# Deploy-Starter — FastAPI auf IBM Cloud Code Engine

> *English version:* [README.en.md](./README.en.md).

Minimaler Ausgangspunkt für eure Hackathon-App. Eine kleine **FastAPI**-Anwendung
(Jinja2-Dashboard mit Dummy-Daten), die per **Docker** gebaut und über die
bereitgestellte **IBM Cloud Code Engine**-Infrastruktur deployt wird. Hier
ersetzt ihr die Dummy-Daten durch die echten Datensätze aus [`../data/`](../data/).

## Lokal starten

```bash
# mit uv (empfohlen)
uv run uvicorn app.main:app --reload      # http://localhost:8000

# oder klassisch
pip install -e .
uvicorn app.main:app --reload
```

## Container bauen

```bash
docker build -t md-dashboard .
docker run --rm -p 8000:8000 md-dashboard  # http://localhost:8000
```

Der Container lauscht auf Port **8000** (siehe `Dockerfile`).

## Deployment

`.github/workflows/build.yaml` deployt bei jedem Push auf `main`: Es ruft die
Code-Engine-Build-API (`API_BASE`) auf, pollt bis der Build steht, erzeugt eine
neue Revision und wartet, bis die App `ready` ist.

Dafür müssen im GitHub-Repo gesetzt sein:
- **Secret** `API_TOKEN` — Bearer-Token für die Build-API
- **Variable** `API_BASE` — Basis-URL eurer Code-Engine-Instanz

Diese Werte bekommt ihr vom Orga-Team.

## Struktur

```
app/
  main.py            FastAPI-App (ersetzt die DUMMY_DATA durch echte Daten)
  templates/
    dashboard.html   Jinja2-Template
Dockerfile           python:3.12-slim + uv
pyproject.toml       Abhängigkeiten (fastapi, jinja2, uvicorn)
.github/workflows/   Build & Deploy nach Code Engine
```
