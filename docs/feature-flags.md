# Feature flag lifecycle

Flags live in `packages/api/src/api/flags.py` and are evaluated by
`is_enabled(name, user_id)` (deterministic percentage rollout).

## Lifecycle

1. **Create** — add an entry to `FLAGS` with owner, description and rollout %.
2. **Roll out** — increase `rollout` gradually (10 -> 50 -> 100).
3. **Clean up** — once a flag is at 100% for 2 weeks, remove the flag and the
   dead branch. `scripts/check_flags.py` (run in CI and pre-commit) fails the
   build when a flag is defined but never referenced, and lists flags whose
   rollout is complete so the owner can remove them.

## Auditing

```bash
make flags-audit    # dead/stale flag report
```
