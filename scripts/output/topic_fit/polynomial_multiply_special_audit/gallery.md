# Multiply special products

Polynomial-primitive audit for `polynomial_multiply_special` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0]. Degree grows as min(policy.max_degree, 2 + floor(log2(1 + D/4))).

| D | Prompt | Answer | Degree | Upgrades |
|--:|--------|--------|--------|----------|
| 0 | $\text{Multiply: } \left(x + 1\right)\left(x - 1\right)$ | $x^{2} - 1$ | 2 | degree:2, diff_squares, monic |
| 0 | $\text{Multiply: } \left(x + 2\right)^{2}$ | $x^{2} + 4x + 4$ | 2 | degree:2, square, monic |
| 0 | $\text{Multiply: } \left(x + 2\right)\left(x - 2\right)$ | $x^{2} - 4$ | 2 | degree:2, diff_squares, monic |
| 3 | $\text{Multiply: } \left(x + 2\right)^{2}$ | $x^{2} + 4x + 4$ | 2 | degree:2, square, monic |
| 3 | $\text{Multiply: } \left(x + 1\right)^{2}$ | $x^{2} + 2x + 1$ | 2 | degree:2, square, monic |
| 3 | $\text{Multiply: } \left(x + 1\right)\left(x - 1\right)$ | $x^{2} - 1$ | 2 | degree:2, diff_squares, monic |
| 6 | $\text{Multiply: } \left(x + 3\right)\left(x - 3\right)$ | $x^{2} - 9$ | 2 | degree:2, diff_squares, monic |
| 6 | $\text{Multiply: } \left(x + 2\right)\left(x - 2\right)$ | $x^{2} - 4$ | 2 | degree:2, diff_squares, monic |
| 6 | $\text{Multiply: } \left(x + 3\right)\left(x - 1\right)$ | $x^{2} + 2x - 3$ | 2 | degree:2, sum_diff, monic |
| 10 | $\text{Multiply: } \left(x + 1\right)\left(x + 2\right)$ | $x^{2} + 3x + 2$ | 2 | degree:2, sum_diff, monic |
| 10 | $\text{Multiply: } \left(x + 1\right)\left(x + 3\right)$ | $x^{2} + 4x + 3$ | 2 | degree:2, sum_diff, monic |
| 10 | $\text{Multiply: } \left(3x + 2\right)\left(3x - 3\right)$ | $9x^{2} - 3x - 6$ | 2 | degree:2, sum_diff, nonmonic |
| 14 | $\text{Multiply: } \left(x + 4\right)\left(x - 4\right)$ | $x^{2} - 16$ | 2 | degree:2, diff_squares, monic |
| 14 | $\text{Multiply: } \left(2x + 4\right)^{2}$ | $4x^{2} + 16x + 16$ | 2 | degree:2, square, nonmonic |
| 14 | $\text{Multiply: } \left(x + 1\right)\left(x - 1\right)$ | $x^{2} - 1$ | 2 | degree:2, diff_squares, monic |
| 20 | $\text{Multiply: } \left(x + 4\right)\left(x - 5\right)$ | $x^{2} - x - 20$ | 2 | degree:2, sum_diff, monic |
| 20 | $\text{Multiply: } \left(x + 1\right)\left(x - 1\right)$ | $x^{2} - 1$ | 2 | degree:2, diff_squares, monic |
| 20 | $\text{Multiply: } \left(3x + 1\right)\left(3x + 6\right)$ | $9x^{2} + 21x + 6$ | 2 | degree:2, sum_diff, nonmonic |
