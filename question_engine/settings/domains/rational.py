"""Settings fields for rational-expression question types."""

from __future__ import annotations

from ...core.models import SettingField


def rational_operation_settings() -> list[SettingField]:
    return [
        SettingField("allow_add", "Allow addition", "bool", True, group="rational"),
        SettingField("allow_subtract", "Allow subtraction", "bool", True, group="rational"),
        SettingField("allow_multiply", "Allow multiplication", "bool", True, group="rational"),
        SettingField("allow_divide", "Allow division", "bool", True, group="rational"),
    ]


def division_notation_settings() -> list[SettingField]:
    """Multi-select forms for fraction / rational division prompts.

    At least one must stay enabled; generation falls back to obelus (÷) if none are.
    """
    return [
        SettingField(
            "allow_obelus",
            "Allow ÷ symbol",
            "bool",
            True,
            group="difficulty",
        ),
        SettingField(
            "allow_complex_fraction",
            "Allow complex fraction (stacked)",
            "bool",
            True,
            group="difficulty",
        ),
        SettingField(
            "allow_slash",
            "Allow slash form (a/b) / (c/d)",
            "bool",
            True,
            group="difficulty",
        ),
    ]


def fraction_form_settings() -> list[SettingField]:
    """Controls improper fractions and mixed-number display for arithmetic prompts."""
    return [
        SettingField(
            "allow_mixed",
            "Allow mixed numbers",
            "bool",
            False,
            group="number",
        ),
        SettingField(
            "require_proper",
            "Require proper fractions",
            "bool",
            False,
            group="number",
        ),
    ]


def rational_equation_form_settings() -> list[SettingField]:
    """Selectable templates for rational equations.

    Easy uses a single fraction or simple proportion. Medium adds a constant
    term beside a fraction. Hard uses two rational terms (LCD / extraneous).
    """
    return [
        SettingField(
            "allow_simple_fraction",
            "Allow simple fraction = constant (e.g. a/x = b)",
            "bool",
            True,
            group="rational_equation_forms",
        ),
        SettingField(
            "allow_proportion",
            "Allow proportions (e.g. a/x = b/c)",
            "bool",
            False,
            group="rational_equation_forms",
        ),
        SettingField(
            "allow_fraction_plus_constant",
            "Allow fraction plus a constant (e.g. a/x + b = c)",
            "bool",
            False,
            group="rational_equation_forms",
        ),
        SettingField(
            "allow_two_fractions",
            "Allow two rational terms (LCD; check extraneous)",
            "bool",
            False,
            group="rational_equation_forms",
        ),
    ]


def rational_cancel_count_settings() -> list[SettingField]:
    """How many linear factors cancel — skill control for simplify / ± / ×÷.

    Classroom select keeps 0–3, ``4`` (= all available), and ``auto``. Continuous
    ``difficulty`` with ``auto`` unlocks exact counts beyond 4 unboundedly.
    Integer API values are exact counts (no hard max of 4).

    For add/subtract (±) with RRT off, end-of-addition cancel is clamped so the
    expanded combined numerator stays hand-factorable (typically ≤ 2 factors).
    Simplify and ×÷ can still cancel more because factors stay visible in the prompt.
    """
    return [
        SettingField(
            "cancel_factor_count",
            "Canceling factors",
            "select",
            "1",
            options=["0", "1", "2", "3", "4", "auto"],
            # Same UI section as the difficulty slider (not buried in topic-specific knobs).
            group="difficulty",
        ),
    ]


def rational_rrt_settings() -> list[SettingField]:
    """RRT on/off — presentation / construction for dens that need rational roots."""
    return [
        SettingField(
            "factor_rrt",
            "Rational root theorem (RRT)",
            "bool",
            False,
            # Directly under canceling factors in the topic-options difficulty block.
            group="difficulty",
        ),
    ]


def rational_constructive_adjacent_settings() -> list[SettingField]:
    """Highest-level knobs for constructive rational ± / simplify (under difficulty)."""
    return [
        *rational_cancel_count_settings(),
        *rational_rrt_settings(),
        SettingField(
            "allow_polynomial_terms",
            "Allow terms with no denominator",
            "bool",
            True,
            group="difficulty",
        ),
        SettingField(
            "force_lcd",
            "Force a full-LCD term in every problem",
            "bool",
            False,
            group="difficulty",
        ),
    ]


def rational_simplify_adjacent_settings() -> list[SettingField]:
    """Cancel + RRT for single-fraction simplify (no ± LCD-term knobs)."""
    return [
        *rational_cancel_count_settings(),
        *rational_rrt_settings(),
    ]


def rational_simplification_settings() -> list[SettingField]:
    """Controls for simplify-and-excluded-values rational expressions."""
    return rational_simplify_adjacent_settings()


def rational_multiply_divide_settings() -> list[SettingField]:
    """Structural controls for multiplying / dividing rational expressions."""
    return [
        SettingField(
            "allow_multiply",
            "Allow multiplication",
            "bool",
            True,
            group="difficulty",
        ),
        SettingField(
            "allow_divide",
            "Allow division",
            "bool",
            True,
            group="difficulty",
        ),
        *rational_cancel_count_settings(),
        *rational_rrt_settings(),
        SettingField(
            "max_factor_degree",
            "Max factor degree",
            "int",
            1,
            min=1,
            max=2,
            group="difficulty",
        ),
        SettingField(
            "expand_polynomials",
            "Show expanded polynomials",
            "bool",
            False,
            group="difficulty",
        ),
        SettingField(
            "operand_count",
            "Number of rational factors",
            "int",
            2,
            min=2,
            max=500,
            group="difficulty",
        ),
        SettingField(
            "leading_coefficient_one",
            "Leading coefficient one",
            "bool",
            True,
            group="difficulty",
        ),
    ]


def rational_expression_extra_settings() -> list[SettingField]:
    """Type-specific controls for combining rational terms."""
    return [
        SettingField(
            "term_count",
            "Number of rational terms",
            "int",
            3,
            min=2,
            max=500,
            group="rational",
        ),
        SettingField(
            "add_subtract_structure",
            "Add/subtract structure",
            "select",
            "auto",
            options=["auto", "shared_lcd", "unlike_binomials", "multi_term", "complex"],
            group="rational",
        ),
        SettingField(
            "max_lcd_factors",
            "Max distinct LCD factors",
            "int",
            4,
            min=1,
            max=500,
            group="rational",
        ),
        SettingField(
            "prefer_simple_factors",
            "Prefer small linear denominator factors",
            "bool",
            True,
            group="rational",
        ),
        SettingField(
            "content_primitive_denominators",
            "Strip large content GCFs from factors",
            "bool",
            True,
            group="rational",
        ),
        SettingField(
            "use_random_partial_solution",
            "Use random partial-fraction numerators",
            "bool",
            True,
            group="rational",
        ),
        SettingField(
            "allow_polynomial_terms",
            "Allow terms with no denominator",
            "bool",
            True,
            group="rational",
        ),
        SettingField(
            "allow_full_lcd_terms",
            "Allow terms over the full LCD",
            "bool",
            True,
            group="rational",
        ),
        SettingField(
            "inflation_chance",
            "Degree inflation chance (%)",
            "range",
            15,
            min=0,
            max=100,
            group="rational",
        ),
        SettingField(
            "max_inflation_degree",
            "Max inflation factor degree",
            "int",
            2,
            min=1,
            max=4,
            group="rational",
        ),
        SettingField(
            "include_solution_details",
            "Include complete solution details in metadata",
            "bool",
            True,
            group="rational",
        ),
        SettingField(
            "force_lcd",
            "Force a full-LCD term in every problem",
            "bool",
            False,
            group="rational",
        ),
        SettingField(
            "allow_unlike_denominators",
            "Allow unlike denominators",
            "bool",
            True,
            group="rational",
        ),
        SettingField(
            "max_rational_terms",
            "Maximum rational terms",
            "int",
            5,
            min=2,
            max=500,
            group="rational",
        ),
    ]
