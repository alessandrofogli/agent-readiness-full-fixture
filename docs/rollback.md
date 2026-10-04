# Rollback

Rollback is one command and does not require investigation:

```bash
make rollback                 # roll back to previous known-good revision
./scripts/rollback.sh v1.2.3  # or pin a specific revision
```

Or from GitHub Actions: **Actions -> rollback -> Run workflow**.

## Procedure

1. Run the rollback (above). Canary traffic moves back first.
2. Verify `/health` and the error-rate dashboard.
3. File an incident issue with the failed revision; the deploy is blocked until
   the cause is understood.
