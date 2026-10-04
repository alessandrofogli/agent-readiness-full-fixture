"""Lightweight profiling helper (see docs/profiling.md)."""

from __future__ import annotations

import cProfile
import io
import pstats
from collections.abc import Callable
from functools import wraps
from typing import Any


def profile(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that records cumulative stats of the wrapped callable."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        pr = cProfile.Profile()
        pr.enable()
        try:
            return func(*args, **kwargs)
        finally:
            pr.disable()
            buf = io.StringIO()
            pstats.Stats(pr, stream=buf).sort_stats("cumulative").print_stats(10)
            wrapper.last_stats = buf.getvalue()  # type: ignore[attr-defined]

    wrapper.last_stats = ""  # type: ignore[attr-defined]
    return wrapper
