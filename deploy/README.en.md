# Deploy starter — FastAPI on IBM Cloud Code Engine

> *Deutsche Fassung:* [README.md](./README.md).

Minimal starting point for your hackathon app. A small **FastAPI** application
(Jinja2 dashboard with dummy data), built with **Docker** and deployed via the
provided **IBM Cloud Code Engine** infrastructure. Here you replace the dummy data
with the real datasets from [`../data/`](../data/).

## Run locally

```bash
# with uv (recommended)
uv run uvicorn app.main:app --reload      # http://localhost:8000

# or the classic way
pip install -e .
uvicorn app.main:app --reload
```

## Build the container

```bash
docker build -t md-dashboard .
docker run --rm -p 8000:8000 md-dashboard  # http://localhost:8000
```

The container listens on port **8000** (see `Dockerfile`).

## Deployment

`.github/workflows/build.yaml` deploys on every push to `main`: it calls the
Code Engine build API (`API_BASE`), polls until the build is ready, creates a new
revision and waits until the app is `ready`.

For this, the GitHub repo must have:
- **Secret** `API_TOKEN` — bearer token for the build API
- **Variable** `API_BASE` — base URL of your Code Engine instance

You'll get these values from the organizer team.

## Structure

```
app/
  main.py            FastAPI app (replace DUMMY_DATA with real data)
  templates/
    dashboard.html   Jinja2 template
Dockerfile           python:3.12-slim + uv
pyproject.toml       dependencies (fastapi, jinja2, uvicorn)
.github/workflows/   build & deploy to Code Engine
```
