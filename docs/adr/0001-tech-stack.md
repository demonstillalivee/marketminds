# ADR-0001 — Tech stack

**Status:** Accepted
**Date:** 2026-05-24

## Context

Market Minds v2 is a rebuild of a college project as a recruiter-facing portfolio piece for DevOps + SDET roles. Capacity is ~1.5 hrs/week over ~15 weeks. The output needs to be live and runnable, with credible CI/CD + testing signals.

## Decision

The stack is:

- **Python 3.11+** — primary language; finance/data ecosystem is rich here.
- **Ruff** for lint + format — replaces flake8/isort/black-equivalent; the modern default.
- **Mypy** for static typing — non-strict at first, tightened to strict in Sprint 14.
- **Pytest + pytest-cov + pytest-mock** — standard test stack.
- **Pandas / NumPy / yfinance** for data + analytics.
- **scipy.optimize** for Markowitz mean-variance optimization.
- **FastAPI + pydantic v2 + uvicorn** for the API surface (showcased in repo, runnable via docker compose).
- **Streamlit + Plotly** for the dashboard (live on Streamlit Community Cloud).
- **Docker** + **docker-compose** for local orchestration.
- **GitHub Actions** for CI.
- **Streamlit Community Cloud** for live deployment.

## Consequences

- Two parallel surfaces (FastAPI + Streamlit) sharing one core package. Slightly more files, but recruiters see API design AND a live UI without paying for cloud hosting.
- `mypy --strict` deferred to Sprint 14 — adoption cost too high in early sprints.
- No DB in v1 (see ADR-0002).
- Live deployment via Streamlit Cloud means FastAPI is not exposed publicly (see ADR-0004).

## Alternatives considered

- **Flask** instead of FastAPI — rejected; no async, no auto-OpenAPI.
- **Poetry** instead of setuptools — rejected; modern setuptools + uv is simpler.
- **React UI** instead of Streamlit — rejected; budget doesn't support frontend tooling overhead.
- **Kubernetes / live cloud** — rejected; massive overkill for one container.
