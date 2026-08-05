"""Unified effort scoring interface for generation records.

Difficulty is **effort / meaningful steps**, not raw magnitude.
Per-topic scorers return ``(effort: float, feats: dict)`` on the 0–25 scale used
by G6 continuous-D verification. Types without a registered scorer return
``(None, {})``.
"""

from __future__ import annotations

import math
import re
from collections.abc import Callable
from typing import Any

from question_engine.frameworks.number import (
    meaningful_cancel_steps,
    strip_place_value_tens,
)

EffortScorer = Callable[[str, str], tuple[float, dict[str, Any]]]


def effort_intro_ratios(prompt: str, answer: str) -> tuple[float, dict]:
    m = re.search(r"Write the ratio \} (\d+):(\d+)", prompt)
    form = "simplify"
    if m:
        a, b = int(m.group(1)), int(m.group(2))
    else:
        m = re.search(r"There are (\d+) .* and (\d+) ", prompt)
        if not m:
            return 8.0, {"parse_fail": True}
        a, b = int(m.group(1)), int(m.group(2))
        form = "word"
    g = math.gcd(a, b)
    steps = meaningful_cancel_steps(g)
    feats = {"a": a, "b": b, "gcd": g, "form": form, "meaningful_steps": steps}
    if form == "word":
        return min(2.0, 0.5 + 0.3 * (max(a, b) >= 20)), feats
    if steps == 0:
        e = 2.0 if g == 1 else 2.5
        if g > 1 and strip_place_value_tens(g) == 1:
            e = 3.0
    else:
        e = 4.0 + 3.0 * steps + (1.5 if steps >= 3 else 0) + (2.0 if steps >= 5 else 0)
    return round(min(e, 25.0), 1), feats


def effort_equivalent(prompt: str, answer: str) -> tuple[float, dict]:
    m = re.search(r"(\d+):(\d+) = (\d+):x", prompt)
    if not m:
        m = re.search(r"frac\{(\d+)\}\{(\d+)\} = \\frac\{(\d+)\}\{x\}", prompt)
    if not m:
        return 8.0, {"parse_fail": True}
    a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
    g = math.gcd(a, b)
    steps = meaningful_cancel_steps(g)
    surface_int = c % a == 0 if a else False
    e = 3.0
    e += 2.5 * steps
    if not surface_int:
        e += 4.0
    elif surface_int and (c // a) >= 5:
        e += 2.0
    return round(min(e, 25.0), 1), {
        "a": a,
        "b": b,
        "c": c,
        "gcd": g,
        "steps": steps,
        "surface_int": surface_int,
    }


def effort_ppw(prompt: str, answer: str) -> tuple[float, dict]:
    e = 4.0
    feats: dict = {}
    if "split in the ratio" in prompt:
        e = 12.0
        feats["mode"] = "missing_part"
    elif "both in simplest form" in prompt:
        e = 14.0
        feats["mode"] = "both"
    elif "to all" in prompt or ("all " in prompt and "to" in prompt):
        e = 8.0
        feats["mode"] = "part_whole"
        if "simplest form" in prompt:
            e += 3.0
    else:
        e = 4.0
        feats["mode"] = "part_part"
        if "simplest form" in prompt:
            e += 3.0
    nums = [int(x) for x in re.findall(r"\b(\d+)\b", prompt)]
    if nums:
        mx = max(nums)
        if mx >= 40:
            e += 2.0
        if mx >= 80:
            e += 2.0
    return round(min(e, 25.0), 1), feats


def effort_compare_ratios(prompt: str, answer: str) -> tuple[float, dict]:
    nums = [int(x) for x in re.findall(r"(\d+)", prompt)]
    if len(nums) < 4:
        return 8.0, {"parse_fail": True}
    a, b, c, d = nums[0], nums[1], nums[2], nums[3]
    g1, g2 = math.gcd(a, b), math.gcd(c, d)
    steps = meaningful_cancel_steps(g1) + meaningful_cancel_steps(g2)
    close = abs(a / b - c / d) < 0.2
    same_part = a == c or b == d
    e = 3.0
    if same_part:
        e += 1.0
    else:
        e += 4.0 + 2.0 * steps
    if close:
        e += 4.0
    if "frac" in prompt:
        e += 1.0
    return round(min(e, 25.0), 1), {"steps": steps, "close": close, "same_part": same_part}


def effort_unit_rates(prompt: str, answer: str) -> tuple[float, dict]:
    nums = [int(x) for x in re.findall(r"(\d+)", prompt)]
    equiv = "same rate" in prompt or "At the same rate" in prompt
    e = 5.0 if not equiv else 8.0
    if len(nums) >= 2:
        steps = (
            meaningful_cancel_steps(nums[1])
            if not equiv
            else meaningful_cancel_steps(math.gcd(nums[0], nums[1]) if len(nums) >= 2 else 1)
        )
        e += 2.5 * steps
        if max(nums) >= 50:
            e += 1.5
    return round(min(e, 25.0), 1), {"equiv": equiv, "nums": nums[:4]}


def effort_comparing_rates(prompt: str, answer: str) -> tuple[float, dict]:
    nums = [int(x) for x in re.findall(r"(\d+)", prompt)]
    e = 6.0
    if len(nums) >= 4:
        steps = meaningful_cancel_steps(math.gcd(nums[0], nums[1])) + meaningful_cancel_steps(
            math.gcd(nums[2], nums[3])
        )
        e += 2.5 * steps
        unit_bottoms = sum(1 for x in (nums[1], nums[3]) if x == 1)
        e += (2 - unit_bottoms) * 3.0
    return round(min(e, 25.0), 1), {"nums": nums[:4]}


def effort_converting(prompt: str, answer: str) -> tuple[float, dict]:
    e = 4.0
    approx = any(w in prompt.lower() for w in ("about", "approximately", "≈", "approx"))
    if approx:
        e += 6.0
    nums = [int(x) for x in re.findall(r"(\d+)", prompt)]
    if nums and max(nums) >= 100:
        e += 2.0
    if nums and max(nums) >= 500:
        e += 3.0
    return round(min(e, 25.0), 1), {"approx": approx, "max_num": max(nums) if nums else 0}


def effort_finding_equiv(prompt: str, answer: str) -> tuple[float, dict]:
    e = 4.0
    if "denominator 100" in prompt:
        e += 1.0
    m = re.search(r"frac\{(\d+)\}\{(\d+)\}", prompt)
    if m:
        num, den = int(m.group(1)), int(m.group(2))
        g = math.gcd(num, den)
        steps = meaningful_cancel_steps(g)
        e += 2.5 * steps
        red_den = den // g
        if red_den in (1, 2, 4, 5, 10, 20, 25, 50, 100):
            k = 100 // red_den if red_den and 100 % red_den == 0 else 1
            if k in (1, 2, 5, 10):
                e += 1.0
            elif k in (4,):
                e += 3.0
            else:
                e += 2.0
        elif red_den in (8, 16, 32, 40, 80):
            e += 6.0 + (2.0 if red_den >= 16 else 0)
        else:
            e += 5.0
    elif "%" in prompt:
        if any(x in prompt for x in ("12.5", "37.5", "62.5", "6.25", "18.75", "87.5")):
            e += 8.0
        elif any(x in prompt for x in ("25", "50", "75", "10", "20")):
            e += 2.0
        else:
            e += 4.0
    return round(min(e, 25.0), 1), {}


def effort_intro_percents(prompt: str, answer: str) -> tuple[float, dict]:
    e = 4.0
    pl = prompt.lower()
    if "several figures" in pl or "each figure" in pl:
        e = 18.0
    elif "circle" in pl:
        e = 14.0
    elif "bar" in pl:
        e = 9.0
    elif "grid" in pl:
        e = 6.0
    m = re.search(r"(\d+)\\?%", prompt)
    if m:
        p = int(m.group(1))
        if p % 5 != 0:
            e += 4.0
        elif p not in (10, 25, 50, 75, 100):
            e += 2.0
        else:
            e = min(e, 5.0) if e <= 6 else e
    return round(min(e, 25.0), 1), {}


def effort_relating(prompt: str, answer: str) -> tuple[float, dict]:
    e = 5.0
    has_pct = "%" in prompt or "percent" in prompt.lower()
    if not has_pct:
        e = 3.0
    hard_markers = (
        "0.125",
        "12.5",
        "37.5",
        "62.5",
        "6.25",
        "18.75",
        "0.0625",
        "0.1875",
        "0.875",
        "87.5",
        "\\frac{1}{8}",
        "\\frac{3}{8}",
        "\\frac{5}{8}",
        "\\frac{7}{8}",
        "\\frac{1}{16}",
        "\\frac{3}{16}",
    )
    if any(x in prompt for x in hard_markers):
        e += 8.0
    elif "0.05" in prompt or "\\frac{1}{20}" in prompt or "\\frac{1}{25}" in prompt:
        e += 2.0
    if "simplest form" in prompt:
        e += 2.0
    return round(min(e, 25.0), 1), {"has_pct": has_pct}


def effort_formulas(prompt: str, answer: str) -> tuple[float, dict]:
    e = 5.0
    if "what percent" in prompt.lower():
        e += 3.0
    if "of what number" in prompt.lower():
        e += 5.0
    nums = re.findall(r"(\d+(?:\.\d+)?)", prompt)
    if any("." in x for x in nums):
        e += 4.0
    ints = [int(float(x)) for x in nums]
    if ints and max(ints) >= 200:
        e += 3.0
    if ints and max(ints) >= 500:
        e += 3.0
    return round(min(e, 25.0), 1), {}


# ---------------------------------------------------------------------------
# Pre-Algebra / shared number-lane scorers (0–25 effort scale)
# ---------------------------------------------------------------------------


def _omega(n: int) -> int:
    """Total number of prime factors with multiplicity (Ω)."""
    n = abs(int(n))
    if n <= 1:
        return 0
    count = 0
    while n % 2 == 0:
        count += 1
        n //= 2
    f = 3
    while f * f <= n:
        while n % f == 0:
            count += 1
            n //= f
        f += 2
    if n > 1:
        count += 1
    return count


def effort_integer_ops(prompt: str, answer: str) -> tuple[float, dict]:
    """Integer ± / × / ÷ — signs + digit work + non-integer quotient, not |n| alone."""
    pl = prompt.replace("{", "").replace("}", "")
    nums = [int(x) for x in re.findall(r"-?\d+", pl)]
    feats: dict[str, Any] = {"nums": nums[:4]}
    if len(nums) < 2:
        return 6.0, {**feats, "parse_fail": True}
    a, b = nums[0], nums[1]
    op = "+"
    if "\\cdot" in prompt or "\\times" in prompt or " * " in prompt:
        op = "*"
    elif "\\div" in prompt or " / " in prompt:
        op = "/"
    elif " - " in prompt or "]-" in pl or re.search(r"\d\s*-\s*-?\d", pl):
        op = "-"
    feats["op"] = op
    e = 2.0
    signs = (a < 0) + (b < 0)
    e += 1.5 * signs
    mag = max(abs(a), abs(b), 1)
    # Digit / place work (log scale), not raw magnitude theater.
    digits = len(str(mag))
    e += 1.5 * max(0, digits - 1)
    if op == "*":
        e += 2.0
        if abs(a) >= 10 and abs(b) >= 10:
            e += 3.0
        elif abs(a) >= 10 or abs(b) >= 10:
            e += 1.5
    elif op == "/":
        e += 2.5
        if "frac" in (answer or "") or (
            b != 0 and a % b != 0
        ):
            e += 5.0
            feats["nonint"] = True
        elif b != 0 and abs(a // b) >= 20:
            e += 2.0
    elif op == "-":
        e += 1.0
        if signs == 1:
            e += 1.5  # subtracting a negative / mixed signs
    return round(min(e, 25.0), 1), feats


def effort_factoring(prompt: str, answer: str) -> tuple[float, dict]:
    m = re.search(r"prime factorization of \}?\s*(\d+)", prompt)
    if not m:
        m = re.search(r"factor(?:ization)? of \}?\s*(\d+)", prompt, re.I)
    if not m:
        nums = [int(x) for x in re.findall(r"\b(\d+)\b", prompt)]
        if not nums:
            return 8.0, {"parse_fail": True}
        n = max(nums)
    else:
        n = int(m.group(1))
    omega = _omega(n)
    steps = meaningful_cancel_steps(n) if n > 1 else 0
    # Ω drives effort; pure place-value powers of 10 stay cheap.
    e = 2.0 + 2.5 * max(0, omega - 1) + 1.0 * steps
    if omega >= 5:
        e += 2.0
    return round(min(e, 25.0), 1), {"n": n, "omega": omega, "steps": steps}


def effort_gcf(prompt: str, answer: str) -> tuple[float, dict]:
    nums = [int(x) for x in re.findall(r"\b(\d+)\b", prompt)]
    if len(nums) < 2:
        return 8.0, {"parse_fail": True}
    g = nums[0]
    for x in nums[1:]:
        g = math.gcd(g, x)
    steps = meaningful_cancel_steps(g)
    omega = _omega(g)
    e = 3.0 + 2.5 * steps + 1.5 * max(0, omega - 1)
    if len(nums) >= 3:
        e += 3.0
    # Near-coprime large pairs without shared factors are still some work.
    if g == 1 and max(nums) >= 30:
        e = max(e, 6.0)
    return round(min(e, 25.0), 1), {"nums": nums[:4], "gcf": g, "steps": steps}


def effort_lcm(prompt: str, answer: str) -> tuple[float, dict]:
    nums = [int(x) for x in re.findall(r"\b(\d+)\b", prompt)]
    if len(nums) < 2:
        return 8.0, {"parse_fail": True}
    a, b = nums[0], nums[1]
    g = math.gcd(a, b)
    # LCM effort ≈ combined unique prime work.
    omega_a, omega_b = _omega(a), _omega(b)
    combined = omega_a + omega_b - _omega(g)
    steps = meaningful_cancel_steps(g)
    e = 3.5 + 2.0 * max(1, combined) + 1.5 * steps
    if len(nums) >= 3:
        e += 3.0
    return round(min(e, 25.0), 1), {
        "nums": nums[:4],
        "gcf": g,
        "combined_omega": combined,
        "steps": steps,
    }


def effort_simplify_fractions(prompt: str, answer: str) -> tuple[float, dict]:
    m = re.search(r"frac\{(-?\d+)\}\{(-?\d+)\}", prompt)
    if not m:
        return 6.0, {"parse_fail": True}
    num, den = abs(int(m.group(1))), abs(int(m.group(2)))
    g = math.gcd(num, den) if den else 1
    steps = meaningful_cancel_steps(g)
    e = 2.0
    if steps == 0 and g > 1 and strip_place_value_tens(g) == 1:
        e = 3.0  # place-value cancel only
    elif steps == 0:
        e = 2.5
    else:
        e = 3.5 + 3.0 * steps + (1.5 if steps >= 3 else 0) + (2.0 if steps >= 5 else 0)
    return round(min(e, 25.0), 1), {"num": num, "den": den, "gcd": g, "steps": steps}


def effort_fraction_decimal_convert(prompt: str, answer: str) -> tuple[float, dict]:
    """F↔D only — denom / terminating-decimal awkwardness (not percent relating)."""
    e = 3.0
    hard = (
        "0.125",
        "0.375",
        "0.625",
        "0.875",
        "0.0625",
        "0.1875",
        "12.5",
        "\\frac{1}{8}",
        "\\frac{3}{8}",
        "\\frac{5}{8}",
        "\\frac{7}{8}",
        "\\frac{1}{16}",
        "\\frac{3}{16}",
        "\\frac{13}{40}",
    )
    mid = (
        "0.04",
        "0.02",
        "0.15",
        "\\frac{1}{25}",
        "\\frac{1}{50}",
        "\\frac{3}{20}",
        "\\frac{1}{8}",
    )
    if any(x in prompt for x in hard):
        e += 8.0
    elif any(x in prompt for x in mid):
        e += 4.0
    elif "0.5" in prompt or "\\frac{1}{2}" in prompt or "0.25" in prompt or "0.75" in prompt:
        e += 1.0
    else:
        e += 2.5
    if "simplest form" in prompt:
        e += 1.5
    return round(min(e, 25.0), 1), {}


def effort_place_value_rounding(prompt: str, answer: str) -> tuple[float, dict]:
    pl = prompt.lower()
    e = 3.0
    place_cost = {
        "thousandth": 8.0,
        "hundredth": 5.0,
        "tenth": 2.0,
        "ones": 1.0,
        "whole": 1.5,
    }
    for name, cost in place_cost.items():
        if name in pl:
            e += cost
            break
    else:
        e += 2.0
    # Magnitude of the displayed number.
    m = re.search(r"(\d+\.\d+|\d+)", prompt)
    if m:
        digs = len(m.group(1).replace(".", ""))
        e += 0.8 * max(0, digs - 2)
    if "round" in pl:
        e += 1.5
    return round(min(e, 25.0), 1), {}


def effort_writing_numbers_words(prompt: str, answer: str) -> tuple[float, dict]:
    e = 2.0
    reverse = "numerals" in prompt.lower() or "Write in numerals" in prompt
    if reverse:
        e += 3.0
        words = re.sub(r".*Write in numerals:\s*}?\s*\\?text\{?", "", prompt)
        token_count = len(re.findall(r"[a-z]+", words.lower()))
        e += 0.6 * max(0, token_count - 2)
        if "million" in words.lower():
            e += 6.0
        elif "thousand" in words.lower():
            e += 3.0
        return round(min(e, 25.0), 1), {"reverse": True, "tokens": token_count}
    m = re.search(r"Write \}?\s*(\d+)", prompt)
    n = int(m.group(1)) if m else 0
    if n >= 1_000_000:
        e += 10.0
    elif n >= 100_000:
        e += 7.0
    elif n >= 10_000:
        e += 5.5
    elif n >= 1_000:
        e += 4.0
    elif n >= 100:
        e += 2.5
    elif n >= 20:
        e += 1.5
    return round(min(e, 25.0), 1), {"n": n, "reverse": False}


def effort_interest(prompt: str, answer: str) -> tuple[float, dict]:
    pl = prompt.lower()
    compound = "compound" in pl
    e = 6.0 if not compound else 11.0
    feats: dict[str, Any] = {"compound": compound}
    if "balance" in pl or "account balance" in pl or "end of the term" in pl:
        e += 2.0
        feats["ask"] = "amount"
    else:
        feats["ask"] = "interest"
    # Decimal rates and long horizons add steps.
    if re.search(r"\d+\.\d+\\?%", prompt):
        e += 3.0
        feats["decimal_rate"] = True
    years = re.search(r"for (\d+) years?", pl)
    if years:
        t = int(years.group(1))
        feats["years"] = t
        if t >= 8:
            e += 2.5
        elif t >= 5:
            e += 1.5
    if "monthly" in pl:
        e += 2.0
    elif "quarter" in pl:
        e += 1.5
    elif "annual" in pl or "yearly" in pl or "once a year" in pl:
        e += 0.5
    return round(min(e, 25.0), 1), feats


def effort_squares_roots(prompt: str, answer: str) -> tuple[float, dict]:
    e = 3.0
    feats: dict[str, Any] = {}
    if "squared" in prompt.lower() or "^{2}" in prompt or "^2" in prompt:
        feats["mode"] = "square"
        m = re.search(r"What is \}?\s*(\d+)", prompt) or re.search(
            r"(\d+)\s*\^\s*\{?2\}?", prompt
        )
        if not m:
            m = re.search(r"(\d+)", prompt)
        n = int(m.group(1)) if m else 5
        e = 2.5 + (1.5 if n >= 15 else 0) + (2.0 if n >= 25 else 0)
        feats["n"] = n
    elif "\\sqrt" in prompt or "sqrt(" in prompt:
        feats["mode"] = "root"
        m = re.search(r"sqrt\{(\d+)\}", prompt) or re.search(r"sqrt\((\d+)\)", prompt)
        rad = int(m.group(1)) if m else 16
        feats["radicand"] = rad
        root = int(math.isqrt(rad))
        if root * root == rad:
            e = 3.0 + (1.5 if root >= 15 else 0) + (2.0 if root >= 25 else 0)
            feats["perfect"] = True
        else:
            e = 10.0 + (
                3.0 if any(rad % s == 0 for s in (4, 9, 16, 25, 36, 49) if s < rad) else 2.0
            )
            feats["perfect"] = False
    return round(min(e, 25.0), 1), feats


def effort_markup_discount(prompt: str, answer: str) -> tuple[float, dict]:
    """WP percent (markup / discount / tax / tip) — reuse formula-style signals."""
    e, feats = effort_formulas(prompt, answer)
    pl = prompt.lower()
    if "discount" in pl and "tax" in pl:
        e += 3.5
        feats["kind"] = "discount_then_tax"
    elif "discount" in pl or "sale" in pl:
        e += 1.5
        feats["kind"] = "discount"
    elif "tax" in pl:
        e += 1.0
        feats["kind"] = "tax"
    elif "markup" in pl or "mark up" in pl:
        e += 2.0
        feats["kind"] = "markup"
    elif "tip" in pl:
        e += 1.5
        feats["kind"] = "tip"
    if "including tip" in pl or "total, including" in pl:
        e += 1.0
        feats["tip_total"] = True
    return round(min(e, 25.0), 1), feats


_FRAC_RE = re.compile(r"frac\{(-?\d+)\}\{(-?\d+)\}")


def _parse_fracs(prompt: str) -> list[tuple[int, int]]:
    return [(int(a), int(b)) for a, b in _FRAC_RE.findall(prompt)]


def effort_fraction_ops(prompt: str, answer: str) -> tuple[float, dict]:
    """Fraction ± / × / ÷ — LCD / cancel / signs, not raw numerator size."""
    fracs = _parse_fracs(prompt)
    feats: dict[str, Any] = {"n_fracs": len(fracs)}
    if len(fracs) < 1:
        return 6.0, {**feats, "parse_fail": True}

    op = "+"
    if "\\cdot" in prompt or "\\times" in prompt or " * " in prompt:
        op = "*"
    elif (
        "\\div" in prompt
        or " / " in prompt
        or "}/{" in prompt.replace(" ", "")
        or re.search(r"frac\{.*\\frac", prompt)
    ):
        # Nested frac / slash layout often means division (A1 rational_divide uses " / ").
        if "\\div" in prompt or " / " in prompt or prompt.count("frac{") >= 3:
            op = "/"
        elif "\\cdot" not in prompt and "\\times" not in prompt:
            # \frac{a/b}{c/d} style
            if prompt.count("frac{") >= 3:
                op = "/"
    elif " - " in prompt or re.search(r"\}\s*-\s*(?:\\frac|-)", prompt):
        op = "-"
    feats["op"] = op

    dens = [abs(d) for _, d in fracs if d]
    nums = [abs(n) for n, _ in fracs]
    signs = sum(1 for n, _ in fracs if n < 0) + ("-" in prompt[: max(prompt.find("frac"), 0) + 1])
    e = 3.0
    e += 1.0 * min(signs, 2)

    if op in ("+", "-"):
        like = len(set(dens)) <= 1 if dens else True
        feats["like_denoms"] = like
        if like:
            e += 1.5
        else:
            # LCD construction: product vs smaller LCD.
            if len(dens) >= 2:
                g = math.gcd(dens[0], dens[1])
                product = dens[0] * dens[1]
                lcd = product // g if g else product
                feats["lcd"] = lcd
                e += 5.0 if lcd == product and g == 1 else 3.5
                if lcd >= 24:
                    e += 2.0
            else:
                e += 3.0
        # Simplify after.
        m = _FRAC_RE.search(answer or "")
        if m:
            ag = math.gcd(abs(int(m.group(1))), abs(int(m.group(2))) or 1)
            steps = meaningful_cancel_steps(ag) if ag > 1 else 0
            e += 1.5 * steps
            feats["answer_steps"] = steps
    elif op == "*":
        e += 3.0
        # Cross-cancel opportunity between num_i and den_j.
        cancel = 0
        if len(fracs) >= 2:
            (a, b), (c, d) = fracs[0], fracs[1]
            cancel = meaningful_cancel_steps(math.gcd(abs(a), abs(d))) + meaningful_cancel_steps(
                math.gcd(abs(c), abs(b))
            )
        feats["cancel"] = cancel
        e += 2.0 * cancel
        if not cancel and dens and max(dens + nums) >= 20:
            e += 2.5  # no-cancel large product
    else:  # divide
        e += 5.0  # reciprocal step
        if len(fracs) >= 2:
            (a, b), (c, d) = fracs[0], fracs[1]
            cancel = meaningful_cancel_steps(math.gcd(abs(a), abs(c))) + meaningful_cancel_steps(
                math.gcd(abs(d), abs(b))
            )
            feats["cancel"] = cancel
            e += 1.5 * cancel
        if dens and max(dens) >= 12:
            e += 1.5

    return round(min(e, 25.0), 1), feats


def effort_equations(prompt: str, answer: str) -> tuple[float, dict]:
    """Linear / multi-step equations & inequalities — structure over |coef|."""
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 4.0
    # Word-problem wrapper.
    if "text{" in prompt and ("number" in pl or "equation is" in pl or "operations" in pl):
        e += 3.0
        feats["wp"] = True
        if "two" in pl or "two-step" in pl or "two operations" in pl:
            e += 2.0
            feats["wp_steps"] = 2
        else:
            feats["wp_steps"] = 1
    # Distributed / parenthetical forms.
    paren = prompt.count("left(") + prompt.count("(")
    feats["parens"] = paren
    e += 2.0 * min(paren, 4)
    # Fraction coefficients.
    fracs = _parse_fracs(prompt)
    feats["n_fracs"] = len(fracs)
    e += 2.5 * min(len(fracs), 3)
    # Variable occurrences ≈ term load (x/y/z + common greek).
    var_hits = len(
        re.findall(
            r"(?<![a-z])(?:[xyz]|\\alpha|\\beta|\\gamma|\\theta)(?![a-z])",
            prompt,
            re.I,
        )
    )
    feats["var_hits"] = var_hits
    e += 1.2 * max(0, var_hits - 1)
    # Two-step shape: coeff·var ± constant on a side (without heavy paren nesting).
    if paren == 0 and re.search(
        r"(?:-?\d+|\\frac\{[^}]+\}\{[^}]+\})\s*[a-zA-Z\\]", prompt
    ) and re.search(r"[a-zA-Z\\].*[+\-].*=|=.*[+\-]", prompt):
        e += 2.0
        feats["two_step_shape"] = True
    # Inequality flip — avoid false positives from \left / \right.
    if re.search(
        r"(?:\\leq|\\geq|\\le(?![a-z])|\\ge(?![a-z])|\\lt|\\gt|(?<![\\a-z])[<>](?![\\a-z]))",
        prompt,
    ):
        e += 2.0
        feats["inequality"] = True
    # Rational answer slightly harder than integer.
    if "frac" in (answer or ""):
        e += 1.5
        feats["rational_sol"] = True
    return round(min(e, 25.0), 1), feats


def effort_proportions(prompt: str, answer: str) -> tuple[float, dict]:
    """Proportion solve / check / WP — variable placement + cross-multiply size."""
    feats: dict[str, Any] = {}
    e = 4.0
    pl = prompt.lower()
    if "scale" in pl or "recipe" in pl or ("proportion" in pl and "text{" in prompt):
        e += 2.5
        feats["wp"] = True
    # Variable in a linear expression inside a ratio slot (e.g. (y+2)/6).
    if re.search(r"frac\{[^}]*[+\-][^}]*\}", prompt):
        e += 3.0
        feats["linear_slot"] = True
    # Extract ratio parts around x.
    nums = [int(x) for x in re.findall(r"\b(\d+)\b", prompt)]
    feats["nums"] = nums[:6]
    if re.search(r"frac\{[^}]*\}\{(?:[xyz]|\\[a-z]+)\}", prompt) or re.search(
        r"frac\{\d+\}\{[xyz]\}", prompt
    ):
        e += 2.0
        feats["var_in_den"] = True
    elif re.search(r"frac\{(?:[xyz]|\\[a-z]+|[xyz]\s*[+\-])", prompt):
        e += 1.0
        feats["var_in_num"] = True
    if nums:
        mag = max(nums)
        e += 0.8 * max(0, len(str(mag)) - 1)
        if mag >= 30:
            e += 1.5
    if "frac" in (answer or ""):
        e += 2.0
        feats["rational_sol"] = True
    return round(min(e, 25.0), 1), feats


def effort_slope(prompt: str, answer: str) -> tuple[float, dict]:
    """Slope — two-point (sign / non-int) or read-m from y=mx+b (OpenStax §4.4–4.5)."""
    feats: dict[str, Any] = {}
    pl = prompt.lower()
    two_point = "through" in pl or len(re.findall(r"\([^)]+,[^)]+\)", prompt)) >= 2
    if not two_point and re.search(r"y\s*=", prompt):
        # Read slope from slope-intercept / equation form.
        e = 2.5
        feats["mode"] = "from_equation"
        if "frac" in prompt:
            e += 2.0
            feats["fractional_m"] = True
        rhs = prompt.split("=", 1)[-1]
        if re.search(r"-\s*(\\frac|\d|[a-z])", rhs) or "=-" in prompt.replace(" ", ""):
            e += 1.0
            feats["negative_m"] = True
        return round(min(e, 25.0), 1), feats

    coords = [int(x) for x in re.findall(r"-?\d+", prompt)]
    feats["coords"] = coords[:4]
    feats["mode"] = "two_point"
    e = 3.5
    if len(coords) >= 4:
        x1, y1, x2, y2 = coords[0], coords[1], coords[2], coords[3]
        dx, dy = x2 - x1, y2 - y1
        feats["dx"] = dx
        feats["dy"] = dy
        if dx == 0:
            e += 6.0
            feats["undefined"] = True
        else:
            if dy < 0 or dx < 0:
                e += 1.5
            mag = max(abs(x1), abs(y1), abs(x2), abs(y2))
            e += 0.6 * max(0, len(str(mag)) - 1)
            if abs(dx) > 1 and abs(dy) % abs(dx) != 0:
                e += 3.0
                feats["nonint"] = True
            elif abs(dy // dx) if dx else 0 >= 5:
                e += 1.0
    else:
        e += 2.0
        feats["parse_fail"] = len(coords) < 4
    return round(min(e, 25.0), 1), feats


def effort_linear_write(prompt: str, answer: str) -> tuple[float, dict]:
    """Slope-intercept write — given slope/intercept vs two points."""
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 3.0
    if "two points" in pl or "through" in pl and "slope" not in pl:
        e += 5.0
        feats["mode"] = "two_points"
    elif "slope" in pl and ("intercept" in pl or "y-intercept" in pl or "y\\text{-intercept}" in prompt):
        e += 2.0
        feats["mode"] = "slope_intercept"
        nums = [int(x) for x in re.findall(r"-?\d+", prompt)]
        if any(n < 0 for n in nums):
            e += 1.5
        if any(abs(n) >= 10 for n in nums):
            e += 1.0
    elif "point" in pl and "slope" in pl:
        e += 4.0
        feats["mode"] = "point_slope"
    else:
        e += 2.5
        feats["mode"] = "other"
    return round(min(e, 25.0), 1), feats


def effort_systems(prompt: str, answer: str) -> tuple[float, dict]:
    """2×2 systems — isolation form, coef size, WP wrapper."""
    feats: dict[str, Any] = {}
    e = 6.0
    pl = prompt.lower()
    if "text{" in prompt and ("buys" in pl or "costs" in pl or "items" in pl):
        e += 3.0
        feats["wp"] = True
    if "graphing" in pl:
        e += 2.0
        feats["graph"] = True
    # Already solved for y → easier substitution start.
    if re.search(r"y\s*=", prompt):
        e -= 1.5
        feats["isolated_y"] = True
    coefs = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if coefs:
        m = max(coefs)
        feats["max_coef"] = m
        e += 0.5 * max(0, len(str(m)) - 1)
        if m >= 12:
            e += 2.0
    if "no solution" in (answer or "").lower() or "infinite" in (answer or "").lower():
        e += 2.5
        feats["special"] = True
    return round(min(max(e, 2.0), 25.0), 1), feats


def effort_polynomials(prompt: str, answer: str) -> tuple[float, dict]:
    """Poly simplify / ± / × / naming — degree, distribute, term count."""
    feats: dict[str, Any] = {}
    e = 3.5
    pl = prompt.lower()
    # Naming: degree / term count of the displayed polynomial.
    if "name the polynomial" in pl:
        feats["op"] = "naming"
        e = 2.0
        degs = [int(x) for x in re.findall(r"\^\{?(\d+)\}?", prompt)]
        max_deg = max(degs) if degs else (1 if re.search(r"[a-z]", pl) else 0)
        feats["max_deg"] = max_deg
        e += 1.8 * max_deg
        terms = 1 + len(re.findall(r"[+-]", prompt.split(":", 1)[-1]))
        feats["n_terms"] = terms
        e += 0.8 * max(0, terms - 2)
        return round(min(e, 25.0), 1), feats

    is_special = (
        r")^{2}" in prompt.replace(" ", "")
        or r")^2" in prompt.replace(" ", "")
        or r"\right)^{2}" in prompt.replace(" ", "")
        or r"\right)^2" in prompt.replace(" ", "")
    )
    is_mul = (
        "multiply" in pl
        or ")(" in prompt.replace(" ", "")
        or r"\right)\left(" in prompt
        or is_special
    )
    if is_mul:
        e += 7.0
        feats["op"] = "multiply"
        if is_special or "difference of" in pl:
            e += 1.5
            feats["special"] = True
            # (a+b)(a-b) / square patterns are slightly lighter than general FOIL
            # once recognized — keep premium modest via no extra paren tax below.
    elif "simplify" in pl or "+" in prompt or "-" in prompt:
        feats["op"] = "add_sub_or_simplify"
        e += 1.5
    # Degree from exponents.
    degs = [int(x) for x in re.findall(r"\^\{?(\d+)\}?", prompt)]
    max_deg = max(degs) if degs else (1 if re.search(r"(?<![a-z])[a-z](?![a-z])", pl) else 0)
    feats["max_deg"] = max_deg
    e += 1.5 * max(0, max_deg - 1)
    # Distribute / paren count (multiply already paid a base premium).
    paren = prompt.count("left(") + prompt.count("(")
    feats["parens"] = paren
    e += (1.0 if is_mul else 1.8) * min(paren, 3)
    # Term-ish count via +/− between chunks.
    terms = len(re.findall(r"[+-]", prompt))
    feats["pm_ops"] = terms
    e += 0.6 * max(0, terms - 2)
    # Outer distribute coefficient (e.g. 5(poly) − …).
    if re.search(r"(?<![a-z])\d+\s*\\?left?\(", prompt) or re.search(
        r"(?<![a-z])\d+\(", prompt
    ):
        e += 2.0
        feats["outer_distribute"] = True
    return round(min(e, 25.0), 1), feats


def effort_poly_gcf(prompt: str, answer: str) -> tuple[float, dict]:
    """Factor GCF from a polynomial — GCF richness + term count, not |coef| theater."""
    feats: dict[str, Any] = {}
    e = 4.0
    # Terms in the prompt polynomial (after "Factor:").
    body = prompt.split(":", 1)[-1] if ":" in prompt else prompt
    terms = 1 + len(re.findall(r"[+-]", body))
    feats["n_terms"] = terms
    e += 1.5 * max(0, terms - 2)
    degs = [int(x) for x in re.findall(r"\^\{?(\d+)\}?", prompt)]
    max_deg = max(degs) if degs else (1 if re.search(r"[a-zA-Z]", body) else 0)
    feats["max_deg"] = max_deg
    e += 1.2 * max(0, max_deg - 1)
    # Answer GCF: numeric factor and/or variable power.
    ans = answer or ""
    m = re.match(r"\s*(-?\d+)?([a-zA-Z])?(?:\^\{?(\d+)\}?)?\s*\\?left?\(", ans)
    if not m:
        m = re.match(r"\s*(-?\d+)?([a-zA-Z])?(?:\^\{?(\d+)\}?)?\(", ans)
    if m:
        coef = abs(int(m.group(1))) if m.group(1) else 1
        var = m.group(2)
        pwr = int(m.group(3)) if m.group(3) else (1 if var else 0)
        feats["gcf_coef"] = coef
        feats["gcf_var_pow"] = pwr
        if coef > 1:
            e += 1.5 + 1.0 * max(0, meaningful_cancel_steps(coef) - 1)
        if var:
            e += 2.0 + 1.0 * max(0, pwr - 1)
    else:
        feats["parse_fail"] = True
        e += 2.0
    return round(min(e, 25.0), 1), feats


def _poly_factor_body(prompt: str) -> str:
    """Prompt polynomial body after optional ``Factor:`` / equation LHS."""
    body = prompt.split(":", 1)[-1] if ":" in prompt else prompt
    if "=" in body:
        body = body.split("=", 1)[0]
    return body


def _poly_prompt_term_count(prompt: str) -> int:
    body = _poly_factor_body(prompt)
    # Drop outer ``k\left(...\right)`` wrapper so term count is of the poly.
    inner = re.search(r"\\left\((.+)\\right\)\s*$", body.replace("\n", " "))
    if inner:
        body = inner.group(1)
    return 1 + len(re.findall(r"(?<![\^e])[+-]", body))


def _poly_max_deg(prompt: str) -> int:
    degs = [int(x) for x in re.findall(r"\^\{?(\d+)\}?", prompt)]
    if degs:
        return max(degs)
    return 1 if re.search(r"[a-zA-Z]", _poly_factor_body(prompt)) else 0


def _answer_has_numeric_gcf(answer: str) -> bool:
    """True when factored form starts with a numeric GCF before a paren."""
    ans = answer or ""
    return bool(
        re.match(r"\s*-?\d+[a-zA-Z]?(?:\^\{?\d+\}?)?\s*(?:\\left\(|\()", ans)
    )


def _answer_binomial_count(answer: str) -> int:
    ans = answer or ""
    return len(re.findall(r"\\left\(|(?<![a-zA-Z0-9])\(", ans))


def _prompt_unsimplified(prompt: str) -> bool:
    """Outer distribute / numeric split disguise (compose unsimplify)."""
    return bool(
        re.search(r"(?<![a-zA-Z])\d+\s*\\left\(", prompt)
        or re.search(r"(?<![a-zA-Z])\d+\(", prompt)
        or (" + " in prompt and " - " in prompt and prompt.count("+") + prompt.count("-") >= 4)
    )


def effort_poly_grouping(prompt: str, answer: str) -> tuple[float, dict]:
    """Factor by grouping — 4-term split, degree, GCF-first (OpenStax §7.1)."""
    feats: dict[str, Any] = {}
    e = 7.0
    terms = _poly_prompt_term_count(prompt)
    feats["n_terms"] = terms
    if terms >= 4:
        e += 3.0
        feats["four_term"] = True
    elif terms == 3:
        e += 1.5
    max_deg = _poly_max_deg(prompt)
    feats["max_deg"] = max_deg
    e += 1.5 * max(0, max_deg - 2)
    if _answer_has_numeric_gcf(answer):
        e += 2.5
        feats["gcf_first"] = True
    if _prompt_unsimplified(prompt):
        e += 2.0
        feats["unsimplified"] = True
    return round(min(e, 25.0), 1), feats


def effort_poly_special(prompt: str, answer: str) -> tuple[float, dict]:
    """Special-product factoring — DOS / PST / cubes (OpenStax §7.4)."""
    feats: dict[str, Any] = {}
    e = 5.0
    body = _poly_factor_body(prompt)
    terms = _poly_prompt_term_count(prompt)
    feats["n_terms"] = terms
    ans = answer or ""
    max_deg = _poly_max_deg(prompt)
    feats["max_deg"] = max_deg

    is_square_ans = bool(
        re.search(r"(\\right\)|\))\s*\^\s*\{?\s*2\s*\}?", ans)
        or re.search(r"(\\left\(|\()[^)]+(\\right\)|\))\s*\\?left?\(\s*\1", ans)
    )
    # Repeated identical binomial: (x+1)(x+1)
    if not is_square_ans and _answer_binomial_count(ans) >= 2:
        parts = re.findall(r"\\left\(([^)]+)\\right\)|\(([^)]+)\)", ans)
        flats = [(a or b).replace(" ", "") for a, b in parts]
        if len(flats) >= 2 and flats[0] == flats[1]:
            is_square_ans = True

    if max_deg >= 3 and terms <= 2:
        feats["pattern"] = "sum_diff_cubes"
        e += 6.0
    elif is_square_ans or terms == 3:
        feats["pattern"] = "perfect_square"
        e += 4.0
    elif terms == 2:
        feats["pattern"] = "diff_squares"
        e += 2.0
    else:
        feats["pattern"] = "other_special"
        e += 3.0

    # Leading coef ≠ 1 on expanded (or non-monic factors).
    lead = re.match(r"\s*(-?\d+)\s*[a-zA-Z]", body.lstrip())
    if lead and abs(int(lead.group(1))) != 1:
        e += 2.5
        feats["nonmonic"] = True
    if _answer_has_numeric_gcf(answer):
        e += 2.0
        feats["gcf_first"] = True
    if _prompt_unsimplified(prompt):
        e += 2.0
        feats["unsimplified"] = True
    return round(min(e, 25.0), 1), feats


def effort_quadratic_factoring(prompt: str, answer: str) -> tuple[float, dict]:
    """Trinomial / quadratic factoring — monic vs ac, signs, GCF (OpenStax §7.2–7.3)."""
    feats: dict[str, Any] = {}
    e = 5.0
    body = _poly_factor_body(prompt)
    terms = _poly_prompt_term_count(prompt)
    feats["n_terms"] = terms
    e += 0.8 * max(0, terms - 3)

    lead = re.match(r"\s*(-?\d+)\s*[a-zA-Z]", body.lstrip())
    lead_coef = abs(int(lead.group(1))) if lead else 1
    # Bare ``x^2`` → monic.
    if re.match(r"\s*[a-zA-Z]", body.lstrip()):
        lead_coef = 1
    feats["lead_coef"] = lead_coef
    if lead_coef == 1:
        feats["method"] = "monic"
        e += 1.5
    else:
        feats["method"] = "ac"
        e += 5.0
        e += 0.5 * max(0, meaningful_cancel_steps(lead_coef) - 1)

    ans = answer or ""
    n_bins = _answer_binomial_count(ans)
    feats["n_binomials"] = n_bins
    # Sign patterns in factors (mixed signs harder).
    factor_bodies = re.findall(r"\\left\(([^)]+)\\right\)|\(([^)]+)\)", ans)
    signs = 0
    for a, b in factor_bodies:
        chunk = a or b
        if "-" in chunk:
            signs += 1
    feats["neg_factor_signs"] = signs
    e += 1.2 * signs

    if _answer_has_numeric_gcf(answer):
        e += 2.5
        feats["gcf_first"] = True
    if _prompt_unsimplified(prompt):
        e += 2.0
        feats["unsimplified"] = True
    # Fractional / awkward constant pairs in factors.
    if "frac" in ans:
        e += 2.0
        feats["frac_factor"] = True
    return round(min(e, 25.0), 1), feats


def effort_poly_general_strategy(prompt: str, answer: str) -> tuple[float, dict]:
    """General factoring strategy — method choice + structure (OpenStax §7.5)."""
    feats: dict[str, Any] = {}
    e = 8.0  # choose-method premium
    feats["strategy"] = True
    terms = _poly_prompt_term_count(prompt)
    max_deg = _poly_max_deg(prompt)
    feats["n_terms"] = terms
    feats["max_deg"] = max_deg

    # Route structural cues toward the matching ladder scorers' drivers.
    if terms >= 4:
        e_g, fg = effort_poly_grouping(prompt, answer)
        e = max(e, e_g + 1.5)
        feats.update({f"g_{k}": v for k, v in fg.items()})
        feats["routed"] = "grouping"
    elif terms == 2 and max_deg >= 2:
        e_s, fs = effort_poly_special(prompt, answer)
        e = max(e, e_s + 1.5)
        feats.update({f"s_{k}": v for k, v in fs.items()})
        feats["routed"] = "special"
    else:
        e_q, fq = effort_quadratic_factoring(prompt, answer)
        e = max(e, e_q + 1.5)
        feats.update({f"q_{k}": v for k, v in fq.items()})
        feats["routed"] = "quadratic"
    if _prompt_unsimplified(prompt):
        e += 1.0
        feats["unsimplified"] = True
    return round(min(e, 25.0), 1), feats


def effort_quadratic_factor_solve(prompt: str, answer: str) -> tuple[float, dict]:
    """Solve by factoring — factor ladder + zero-product (OpenStax §7.6)."""
    e_fac, feats = effort_quadratic_factoring(prompt, answer)
    e = e_fac + 3.0
    feats = {**feats, "solve": True}
    pl = prompt.replace(" ", "")
    if "=0" not in pl and r"=0" not in pl:
        # Needs rearrange / move-to-zero first.
        e += 2.0
        feats["rearrange"] = True
    ans = answer or ""
    if "frac" in ans:
        e += 2.0
        feats["frac_root"] = True
    # Two distinct roots vs repeated.
    if ans.count("x") >= 2 or "," in ans:
        e += 0.5
    return round(min(e, 25.0), 1), feats


def effort_properties_of_exponents(prompt: str, answer: str) -> tuple[float, dict]:
    """Exponent laws — pattern type + exponent size, not raw |n| theater."""
    feats: dict[str, Any] = {}
    e = 3.0
    exps = [int(x) for x in re.findall(r"\^\{(-?\d+)\}", prompt)]
    feats["exps"] = exps[:4]
    # Pattern ladder (matches generator unlock order).
    if re.search(r"\\left\(.+?\\right\)\^\{", prompt) or re.search(
        r"\([^)]+\)\^\{", prompt
    ):
        feats["pattern"] = "power"
        e += 5.0
    elif re.search(r"\^\{-\d+\}", prompt) and "cdot" not in prompt and "frac" not in prompt:
        feats["pattern"] = "negative"
        e += 6.0
    elif "frac{" in prompt:
        feats["pattern"] = "quotient"
        e += 3.5
        if any(x < 0 for x in exps) or (len(exps) >= 2 and exps[0] < exps[1]):
            e += 2.0
            feats["neg_result"] = True
    elif "cdot" in prompt or r"\cdot" in prompt:
        feats["pattern"] = "product"
        e += 2.0
    elif re.search(r"\^[{\d].*[+\-].*\^", prompt) or (
        "+" in prompt
        or (
            prompt.count("-")
            - len(re.findall(r"\^\{-\d+\}", prompt))
            - prompt.count("^{-")
        )
        >= 1
        and "^" in prompt
    ):
        # Sum/difference of like bases — already simplified / trap.
        feats["pattern"] = "sum"
        e += 7.0
    else:
        feats["pattern"] = "other"
        e += 3.0
    if exps:
        mag = max(abs(x) for x in exps)
        e += 0.35 * max(0, mag - 3)
        if mag >= 10:
            e += 1.5
    if "-" in (answer or "") and "frac" in (answer or ""):
        e += 1.0
    return round(min(e, 25.0), 1), feats


def effort_rational_simplification(prompt: str, answer: str) -> tuple[float, dict]:
    """Cancel / simplify rational expressions — degree + cancel load + LCD addends."""
    feats: dict[str, Any] = {}
    e = 5.0
    # Degree proxies from expanded powers in prompt.
    degs = [int(x) for x in re.findall(r"\^\{?(\d+)\}?", prompt)]
    max_deg = max(degs) if degs else (1 if "x" in prompt else 0)
    feats["max_deg"] = max_deg
    e += 1.8 * max(0, max_deg - 1)
    # Term density (expanded poly terms).
    pm = len(re.findall(r"[+-]", prompt))
    feats["pm_ops"] = pm
    e += 0.5 * max(0, pm - 3)
    # Factor-form dens (LCD / factored) vs expanded.
    factor_parens = prompt.count("(") + prompt.count("left(")
    feats["factor_parens"] = factor_parens
    if factor_parens >= 2:
        e += 2.5 * min(factor_parens, 4)
        feats["factored_form"] = True
    # Multiple addends → rational expression ± path.
    n_fracs = prompt.count("frac{")
    feats["n_fracs"] = n_fracs
    if n_fracs >= 2:
        e += 4.0
        feats["multi_addend"] = True
    # Excluded values in the answer ≈ cancel / domain work.
    if "neq" in (answer or "") or "≠" in (answer or ""):
        tail = (answer or "").split("neq", 1)[-1] if "neq" in (answer or "") else ""
        if "≠" in (answer or "") and "neq" not in (answer or ""):
            tail = (answer or "").split("≠", 1)[-1]
        excl_vals = 1 + tail.count(",")
        feats["n_excluded"] = excl_vals
        e += 1.5 * excl_vals
    else:
        feats["n_excluded"] = 0
    # Answer still a ratio (didn't cancel to a polynomial).
    if "frac" in (answer or ""):
        e += 2.0
        feats["ratio_answer"] = True
    # Large expanded coefs are secondary (error-prone arithmetic).
    coefs = [abs(int(x)) for x in re.findall(r"(?<!\\)(?<!\\^)-?\d+", prompt)]
    if coefs and max(coefs) >= 100:
        e += 2.0
        feats["large_coef"] = True
    return round(min(e, 25.0), 1), feats


# ---------------------------------------------------------------------------
# Algebra 1 first-family scorers (rational / percent / sci / verbal / OOO)
# ---------------------------------------------------------------------------


def effort_percent_of_change(prompt: str, answer: str) -> tuple[float, dict]:
    """Percent increase/decrease — direction + awkward % of base, not |n|."""
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    if "increase" in pl:
        e += 1.0
        feats["dir"] = "increase"
    elif "decrease" in pl:
        e += 1.5
        feats["dir"] = "decrease"
    nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)", prompt)]
    feats["nums"] = nums[:4]
    if len(nums) >= 2:
        a, b = nums[0], nums[1]
        base = a if a else 1.0
        pct = abs(b - a) / base * 100.0
        feats["pct_change"] = round(pct, 2)
        nearest = round(pct)
        if abs(pct - nearest) > 0.05:
            e += 4.0
            feats["awkward"] = True
        elif nearest % 5 != 0:
            e += 2.5
        elif nearest not in (10, 20, 25, 50, 75, 100):
            e += 1.5
        if max(a, b) >= 100:
            e += 1.5
        if max(a, b) >= 500:
            e += 1.5
        # Tiny relative change (e.g. 20→19) is more error-prone than 50%.
        if 0 < pct < 10:
            e += 2.0
    # Answer may ask for signed / absolute phrasing.
    if "%" in (answer or "") and re.search(r"\d+\.\d+", answer or ""):
        e += 2.0
    return round(min(e, 25.0), 1), feats


def effort_scientific_notation(prompt: str, answer: str) -> tuple[float, dict]:
    """Sci-notation write / compare / ×÷ / ± — mantissa+exponent structure."""
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 3.0
    exps = [int(x) for x in re.findall(r"10\^\{(-?\d+)\}", prompt)]
    feats["exps"] = exps[:4]
    neg_exp = sum(1 for x in exps if x < 0)
    e += 1.5 * neg_exp

    if "which is greater" in pl or "compare" in pl:
        feats["mode"] = "compare"
        e += 4.0
        if len(exps) >= 2 and (exps[0] < 0) != (exps[1] < 0):
            e += 2.0  # opposite-sign exponents
    elif "write in scientific" in pl or (
        "scientific notation" in pl and "\\times 10" not in prompt.replace(" ", "")
    ):
        feats["mode"] = "write"
        e += 2.0
        m = re.search(r"(\d+(?:\.\d+)?)", prompt)
        if m:
            raw = m.group(1).replace(".", "")
            feats["digits"] = len(raw)
            e += 0.8 * max(0, len(raw) - 2)
            if len(raw) >= 7:
                e += 2.0
    else:
        # Operations between scientific forms.
        if "\\div" in prompt or " / " in prompt:
            feats["op"] = "div"
            e += 5.5
        elif prompt.count("\\times 10") >= 2 and (
            ") \\times (" in prompt.replace(" ", "")
            or ")\\times(" in prompt.replace(" ", "")
            or re.search(r"\)\s*\\times\s*\(", prompt)
        ):
            feats["op"] = "mul"
            e += 4.0
        elif " - " in prompt or re.search(r"\)\s*-\s*\(", prompt):
            feats["op"] = "sub"
            e += 4.0
        else:
            feats["op"] = "add"
            e += 3.5
        if len(exps) >= 2 and exps[0] != exps[1]:
            e += 3.5
            feats["exp_mismatch"] = True
        # Extra mantissa precision.
        mant_digits = [len(x.replace(".", "")) for x in re.findall(r"(\d+\.\d+)", prompt)]
        if mant_digits and max(mant_digits) >= 4:
            e += 1.5
    return round(min(e, 25.0), 1), feats


def effort_order_of_operations(prompt: str, answer: str) -> tuple[float, dict]:
    """OOO evaluate — operator count, exponents, nesting (not raw magnitude)."""
    feats: dict[str, Any] = {}
    e = 3.0
    # Count binary ops (rough).
    ops = len(re.findall(r"\\cdot|\\times|\\div|[+\-]|/", prompt))
    # Avoid double-counting unary minus in exponents like 10^{-3} — rare in OOO.
    feats["ops"] = ops
    e += 1.5 * max(0, ops - 1)
    if "^{" in prompt or re.search(r"\^\d", prompt):
        e += 3.0
        feats["exponent"] = True
    paren = prompt.count("left(") + prompt.count("(")
    feats["parens"] = paren
    e += 2.0 * min(paren, 4)
    # Nested fraction / mixed forms.
    fracs = _parse_fracs(prompt)
    if fracs:
        e += 2.5 * min(len(fracs), 2)
        feats["n_fracs"] = len(fracs)
    return round(min(e, 25.0), 1), feats


def effort_distributive(prompt: str, answer: str) -> tuple[float, dict]:
    """Distributive expand — signs, var outer, fractions."""
    feats: dict[str, Any] = {}
    e = 3.0
    if re.search(r"(?<![a-z])[a-z](?![a-z])", prompt, re.I):
        e += 3.0
        feats["algebraic"] = True
    fracs = _parse_fracs(prompt)
    feats["n_fracs"] = len(fracs)
    e += 2.5 * min(len(fracs), 2)
    # Negatives inside or outside.
    if "-" in prompt:
        e += 1.5
        feats["has_minus"] = True
    paren = prompt.count("left(") + prompt.count("(")
    feats["parens"] = paren
    e += 1.0 * min(paren, 3)
    # Two-term binomial vs longer.
    inner_ops = len(re.findall(r"[+\-]", prompt))
    e += 0.8 * max(0, inner_ops - 1)
    if "frac" in (answer or ""):
        e += 1.5
    return round(min(e, 25.0), 1), feats


def effort_verbal_expressions(prompt: str, answer: str) -> tuple[float, dict]:
    """Verbal → algebra — phrase nesting / consecutive / quantity wrappers."""
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 3.0
    if "consecutive" in pl:
        e += 8.0
        feats["consecutive"] = True
        if "even" in pl or "odd" in pl:
            e += 2.0
    if "quantity" in pl or "the quantity" in pl:
        e += 3.0
        feats["quantity"] = True
    if "twice" in pl or "triple" in pl or "double" in pl:
        e += 2.0
    # Compound phrases (product + more/less, sum of product, …).
    compound_markers = ("more than", "less than", "decreased", "increased", "sum of", "difference")
    hits = sum(1 for m in compound_markers if m in pl)
    feats["compound_hits"] = hits
    e += 2.0 * hits
    if "product" in pl and hits:
        e += 2.0
    ans = answer or ""
    if "(" in ans:
        e += 2.0
        feats["paren_answer"] = True
    if ans.count("x") >= 3 or ans.count("+") >= 2:
        e += 2.0
        feats["multi_term"] = True
    return round(min(e, 25.0), 1), feats


def effort_literal_equations(prompt: str, answer: str) -> tuple[float, dict]:
    """Solve formula / literal for a variable — form depth + isolate cost."""
    feats: dict[str, Any] = {}
    e = 4.0
    # Count distinct letter variables (ignore common latex commands).
    body = re.sub(r"\\[a-zA-Z]+", " ", prompt)
    vars_found = sorted(set(re.findall(r"(?<![a-zA-Z])([A-Za-z])(?![a-zA-Z])", body)))
    feats["n_vars"] = len(vars_found)
    e += 1.8 * max(0, len(vars_found) - 2)
    # Point-slope / slope-intercept style.
    if "solve for" in prompt.lower() and re.search(r"y\s*-\s*.*=.*\(.*x", prompt.replace(" ", "")):
        e += 4.0
        feats["form"] = "point_slope"
    elif re.search(r"V\s*=|A\s*=|P\s*=|C\s*=|F\s*=", prompt):
        e += 2.0
        feats["form"] = "named_formula"
    else:
        feats["form"] = "generic"
    # Product of variables in denominator after isolate (A=ℓw → A/ℓ).
    if "frac" in (answer or ""):
        e += 2.5
        feats["frac_sol"] = True
        rhs = (answer or "").split("=", 1)[-1]
        rhs_clean = re.sub(r"\\[a-zA-Z]+", " ", rhs)
        n_rhs_vars = len(set(re.findall(r"[A-Za-z]", rhs_clean)))
        feats["rhs_vars"] = n_rhs_vars
        e += 1.5 * max(0, n_rhs_vars - 1)
    paren = prompt.count("left(") + prompt.count("(")
    if paren:
        e += 1.5 * min(paren, 2)
        feats["parens"] = paren
    return round(min(e, 25.0), 1), feats


def effort_compound_inequalities(prompt: str, answer: str) -> tuple[float, dict]:
    """Compound inequalities — and vs or + linear vs bare interval."""
    feats: dict[str, Any] = {}
    e = 6.0
    pl = prompt.lower()
    if re.search(r"\bor\b", pl) or r"\text{ or }" in prompt:
        e += 3.0
        feats["style"] = "or"
    elif re.search(r"\band\b", pl) or r"\text{ and }" in prompt:
        e += 2.0
        feats["style"] = "and"
    else:
        # Compact a < x < b form.
        feats["style"] = "interval"
        e += 0.5
    # Two linear sides vs already-isolated.
    linear_hits = len(re.findall(r"-?\d*\s*[a-zA-Z]\s*[+\-]", prompt))
    feats["linearish"] = linear_hits
    e += 2.0 * min(linear_hits, 2)
    if "frac" in (answer or ""):
        e += 1.5
    return round(min(e, 25.0), 1), feats


def effort_absolute_value(prompt: str, answer: str) -> tuple[float, dict]:
    """Absolute value equations / inequalities — nesting + solution branching."""
    feats: dict[str, Any] = {}
    e = 5.0
    # | | markers: \left| or bare |.
    abs_count = prompt.count(r"\left|") + prompt.count(r"|") // 2
    feats["abs_count"] = abs_count
    e += 2.0 * max(0, abs_count - 1)
    # Linear inside: ax+b vs bare x.
    if re.search(r"\|[^|]*[a-zA-Z]\s*[+\-]|\\left\|[^}]*[+\-]", prompt):
        e += 2.5
        feats["shifted"] = True
    if re.search(r"\d+\s*\(|\d+\\left\(|\d+\(", prompt.replace(" ", "")):
        e += 2.0
        feats["factored_inside"] = True
    # Inequality vs equation.
    if re.search(
        r"(?:\\leq|\\geq|\\le(?![a-z])|\\ge(?![a-z])|\\lt|\\gt|(?<![\\a-z])[<>](?![\\a-z]))",
        prompt,
    ):
        e += 2.5
        feats["inequality"] = True
    ans = (answer or "").lower()
    if " or " in ans or r"\text{ or }" in (answer or ""):
        e += 2.0
        feats["two_cases"] = True
    if "frac" in (answer or ""):
        e += 1.5
        feats["rational_sol"] = True
    coefs = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if coefs and max(coefs) >= 20:
        e += 1.5
        feats["large_coef"] = True
    return round(min(e, 25.0), 1), feats


def effort_rational_expression_ops(prompt: str, answer: str) -> tuple[float, dict]:
    """Rational expression ×÷ — op form + expand/cancel load + domain."""
    feats: dict[str, Any] = {}
    e = 6.0
    pl = prompt
    # Op form: multiply · vs ÷ / complex stacked fraction.
    if r"\div" in pl or " \\div " in pl:
        e += 3.0
        feats["op"] = "divide"
    elif pl.strip().startswith(r"\frac{\frac") or pl.strip().startswith(r"\frac{\frac{"):
        e += 4.0
        feats["op"] = "complex_fraction"
    elif r"\cdot" in pl or "·" in pl:
        e += 1.5
        feats["op"] = "multiply"
    else:
        feats["op"] = "other"
        e += 2.0
    # Operand count (· / ÷ markers + stacked).
    n_ops = pl.count(r"\cdot") + pl.count(r"\div")
    if feats.get("op") == "complex_fraction":
        n_ops = max(n_ops, 1)
    feats["n_ops"] = n_ops
    e += 2.0 * max(0, n_ops - 1)
    # Expanded quadratics in prompt → factor-first work.
    degs = [int(x) for x in re.findall(r"\^\{?(\d+)\}?", pl)]
    max_deg = max(degs) if degs else 0
    feats["max_deg"] = max_deg
    e += 2.5 * max(0, max_deg - 1)
    # Non-monic leading coefs in expanded numer/denom.
    if re.search(r"\\frac\{[1-9]\d*[a-zA-Z]\^|\\frac\{[2-9][a-zA-Z]\^", pl):
        e += 2.0
        feats["nonmonic"] = True
    elif re.search(r"(?<![0-9])[2-9]\d*x\^\{?2", pl):
        e += 2.0
        feats["nonmonic"] = True
    # Factored paren density (cancel-visible).
    factor_parens = pl.count("(") + pl.count("left(")
    feats["factor_parens"] = factor_parens
    if factor_parens >= 4 and max_deg <= 1:
        e += 1.0  # already factored — lighter than expanded
        feats["prefactored"] = True
    # Domain / excluded values in answer.
    if "neq" in (answer or "") or "≠" in (answer or ""):
        tail = (answer or "").split("neq", 1)[-1] if "neq" in (answer or "") else ""
        if "≠" in (answer or "") and "neq" not in (answer or ""):
            tail = (answer or "").split("≠", 1)[-1]
        excl = 1 + tail.count(",")
        feats["n_excluded"] = excl
        e += 1.2 * excl
    else:
        feats["n_excluded"] = 0
    if "frac" in (answer or ""):
        e += 1.5
        feats["ratio_answer"] = True
    return round(min(e, 25.0), 1), feats


def effort_radical_add_subtract(prompt: str, answer: str) -> tuple[float, dict]:
    """Radical ± — like vs unsimplified + term count + outer coeffs."""
    feats: dict[str, Any] = {}
    e = 3.0
    # Radical terms.
    insides = [int(x) for x in re.findall(r"\\sqrt\{(\d+)\}", prompt)]
    feats["n_terms"] = max(len(insides), 1)
    e += 1.8 * max(0, len(insides) - 2)
    # Unsimplified: radicand has square factor > 1 (not square-free small set).
    square_free = {2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23, 26, 29, 30, 31}
    unsimplified = [n for n in insides if n not in square_free and n > 1]
    feats["n_unsimplified"] = len(unsimplified)
    if unsimplified:
        e += 3.0 + 1.5 * (len(unsimplified) - 1)
        feats["mode"] = "unsimplified"
    else:
        feats["mode"] = "like"
    # Distinct radicands before simplify.
    feats["n_bases"] = len(set(insides))
    if len(set(insides)) >= 2:
        e += 2.0
        feats["mixed_bases"] = True
    # Outer coefficients present (digit before \sqrt).
    outer_coefs = re.findall(r"(-?\d+)\\sqrt\{", prompt)
    if outer_coefs:
        e += 1.5
        feats["has_outer_coef"] = True
        max_c = max(abs(int(c)) for c in outer_coefs)
        if max_c >= 6:
            e += 1.5
            feats["large_outer"] = True
    # Subtraction mix.
    if "-" in prompt:
        e += 1.0
        feats["has_subtract"] = True
    # Answer still radical vs rationalized fully.
    if "sqrt" in (answer or ""):
        e += 0.5
    return round(min(e, 25.0), 1), feats


def _quad_lead_coef(prompt: str) -> int:
    """Leading coefficient of an ax^2… polynomial stem (1 if monic / bare)."""
    body = prompt.split("of ", 1)[-1] if "discriminant" in prompt.lower() else prompt
    body = body.split("=", 1)[0]
    m = re.search(r"(-?\d+)\s*[a-zA-Z]\^?\{?2", body)
    if m:
        return abs(int(m.group(1)))
    if re.search(r"[a-zA-Z]\^?\{?2", body):
        return 1
    return 1


def effort_quadratic_square_roots(prompt: str, answer: str) -> tuple[float, dict]:
    """Square-root property — form ladder ±√ / (x−h)² / expand-first (EA2e §10.1)."""
    feats: dict[str, Any] = {}
    e = 4.0
    pl = prompt.replace(" ", "")
    ans = answer or ""
    if re.search(r"\([^)]+\)\^\{?2\}?", pl) or re.search(r"\\left\([^)]+\\right\)\^\{?2", prompt):
        feats["form"] = "vertex"
        e += 4.0
        if re.match(r"-?\d+\(", pl) or re.search(r"(?<![a-zA-Z])\d+\\?left?\(", prompt):
            e += 2.5
            feats["scaled_a"] = True
    elif re.search(r"[a-zA-Z]\^\{?2\}?[^=]*=", pl) and not re.search(
        r"[a-zA-Z]\^\{?2\}?[^+-=][+-]", pl.split("=", 1)[0]
    ):
        feats["form"] = "isolated"
        e += 1.5
        if _quad_lead_coef(prompt) > 1:
            e += 1.5
            feats["scaled_a"] = True
    else:
        feats["form"] = "complete_square"
        e += 7.0
        if _quad_lead_coef(prompt) > 1:
            e += 2.0
            feats["scaled_a"] = True
    if "no real" in ans.lower():
        e += 1.5
        feats["no_real"] = True
    if "sqrt" in ans:
        e += 2.0
        feats["irrational"] = True
    if "\\pm" in ans or "pm" in ans:
        e += 0.5
        feats["pm"] = True
    return round(min(e, 25.0), 1), feats


def effort_completing_square_constant(prompt: str, answer: str) -> tuple[float, dict]:
    """Find c for PST — half-b square (EA2e §10.2 find-constant)."""
    feats: dict[str, Any] = {}
    e = 3.0
    compact = prompt.replace(" ", "")
    m = re.search(r"[a-zA-Z]\^\{?2\}?([+-])(\d+)[a-zA-Z]", compact)
    if m:
        b = int(m.group(2))
        feats["abs_b"] = b
        half = b / 2.0
        feats["half_b"] = half
        e += 0.5 * max(0, abs(half) - 2)
        if b % 2 == 1:
            e += 3.0
            feats["odd_b"] = True
    ans = answer or ""
    if "frac" in ans:
        e += 3.0
        feats["frac_c"] = True
    return round(min(e, 25.0), 1), feats


def effort_completing_square_solve(prompt: str, answer: str) -> tuple[float, dict]:
    """Solve by completing the square — lead a≠1 + half-b (EA2e §10.2)."""
    feats: dict[str, Any] = {}
    e = 7.0  # method premium vs factoring
    lead = _quad_lead_coef(prompt)
    feats["lead_coef"] = lead
    if lead > 1:
        e += 3.5
        feats["a_ne_1"] = True
    compact = prompt.replace(" ", "")
    m = re.search(r"[a-zA-Z]\^\{?2\}?[+-](\d+)[a-zA-Z]", compact)
    if m:
        b = abs(int(m.group(1)))
        feats["abs_b"] = b
        e += 0.35 * max(0, b - 6)
    ans = answer or ""
    if "no real" in ans.lower():
        e += 2.0
        feats["no_real"] = True
    if "frac" in ans:
        e += 2.0
        feats["frac_root"] = True
    if "\\pm" in ans or "pm" in ans:
        e += 1.0
        feats["pm"] = True
    if "sqrt" in ans:
        e += 2.0
        feats["irrational"] = True
    return round(min(e, 25.0), 1), feats


def effort_quadratic_formula(prompt: str, answer: str) -> tuple[float, dict]:
    """Quadratic formula — a,b,c identify + radical simplify (EA2e §10.3)."""
    feats: dict[str, Any] = {}
    e = 6.0
    lead = _quad_lead_coef(prompt)
    feats["lead_coef"] = lead
    if lead > 1:
        e += 2.5
        feats["a_ne_1"] = True
    body = prompt.split("=", 1)[0]
    has_linear = bool(
        re.search(r"[+-]\s*\d*[a-zA-Z](?!\^)", body)
        or re.search(r"[+-]\s*[a-zA-Z](?!\^)", body)
    )
    has_const = bool(re.search(r"[+-]\s*\d+\s*$", body.strip()))
    feats["has_linear"] = has_linear
    feats["has_const"] = has_const
    if has_linear and has_const:
        e += 2.0
        feats["full_abc"] = True
    elif has_linear or has_const:
        e += 0.5
    ans = answer or ""
    if "no real" in ans.lower():
        e += 1.5
        feats["no_real"] = True
    if "sqrt" in ans:
        e += 3.0
        feats["radical_simplify"] = True
    if "frac" in ans:
        e += 2.0
        feats["frac_root"] = True
    if ans.count("x") >= 2 or ("," in ans and "x" in ans):
        e += 0.5
    return round(min(e, 25.0), 1), feats


def effort_quadratic_discriminant(prompt: str, answer: str) -> tuple[float, dict]:
    """Discriminant value + root classification (EA2e §10.3)."""
    feats: dict[str, Any] = {}
    e = 4.0
    lead = _quad_lead_coef(prompt)
    feats["lead_coef"] = lead
    if lead > 1:
        e += 1.5
        feats["a_ne_1"] = True
    ans = answer or ""
    m = re.search(r"D\s*=\s*(-?\d+)", ans.replace(" ", ""))
    if m:
        d_val = int(m.group(1))
        feats["disc"] = d_val
        if d_val < 0:
            e += 2.0
            feats["classify"] = "none"
        elif d_val == 0:
            e += 1.0
            feats["classify"] = "one"
        else:
            feats["classify"] = "two"
            root = int(math.isqrt(abs(d_val)))
            if root * root != d_val:
                e += 2.0
                feats["non_square"] = True
            else:
                e += 0.5
    elif "no real" in ans.lower():
        e += 2.0
        feats["classify"] = "none"
    elif "one real" in ans.lower():
        e += 1.0
        feats["classify"] = "one"
    else:
        feats["classify"] = "two"
        e += 1.0
    return round(min(e, 25.0), 1), feats


def effort_radical_multiply(prompt: str, answer: str) -> tuple[float, dict]:
    """Radical × — product rule / coeffs / FOIL (EA2e §9.4)."""
    feats: dict[str, Any] = {}
    e = 3.0
    insides = [int(x) for x in re.findall(r"\\sqrt\{(\d+)\}", prompt)]
    feats["n_radicals"] = len(insides)
    if prompt.count("(") + prompt.count("left(") >= 2 and ("+" in prompt or "-" in prompt):
        feats["mode"] = "binomial"
        e += 7.0
    elif re.search(r"(-?\d+)\\sqrt\{", prompt):
        feats["mode"] = "coeff"
        e += 3.0
        outer = [abs(int(c)) for c in re.findall(r"(-?\d+)\\sqrt\{", prompt)]
        if outer and max(outer) >= 5:
            e += 1.5
            feats["large_outer"] = True
    else:
        feats["mode"] = "simple"
        e += 1.5
    square_free = {2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23, 26, 29, 30, 31}
    if any(n not in square_free and n > 1 for n in insides):
        e += 2.0
        feats["needs_simplify"] = True
    if "sqrt" in (answer or ""):
        e += 0.5
    elif answer and answer.strip() not in {"0"}:
        e += 1.0
        feats["rational_answer"] = True
    return round(min(e, 25.0), 1), feats


def effort_radical_divide(prompt: str, answer: str) -> tuple[float, dict]:
    """Radical ÷ / rationalize — cancel vs conjugate (EA2e §9.5)."""
    feats: dict[str, Any] = {}
    e = 3.5
    insides = [int(x) for x in re.findall(r"\\sqrt\{(\d+)\}", prompt)]
    feats["n_radicals"] = len(insides)
    frac = re.search(
        r"\\frac\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        prompt,
    )
    den = frac.group(2) if frac else ""
    num = frac.group(1) if frac else prompt
    den_sqrts = len(re.findall(r"\\sqrt\{", den))
    num_sqrts = len(re.findall(r"\\sqrt\{", num))
    feats["den_sqrts"] = den_sqrts
    feats["num_sqrts"] = num_sqrts
    den_has_pm = ("+" in den) or (den.count("-") > den.count("^{-"))
    if den_sqrts >= 1 and den_has_pm and ("(" in den or "left" in den or den_sqrts >= 1):
        feats["mode"] = "conjugate"
        e += 7.0
    elif den_sqrts >= 1 and num_sqrts == 0:
        feats["mode"] = "rationalize"
        e += 5.0
    elif den_sqrts >= 1 and num_sqrts >= 1:
        if len(set(insides)) == 1 and len(insides) >= 2:
            feats["mode"] = "reduced"
            e += 1.5
        else:
            feats["mode"] = "simplify_quotient"
            e += 3.5
    else:
        feats["mode"] = "other"
        e += 2.0
    if re.search(r"(-?\d+)\\sqrt\{", prompt):
        e += 1.5
        feats["has_outer_coef"] = True
    if "sqrt" in (answer or ""):
        e += 1.0
        feats["radical_answer"] = True
    return round(min(e, 25.0), 1), feats


def effort_radical_equations(prompt: str, answer: str) -> tuple[float, dict]:
    """Radical equations — isolate / square / extraneous (EA2e §9.6)."""
    feats: dict[str, Any] = {}
    e = 5.0
    n_sqrt = prompt.count("\\sqrt") + prompt.count("sqrt(")
    feats["n_sqrt"] = n_sqrt
    if n_sqrt >= 2:
        e += 6.0
        feats["form"] = "two_radicals"
    else:
        rhs = prompt.split("=", 1)[-1] if "=" in prompt else ""
        lhs = prompt.split("=", 1)[0] if "=" in prompt else prompt
        rhs_has_x = bool(re.search(r"[a-zA-Z]", rhs))
        if re.search(r"(?<![a-zA-Z])\d+\\sqrt", prompt.replace(" ", "")):
            e += 2.5
            feats["scaled_radical"] = True
        if rhs_has_x and "sqrt" not in rhs:
            e += 4.0
            feats["form"] = "radical_equals_linear"
        elif re.search(r"[+-]\s*\d+", lhs) and "sqrt" in lhs:
            e += 2.0
            feats["form"] = "light_prep"
        else:
            feats["form"] = "isolate"
            e += 1.5
    ans = answer or ""
    if "extraneous" in ans.lower():
        e += 3.0
        feats["extraneous"] = True
    if "no solution" in ans.lower() or "no real" in ans.lower():
        e += 2.0
        feats["no_solution"] = True
    return round(min(e, 25.0), 1), feats


def effort_rational_equations(prompt: str, answer: str) -> tuple[float, dict]:
    """Rational equations — clear dens + extraneous (EA2e §8.6)."""
    feats: dict[str, Any] = {}
    e = 5.0
    n_fracs = prompt.count("frac{")
    feats["n_fracs"] = n_fracs
    if n_fracs >= 2:
        left = prompt.split("=", 1)[0]
        if left.count("frac{") >= 2:
            feats["form"] = "two_fractions"
            e += 5.5
        elif re.search(r"\\frac.*=\s*\\frac", prompt):
            feats["form"] = "proportion"
            e += 3.0
        else:
            feats["form"] = "two_fractions"
            e += 5.5
    elif n_fracs == 1:
        left = prompt.split("=", 1)[0] if "=" in prompt else prompt
        # Constant ± single fraction on a side.
        if re.search(r"(?<!frac)(?<!\{)\d+\s*[+-]\s*\\frac|[+-]\s*\\frac", left):
            feats["form"] = "fraction_plus_constant"
            e += 3.5
        else:
            feats["form"] = "simple_fraction"
            e += 1.5
    else:
        feats["form"] = "other"
        e += 2.0
    if re.search(
        r"\\frac\{[^}]+\}\{[^{}]*[a-zA-Z]\s*[+-]|\\frac\{[^}]+\}\{\\left",
        prompt,
    ) or re.search(r"\\frac\{[^}]+\}\{[^{}]*[+-][^}]*[a-zA-Z]", prompt):
        e += 2.0
        feats["linear_den"] = True
    ans = answer or ""
    if "extraneous" in ans.lower():
        e += 3.5
        feats["extraneous"] = True
    if "no solution" in ans.lower():
        e += 2.0
        feats["no_solution"] = True
    if "frac" in ans:
        e += 1.5
        feats["frac_root"] = True
    return round(min(e, 25.0), 1), feats


def effort_poly_long_division(prompt: str, answer: str) -> tuple[float, dict]:
    """Polynomial ÷ polynomial — degree gap + remainder (EA2e §6.5–6.6)."""
    feats: dict[str, Any] = {}
    e = 5.0
    degs = [int(x) for x in re.findall(r"\^\{?(\d+)\}?", prompt)]
    num_deg = max(degs) if degs else 1
    # Denominator often lower degree; estimate from second poly chunk.
    parts = re.split(r"\}\{", prompt.replace(" ", ""), maxsplit=1)
    if len(parts) == 2:
        den_degs = [int(x) for x in re.findall(r"\^\{?(\d+)\}?", parts[1])]
        den_deg = max(den_degs) if den_degs else (1 if re.search(r"[a-zA-Z]", parts[1]) else 0)
    else:
        den_deg = 1
    feats["num_deg"] = num_deg
    feats["den_deg"] = den_deg
    gap = max(0, num_deg - den_deg)
    feats["deg_gap"] = gap
    e += 2.2 * gap + 1.5 * max(0, den_deg - 1)
    ans = answer or ""
    if "+" in ans and ("frac" in ans or "/" in ans or "remainder" in ans.lower()):
        e += 4.0
        feats["remainder"] = True
    elif re.search(r"\\frac\{[^}]+\}\{", ans) and re.search(r"[a-zA-Z]", ans):
        e += 4.0
        feats["remainder"] = True
    terms = len(re.findall(r"[+-]", prompt)) + 1
    feats["n_terms"] = terms
    if terms >= 6:
        e += 2.0
    elif terms >= 4:
        e += 1.0
    coefs = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if coefs and max(coefs) >= 20:
        e += 1.5
        feats["large_coef"] = True
    return round(min(e, 25.0), 1), feats


def effort_radical_simplification(prompt: str, answer: str) -> tuple[float, dict]:
    """Simplify √n — perfect-square factor size (EA2e §9.1–9.2)."""
    e, feats = effort_squares_roots(prompt, answer)
    feats["skill"] = "simplify"
    m = re.search(r"sqrt\{(\d+)\}", prompt) or re.search(r"sqrt\((\d+)\)", prompt)
    if m:
        rad = int(m.group(1))
        feats["radicand"] = rad
        # Larger extractable squares → more bookkeeping.
        sq = max(
            (s for s in (4, 9, 16, 25, 36, 49, 64, 81, 100) if rad % s == 0 and s < rad),
            default=1,
        )
        feats["outer_sq"] = sq
        if sq >= 36:
            e += 3.0
        elif sq >= 16:
            e += 2.0
        elif sq >= 4:
            e += 1.0
        if rad >= 200:
            e += 1.5
        if rad >= 500:
            e += 1.5
    if re.search(r"sqrt\[\d+\]", prompt) or re.search(r"\\sqrt\[\d+\]", prompt):
        e += 4.0
        feats["higher_index"] = True
    return round(min(e, 25.0), 1), feats


def effort_wp_mixture(prompt: str, answer: str) -> tuple[float, dict]:
    """Mixture WP — percent vs cost blend + amount awkwardness."""
    feats: dict[str, Any] = {}
    pl = prompt.lower()
    e = 6.0
    if "cost" in pl or "per lb" in pl or "$" in prompt or r"\$" in prompt:
        e += 3.5
        feats["kind"] = "cost"
    else:
        e += 1.5
        feats["kind"] = "percent"
    nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)", prompt)]
    feats["n_nums"] = len(nums)
    if nums:
        mx = max(nums)
        feats["max_num"] = mx
        if mx >= 40:
            e += 1.5
        if mx >= 75:
            e += 1.5
    # Awkward mixture rates: percents next to \% or dollar costs.
    pcts = [int(x) for x in re.findall(r"(\d+)\\?%", prompt)]
    costs = [int(x) for x in re.findall(r"\\?\$(\d+)", prompt)]
    rates = pcts or costs
    if rates and any(r % 5 != 0 for r in rates):
        e += 2.0
        feats["awkward_rate"] = True
    ans = answer or ""
    if "." in ans or re.search(r"\d+\.\d+", ans):
        e += 2.0
        feats["decimal_ans"] = True
    return round(min(e, 25.0), 1), feats


def effort_wp_distance_rate_time(prompt: str, answer: str) -> tuple[float, dict]:
    """DRT WP — find-missing vs round-trip / opposite / catch-up."""
    feats: dict[str, Any] = {}
    pl = prompt.lower()
    e = 6.0
    if "returns" in pl or "round trip" in pl or "way back" in pl or "trip there" in pl:
        e += 3.5
        feats["mode"] = "round_trip"
    elif "opposite" in pl or "toward each other" in pl or "towards each other" in pl:
        e += 4.5
        feats["mode"] = "opposite"
    elif "catch" in pl or ("same direction" in pl) or ("leaves" in pl and "later" in pl):
        e += 5.0
        feats["mode"] = "catch_up"
    elif "two" in pl and ("leg" in pl or "segment" in pl or "then" in pl):
        e += 4.0
        feats["mode"] = "two_segments"
    else:
        e += 1.5
        feats["mode"] = "find_missing"
    rates = [int(x) for x in re.findall(r"(\d+)\s*(?:mi|km|m|ft)?\s*/\s*(?:hr|h|min)", pl)]
    if not rates:
        rates = [int(x) for x in re.findall(r"(\d+)\s*(?:mph|km/h)", pl)]
    if rates:
        feats["rates"] = rates[:3]
        if max(rates) >= 50:
            e += 1.5
        if any(r % 5 != 0 for r in rates):
            e += 1.5
            feats["awkward_rate"] = True
    if "min" in pl:
        e += 1.0
        feats["time_min"] = True
    return round(min(e, 25.0), 1), feats


def effort_wp_work(prompt: str, answer: str) -> tuple[float, dict]:
    """Work WP — together / find-one / three / pipes / starts-later."""
    feats: dict[str, Any] = {}
    pl = prompt.lower()
    e = 6.5
    if "pipe" in pl or ("fill" in pl and "tank" in pl):
        e += 5.0
        feats["mode"] = "pipes"
    elif "later" in pl or ("starts" in pl and "after" in pl):
        e += 4.5
        feats["mode"] = "starts_later"
    elif re.search(r"\bthree\b", pl) or pl.count("can finish") >= 3:
        e += 4.0
        feats["mode"] = "three"
    elif ("how long does it take" in pl and "alone" in pl) or "working alone" in pl:
        e += 3.0
        feats["mode"] = "find_one"
    elif "working together" in pl or "work together" in pl:
        e += 2.0
        feats["mode"] = "together"
    else:
        e += 2.5
        feats["mode"] = "other"
    times = [int(x) for x in re.findall(r"(\d+)\s*(?:hr|hour|min)", pl)]
    if times:
        feats["times"] = times[:4]
        if max(times) >= 18:
            e += 1.5
        if any(t % 3 != 0 and t % 2 != 0 for t in times):
            e += 1.0
    if "min" in pl:
        e += 0.5
    return round(min(e, 25.0), 1), feats


def effort_wp_coin(prompt: str, answer: str) -> tuple[float, dict]:
    """Coin WP — shape complexity (denoms / relations / trade) over magnitude."""
    feats: dict[str, Any] = {"kind": "coin"}
    pl = prompt.lower()
    e = 5.5
    denoms = 0
    for name in ("quarter", "dime", "nickel", "penny", "pennies"):
        if name in pl:
            denoms += 1
    feats["denoms"] = denoms
    e += 1.0 * max(denoms - 1, 0)
    if denoms >= 3:
        e += 2.5
        feats["three_denoms"] = True
    if "twice" in pl or "times as many" in pl:
        e += 2.5
        feats["ratio"] = True
    if "more" in pl and ("than" in pl):
        e += 2.0
        feats["diff_rel"] = True
    if "traded" in pl or "added" in pl and "removed" in pl:
        e += 4.0
        feats["trade"] = True
    if "total value" in pl or "worth" in pl and "how many" not in pl:
        e += 1.0
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    if nums:
        feats["max_num"] = max(nums)
        if max(nums) >= 20:
            e += 1.0
        if max(nums) >= 40:
            e += 1.0
    if re.search(r"\$\d+\.\d*[1-9]", prompt) or re.search(r"\\\$\d+\.\d*[1-9]", prompt):
        e += 1.5
        feats["awkward_cents"] = True
    return round(min(e, 25.0), 1), feats


def effort_wp_age(prompt: str, answer: str) -> tuple[float, dict]:
    """Age WP — time shift / times-as-old / three-person cues."""
    feats: dict[str, Any] = {"kind": "age"}
    pl = prompt.lower()
    e = 5.5
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    if nums:
        feats["max_num"] = max(nums)
        if max(nums) >= 20:
            e += 1.5
        if max(nums) >= 40:
            e += 1.5
    if "older" in pl or "younger" in pl:
        e += 1.5
        feats["diff"] = True
    if "sum" in pl or "together" in pl or "combined" in pl:
        e += 1.0
        feats["sum"] = True
    if "ago" in pl or re.search(r"\bin\s+\d+\s+years?\b", pl):
        e += 2.5
        feats["time_shift"] = True
    if "twice as old" in pl or "times as old" in pl:
        e += 3.0
        feats["times"] = True
    # Three named people ≈ two "is N years older" clauses.
    if pl.count("older than") >= 2:
        e += 3.5
        feats["three_people"] = True
    ans = answer or ""
    if "frac" in ans or "/" in ans:
        e += 2.0
        feats["frac_ans"] = True
    return round(min(e, 25.0), 1), feats


def effort_wp_consecutive(prompt: str, answer: str) -> tuple[float, dict]:
    """Consecutive-integer WP — count / parity / product vs sum."""
    feats: dict[str, Any] = {"kind": "consecutive"}
    pl = prompt.lower()
    e = 5.0
    if "even" in pl:
        e += 2.0
        feats["parity"] = "even"
    elif "odd" in pl:
        e += 2.0
        feats["parity"] = "odd"
    else:
        feats["parity"] = "any"
        e += 0.5
    count = 2
    for word, n in (
        ("five", 5),
        ("four", 4),
        ("three", 3),
        ("two", 2),
    ):
        if word in pl:
            count = n
            break
    feats["count"] = count
    e += 1.0 * (count - 2)
    if "product" in pl:
        e += 3.5
        feats["goal"] = "product"
    elif "first and last" in pl or "first and the last" in pl:
        e += 2.0
        feats["goal"] = "sum_first_last"
    else:
        e += 1.0
        feats["goal"] = "sum"
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    if nums and max(nums) >= 50:
        e += 1.5
        feats["large_clue"] = True
    return round(min(e, 25.0), 1), feats


def effort_evaluating_functions(prompt: str, answer: str) -> tuple[float, dict]:
    """Evaluate f(a) — family + input awkwardness (prompt-based; graph is stimulus)."""
    feats: dict[str, Any] = {}
    e = 3.5
    pl = prompt.lower()
    if "x^{2}" in prompt or "x^2" in prompt or "^{2}" in prompt:
        e += 3.0
        feats["family"] = "quadratic"
    elif "abs" in pl or "|x|" in prompt or r"\left|" in prompt:
        e += 2.5
        feats["family"] = "abs"
    elif "sqrt" in pl:
        e += 3.5
        feats["family"] = "radical"
    else:
        feats["family"] = "linear"
        e += 1.0
    # Input value magnitude / sign.
    m = re.search(r"f\s*\(\s*(-?\d+)\s*\)", prompt) or re.search(
        r"find\s*\}?\s*f\s*\(\s*(-?\d+)", pl
    )
    if m:
        a = int(m.group(1))
        feats["input"] = a
        if a < 0:
            e += 1.5
        if abs(a) >= 10:
            e += 1.0
        if abs(a) >= 20:
            e += 1.0
    if "frac" in prompt:
        e += 2.0
        feats["frac_coef"] = True
    return round(min(e, 25.0), 1), feats


def effort_graph_linear_equation(prompt: str, answer: str) -> tuple[float, dict]:
    """Graph y=mx+b / Ax+By=C — form complexity from the prompt equation."""
    feats: dict[str, Any] = {}
    e = 4.0
    pl = prompt.lower()
    if "standard" in pl or re.search(r"\d+\s*x\s*[+-]\s*\d+\s*y\s*=", prompt):
        e += 3.0
        feats["form"] = "standard"
    elif "frac" in prompt:
        e += 2.5
        feats["form"] = "fractional_slope"
    elif re.search(r"y\s*=", prompt):
        feats["form"] = "slope_intercept"
        e += 1.0
    else:
        feats["form"] = "other"
        e += 1.5
    if re.search(r"-\s*(\\frac|\d|[a-z])", prompt) or "=-" in prompt.replace(" ", ""):
        e += 1.0
        feats["negative"] = True
    coefs = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if coefs and max(coefs) >= 8:
        e += 1.5
    return round(min(e, 25.0), 1), feats


def effort_a2_exp_equation(prompt: str, answer: str) -> tuple[float, dict]:
    """A2 exponential equations — matching bases vs coef-on-exponent."""
    from question_engine.ml.effort_calc import effort_exp_equation

    e, feats = effort_exp_equation(prompt, answer)
    # ``3^{3x}`` / ``2^{5x}`` — rearrange then divide (or take log).
    if re.search(r"\^\{\d+[a-zA-Z]", prompt):
        e += 3.5
        feats["coef_on_exponent"] = True
    elif re.search(r"\^\{[a-zA-Z]", prompt) or re.search(r"\^[a-zA-Z]\b", prompt):
        feats["plain_exponent"] = True
    bases = re.findall(r"(\d+)\^\{", prompt)
    if bases:
        try:
            b = int(bases[0])
            feats["base"] = b
            if b >= 7:
                e += 1.0
        except ValueError:
            pass
    rhs = re.findall(r"=\s*(\d+)", prompt.replace(" ", ""))
    if rhs:
        try:
            rval = int(rhs[0])
            # Store magnitude only — raw RHS can be 6^{25}+ and poison float32 ML.
            feats["rhs_log10"] = round(math.log10(max(rval, 1)), 3)
            if rval >= 1000:
                e += 1.5
            if rval >= 10000:
                e += 1.5
        except ValueError:
            pass
    return round(min(e, 25.0), 1), feats


def effort_a2_log_equation(prompt: str, answer: str) -> tuple[float, dict]:
    """A2 logarithmic equations — evaluate scorer + solve premium."""
    from question_engine.ml.effort_calc import effort_log_evaluate

    e, feats = effort_log_evaluate(prompt, answer)
    e += 2.5
    feats["equation"] = True
    if r"\ln" in prompt:
        e += 1.0
    if "=" in prompt and "x" in prompt:
        feats["solve_for_x"] = True
    ans = answer or ""
    if "extraneous" in ans.lower():
        e += 3.0
        feats["extraneous"] = True
    m = re.search(r"x\s*=\s*(\d+)", ans.replace(" ", ""))
    if m and int(m.group(1)) >= 10000:
        e += 2.0
        feats["large_solution"] = True
    return round(min(e, 25.0), 1), feats


def effort_graph_linear(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Graph y=mx+b / linear inequality — slope & intercept complexity."""
    _ = answer
    feats: dict[str, Any] = {"family": "linear"}
    e = 3.0
    pl = prompt.lower()
    if "cases" in pl or prompt.count("y ") >= 2 or prompt.count("y\\") >= 2:
        e += 3.0
        feats["system"] = True
    if "inequal" in pl or any(s in prompt for s in (r"\le", r"\ge", r"\lt", r"\gt", "≤", "≥", "<", ">")):
        e += 2.0
        feats["inequality"] = True
    if "frac" in prompt:
        e += 2.5
        feats["fractional"] = True
    nums = [int(x) for x in re.findall(r"-?\d+", prompt)]
    if any(n < 0 for n in nums):
        e += 1.0
        feats["negative"] = True
    if any(abs(n) >= 5 for n in nums):
        e += 1.0
        feats["large_coef"] = True
    # Bare y=x or y=-x is easy.
    if re.search(r"y\s*=\s*-?x\b", prompt.replace(" ", "")) and len(nums) <= 1:
        e = min(e, 3.5)
        feats["parent_like"] = True
    return round(min(e, 25.0), 1), feats


def effort_graph_transform(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Graph abs / radical / rational / quadratic / exp / log — transform depth."""
    _ = answer
    feats: dict[str, Any] = {}
    e = 4.0
    p = prompt
    if "|" in p or "lvert" in p or "abs" in p.lower():
        feats["kind"] = "abs"
        e += 1.0
    elif "sqrt" in p:
        feats["kind"] = "radical"
        e += 1.5
    elif "frac" in p and "log" not in p and "x^2" not in p.replace(" ", "") and "x^{2}" not in p:
        feats["kind"] = "rational"
        e += 2.0
    elif "log" in p:
        feats["kind"] = "log"
        e += 2.0
    elif re.search(r"\^\{?[xX]", p) or re.search(r"\d+\^\{?x", p):
        feats["kind"] = "exp"
        e += 2.0
    elif "x^2" in p.replace(" ", "") or "x^{2}" in p or re.search(
        r"\([^)]*x[^)]*\)\s*\^\s*\{?2\}?", p
    ) or ")^2" in p.replace(" ", "") or ")^{2}" in p:
        feats["kind"] = "quadratic"
        e += 1.5
        # Standard / factored / messy form premiums for graphing.
        if re.search(r"x\s*\(|\)\s*\(", p) or ")(" in p.replace(" ", ""):
            e += 2.0
            feats["form"] = "factored"
        elif re.search(r"[+-]\s*\d+\s*x\b", p) or re.search(r"[+-]\s*\d+x\b", p.replace(" ", "")):
            e += 2.5
            feats["form"] = "standard"
        elif "(" in p and (")^2" in p.replace(" ", "") or ")^{2}" in p):
            feats["form"] = "vertex"
        else:
            feats["form"] = "other"
    else:
        feats["kind"] = "other"

    # Horizontal / vertical shifts: (x±h) or +k outside.
    if re.search(r"x\s*[+\-]", p) or re.search(r"\(x[+\-]", p):
        e += 2.0
        feats["h_shift"] = True
    nums = [int(x) for x in re.findall(r"-?\d+", p)]
    # Outside constant term (rough): trailing ±k after the main form.
    if re.search(r"(\)|\}|x)\s*[+\-]\s*\d+", p) or re.search(r"\^\{\s*x\s*\}\s*[+\-]", p):
        e += 1.5
        feats["k_shift"] = True
    if any(abs(n) >= 2 and n not in (10,) for n in nums) and (
        re.search(r"(?<![_\^])-?\d+\s*(\\?sqrt|\\?left\||\|)", p)
        or re.search(r"y\s*=\s*-?\d+", p)
    ):
        e += 1.5
        feats["stretch"] = True
    if "-" in p and ("sqrt" in p or "|" in p or "frac" in p or "x^2" in p.replace(" ", "") or "x^{2}" in p):
        # Reflection cue: leading negative stretch.
        if re.search(r"y\s*=\s*-", p.replace(" ", "")):
            e += 1.0
            feats["reflection"] = True
    if any(s in p for s in (r"\le", r"\ge", r"\lt", r"\gt", "≤", "≥", "<", ">")):
        e += 2.0
        feats["inequality"] = True
    return round(min(e, 25.0), 1), feats


def effort_graph_trig(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Graph trig y=A sin/cos (bx − phase) — amplitude / period / phase."""
    _ = answer
    feats: dict[str, Any] = {"family": "trig"}
    e = 4.0
    if re.search(r"(sin|cos|tan)", prompt):
        feats["fn"] = re.search(r"(sin|cos|tan)", prompt).group(1)  # type: ignore[union-attr]
    nums = [int(x) for x in re.findall(r"-?\d+", prompt)]
    if any(abs(n) >= 2 for n in nums):
        e += 2.0
        feats["amplitude"] = True
    if re.search(r"(sin|cos|tan)\s*\\?left\(|\\(sin|cos|tan)\\left\(", prompt) or re.search(
        r"(sin|cos|tan)\([^x]*x", prompt
    ):
        e += 2.5
        feats["period_or_arg"] = True
    if "pi" in prompt or r"\pi" in prompt:
        e += 2.0
        feats["phase"] = True
    if re.search(r"y\s*=\s*-", prompt.replace(" ", "")) or prompt.strip().startswith("-"):
        e += 1.0
        feats["reflection"] = True
    return round(min(e, 25.0), 1), feats


def effort_growth_decay(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Exponential growth/decay word problems — rate, periods, ask mode."""
    feats: dict[str, Any] = {}
    e = 5.0
    pl = prompt.lower()
    if "decay" in pl or "half" in pl:
        e += 1.0
        feats["decay"] = True
    else:
        feats["growth"] = "growth" in pl or "invest" in pl or "population" in pl
    nums = [int(x) for x in re.findall(r"-?\d+", prompt)]
    rates = [n for n in nums if 1 <= n <= 50]
    periods = [n for n in nums if n > 50 or (n >= 2 and n not in rates[:1])]
    if rates:
        r = max(rates)
        feats["rate"] = r
        e += 0.15 * max(0, r - 5)
    if any(n >= 8 for n in nums):
        e += 1.5
        feats["long_horizon"] = True
    if "rate" in pl and ("need" in pl or "what" in pl):
        e += 4.0
        feats["mode"] = "find_rate"
    elif "how many" in pl and ("year" in pl or "hour" in pl or "period" in pl):
        e += 3.5
        feats["mode"] = "find_periods"
    elif "initial" in pl or "start" in pl and "find" in pl:
        e += 3.0
        feats["mode"] = "find_initial"
    elif "half" in pl:
        e += 4.0
        feats["mode"] = "half_life"
    elif "more" in pl or "difference" in pl or "compare" in pl:
        e += 3.0
        feats["mode"] = "compare"
    else:
        feats["mode"] = "find_final"
    if "continuous" in pl or "e^{" in prompt or r"e^" in prompt:
        e += 2.5
        feats["continuous"] = True
    # Answer magnitude as proxy for computation load.
    try:
        aval = float(re.sub(r"[^\d.\-]", "", (answer or "").split()[0] or "0") or 0)
        if aval >= 1000:
            e += 1.5
            feats["large_answer"] = True
    except (ValueError, IndexError):
        pass
    return round(min(e, 25.0), 1), feats


def effort_inverse_exp_log(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Find inverse of shifted exp / log functions."""
    _ = answer
    feats: dict[str, Any] = {}
    e = 6.0
    if "log" in prompt and ("Find the inverse" in prompt or "inverse" in prompt.lower()):
        # Distinguishing whether the given is exp or log.
        if re.search(r"\d+\^\{", prompt) or re.search(r"\^\{\s*x", prompt):
            feats["given"] = "exp"
            e += 1.0
        else:
            feats["given"] = "log"
            e += 1.5
    nums = [int(x) for x in re.findall(r"-?\d+", prompt)]
    if any(n not in (0, 1, -1) and abs(n) >= 2 for n in nums):
        e += 1.5
        feats["shifts"] = True
    if any(abs(n) >= 5 for n in nums):
        e += 1.0
        feats["large_shift_or_base"] = True
    if "10" in nums or 10 in nums:
        e += 0.5
        feats["base_10"] = True
    return round(min(e, 25.0), 1), feats


def effort_matrix_ops(prompt: str, answer: str = "") -> tuple[float, dict]:
    """2×2 matrix add/subtract/scalar — entry magnitude + op."""
    _ = answer
    feats: dict[str, Any] = {}
    e = 3.5
    if r"cdot" in prompt or re.search(r"^\s*-?\d+\s*\\begin\{pmatrix\}", prompt):
        e += 1.5
        feats["op"] = "scalar"
    elif "-" in prompt.split(r"pmatrix")[0] if "pmatrix" in prompt else False:
        e += 1.0
        feats["op"] = "subtract"
    else:
        feats["op"] = "add"
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_entry"] = max(nums)
        e += 0.35 * max(0, max(nums) - 3)
    if prompt.count("pmatrix") >= 4 or prompt.count(r"\\") >= 2:
        e += 0.5
    return round(min(e, 25.0), 1), feats


def effort_matrix_inverse(prompt: str, answer: str = "") -> tuple[float, dict]:
    """2×2 matrix inverse — det size / fraction."""
    feats: dict[str, Any] = {"op": "inverse"}
    e = 7.0
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_entry"] = max(nums)
        e += 0.4 * max(0, max(nums) - 2)
    if "frac" in (answer or "") or (answer or "").startswith(r"\frac"):
        e += 1.5
        feats["frac_det"] = True
    det_m = re.search(r"\\frac\{1\}\{(-?\d+)\}", answer or "")
    if det_m and abs(int(det_m.group(1))) >= 4:
        e += 1.5
        feats["large_det"] = True
    return round(min(e, 25.0), 1), feats


def effort_matrix_cramer(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Cramer's rule 2×2 — coef size."""
    _ = answer
    feats: dict[str, Any] = {"op": "cramer"}
    e = 8.0
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_coef"] = max(nums)
        e += 0.3 * max(0, max(nums) - 3)
    if "cases" in prompt:
        e += 0.5
    return round(min(e, 25.0), 1), feats


def effort_conic(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Conic classify / write / properties — translated + axis size."""
    feats: dict[str, Any] = {}
    e = 5.0
    pl = prompt.lower()
    if "classify" in pl:
        e += 2.0
        feats["mode"] = "classify"
    elif "write" in pl:
        e += 3.0
        feats["mode"] = "write"
    else:
        feats["mode"] = "properties"
    if "ellipse" in pl or (r"\frac" in prompt and "+" in prompt and "=1" in prompt.replace(" ", "")):
        feats["kind"] = "ellipse"
        e += 1.5
    elif "hyperbola" in pl or (r"\frac" in prompt and "-" in prompt and "=1" in prompt.replace(" ", "")):
        feats["kind"] = "hyperbola"
        e += 2.0
    elif "circle" in pl or "radius" in pl or "x^2+y^2" in prompt.replace(" ", ""):
        feats["kind"] = "circle"
    elif "parabola" in pl:
        feats["kind"] = "parabola"
        e += 1.0
    # Translated center (h,k) nonzero.
    if re.search(r"\(x-\(|\(x-\(-?\d|center.*\(-?[1-9]", prompt) or re.search(
        r"\(x-\(-?\d", prompt
    ):
        e += 2.5
        feats["translated"] = True
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums and max(nums) >= 16:  # r^2 or a^2 large
        e += 1.0
        feats["large_param"] = True
    if answer and ("center" in answer or "radius" in answer):
        e += 0.5
    return round(min(e, 25.0), 1), feats


def effort_sequence(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Arithmetic/geometric sequences and series — n, |d|/|r|, sum vs term."""
    _ = answer
    feats: dict[str, Any] = {}
    e = 4.0
    pl = prompt.lower()
    if "sum" in pl or "series" in pl:
        e += 3.0
        feats["mode"] = "series"
    elif "mean" in pl:
        e += 2.0
        feats["mode"] = "mean"
        if "geometric" in pl:
            e += 1.5
            feats["geo_mean"] = True
    else:
        feats["mode"] = "nth_term"
    if "geometric" in pl:
        e += 1.5
        feats["kind"] = "geometric"
    elif "arithmetic" in pl:
        feats["kind"] = "arithmetic"
    nums = [int(x) for x in re.findall(r"-?\d+", prompt)]
    # Heuristic: largest positive small int near "th" is n.
    n_m = re.search(r"(\d+)\s*\^\{\\text\{th\}\}|first\s*\}\s*(\d+)|(\d+)\s*\\text\{th\}", prompt)
    if not n_m:
        n_m = re.search(r"(\d+)(?:\^\{?\\mathrm\{th\}|\s*th)", prompt)
    n_val = None
    if n_m:
        for g in n_m.groups():
            if g:
                n_val = int(g)
                break
    if n_val is None and nums:
        # Fall back: pick a plausible n in 3..20.
        candidates = [n for n in nums if 3 <= n <= 24]
        n_val = max(candidates) if candidates else None
    if n_val is not None:
        feats["n"] = n_val
        e += 0.35 * max(0, n_val - 4)
    if any(n < 0 for n in nums):
        e += 1.5
        feats["negative_param"] = True
    if any(abs(n) >= 5 for n in nums if n != n_val):
        e += 1.0
        feats["large_param"] = True
    return round(min(e, 25.0), 1), feats


def effort_law_of_sines_cosines(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Law of Sines / Cosines / triangle area prompts."""
    _ = answer
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    if "area" in pl:
        e = 6.5
        feats["mode"] = "area"
    elif "cosine" in pl:
        e = 7.5
        feats["mode"] = "cosines"
    else:
        e = 6.0
        feats["mode"] = "sines"
    nums = [int(x) for x in re.findall(r"-?\d+", prompt)]
    angles = [n for n in nums if 20 <= abs(n) <= 160]
    sides = [n for n in nums if 1 <= abs(n) <= 40 and n not in angles]
    if angles:
        feats["max_angle"] = max(abs(a) for a in angles)
        e += 0.04 * max(0, feats["max_angle"] - 40)
        if any(a > 90 for a in angles):
            e += 2.0
            feats["obtuse"] = True
    if sides:
        feats["max_side"] = max(abs(s) for s in sides)
        e += 0.15 * max(0, feats["max_side"] - 8)
    return round(min(e, 25.0), 1), feats


def effort_complex_ops(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Complex add/subtract/multiply, modulus, conjugate rationalize, plot."""
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    if "rationalize" in pl or r"\dfrac" in prompt:
        e = 8.0
        feats["mode"] = "rationalize"
        if prompt.count("i") >= 3:
            e += 2.0
            feats["binomial_num"] = True
    elif "plot" in pl or "complex plane" in pl:
        e = 3.5
        feats["mode"] = "graph"
    elif r"\left|" in prompt or "absolute" in pl or "modulus" in pl:
        e = 5.0
        feats["mode"] = "modulus"
        if r"\sqrt" in (answer or ""):
            e += 2.0
            feats["irrational"] = True
    elif ")(" in prompt.replace(" ", "") or r"\right)\left(" in prompt:
        e = 6.5
        feats["mode"] = "multiply"
    else:
        e = 4.5
        feats["mode"] = "add_sub"
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_entry"] = max(nums)
        e += 0.25 * max(0, feats["max_entry"] - 4)
    return round(min(e, 25.0), 1), feats


def effort_planes(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Point-on-plane membership checks."""
    _ = answer
    feats: dict[str, Any] = {"mode": "point_on_plane"}
    e = 5.0
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_abs"] = max(nums)
        e += 0.3 * max(0, feats["max_abs"] - 3)
    if prompt.count("x") + prompt.count("y") + prompt.count("z") >= 3:
        e += 1.0
        feats["three_vars"] = True
    return round(min(e, 25.0), 1), feats


def effort_systems_three(prompt: str, answer: str = "") -> tuple[float, dict]:
    """3×3 linear systems — harder than 2-var systems."""
    e, feats = effort_systems(prompt, answer)
    feats = dict(feats)
    feats["vars"] = 3
    e = float(e) + 4.0
    # Extra equations in cases block.
    n_eq = prompt.count("=")
    if n_eq >= 3:
        e += 1.5
        feats["n_eq"] = n_eq
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_coef"] = max(nums)
        e += 0.2 * max(0, feats["max_coef"] - 4)
    return round(min(e, 25.0), 1), feats


def effort_relations(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Discrete table-complete / continuous evaluate linear relations."""
    _ = answer
    feats: dict[str, Any] = {}
    e = 3.0
    if "array" in prompt or "Complete the table" in prompt:
        feats["mode"] = "discrete_table"
        e += 2.0
        rows = prompt.count("\\\\")
        feats["rows"] = rows
        e += 0.4 * max(0, rows - 3)
    else:
        feats["mode"] = "continuous_eval"
        e += 1.0
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_abs"] = max(nums)
        e += 0.25 * max(0, feats["max_abs"] - 4)
    if re.search(r"-\s*\d|y\s*=\s*-", prompt):
        e += 0.8
        feats["negative"] = True
    return round(min(e, 25.0), 1), feats


def effort_points_3d(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Echo / read 3D point coordinates."""
    _ = answer
    feats: dict[str, Any] = {"mode": "points_3d"}
    e = 2.5
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_abs"] = max(nums)
        e += 0.35 * max(0, feats["max_abs"] - 3)
    if "three dimensions" in prompt.lower() or "P=(" in prompt.replace(" ", ""):
        e += 0.5
    return round(min(e, 25.0), 1), feats


def effort_solve_by_graphing(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Solve polynomial by graphing — degree / factored / leading coef."""
    feats: dict[str, Any] = {"mode": "solve_by_graphing"}
    e = 6.0
    # Factored linear factors vs expanded.
    n_factors = prompt.count("(x") + prompt.count("(x ")
    if n_factors >= 2 or ")(" in prompt.replace(" ", ""):
        feats["form"] = "factored"
        e += 1.0
        if n_factors >= 3:
            e += 2.5
            feats["cubic_plus"] = True
    else:
        feats["form"] = "expanded"
        e += 2.0
    # Degree proxy via x^3 / x^{3}.
    if "x^{3}" in prompt or "x^3" in prompt:
        e += 2.5
        feats["degree"] = 3
    elif "x^{2}" in prompt or "x^2" in prompt:
        feats["degree"] = 2
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_coef"] = max(nums)
        e += 0.25 * max(0, feats["max_coef"] - 3)
    # Multiple roots in answer.
    n_roots = (answer or "").count("x =")
    if n_roots >= 3:
        e += 1.5
        feats["n_roots"] = n_roots
    return round(min(e, 25.0), 1), feats


def effort_binomial_theorem(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Binomial coefficient of x^k in (a+x)^n."""
    feats: dict[str, Any] = {"mode": "binomial"}
    e = 5.0
    n_m = re.search(r"\+\s*x\)\^\{(\d+)\}", prompt) or re.search(r"\+ x\)\^\{(\d+)\}", prompt)
    k_m = re.search(r"x\^\{(\d+)\}", prompt)
    a_m = re.search(r"\((\d+)\s*\+\s*x\)", prompt)
    if n_m:
        n = int(n_m.group(1))
        feats["n"] = n
        e += 0.6 * max(0, n - 3)
    if k_m:
        feats["k"] = int(k_m.group(1))
    if a_m:
        a = int(a_m.group(1))
        feats["a"] = a
        if a >= 3:
            e += 1.5
        if a >= 5:
            e += 1.0
    try:
        aval = abs(int(re.sub(r"[^\d\-]", "", (answer or "").split()[0] or "0") or 0))
        if aval >= 50:
            e += 1.5
            feats["large_coef"] = True
    except (ValueError, IndexError):
        pass
    return round(min(e, 25.0), 1), feats


def effort_remainder_theorem(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Remainder when p(x) divided by (x-a)."""
    _ = answer
    feats: dict[str, Any] = {"mode": "remainder"}
    e = 4.5
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_abs"] = max(nums)
        e += 0.35 * max(0, feats["max_abs"] - 4)
    if "x^{3}" in prompt or "x^3" in prompt:
        e += 2.0
        feats["cubic"] = True
    return round(min(e, 25.0), 1), feats


def effort_polynomial_writing(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Write poly from zeros / conjugate roots."""
    feats: dict[str, Any] = {}
    e = 5.5
    pl = prompt.lower()
    # Complex-root stems mention an imaginary unit after a digit (e.g. ``2i``).
    if re.search(r"\d\s*i\b", prompt) or re.search(r"\di\b", prompt.replace(" ", "")):
        feats["mode"] = "conjugate"
        e += 3.0
    else:
        feats["mode"] = "real_zeros"
        e += 1.0
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_abs"] = max(nums)
        e += 0.3 * max(0, feats["max_abs"] - 3)
    if "leading coefficient" in pl and re.search(r"leading coefficient\s*\}\s*(-?[2-9])", pl):
        e += 1.0
        feats["nonunit_lead"] = True
    return round(min(e, 25.0), 1), feats


def effort_descartes(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Descartes' rule of signs — degree / sign-change density."""
    _ = answer
    feats: dict[str, Any] = {"mode": "descartes"}
    e = 5.0
    # Degree from highest power.
    powers = [int(p) for p in re.findall(r"x\^\{(\d+)\}", prompt)] + (
        [2] if "x^2" in prompt or "x^{2}" in prompt else []
    )
    if powers:
        feats["degree"] = max(powers)
        e += 0.7 * max(0, feats["degree"] - 3)
    nums = [int(x) for x in re.findall(r"-?\d+", prompt)]
    # Sign changes proxy: count minus signs in poly body.
    minus = prompt.count("-")
    feats["minus_marks"] = minus
    e += 0.4 * max(0, minus - 1)
    if nums:
        e += 0.15 * max(0, max(abs(n) for n in nums) - 4)
    return round(min(e, 25.0), 1), feats


def effort_rational_zero(prompt: str, answer: str = "") -> tuple[float, dict]:
    """List possible rational zeros (p/q)."""
    feats: dict[str, Any] = {"mode": "rational_zero"}
    e = 6.0
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_coef"] = max(nums)
        e += 0.35 * max(0, feats["max_coef"] - 3)
    # Candidate list length in answer.
    n_cand = (answer or "").count(",") + (1 if answer and "pm" in answer else 0)
    if n_cand >= 4:
        e += 1.5
        feats["many_candidates"] = True
    if n_cand >= 8:
        e += 1.5
    return round(min(e, 25.0), 1), feats


def effort_fta(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Fundamental Theorem of Algebra — degree recall."""
    _ = answer
    feats: dict[str, Any] = {"mode": "fta"}
    e = 2.0
    m = re.search(r"degree-?\s*\}?\s*(\d+)", prompt) or re.search(r"degree-(\d+)", prompt)
    if m:
        deg = int(m.group(1))
        feats["degree"] = deg
        e += 0.4 * max(0, deg - 3)
    return round(min(e, 25.0), 1), feats


def effort_poly_end_behavior(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Polynomial end behavior from leading term."""
    _ = answer
    feats: dict[str, Any] = {"mode": "end_behavior"}
    e = 4.0
    powers = [int(p) for p in re.findall(r"x\^\{(\d+)\}", prompt)]
    if "x^2" in prompt or "x^{2}" in prompt:
        powers.append(2)
    if powers:
        deg = max(powers)
        feats["degree"] = deg
        e += 0.5 * max(0, deg - 3)
        if deg % 2 == 1:
            e += 1.0
            feats["odd"] = True
    if re.search(r"-\s*\d+x|f\(x\)=-\d|-\d+x\^", prompt):
        e += 1.0
        feats["neg_leading"] = True
    return round(min(e, 25.0), 1), feats


def effort_inverse_function(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Inverse of linear f(x)=mx+b (not exp/log)."""
    feats: dict[str, Any] = {"mode": "inverse_linear"}
    e = 4.5
    if "frac" in (answer or "") or r"\frac" in (answer or ""):
        e += 2.0
        feats["frac_slope"] = True
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_abs"] = max(nums)
        e += 0.3 * max(0, feats["max_abs"] - 3)
    if re.search(r"f\(x\)\s*=\s*-", prompt.replace(" ", "")) or "-x" in prompt:
        e += 1.0
        feats["neg_slope"] = True
    return round(min(e, 25.0), 1), feats


def effort_radical_domain_range(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Domain and range of a√(x−h)+k."""
    _ = answer
    feats: dict[str, Any] = {"mode": "radical_domain_range"}
    e = 5.0
    if re.search(r"-\s*\\sqrt|f\(x\)=-\d|-\d\\sqrt", prompt) or re.search(
        r"=-\d+\\sqrt", prompt.replace(" ", "")
    ):
        e += 2.0
        feats["reflected"] = True
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_abs"] = max(nums)
        e += 0.3 * max(0, feats["max_abs"] - 3)
        if any(n >= 2 for n in nums if n not in (0, 1)):
            # stretch |a|≠1
            if re.search(r"[2-9]\\sqrt|[2-9]\\sqrt", prompt) or re.search(
                r"(?<![0-9])[2-9]\\sqrt", prompt
            ):
                e += 1.0
                feats["stretch"] = True
    return round(min(e, 25.0), 1), feats


def effort_quadratic_system(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Linear–quadratic system (y=x^2 and y=mx+b)."""
    feats: dict[str, Any] = {"mode": "quadratic_system"}
    e = 7.0
    if "x^2" in prompt or "x^{2}" in prompt:
        e += 1.0
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums:
        feats["max_abs"] = max(nums)
        e += 0.3 * max(0, feats["max_abs"] - 3)
    n_pts = (answer or "").count("(")
    if n_pts >= 2:
        e += 1.0
        feats["two_solutions"] = True
    return round(min(e, 25.0), 1), feats


def effort_stats_counting(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Fundamental counting principle word prompts."""
    _ = answer
    feats: dict[str, Any] = {"mode": "counting"}
    e = 3.5
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    feats["n_factors"] = max(2, len(nums))
    e += 1.2 * max(0, feats["n_factors"] - 2)
    if nums:
        feats["product_span"] = max(nums)
        e += 0.15 * max(0, feats["product_span"] - 5)
    return round(min(e, 25.0), 1), feats


def effort_stats_probability(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Independent / mutually exclusive / compound probability."""
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 4.0
    if " or " in pl:
        e = 5.5
        feats["mode"] = "mutually_exclusive"
    elif "both" in pl or " and " in pl or "replace" in pl:
        e = 6.5
        feats["mode"] = "independent"
        if "replace" in pl or "again" in pl:
            e += 1.0
            feats["with_replacement"] = True
    else:
        feats["mode"] = "single"
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    if nums:
        feats["max_count"] = max(nums)
        e += 0.12 * max(0, feats["max_count"] - 6)
    if r"\frac" in (answer or "") or "/" in (answer or ""):
        e += 0.5
    return round(min(e, 25.0), 1), feats


def effort_stats_perm_comb(prompt: str, answer: str = "") -> tuple[float, dict]:
    """Permutations / combinations evaluate or word contexts."""
    _ = answer
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    if "lined up" in pl or "arranged" in pl or "order" in pl:
        feats["mode"] = "perm_word"
        e = 6.5
    elif "chosen" in pl or "committee" in pl or "select" in pl:
        feats["mode"] = "comb_word"
        e = 6.0
    elif "P_" in prompt or r"P_{" in prompt or "permutation" in pl:
        feats["mode"] = "perm"
        e = 5.5
    elif "C_" in prompt or r"C_{" in prompt or "combination" in pl:
        feats["mode"] = "comb"
        e = 5.0
    else:
        feats["mode"] = "mixed"
        e = 6.0
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    if len(nums) >= 2:
        n, r = max(nums), min(nums)
        # Prefer n > r when both look like nPr args.
        candidates = sorted(nums, reverse=True)
        n, r = candidates[0], candidates[1] if candidates[1] < candidates[0] else (
            candidates[0],
            min(candidates[1], 5),
        )
        feats["n"], feats["r"] = n, r
        e += 0.35 * max(0, n - 6) + 0.5 * max(0, r - 2)
    return round(min(e, 25.0), 1), feats


# First-11 G6 ratio/percent Ready topics (verified ramp specs).
EFFORT_SCORERS: dict[str, EffortScorer] = {
    "g6_introduction_to_ratios": effort_intro_ratios,
    "g6_equivalent_ratios": effort_equivalent,
    "g6_part_part_whole_ratios": effort_ppw,
    "g6_comparing_ratios": effort_compare_ratios,
    "g6_unit_rates_and_equivalent_rates": effort_unit_rates,
    "g6_comparing_rates": effort_comparing_rates,
    "g6_converting_units": effort_converting,
    "g6_introduction_to_percents": effort_intro_percents,
    "g6_relating_percents_fractions_and_decimals": effort_relating,
    "g6_finding_percents_with_equivalent_fractions": effort_finding_equiv,
    "g6_solving_percent_problems_with_formulas": effort_formulas,
    # Shared G6 number-lane scorers (also aliased by PA catalog type_ids).
    "g6_factoring": effort_factoring,
    "g6_greatest_common_factor": effort_gcf,
    "g6_least_common_multiple": effort_lcm,
    # PA first-tranche continuous types.
    "pa_integers_adding_and_subtracting": effort_integer_ops,
    "pa_integers_multiplying": effort_integer_ops,
    "pa_integers_dividing": effort_integer_ops,
    "pa_factoring": effort_factoring,
    "pa_greatest_common_factor": effort_gcf,
    "pa_least_common_multiple": effort_lcm,
    "pa_simplifying_fractions": effort_simplify_fractions,
    "pa_converting_fractions_and_decimals": effort_fraction_decimal_convert,
    "pa_fractions_decimals_and_percents": effort_relating,
    "pa_simple_and_compound_interest": effort_interest,
    "pa_naming_decimal_places_and_rounding": effort_place_value_rounding,
    "pa_writing_numbers_with_words": effort_writing_numbers_words,
    "pa_squares_and_square_roots": effort_squares_roots,
    # pa_markup_discount_and_tax: narrative PercentWordProblemFramework (wp_percent unblocked).
    "pa_markup_discount_and_tax": effort_markup_discount,
    # PA second tranche — fraction aliases (OpenStax §4.2/4.4/4.5).
    "pa_fractions_add_like": effort_fraction_ops,
    "pa_fractions_subtract_like": effort_fraction_ops,
    "pa_fractions_add_unlike": effort_fraction_ops,
    "pa_fractions_subtract_unlike": effort_fraction_ops,
    "pa_fractions_multiply": effort_fraction_ops,
    "pa_fractions_divide": effort_fraction_ops,
    # PA second tranche — already_continuous algebra / linear / polys.
    "pa_equations_one_step_word_problems": effort_equations,
    "pa_equations_two_step_word_problems": effort_equations,
    "pa_equations_multi_step_equations": effort_equations,
    "pa_multi_step_inequalities": effort_equations,
    "pa_checking_for_a_proportion": effort_proportions,
    "pa_proportions_word_problems": effort_proportions,
    "pa_slope": effort_slope,
    "pa_writing_linear_equations": effort_linear_write,
    "pa_graphing_systems_of_equations": effort_systems,
    "pa_systems_substitution": effort_systems,
    "pa_systems_word_problems": effort_systems,
    "pa_polynomials_simplifying": effort_polynomials,
    "pa_polynomials_adding_and_subtracting": effort_polynomials,
    "pa_polynomials_multiplying": effort_polynomials,
    # Algebra 1 first family batch (roadmap §1–4).
    "rational_add_subtract": effort_fraction_ops,
    "rational_multiply": effort_fraction_ops,
    "rational_divide": effort_fraction_ops,
    "percents": effort_formulas,
    "percent_of_change": effort_percent_of_change,
    "scientific_notation_write": effort_scientific_notation,
    "scientific_notation_operations": effort_scientific_notation,
    "scientific_notation_add_subtract": effort_scientific_notation,
    "verbal_expressions": effort_verbal_expressions,
    "order_of_operations": effort_order_of_operations,
    "distributive_property": effort_distributive,
    # Algebra 1 second family — equations / proportions / exponents / polys / rationals.
    "one_step_equations": effort_equations,
    "two_step_equations": effort_equations,
    "multi_step_equations": effort_equations,
    "solving_proportions": effort_proportions,
    "properties_of_exponents": effort_properties_of_exponents,
    "polynomial_naming": effort_polynomials,
    "polynomial_add_subtract": effort_polynomials,
    "simplify_polynomials": effort_polynomials,
    "polynomial_multiply": effort_polynomials,
    "polynomial_multiply_special": effort_polynomials,
    "polynomial_factoring_common_factor": effort_poly_gcf,
    "rational_simplification": effort_rational_simplification,
    "rational_expression_simplification": effort_rational_simplification,
    # Algebra 1 — Elementary Algebra 2e follow-up (aliases + factoring ladder).
    "slope": effort_slope,
    "more_on_slope": effort_slope,
    "writing_linear_equations": effort_linear_write,
    "systems_graphing": effort_systems,
    "systems_substitution": effort_systems,
    "systems_elimination": effort_systems,
    "systems_word_problems": effort_systems,
    "polynomial_factoring_grouping": effort_poly_grouping,
    "polynomial_factoring_special_cases": effort_poly_special,
    "quadratic_factoring": effort_quadratic_factoring,
    "polynomial_factoring_general_strategy": effort_poly_general_strategy,
    "quadratic_factoring_equations": effort_quadratic_factor_solve,
    # Algebra 1 — literals / inequality ladder / absolute value.
    "literal_equations": effort_literal_equations,
    "one_step_inequalities": effort_equations,
    "two_step_inequalities": effort_equations,
    "multi_step_inequalities": effort_equations,
    "compound_inequalities": effort_compound_inequalities,
    "absolute_value_equations": effort_absolute_value,
    "absolute_value_inequalities": effort_absolute_value,
    # Algebra 1 — rational ×÷ expressions + radical ±.
    "rational_expression_multiply_divide": effort_rational_expression_ops,
    "radical_add_subtract": effort_radical_add_subtract,
    # Algebra 1 — quadratic methods beyond factoring (EA2e Ch 10).
    "quadratic_square_roots": effort_quadratic_square_roots,
    "quadratic_completing_square_constant": effort_completing_square_constant,
    "quadratic_completing_square_solve": effort_completing_square_solve,
    "quadratic_formula": effort_quadratic_formula,
    "quadratic_discriminant": effort_quadratic_discriminant,
    # Algebra 1 — radical ×÷ / equations + rational equations (EA2e Ch 8–9).
    "radical_multiply": effort_radical_multiply,
    "radical_divide": effort_radical_divide,
    "radical_equations": effort_radical_equations,
    "rational_expressions_equations": effort_rational_equations,
    # Algebra 1 — orphans + WP stems + prompt-based graph leaves.
    "polynomial_long_division": effort_poly_long_division,
    "radical_simplification": effort_radical_simplification,
    "mixture_word_problems": effort_wp_mixture,
    "distance_rate_time_word_problems": effort_wp_distance_rate_time,
    "work_word_problems": effort_wp_work,
    "age_word_problems": effort_wp_age,
    "coin_word_problems": effort_wp_coin,
    "consecutive_integers_word_problems": effort_wp_consecutive,
    "percent_word_problems": effort_markup_discount,
    "evaluating_graphing_functions": effort_evaluating_functions,
    "graphing_linear_equations": effort_graph_linear_equation,
    "graphing_absolute_value_equations": effort_graph_transform,
    "graphing_systems_of_inequalities": effort_graph_linear,
    "graphing_quadratic_functions": effort_graph_transform,
    "graphing_quadratic_inequalities": effort_graph_transform,
    # Algebra 2 aliases — shared generators / stems with A1–PA scorers.
    "a2_rational_expressions_multiplying_and_dividing": effort_rational_expression_ops,
    "a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions": effort_radical_add_subtract,
    "a2_quadratic_functions_and_inequalities_completing_the_square": effort_completing_square_constant,
    "a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square": effort_completing_square_solve,
    "a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula": effort_quadratic_formula,
    "a2_quadratic_functions_and_inequalities_the_discriminant": effort_quadratic_discriminant,
    "a2_radical_functions_and_rational_exponents_multiplying_radical_expressions": effort_radical_multiply,
    "a2_radical_functions_and_rational_exponents_dividing_radical_expressions": effort_radical_divide,
    "a2_radical_functions_and_rational_exponents_radical_equations": effort_radical_equations,
    "a2_radical_functions_and_rational_exponents_rational_exponent_equations": effort_radical_equations,
    "a2_rational_expressions_equations": effort_rational_equations,
    "geo_review_multiplying_square_roots": effort_radical_multiply,
    "geo_review_dividing_square_roots": effort_radical_divide,
    "a2_equations_and_inequalities_multi_step_equations": effort_equations,
    "a2_equations_and_inequalities_multi_step_inequalities": effort_equations,
    "a2_equations_and_inequalities_compound_inequalities": effort_compound_inequalities,
    "a2_equations_and_inequalities_absolute_value_equations": effort_absolute_value,
    "a2_equations_and_inequalities_absolute_value_inequalities": effort_absolute_value,
    "a2_linear_relations_and_functions_writing_linear_equations": effort_linear_write,
    "a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables": effort_systems,
    "a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables": effort_systems,
    "a2_systems_of_equations_and_inequalities_solving_systems_by_graphing_2_variables": effort_systems,
    "a2_systems_of_equations_and_inequalities_systems_of_equations_word_problems_2_variables": effort_systems,
    "a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions": effort_quadratic_factoring,
    "a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions": effort_poly_special,
    "a2_quadratic_functions_and_inequalities_solving_equations_by_factoring": effort_quadratic_factor_solve,
    "a2_polynomial_functions_factoring_by_grouping": effort_poly_grouping,
    "a2_polynomial_functions_conjugate_roots_and_factoring": effort_poly_special,
    "a2_polynomial_functions_solving_polynomial_equations": effort_quadratic_factor_solve,
    "a2_rational_expressions_simplifying": effort_rational_simplification,
    "a2_rational_expressions_adding_and_subtracting": effort_rational_simplification,
    "a2_radical_functions_and_rational_exponents_the_properties_of_exponents": effort_properties_of_exponents,
    "a2_radical_functions_and_rational_exponents_evaluating_rational_exponent_expressions": effort_properties_of_exponents,
    "a2_radical_functions_and_rational_exponents_connecting_radical_expressions_and_rational_exponents": effort_properties_of_exponents,
    "a2_radical_functions_and_rational_exponents_simplifying_radicals": effort_radical_simplification,
    "a2_polynomial_functions_dividing": effort_poly_long_division,
    "a2_equations_and_inequalities_mixture_word_problems": effort_wp_mixture,
    "a2_equations_and_inequalities_distance_rate_time_word_problems": effort_wp_distance_rate_time,
    "a2_equations_and_inequalities_work_word_problems": effort_wp_work,
    "a2_linear_relations_and_functions_graphing_linear_equations": effort_graph_linear_equation,
    "a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots": effort_quadratic_square_roots,
    "a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms": effort_a2_exp_equation,
    "a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms": effort_a2_exp_equation,
    "a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple": effort_a2_log_equation,
    "a2_exponential_and_logarithmic_expressions_logarithmic_equations_hard": effort_a2_log_equation,
    "a2_beginning_algebra_order_of_operations": effort_order_of_operations,
    # A2 literal equations — A1 generator + dedicated literal scorer.
    "a2_equations_and_inequalities_literal_equations": effort_literal_equations,
    # A2 graph UX (parseable prompts).
    "a2_linear_relations_and_functions_graphing_linear_inequalities": effort_graph_linear,
    "a2_linear_relations_and_functions_graphing_absolute_value_equations": effort_graph_transform,
    "a2_quadratic_functions_and_inequalities_graphing_quadratic_functions": effort_graph_transform,
    "a2_quadratic_functions_and_inequalities_graphing_quadratic_inequalities": effort_graph_transform,
    "a2_radical_functions_and_rational_exponents_graphing_radical_equations": effort_graph_transform,
    "a2_rational_expressions_graphing": effort_graph_transform,
    "a2_exponential_and_logarithmic_expressions_graphing_exponential_functions": effort_graph_transform,
    "a2_exponential_and_logarithmic_expressions_graphing_logarithmic_functions": effort_graph_transform,
    "a2_conic_sections_parabolas_graphing_and_properties": effort_graph_transform,
    "a2_trigonometry_graphing_trig_functions": effort_graph_trig,
    # A2 exp/log growth–decay + inverses.
    "a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems": effort_growth_decay,
    "a2_exponential_and_logarithmic_expressions_continuous_exponential_growth_and_decay_word_problems": effort_growth_decay,
    "a2_exponential_and_logarithmic_expressions_inverses_of_exponential_and_logarithmic_functions": effort_inverse_exp_log,
    "exponential_growth_decay": effort_growth_decay,
    # A2 matrices.
    "a2_matrices_operations": effort_matrix_ops,
    "a2_matrices_determinants": effort_matrix_ops,
    "a2_matrices_equations": effort_matrix_ops,
    "a2_matrices_inverses": effort_matrix_inverse,
    "a2_matrices_cramers_rule": effort_matrix_cramer,
    # A2 conics.
    "a2_conic_sections_circles_graphing_and_properties": effort_conic,
    "a2_conic_sections_circles_writing_equations": effort_conic,
    "a2_conic_sections_ellipses_graphing_and_properties": effort_conic,
    "a2_conic_sections_ellipses_writing_equations": effort_conic,
    "a2_conic_sections_hyperbolas_graphing_and_properties": effort_conic,
    "a2_conic_sections_hyperbolas_writing_equations": effort_conic,
    "a2_conic_sections_classifying": effort_conic,
    # A2 sequences.
    "a2_sequences_and_series_general_sequences": effort_sequence,
    "a2_sequences_and_series_arithmetic_sequences": effort_sequence,
    "a2_sequences_and_series_geometric_sequences": effort_sequence,
    "a2_sequences_and_series_arithmetic_and_geometric_mean": effort_sequence,
    "a2_sequences_and_series_general_series": effort_sequence,
    "a2_sequences_and_series_arithmetic_series": effort_sequence,
    "a2_sequences_and_series_geometric_series": effort_sequence,
    # Shared G6 leaves that use the same generators.
    "g6_numeric_expressions_and_order_of_operations": effort_order_of_operations,
    "g6_distributive_property_numeric": effort_distributive,
    "g6_writing_algebraic_expressions": effort_verbal_expressions,
    "pa_verbal_expressions": effort_verbal_expressions,
}


def register_effort_scorer(type_id: str, scorer: EffortScorer) -> None:
    """Register or replace a per-topic effort scorer."""
    EFFORT_SCORERS[type_id] = scorer


from question_engine.ml.effort_calc import (
    effort_log_evaluate,
    effort_trig_evaluate,
    register_precalc_calc_scorers,
)

register_precalc_calc_scorers(register_effort_scorer)

from question_engine.ml.effort_geo import register_geo_stats_scorers

register_geo_stats_scorers(register_effort_scorer)

from question_engine.ml.effort_geo import effort_transformation  # noqa: E402

# A1 prompt-graph scorers win over thinner geo graph overlays.
register_effort_scorer("graphing_linear_equations", effort_graph_linear_equation)
register_effort_scorer(
    "a2_linear_relations_and_functions_graphing_linear_equations",
    effort_graph_linear_equation,
)
register_effort_scorer("graphing_absolute_value_equations", effort_graph_transform)
register_effort_scorer("graphing_systems_of_inequalities", effort_graph_linear)
register_effort_scorer("graphing_quadratic_functions", effort_graph_transform)
register_effort_scorer("graphing_quadratic_inequalities", effort_graph_transform)
register_effort_scorer("graphing_linear_inequalities", effort_graph_linear)

# Diagram percent leaf shares formula percent stems.
register_effort_scorer("g6_solving_percent_problems_with_diagrams", effort_formulas)

# A2 log evaluate / properties — shared precalc stems (after PC registration).
for _a2_log_tid in (
    "a2_exponential_and_logarithmic_expressions_evaluating_logarithms",
    "a2_exponential_and_logarithmic_expressions_exponents_and_logarithms",
    "a2_exponential_and_logarithmic_expressions_logarithms_and_exponents_as_inverses",
    "a2_exponential_and_logarithmic_expressions_properties_of_logarithms",
    "a2_exponential_and_logarithmic_expressions_writing_logs_in_terms_of_others",
):
    register_effort_scorer(_a2_log_tid, effort_log_evaluate)

# A2 trig evaluate / simple equations — reuse precalc scorers.
for _a2_trig_tid in (
    "a2_trigonometry_trig_functions_of_any_angle",
    "a2_trigonometry_radians_and_degrees",
    "a2_trigonometry_coterminal_angles",
    "a2_trigonometry_equations",
):
    register_effort_scorer(_a2_trig_tid, effort_trig_evaluate)

# A2 thin-leaf gap-fill: 3-var / planes / laws / complex / stats.
for _a2_law_tid in (
    "a2_trigonometry_the_law_of_sines",
    "a2_trigonometry_the_law_of_cosines",
    "a2_trigonometry_area_and_laws_of_sines_and_cosines",
):
    register_effort_scorer(_a2_law_tid, effort_law_of_sines_cosines)

for _a2_cx_tid in (
    "a2_complex_numbers_operations",
    "a2_complex_numbers_graphing",
    "a2_complex_numbers_absolute_value",
    "a2_complex_numbers_rationalizing_denominators",
):
    register_effort_scorer(_a2_cx_tid, effort_complex_ops)

register_effort_scorer(
    "a2_systems_of_equations_and_inequalities_planes",
    effort_planes,
)
register_effort_scorer(
    "a2_systems_of_equations_and_inequalities_solving_systems_with_three_variables",
    effort_systems_three,
)

for _a2_count_tid in (
    "a2_probability_and_statistics_sample_spaces_and_the_fundamental_counting_principle",
):
    register_effort_scorer(_a2_count_tid, effort_stats_counting)

for _a2_prob_tid in (
    "a2_probability_and_statistics_probability_of_independent_and_dependent_events",
    "a2_probability_and_statistics_probability_of_independent_and_dependent_events_word_problems",
    "a2_probability_and_statistics_probability_of_mutually_exclusive_events",
    "a2_probability_and_statistics_probability_of_mutually_exclusive_events_word_problems",
):
    register_effort_scorer(_a2_prob_tid, effort_stats_probability)

for _a2_pc_tid in (
    "a2_probability_and_statistics_permutations",
    "a2_probability_and_statistics_combinations",
    "a2_probability_and_statistics_permutations_vs_combinations",
    "a2_probability_and_statistics_probability_with_permutations_and_combinations",
):
    register_effort_scorer(_a2_pc_tid, effort_stats_perm_comb)

# Wave: geo probability + G6 fraction/GCF WP + A2 poly ops (reuse existing scorers).
# Kept append-only for merge-friendliness with concurrent effort.py editors.
for _geo_count_tid in (
    "geo_probability_sample_spaces_and_fundamental_counting_principle",
):
    register_effort_scorer(_geo_count_tid, effort_stats_counting)

for _geo_prob_tid in (
    "geo_probability_independent_and_dependent_events",
    "geo_probability_independent_and_dependent_events_word_problems",
    "geo_probability_mutually_exclusive_events",
    "geo_probability_mutually_exclusive_events_word_problems",
):
    register_effort_scorer(_geo_prob_tid, effort_stats_probability)

for _geo_pc_tid in (
    "geo_probability_permutations",
    "geo_probability_combinations",
    "geo_probability_permutations_vs_combinations",
    "geo_probability_with_permutations_and_combinations",
):
    register_effort_scorer(_geo_pc_tid, effort_stats_perm_comb)

register_effort_scorer("g6_dividing_fractions", effort_fraction_ops)
register_effort_scorer("g6_gcf_and_lcm_word_problems", effort_gcf)
register_effort_scorer("g6_how_many_groups_times", effort_fraction_ops)
register_effort_scorer("g6_how_much_in_each_group_time", effort_fraction_ops)

for _a2_poly_tid in (
    "a2_polynomial_functions_adding_and_subtracting",
    "a2_polynomial_functions_multiplying",
    "a2_polynomial_functions_multiplying_special_cases",
    "a2_polynomial_functions_simplifying",
    "a2_polynomial_functions_naming",
):
    register_effort_scorer(_a2_poly_tid, effort_polynomials)

register_effort_scorer(
    "a2_polynomial_functions_factoring_sum_difference_of_cubes",
    effort_poly_special,
)
register_effort_scorer(
    "a2_polynomial_functions_factoring_quadratic_form",
    effort_quadratic_factoring,
)
register_effort_scorer(
    "a2_beginning_algebra_simplifying_algebraic_expressions",
    effort_polynomials,
)

# Geo review radical leaves share PA/A1 radical scorers where present.
for _geo_rad_tid in (
    "geo_review_simplifying_square_roots",
    "geo_review_adding_and_subtracting_square_roots",
):
    register_effort_scorer(_geo_rad_tid, effort_squares_roots)

register_effort_scorer("geo_review_multi_step_equations", effort_equations)

# G6 equations / inequalities / tape — reuse equation scorer.
for _g6_eq_tid in (
    "g6_solutions_to_equations",
    "g6_equations_word_problems",
    "g6_equations_tape_diagrams",
    "g6_equations_hanger_diagrams",
    "g6_constant_rate_equations",
    "g6_equations_for_other_relationships",
    "g6_equivalent_ratio_equations",
    "g6_solutions_to_inequalities",
    "g6_solving_and_graphing_one_step_inequalities",
    "g6_writing_and_graphing_inequalities",
    "g6_inequalities_word_problems",
    "g6_inequalities_hanger_diagrams",
):
    register_effort_scorer(_g6_eq_tid, effort_equations)

register_effort_scorer("a2_general_functions_evaluating", effort_evaluating_functions)
register_effort_scorer(
    "a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions",
    effort_evaluating_functions,
)
register_effort_scorer(
    "a2_systems_of_equations_and_inequalities_graphing_systems_of_linear_inequalities",
    effort_graph_linear,
)
register_effort_scorer(
    "a2_rational_expressions_complex_fractions",
    effort_rational_simplification,
)
register_effort_scorer(
    "a2_polynomial_functions_factoring_all_techniques",
    effort_poly_general_strategy,
)

# A2 final gap-fill: relations / poly theory / inverses / radical D&R / quadratic systems.
register_effort_scorer(
    "a2_relations_and_introduction_to_functions_discrete_relations",
    effort_relations,
)
register_effort_scorer(
    "a2_relations_and_introduction_to_functions_continuous_relations",
    effort_relations,
)
register_effort_scorer(
    "a2_systems_of_equations_and_inequalities_points_in_three_dimensions",
    effort_points_3d,
)
register_effort_scorer(
    "a2_matrices_geometric_transformations",
    effort_transformation,
)
register_effort_scorer(
    "a2_quadratic_functions_and_inequalities_solving_equations_by_graphing",
    effort_solve_by_graphing,
)
register_effort_scorer(
    "a2_polynomial_functions_the_binomial_theorem",
    effort_binomial_theorem,
)
register_effort_scorer(
    "a2_polynomial_functions_the_remainder_theorem",
    effort_remainder_theorem,
)
register_effort_scorer(
    "a2_polynomial_functions_writing_functions",
    effort_polynomial_writing,
)
register_effort_scorer(
    "a2_polynomial_functions_conjugate_roots_and_writing_functions",
    effort_polynomial_writing,
)
register_effort_scorer(
    "a2_polynomial_functions_descartes_rule_of_signs",
    effort_descartes,
)
register_effort_scorer(
    "a2_polynomial_functions_rational_zero_root_theorem",
    effort_rational_zero,
)
register_effort_scorer(
    "a2_polynomial_functions_fundamental_theorem_of_algebra",
    effort_fta,
)
register_effort_scorer(
    "a2_polynomial_functions_end_behavior_and_general_graph_shape",
    effort_poly_end_behavior,
)
register_effort_scorer(
    "a2_polynomial_functions_graphing",
    effort_graph_transform,
)
register_effort_scorer("a2_general_functions_inverses", effort_inverse_function)
register_effort_scorer(
    "a2_radical_functions_and_rational_exponents_domain_and_range_of_radical_functions",
    effort_radical_domain_range,
)
register_effort_scorer(
    "a2_conic_sections_parabolas_writing_equations",
    effort_conic,
)
register_effort_scorer(
    "a2_conic_sections_systems_of_quadratic_equations",
    effort_quadratic_system,
)

# Precalc twins sharing the same generators.
register_effort_scorer("pc_binomial_theorem", effort_binomial_theorem)
register_effort_scorer(
    "pc_remainder_theorem_and_bounds_of_real_zeros",
    effort_remainder_theorem,
)
register_effort_scorer(
    "pc_polynomial_graphs_real_zeros_and_end_behavior",
    effort_poly_end_behavior,
)
register_effort_scorer("pc_inverses", effort_inverse_function)
register_effort_scorer("graphing_exponential_functions", effort_graph_transform)
register_effort_scorer("quadratic_solve_by_graphing", effort_solve_by_graphing)


def has_effort_scorer(type_id: str) -> bool:
    return type_id in EFFORT_SCORERS


def score_effort(
    type_id: str,
    prompt: str,
    answer: str = "",
) -> tuple[float | None, dict[str, Any]]:
    """Score effort for a generated question.

    Returns ``(None, {})`` when no scorer is registered for ``type_id``.
    """
    scorer = EFFORT_SCORERS.get(type_id)
    if scorer is None:
        return None, {}
    effort, feats = scorer(prompt or "", answer or "")
    return float(effort), dict(feats or {})
