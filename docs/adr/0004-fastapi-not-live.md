# ADR-0004 — FastAPI lives in-repo, not in production

**Status:** Accepted
**Date:** 2026-05-24

## Context

The plan calls for both a FastAPI service AND a Streamlit dashboard. Streamlit Community Cloud (see ADR-0003) hosts the Streamlit app and runs Python in-process, but does not expose arbitrary HTTP servers. Hosting FastAPI separately requires a second deployment target.

## Decision

**The Streamlit dashboard calls the `marketminds` core package directly, in-process.** It does NOT make HTTP calls to FastAPI.

FastAPI exists in the repo at `src/marketminds/api/` and is fully wired (endpoints, pydantic schemas, OpenAPI docs at `/docs`). It is runnable locally via `docker compose up` and is included in CI (tested, type-checked). It is **not** deployed publicly.

## Why have FastAPI at all then?

- Recruiters reading the code see a real API surface with schemas, endpoints, error handling, OpenAPI docs.
- It demonstrates API design + pydantic validation + FastAPI patterns — skills that don't surface in a Streamlit-only codebase.
- Local `docker compose` runs both for development; screenshots of `/docs` go in the README.

## Consequences

- Some code duplication: Streamlit and FastAPI each have their own input handling. Acceptable; both call into the same core package, so business logic stays in one place.
- The live URL doesn't include API endpoints — the README compensates with code + screenshots.
- Tests cover both layers, including FastAPI endpoint tests via `TestClient`.

## Alternatives considered

- **Deploy FastAPI somewhere too** — doubles the deployment surface; budget doesn't allow.
- **Drop FastAPI entirely** — loses a significant signal for backend/DevOps roles.
- **Run FastAPI inside the Streamlit process via subprocess** — fragile, no real benefit.
