# Multiply polynomials

Polynomial-primitive audit for `polynomial_multiply` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0]. Degree grows as min(policy.max_degree, 2 + floor(log2(1 + D/4))).

| D | Prompt | Answer | Degree | Upgrades |
|--:|--------|--------|--------|----------|
| 0 | $\text{Multiply: } \left(-x\right)\left(x + 3\right)$ | $-x^{2} - 3x$ | 2 | degree:2, shape:1x2, distribute |
| 0 | $\text{Multiply: } \left(3x + 1\right)\left(3x\right)$ | $9x^{2} + 3x$ | 2 | degree:2, shape:2x1, distribute |
| 0 | $\text{Multiply: } \left(-3x\right)\left(x + 3\right)$ | $-3x^{2} - 9x$ | 2 | degree:2, shape:1x2, distribute |
| 3 | $\text{Multiply: } \left(-x^{2} + 1\right)\left(-x\right)$ | $x^{3} - x$ | 3 | degree:3, shape:2x1, distribute |
| 3 | $\text{Multiply: } \left(3x + 2\right)\left(x + 1\right)$ | $3x^{2} + 5x + 2$ | 2 | degree:2, shape:2x2, foil |
| 3 | $\text{Multiply: } \left(-2x\right)\left(3x - 2\right)$ | $-6x^{2} + 4x$ | 2 | degree:2, shape:1x2, distribute |
| 6 | $\text{Multiply: } \left(x - 3\right)\left(2x + 1\right)$ | $2x^{2} - 5x - 3$ | 2 | degree:2, shape:2x2, foil |
| 6 | $\text{Multiply: } \left(3x + 2\right)\left(x - 2\right)$ | $3x^{2} - 4x - 4$ | 2 | degree:2, shape:2x2, foil |
| 6 | $\text{Multiply: } \left(x + 1\right)\left(-3x + 1\right)$ | $-3x^{2} - 2x + 1$ | 2 | degree:2, shape:2x2, foil |
| 10 | $\text{Multiply: } \left(x^{2}\right)\left(-x - 1\right)$ | $-x^{3} - x^{2}$ | 3 | degree:3, shape:1x2, distribute |
| 10 | $\text{Multiply: } \left(-3x + 3\right)\left(x + 3\right)$ | $-3x^{2} - 6x + 9$ | 2 | degree:2, shape:2x2, foil |
| 10 | $\text{Multiply: } \left(-x^{2}\right)\left(2x + 1\right)$ | $-2x^{3} - x^{2}$ | 3 | degree:3, shape:1x3, distribute |
| 14 | $\text{Multiply: } \left(2x^{2} + x + 3\right)\left(2x\right)$ | $4x^{3} + 2x^{2} + 6x$ | 3 | degree:3, shape:3x1, distribute |
| 14 | $\text{Multiply: } \left(x^{2}\right)\left(2x + 2\right)$ | $2x^{3} + 2x^{2}$ | 3 | degree:3, shape:1x3, distribute |
| 14 | $\text{Multiply: } \left(2x + 2\right)\left(-x + 3\right)$ | $-2x^{2} + 4x + 6$ | 2 | degree:2, shape:2x2, foil |
| 20 | $\text{Multiply: } \left(x^{2} + x + 2\right)\left(-2x\right)$ | $-2x^{3} - 2x^{2} - 4x$ | 3 | degree:3, shape:3x1, distribute |
| 20 | $\text{Multiply: } \left(4x^{2}\right)\left(3x + 4\right)$ | $12x^{3} + 16x^{2}$ | 3 | degree:3, shape:1x3, distribute |
| 20 | $\text{Multiply: } \left(x + 4\right)\left(-x + 1\right)$ | $-x^{2} - 3x + 4$ | 2 | degree:2, shape:2x2, foil |
