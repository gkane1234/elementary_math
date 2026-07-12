"""Tests for difficulty-tier setting presets."""

from __future__ import annotations

from question_engine.settings.presets import (
    apply_difficulty_presets,
    lookup_difficulty_preset,
)
from question_engine.settings.resolve import TypeSettingConfig, resolve_type_settings


def test_equation_hard_preset_widens_coefficients():
    easy = lookup_difficulty_preset("easy", setting_profile="equation")
    hard = lookup_difficulty_preset("hard", setting_profile="equation")
    assert easy["coef_max"] < hard["coef_max"]
    assert hard["integer_only"] is False


def test_apply_presets_fills_gaps_but_keeps_overrides():
    resolved = apply_difficulty_presets(
        {"difficulty_tier": "hard", "coef_max": 7},
        setting_profile="equation",
    )
    assert resolved["coef_max"] == 7
    assert resolved["coef_min"] == -20
    assert resolved["difficulty_tier"] == "hard"


def test_difficulty_group_appears_before_domain_groups():
    schema = resolve_type_settings(
        TypeSettingConfig(setting_profile="equation", inherits=("common_enrichment",))
    )
    groups = [field.group for field in schema if field.group]
    assert "difficulty" in groups
    assert "equation" in groups
    assert groups.index("difficulty") < groups.index("equation")


def test_consecutive_integers_presets_differ_by_tier():
    easy = lookup_difficulty_preset(
        "easy", type_id="consecutive_integers_word_problems"
    )
    medium = lookup_difficulty_preset(
        "medium", type_id="consecutive_integers_word_problems"
    )
    hard = lookup_difficulty_preset(
        "hard", type_id="consecutive_integers_word_problems"
    )
    assert easy["max_consecutive_count"] == 3
    assert medium["min_consecutive_count"] == 3
    assert medium["max_consecutive_count"] == 4
    assert hard["min_consecutive_count"] == 4
    assert hard["max_consecutive_count"] == 5
    assert easy["allow_consecutive_even"] is False
    assert medium["allow_consecutive_even"] is True
    assert hard["allow_product_goal"] is True
    assert easy["allow_product_goal"] is False


def test_consecutive_integers_apply_presets_fill_count_bounds():
    resolved = apply_difficulty_presets(
        {"difficulty_tier": "hard"},
        type_id="consecutive_integers_word_problems",
    )
    assert resolved["min_consecutive_count"] == 4
    assert resolved["max_consecutive_count"] == 5
    assert resolved["allow_product_goal"] is True
    assert resolved["difficulty"] == "hard"


def test_drt_presets_differ_by_structure():
    easy = lookup_difficulty_preset("easy", type_id="wp_distance_rate_time")
    medium = lookup_difficulty_preset("medium", type_id="wp_distance_rate_time")
    hard = lookup_difficulty_preset("hard", type_id="wp_distance_rate_time")
    assert easy["allow_drt_find_missing"] is True
    assert easy["allow_drt_opposite"] is False
    assert medium["allow_drt_round_trip"] is True
    assert medium["allow_drt_opposite"] is False
    assert hard["allow_drt_find_missing"] is False
    assert hard["allow_drt_opposite"] is True
    assert hard["allow_drt_same_direction"] is True


def test_work_presets_differ_by_structure():
    easy = lookup_difficulty_preset("easy", type_id="wp_work")
    medium = lookup_difficulty_preset("medium", type_id="work_word_problems")
    hard = lookup_difficulty_preset("hard", type_id="wp_work")
    assert easy["allow_work_together"] is True
    assert easy["allow_work_pipes"] is False
    assert medium["allow_work_three"] is True
    assert medium["allow_work_together"] is False
    assert hard["allow_work_starts_later"] is True
    assert hard["allow_work_pipes"] is True
    assert hard["allow_work_together"] is False


def test_exponential_growth_decay_presets_differ_by_tier():
    easy = lookup_difficulty_preset("easy", type_id="exponential_growth_decay")
    medium = lookup_difficulty_preset("medium", type_id="exponential_growth_decay")
    hard = lookup_difficulty_preset("hard", type_id="exponential_growth_decay")
    assert easy["ask_mode"] == "find_final"
    assert easy["periods_max"] == 4
    assert easy["allow_compare"] is False
    assert medium["ask_mode"] == "mixed"
    assert medium["allow_how_much_more"] is True
    assert medium["allow_compare"] is False
    assert hard["allow_compare"] is True
    assert hard["allow_threshold"] is True
    assert hard["allow_half_life"] is True
    assert hard["allow_fractional_periods"] is True
    assert hard["periods_max"] > medium["periods_max"] > easy["periods_max"]
    assert hard["rate_max"] > medium["rate_max"] >= easy["rate_max"]


def test_more_on_slope_presets_differ_by_tier():
    easy = lookup_difficulty_preset("easy", type_id="more_on_slope")
    medium = lookup_difficulty_preset("medium", type_id="more_on_slope")
    hard = lookup_difficulty_preset("hard", type_id="more_on_slope")
    assert easy["allow_from_points"] is True
    assert easy["allow_from_graph"] is True
    assert easy["allow_find_equation"] is False
    assert easy["allow_parallel_perpendicular"] is False
    assert easy["show_points"] is False
    assert medium["allow_find_equation"] is True
    assert medium["allow_parallel_perpendicular"] is True
    assert hard["allow_parallel_perpendicular"] is True
    assert hard["slope_max"] > medium["slope_max"] > easy["slope_max"]
    # Profile presets match generator overrides for this type.
    profile = lookup_difficulty_preset("medium", setting_profile="more_on_slope")
    assert profile["allow_parallel_perpendicular"] is True


def test_a2_discrete_exponential_growth_decay_presets_match():
    a1 = lookup_difficulty_preset("hard", type_id="exponential_growth_decay")
    a2 = lookup_difficulty_preset(
        "hard",
        type_id="a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems",
    )
    assert a1 == a2
    assert a2["discrete_only"] is True
    assert a2["ask_mode"] == "mixed"


def test_scientific_notation_presets_differ_by_tier():
    easy = lookup_difficulty_preset("easy", setting_profile="scientific_notation")
    medium = lookup_difficulty_preset("medium", setting_profile="scientific_notation")
    hard = lookup_difficulty_preset("hard", setting_profile="scientific_notation")
    assert easy["sci_exp_max"] < medium["sci_exp_max"] < hard["sci_exp_max"]
    assert easy["allow_negative_exponents"] is False
    assert medium["allow_negative_exponents"] is True
    assert easy["sci_write_direction"] == "to_sci"
    assert medium["sci_write_direction"] == "both"
    assert easy["sci_operation"] == "multiply"
    assert medium["sci_operation"] == "mixed"
    assert easy["require_normalization"] is False
    assert hard["require_normalization"] is True
    assert easy["sci_exp_diff_max"] == 0
    assert medium["sci_exp_diff_min"] == 1
    assert hard["sci_exp_diff_min"] >= 3
    assert hard["allow_magnitude_compare"] is True


def test_absolute_value_inequalities_presets_differ_by_tier():
    easy = lookup_difficulty_preset("easy", type_id="absolute_value_inequalities")
    medium = lookup_difficulty_preset("medium", type_id="absolute_value_inequalities")
    hard = lookup_difficulty_preset("hard", type_id="absolute_value_inequalities")
    assert easy["allow_simple"] is True
    assert easy["allow_linear"] is False
    assert medium["allow_simple"] is False
    assert medium["allow_linear"] is True
    assert medium["allow_abs_vs_linear"] is False
    assert hard["allow_abs_plus_constant"] is True
    assert hard["allow_abs_vs_linear"] is True
    assert easy["coef_max"] < medium["coef_max"] < hard["coef_max"]
    a2 = lookup_difficulty_preset(
        "hard",
        type_id="a2_equations_and_inequalities_absolute_value_inequalities",
    )
    assert a2["allow_abs_vs_linear"] is True


def test_polynomial_multiply_presets_differ_by_tier():
    easy = lookup_difficulty_preset("easy", type_id="polynomial_multiply")
    medium = lookup_difficulty_preset("medium", type_id="polynomial_multiply")
    hard = lookup_difficulty_preset("hard", type_id="polynomial_multiply")
    assert easy["leading_coefficient_one"] is True
    assert easy["allow_trinomial"] is False
    assert easy["max_factor_terms"] == 2
    assert medium["leading_coefficient_one"] is False
    assert medium["allow_trinomial"] is True
    assert medium["max_factor_terms"] == 3
    assert hard["max_factor_terms"] >= 4
    assert hard["leading_coefficient_one"] is False
    pa = lookup_difficulty_preset("easy", type_id="pa_polynomials_multiplying")
    assert pa["leading_coefficient_one"] is True
    a2 = lookup_difficulty_preset("hard", type_id="a2_polynomial_functions_multiplying")
    assert a2["max_factor_terms"] == hard["max_factor_terms"]


def test_absolute_value_inequalities_samples_differ_structurally():
    import random
    import re

    from question_engine.frameworks.equation import AbsoluteValueInequalitiesFramework

    fw = AbsoluteValueInequalitiesFramework()

    def sample_prompts(tier: str, n: int = 16) -> list[str]:
        settings = apply_difficulty_presets(
            {"difficulty_tier": tier},
            type_id="absolute_value_inequalities",
        )
        out: list[str] = []
        for i in range(n):
            random.seed(9000 + i * 17 + len(tier) * 100)
            prompt, _, _ = fw.build_prompt(settings)
            out.append(prompt)
        return out

    easy = sample_prompts("easy")
    medium = sample_prompts("medium")
    hard = sample_prompts("hard")

    unit_or_shift = re.compile(r"^\|x(?: [+-] \d+)?\|")
    linear_coef = re.compile(r"\|-?\d+x")
    plus_const = re.compile(r"\|.+\| [+-] \d+")

    assert any(unit_or_shift.match(p) for p in easy)
    assert not any(linear_coef.search(p) for p in easy)
    assert all(linear_coef.search(p) for p in medium)
    assert any(linear_coef.search(p) for p in hard)
    assert any(plus_const.search(p) or "x +" in p or "x -" in p.split("|")[-1] for p in hard)


def test_compound_inequality_presets_differ_by_tier():
    easy = lookup_difficulty_preset("easy", setting_profile="compound_inequality")
    medium = lookup_difficulty_preset("medium", setting_profile="compound_inequality")
    hard = lookup_difficulty_preset("hard", setting_profile="compound_inequality")
    assert easy["steps"] == 1
    assert medium["steps"] == 2
    assert hard["steps"] == 3
    assert easy["allow_inclusive"] is False
    assert medium["allow_inclusive"] is True
    assert hard["allow_inclusive"] is True
    assert easy["compound_style"] == "mixed"
    assert easy["coef_max"] < medium["coef_max"] < hard["coef_max"]
    assert easy["integer_only"] is True
    assert hard["integer_only"] is False


def test_compound_inequality_samples_differ_structurally():
    import random
    import re

    from question_engine.frameworks.equation import CompoundInequalitiesFramework

    fw = CompoundInequalitiesFramework()

    def sample(tier: str, n: int = 20) -> list[str]:
        settings = apply_difficulty_presets(
            {"difficulty_tier": tier, "include_graph_metadata": True},
            setting_profile="compound_inequality",
        )
        out: list[str] = []
        for i in range(n):
            random.seed(4100 + i * 19 + len(tier) * 80)
            prompt, _, _ = fw.build_prompt(settings)
            out.append(prompt)
        return out

    easy = sample("easy")
    medium = sample("medium")
    hard = sample("hard")

    middle_linear = re.compile(r"-?\d+x")
    distributed = re.compile(r"\d+\(")

    assert all(
        p.startswith("x ") or re.match(r"^-?\d+ (?:\\leq|<) x ", p) for p in easy
    )
    assert not any(middle_linear.search(p) for p in easy)
    assert any(middle_linear.search(p) for p in medium)
    assert not any(distributed.search(p) for p in medium)
    assert any(distributed.search(p) or r"\text{ and }" in p for p in hard)
    assert any(middle_linear.search(p) for p in hard)


def test_polynomial_factoring_presets_follow_leading_coeff_pedagogy():
    easy = lookup_difficulty_preset("easy", setting_profile="polynomial_factoring")
    medium = lookup_difficulty_preset("medium", setting_profile="polynomial_factoring")
    hard = lookup_difficulty_preset("hard", setting_profile="polynomial_factoring")

    assert easy["leading_coefficient_one"] is True
    assert easy["monic_only"] is True
    assert easy["factor_normal"] is True
    assert easy["factor_grouping"] is False
    assert easy["min_degree"] == 2
    assert easy["max_degree"] == 2

    assert medium["leading_coefficient_one"] is False
    assert medium["monic_only"] is False
    assert medium["factor_normal"] is True
    assert medium["max_degree"] == 2

    assert hard["factor_normal"] is False
    assert hard["factor_grouping"] is True
    assert hard["factor_difference_of_cubes"] is True
    assert hard["factor_sum_of_cubes"] is True
    assert hard["factor_difference_of_squares"] is False
    assert hard["min_degree"] >= 3


def test_quadratic_factoring_tiers_generate_expected_shapes():
    import random
    import re

    from question_engine.types.algebra_1.polynomials.quadratic_factoring import (
        QuadraticFactoringQuestionType,
    )

    qt = QuadraticFactoringQuestionType()

    def leading_coeff(prompt: str) -> int:
        match = re.match(r"^(-?\d+)?x", prompt.replace(" ", ""))
        if not match:
            return 1
        raw = match.group(1)
        if raw in (None, ""):
            return 1
        if raw == "-":
            return -1
        return int(raw)

    random.seed(7)
    easy_qs = qt.generate(
        apply_difficulty_presets(
            {"difficulty_tier": "easy", "count": 12, "include_answer_key": True},
            type_id="quadratic_factoring",
        )
    )
    assert all(leading_coeff(q.prompt_text) == 1 for q in easy_qs)
    assert all(q.metadata.get("factoring_method") == "normal" for q in easy_qs)
    assert all(int(q.metadata.get("degree", 0)) == 2 for q in easy_qs)

    random.seed(11)
    medium_qs = qt.generate(
        apply_difficulty_presets(
            {"difficulty_tier": "medium", "count": 12, "include_answer_key": True},
            type_id="quadratic_factoring",
        )
    )
    assert all(abs(leading_coeff(q.prompt_text)) != 1 for q in medium_qs)
    assert all(q.metadata.get("factoring_method") == "normal" for q in medium_qs)
    assert all(int(q.metadata.get("degree", 0)) == 2 for q in medium_qs)

    random.seed(19)
    hard_qs = qt.generate(
        apply_difficulty_presets(
            {"difficulty_tier": "hard", "count": 12, "include_answer_key": True},
            type_id="quadratic_factoring",
        )
    )
    # Hard stays quadratic but unlocks DOS/PST and larger coeffs (still degree 2).
    hard_methods = {q.metadata.get("factoring_method") for q in hard_qs}
    assert hard_methods <= {"normal", "difference_of_squares", "perfect_square_trinomial"}
    assert all(int(q.metadata.get("degree", 0)) == 2 for q in hard_qs)
    assert any(abs(leading_coeff(q.prompt_text)) != 1 for q in hard_qs)


def test_quadratic_square_roots_difficulty_forms():
    easy = lookup_difficulty_preset("easy", type_id="quadratic_square_roots")
    medium = lookup_difficulty_preset("medium", type_id="quadratic_square_roots")
    hard = lookup_difficulty_preset("hard", type_id="quadratic_square_roots")

    assert easy["allow_isolated"] is True
    assert easy["allow_vertex"] is False
    assert easy["allow_complete_square"] is False

    assert medium["allow_isolated"] is False
    assert medium["allow_vertex"] is True
    assert medium["allow_complete_square"] is False

    assert hard["allow_isolated"] is False
    assert hard["allow_vertex"] is True
    assert hard["allow_complete_square"] is True

    a2 = lookup_difficulty_preset(
        "hard",
        type_id="a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots",
    )
    assert a2 == hard


def test_quadratic_square_roots_easy_vs_hard_prompts():
    import re
    import random
    from question_engine.core.base import QUESTION_TYPES

    qt = QUESTION_TYPES["quadratic_square_roots"]

    random.seed(7)
    easy_qs = qt.generate(
        apply_difficulty_presets(
            {"difficulty_tier": "easy", "count": 12, "include_answer_key": True},
            type_id="quadratic_square_roots",
        )
    )
    random.seed(7)
    hard_qs = qt.generate(
        apply_difficulty_presets(
            {"difficulty_tier": "hard", "count": 12, "include_answer_key": True},
            type_id="quadratic_square_roots",
        )
    )

    def looks_isolated(latex: str) -> bool:
        # ax^2 = k or (x ± h)^2 = k with no leftover linear/constant on the squared side.
        return bool(re.fullmatch(r"(?:\d+)?x\^\{?2\}? = -?\d+", latex)) or bool(
            re.fullmatch(r"\(x [+-] \d+\)\^\{?2\}? = -?\d+", latex)
        )

    def looks_vertex(latex: str) -> bool:
        return "(x" in latex and (
            " = 0" in latex or re.search(r"\)\^\{?2\}? = ", latex) is not None
        )

    def looks_standard(latex: str) -> bool:
        return ("x^{2}" in latex or "x^2" in latex) and "x" in latex and "(" not in latex

    assert all(looks_isolated(q.prompt_latex) for q in easy_qs)
    assert not any(looks_isolated(q.prompt_latex) for q in hard_qs)
    assert any(looks_vertex(q.prompt_latex) or looks_standard(q.prompt_latex) for q in hard_qs)


def test_quadratic_inequality_presets_differ_by_tier():
    easy = lookup_difficulty_preset("easy", setting_profile="quadratic_inequality_graph")
    medium = lookup_difficulty_preset("medium", setting_profile="quadratic_inequality_graph")
    hard = lookup_difficulty_preset("hard", setting_profile="quadratic_inequality_graph")
    assert easy["allow_messy_form"] is False
    assert easy["allow_factored_form"] is False
    assert easy["allow_stretch"] is False
    assert easy["allow_standard_form"] is True
    assert easy["allow_lte"] is False
    assert medium["allow_factored_form"] is True
    assert medium["allow_messy_form"] is True
    assert medium["allow_stretch"] is True
    assert medium["allow_lte"] is True
    assert hard["integer_only"] is False
    assert hard["allow_messy_form"] is True
    assert easy["coef_max"] < medium["coef_max"] <= hard["coef_max"]
    assert easy != hard


def test_quadratic_inequality_samples_need_algebra_on_harder_tiers():
    import random
    import re

    from question_engine.frameworks.graphing import GraphQuadraticInequalityFramework

    fw = GraphQuadraticInequalityFramework()

    def sample(tier: str, n: int = 24) -> list[str]:
        settings = apply_difficulty_presets(
            {"difficulty_tier": tier, "include_graph_metadata": True},
            type_id="graph_quadratic_inequality",
            setting_profile="quadratic_inequality_graph",
        )
        out: list[str] = []
        for i in range(n):
            random.seed(5200 + i * 23 + len(tier) * 90)
            prompt, _, _ = fw.build_prompt(settings)
            out.append(prompt)
        return out

    easy = sample("easy")
    medium = sample("medium")
    hard = sample("hard")

    # Easy: clean y relation vertex/standard; no factored / scale / rearrange.
    assert all(p.startswith("y ") for p in easy)
    assert not any(")(" in p for p in easy)
    assert not any(re.search(r"^\d+y ", p) for p in easy)
    assert not any(re.search(r"^y [+-] ", p) for p in easy)
    assert not any(r"\frac" in p for p in easy)

    def needs_algebra(p: str) -> bool:
        return bool(
            ")(" in p
            or re.search(r"^\d+y ", p)
            or re.search(r"^y [+-] ", p)
            or r"\frac" in p
            or re.search(r"(?<![0-9])[23]\(x", p)
            or re.search(r"-[23]\(x", p)
        )

    assert any(needs_algebra(p) for p in medium)
    assert any(needs_algebra(p) for p in hard)
    assert any(
        r"\frac" in p or re.search(r"^\d+y ", p) or re.search(r"^y [+-] ", p)
        for p in hard
    )


def test_quadratic_profile_easy_is_monic():
    easy = lookup_difficulty_preset("easy", setting_profile="quadratic")
    medium = lookup_difficulty_preset("medium", setting_profile="quadratic")
    hard = lookup_difficulty_preset("hard", setting_profile="quadratic")
    assert easy["leading_coefficient_one"] is True
    assert easy["monic_only"] is True
    assert medium["leading_coefficient_one"] is False
    assert medium["monic_only"] is False
    assert hard["leading_coefficient_one"] is False
    assert hard["coef_max"] > medium["coef_max"] > easy["coef_max"]

    formula_easy = lookup_difficulty_preset(
        "easy", type_id="quadratic_formula", setting_profile="quadratic"
    )
    assert formula_easy["monic_only"] is True
    sq_easy = lookup_difficulty_preset("easy", type_id="quadratic_square_roots")
    assert sq_easy["monic_only"] is True
    sq_hard = lookup_difficulty_preset("hard", type_id="quadratic_square_roots")
    assert sq_hard["monic_only"] is False


def test_quadratic_formula_easy_monic_vs_hard_nonunit():
    import random
    import re

    from question_engine.core.base import QUESTION_TYPES

    qt = QUESTION_TYPES["quadratic_formula"]

    def leading_coeff(prompt: str) -> int:
        match = re.match(r"^(-?\d+)?x", prompt.replace(" ", ""))
        if not match:
            return 1
        raw = match.group(1)
        if raw in (None, ""):
            return 1
        if raw == "-":
            return -1
        return int(raw)

    random.seed(41)
    easy_qs = qt.generate(
        apply_difficulty_presets(
            {"difficulty_tier": "easy", "count": 16, "include_answer_key": True},
            type_id="quadratic_formula",
        )
    )
    assert all(leading_coeff(q.prompt_latex) == 1 for q in easy_qs)

    random.seed(43)
    hard_qs = qt.generate(
        apply_difficulty_presets(
            {"difficulty_tier": "hard", "count": 20, "include_answer_key": True},
            type_id="quadratic_formula",
        )
    )
    assert any(abs(leading_coeff(q.prompt_latex)) != 1 for q in hard_qs)


def test_format_polynomial_omits_unit_and_zero_coeffs():
    from packages.polynomial_core import format_polynomial_latex

    assert format_polynomial_latex([1, -1, 0]) == "x^{2} - x"
    assert format_polynomial_latex([1, 1, -3]) == "x^{2} + x - 3"
    assert format_polynomial_latex([-1, 0, 4]) == "-x^{2} + 4"
    assert format_polynomial_latex([2, 0, -5]) == "2x^{2} - 5"


def test_radical_equations_difficulty_forms():
    easy = lookup_difficulty_preset("easy", type_id="radical_equations")
    medium = lookup_difficulty_preset("medium", type_id="radical_equations")
    hard = lookup_difficulty_preset("hard", type_id="radical_equations")

    assert easy["allow_light_prep"] is True
    assert easy["allow_isolate_algebra"] is False
    assert easy["allow_two_radicals"] is False
    assert easy["integer_only"] is True

    assert medium["allow_light_prep"] is False
    assert medium["allow_isolate_algebra"] is True
    assert medium["allow_radical_equals_linear"] is True
    assert medium["allow_two_radicals"] is False
    assert medium["integer_only"] is True

    assert hard["allow_two_radicals"] is True
    assert hard["allow_light_prep"] is False
    assert hard["integer_only"] is True

    a2 = lookup_difficulty_preset(
        "hard",
        type_id="a2_radical_functions_and_rational_exponents_radical_equations",
    )
    assert a2 == hard


def test_radical_equations_easy_vs_hard_prompts():
    import re
    import random
    from question_engine.core.base import QUESTION_TYPES

    qt = QUESTION_TYPES["radical_equations"]

    random.seed(11)
    easy_qs = qt.generate(
        apply_difficulty_presets(
            {"difficulty_tier": "easy", "count": 16, "include_answer_key": True},
            type_id="radical_equations",
        )
    )
    random.seed(11)
    hard_qs = qt.generate(
        apply_difficulty_presets(
            {"difficulty_tier": "hard", "count": 16, "include_answer_key": True},
            type_id="radical_equations",
        )
    )

    def sqrt_count(latex: str) -> int:
        return latex.count("\\sqrt")

    def has_decimal_coef(latex: str) -> bool:
        return bool(re.search(r"\d+\.\d+", latex))

    assert all(not has_decimal_coef(q.prompt_latex) for q in easy_qs + hard_qs)
    assert all(sqrt_count(q.prompt_latex) == 1 for q in easy_qs)
    assert any(sqrt_count(q.prompt_latex) >= 2 for q in hard_qs)
    assert any(
        q.answer_latex and "extraneous" in q.answer_latex for q in hard_qs + easy_qs
    )
