#!/usr/bin/env python3
"""Dead feature flag audit (CI + pre-commit gate).

- fails when a flag is defined in FLAGS but referenced nowhere else
- lists flags whose rollout is complete so owners can remove them
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAGS_FILE = ROOT / "packages" / "api" / "src" / "api" / "flags.py"
SKIP_DIRS = {".git", ".venv", "node_modules", "dist", "__pycache__"}


def defined_flags() -> dict[str, int]:
    text = FLAGS_FILE.read_text()
    flags: dict[str, int] = {}
    for m in re.finditer(r'"([a-z_]+)":\s*\{[^}]*?"rollout":\s*(\d+)', text, re.DOTALL):
        flags[m.group(1)] = int(m.group(2))
    return flags


def is_referenced(name: str) -> bool:
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file() or path == FLAGS_FILE:
            continue
        if path.suffix not in {".py", ".md", ".yml", ".yaml"}:
            continue
        try:
            if re.search(rf'["\']?{re.escape(name)}["\']?', path.read_text(errors="ignore")):
                return True
        except OSError:
            continue
    return False


def main() -> int:
    flags = defined_flags()
    dead = [name for name in flags if not is_referenced(name)]
    complete = [name for name, rollout in flags.items() if rollout >= 100]
    for name in dead:
        print(f"DEAD FLAG: '{name}' is defined but never referenced — remove it")
    for name in complete:
        print(f"STALE FLAG: '{name}' is at 100% rollout — schedule cleanup")
    print(f"audited {len(flags)} flags — {len(dead)} dead, {len(complete)} complete")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
