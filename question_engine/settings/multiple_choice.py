"""Multiple-choice choice builders and distractor helpers."""

from __future__ import annotations

import random
import re
import string
from typing import Any

_CHOICE_IDS = string.ascii_lowercase
_FRAC_RE = re.compile(
    r"^\\frac\{(-?\d+)\}\{(-?\d+)\}$|^(-?\d+)/(-?\d+)$"
)
_PERCENT_RE = re.compile(r"^(-?\d+(?:\.\d+)?)\\?%$")
_NUMERIC_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
_POINT_RE = re.compile(r"^\(?\s*(-?\d+)\s*,\s*(-?\d+)\s*\)?$")


def make_multiple_choice_choices(
    correct: str,
    distractors: list[str] | None = None,
    *,
    count: int = 4,
) -> list[dict[str, Any]]:
    """Build shuffled MC choices as ``[{id, latex, correct}, ...]``.

    Ensures exactly one correct choice and up to ``count - 1`` unique distractors.
    Choice ids are lowercase letters in display order after shuffle (a, b, c, …).
    """
    correct_latex = str(correct).strip()
    pool: list[str] = []
    seen = {correct_latex}
    for raw in distractors or []:
        text = str(raw).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        pool.append(text)

    while len(pool) < max(0, count - 1):
        generated = _distractor_values(correct_latex, exclude=seen)
        added = False
        for candidate in generated:
            if candidate in seen:
                continue
            seen.add(candidate)
            pool.append(candidate)
            added = True
            if len(pool) >= count - 1:
                break
        if not added:
            # Deterministic fallbacks so we always reach ``count`` options.
            fallback = f"{correct_latex} + {len(pool) + 1}"
            if fallback not in seen:
                seen.add(fallback)
                pool.append(fallback)
            else:
                break

    selected = pool[: count - 1]
    entries = [{"latex": correct_latex, "correct": True}] + [
        {"latex": text, "correct": False} for text in selected
    ]
    random.shuffle(entries)
    return [
        {"id": _CHOICE_IDS[index], "latex": entry["latex"], "correct": entry["correct"]}
        for index, entry in enumerate(entries)
    ]


def multiple_choice_enabled(settings: dict) -> bool:
    """Return True when this question should use multiple-choice presentation."""
    if bool(settings.get("multiple_choice", False)):
        return True
    if str(settings.get("answer_format", "auto")) == "multiple_choice":
        return True
    ratio = max(0, min(100, int(settings.get("multiple_choice_ratio", 0) or 0)))
    if ratio <= 0:
        return False
    if ratio >= 100:
        return True
    return random.randint(1, 100) <= ratio


def build_multiple_choice_metadata(
    answer: str,
    *,
    distractors: list[str] | None = None,
) -> dict[str, Any]:
    choices = make_multiple_choice_choices(answer, distractors)
    return {
        "choices": choices,
        "answer_mode": "multiple_choice",
    }


def _distractor_values(correct: str, *, exclude: set[str] | None = None) -> list[str]:
    exclude = exclude or set()
    generators = (
        _linear_equation_distractors,
        _fraction_distractors,
        _percent_distractors,
        _point_distractors,
        _numeric_distractors,
        _generic_distractors,
    )
    pool: list[str] = []
    for generator in generators:
        for candidate in generator(correct):
            if candidate and candidate not in exclude and candidate != correct:
                pool.append(candidate)
        if len(pool) >= 6:
            break
    random.shuffle(pool)
    return pool


def _numeric_distractors(correct: str) -> list[str]:
    if not _NUMERIC_RE.match(correct):
        return []
    base = float(correct)
    deltas = [-5, -3, -2, -1, 1, 2, 3, 5, -10, 10]
    if base != 0:
        deltas.extend([int(base), -int(base)] if float(base).is_integer() else [])
    pool: list[str] = []
    for delta in deltas:
        candidate = base + delta
        if candidate == base:
            continue
        text = str(int(candidate)) if float(candidate).is_integer() else f"{candidate:.4g}"
        pool.append(text)
    if float(base).is_integer():
        n = int(base)
        pool.extend([str(-n), str(n + 1), str(n - 1), str(2 * n if n else 2)])
    return pool


def _percent_distractors(correct: str) -> list[str]:
    match = _PERCENT_RE.match(correct.replace(" ", ""))
    if not match:
        # Also accept bare number when original used \\%
        if "\\%" in correct or correct.endswith("%"):
            raw = correct.replace("\\%", "").replace("%", "").strip()
            if _NUMERIC_RE.match(raw):
                base = float(raw)
            else:
                return []
        else:
            return []
    else:
        base = float(match.group(1))

    pool: list[str] = []
    for delta in (-10, -5, -2, -1, 1, 2, 5, 10):
        candidate = base + delta
        if candidate == base or candidate < 0:
            continue
        text = str(int(candidate)) if float(candidate).is_integer() else f"{candidate:.3g}"
        pool.append(f"{text}\\%")
    return pool


def _fraction_distractors(correct: str) -> list[str]:
    match = _FRAC_RE.match(correct.replace(" ", ""))
    if not match:
        return []
    if match.group(1) is not None:
        num, den = int(match.group(1)), int(match.group(2))
    else:
        num, den = int(match.group(3)), int(match.group(4))
    if den == 0:
        return []

    def frac(n: int, d: int) -> str:
        if d < 0:
            n, d = -n, -d
        if d == 1:
            return str(n)
        return f"\\frac{{{n}}}{{{d}}}"

    pool = [
        frac(den, num) if num != 0 else frac(1, den),
        frac(-num, den),
        frac(num + 1, den),
        frac(num - 1, den) if num - 1 != 0 or den != 1 else frac(num + 2, den),
        frac(num, den + 1) if den + 1 != 0 else frac(num, den + 2),
        frac(num, max(1, den - 1)),
        str(num) if den != 1 else frac(num, 2),
    ]
    return pool


def _linear_equation_distractors(correct: str) -> list[str]:
    text = correct.strip()
    if not text.startswith("y"):
        return []

    # y = b
    const = re.match(r"^y\s*=\s*(-?\d+)$", text)
    if const:
        b = int(const.group(1))
        return [f"y = {b + 1}", f"y = {b - 1}", f"y = {-b}", f"y = {2 * b if b else 1}"]

    # y = mx + b / y = mx - b / y = mx / y = -x + b
    m_match = re.match(
        r"^y\s*=\s*(-?\d*)x(?:\s*([+-])\s*(\d+))?$",
        text,
    )
    if not m_match:
        return []

    raw_m = m_match.group(1)
    if raw_m in ("", None):
        m = 1
    elif raw_m == "-":
        m = -1
    else:
        m = int(raw_m)
    sign = m_match.group(2)
    b_abs = int(m_match.group(3)) if m_match.group(3) is not None else 0
    b = b_abs if sign == "+" else -b_abs if sign == "-" else 0

    def slope_intercept(slope: int, intercept: int) -> str:
        if slope == 0:
            return f"y = {intercept}"
        if slope == 1:
            slope_part = "x"
        elif slope == -1:
            slope_part = "-x"
        else:
            slope_part = f"{slope}x"
        if intercept == 0:
            return f"y = {slope_part}"
        op = "+" if intercept > 0 else "-"
        return f"y = {slope_part} {op} {abs(intercept)}"

    return [
        slope_intercept(-m, b),
        slope_intercept(m, -b),
        slope_intercept(m + 1 if m != -1 else m + 2, b),
        slope_intercept(m - 1 if m != 1 else m - 2, b),
        slope_intercept(m, b + 1),
        slope_intercept(m, b - 1),
    ]


def _point_distractors(correct: str) -> list[str]:
    match = _POINT_RE.match(correct.replace(" ", ""))
    if not match:
        # (x, y) = (a, b)
        eq = re.match(r"^\(x,\s*y\)\s*=\s*\((-?\d+),\s*(-?\d+)\)$", correct.replace(" ", ""))
        if not eq:
            return []
        x, y = int(eq.group(1)), int(eq.group(2))
        fmt = lambda a, b: f"(x, y) = ({a}, {b})"
    else:
        x, y = int(match.group(1)), int(match.group(2))
        fmt = lambda a, b: f"({a}, {b})"
    return [
        fmt(y, x),
        fmt(-x, y),
        fmt(x, -y),
        fmt(x + 1, y),
        fmt(x, y + 1),
        fmt(x - 1, y - 1),
    ]


def _generic_distractors(correct: str) -> list[str]:
    return [
        f"-({correct})",
        f"{correct} + 1",
        f"{correct} - 1",
        f"2({correct})",
    ]
