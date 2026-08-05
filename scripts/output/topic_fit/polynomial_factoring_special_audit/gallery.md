# Special product factoring

Polynomial-primitive audit for `polynomial_factoring_special_cases` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0]. Degree grows as min(policy.max_degree, 2 + floor(log2(1 + D/4))).

| D | Prompt | Answer | Degree | Upgrades |
|--:|--------|--------|--------|----------|
| 0 | $\text{Factor: } x^{2} - 2x + 1$ | $\left(x - 1\right)^{2}$ | 2 | perfect_square, degree:2, monic |
| 0 | $\text{Factor: } x^{2} - 9$ | $\left(x + 3\right)\left(x - 3\right)$ | 2 | difference_of_squares, degree:2, monic |
| 0 | $\text{Factor: } x^{2} - 1$ | $\left(x + 1\right)\left(x - 1\right)$ | 2 | difference_of_squares, degree:2, monic |
| 3 | $\text{Factor: } x^{2} - 4$ | $\left(x + 2\right)\left(x - 2\right)$ | 2 | difference_of_squares, degree:2, monic |
| 3 | $\text{Factor: } x^{2} - 9$ | $\left(x + 3\right)\left(x - 3\right)$ | 2 | difference_of_squares, degree:2, monic |
| 3 | $\text{Factor: } x^{2} + 2x + 1$ | $\left(x + 1\right)^{2}$ | 2 | perfect_square, degree:2, monic |
| 6 | $\text{Factor: } x^{2} + 2x + 1$ | $\left(x + 1\right)^{2}$ | 2 | perfect_square, degree:2, monic |
| 6 | $\text{Factor: } x^{2} - 1$ | $\left(x + 1\right)\left(x - 1\right)$ | 2 | difference_of_squares, degree:2, monic |
| 6 | $\text{Factor: } x^{2} + 2x + 1$ | $\left(x + 1\right)^{2}$ | 2 | perfect_square, degree:2, monic |
| 10 | $\text{Factor: } x^{2} - 1$ | $\left(x + 1\right)\left(x - 1\right)$ | 2 | difference_of_squares, degree:2, monic |
| 10 | $\text{Factor: } 4x^{2} - 9$ | $\left(2x + 3\right)\left(2x - 3\right)$ | 2 | difference_of_squares, degree:2, nonmonic |
| 10 | $\text{Factor: } 9x^{2} + 18x + 9$ | $\left(3x + 3\right)^{2}$ | 2 | perfect_square, degree:2, nonmonic |
| 14 | $\text{Factor: } 9x^{2} + 30x + 25$ | $\left(3x + 5\right)^{2}$ | 2 | perfect_square, degree:2, nonmonic |
| 14 | $\text{Factor: } x^{2} - 9$ | $\left(x + 3\right)\left(x - 3\right)$ | 2 | difference_of_squares, degree:2, monic |
| 14 | $\text{Factor: } x^{2} - 4x + 4$ | $\left(x - 2\right)^{2}$ | 2 | perfect_square, degree:2, monic |
| 20 | $\text{Factor: } 9x^{2} - 9$ | $\left(3x + 3\right)\left(3x - 3\right)$ | 2 | difference_of_squares, degree:2, nonmonic |
| 20 | $\text{Factor: } x^{2} + 2x + 1$ | $\left(x + 1\right)^{2}$ | 2 | perfect_square, degree:2, monic |
| 20 | $\text{Factor: } x^{2} - 6x + 9$ | $\left(x - 3\right)^{2}$ | 2 | perfect_square, degree:2, monic |
