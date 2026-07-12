"""Radical equation generators with structure-based difficulty tiers.

Easy   — single radical; light prep (move constant / divide) before squaring;
         occasional simple √ = linear that needs an extraneous check.
Medium — more algebra to isolate; √ = linear with checking.
Hard   — two radicals that require squaring more than once; nestier forms;
         problems designed so extraneous candidates appear.

All tiers use integer coefficients only (no decimal mess in prompts).
"""

from __future__ import annotations

import random
from fractions import Fraction

from packages.polynomial_core import format_linear_latex

from ..settings.params import format_solution_value
from .utils import _make_questions, format_equation_latex


_FORM_KEYS = (
    ("light_prep", "allow_light_prep"),
    ("isolate_algebra", "allow_isolate_algebra"),
    ("radical_equals_linear", "allow_radical_equals_linear"),
    ("two_radicals", "allow_two_radicals"),
)


def _enabled_forms(settings: dict) -> list[str]:
    forms = [name for name, key in _FORM_KEYS if bool(settings.get(key, name == "light_prep"))]
    return forms or ["light_prep"]


def _choose_form(settings: dict) -> str:
    forms = _enabled_forms(settings)
    # Hard unlocks two-radical forms — prefer them so Easy ≠ Hard is obvious.
    if "two_radicals" in forms and len(forms) > 1 and random.random() < 0.72:
        return "two_radicals"
    return random.choice(forms)

def _coef_hi(settings: dict) -> int:
    return max(2, min(12, abs(int(settings.get("coef_max", 6))) or 6))


def _pick_int(lo: int, hi: int, *, nonzero: bool = False, positive: bool = False) -> int:
    if positive:
        lo = max(1, lo)
    if lo > hi:
        lo, hi = hi, lo
    for _ in range(40):
        value = random.randint(lo, hi)
        if nonzero and value == 0:
            continue
        return value
    if positive:
        return max(1, hi)
    if nonzero:
        return 1 if hi >= 1 else -1
    return lo


def _sqrt_linear(a: int, b: int, *, variable: str = "x") -> str:
    return f"\\sqrt{{{format_linear_latex(a, b, variable=variable)}}}"


def _signed_const(value: int) -> str:
    if value >= 0:
        return f"+ {value}"
    return f"- {abs(value)}"


def _format_answer(
    valid: list[int | Fraction],
    extraneous: list[int | Fraction],
    settings: dict,
    *,
    variable: str = "x",
) -> str | None:
    if not bool(settings.get("include_answer_key", False)):
        return None

    def _parts(values: list[int | Fraction]) -> list[str]:
        unique: list[int | Fraction] = []
        seen: set[Fraction] = set()
        for raw in values:
            frac = Fraction(raw).limit_denominator()
            if frac in seen:
                continue
            seen.add(frac)
            unique.append(int(frac) if frac.denominator == 1 else frac)
        unique.sort(key=lambda item: float(item))
        return [f"{variable} = {format_solution_value(v, settings)}" for v in unique]

    valid_parts = _parts(valid)
    extra_parts = _parts(extraneous)
    if not valid_parts:
        if extra_parts:
            discarded = r" \text{ or } ".join(extra_parts)
            return rf"\text{{no solution}};\ {discarded} \text{{ (extraneous)}}"
        return r"\text{no solution}"
    body = r" \text{ or } ".join(valid_parts)
    if extra_parts:
        discarded = r" \text{ or } ".join(extra_parts)
        return rf"{body};\ {discarded} \text{{ (extraneous)}}"
    return body


def _check_sqrt_equals_linear(
    a: int,
    b: int,
    c: int,
    d: int,
    candidates: list[int | Fraction],
) -> tuple[list[int | Fraction], list[int | Fraction]]:
    """Split candidates into valid / extraneous for √(ax+b) = cx+d."""
    valid: list[int | Fraction] = []
    extraneous: list[int | Fraction] = []
    for raw in candidates:
        x = Fraction(raw).limit_denominator()
        radicand = a * x + b
        rhs = c * x + d
        if radicand < 0 or rhs < 0:
            extraneous.append(x)
            continue
        if rhs * rhs == radicand:
            valid.append(x)
        else:
            extraneous.append(x)
    return valid, extraneous


def _quadratic_candidates_from_sqrt_linear(
    a: int,
    b: int,
    c: int,
    d: int,
) -> list[Fraction]:
    """Candidates from squaring √(ax+b) = cx+d → (cx+d)² = ax+b."""
    # (c x + d)^2 - a x - b = 0
    # c² x² + (2cd - a) x + (d² - b) = 0
    A = c * c
    B = 2 * c * d - a
    C = d * d - b
    if A == 0:
        if B == 0:
            return []
        return [Fraction(-C, B)]
    disc = B * B - 4 * A * C
    if disc < 0:
        return []
    root = int(disc**0.5)
    if root * root != disc:
        return []
    return [Fraction(-B + root, 2 * A), Fraction(-B - root, 2 * A)]


def _build_light_prep(settings: dict) -> tuple[str, str, str | None] | None:
    """Single radical; move a constant or divide, then square."""
    var = str(settings.get("variable", "x"))
    hi = _coef_hi(settings)

    # Occasional simple √ = linear so students practice checking.
    if random.random() < 0.25:
        return _build_simple_extraneous(settings)

    style = random.choice(["move", "divide", "isolated"])

    k = _pick_int(1, min(6, hi), positive=True)
    a = _pick_int(1, min(4, hi), positive=True)
    x = _pick_int(0, max(2, hi))
    b = k * k - a * x
    if abs(b) > 20:
        x = _pick_int(0, 6)
        b = k * k - a * x

    sqrt_term = _sqrt_linear(a, b, variable=var)

    if style == "divide":
        m = _pick_int(2, min(5, hi), positive=True)
        prompt = format_equation_latex(f"{m}{sqrt_term}", str(m * k))
        return prompt, prompt, _format_answer([x], [], settings, variable=var)

    if style == "move":
        c = _pick_int(1, min(8, hi), positive=True)
        if random.choice([True, False]):
            # √(...) + c = d
            prompt = format_equation_latex(f"{sqrt_term} + {c}", str(k + c))
        else:
            # √(...) - c = d with d ≥ 0
            if k >= c:
                prompt = format_equation_latex(f"{sqrt_term} - {c}", str(k - c))
            else:
                # Flip: c + √(...) = d
                prompt = format_equation_latex(f"{c} + {sqrt_term}", str(k + c))
        return prompt, prompt, _format_answer([x], [], settings, variable=var)

    prompt = format_equation_latex(sqrt_term, str(k))
    return prompt, prompt, _format_answer([x], [], settings, variable=var)


def _build_simple_extraneous(settings: dict) -> tuple[str, str, str | None] | None:
    """Classic single-radical extraneous checks suitable for easy/medium."""
    var = str(settings.get("variable", "x"))
    hi = _coef_hi(settings)

    if random.choice([True, False]):
        # √x = x - q  (e.g. √x = x - 2 → x=4 valid, x=1 extraneous)
        k = _pick_int(2, min(5, hi), positive=True)
        q = k * k - k
        prompt = format_equation_latex(f"\\sqrt{{{var}}}", format_linear_latex(1, -q, variable=var))
        candidates = _quadratic_candidates_from_sqrt_linear(1, 0, 1, -q)
        valid, extra = _check_sqrt_equals_linear(1, 0, 1, -q, candidates)
        return prompt, prompt, _format_answer(valid, extra, settings, variable=var)

    # √(x + p) = x - q
    k = _pick_int(2, min(5, hi), positive=True)
    r = _pick_int(1, k - 1, positive=True)
    q = k - r
    p = r * r - k
    prompt = format_equation_latex(
        _sqrt_linear(1, p, variable=var),
        format_linear_latex(1, -q, variable=var),
    )
    candidates = _quadratic_candidates_from_sqrt_linear(1, p, 1, -q)
    valid, extra = _check_sqrt_equals_linear(1, p, 1, -q, candidates)
    return prompt, prompt, _format_answer(valid, extra, settings, variable=var)


def _build_isolate_algebra(settings: dict) -> tuple[str, str, str | None] | None:
    """More algebra before isolating the radical, then square."""
    var = str(settings.get("variable", "x"))
    hi = _coef_hi(settings)
    k = _pick_int(1, min(7, hi), positive=True)
    a = _pick_int(1, min(5, hi), positive=True)
    x = _pick_int(0, max(3, hi))
    b = k * k - a * x
    if abs(b) > 24:
        x = _pick_int(0, 8)
        b = k * k - a * x

    sqrt_term = _sqrt_linear(a, b, variable=var)
    # Prefer forms that need real isolation algebra (not just move a constant).
    style = random.choice(["coeff_and_const", "linear_right_prep", "linear_right_prep"])

    if style == "coeff_and_const":
        m = _pick_int(2, min(5, hi), positive=True)
        c = _pick_int(1, min(9, hi), nonzero=True)
        d = m * k + c
        prompt = format_equation_latex(f"{m}{sqrt_term} {_signed_const(c)}", str(d))
        return prompt, prompt, _format_answer([x], [], settings, variable=var)

    # √(ax+b) + c = dx + e  → isolate, square, check extraneous.
    c = _pick_int(1, min(6, hi), positive=True)
    d_coef = _pick_int(1, min(3, hi), nonzero=True)
    if random.choice([True, False]):
        d_coef = -d_coef
    e = (k + c) - d_coef * x
    prompt = format_equation_latex(
        f"{sqrt_term} {_signed_const(c)}",
        format_linear_latex(d_coef, e, variable=var),
    )
    candidates = _quadratic_candidates_from_sqrt_linear(a, b, d_coef, e - c)
    valid, extra = _check_sqrt_equals_linear(a, b, d_coef, e - c, candidates)
    return prompt, prompt, _format_answer(valid, extra, settings, variable=var)


def _build_radical_equals_linear(settings: dict) -> tuple[str, str, str | None] | None:
    """√(ax+b) = cx+d — always check; often produces an extraneous root."""
    var = str(settings.get("variable", "x"))
    hi = _coef_hi(settings)

    # Prefer designing a valid root and letting squaring introduce an extraneous.
    want_extraneous = random.random() < 0.7
    for _ in range(30):
        c = _pick_int(1, min(3, hi), nonzero=True)
        if random.random() < 0.35:
            c = -c
        x_valid = _pick_int(0, max(4, hi))
        # rhs at solution must be > 0
        k = _pick_int(1, min(6, hi), positive=True)
        d = k - c * x_valid
        if c * x_valid + d <= 0:
            continue
        a = _pick_int(1, min(5, hi), positive=True)
        b = k * k - a * x_valid
        if abs(b) > 30:
            continue
        candidates = _quadratic_candidates_from_sqrt_linear(a, b, c, d)
        valid, extra = _check_sqrt_equals_linear(a, b, c, d, candidates)
        if not valid:
            continue
        if want_extraneous and not extra:
            # Force a classic extraneous pair when possible: √(x+p) = x - q
            continue
        if not want_extraneous and extra and random.random() < 0.5:
            continue
        prompt = format_equation_latex(
            _sqrt_linear(a, b, variable=var),
            format_linear_latex(c, d, variable=var),
        )
        return prompt, prompt, _format_answer(valid, extra, settings, variable=var)

    # Guaranteed classic with extraneous: √x = x - 2
    prompt = format_equation_latex(f"\\sqrt{{{var}}}", format_linear_latex(1, -2, variable=var))
    candidates = _quadratic_candidates_from_sqrt_linear(1, 0, 1, -2)
    valid, extra = _check_sqrt_equals_linear(1, 0, 1, -2, candidates)
    return prompt, prompt, _format_answer(valid, extra, settings, variable=var)


def _build_two_radicals(settings: dict) -> tuple[str, str, str | None] | None:
    """Two radicals — isolate and square more than once."""
    var = str(settings.get("variable", "x"))
    hi = _coef_hi(settings)
    # Prefer nestier / difference forms that surface extraneous candidates.
    style = random.choices(
        ["sum", "difference", "nested_shift"],
        weights=[2, 3, 4],
        k=1,
    )[0]

    # Pick two positive radical values u, v and a shared x.
    u = _pick_int(1, min(5, hi), positive=True)
    v = _pick_int(1, min(5, hi), positive=True)
    if style == "difference" and u == v:
        u = v + _pick_int(1, 3, positive=True)

    x = _pick_int(0, max(4, hi))
    p = u * u - x
    q = v * v - x
    if abs(p) > 24 or abs(q) > 24:
        x = _pick_int(0, 8)
        p = u * u - x
        q = v * v - x
    # Avoid trivial identical radicals (√A + √A = c).
    if p == q:
        if style == "sum":
            v = u + _pick_int(1, 3, positive=True)
            q = v * v - x
        else:
            return None

    left = _sqrt_linear(1, p, variable=var)
    right = _sqrt_linear(1, q, variable=var)

    if style == "sum":
        total = u + v
        prompt = format_equation_latex(f"{left} + {right}", str(total))
        valid, extra = _verify_two_sqrt_sum(1, p, 1, q, total, [x], search_hi=hi)
        return prompt, prompt, _format_answer(valid, extra, settings, variable=var)

    if style == "difference":
        if u < v:
            u, v = v, u
            p, q = q, p
            left, right = right, left
        diff = u - v
        if diff <= 0:
            return None
        prompt = format_equation_latex(f"{left} - {right}", str(diff))
        valid, extra = _verify_two_sqrt_diff(1, p, 1, q, diff, [x], search_hi=hi)
        # If no algebraic extraneous showed up, try the classic flipped form
        # by also checking √A + √B = diff ghosts (already in verifier).
        return prompt, prompt, _format_answer(valid, extra, settings, variable=var)

    # √(ax+b) = √(cx+d) + e — square twice; design an extraneous when possible.
    e = _pick_int(1, min(4, hi), positive=True)
    v = _pick_int(1, min(4, hi), positive=True)
    u = v + e
    x = _pick_int(0, max(4, hi))
    a = _pick_int(1, min(4, hi), positive=True)
    c_coef = _pick_int(1, min(4, hi), positive=True)
    b = u * u - a * x
    d = v * v - c_coef * x
    if abs(b) > 28 or abs(d) > 28:
        return None
    lhs = _sqrt_linear(a, b, variable=var)
    rhs = f"{_sqrt_linear(c_coef, d, variable=var)} + {e}"
    prompt = format_equation_latex(lhs, rhs)
    valid, extra = _verify_nested_shift(a, b, c_coef, d, e, seed_roots=[x], search_hi=hi)
    return prompt, prompt, _format_answer(valid, extra, settings, variable=var)


def _integer_search_range(seed_roots: list[int], search_hi: int) -> list[int]:
    lo = min([-2, *seed_roots]) - 4
    hi = max([search_hi, *seed_roots]) + 6
    return list(range(lo, hi + 1))


def _verify_two_sqrt_sum(
    a1: int,
    b1: int,
    a2: int,
    b2: int,
    total: int,
    seed_roots: list[int],
    *,
    search_hi: int,
) -> tuple[list[int | Fraction], list[int | Fraction]]:
    """Find integer solutions to √(a1 x+b1) + √(a2 x+b2) = total by checking."""
    valid: list[int | Fraction] = []
    # Algebraic extraneous from one isolation: isolate first radical and square once
    # produces a linear/quadratic residue; we also collect near-miss integers that
    # satisfy the squared equation but not the original.
    squared_hits: list[int] = []
    for x in _integer_search_range(seed_roots, search_hi):
        r1 = a1 * x + b1
        r2 = a2 * x + b2
        if r1 < 0 or r2 < 0:
            continue
        s1 = int(r1**0.5)
        s2 = int(r2**0.5)
        if s1 * s1 == r1 and s2 * s2 == r2:
            if s1 + s2 == total:
                valid.append(x)
            elif abs(s1 - s2) == total or s1 + s2 == -total:
                squared_hits.append(x)
            # Also flag if (total - s2)^2 == r1 but s2 wrong sign path
            if (total - s2) * (total - s2) == r1 and s1 + s2 != total and total - s2 >= 0:
                if x not in squared_hits and x not in valid:
                    squared_hits.append(x)
    extra = [v for v in squared_hits if v not in valid]
    # Ensure seed roots that work are included
    for x in seed_roots:
        r1 = a1 * x + b1
        r2 = a2 * x + b2
        if r1 >= 0 and r2 >= 0:
            s1 = int(r1**0.5)
            s2 = int(r2**0.5)
            if s1 * s1 == r1 and s2 * s2 == r2 and s1 + s2 == total and x not in valid:
                valid.append(x)
    return valid, extra


def _verify_two_sqrt_diff(
    a1: int,
    b1: int,
    a2: int,
    b2: int,
    diff: int,
    seed_roots: list[int],
    *,
    search_hi: int,
) -> tuple[list[int | Fraction], list[int | Fraction]]:
    valid: list[int | Fraction] = []
    squared_hits: list[int] = []
    for x in _integer_search_range(seed_roots, search_hi):
        r1 = a1 * x + b1
        r2 = a2 * x + b2
        if r1 < 0 or r2 < 0:
            continue
        s1 = int(r1**0.5)
        s2 = int(r2**0.5)
        if s1 * s1 != r1 or s2 * s2 != r2:
            continue
        if s1 - s2 == diff:
            valid.append(x)
        elif s2 - s1 == diff or s1 + s2 == diff:
            squared_hits.append(x)
    extra = [v for v in squared_hits if v not in valid]
    for x in seed_roots:
        r1 = a1 * x + b1
        r2 = a2 * x + b2
        if r1 >= 0 and r2 >= 0:
            s1 = int(r1**0.5)
            s2 = int(r2**0.5)
            if s1 * s1 == r1 and s2 * s2 == r2 and s1 - s2 == diff and x not in valid:
                valid.append(x)
    return valid, extra


def _verify_nested_shift(
    a: int,
    b: int,
    c: int,
    d: int,
    e: int,
    seed_roots: list[int],
    *,
    search_hi: int,
) -> tuple[list[int | Fraction], list[int | Fraction]]:
    """√(ax+b) = √(cx+d) + e — check integer candidates; note extras from squaring."""
    valid: list[int | Fraction] = []
    # After one square: ax+b = (cx+d) + e² + 2e√(cx+d)
    # Isolate and square again → polynomial. Collect integers that satisfy the
    # once-squared relation with a negative radical branch.
    extraneous: list[int | Fraction] = []
    for x in _integer_search_range(seed_roots, search_hi):
        left = a * x + b
        right_inner = c * x + d
        if left < 0 or right_inner < 0:
            continue
        s_left = int(left**0.5)
        s_right = int(right_inner**0.5)
        if s_left * s_left != left or s_right * s_right != right_inner:
            continue
        if s_left == s_right + e:
            valid.append(x)
        elif s_left == abs(s_right - e) or s_left + e == s_right:
            # Typical extraneous from squaring (wrong sign / swapped).
            extraneous.append(x)
        elif left == right_inner + e * e - 2 * e * s_right:
            # Satisfies a once-squared identity with flipped sign.
            extraneous.append(x)
    for x in seed_roots:
        left = a * x + b
        right_inner = c * x + d
        if left >= 0 and right_inner >= 0:
            s_left = int(left**0.5)
            s_right = int(right_inner**0.5)
            if (
                s_left * s_left == left
                and s_right * s_right == right_inner
                and s_left == s_right + e
                and x not in valid
            ):
                valid.append(x)
    extra = [v for v in extraneous if v not in valid]
    return valid, extra


def _try_build(form: str, settings: dict) -> tuple[str, str, str | None] | None:
    builders = {
        "light_prep": _build_light_prep,
        "isolate_algebra": _build_isolate_algebra,
        "radical_equals_linear": _build_radical_equals_linear,
        "two_radicals": _build_two_radicals,
    }
    builder = builders.get(form)
    if builder is None:
        return None
    for _ in range(40):
        built = builder(settings)
        if built is not None:
            prompt, text, answer = built
            # Reject decimal-looking coefficients in the prompt (safety net).
            if "." in prompt:
                continue
            return prompt, text, answer
    return None


def generate_radical_equations(topic: str, settings: dict) -> list:
    """Generate radical-equation questions for *topic*."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        for _ in range(80):
            form = _choose_form(settings)
            built = _try_build(form, settings)
            if built is not None:
                return built
        # Absolute fallback: √(x + 3) = 2 → x = 1
        var = str(settings.get("variable", "x"))
        prompt = format_equation_latex(_sqrt_linear(1, 3, variable=var), "2")
        answer = _format_answer([1], [], {**settings, "include_answer_key": include_answer_key}, variable=var)
        return prompt, prompt, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)
