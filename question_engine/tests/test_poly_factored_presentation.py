"""Unfactorable / RRT-demanding polys prefer factored presentation; RRT off by default."""

from __future__ import annotations

from packages.polynomial_core import (
    NONCLASSROOM_FACTOR_STEP_FLAG,
    FactorablePolynomialOptions,
    collect_nonclassroom_factor_step_details,
    format_polynomial_from_factors,
    is_classroom_factorable,
    should_display_factor_product_expanded,
)
from packages.polynomial_core.polynomial import Polynomial
from packages.polynomial_core.rational import RationalExpressionTerm
from question_engine.frameworks.graphing import _sample_solve_by_graphing
from question_engine.frameworks.primitives import (
    PRIM_NUMBERS,
    PRIM_VARIABLE,
    build_context,
)
from question_engine.frameworks.primitives.constructive import construct_rational_sum
from question_engine.frameworks.primitives.expression_policy import POLYNOMIAL_POLICY_DEFAULT
from question_engine.settings.factoring_settings import parse_factoring_settings
from question_engine.settings.generator_profiles import schema_for_generator


def test_rrt_deselected_by_default_in_parse_and_schema():
    parsed = parse_factoring_settings({})
    assert parsed.rrt_mode == "exclude"
    assert parsed.enabled_methods["rrt"] is False

    opts = FactorablePolynomialOptions(coef_min=-5, coef_max=5)
    assert opts.rrt_mode == "exclude"
    assert "rrt" not in opts.enabled_method_pool()

    for gen in (
        "quadratic_factoring",
        "polynomial_factoring_grouping",
        "a2_polynomial_functions_factoring_all_techniques",
    ):
        fields = {f.key: f for f in schema_for_generator(gen)}
        assert fields["factor_rrt"].default is False


def test_three_plus_linears_stay_factored_when_rrt_excluded():
    factors = (Polynomial([1, -1]), Polynomial([1, -2]), Polynomial([1, 3]), Polynomial([1, 4]))
    exclude = FactorablePolynomialOptions(coef_min=-6, coef_max=6, rrt_mode="exclude")
    allow = FactorablePolynomialOptions(
        coef_min=-6,
        coef_max=6,
        rrt_mode="allow",
        enabled_methods={"rrt": True, "normal": True},
    )

    assert should_display_factor_product_expanded(factors, exclude) is False
    assert should_display_factor_product_expanded(factors, allow) is True

    factored = format_polynomial_from_factors(factors, exclude)
    assert factored.startswith("(")
    assert "x^{" not in factored or factored.count("(") >= 3

    expanded = format_polynomial_from_factors(factors, allow)
    assert "(" not in expanded
    assert "x^{4}" in expanded or "x^4" in expanded.replace("{", "").replace("}", "")


def test_two_linears_still_expand_for_normal_factoring():
    factors = (Polynomial([1, -2]), Polynomial([1, 3]))
    opts = FactorablePolynomialOptions(coef_min=-6, coef_max=6, rrt_mode="exclude")
    assert should_display_factor_product_expanded(factors, opts) is True
    latex = format_polynomial_from_factors(factors, opts)
    assert "(" not in latex


def test_constant_plus_two_linears_still_expand():
    """Leading constant does not turn a classroom quadratic into an RRT problem."""
    factors = (Polynomial([2]), Polynomial([1, -1]), Polynomial([1, 2]))
    opts = FactorablePolynomialOptions(coef_min=-6, coef_max=6, rrt_mode="exclude")
    assert should_display_factor_product_expanded(factors, opts) is True


def test_solve_by_graphing_cubic_prefers_factored_without_rrt():
    settings = {
        "leading_coefficient_one": True,
        "monic_only": True,
        "allow_factored_form": False,
        "factor_rrt": False,
        "min_degree": 3,
        "max_degree": 3,
        "root_min": -4,
        "root_max": 4,
        "coef_min": 1,
        "coef_max": 1,
        "integer_only": True,
    }
    for _ in range(12):
        prompt, _, _, roots, _ = _sample_solve_by_graphing(settings)
        if len(roots) < 3:
            continue
        assert "(x" in prompt or "x +" in prompt or "x -" in prompt
        assert prompt.count("(") >= 2
        return
    raise AssertionError("expected at least one cubic sample")


def _rational_ctx(seed: int = 0, **extra):
    settings = {"count": 1, "seed": seed, "factor_rrt": False, **extra}
    return build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE],
        policy=POLYNOMIAL_POLICY_DEFAULT,
        leaf_id="rational_expression_simplification",
    )


def test_rational_add_quadratic_dens_expand_when_rrt_off():
    """Two-linear dens (quadratic) stay expanded — classroom factoring for LCD."""
    seen_quad = False
    for seed in range(16):
        ctx = _rational_ctx(seed)
        surface = construct_rational_sum(ctx, d=10.0, cancel_count=1, as_sum=True)
        if "x^{2}" in surface.latex:
            seen_quad = True
            # cancel_count=1 → at most 2 linear dens per term → no cubic/quartic dens.
            assert "x^{3}" not in surface.latex
            assert "x^{4}" not in surface.latex
    assert seen_quad


def test_rational_add_three_plus_linears_factored_when_rrt_off():
    """3+ linear dens stay factored unless RRT is enabled."""
    found = False
    for seed in range(24):
        ctx = _rational_ctx(seed)
        surface = construct_rational_sum(
            ctx, d=14.0, cancel_count=2, as_sum=True, n_terms=3
        )
        if r"\left(" in surface.latex and surface.latex.count(r"\left(") >= 3:
            found = True
            assert "x^{3}" not in surface.latex
            assert "x^{4}" not in surface.latex
            break
    assert found


def test_rational_add_three_plus_linears_may_expand_when_rrt_on():
    found = False
    for seed in range(12):
        ctx = _rational_ctx(seed, factor_rrt=True)
        surface = construct_rational_sum(ctx, d=14.0, cancel_count=2, as_sum=True, n_terms=3)
        # With RRT on, multi-linear products are allowed to expand to x^{3}/x^{4}.
        if "x^{3}" in surface.latex or "x^{4}" in surface.latex or r"\left(" in surface.latex:
            found = True
            break
    assert found

def test_inflated_three_linear_lcd_den_stays_factored_when_rrt_off():
    """Regression: inflation must not expand a 3-linear den after a 2-linear expand decision.

    Shape like ``…/(4x-5)(3x-5)(x-3) + 4/(4x-5)`` — dense cubic would need RRT.
    """
    import random

    from packages.polynomial_core import (
        build_rational_expression_problem,
        should_display_factor_product_expanded,
        sum_of_fractions_latex,
    )
    from question_engine.factoring_settings import build_factorable_options

    opts = build_factorable_options(
        {"factor_rrt": False, "coef_min": -5, "coef_max": 5},
        target_degree_min=1,
        target_degree_max=1,
    )
    found = False
    for seed in range(80):
        random.seed(seed)
        sol = build_rational_expression_problem(
            opts,
            term_count=2,
            allow_polynomial_terms=False,
            allow_full_lcd_terms=False,
            inflation_chance=1.0,
            cancel_factor_count=0,
            max_lcd_factors=2,
            prefer_simple_factors=True,
            content_primitive=True,
            allow_empty_denominators=False,
        )
        for term in sol.display_terms:
            variable = [f for f in term.denominator_factors if f.deg() >= 1]
            if len(variable) < 3:
                continue
            found = True
            assert term.denominator_display_expanded is False
            assert should_display_factor_product_expanded(term.denominator_factors, opts) is False
            latex = sum_of_fractions_latex(list(sol.display_terms))
            assert "x^{3}" not in latex
            assert "(" in latex or r"\left(" in latex
            break
        if found:
            break
    assert found, "expected an inflated 3-linear denominator sample"


def test_add_then_cancel_avoids_per_term_cancel_inflation():
    """cancel_factor_count means cancel after combining — not per-term num/den inflate."""
    import random

    from packages.polynomial_core import build_rational_expression_problem
    from packages.polynomial_core.rational import _numerator_shares_den_factor
    from question_engine.factoring_settings import build_factorable_options

    opts = build_factorable_options(
        {"factor_rrt": False, "coef_min": -8, "coef_max": 8},
        target_degree_min=1,
        target_degree_max=1,
    )
    for cancel in (1, 2):
        per_term = 0
        frac_terms = 0
        for seed in range(36):
            random.seed(seed)
            sol = build_rational_expression_problem(
                opts,
                term_count=3,
                allow_polynomial_terms=False,
                allow_full_lcd_terms=False,
                inflation_chance=0,
                cancel_factor_count=cancel,
                max_lcd_factors=4,
                prefer_simple_factors=True,
                content_primitive=True,
                allow_empty_denominators=False,
            )
            assert len(sol.cancelled_lcd_factors) == cancel
            for term in sol.display_terms:
                if term.is_polynomial_term or not term.denominator_factors:
                    continue
                frac_terms += 1
                if _numerator_shares_den_factor(term.numerator, term.denominator_factors):
                    per_term += 1
        assert frac_terms >= 60
        # Light spice may create a few; must stay rare (not the main mechanism).
        assert per_term / frac_terms < 0.15, (
            f"cancel={cancel}: per-term cancel rate {per_term}/{frac_terms}"
        )


def test_rational_answer_stays_factored_for_multi_linear_remaining():
    """Remaining dens factors stay factored in the answer when RRT is off (2+)."""
    import random

    from packages.polynomial_core import build_rational_expression_problem
    from packages.polynomial_core.rational import format_simplified_rational_latex
    from question_engine.factoring_settings import build_factorable_options

    opts = build_factorable_options(
        {"factor_rrt": False, "coef_min": -6, "coef_max": 6},
        target_degree_min=1,
        target_degree_max=1,
    )
    found = False
    for seed in range(80):
        random.seed(seed)
        sol = build_rational_expression_problem(
            opts,
            term_count=3,
            allow_polynomial_terms=False,
            allow_full_lcd_terms=False,
            inflation_chance=0,
            cancel_factor_count=1,
            max_lcd_factors=4,
            prefer_simple_factors=True,
            content_primitive=True,
            allow_empty_denominators=False,
        )
        if len(sol.final_denominator_factors) < 2:
            continue
        found = True
        latex = format_simplified_rational_latex(
            sol.final_numerator or sol.simplified_numerator,
            sol.final_denominator or sol.simplified_denominator,
            numerator_factors=sol.final_numerator_factors,
            denominator_factors=sol.final_denominator_factors,
            options=opts,
        )
        assert "x^{2}" not in latex or "(" in latex or r"\left(" in latex
        assert "x^{3}" not in latex
        assert "x^{4}" not in latex
        # 2+ remaining linears must stay factored (not a lone expanded quadratic dens).
        assert "(" in latex or r"\left(" in latex
        break
    assert found, "expected a sample with 2+ remaining dens factors"


def test_combined_before_cancel_step_shows_expanded_hand_factorable_numerator():
    """Cancel≥1 combined step shows expanded num students can factor by hand.

    No construction-secret factorization of the combined numerator — students
    only have the expanded sum after adding over the LCD.
    """
    import random

    from packages.polynomial_core import build_rational_expression_problem
    from question_engine.factoring_settings import build_factorable_options

    opts = build_factorable_options(
        {"factor_rrt": False, "coef_min": -6, "coef_max": 6},
        target_degree_min=1,
        target_degree_max=1,
    )
    found = False
    for seed in range(80):
        random.seed(seed)
        sol = build_rational_expression_problem(
            opts,
            term_count=3,
            allow_polynomial_terms=False,
            allow_full_lcd_terms=False,
            inflation_chance=0,
            cancel_factor_count=2,
            max_lcd_factors=4,
            prefer_simple_factors=True,
            content_primitive=True,
            allow_empty_denominators=False,
        )
        if len(sol.cancelled_lcd_factors) < 2:
            continue
        roles = {s["role"]: s["latex"] for s in sol.generation_steps if isinstance(s, dict)}
        combined = roles.get("combined_before_cancel")
        if not combined:
            continue
        found = True
        # Expanded combined num must stay classroom-factorable (≤ quadratic).
        assert sol.combined_numerator.deg() <= 2
        assert "x^{3}" not in combined
        assert "x^{4}" not in combined
        assert "x^{5}" not in combined
        # Numerator side should be expanded (no secret cancel-product display).
        assert combined.startswith(r"\frac{")
        inner = combined[len(r"\frac{") :]
        depth = 1
        num_end = None
        for i, ch in enumerate(inner):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    num_end = i
                    break
        assert num_end is not None
        num_tex = inner[:num_end]
        # Expanded quadratic/linear — not a parenthesized factor product of cancels.
        # Dens may still be factored (LCD rewrite exposes those factors).
        assert "(" not in num_tex and r"\left(" not in num_tex
        break
    assert found, "expected cancel≥2 sample with combined_before_cancel step"


def test_high_cancel_request_clamps_for_hand_factorable_end_cancel():
    """Requested cancel≥3 with RRT off clamps so combined num stays ≤ quadratic."""
    import random

    from packages.polynomial_core import build_rational_expression_problem
    from question_engine.factoring_settings import build_factorable_options

    opts = build_factorable_options(
        {"factor_rrt": False, "coef_min": -6, "coef_max": 6},
        target_degree_min=1,
        target_degree_max=1,
    )
    for seed in range(40):
        random.seed(seed)
        sol = build_rational_expression_problem(
            opts,
            term_count=3,
            allow_polynomial_terms=False,
            allow_full_lcd_terms=False,
            inflation_chance=0,
            cancel_factor_count=5,
            max_lcd_factors=6,
            prefer_simple_factors=True,
            content_primitive=True,
            allow_empty_denominators=False,
        )
        assert len(sol.cancelled_lcd_factors) <= 2
        if sol.cancelled_lcd_factors:
            assert sol.combined_numerator.deg() <= 2
            roles = {s["role"]: s["latex"] for s in sol.generation_steps if isinstance(s, dict)}
            combined = roles.get("combined_before_cancel", "")
            assert "x^{3}" not in combined
            assert "x^{4}" not in combined


def test_rrt_hard_numerator_stays_factored_in_display_term():
    """3+ linear numerator factors stay factored when RRT is excluded."""
    from packages.polynomial_core import FactorablePolynomialOptions
    from packages.polynomial_core.polynomial import Polynomial
    from packages.polynomial_core.rational import (
        _build_fraction_display_term,
        term_numerator_latex,
    )

    opts = FactorablePolynomialOptions(coef_min=-6, coef_max=6, rrt_mode="exclude")
    factors = (Polynomial([1, -1]), Polynomial([1, -2]), Polynomial([1, 3]))
    product = factors[0] * factors[1] * factors[2]
    dens = (Polynomial([1, 4]), Polynomial([1, 5]), Polynomial([1, 6]))
    term = _build_fraction_display_term(
        product,
        dens,
        Polynomial([1]),
        opts,
        numerator_factors=factors,
    )
    assert term.numerator_display_expanded is False
    num_latex = term_numerator_latex(term)
    assert "x^{3}" not in num_latex
    assert num_latex.count("(") >= 2 or r"\left(" in num_latex


def test_is_classroom_factorable_quadratic_and_gcf():
    opts = FactorablePolynomialOptions(coef_min=-6, coef_max=6, rrt_mode="exclude")
    linear = Polynomial([1, -2])
    quadratic = Polynomial([1, -1]) * Polynomial([1, -3])
    assert is_classroom_factorable(linear, opts) is True
    assert is_classroom_factorable(quadratic, opts, factors=(Polynomial([1, -1]), Polynomial([1, -3]))) is True
    # Constant × two linears still classroom (GCF + quadratic).
    with_gcf = (Polynomial([2]), Polynomial([1, -1]), Polynomial([1, 4]))
    product = with_gcf[0] * with_gcf[1] * with_gcf[2]
    assert is_classroom_factorable(product, opts, factors=with_gcf) is True


def test_is_classroom_factorable_three_linears_needs_rrt_when_excluded():
    factors = (Polynomial([1, -1]), Polynomial([1, -2]), Polynomial([1, 3]))
    product = factors[0] * factors[1] * factors[2]
    exclude = FactorablePolynomialOptions(coef_min=-6, coef_max=6, rrt_mode="exclude")
    allow = FactorablePolynomialOptions(
        coef_min=-6,
        coef_max=6,
        rrt_mode="allow",
        enabled_methods={"rrt": True, "normal": True},
    )
    assert is_classroom_factorable(product, exclude, factors=factors) is False
    assert is_classroom_factorable(product, allow, factors=factors) is True
    # Deg ≥ 3 with no factors → flag as non-classroom under RRT exclude.
    assert is_classroom_factorable(product, exclude) is False


def test_nonclassroom_factor_step_flag_fires_on_dense_combined_cancel():
    """End-cancel whose expanded combined num needs RRT raises qa flag."""
    opts = FactorablePolynomialOptions(coef_min=-6, coef_max=6, rrt_mode="exclude")
    cancel = (
        Polynomial([1, -1]),
        Polynomial([1, -2]),
        Polynomial([1, 3]),
    )
    combined = cancel[0] * cancel[1] * cancel[2]
    details = collect_nonclassroom_factor_step_details(
        (),
        combined_numerator=combined,
        cancelled_lcd_factors=cancel,
        final_numerator=Polynomial([1]),
        final_numerator_factors=(),
        options=opts,
    )
    assert details
    assert details[0]["flag"] == NONCLASSROOM_FACTOR_STEP_FLAG
    assert details[0]["role"] == "combined_before_cancel"
    assert details[0]["degree"] == 3


def test_nonclassroom_factor_step_flag_silent_on_hand_factorable_quadratic_cancel():
    opts = FactorablePolynomialOptions(coef_min=-6, coef_max=6, rrt_mode="exclude")
    cancel = (Polynomial([1, -1]), Polynomial([1, 4]))
    combined = cancel[0] * cancel[1]
    details = collect_nonclassroom_factor_step_details(
        (),
        combined_numerator=combined,
        cancelled_lcd_factors=cancel,
        final_numerator=Polynomial([1]),
        options=opts,
    )
    assert details == []


def test_nonclassroom_factor_step_flag_fires_on_expanded_prompt_den():
    """Prompt den shown expanded despite needing RRT → flag."""
    opts = FactorablePolynomialOptions(coef_min=-6, coef_max=6, rrt_mode="exclude")
    dens = (Polynomial([1, -1]), Polynomial([1, -2]), Polynomial([1, 3]))
    den = dens[0] * dens[1] * dens[2]
    term = RationalExpressionTerm(
        numerator=Polynomial([1]),
        denominator=den,
        denominator_factors=dens,
        denominator_display_expanded=True,  # incorrect pedagogy
        numerator_factors=(),
        numerator_display_expanded=True,
    )
    details = collect_nonclassroom_factor_step_details(
        (term,),
        combined_numerator=Polynomial([1]),
        cancelled_lcd_factors=(),
        options=opts,
    )
    assert any(d.get("role") == "prompt_denominator" for d in details)
    assert NONCLASSROOM_FACTOR_STEP_FLAG in {d["flag"] for d in details}


def test_generated_hand_factorable_cancel_does_not_set_qa_flag():
    """Live ± generation with RRT off + hand-factorable cancel stays clean."""
    import random

    from packages.polynomial_core import build_rational_expression_problem
    from question_engine.factoring_settings import build_factorable_options

    opts = build_factorable_options(
        {"factor_rrt": False, "coef_min": -6, "coef_max": 6},
        target_degree_min=1,
        target_degree_max=1,
    )
    found = False
    for seed in range(40):
        random.seed(seed)
        sol = build_rational_expression_problem(
            opts,
            term_count=3,
            allow_polynomial_terms=False,
            allow_full_lcd_terms=False,
            inflation_chance=0,
            cancel_factor_count=2,
            max_lcd_factors=4,
            prefer_simple_factors=True,
            content_primitive=True,
            allow_empty_denominators=False,
        )
        if len(sol.cancelled_lcd_factors) < 1:
            continue
        found = True
        assert sol.combined_numerator.deg() <= 2
        assert NONCLASSROOM_FACTOR_STEP_FLAG not in sol.qa_flags
        assert sol.qa_flags == []
        break
    assert found


def test_api_metadata_surfaces_qa_flags_for_nonclassroom_step():
    """Question metadata carries qa_flags when detection fires (synthetic)."""
    from question_engine.api.handler import _annotate_questions
    from question_engine.core.base import QUESTION_TYPES
    from question_engine.models import Question
    from question_engine.settings.enrichment import merge_enrichment_metadata

    qtype = QUESTION_TYPES.get("rational_expression_simplification")
    if qtype is None:
        # Alias used in some catalogs.
        qtype = QUESTION_TYPES.get("a1_rational_expressions_adding_and_subtracting")
    assert qtype is not None

    metadata = merge_enrichment_metadata(
        {"count": 1},
        {
            "qa_flags": [NONCLASSROOM_FACTOR_STEP_FLAG],
            "qa_flag_details": [
                {
                    "flag": NONCLASSROOM_FACTOR_STEP_FLAG,
                    "role": "combined_before_cancel",
                    "degree": 3,
                    "latex": "x^{3}-6x^{2}+11x-6",
                }
            ],
        },
        answer=r"\frac{1}{x-4}",
    )
    question = Question(
        id="t",
        topic=qtype.id,
        prompt_latex="p",
        prompt_text="p",
        answer_latex=r"\frac{1}{x-4}",
        metadata=metadata,
    )
    annotated = _annotate_questions([question], qtype, {"count": 1})
    assert NONCLASSROOM_FACTOR_STEP_FLAG in annotated[0].metadata["qa_flags"]
    assert annotated[0].metadata["qa_flag_details"][0]["role"] == "combined_before_cancel"
