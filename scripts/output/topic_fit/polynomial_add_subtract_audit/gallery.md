# Add/subtract polynomials

Polynomial-primitive audit for `polynomial_add_subtract` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0]. Degree grows as min(policy.max_degree, 2 + floor(log2(1 + D/4))).

| D | Prompt | Answer | Degree | Upgrades |
|--:|--------|--------|--------|----------|
| 0 | $\text{Simplify: } \left(2x^{2} + x\right) - \left(2x^{2} + 3\right)$ | $x - 3$ | 2 | degree:2, op:-, terms:2 |
| 0 | $\text{Simplify: } \left(2x^{2} + 1\right) - \left(2x - 3\right)$ | $2x^{2} - 2x + 4$ | 2 | degree:2, op:-, terms:2 |
| 0 | $\text{Simplify: } \left(3x^{2} + 3\right) + \left(3x^{2} - 3\right)$ | $6x^{2}$ | 2 | degree:2, op:+, terms:2 |
| 3 | $\text{Simplify: } \left(2x^{2} + 2x\right) - \left(-x^{2} - 1\right)$ | $3x^{2} + 2x + 1$ | 2 | degree:2, op:-, terms:2 |
| 3 | $\text{Simplify: } \left(2x^{2} + 3\right) + \left(3x^{2} - x\right)$ | $5x^{2} - x + 3$ | 2 | degree:2, op:+, terms:2 |
| 3 | $\text{Simplify: } \left(3x^{2} + 2\right) + \left(2x^{2} + 3\right)$ | $5x^{2} + 5$ | 2 | degree:2, op:+, terms:2 |
| 6 | $\text{Simplify: } \left(2x^{2} + 3\right) + \left(2x + 2\right)$ | $2x^{2} + 2x + 5$ | 2 | degree:2, op:+, terms:2 |
| 6 | $\text{Simplify: } \left(2x^{2} + 3x\right) - \left(3x^{2} + 2x\right)$ | $-x^{2} + x$ | 2 | degree:2, op:-, terms:2 |
| 6 | $\text{Simplify: } \left(x^{2} + 2\right) + \left(3x^{2} - 1\right)$ | $4x^{2} + 1$ | 2 | degree:2, op:+, terms:2 |
| 10 | $\text{Simplify: } \left(4x^{2} + 4\right) - \left(3x^{2} + x\right)$ | $x^{2} - x + 4$ | 2 | degree:2, op:-, terms:2 |
| 10 | $\text{Simplify: } \left(2x^{3} + 2x^{2} + 1\right) + \left(x^{2} + 2\right)$ | $2x^{3} + 3x^{2} + 3$ | 3 | degree:3, op:+, terms:3 |
| 10 | $\text{Simplify: } \left(-4x^{3} + 4x^{2} + x\right) + \left(2x^{3} - 1\right)$ | $-2x^{3} + 4x^{2} + x - 1$ | 3 | degree:3, op:+, terms:3 |
| 14 | $\text{Simplify: } \left(2x^{3} - x^{2} + x - 2\right) + \left(x^{3} - 3x^{2} + 1\right)$ | $3x^{3} - 4x^{2} + x - 1$ | 3 | degree:3, op:+, terms:4 |
| 14 | $\text{Simplify: } \left(x^{3} + x^{2} - x\right) - \left(2x^{3} + 4\right)$ | $-x^{3} + x^{2} - x - 4$ | 3 | degree:3, op:-, terms:3 |
| 14 | $\text{Simplify: } \left(2x^{2} + 1\right) + \left(2x^{2} + 3\right)$ | $4x^{2} + 4$ | 2 | degree:2, op:+, terms:2 |
| 20 | $\text{Simplify: } \left(4x^{3} - x^{2} - x + 1\right) - \left(3x^{3} + 5x^{2} - 1\right)$ | $x^{3} - 6x^{2} - x + 2$ | 3 | degree:3, op:-, terms:4 |
| 20 | $\text{Simplify: } \left(-4x^{3} + 2x^{2} + 3x + 1\right) - \left(3x^{3} + 3x^{2} - 1\right)$ | $-7x^{3} - x^{2} + 3x + 2$ | 3 | degree:3, op:-, terms:4 |
| 20 | $\text{Simplify: } \left(x^{3} + 3x + 2\right) - \left(2x^{2} - 2\right)$ | $x^{3} - 2x^{2} + 3x + 4$ | 3 | degree:3, op:-, terms:3 |
