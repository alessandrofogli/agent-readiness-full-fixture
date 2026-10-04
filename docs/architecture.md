# Architecture

## Service flow

```
client -> FastAPI (packages/api) -> Postgres (users, orders)
                   |                     ^
                   v                     |
              Redis (queue) -> worker (packages/worker, nightly digest)
                   |
                   v
          external service (via resilience.py: retry + circuit breaker)
```

- **api** owns the HTTP surface, database models, migrations, privacy endpoints.
- **worker** consumes jobs from Redis and writes digests; it imports api's public
  modules (models, db, flags) but not its routing internals (enforced by
  import-linter contracts).
- **web** is a small bundled frontend (size budget enforced in CI).

## Deployment

Deploys are canary: 10% -> 50% -> 100% (`.github/workflows/deploy.yml`).
Rollback is one command: `make rollback` or the `rollback` workflow.
