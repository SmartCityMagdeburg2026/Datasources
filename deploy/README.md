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

## Gehosteter LLM (watsonx — Granite 4 Small)

Neben einem lokalen Ollama-Modell könnt ihr im **deployten** Zustand einen von der
Orga bereitgestellten LLM nutzen (IBM Cloud / watsonx, **Granite 4 Small**) — ideal,
wenn die Team-Maschine kein eigenes Chat-Modell stemmt.

Im Deployment stehen dafür zwei Umgebungsvariablen bereit:
- `SERVER_URL` — Backend, das zu watsonx vermittelt
- `SERVER_TOKEN` — Bearer-Token

Chat-Endpoint: **POST** `${SERVER_URL}/api/llm/chat`

```bash
curl -X POST "$SERVER_URL/api/llm/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SERVER_TOKEN" \
  -d '{"messages":[{"role":"user","content":"Was ist die Grüne Zitadelle?"}]}'
# → { "response": "..." }
```

In FastAPI (z. B. in `app/main.py`):

```python
import os, httpx

SERVER_URL = os.environ["SERVER_URL"]
SERVER_TOKEN = os.environ["SERVER_TOKEN"]

async def ask_llm(prompt: str, system: str | None = None) -> str:
    messages = ([{"role": "system", "content": system}] if system else []) \
        + [{"role": "user", "content": prompt}]
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            f"{SERVER_URL}/api/llm/chat",
            headers={"Authorization": f"Bearer {SERVER_TOKEN}",
                     "Content-Type": "application/json"},
            json={"messages": messages},
        )
        r.raise_for_status()
        return r.json()["response"]
```

`messages[].role` kann `user`, `system` oder `assistant` sein. Antwort:
`{ "response": "..." }`.

**Bitte beachten:**
- **Gemeinsames Token-Budget** — die Tokens sind begrenzt und werden von allen
  Teams geteilt. Haltet Prompts kurz und vermeidet unnötige Aufrufe (kein
  Polling/Spamming).
- **Kleiner Kontext (~1024 Tokens)** — Prompt **+** ggf. RAG-Kontext **+** Antwort
  müssen zusammen in ~1024 Tokens passen. Für RAG also nur 1–2 kurze Chunks
  beilegen und den System-Prompt knapp halten.
- **Modell:** Granite 4 Small.

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
