# Market Minds

> Modern Python portfolio analytics — FastAPI + Streamlit, deployed live, tested, and CI/CD'd.

🚀 **Live demo:** *coming Sprint 10 — `marketminds.streamlit.app`*

[![CI](https://github.com/demonstillalivee/marketminds/actions/workflows/ci.yml/badge.svg)](https://github.com/demonstillalivee/marketminds/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What it does

Input a portfolio (tickers + weights). Get back risk-return metrics — Sharpe, Beta, Alpha, volatility — plus a Markowitz mean-variance optimized re-weighting, benchmarked against Nifty 50.

Built end-to-end as a demonstration of modern Python product delivery: type-checked, tested, containerized, and continuously deployed.

## Architecture

```
Streamlit Cloud  ──►  Streamlit Dashboard  ──►  marketminds (core engine)
                                                        ▲
                                       local Docker ──► │ ◄── FastAPI (showcase)
```

See [`docs/adr/`](docs/adr/) for the why behind each major call.

## Quickstart (local)

```bash
git clone https://github.com/demonstillalivee/marketminds.git
cd marketminds
docker compose up
# Streamlit:  http://localhost:8501
# FastAPI:    http://localhost:8000/docs
```

## Development

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"

# Run the toolchain (same as CI)
ruff check .
ruff format --check .
mypy src/
pytest --cov=marketminds
```

## Project status

This is being built in **public, sprint by sprint**, at ~1.5 hrs/week. See [`docs/velocity.md`](docs/velocity.md) for the running log, [`docs/retros/`](docs/retros/) for weekly retros, and the [project plan](https://github.com/demonstillalivee/marketminds#) for the full roadmap.

| Sprint | Goal | Status |
|---|---|---|
| 0 | Repo skeleton + green CI | ✅ |
| 1–14 | Build out the engine, API, UI | 🏗 |
| 15 | Live deploy + README polish | ⏳ |

## Disclaimer

Not financial advice. Daily-close data only. Educational portfolio project — not for trading decisions.

## License

MIT — see [LICENSE](LICENSE).
