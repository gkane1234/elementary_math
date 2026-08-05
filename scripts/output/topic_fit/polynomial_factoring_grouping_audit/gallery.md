# Factoring by grouping

Polynomial-primitive audit for `polynomial_factoring_grouping` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0]. Degree grows as min(policy.max_degree, 2 + floor(log2(1 + D/4))).

| D | Prompt | Answer | Degree | Upgrades |
|--:|--------|--------|--------|----------|
| 0 | $\text{Factor: } 2x^{2} - 2$ | $\left(x - 1\right)\left(2x + 2\right)$ | 2 | grouping_quadratic, degree:2 |
| 0 | $\text{Factor: } x^{2} + 2x - 3$ | $\left(x - 1\right)\left(x + 3\right)$ | 2 | grouping_quadratic, degree:2 |
| 0 | $\text{Factor: } x^{2} - 3x + 2$ | $\left(x - 2\right)\left(x - 1\right)$ | 2 | grouping_quadratic, degree:2 |
| 3 | $\text{Factor: } x^{2} + 4x + 3$ | $\left(x + 1\right)\left(x + 3\right)$ | 2 | grouping_quadratic, degree:2 |
| 3 | $\text{Factor: } 3x^{2} + 4x - 4$ | $\left(x + 2\right)\left(3x - 2\right)$ | 2 | grouping_quadratic, degree:2 |
| 3 | $\text{Factor: } 3x^{2} + 9x + 6$ | $\left(x + 2\right)\left(3x + 3\right)$ | 2 | grouping_quadratic, degree:2 |
| 6 | $\text{Factor: } x^{2} + 5x + 6$ | $\left(x + 3\right)\left(x + 2\right)$ | 2 | grouping_quadratic, degree:2 |
| 6 | $\text{Factor: } x^{2} + 5x + 6$ | $\left(x + 3\right)\left(x + 2\right)$ | 2 | grouping_quadratic, degree:2 |
| 6 | $\text{Factor: } x^{3} + x^{2} - x - 1$ | $\left(x + 1\right)\left(x^{2} - 1\right)$ | 3 | grouping_cubic, degree:3 |
| 10 | $\text{Factor: } x^{2} + 4x + 4$ | $\left(x + 2\right)\left(x + 2\right)$ | 2 | grouping_quadratic, degree:2 |
| 10 | $\text{Factor: } 3x^{3} - 3x^{2} + x - 1$ | $\left(x - 1\right)\left(3x^{2} + 1\right)$ | 3 | grouping_cubic, degree:3 |
| 10 | $\text{Factor: } x^{3} + x^{2} + 3x + 3$ | $\left(x + 1\right)\left(x^{2} + 3\right)$ | 3 | grouping_cubic, degree:3 |
| 14 | $\text{Factor: } 3x^{3} + 6x^{2} + 2x + 4$ | $\left(x + 2\right)\left(3x^{2} + 2\right)$ | 3 | grouping_cubic, degree:3 |
| 14 | $\text{Factor: } 2x^{3} - 4x^{2} + 3x - 6$ | $\left(x - 2\right)\left(2x^{2} + 3\right)$ | 3 | grouping_cubic, degree:3 |
| 14 | $\text{Factor: } 2x^{3} + 10x^{2} - x - 5$ | $\left(x + 5\right)\left(2x^{2} - 1\right)$ | 3 | grouping_cubic, degree:3 |
| 20 | $\text{Factor: } x^{3} + 4x^{2} + x + 4$ | $\left(x + 4\right)\left(x^{2} + 1\right)$ | 3 | grouping_cubic, degree:3 |
| 20 | $\text{Factor: } x^{3} + 3x^{2} - 3x - 9$ | $\left(x + 3\right)\left(x^{2} - 3\right)$ | 3 | grouping_cubic, degree:3 |
| 20 | $\text{Factor: } 4x^{3} + 4x^{2} + 3x + 3$ | $\left(x + 1\right)\left(4x^{2} + 3\right)$ | 3 | grouping_cubic, degree:3 |
