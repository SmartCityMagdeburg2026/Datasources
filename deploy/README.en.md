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

## Hosted LLM (watsonx — Granite 4 Small)

Besides a local Ollama model, the **deployed** app can use an LLM provided by the
organizers (IBM Cloud / watsonx, **Granite 4 Small**) — ideal when a team's machine
can't run its own chat model.

Two environment variables are injected in the deployment:
- `SERVER_URL` — backend that mediates with watsonx
- `SERVER_TOKEN` — bearer token

Chat endpoint: **POST** `${SERVER_URL}/api/llm/chat`

```bash
curl -X POST "$SERVER_URL/api/llm/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SERVER_TOKEN" \
  -d '{"messages":[{"role":"user","content":"What is the Grüne Zitadelle?"}]}'
# → { "response": "..." }
```

In FastAPI (e.g. in `app/main.py`):

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

`messages[].role` can be `user`, `system` or `assistant`. Response:
`{ "response": "..." }`.

**Please note:**
- **Shared token budget** — tokens are limited and shared across all teams. Keep
  prompts short and avoid unnecessary calls (no polling/spamming).
- **Small context (~1024 tokens)** — prompt **+** any RAG context **+** answer must
  fit within ~1024 tokens together. For RAG, attach only 1–2 short chunks and keep
  the system prompt terse.
- **Model:** Granite 4 Small.

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
