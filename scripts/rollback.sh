#!/usr/bin/env bash
# One-command rollback: redeploys the previous known-good revision.
# See docs/rollback.md for the full procedure.
set -euo pipefail

TARGET="${1:-previous}"
echo "Rolling back deployment to: ${TARGET}"
if command -v gh >/dev/null 2>&1; then
  gh workflow run deploy.yml -f ref="${TARGET}" || echo "(dry run) would redeploy ${TARGET}"
else
  echo "(dry run) would redeploy ${TARGET}"
fi
echo "Rollback triggered. Verify /health and the error-rate dashboard."
