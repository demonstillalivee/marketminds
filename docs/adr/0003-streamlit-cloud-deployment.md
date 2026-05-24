# ADR-0003 — Live deployment on Streamlit Community Cloud

**Status:** Accepted
**Date:** 2026-05-24

## Context

The project needs a clickable live URL for recruiters. Capacity won't support a full cloud setup (AWS/GCP/Render with health checks, secrets management, custom domain, etc.). GitHub Pages can't run Python.

## Decision

Deploy the **Streamlit dashboard only** to Streamlit Community Cloud:

- Free.
- Auto-deploys on push to `main`.
- Persistent URL: `marketminds.streamlit.app` (subject to availability).
- Sleeps after long idle but wakes on first request.

The FastAPI service stays in the repo as code (runnable locally via `docker compose up`). It is **not** exposed publicly. Both Streamlit and FastAPI import the same `marketminds` core package, so feature parity is automatic.

## Consequences

- Live URL exists from Sprint 10 onwards — every subsequent merge updates it. Recruiters can watch the project evolve.
- The continuous-deployment story becomes an interview talking point (see plan.md §15).
- No infrastructure-as-code in v1 (no Terraform, no Helm). Acceptable: not the goal of this project.
- No way for a recruiter to call FastAPI without cloning the repo. Acceptable: the README shows the code + has screenshots of `/docs`.

## Alternatives considered

- **HuggingFace Spaces** — supports the full stack via Docker. Slightly more flexible but less well-known to mainstream recruiters; keep as v2 option.
- **Render free tier** — sleeps aggressively and requires a credit card for some plans.
- **Fly.io free tier** — credit card required, more complex setup than the budget allows.
- **No live deployment** — significantly weaker portfolio signal; rejected.
