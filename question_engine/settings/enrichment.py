"""Runtime helpers for common enrichment settings used during generation."""

from __future__ import annotations

import math
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from typing import Any

from ..generators.utils import frac_latex

_DIFFICULTY_SCALE = {"easy": 0.55, "medium": 1.0, "hard": 1.45}


def difficulty_scale(settings: dict) -> float:
    """Scale factor for coefficient spans from continuous D or EMH tier."""
    if "difficulty" in settings and settings["difficulty"] is not None:
        raw = settings["difficulty"]
        try:
            d = max(0.0, float(raw))
            # D=0 → ~0.45, D=8 → ~1.0, D=20 → ~1.5 (soft asymptote).
            return 0.45 + 1.2 * (1.0 - math.exp(-d / 9.0))
        except (TypeError, ValueError):
            mapped = _DIFFICULTY_SCALE.get(str(raw).strip().lower())
            if mapped is not None:
                return mapped
    tier = str(settings.get("difficulty_tier", "medium")).strip().lower()
    return _DIFFICULTY_SCALE.get(tier, 1.0)


def scaled_int_range(
    settings: dict,
    lo: int,
    hi: int,
    *,
    minimum_span: int = 2,
    floor: int | None = None,
    ceiling: int | None = None,
) -> tuple[int, int]:
    """Scale a coefficient bound pair by difficulty tier."""
    if lo > hi:
        lo, hi = hi, lo
    center = (lo + hi) / 2
    half_span = max(minimum_span / 2, (hi - lo) / 2 * difficulty_scale(settings))
    new_lo = int(round(center - half_span))
    new_hi = int(round(center + half_span))
    if floor is not None:
        new_lo = max(floor, new_lo)
    if ceiling is not None:
        new_hi = min(ceiling, new_hi)
    if new_lo > new_hi:
        new_lo, new_hi = new_hi, new_lo
    return new_lo, new_hi


def apply_positive_coefficient_restriction(settings: dict, lo: int, hi: int) -> tuple[int, int]:
    if not bool(settings.get("coefficients_positive_only", False)):
        return lo, hi
    return max(1, lo), max(1, hi)


def random_term_count(settings: dict, *, default: int = 3) -> int:
    lo = int(settings.get("min_terms", default))
    hi = int(settings.get("max_terms", default))
    if lo > hi:
        lo, hi = hi, lo
    return random.randint(lo, hi)


def solution_allowed(settings: dict, value: int | Fraction) -> bool:
    if not bool(settings.get("exclude_zero_solutions", False)):
        return True
    if isinstance(value, Fraction):
        return value != 0
    return value != 0


def random_solution_in_range(
    settings: dict,
    lo: int,
    hi: int,
    *,
    integer_only: bool = True,
) -> int | Fraction:
    from .params import random_equation_solution
    from .params import EquationParams

    scaled_lo, scaled_hi = scaled_int_range(settings, lo, hi)
    scaled_lo, scaled_hi = apply_positive_coefficient_restriction(settings, scaled_lo, scaled_hi)
    params = EquationParams(coef_min=scaled_lo, coef_max=scaled_hi, integer_only=integer_only)
    for _ in range(40):
        value = random_equation_solution(params)
        if solution_allowed(settings, value):
            return value
    return 1 if scaled_lo <= 1 <= scaled_hi else scaled_lo


def format_answer_value(settings: dict, value: int | float | Fraction | Decimal) -> str:
    answer_format = str(settings.get("answer_format", "auto"))
    round_whole = bool(settings.get("round_answers_to_whole", False))

    if isinstance(value, Fraction):
        numeric = float(value)
    elif isinstance(value, Decimal):
        numeric = float(value)
    else:
        numeric = float(value)

    if round_whole:
        numeric = float(Decimal(str(numeric)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    if answer_format == "integer" or (answer_format == "auto" and round_whole):
        return str(int(round(numeric)))

    if answer_format == "fraction" and isinstance(value, Fraction):
        return frac_latex(value)

    if answer_format == "decimal":
        text = f"{numeric:.4g}"
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        return text

    if isinstance(value, Fraction) and value.denominator != 1:
        return frac_latex(value)
    if float(numeric).is_integer():
        return str(int(numeric))
    text = f"{numeric:.4g}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def enrichment_metadata(settings: dict, *, answer: str | None) -> dict[str, Any]:
    from .multiple_choice import build_multiple_choice_metadata, multiple_choice_enabled

    meta: dict[str, Any] = {}
    work_lines = int(settings.get("show_work_lines", 0))
    if work_lines > 0:
        meta["work_lines"] = work_lines

    if answer is not None and multiple_choice_enabled(settings):
        provided = settings.get("mc_distractors")
        distractors = [str(d) for d in provided] if isinstance(provided, list) else None
        meta.update(build_multiple_choice_metadata(answer, distractors=distractors))

    if "difficulty" in settings and settings["difficulty"] is not None:
        meta["difficulty"] = settings["difficulty"]
    tier = settings.get("difficulty_tier")
    if tier:
        meta["difficulty_tier"] = tier
    return meta


def merge_enrichment_metadata(settings: dict, metadata: dict[str, Any], *, answer: str | None) -> dict[str, Any]:
    merged = dict(metadata)
    framework_distractors = merged.pop("mc_distractors", None)
    settings_for_enrichment = settings
    if isinstance(framework_distractors, list):
        settings_for_enrichment = {**settings, "mc_distractors": framework_distractors}

    enrichment = enrichment_metadata(settings_for_enrichment, answer=answer)
    # Preserve choices a framework already attached.
    if "choices" in merged:
        enrichment.pop("choices", None)
        enrichment.pop("answer_mode", None)
    merged.update(enrichment)
    return merged
