"""PII masking helpers — all logging of personal data must go through these."""

from __future__ import annotations

import hashlib
import re

_EMAIL_RE = re.compile(r"^([^@]{1,2})([^@]*)(@.*)$")
_NON_DIGIT = re.compile(r"\D")


def mask_email(email: str) -> str:
    m = _EMAIL_RE.match(email)
    if not m:
        return "***"
    return f"{m.group(1)}{'*' * len(m.group(2))}{m.group(3)}"


def mask_phone(phone: str) -> str:
    digits = _NON_DIGIT.sub("", phone)
    return "*" * max(len(digits) - 4, 0) + digits[-4:]


def pseudonymize(value: str, salt: str = "fixture-salt") -> str:
    return hashlib.sha256((salt + value).encode()).hexdigest()[:16]
