# polynomial_core

Symbolic polynomial and rational-expression library used by the question engine.

## Package layout

| Module | Purpose |
|--------|---------|
| `polynomial.py` | `Polynomial` class — arithmetic, degree, evaluation, division |
| `latex.py` | Centralized LaTeX formatting |
| `factoring.py` | Factorable polynomial factories and metadata |
| `rational.py` | Rational expression problem builders |
| `operations.py` | GCD, LCM, content helpers |

## Quick start

```python
from packages.polynomial_core import (
    Polynomial,
    create_factorable_polynomial,
    FactorablePolynomialOptions,
    build_rational_expression_problem,
    random_polynomial,
    from_roots,
)

# Arithmetic and display
p = Polynomial([1, -3, 2])          # x^2 - 3x + 2
print(p.to_latex())                  # LaTeX
print(p.evaluate(2))                 # 0

# From roots: (x - 1)(x - 2)
q = from_roots([1, 2])
assert q == p

# Random polynomial for worksheets
r = random_polynomial(degree=3, coef_min=-6, coef_max=6)

# Factoring with metadata
options = FactorablePolynomialOptions(coef_min=-8, coef_max=8, target_degree_min=2, target_degree_max=2)
result = create_factorable_polynomial(options)
print(result.polynomial)               # expanded form
print(result.factors)                  # known factorization
print(result.method)                   # e.g. "difference_of_squares"

# Rational expression (sum of fractions → single fraction)
solution = build_rational_expression_problem(options, term_count=3)
print(solution.final_numerator.to_latex(), "/", solution.final_denominator.to_latex())
```

## Polynomial API

### Construction

| Method | Description |
|--------|-------------|
| `Polynomial([a, b, c])` | Coefficients high-degree first |
| `Polynomial.from_coefficients([...])` | Same as list constructor |
| `Polynomial.from_roots([r1, r2, ...])` | Build from zeros |
| `Polynomial.random_polynomial(deg, min, max)` | Random integer coefficients |

### Properties & accessors

| Name | Description |
|------|-------------|
| `p.deg()` / `p.degree` | Degree |
| `p.leading_coefficient()` | Leading coefficient |
| `p.coef_list()` | Coefficients high-degree first |
| `p.evaluate(x)` | Value at *x* |

### Operations

| Method | Description |
|--------|-------------|
| `p + q`, `p * q`, `p - q` | Arithmetic |
| `p.poly_div(q)` / `p.divide(q)` | Long division → `(quotient, remainder)` |
| `p.gcd(q)` / `p.gcf(q)` | Polynomial GCD |
| `p.lcm(q)` | Polynomial LCM |
| `p.content_gcd()` | GCD of integer coefficients |

### Display

| Method | Description |
|--------|-------------|
| `p.to_latex()` | LaTeX |
| `str(p)` / `p.to_text()` | Plain text |

## Factoring API

```python
from packages.polynomial_core import (
    FactorablePolynomialOptions,
    create_factorable_polynomial,
)

options = FactorablePolynomialOptions(
    coef_min=-10,
    coef_max=10,
    target_degree_min=2,
    target_degree_max=4,
    rrt_mode="exclude",                  # "allow" | "exclude" | "only"
)
result = create_factorable_polynomial(options)
# result.polynomial, result.factors, result.method
```

Supported `method` values: `normal`, `grouping`, `substitution`, `difference_of_squares`, `perfect_square_trinomial`, `difference_of_cubes`, `sum_of_cubes`, `rrt`.

## Special products (factoring practice)

```python
from packages.polynomial_core import create_special_product_problem

result = create_special_product_problem({
    "factor_difference_of_squares": True,
    "factor_perfect_square_trinomial": True,
    "factor_sum_of_cubes": True,
    "factor_difference_of_cubes": True,
    "allow_higher_even_powers": True,  # Hard: x^4-1, x^8-1, ...
    "max_even_power": 8,
})
print(result.polynomial.to_latex())  # expanded prompt, e.g. x^{8}-1
print(result.answer_latex())         # (x-1)(x+1)(x^{2}+1)(x^{4}+1)
print(result.pattern)
```

## Rational expressions

```python
from packages.polynomial_core import (
    build_rational_expression_problem,
    sum_of_fractions_latex,
    polynomial_excluded_values,
    rational_excluded_values_latex,
)

solution = build_rational_expression_problem(options, term_count=3)
prompt = sum_of_fractions_latex(list(solution.display_terms))

excluded = polynomial_excluded_values(solution.final_denominator, coef_min=-20, coef_max=20)
note = rational_excluded_values_latex(excluded)   # "x \neq 2, -1"
```
