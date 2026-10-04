#!/usr/bin/env python3
"""Detect dependency version drift across workspace packages (CI gate).

Fails when the same dependency appears with different specifiers in more than
one package's pyproject.toml, or contradicts constraints.txt pins.
"""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_constraints() -> dict[str, str]:
    pins: dict[str, str] = {}
    for line in (ROOT / "constraints.txt").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_.-]+)==([^\s]+)$", line)
        if m:
            pins[m.group(1).lower()] = m.group(2)
    return pins


def package_deps() -> dict[str, dict[str, str]]:
    deps: dict[str, dict[str, str]] = {}
    for pyproject in sorted(ROOT.glob("packages/*/pyproject.toml")):
        data = tomllib.loads(pyproject.read_text())
        specifiers: dict[str, str] = {}
        for dep in data.get("project", {}).get("dependencies", []):
            m = re.match(r"^([A-Za-z0-9_.-]+)(\[[^\]]*\])?\s*(.*)$", dep)
            if m:
                specifiers[m.group(1).lower()] = m.group(3).strip()
        deps[pyproject.parent.name] = specifiers
    return deps


def main() -> int:
    constraints = load_constraints()
    deps = package_deps()
    drift = False
    seen: dict[str, tuple[str, str]] = {}
    for pkg, specifiers in deps.items():
        for name, spec in specifiers.items():
            if name in seen and seen[name][1] != spec:
                print(
                    f"DRIFT: {name} is '{seen[name][1]}' in {seen[name][0]} but '{spec}' in {pkg}"
                )
                drift = True
            else:
                seen[name] = (pkg, spec)
    print(
        f"checked {len(deps)} packages, {len(seen)} dependencies, "
        f"{len(constraints)} constraints — {'DRIFT FOUND' if drift else 'no drift'}"
    )
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
