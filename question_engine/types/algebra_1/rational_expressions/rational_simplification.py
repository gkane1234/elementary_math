"""Simplify rational expressions and state excluded values.

Problems are built from linear factors with small integer roots, then expanded
for the prompt so every difficulty stays classroom-factorable (Algebra 1/2).
"""

from __future__ import annotations

import random
import uuid

from packages.polynomial_core import (
    Polynomial,
    polynomial_excluded_values,
    polynomial_fraction_latex,
    rational_excluded_values_latex,
)

from question_engine.base import QuestionType, register
from question_engine.models import Question
from question_engine.settings.generator_profiles import schema_for_generator


def _normalize_range(min_value: int, max_value: int) -> tuple[int, int]:
    if min_value > max_value:
        return max_value, min_value
    return min_value, max_value


def _root_bound(coef_min: int, coef_max: int) -> int:
    return max(1, min(6, abs(coef_min), abs(coef_max) or 6))


def _pick_root(bound: int, used: set[int], *, allow_zero: bool = True) -> int:
    candidates = [
        r
        for r in range(-bound, bound + 1)
        if r not in used and (allow_zero or r != 0)
    ]
    if not candidates:
        # Fall back to an unused root just outside the bound.
        for offset in range(1, bound + 8):
            for r in (bound + offset, -(bound + offset)):
                if r not in used:
                    return r
        return bound + 1
    return random.choice(candidates)


def _linear_factor(root: int, *, monic: bool, coef_bound: int) -> Polynomial:
    """Return a linear factor with integer root ``root`` (ax - a·root)."""
    if monic:
        leading = 1
    else:
        leading = random.randint(2, max(2, min(3, coef_bound)))
    return Polynomial([leading, -leading * root])


def _product(factors: list[Polynomial]) -> Polynomial:
    result = Polynomial([1])
    for factor in factors:
        result *= factor
    return result


def _content_scale(poly: Polynomial, scale: int) -> Polynomial:
    if scale == 1:
        return poly
    return Polynomial([int(c) * scale for c in poly.coef_list()])


def _resolve_cancel_factor_count(settings: dict) -> int:
    """Exact number of linear factors that must cancel.

    Prefers ``cancel_factor_count``. Falls back to legacy ``max_cancel_factors``
    (treated as an exact count) so older saved settings still work.
    UI string ``\"4\"`` / ``\"all\"`` means all-available (cancel every factor in
    a normal-sized problem, capped — not continuous D max).
    """
    if "cancel_factor_count" in settings and settings["cancel_factor_count"] is not None:
        raw = settings["cancel_factor_count"]
        if isinstance(raw, str):
            from question_engine.frameworks.primitives.rational_cancel import (
                ALL_AVAILABLE_CANCEL,
                resolve_rational_cancel_count,
                sample_all_available_factor_count,
            )

            text = raw.strip().lower()
            if text in {
                "",
                "random",
                "auto",
                "all",
                "all_available",
                "max",
                "4",  # UI: "All available"
            }:
                resolved = resolve_rational_cancel_count(settings)
                if resolved >= ALL_AVAILABLE_CANCEL:
                    # Size from degree settings / continuous sample, hard-capped.
                    den_max = int(settings.get("denominator_degree_max", 3))
                    sampled = sample_all_available_factor_count(settings, default=max(1, den_max))
                    return max(1, min(sampled, max(1, den_max)))
                return resolved
            return max(0, int(text))
        return max(0, int(raw))
    if "max_cancel_factors" in settings and settings["max_cancel_factors"] is not None:
        return max(0, int(settings["max_cancel_factors"]))
    from question_engine.frameworks.primitives.rational_cancel import (
        resolve_rational_cancel_count,
    )

    return resolve_rational_cancel_count(settings)


def _create_rational_simplification_problem(
    settings: dict,
    numerator_degree_min: int,
    numerator_degree_max: int,
    denominator_degree_min: int,
    denominator_degree_max: int,
) -> tuple[Polynomial, Polynomial, Polynomial, Polynomial, list[int], int]:
    """Build an expanded rational expression from cancelable linear factors.

    Returns
    (numerator, denominator, reduced_num, reduced_den, excluded_roots, cancel_count)
    where excluded_roots are zeros of the *original* denominator.
    """
    num_min, num_max = _normalize_range(numerator_degree_min, numerator_degree_max)
    den_min, den_max = _normalize_range(denominator_degree_min, denominator_degree_max)
    # Need room to cancel at least one factor; reduced denominator may be constant.
    den_min = max(1, den_min)
    den_max = max(den_min, den_max)
    num_min = max(1, num_min)
    num_max = max(num_min, num_max)

    coef_min = int(settings.get("coef_min", settings.get("c_min", -8)))
    coef_max = int(settings.get("coef_max", settings.get("c_max", 8)))
    monic = bool(settings.get("leading_coefficient_one", False)) or bool(
        settings.get("monic_only", False)
    )
    prefer_difference_of_squares = bool(
        settings.get("prefer_difference_of_squares", False)
    )
    allow_gcf = bool(settings.get("allow_constant_gcf", False))
    cancel_count = _resolve_cancel_factor_count(settings)

    # Degrees must be high enough to host the requested cancel factors.
    num_min = max(num_min, cancel_count)
    num_max = max(num_max, cancel_count)
    den_min = max(den_min, cancel_count)
    den_max = max(den_max, cancel_count)

    bound = _root_bound(coef_min, coef_max)
    coef_bound = max(1, min(4, abs(coef_min), abs(coef_max) or 4))

    for _ in range(200):
        target_num = random.randint(num_min, num_max)
        target_den = random.randint(den_min, den_max)
        common_count = cancel_count
        if common_count > min(target_num, target_den):
            continue

        reduced_num_degree = target_num - common_count
        reduced_den_degree = target_den - common_count
        if reduced_den_degree < 0:
            continue

        used: set[int] = set()
        common_roots: list[int] = []
        for _i in range(common_count):
            root = _pick_root(bound, used, allow_zero=True)
            used.add(root)
            common_roots.append(root)

        num_roots: list[int] = []
        for _i in range(reduced_num_degree):
            if (
                prefer_difference_of_squares
                and reduced_num_degree - len(num_roots) >= 2
                and random.random() < 0.45
            ):
                r = _pick_root(bound, used, allow_zero=False)
                if -r not in used and r != 0:
                    used.add(r)
                    used.add(-r)
                    num_roots.extend([r, -r])
                    continue
            root = _pick_root(bound, used, allow_zero=True)
            used.add(root)
            num_roots.append(root)

        den_roots: list[int] = []
        for _i in range(reduced_den_degree):
            if (
                prefer_difference_of_squares
                and reduced_den_degree - len(den_roots) >= 2
                and random.random() < 0.45
            ):
                r = _pick_root(bound, used, allow_zero=False)
                if -r not in used and r != 0:
                    used.add(r)
                    used.add(-r)
                    den_roots.extend([r, -r])
                    continue
            root = _pick_root(bound, used, allow_zero=True)
            used.add(root)
            den_roots.append(root)

        # Trim if difference-of-squares pairing overshot the target degrees.
        num_roots = num_roots[:reduced_num_degree]
        den_roots = den_roots[:reduced_den_degree]
        if len(num_roots) != reduced_num_degree or len(den_roots) != reduced_den_degree:
            continue

        common_factors = [
            _linear_factor(r, monic=monic or random.random() < 0.7, coef_bound=coef_bound)
            for r in common_roots
        ]
        reduced_num_factors = [
            _linear_factor(r, monic=monic or random.random() < 0.55, coef_bound=coef_bound)
            for r in num_roots
        ]
        reduced_den_factors = [
            _linear_factor(r, monic=monic or random.random() < 0.55, coef_bound=coef_bound)
            for r in den_roots
        ]

        reduced_numerator = (
            _product(reduced_num_factors) if reduced_num_factors else Polynomial([1])
        )
        reduced_denominator = (
            _product(reduced_den_factors) if reduced_den_factors else Polynomial([1])
        )
        common = _product(common_factors)

        numerator = common * reduced_numerator
        denominator = common * reduced_denominator

        # Optional shared constant GCF in the prompt; it cancels in the answer.
        if allow_gcf and random.random() < 0.55:
            scale = random.choice([2, 3, 4, 5])
            numerator = _content_scale(numerator, scale)
            denominator = _content_scale(denominator, scale)

        if numerator.deg() != target_num or denominator.deg() != target_den:
            continue
        if reduced_denominator.is_zero():
            continue

        # Prefer a positive leading coefficient on the denominator.
        if int(denominator.coef_list()[0]) < 0:
            numerator = _content_scale(numerator, -1)
            denominator = _content_scale(denominator, -1)
            reduced_numerator = _content_scale(reduced_numerator, -1)
            reduced_denominator = _content_scale(reduced_denominator, -1)

        # Excluded values: zeros of the *original* denominator (before canceling).
        original_den_roots = set(common_roots + den_roots)
        scanned = polynomial_excluded_values(
            denominator,
            coef_min=min(-20, -bound - 2),
            coef_max=max(20, bound + 2),
        )
        excluded = sorted(original_den_roots | set(scanned))

        return (
            numerator,
            denominator,
            reduced_numerator,
            reduced_denominator,
            excluded,
            common_count,
        )

    # Deterministic classroom-safe fallback sized to the requested cancel count.
    common_roots = list(range(2, 2 + cancel_count))
    leftover_num = cancel_count + 1
    leftover_den = -(cancel_count + 1)
    common = _product([Polynomial([1, -r]) for r in common_roots])
    reduced_numerator = Polynomial([1, -leftover_num])
    reduced_denominator = Polynomial([1, -leftover_den])
    return (
        common * reduced_numerator,
        common * reduced_denominator,
        reduced_numerator,
        reduced_denominator,
        sorted(set(common_roots + [leftover_den])),
        cancel_count,
    )


def _answer_latex(
    reduced_numerator: Polynomial,
    reduced_denominator: Polynomial,
    excluded: list[int],
) -> str:
    from packages.polynomial_core.rational import _scale_fraction_to_integers

    num, den = _scale_fraction_to_integers(reduced_numerator, reduced_denominator)
    if den.deg() == 0:
        den_const = int(round(float(den.coef_list()[0])))
        if den_const == 1:
            simplified = num.to_latex()
        elif den_const == -1:
            flipped = Polynomial(
                tuple(
                    (-int(round(float(c))), e)
                    for c, e in num.terms
                    if abs(float(c)) >= 1e-12
                )
                or ((0, 0),)
            )
            simplified = flipped.to_latex()
        else:
            simplified = polynomial_fraction_latex(num, den)
    else:
        simplified = polynomial_fraction_latex(num, den)
    note = rational_excluded_values_latex(excluded)
    if not note:
        return simplified
    return f"{simplified},\\; {note}"


@register
class RationalSimplificationQuestionType(QuestionType):
    id = "rational_simplification"
    name = "Simplifying and excluded values"
    category = "Algebra 1 — Rational Expressions"
    description = (
        "Simplify rational expressions by canceling common polynomial factors "
        "and state excluded values from the original denominator."
    )
    instruction_latex = (
        r"\text{Simplify. State any excluded values.}"
    )
    instruction_text = "Simplify. State any excluded values."

    def settings_schema(self):
        return schema_for_generator(self.id)

    def generate(self, settings: dict) -> list[Question]:
        count = int(settings.get("count", 10))
        numerator_degree_min = int(settings.get("numerator_degree_min", 2))
        numerator_degree_max = int(settings.get("numerator_degree_max", 3))
        denominator_degree_min = int(settings.get("denominator_degree_min", 2))
        denominator_degree_max = int(settings.get("denominator_degree_max", 3))
        include_answer_key = bool(settings.get("include_answer_key", False))

        questions: list[Question] = []
        for _ in range(count):
            (
                numerator,
                denominator,
                reduced_numerator,
                reduced_denominator,
                excluded,
                cancel_count,
            ) = _create_rational_simplification_problem(
                settings,
                numerator_degree_min,
                numerator_degree_max,
                denominator_degree_min,
                denominator_degree_max,
            )

            answer_latex = None
            if include_answer_key:
                answer_latex = _answer_latex(
                    reduced_numerator,
                    reduced_denominator,
                    excluded,
                )

            from packages.polynomial_core.rational import _scale_fraction_to_integers

            simplified_num, simplified_den = _scale_fraction_to_integers(
                reduced_numerator,
                reduced_denominator,
            )
            if (
                simplified_den.deg() == 0
                and abs(float(simplified_den.coef_list()[0]) - 1) < 1e-10
            ):
                simplified_meta = simplified_num.to_latex()
            else:
                simplified_meta = polynomial_fraction_latex(simplified_num, simplified_den)

            questions.append(
                Question(
                    id=str(uuid.uuid4()),
                    topic=self.id,
                    prompt_latex=polynomial_fraction_latex(numerator, denominator),
                    prompt_text=f"({numerator}) / ({denominator})",
                    answer_latex=answer_latex,
                    metadata={
                        "numerator_degree": numerator.deg(),
                        "denominator_degree": denominator.deg(),
                        "cancel_factor_count": cancel_count,
                        "excluded_values": excluded,
                        "simplified_latex": simplified_meta,
                    },
                )
            )

        return questions
