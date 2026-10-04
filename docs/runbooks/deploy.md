# Runbook: deploy

1. Merge to `main` (CI must be green).
2. `deploy` workflow starts automatically: canary 10% -> 50% -> 100%.
3. Watch the canary error rate for 10 minutes at each ring; if it regresses,
   run the rollback workflow.
