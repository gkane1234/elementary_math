#!/usr/bin/env python3
"""Print the complete solution set for a generated rational expression problem."""

from __future__ import annotations

import argparse
import json

import question_engine.types  # noqa: F401
from packages.polynomial_core import build_rational_expression_problem, sum_of_fractions_latex
from question_engine.factoring_settings import build_factorable_options


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--term-count", type=int, default=2)
    parser.add_argument("--denominator-degree-min", type=int, default=2)
    parser.add_argument("--denominator-degree-max", type=int, default=3)
    parser.add_argument("--coef-min", type=int, default=-6)
    parser.add_argument("--coef-max", type=int, default=6)
    parser.add_argument("--random-partial", action="store_true", default=True)
    parser.add_argument("--inflation-chance", type=int, default=15)
    parser.add_argument("--max-inflation-degree", type=int, default=2)
    parser.add_argument("--no-polynomial-terms", action="store_true")
    parser.add_argument("--no-full-lcd-terms", action="store_true")
    parser.add_argument("--cancel-factor-count", default="random")
    args = parser.parse_args()

    settings = {
        "coef_min": args.coef_min,
        "coef_max": args.coef_max,
        "positive_leading_coefficient": True,
        "leading_coefficient_one": False,
        "factor_rrt": False,
    }
    options = build_factorable_options(
        settings,
        args.denominator_degree_min,
        args.denominator_degree_max,
    )

    solution = build_rational_expression_problem(
        options,
        term_count=args.term_count,
        use_random_partial_solution=args.random_partial,
        allow_polynomial_terms=not args.no_polynomial_terms,
        allow_full_lcd_terms=not args.no_full_lcd_terms,
        inflation_chance=max(0.0, min(1.0, args.inflation_chance / 100.0)),
        max_inflation_degree=args.max_inflation_degree,
        cancel_factor_count=args.cancel_factor_count,
    )

    print("Problem:")
    print(sum_of_fractions_latex(list(solution.display_terms)))
    print()
    print("Complete solution set:")
    print(json.dumps(solution.to_dict(), indent=2, ensure_ascii=False))
    print()
    print("Simplified answer:")
    final_num = solution.final_numerator or solution.simplified_numerator
    final_den = solution.final_denominator or solution.simplified_denominator
    print(f"{final_num.to_latex()} / {final_den.to_latex()}")
    print(f"Cancelled LCD factors: {len(solution.cancelled_lcd_factors)}")


if __name__ == "__main__":
    main()
