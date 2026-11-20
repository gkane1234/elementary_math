"""Pick a same-skill question form from the worksheet seed.

Unseeded calls stay on form 0 so existing unit samples keep their shape.
A seeded batch rotates forms by item, so one topic set can ask every form.
"""

from __future__ import annotations

from typing import Any


def form_slot(settings: dict[str, Any] | None, n: int) -> int:
    """Return an index in ``0 .. n-1``.

    Uses the worksheet seed plus the per-item batch index. Does not draw from
    ``random``, so the numeric sample for form 0 stays on its old sequence.
    """
    if n <= 1 or not settings:
        return 0
    raw = settings.get("seed")
    if raw is None:
        return 0
    try:
        seed = int(raw)
    except (TypeError, ValueError):
        return 0
    try:
        batch = int(settings.get("_batch_index") or 0)
    except (TypeError, ValueError):
        batch = 0
    return (seed + batch) % n
