# Runbook: incident

1. Page the on-call (fixture: open a `bug` issue).
2. If a recent deploy is suspected: `make rollback`.
3. Capture logs (masked PII only) and open a postmortem issue.
