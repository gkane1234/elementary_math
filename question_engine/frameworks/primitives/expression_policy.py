"""Expression family / policy — hard constraints for linear vs polynomial leaves.

Difficulty ``D`` never raises ``max_degree`` on a linear leaf; degree is a
catalog/policy constant (or a poly-only setting).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Literal

ExpressionFamily = Literal["linear", "polynomial", "numeric"]


@dataclass(frozen=True)
class ExpressionPolicy:
    """Hard constraints threaded on every PrimitiveContext."""

    family: ExpressionFamily = "linear"
    max_degree: int = 1
    max_variables: int = 2
    allow_var_var_product: bool = False
    allow_abs: bool = False
    allow_higher_powers: bool = False  # x^n for n > max_degree

    def assert_degree(self, degree: int, *, where: str = "") -> None:
        if degree > self.max_degree:
            loc = f" ({where})" if where else ""
            raise ValueError(
                f"expression degree {degree} exceeds policy max_degree={self.max_degree}{loc}"
            )

    def allows_upgrade(self, upgrade_id: str) -> bool:
        """Gate structure upgrades that would raise degree under linear policy.

        ``three_terms`` is allowed on linear leaves — factor_gcf keeps it affine.
        ``variable_gcf`` always produces x^2 and is poly-only.
        """
        if upgrade_id == "variable_gcf" and self.max_degree <= 1:
            return False
        return True

    def as_dict(self) -> dict[str, Any]:
        return {
            "family": self.family,
            "max_degree": self.max_degree,
            "max_variables": self.max_variables,
            "allow_var_var_product": self.allow_var_var_product,
            "allow_abs": self.allow_abs,
            "allow_higher_powers": self.allow_higher_powers,
        }


LINEAR_POLICY = ExpressionPolicy(
    family="linear",
    max_degree=1,
    max_variables=2,
    allow_var_var_product=False,
    allow_abs=False,
    allow_higher_powers=False,
)

LINEAR_ABS_POLICY = ExpressionPolicy(
    family="linear",
    max_degree=1,
    max_variables=1,
    allow_var_var_product=False,
    allow_abs=True,
    allow_higher_powers=False,
)

SYSTEMS_POLICY = ExpressionPolicy(
    family="linear",
    max_degree=1,
    max_variables=2,
    allow_var_var_product=False,
    allow_abs=False,
    allow_higher_powers=False,
)

POLYNOMIAL_POLICY_DEFAULT = ExpressionPolicy(
    family="polynomial",
    max_degree=3,
    max_variables=2,
    allow_var_var_product=True,
    allow_abs=False,
    allow_higher_powers=True,
)

NUMERIC_POLICY = ExpressionPolicy(
    family="numeric",
    max_degree=0,
    max_variables=0,
    allow_var_var_product=False,
    allow_abs=False,
    allow_higher_powers=False,
)


def polynomial_policy(*, max_degree: int = 3, max_variables: int = 2) -> ExpressionPolicy:
    return ExpressionPolicy(
        family="polynomial",
        max_degree=max(1, int(max_degree)),
        max_variables=max(1, int(max_variables)),
        allow_var_var_product=True,
        allow_abs=False,
        allow_higher_powers=True,
    )


# Leaf / generator keys → default policy. Unlisted leaves that map to algebra
# primitives default to LINEAR_POLICY via build_context.
LEAF_POLICY: dict[str, ExpressionPolicy] = {
    # Explicit poly leaf that currently shares factor_gcf engine — keep poly able
    # to widen later; G6 / early factor leaves stay linear.
    "polynomial_factoring_common_factor": POLYNOMIAL_POLICY_DEFAULT,
    "polynomial_naming": POLYNOMIAL_POLICY_DEFAULT,
    "a2_polynomial_functions_naming": POLYNOMIAL_POLICY_DEFAULT,
    "polynomial_add_subtract": POLYNOMIAL_POLICY_DEFAULT,
    "pa_polynomials_adding_and_subtracting": POLYNOMIAL_POLICY_DEFAULT,
    "a2_polynomial_functions_adding_and_subtracting": POLYNOMIAL_POLICY_DEFAULT,
    "polynomial_multiply": POLYNOMIAL_POLICY_DEFAULT,
    "pa_polynomials_multiplying": POLYNOMIAL_POLICY_DEFAULT,
    "a2_polynomial_functions_multiplying": POLYNOMIAL_POLICY_DEFAULT,
    "polynomial_multiply_special": POLYNOMIAL_POLICY_DEFAULT,
    "a2_polynomial_functions_multiplying_special_cases": POLYNOMIAL_POLICY_DEFAULT,
    "evaluate_polynomial": POLYNOMIAL_POLICY_DEFAULT,
    "poly_combine_like_terms": POLYNOMIAL_POLICY_DEFAULT,
    "poly_expand_simplify": POLYNOMIAL_POLICY_DEFAULT,
    "quadratic_factoring": polynomial_policy(max_degree=2),
    "a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions": polynomial_policy(
        max_degree=2
    ),
    "a2_polynomial_functions_factoring_quadratic_form": polynomial_policy(max_degree=2),
    "polynomial_factoring_special_cases": POLYNOMIAL_POLICY_DEFAULT,
    "a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions": (
        polynomial_policy(max_degree=2)
    ),
    "a2_polynomial_functions_factoring_sum_difference_of_cubes": POLYNOMIAL_POLICY_DEFAULT,
    "polynomial_factoring_grouping": POLYNOMIAL_POLICY_DEFAULT,
    "a2_polynomial_functions_factoring_by_grouping": POLYNOMIAL_POLICY_DEFAULT,
    "a2_polynomial_functions_factoring_all_techniques": POLYNOMIAL_POLICY_DEFAULT,
    "rational_expression_simplification": POLYNOMIAL_POLICY_DEFAULT,
    "a2_rational_expressions_adding_and_subtracting": POLYNOMIAL_POLICY_DEFAULT,
    "rational_simplification": POLYNOMIAL_POLICY_DEFAULT,
    "a2_rational_expressions_simplifying": POLYNOMIAL_POLICY_DEFAULT,
    "partial_fraction_decomposition": POLYNOMIAL_POLICY_DEFAULT,
    "pc_partial_fraction_decomposition": POLYNOMIAL_POLICY_DEFAULT,
    "absolute_value_equations": LINEAR_ABS_POLICY,
    "a2_equations_and_inequalities_absolute_value_equations": LINEAR_ABS_POLICY,
    "absolute_value_inequalities": LINEAR_ABS_POLICY,
    "a2_equations_and_inequalities_absolute_value_inequalities": LINEAR_ABS_POLICY,
    "systems_elimination": SYSTEMS_POLICY,
    "systems_substitution": SYSTEMS_POLICY,
    "systems_graphing": SYSTEMS_POLICY,
    "graph_system": SYSTEMS_POLICY,
    "wp_systems": SYSTEMS_POLICY,
}


def resolve_policy(
    leaf_or_settings: str | dict[str, Any] | None = None,
    *,
    settings: dict[str, Any] | None = None,
    explicit: ExpressionPolicy | None = None,
) -> ExpressionPolicy:
    """Resolve policy from explicit arg, settings, or leaf id."""
    if explicit is not None:
        return explicit
    settings = settings or {}
    if isinstance(leaf_or_settings, dict):
        settings = {**leaf_or_settings, **settings}
        leaf_or_settings = None

    family = str(settings.get("expression_family") or "").strip().lower()
    if family == "polynomial":
        md = settings.get("max_degree", settings.get("poly_max_degree", 3))
        return polynomial_policy(max_degree=int(md))
    if family == "numeric":
        return NUMERIC_POLICY
    if family == "linear":
        return LINEAR_POLICY

    leaf = str(settings.get("leaf_id") or settings.get("generator") or leaf_or_settings or "")
    if leaf in LEAF_POLICY:
        return LEAF_POLICY[leaf]

    # Flat overrides for poly experiments without full leaf map.
    if "max_degree" in settings and int(settings["max_degree"]) > 1:
        return polynomial_policy(max_degree=int(settings["max_degree"]))

    return LINEAR_POLICY


_POWER_RE = re.compile(r"\^\{?(\d+)\}?|\*\*\s*(\d+)")


def max_power_in_latex(blob: str) -> int:
    """Best-effort max exponent appearing in latex/text (0 if none)."""
    if not blob:
        return 0
    degrees = [1]  # bare variable counts as deg 1 conceptually; callers check ^n
    for m in _POWER_RE.finditer(blob):
        n = m.group(1) or m.group(2)
        if n:
            degrees.append(int(n))
    # Also catch unicode / plain x^2 without braces already covered.
    return max(degrees) if len(degrees) > 1 else 0


def assert_linear_sample(latex: str, text: str = "", *, policy: ExpressionPolicy) -> None:
    """Audit helper: fail if sample exceeds policy degree / var×var product."""
    if policy.max_degree <= 1:
        for blob in (latex, text):
            if not blob:
                continue
            if "^{2}" in blob or "^2" in blob or "^{3}" in blob:
                raise AssertionError(f"degree > 1 under linear policy: {blob!r}")
            if re.search(r"([a-zA-Z])\s*[·*]\s*\1", blob):
                raise AssertionError(f"var×var product under linear policy: {blob!r}")
            p = max_power_in_latex(blob)
            if p > policy.max_degree:
                raise AssertionError(
                    f"power {p} > max_degree {policy.max_degree}: {blob!r}"
                )
