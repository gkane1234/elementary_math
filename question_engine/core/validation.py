"""Answer validation utilities."""

from __future__ import annotations

import re


def _normalize_answer(value: str) -> str:
    return re.sub(r"\s+", "", value.strip().lower())


def answers_equivalent(
    given: str,
    expected: str,
    *,
    rtol: float = 1e-9,
    atol: float = 1e-9,
) -> bool:
    """Check whether two answers match.

    Current strategy:
    - normalized string equality (whitespace/case insensitive)
    - simple numeric comparison with relative/absolute tolerance

  Extension point: plug in symbolic equivalence (e.g. sympy) for
  algebraic expressions without changing call sites.
    """
    if _normalize_answer(given) == _normalize_answer(expected):
        return True

    given_numeric = _try_parse_numeric(given)
    expected_numeric = _try_parse_numeric(expected)
    if given_numeric is None or expected_numeric is None:
        return False

    return abs(given_numeric - expected_numeric) <= atol + rtol * abs(expected_numeric)


def _try_parse_numeric(value: str) -> float | None:
    cleaned = value.strip().rstrip("%").replace(",", "")
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None
