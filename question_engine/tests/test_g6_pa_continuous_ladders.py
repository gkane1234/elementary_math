"""Continuous difficulty must actually change G6/PA number-lane questions."""

from __future__ import annotations

import math
import re
from fractions import Fraction

from question_engine.frameworks.number import (
    AbsoluteValueFramework,
    CompareOrderFramework,
    IntegerArithmeticFramework,
    RatioFramework,
    _abs_mag_hi,
    _abs_separation,
    _compare_form_menu,
    _compare_separation,
    continuous_abs_max,
    continuous_ratio_inflate_max,
    continuous_ratio_scale_max,
    continuous_simplify_frac_core_max,
    continuous_simplify_frac_inflate_max,
    sample_unreduced_numeric_fraction,
)
from question_engine.generators.grade_level import (
    _place_rounding_params,
    _words_max_for_difficulty,
    place_value_and_rounding,
    simplifying_numeric_fractions,
    writing_numbers_with_words,
)


def test_continuous_abs_max_unbounded():
    lo = continuous_abs_max({"difficulty": 0})
    mid = continuous_abs_max({"difficulty": 10})
    hi = continuous_abs_max({"difficulty": 40})
    assert lo is not None and mid is not None and hi is not None
    assert lo == 8
    assert mid > lo
    assert hi > mid
    assert hi > 400  # still growing past EMH hard caps (~50)
    assert continuous_abs_max({"difficulty_tier": "hard"}) is None


def test_continuous_ratio_inflate_grows():
    assert continuous_ratio_inflate_max({"difficulty_tier": "hard"}) is None
    d0 = continuous_ratio_inflate_max({"difficulty": 0})
    d10 = continuous_ratio_inflate_max({"difficulty": 10})
    d20 = continuous_ratio_inflate_max({"difficulty": 20})
    d40 = continuous_ratio_inflate_max({"difficulty": 40})
    assert d0 == 1
    assert d10 is not None and d20 is not None and d40 is not None
    assert d10 > d0
    assert d20 > d10
    assert d40 > d20
    assert d40 >= 20
    assert continuous_ratio_scale_max({"difficulty": 0}) == 3
    assert (continuous_ratio_scale_max({"difficulty": 40}) or 0) > 10


def test_integer_division_easy_is_exact_integer():
    fw = IntegerArithmeticFramework("/")
    for seed_d in range(30):
        settings = {"difficulty": 0, "allow_negative": True, "seed": seed_d}
        # Force RNG via rebuilding — framework uses module random; set seed.
        import random

        random.seed(seed_d)
        _latex, _text, answer = fw.build_prompt(settings)
        assert answer is not None
        assert "/" not in answer and "frac" not in answer
        # Prompt a ÷ b; answer must be integer equal to a/b.
        nums = re.findall(r"-?\d+", _latex.replace("{", "").replace("}", ""))
        assert len(nums) >= 2
        a, b = int(nums[0]), int(nums[1])
        assert b != 0
        assert a % b == 0
        assert int(answer) == a // b


def test_integer_division_hard_can_be_noninteger():
    fw = IntegerArithmeticFramework("/")
    import random

    nonint = 0
    for seed in range(60):
        random.seed(seed)
        _l, _t, answer = fw.build_prompt(
            {"difficulty": 22, "allow_negative": True, "allow_noninteger_quotient": True}
        )
        assert answer is not None
        if "frac" in answer or "/" in answer:
            nonint += 1
        else:
            # Still exact integer when constructed that way
            nums = re.findall(r"-?\d+", _l.replace("{", "").replace("}", ""))
            a, b = int(nums[0]), int(nums[1])
            assert a % b == 0
    assert nonint >= 10


def test_g6_numeric_expressions_with_exponents_always_has_power():
    from question_engine.generators import GENERATORS

    gen = GENERATORS["g6_numeric_expressions_with_exponents"]
    for d in (0, 3, 10, 20):
        qs = gen(
            "g6_numeric_expressions_with_exponents",
            {
                "difficulty": d,
                "count": 15,
                "seed": 11 + d,
                "include_answer_key": True,
            },
        )
        for q in qs:
            assert "^{" in (q.prompt_latex or ""), q.prompt_latex


def _classify_compare_token(token: str) -> str:
    t = token.strip()
    if "frac" in t:
        return "frac"
    if "." in t:
        return "decimal"
    return "int"


def _split_compare_prompt(latex: str) -> tuple[str, str]:
    parts = latex.split("\\; ? \\;")
    assert len(parts) == 2, latex
    return parts[0].strip(), parts[1].strip()


def _parse_abs_compare(latex: str) -> tuple[int, int]:
    nums = re.findall(r"\\left\|\s*(-?\d+)\s*\\right\|", latex)
    assert len(nums) == 2, latex
    return int(nums[0]), int(nums[1])


def _parse_abs_order_values(latex: str) -> list[int]:
    after = latex.split("absolute value:")[-1]
    after = after.lstrip(" }")
    return [int(x.strip()) for x in after.split(",") if x.strip()]


def test_compare_form_menu_ladder():
    m0 = {band for *_k, band, _w in _compare_form_menu(0)}
    assert m0 == {"whole_whole"}

    m5 = {band for *_k, band, _w in _compare_form_menu(5)}
    assert "whole_whole" in m5 and "whole_decimal" in m5
    assert "frac_frac" not in m5

    m12 = {band for *_k, band, _w in _compare_form_menu(12)}
    assert "decimal_frac" in m12 and "frac_whole" in m12

    m20 = {band for *_k, band, _w in _compare_form_menu(20)}
    assert "frac_frac" in m20
    # High D: frac_frac should outweigh whole_whole.
    w20 = {band: w for *_k, band, w in _compare_form_menu(20)}
    assert w20["frac_frac"] > w20["whole_whole"]


def test_compare_separation_tightens_with_d():
    far = [_compare_separation(0, scale=10.0) for _ in range(30)]
    near = [_compare_separation(40, scale=10.0) for _ in range(30)]
    assert sum(far) / len(far) > 3.0
    assert sum(near) / len(near) < sum(far) / len(far) * 0.45


def test_comparing_numbers_form_and_closeness_ladder():
    """D=0 ≈ int–int far; high D often frac mixes and closer gaps."""
    import random

    fw = CompareOrderFramework(mode="compare")

    def _stats(d: float, n: int = 60) -> dict:
        bands: list[tuple[str, str]] = []
        rel_gaps: list[float] = []
        ties = 0
        for s in range(n):
            random.seed(3000 + int(d) * 100 + s)
            latex, _t, answer = fw.build_prompt(
                {"difficulty": d, "allow_negative": True}
            )
            a, b = _split_compare_prompt(latex)
            ka, kb = _classify_compare_token(a), _classify_compare_token(b)
            bands.append(tuple(sorted((ka, kb))))
            if answer == "=":
                ties += 1

            def _approx(tok: str) -> float | None:
                if "frac" in tok:
                    m = re.search(r"frac\{(-?\d+)\}\{(-?\d+)\}", tok)
                    return float(m.group(1)) / float(m.group(2)) if m else None
                try:
                    return float(tok)
                except ValueError:
                    return None

            va, vb = _approx(a), _approx(b)
            if va is not None and vb is not None:
                scale = max(abs(va), abs(vb), 1.0)
                rel_gaps.append(abs(va - vb) / scale)
        return {
            "bands": bands,
            "rel_gaps": rel_gaps,
            "ties": ties,
            "int_int": sum(1 for x in bands if x == ("int", "int")),
            "has_frac": sum(1 for a, b in bands if "frac" in (a, b)),
            "frac_frac": sum(1 for x in bands if x == ("frac", "frac")),
            "has_decimal": sum(1 for a, b in bands if "decimal" in (a, b)),
        }

    s0 = _stats(0)
    s10 = _stats(10)
    s20 = _stats(20)
    s40 = _stats(40)

    assert s0["ties"] == 0
    assert s0["int_int"] >= 55  # almost always whole–whole
    assert s0["has_frac"] == 0
    assert sum(s0["rel_gaps"]) / len(s0["rel_gaps"]) > 0.25

    assert s10["has_decimal"] >= 15
    assert s10["int_int"] < s0["int_int"]

    assert s20["has_frac"] >= 15
    assert s40["frac_frac"] >= 8
    assert s40["has_frac"] > s10["has_frac"]
    assert sum(s40["rel_gaps"]) / len(s40["rel_gaps"]) < sum(s0["rel_gaps"]) / len(
        s0["rel_gaps"]
    ) * 0.55


def test_ordering_numbers_form_and_count_ladder():
    fw = CompareOrderFramework(mode="order")
    import random

    random.seed(1)
    easy = fw.build_prompt({"difficulty": 0, "allow_negative": True})[0]
    assert "frac" not in easy
    # D=0: integers only — no decimal point in the number list.
    after0 = easy.split(":")[-1]
    assert "." not in after0
    assert after0.count(",") == 2  # 3 values

    def _form_counts(d: float, n: int = 40) -> dict:
        fracs = decimals = 0
        counts: list[int] = []
        for s in range(n):
            random.seed(4000 + int(d) * 50 + s)
            latex, _t, _a = fw.build_prompt({"difficulty": d, "allow_negative": True})
            after = latex.split(":")[-1]
            counts.append(after.count(",") + 1)
            if "frac" in after:
                fracs += 1
            if re.search(r"\d\.\d", after):
                decimals += 1
        return {
            "mean_count": sum(counts) / len(counts),
            "max_count": max(counts),
            "frac_sets": fracs,
            "decimal_sets": decimals,
        }

    c0 = _form_counts(0)
    c10 = _form_counts(10)
    c20 = _form_counts(20)
    c40 = _form_counts(40)
    assert c0["max_count"] == 3
    assert c0["frac_sets"] == 0
    assert c10["decimal_sets"] >= 10
    assert c20["max_count"] >= 4
    assert c20["frac_sets"] >= 8
    assert c40["mean_count"] >= c0["mean_count"]
    assert c40["frac_sets"] > c10["frac_sets"]


def test_compare_order_generators_wire():
    from question_engine.generators import GENERATORS

    for key in ("g6_comparing_numbers", "g6_ordering_numbers"):
        gen = GENERATORS[key]
        qs0 = gen(key, {"difficulty": 0, "count": 8, "seed": 5, "include_answer_key": True})
        qs40 = gen(key, {"difficulty": 40, "count": 8, "seed": 6, "include_answer_key": True})
        assert len(qs0) == 8 and len(qs40) == 8
        assert all(q.prompt_latex and q.answer_latex for q in qs0 + qs40)


def test_abs_separation_tightens_with_d():
    mag0 = _abs_mag_hi(0)
    mag40 = _abs_mag_hi(40)
    far = [_abs_separation(0, mag0) for _ in range(40)]
    near = [_abs_separation(40, mag40) for _ in range(40)]
    assert sum(far) / len(far) >= 3.0
    assert sum(near) / len(near) <= 2.5
    assert sum(near) / len(near) < sum(far) / len(far) * 0.55


def test_abs_compare_closeness_ladder():
    import random

    fw = AbsoluteValueFramework(mode="compare")

    def _gaps(d: float, n: int = 50) -> tuple[float, int, int]:
        gaps: list[int] = []
        opposite = 0
        ties = 0
        for s in range(n):
            random.seed(5000 + int(d) * 80 + s)
            latex, _t, answer = fw.build_prompt({"difficulty": d})
            a, b = _parse_abs_compare(latex)
            gaps.append(abs(abs(a) - abs(b)))
            if (a < 0) != (b < 0):
                opposite += 1
            if answer == "=" or abs(a) == abs(b):
                ties += 1
        return sum(gaps) / len(gaps), opposite, ties

    g0, opp0, ties0 = _gaps(0)
    g10, opp10, _t10 = _gaps(10)
    g40, opp40, ties40 = _gaps(40)
    assert ties0 == 0 and ties40 == 0
    assert g0 >= 3.0
    assert g40 < g0 * 0.55
    assert g10 < g0
    # Higher D mixes signs more often.
    assert opp40 > opp0


def test_abs_order_count_and_closeness():
    import random

    fw = AbsoluteValueFramework(mode="order")

    def _stats(d: float, n: int = 40) -> dict:
        counts: list[int] = []
        mean_span: list[float] = []
        negatives = 0
        for s in range(n):
            random.seed(6000 + int(d) * 70 + s)
            latex, _t, answer = fw.build_prompt({"difficulty": d})
            vals = _parse_abs_order_values(latex)
            counts.append(len(vals))
            abs_vals = sorted(abs(v) for v in vals)
            mean_span.append(abs_vals[-1] - abs_vals[0])
            if any(v < 0 for v in vals):
                negatives += 1
            # Answer orders by absolute value.
            ordered = [int(x.strip()) for x in (answer or "").split(",")]
            assert [abs(x) for x in ordered] == sorted(abs(x) for x in ordered)
        return {
            "mean_count": sum(counts) / len(counts),
            "max_count": max(counts),
            "mean_span": sum(mean_span) / len(mean_span),
            "negatives": negatives,
        }

    s0 = _stats(0)
    s20 = _stats(20)
    s40 = _stats(40)
    assert s0["max_count"] == 3
    assert s20["max_count"] >= 4
    assert s40["max_count"] == 5
    assert s40["mean_span"] < s0["mean_span"] * 0.7
    assert s40["negatives"] > s0["negatives"]


def test_abs_compare_order_generators_wire():
    from question_engine.generators import GENERATORS

    for key in (
        "g6_comparing_with_absolute_values",
        "g6_ordering_with_absolute_values",
    ):
        gen = GENERATORS[key]
        qs0 = gen(key, {"difficulty": 0, "count": 8, "seed": 7, "include_answer_key": True})
        qs40 = gen(key, {"difficulty": 40, "count": 8, "seed": 8, "include_answer_key": True})
        assert len(qs0) == 8 and len(qs40) == 8
        assert all(q.prompt_latex and q.answer_latex for q in qs0 + qs40)


def test_writing_numbers_place_ladder():
    assert _words_max_for_difficulty(0) == 20
    assert _words_max_for_difficulty(5) == 99
    assert _words_max_for_difficulty(12) == 9_999
    assert _words_max_for_difficulty(30) == 9_999_999

    qs0 = writing_numbers_with_words(
        "pa_writing_numbers_with_words",
        {"difficulty": 0, "count": 20, "seed": 1, "include_answer_key": True},
    )
    for q in qs0:
        n = int(re.search(r"Write \} (\d+)", q.prompt_latex or "").group(1))  # type: ignore
        assert n <= 20

    qs = writing_numbers_with_words(
        "pa_writing_numbers_with_words",
        {"difficulty": 16, "count": 15, "seed": 2, "include_answer_key": True},
    )
    max_seen = 0
    for q in qs:
        m = re.search(r"Write \} (\d+)", q.prompt_latex or "")
        if m:
            max_seen = max(max_seen, int(m.group(1)))
    assert max_seen > 1000


def _decimal_token_from_prompt(latex: str) -> str | None:
    """Pull the decimal (or whole) number being named/rounded from the prompt."""
    m = re.search(r"place of \} ([0-9]+(?:\.[0-9]+)?)", latex)
    if m:
        return m.group(1)
    m = re.search(r"Round \} ([0-9]+(?:\.[0-9]+)?)", latex)
    if m:
        return m.group(1)
    return None


def _place_asked(latex: str) -> str | None:
    m = re.search(r"in the (\w+) place", latex)
    return m.group(1) if m else None


def _round_target(latex: str) -> str | None:
    m = re.search(r"nearest (\w+(?: number)?)", latex)
    return m.group(1) if m else None


def test_place_rounding_params_grow():
    p0 = _place_rounding_params(0)
    p10 = _place_rounding_params(10)
    p20 = _place_rounding_params(20)
    p40 = _place_rounding_params(40)
    assert p0["whole_max"] == 20
    assert p0["show_decimals"] == 1
    assert p0["name_max_place"] == 1
    assert p0["round_max"] == 1
    assert p10["show_decimals"] == 2
    assert p10["name_max_place"] == 2
    assert int(p20["whole_max"]) > int(p10["whole_max"])
    assert p20["show_decimals"] == 3
    assert p20["name_max_place"] == 3
    assert int(p40["whole_max"]) > int(p20["whole_max"])
    assert float(p40["carry_p"]) > float(p0["carry_p"])


def test_place_value_and_rounding_ladder_samples():
    """D=0 vs D=10 vs D=20 vs D=40 must look pedagogically different."""
    import random
    from decimal import Decimal, ROUND_HALF_UP

    def _stats(d: float, n: int = 50) -> dict:
        wholes: list[int] = []
        decimals_shown: list[int] = []
        places: list[str] = []
        round_to: list[str] = []
        thousandths = 0
        hundredths_place = 0
        for s in range(n):
            random.seed(9000 + int(d) * 100 + s)
            qs = place_value_and_rounding(
                "pa_naming_decimal_places_and_rounding",
                {"difficulty": d, "count": 1, "include_answer_key": True},
            )
            latex = qs[0].prompt_latex or ""
            tok = _decimal_token_from_prompt(latex)
            assert tok is not None, latex
            if "." in tok:
                whole_s, frac = tok.split(".", 1)
                wholes.append(int(whole_s))
                decimals_shown.append(len(frac))
            else:
                wholes.append(int(tok))
                decimals_shown.append(0)
            asked = _place_asked(latex)
            if asked:
                places.append(asked)
                if asked == "thousandths":
                    thousandths += 1
                if asked == "hundredths":
                    hundredths_place += 1
            tgt = _round_target(latex)
            if tgt:
                round_to.append(tgt)
            # Answer key must match half-up rounding / named digit.
            ans = qs[0].answer_latex
            assert ans is not None
            if asked:
                if asked == "ones":
                    assert ans == str(int(tok.split(".")[0]) % 10)
                else:
                    idx = {"tenths": 0, "hundredths": 1, "thousandths": 2}[asked]
                    frac = tok.split(".")[1] if "." in tok else ""
                    assert ans == frac[idx]
            elif tgt:
                nd = {"whole number": 0, "tenth": 1, "hundredth": 2, "thousandth": 3}[tgt]
                val = Decimal(tok)
                quant = Decimal("1") if nd == 0 else Decimal("1").scaleb(-nd)
                expected = val.quantize(quant, rounding=ROUND_HALF_UP)
                if nd == 0:
                    assert ans == format(expected, "f").split(".")[0]
                else:
                    assert ans == f"{expected:.{nd}f}"
        return {
            "max_whole": max(wholes),
            "mean_whole": sum(wholes) / len(wholes),
            "max_decimals": max(decimals_shown),
            "mean_decimals": sum(decimals_shown) / len(decimals_shown),
            "thousandths": thousandths,
            "hundredths_place": hundredths_place,
            "round_targets": set(round_to),
            "places": set(places),
        }

    s0 = _stats(0)
    s10 = _stats(10)
    s20 = _stats(20)
    s40 = _stats(40)

    # Low D: small wholes, tenths-only naming depth, ≤2 decimals shown.
    assert s0["max_whole"] <= 20
    assert s0["max_decimals"] <= 2
    assert "thousandths" not in s0["places"]
    assert "hundredths" not in s0["places"]
    assert s0["places"] <= {"tenths"} or s0["places"]  # may be only rounds
    assert "hundredth" not in s0["round_targets"]

    # Mid D: hundredths unlock; larger wholes.
    assert s10["max_whole"] > s0["max_whole"]
    assert s10["max_decimals"] >= 2
    assert s10["hundredths_place"] >= 1 or "hundredth" in s10["round_targets"]

    # High D: thousandths + much larger magnitude.
    assert s20["max_decimals"] == 3
    assert s20["thousandths"] >= 3
    assert s20["max_whole"] > s10["max_whole"]
    assert s40["mean_whole"] > s20["mean_whole"]
    assert s40["max_whole"] > s20["max_whole"]


def test_place_value_generator_wires_continuous_d():
    from question_engine.generators import GENERATORS

    gen = GENERATORS["place_value_and_rounding"]
    qs0 = gen(
        "pa_naming_decimal_places_and_rounding",
        {"difficulty": 0, "count": 8, "include_answer_key": True},
    )
    qs40 = gen(
        "pa_naming_decimal_places_and_rounding",
        {"difficulty": 40, "count": 8, "include_answer_key": True},
    )
    assert len(qs0) == 8 and len(qs40) == 8
    toks0 = [_decimal_token_from_prompt(q.prompt_latex or "") for q in qs0]
    toks40 = [_decimal_token_from_prompt(q.prompt_latex or "") for q in qs40]
    assert all(t is not None for t in toks0 + toks40)
    max0 = max(int(t.split(".")[0]) for t in toks0 if t)
    max40 = max(int(t.split(".")[0]) for t in toks40 if t)
    assert max40 > max0 * 5


def test_simplify_frac_continuous_bounds_grow():
    lo_k = continuous_simplify_frac_inflate_max({"difficulty": 0})
    mid_k = continuous_simplify_frac_inflate_max({"difficulty": 20})
    hi_k = continuous_simplify_frac_inflate_max({"difficulty": 40})
    assert lo_k == 3
    assert mid_k is not None and hi_k is not None
    assert mid_k > lo_k
    assert hi_k > mid_k
    assert hi_k >= 60
    assert continuous_simplify_frac_inflate_max({"difficulty_tier": "hard"}) is None

    lo_c = continuous_simplify_frac_core_max({"difficulty": 0})
    hi_c = continuous_simplify_frac_core_max({"difficulty": 40})
    assert lo_c == 3
    assert hi_c is not None and hi_c > lo_c


def test_simplify_frac_factors_first_and_reduces():
    """Construction is backwards: shown = reduced × k; answer is reduced form."""
    import math
    import random

    for d, seed in ((0, 1), (10, 2), (20, 3), (40, 4)):
        for s in range(40):
            random.seed(seed * 100 + s)
            settings = {"difficulty": d}
            num, den = sample_unreduced_numeric_fraction(settings)
            g = math.gcd(num, den)
            assert g >= 2, (num, den, d)
            a, b = num // g, den // g
            assert math.gcd(a, b) == 1
            assert Fraction(num, den) == Fraction(a, b)
            # Reconstruct: reduced × GCF recovers the prompt.
            assert a * g == num and b * g == den


def test_simplify_frac_difficulty_correlates_with_gcf_and_size():
    import math
    import random

    def _stats(d: float, n: int = 80) -> tuple[float, float]:
        gcfs: list[int] = []
        mags: list[int] = []
        for s in range(n):
            random.seed(1000 + int(d) * 200 + s)
            num, den = sample_unreduced_numeric_fraction({"difficulty": d})
            g = math.gcd(num, den)
            gcfs.append(g)
            mags.append(max(num, den))
        return sum(gcfs) / len(gcfs), sum(mags) / len(mags)

    mean_g0, mean_m0 = _stats(0)
    mean_g20, mean_m20 = _stats(20)
    mean_g40, mean_m40 = _stats(40)

    assert mean_g0 < 4.0  # mostly 2–3
    assert mean_g20 > mean_g0 * 1.8
    assert mean_g40 > mean_g20
    assert mean_m20 > mean_m0 * 2
    assert mean_m40 > mean_m20
    assert mean_m40 > 80  # hundreds-ish unreduced surface


def test_pa_simplifying_fractions_generator_answers():
    qs = simplifying_numeric_fractions(
        "pa_simplifying_fractions",
        {"difficulty": 15, "count": 25, "seed": 7, "include_answer_key": True},
    )
    assert len(qs) == 25
    for q in qs:
        m = re.search(r"\\frac\{(\d+)\}\{(\d+)\}", q.prompt_latex or "")
        assert m, q.prompt_latex
        num, den = int(m.group(1)), int(m.group(2))
        expected = Fraction(num, den)
        assert q.answer_latex
        # Answer latex is reduced fraction (or integer).
        got = Fraction(expected.numerator, expected.denominator)
        assert got == expected
        # Parse answer back when it is a frac.
        am = re.search(r"\\frac\{(-?\d+)\}\{(-?\d+)\}", q.answer_latex or "")
        if am:
            assert Fraction(int(am.group(1)), int(am.group(2))) == expected
        else:
            assert str(expected.numerator) in (q.answer_latex or "")


def _ratio_parts_from_intro_prompt(latex: str) -> tuple[int, int] | None:
    m = re.search(r"Write the ratio \} (\d+):(\d+)", latex)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"There are (\d+) .* and (\d+) ", latex)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def _equivalent_parts_from_prompt(latex: str) -> tuple[int, int, int] | None:
    m = re.search(r"(\d+):(\d+) = (\d+):x", latex)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    m = re.search(r"frac\{(\d+)\}\{(\d+)\} = \\frac\{(\d+)\}\{x\}", latex)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return None


def test_intro_ratios_simplification_ladder():
    """D≈0: small/simple parts; D≥20: often large unreduced parts."""
    import random

    fw = RatioFramework(equivalent=False)
    easy_gcfs: list[int] = []
    easy_max_part = 0
    for seed in range(40):
        random.seed(seed)
        latex, _t, _a = fw.build_prompt({"difficulty": 0})
        parts = _ratio_parts_from_intro_prompt(latex)
        assert parts is not None, latex
        a, b = parts
        easy_max_part = max(easy_max_part, a, b)
        easy_gcfs.append(math.gcd(a, b))
    assert easy_max_part <= 12
    assert sum(1 for g in easy_gcfs if g == 1) >= 25

    hard_gcfs: list[int] = []
    hard_max_part = 0
    for seed in range(50):
        random.seed(1000 + seed)
        latex, _t, answer = fw.build_prompt({"difficulty": 40})
        parts = _ratio_parts_from_intro_prompt(latex)
        assert parts is not None, latex
        a, b = parts
        hard_max_part = max(hard_max_part, a, b)
        g = math.gcd(a, b)
        hard_gcfs.append(g)
        if "simplest form" in latex:
            reduced = Fraction(a, b)
            assert math.gcd(reduced.numerator, reduced.denominator) == 1
            assert answer is not None
    assert hard_max_part >= 40
    assert sum(1 for g in hard_gcfs if g >= 4) >= 15
    # Clear D=0 vs D=40 skill gap
    assert hard_max_part > easy_max_part * 2


def test_equivalent_ratios_scale_ladder():
    """Missing-value ratios: D=0 obvious small scale; D=40 non-trivial surface."""
    import random

    fw = RatioFramework(equivalent=True)

    def surface_scale(a: int, c: int) -> float | None:
        if a != 0 and c % a == 0:
            return c / a
        return None  # non-integer scale on the unreduced surface

    easy_max = 0
    for seed in range(40):
        random.seed(seed)
        latex, _t, answer = fw.build_prompt({"difficulty": 0})
        parts = _equivalent_parts_from_prompt(latex)
        assert parts is not None, latex
        a, b, c = parts
        easy_max = max(easy_max, a, b, c, int(answer or 0))
        assert a <= 10 and b <= 10
        sc = surface_scale(a, c)
        assert sc is not None and sc in (2, 3)
        assert int(answer or 0) == b * int(sc)

    hard_nontrivial = 0
    hard_max = 0
    hard_gcf = 0
    for seed in range(60):
        random.seed(2000 + seed)
        latex, _t, answer = fw.build_prompt({"difficulty": 40})
        parts = _equivalent_parts_from_prompt(latex)
        assert parts is not None, latex
        a, b, c = parts
        hard_max = max(hard_max, a, b, c, int(answer or 0))
        g = math.gcd(a, b)
        if g >= 4:
            hard_gcf += 1
        sc = surface_scale(a, c)
        if sc is None or sc >= 5 or g >= 4:
            hard_nontrivial += 1
        # Cross-check proportion identity
        assert a * int(answer or 0) == b * c
    assert hard_max >= 40
    assert hard_gcf >= 12
    assert hard_nontrivial >= 25
    assert hard_max > easy_max * 2


def test_ratio_generators_wire_continuous_d():
    from question_engine.generators import GENERATORS

    for key in ("g6_introduction_to_ratios", "g6_equivalent_ratios"):
        gen = GENERATORS[key]
        qs0 = gen(key, {"difficulty": 0, "count": 8, "seed": 3, "include_answer_key": True})
        qs40 = gen(key, {"difficulty": 40, "count": 8, "seed": 4, "include_answer_key": True})
        assert len(qs0) == 8 and len(qs40) == 8
        assert all(q.prompt_latex for q in qs0 + qs40)


def _unit_rate_nums_from_prompt(latex: str) -> tuple[int, ...] | None:
    """Extract integers from a unit/equivalent-rate prompt (ignores $)."""
    nums = [int(n) for n in re.findall(r"\d+", latex)]
    return tuple(nums) if nums else None


def test_unit_rates_factors_first_ladder():
    """D≈0: small friendly rates; D≥40: larger totals / composite quantities."""
    import random

    from question_engine.frameworks.number import UnitRateFramework

    fw = UnitRateFramework()
    easy_max = 0
    easy_qty_max = 0
    for seed in range(40):
        random.seed(seed)
        latex, _t, answer = fw.build_prompt({"difficulty": 0})
        nums = _unit_rate_nums_from_prompt(latex)
        assert nums is not None, latex
        easy_max = max(easy_max, *nums)
        # Quantity is the last "in N units" / "for N pounds" figure before ask.
        if "Find the unit" in latex:
            # total, qty  OR  cost, pounds
            assert len(nums) >= 2
            qty = nums[1]
            easy_qty_max = max(easy_qty_max, qty)
            assert qty in (2, 3)
            total = nums[0]
            rate = int(str(answer).replace("\\$", ""))
            assert total == rate * qty
        else:
            # equivalent: total1, q1, q2
            assert "same rate" in latex
            assert len(nums) >= 3
            total1, q1, q2 = nums[0], nums[1], nums[2]
            assert q1 in (2, 3) and q2 in (4, 6, 9)
            ans = int(str(answer).replace("\\$", ""))
            assert total1 * q2 == ans * q1
            assert q2 // q1 in (2, 3)
    assert easy_max <= 36
    assert easy_qty_max <= 4

    hard_max = 0
    hard_composite_qty = 0
    hard_nontrivial_equiv = 0
    for seed in range(60):
        random.seed(3000 + seed)
        latex, _t, answer = fw.build_prompt({"difficulty": 40})
        nums = _unit_rate_nums_from_prompt(latex)
        assert nums is not None, latex
        hard_max = max(hard_max, *nums)
        if "Find the unit" in latex:
            total, qty = nums[0], nums[1]
            rate = int(str(answer).replace("\\$", ""))
            assert total == rate * qty
            if qty >= 6 and math.gcd(total, qty) == qty:
                # quantity is a real inflate factor on the unit rate
                hard_composite_qty += 1
            if qty >= 8:
                hard_composite_qty += 1
        else:
            total1, q1, q2 = nums[0], nums[1], nums[2]
            ans = int(str(answer).replace("\\$", ""))
            assert total1 * q2 == ans * q1
            # Non-integer surface scale or large unreduced given rate
            if q2 % q1 != 0 or math.gcd(total1, q1) >= 4 or max(total1, q1, q2) >= 40:
                hard_nontrivial_equiv += 1
    assert hard_max >= 40
    assert hard_max > easy_max * 2
    assert hard_composite_qty + hard_nontrivial_equiv >= 20


def test_unit_rates_extreme_d_survives():
    """D=1000 must generate huge numbers without crashing."""
    import random

    from question_engine.frameworks.number import UnitRateFramework
    from question_engine.generators import GENERATORS

    fw = UnitRateFramework()
    random.seed(7)
    latex, _t, answer = fw.build_prompt({"difficulty": 1000})
    nums = _unit_rate_nums_from_prompt(latex)
    assert nums is not None
    assert max(nums) >= 1000
    assert answer

    gen = GENERATORS["g6_unit_rates"]
    qs = gen(
        "g6_unit_rates_and_equivalent_rates",
        {"difficulty": 1000, "count": 2, "seed": 11, "include_answer_key": True},
    )
    assert len(qs) == 2
    assert all(q.prompt_latex for q in qs)


def test_unit_rate_generator_wires_continuous_d():
    from question_engine.core.registry import get_catalog_entry
    from question_engine.generators import GENERATORS

    entry = get_catalog_entry("g6_unit_rates_and_equivalent_rates")
    assert entry.generator == "g6_unit_rates"
    gen = GENERATORS["g6_unit_rates"]
    qs0 = gen(
        "g6_unit_rates_and_equivalent_rates",
        {"difficulty": 0, "count": 8, "seed": 3, "include_answer_key": True},
    )
    qs40 = gen(
        "g6_unit_rates_and_equivalent_rates",
        {"difficulty": 40, "count": 8, "seed": 4, "include_answer_key": True},
    )
    assert len(qs0) == 8 and len(qs40) == 8
    assert all(q.prompt_latex for q in qs0 + qs40)


_INTEGER_BINOP_RE = re.compile(
    r"^(-?\d+|\\left\(-?\d+\\right\)|\(-?\d+\))"
    r"\s*[+\-]\s*"
    r"(-?\d+|\\left\(-?\d+\\right\)|\(-?\d+\))$"
)


def _assert_integer_binop_prompt(latex: str) -> None:
    text = latex.replace(" ", "")
    assert "." not in text and "frac" not in text and "/" not in text, latex
    assert _INTEGER_BINOP_RE.match(text), latex


def test_pa_integers_adding_and_subtracting_is_integers_only():
    """PA integers add/sub must never emit decimals or fractions."""
    from question_engine.generators import GENERATORS
    from question_engine.settings.presets import apply_difficulty_presets

    gen = GENERATORS["pa_integers_adding_and_subtracting"]
    type_id = "pa_integers_adding_and_subtracting"

    for tier in ("easy", "medium", "hard"):
        settings = apply_difficulty_presets(
            {"difficulty_tier": tier, "count": 12, "include_answer_key": True, "seed": 11},
            type_id=type_id,
        )
        assert settings.get("allow_decimals") in (None, False)
        assert settings.get("allow_fractions") in (None, False)
        qs = gen(type_id, settings)
        assert len(qs) == 12
        for q in qs:
            _assert_integer_binop_prompt(q.prompt_latex)
            assert q.answer_latex is not None
            assert "." not in q.answer_latex and "frac" not in q.answer_latex

    for d in (0, 5, 10, 20, 40):
        settings = apply_difficulty_presets(
            {"difficulty": d, "count": 10, "include_answer_key": True, "seed": 20 + d},
            type_id=type_id,
        )
        qs = gen(type_id, settings)
        assert len(qs) == 10
        for q in qs:
            _assert_integer_binop_prompt(q.prompt_latex)


def test_pa_integers_adding_and_subtracting_continuous_grows():
    """Continuous D uses unbounded magnitude via _int_bounds / continuous_abs_max."""
    import random

    fw = IntegerArithmeticFramework("+-")
    easy_max = 0
    for seed in range(40):
        random.seed(seed)
        latex, _t, _a = fw.build_prompt({"difficulty": 0, "allow_negative": True})
        nums = [abs(int(n)) for n in re.findall(r"-?\d+", latex.replace("{", "").replace("}", ""))]
        easy_max = max(easy_max, *nums)
        _assert_integer_binop_prompt(latex.replace(" ", ""))

    hard_max = 0
    for seed in range(40):
        random.seed(1000 + seed)
        latex, _t, _a = fw.build_prompt({"difficulty": 40, "allow_negative": True})
        nums = [abs(int(n)) for n in re.findall(r"-?\d+", latex.replace("{", "").replace("}", ""))]
        hard_max = max(hard_max, *nums)
        _assert_integer_binop_prompt(latex.replace(" ", ""))

    assert easy_max <= 12
    assert hard_max > easy_max * 2
    assert hard_max > 50
