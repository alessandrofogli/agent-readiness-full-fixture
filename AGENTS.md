# AGENTS.md

Guidance for autonomous coding agents working in this repository.

## Setup

```bash
make setup          # uv sync — installs workspace packages and dev tools
make up             # start local services (postgres, redis, pyroscope)
```

## Build

```bash
make migrate        # apply database migrations (alembic)
docker build .      # build the API container image
```

## Test

```bash
make test           # uv run pytest -q  (unit + integration)
make lint           # ruff check + import-linter contracts
make typecheck      # mypy
```

## Development workflow

1. Create a branch, keep changes small and focused.
2. Run `make test lint typecheck` before committing.
3. Feature changes must ship behind a flag from `packages/api/src/api/flags.py`.
4. New external calls must go through `packages/api/src/api/resilience.py`
   (retry + circuit breaker).
5. Update this file when commands change — CI validates it
   (`scripts/validate_agents_md.py`).

## Conventions

- Python 3.12, ruff (line length 100), type hints on public functions.
- No secrets in code — use environment variables (see `.env.example`).
- PII must be masked in logs via `api.pii` helpers.
