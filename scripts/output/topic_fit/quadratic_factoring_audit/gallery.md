# Quadratic factoring

Polynomial-primitive audit for `quadratic_factoring` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0]. Degree grows as min(policy.max_degree, 2 + floor(log2(1 + D/4))).

| D | Prompt | Answer | Degree | Upgrades |
|--:|--------|--------|--------|----------|
| 0 | $\text{Factor: } x^{2} + 3x + 2$ | $\left(x + 1\right)\left(x + 2\right)$ | 2 | monic_trinomial, degree:2 |
| 0 | $\text{Factor: } x^{2} - x - 2$ | $\left(x + 1\right)\left(x - 2\right)$ | 2 | monic_trinomial, degree:2 |
| 0 | $\text{Factor: } x^{2} + 2x - 3$ | $\left(x + 3\right)\left(x - 1\right)$ | 2 | monic_trinomial, degree:2 |
| 3 | $\text{Factor: } x^{2} + 5x + 6$ | $\left(x + 3\right)\left(x + 2\right)$ | 2 | monic_trinomial, degree:2 |
| 3 | $\text{Factor: } x^{2} + 4x + 3$ | $\left(x + 3\right)\left(x + 1\right)$ | 2 | monic_trinomial, degree:2 |
| 3 | $\text{Factor: } x^{2} + 5x + 6$ | $\left(x + 2\right)\left(x + 3\right)$ | 2 | monic_trinomial, degree:2 |
| 6 | $\text{Factor: } x^{2} + 6x + 8$ | $\left(x + 4\right)\left(x + 2\right)$ | 2 | monic_trinomial, degree:2 |
| 6 | $\text{Factor: } x^{2} + 4x + 4$ | $\left(x + 2\right)\left(x + 2\right)$ | 2 | monic_trinomial, degree:2 |
| 6 | $\text{Factor: } x^{2} + 2x + 1$ | $\left(x + 1\right)\left(x + 1\right)$ | 2 | ac_method, degree:2 |
| 10 | $\text{Factor: } x^{2} + 3x - 10$ | $\left(x + 5\right)\left(x - 2\right)$ | 2 | monic_trinomial, degree:2 |
| 10 | $\text{Factor: } x^{2} + 6x + 9$ | $\left(x + 3\right)\left(x + 3\right)$ | 2 | monic_trinomial, degree:2 |
| 10 | $\text{Factor: } 3x^{2} - x - 4$ | $\left(3x - 4\right)\left(x + 1\right)$ | 2 | ac_method, degree:2 |
| 14 | $\text{Factor: } 2x^{2} - x - 3$ | $\left(x + 1\right)\left(2x - 3\right)$ | 2 | ac_method, degree:2 |
| 14 | $\text{Factor: } 18x^{2} - 45x + 27$ | $3\left(3x - 3\right)\left(2x - 3\right)$ | 2 | ac_method, degree:2, with_gcf |
| 14 | $\text{Factor: } 2x^{2} + 4x + 2$ | $\left(2x + 2\right)\left(x + 1\right)$ | 2 | ac_method, degree:2 |
| 20 | $\text{Factor: } x^{2} + x - 2$ | $\left(x - 1\right)\left(x + 2\right)$ | 2 | ac_method, degree:2 |
| 20 | $\text{Factor: } x^{2} + 2x - 3$ | $\left(x + 3\right)\left(x - 1\right)$ | 2 | monic_trinomial, degree:2 |
| 20 | $\text{Factor: } 3x^{2} - 6x + 3$ | $\left(3x - 3\right)\left(x - 1\right)$ | 2 | ac_method, degree:2 |
