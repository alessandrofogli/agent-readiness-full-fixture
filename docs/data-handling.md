# Data handling and PII

## Classification

| Field | Class | Handling |
|---|---|---|
| email | PII | masked in logs via `api.pii.mask_email` |
| full name | PII | never logged |
| phone | PII | masked via `api.pii.mask_phone` |

## Rules

- Logs must go through the masking helpers (`api.pii`); raw PII in logs is a bug.
- Test data is generated with `faker` — never copy production data into tests.
- Exports and deletions go through the `/privacy/*` endpoints (see `PRIVACY.md`).
- A CI secret scan (`detect-secrets` patterns) and the CodeQL workflow run on every push.
