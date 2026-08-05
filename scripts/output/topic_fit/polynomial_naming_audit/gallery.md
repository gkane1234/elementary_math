# Polynomial naming / classify

Polynomial-primitive audit for `polynomial_naming` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0]. Degree grows as min(policy.max_degree, 2 + floor(log2(1 + D/4))).

| D | Prompt | Answer | Degree | Upgrades |
|--:|--------|--------|--------|----------|
| 0 | $\text{Name the polynomial: } 2x^{2} + 1$ | $\text{quadratic}$ | 2 | degree:2, terms:2 |
| 0 | $\text{Name the polynomial: } 2x^{2} - 1$ | $\text{quadratic}$ | 2 | degree:2, terms:2 |
| 0 | $\text{Name the polynomial: } -3x^{2} + 2$ | $\text{quadratic}$ | 2 | degree:2, terms:2 |
| 3 | $\text{Name the polynomial: } x^{2} - 2$ | $\text{quadratic}$ | 2 | degree:2, terms:2 |
| 3 | $\text{Name the polynomial: } 3x^{2} + 2$ | $\text{quadratic}$ | 2 | degree:2, terms:2 |
| 3 | $\text{Name the polynomial: } x^{2} - 1$ | $\text{quadratic}$ | 2 | degree:2, terms:2 |
| 6 | $\text{Name the polynomial: } 2x^{3} + 3x^{2} - x$ | $\text{cubic}$ | 3 | degree:3, terms:3 |
| 6 | $\text{Name the polynomial: } x^{2} + 2$ | $\text{quadratic}$ | 2 | degree:2, terms:2 |
| 6 | $\text{Name the polynomial: } 2x^{3} - x + 2$ | $\text{cubic}$ | 3 | degree:3, terms:3 |
| 10 | $\text{Name the polynomial: } x^{3} - x - 3$ | $\text{cubic}$ | 3 | degree:3, terms:3 |
| 10 | $\text{Name the polynomial: } x^{3} + x^{2} + 1$ | $\text{cubic}$ | 3 | degree:3, terms:3 |
| 10 | $\text{Name the polynomial: } x^{3} + x - 2$ | $\text{cubic}$ | 3 | degree:3, terms:3 |
| 14 | $\text{Name the polynomial: } 3x^{3} - 3x^{2} + 2x + 1$ | $\text{cubic}$ | 3 | degree:3, terms:4, leading_meta |
| 14 | $\text{Name the polynomial: } 3x^{2} + 2$ | $\text{quadratic}$ | 2 | degree:2, terms:2 |
| 14 | $\text{Name the polynomial: } x^{3} + x^{2} + x + 1$ | $\text{cubic}$ | 3 | degree:3, terms:4, leading_meta |
| 20 | $\text{Name the polynomial: } 4x^{3} + 5x^{2} - 4x + 4$ | $\text{cubic}$ | 3 | degree:3, terms:4, leading_meta |
| 20 | $\text{Name the polynomial: } 3x^{3} + x^{2} + x + 2$ | $\text{cubic}$ | 3 | degree:3, terms:4 |
| 20 | $\text{Name the polynomial: } 3x^{3} - 3x^{2} - 3x + 1$ | $\text{cubic}$ | 3 | degree:3, terms:4, leading_meta |
