# Magdeburg RAG — Hackathon Quickstart

Pre-embedded Magdeburg knowledge base for the Tomorrow Labs Smart City
Hackathon (June 5–6, 2026). 54 curated sources → ~3,000 chunks, indexed in
Qdrant with `bge-m3` (1024-d, multilingual) served via Ollama.

You don't have to embed anything yourselves. The stack ships with a prebuilt
snapshot that Qdrant restores on first boot.

---

## 1. Spin it up

```bash
git clone <repo-url>
cd magdeburg-rag-sources
docker compose up -d           # qdrant + ollama
```

Pull bge-m3 once on first start (one-time ~1.2 GB download):

```bash
docker exec magdeburg-ollama ollama pull bge-m3
```

Plus whichever chat LLM you want to ground:

```bash
docker exec magdeburg-ollama ollama pull llama3.1:8b      # or mistral, qwen2.5, ...
```

Qdrant: <http://localhost:6333/dashboard>
Ollama: <http://localhost:11434>

## 2. Restore the snapshot

The snapshot file lives under `./snapshots/magdeburg/magdeburg_rag_v1.snapshot`.
Trigger restore once:

```bash
curl -X PUT 'http://localhost:6333/collections/magdeburg/snapshots/upload?priority=snapshot' \
     -H 'Content-Type:multipart/form-data' \
     -F 'snapshot=@./snapshots/magdeburg/magdeburg_rag_v1.snapshot'
```

Sanity-check the collection:

```bash
curl -s http://localhost:6333/collections/magdeburg | jq .
# expect status: "green", vectors_count: ~3000
```

## 3. Query it (Python)

```python
import requests
from qdrant_client import QdrantClient

OLLAMA = "http://localhost:11434"
qdrant = QdrantClient(url="http://localhost:6333")

def embed(text: str) -> list[float]:
    r = requests.post(f"{OLLAMA}/api/embed",
                      json={"model": "bge-m3", "input": text}, timeout=30)
    r.raise_for_status()
    return r.json()["embeddings"][0]

def search(question: str, k: int = 5, category: str | None = None):
    from qdrant_client.http.models import Filter, FieldCondition, MatchValue
    flt = None
    if category:
        flt = Filter(must=[FieldCondition(key="category",
                                          match=MatchValue(value=category))])
    return qdrant.search(
        collection_name="magdeburg",
        query_vector=embed(question),
        query_filter=flt,
        limit=k,
        with_payload=True,
    )

for hit in search("Welche Smart-City-Projekte werden in Magdeburg gefördert?"):
    p = hit.payload
    print(f"[{hit.score:.3f}] {p['title']}  →  {p['source_url']}")
    print(f"        {p['text'][:160].strip()}…\n")
```

## 4. Generate grounded answers (Ollama chat)

```python
def answer(question: str, k: int = 5):
    hits = search(question, k=k)
    context = "\n\n".join(
        f"[Quelle: {h.payload['title']} — {h.payload['source_url']}]\n{h.payload['text']}"
        for h in hits
    )
    prompt = f"""Beantworte die Frage auf Deutsch. Stütze dich AUSSCHLIESSLICH
auf die folgenden Quellen. Wenn die Quellen die Frage nicht beantworten,
sage das ehrlich. Nenne am Ende die genutzten Quellen.

Quellen:
{context}

Frage: {question}
Antwort:"""
    r = requests.post(f"{OLLAMA}/api/generate",
                      json={"model": "llama3.1:8b", "prompt": prompt, "stream": False},
                      timeout=120)
    return r.json()["response"]

print(answer("Welche Smart-City-Projekte werden in Magdeburg gefördert?"))
```

## 5. Metadata schema (Qdrant payload)

Each chunk carries:

| Field | Example | Use it for |
|---|---|---|
| `chunk_index` | `7` | position within the source doc |
| `source_id` | `isek_2030_plus_full` | matches `sources.yaml` |
| `source_id_alt` | `["ottostadt_marke"]` | deduplicated aliases |
| `category` | `strategie` | filter (see below) |
| `title` | `"ISEK 2030+ — Volldokument"` | display |
| `source_url` | `https://...` | citation link |
| `format` | `pdf` \| `html` \| `wikipedia` | UX hint |
| `page_number` | `12` (PDF only) | citation precision |
| `section_path` | `["Kapitel 4","Mobilität","Radverkehr"]` | breadcrumb |
| `content_density` | `high` \| `low` | low = boilerplate CMS pages, deprioritise |
| `language` | `de` \| `en` | UX / model selection |
| `license` | `cc-by-sa-3.0` \| `source-website` | attribution / reuse |
| `ingested_at` | ISO timestamp | refresh tracking |
| `pipeline_version` | `v1.0.0` | regression checks |
| `text` | "..." | the chunk itself |

### Categories
`strategie`, `tourismus`, `kultur`, `wikipedia`, `historisch`, `mmkt`,
`dates`, `otto`, `restaurants`

### Filter examples

```python
# Only restaurant sources
search("Italienisches Essen am Hasselbachplatz?", category="restaurants")

# Only high-density chunks (exclude landing-page boilerplate)
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
flt = Filter(must=[FieldCondition(key="content_density",
                                  match=MatchValue(value="high"))])
```

## 6. Rebuilding from scratch (optional)

If you want to add your own sources or re-embed:

```bash
# 1. Edit sources.yaml, drop new PDFs/txts into downloads/<category>/
# 2. Run the build profile
docker compose --profile build up --build embedder
# 3. The worker upserts new chunks and creates a fresh snapshot under ./snapshots/
```

Re-runs are idempotent — `chunk_id` is a content hash, so unchanged sources
don't duplicate.

## 7. Troubleshooting

| Symptom | Try |
|---|---|
| `curl localhost:6333/readyz` returns nothing | `docker compose ps`; restart with `docker compose restart qdrant` |
| `ollama pull bge-m3` hangs | mirror via host: `OLLAMA_HOST=http://localhost:11434 ollama pull bge-m3` |
| Search returns garbage | check that the snapshot was restored (`vectors_count` in `/collections/magdeburg`); re-restore from §2 |
| Port conflict (11434 / 6333) | edit `compose.yaml`, change the host-side port mapping |
| Want to use host Ollama (already running) | comment out the `ollama` service and point `OLLAMA_URL` at `host.docker.internal:11434` |

## 8. Source list

See `sources.yaml` for the full manifest. Categories and counts:

| Category | Sources | What's there |
|---|---|---|
| `strategie` | 7 | ISEK 2030+ (full + Stadtteile booklet), Kulturstrategie, Tourismuskonzept, KfW Smart Cities, LSA Digital |
| `tourismus` | 4 | 48-h Frühjahrsbroschüre, TouristCard, visit-magdeburg.de, magdeburg-tourist.de |
| `kultur` | 6 | Dom, Theater, Grüne Zitadelle, Kloster ULF, Kulturhistorisches Museum, Bruno Taut |
| `wikipedia` | 11 | Hauptartikel DE/EN, Geschichte, OvGU, FCM, SCM, Einwohnerentwicklung, Elbe, Wasserstraßenkreuz, MVB, marego |
| `historisch` | 6 | Stadtarchiv landing + Lesesaal PDF, Magdeburger Recht, Magdeburger Hochzeit, Festung, Stadtbibliothek |
| `mmkt` | 1 (post-dedupe) | Magdeburg Marketing GmbH |
| `dates` | 3 | DATEs E-Paper, Veranstaltungskalender |
| `otto` | 6 | Biographie OvG (Uni Flensburg), OvG Wiki DE/EN, Otto I., Edgitha, OvG-Zentrum |
| `restaurants` | 5 | visit-magdeburg Kulinarik, DATEs Restaurants/Bars/Sonntagsbäcker, Top-10 Sehenswürdigkeiten |

Curated specifically for Magdeburg context — see `README.md` for editorial
rationale per category.

---

Built for *Tomorrow Labs Magdeburg Smart City Hackathon*. Questions: open an
issue or ping the organiser team.
