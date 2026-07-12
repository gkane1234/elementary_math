from packages.polynomial_core import Polynomial, fraction_latex


def polynomial_fraction_latex(numerator: Polynomial, denominator: Polynomial) -> str:
    """Render a polynomial ratio as LaTeX (omit trivial ``/1`` denominators)."""
    if denominator is None or denominator.is_zero():
        return numerator.to_latex()
    if denominator.deg() == 0:
        lead = float(denominator.coef(0))
        if abs(lead - 1.0) < 1e-10:
            return numerator.to_latex()
        if abs(lead + 1.0) < 1e-10:
            return (numerator * -1).to_latex()
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
