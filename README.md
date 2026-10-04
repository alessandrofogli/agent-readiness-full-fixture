# Full Fixture

A deliberately complete dummy application used to exercise **every** Agent Readiness
criterion: monorepo, API service, background worker, database, feature flags, canary
deploys, DAST scanning, profiling and privacy tooling.

## Quickstart

```bash
make setup          # uv sync (installs api + worker packages)
make up             # docker compose: postgres + redis + pyroscope
make migrate        # alembic upgrade head
make test           # pytest (unit + integration)
make lint           # ruff + import-linter
make typecheck      # mypy
```

## Layout

| Path | Purpose |
|---|---|
| `packages/api` | FastAPI service (REST API, health probes, privacy endpoints) |
| `packages/worker` | background worker (nightly digest job) |
| `packages/web` | small frontend bundle (size-limited in CI) |
| `tests/` | integration tests (query-count analysis) |
| `docs/` | architecture, runbooks, feature-flag lifecycle, PII handling |
| `scripts/` | version-drift check, dead-flag audit, rollback, profiling |
