# Examples — Datasources Magdeburg

> *Deutsche Fassung:* [README.md](./README.md).

Small, self-contained snippets to get started. Deliberately **without** a build
step and without a framework — they just show how to load and visualize the
prepared JSON data.

| Snippet | Data source | What it shows |
|---|---|---|
| `python/steuereinnahmen.py` | `data/steuereinnahmen/json/` | Trade tax per year + year-over-year change (stdlib, just `print`) |
| `python/sensor_klima.py` | `data/sensor-data/json/` | Annual mean temperature over the last 10 years from monthly values (stdlib) |
| `web/steuereinnahmen.html` | `data/steuereinnahmen/json/` | Bar chart of trade tax (Chart.js via CDN) |

More (weather + rent index, with pandas/matplotlib resp. Chart.js):
see [`../data/kiss-md/examples/`](../data/kiss-md/examples/README.en.md).

## Python examples

No dependencies — Python 3 is enough:

```bash
cd examples/python
python3 steuereinnahmen.py
python3 sensor_klima.py
```

## Web example

Start a static server in the **repo root** so the relative paths to `data/`
resolve:

```bash
python3 -m http.server 8000
# → http://localhost:8000/examples/web/steuereinnahmen.html
```
