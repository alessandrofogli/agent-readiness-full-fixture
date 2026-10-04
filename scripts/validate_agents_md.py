#!/usr/bin/env python3
"""Validate that AGENTS.md stays consistent with the repository.

Checks:
- AGENTS.md exists at the repo root and is substantive (>100 chars)
- every `make <target>` mentioned in AGENTS.md exists in the Makefile
- the documented test command (`uv run pytest`) is configured in pyproject.toml
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    agents = ROOT / "AGENTS.md"
    problems: list[str] = []

    if not agents.exists():
        print("AGENTS.md is missing")
        return 1
    text = agents.read_text()
    if len(text) <= 100:
        problems.append("AGENTS.md is too short (<100 chars)")

    makefile = (ROOT / "Makefile").read_text()
    targets = set(re.findall(r"^([a-zA-Z_-]+):", makefile, re.MULTILINE))
    for target in sorted(set(re.findall(r"make ([a-zA-Z_-]+)", text))):
        if target not in targets:
            problems.append(f"AGENTS.md references 'make {target}' but no such Makefile target")

    pyproject = (ROOT / "pyproject.toml").read_text()
    if "uv run pytest" in text and "[tool.pytest.ini_options]" not in pyproject:
        problems.append("AGENTS.md documents 'uv run pytest' but pytest is not configured")

    if problems:
        for p in problems:
            print(f"AGENTS.md PROBLEM: {p}")
        return 1
    print(f"AGENTS.md OK ({len(text)} chars, all documented commands valid)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
