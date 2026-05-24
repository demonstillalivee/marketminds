# ADR-0002 — No database in v1

**Status:** Accepted
**Date:** 2026-05-24

## Context

Portfolio analytics could justify a database (cache prices, store portfolios, track user history). Adding one means: schema design, migrations, hosting, connection pooling, secrets management — all of which compete for the ~1.5 hrs/week budget.

## Decision

**v1 is stateless.** No database. Specifically:

- yfinance prices are cached to local CSV files (`~/.market_minds_cache/`).
- Portfolios are not persisted across sessions — the user re-enters tickers/weights on each visit.
- No auth, no users, no history.

## Consequences

- Live deploy on Streamlit Community Cloud stays simple — no DB to provision.
- CSV cache is per-instance — on Streamlit Cloud the cache lives in ephemeral storage, which is fine for v1 (re-fetches on cold boot).
- Cannot show "trends over time" features. Acceptable.
- Saves several sprints of work.

## Alternatives considered

- **SQLite** — file-based, no server needed. Still requires schema design + migrations + the test surface. Deferred to v2.
- **Postgres + Alembic** — too much for v1.
- **Redis cache** — overkill; CSV is fine for daily-close data.

## When to revisit

If v2 includes user accounts, portfolio history, or backtesting — pick this back up. Until then, stateless wins.
