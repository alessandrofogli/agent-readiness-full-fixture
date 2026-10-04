# Privacy Policy (fixture)

This document is a dummy policy for testing privacy-compliance tooling.

## Data we process

- Account data: email, full name, phone (optional) — stored in the `users` table.
- Usage data: aggregated request counts (no raw payloads).

## Retention

- Account data is retained while the account is active and deleted within 30 days
  of a deletion request.
- Usage aggregates are retained for 12 months.

## Your rights (GDPR/CCPA)

- **Export**: `POST /privacy/export/{user_id}` returns all stored personal data as JSON.
- **Deletion**: `POST /privacy/delete/{user_id}` removes personal data immediately.
- **Consent**: marketing emails require explicit opt-in (double opt-in flow).

## Contact

privacy@example.com
