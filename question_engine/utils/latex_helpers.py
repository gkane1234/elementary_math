from packages.polynomial_core import Polynomial, fraction_latex


def polynomial_fraction_latex(numerator: Polynomial, denominator: Polynomial) -> str:
    return fraction_latex(
        numerator.to_latex(),
        denominator.to_latex(),
    )


def long_division_answer_latex(
    quotient: Polynomial,
    remainder: Polynomial,
    divisor: Polynomial,
) -> str:
    if remainder.is_zero():
        return quotient.to_latex()
    return (
        f"{quotient.to_latex()}"
        f"+\\frac{{{remainder.to_latex()}}}{{{divisor.to_latex()}}}"
    )
