# syntax=docker/dockerfile:1.7
# Multi-stage Dockerfile. Sprint 0: builds and starts (no real entrypoint yet).
# Real CMDs land in Sprint 8 (FastAPI) and Sprint 10 (Streamlit).

# ---------- builder ----------
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip install --upgrade pip && pip install .

# ---------- runtime ----------
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Bring in the installed package from the builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

EXPOSE 8000 8501

# Placeholder until Sprint 8/10 wire up FastAPI + Streamlit
CMD ["python", "-c", "import marketminds; print('marketminds bootstrap OK')"]
