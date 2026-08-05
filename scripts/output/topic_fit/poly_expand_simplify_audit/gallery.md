# Expand then simplify (poly / FOIL)

Polynomial-primitive audit for `poly_expand_simplify` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0]. Degree grows as min(policy.max_degree, 2 + floor(log2(1 + D/4))).

| D | Prompt | Answer | Degree | Upgrades |
|--:|--------|--------|--------|----------|
| 0 | $\text{Expand and simplify: } \left(-3x\right)\left(-3x + 1\right)$ | $9x^{2} - 3x$ | 2 | factors:2, degree:2, lone:0 |
| 0 | $\text{Expand and simplify: } \left(x + 1\right)\left(-x + 3\right)$ | $-x^{2} + 2x + 3$ | 2 | factors:2, degree:2, lone:0 |
| 0 | $\text{Expand and simplify: } \left(-3x - 3\right)\left(3x + 2\right)$ | $-9x^{2} - 15x - 6$ | 2 | factors:2, degree:2, lone:0 |
| 3 | $\text{Expand and simplify: } \left(3x + 1\right)\left(2x + 2\right)$ | $6x^{2} + 8x + 2$ | 2 | factors:2, degree:2, lone:0 |
| 3 | $\text{Expand and simplify: } \left(2x\right)\left(2x + 2\right)$ | $4x^{2} + 4x$ | 2 | factors:2, degree:2, lone:0 |
| 3 | $\text{Expand and simplify: } \left(2x + 3\right)\left(-2x + 2\right)$ | $-4x^{2} - 2x + 6$ | 2 | factors:2, degree:2, lone:0 |
| 6 | $\text{Expand and simplify: } \left(x + 2\right)\left(-x - 1\right) + 1$ | $-x^{2} - 3x - 1$ | 2 | factors:2, degree:2, lone:1 |
| 6 | $\text{Expand and simplify: } \left(x + 3\right)\left(-3x\right) + 4$ | $-3x^{2} - 9x + 4$ | 2 | factors:2, degree:2, lone:1 |
| 6 | $\text{Expand and simplify: } 2\left(-4x - 2\right)\left(-4x + 4\right)$ | $32x^{2} - 16x - 16$ | 2 | factors:2, degree:2, lone:0, scaled |
| 10 | $\text{Expand and simplify: } \left(4x\right)\left(-3x\right) - 3$ | $-12x^{2} - 3$ | 2 | factors:2, degree:2, lone:1 |
| 10 | $\text{Expand and simplify: } -2\left(-x + 2\right)\left(3x - 2\right) + 1$ | $6x^{2} - 16x + 9$ | 2 | factors:2, degree:2, lone:1, scaled |
| 10 | $\text{Expand and simplify: } 4\left(x\right)\left(2x + 3\right) + 1$ | $8x^{2} + 12x + 1$ | 2 | factors:2, degree:2, lone:1, scaled |
| 14 | $\text{Expand and simplify: } \left(x\right)\left(3x\right) + 1 - 3$ | $3x^{2} - 2$ | 2 | factors:2, degree:2, lone:2 |
| 14 | $\text{Expand and simplify: } \left(2x - 2\right)\left(-x - 1\right) + 1 + 2$ | $-2x^{2} + 5$ | 2 | factors:2, degree:2, lone:2 |
| 14 | $\text{Expand and simplify: } 2\left(-3x + 3\right)\left(-x + 3\right)\left(x\right) - 2$ | $6x^{3} - 24x^{2} + 18x - 2$ | 3 | factors:3, degree:3, lone:1, scaled |
| 20 | $\text{Expand and simplify: } \left(4x + 4\right)\left(5x - 6\right)\left(6x + 1\right) + 4 + 1$ | $120x^{3} - 4x^{2} - 148x - 19$ | 3 | factors:3, degree:3, lone:2 |
| 20 | $\text{Expand and simplify: } 4\left(2x + 2\right)\left(3x + 1\right)\left(-3x + 3\right) + 2 - 4$ | $-72x^{3} - 24x^{2} + 72x + 22$ | 3 | factors:3, degree:3, lone:2, scaled |
| 20 | $\text{Expand and simplify: } \left(3x + 2\right)\left(-x + 2\right) + 1 - 2$ | $-3x^{2} + 4x + 3$ | 2 | factors:2, degree:2, lone:2 |
