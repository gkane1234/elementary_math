# Combine like terms (poly policy)

Polynomial-primitive audit for `poly_combine_like_terms` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0]. Degree grows as min(policy.max_degree, 2 + floor(log2(1 + D/4))).

| D | Prompt | Answer | Degree | Upgrades |
|--:|--------|--------|--------|----------|
| 0 | $\text{Simplify: } x + 3x^{2} + 3 + x + x^{2}$ | $4x^{2} + 2x + 3$ | 2 | degree:2 |
| 0 | $\text{Simplify: } 3x + 3 + x^{2} + x^{2} + 2x$ | $2x^{2} + 5x + 3$ | 2 | degree:2 |
| 0 | $\text{Simplify: } 2x + 3 + 2x + x^{2} + x^{2}$ | $2x^{2} + 4x + 3$ | 2 | degree:2 |
| 3 | $\text{Simplify: } x + 2x^{2} + 3x + 3x^{2} + 3$ | $5x^{2} + 4x + 3$ | 2 | degree:2 |
| 3 | $\text{Simplify: } x + 3x^{2} + 3x + 1 + x^{2} + 2x + x^{2}$ | $5x^{2} + 6x + 1$ | 2 | constants, degree:2, more_like |
| 3 | $\text{Simplify: } 2x^{2} + x + 2 + 3 + 2x + x^{2} + x + 2x^{2}$ | $5x^{2} + 4x + 5$ | 2 | constants, degree:2, more_like |
| 6 | $\text{Simplify: } 2x^{2} - 2x^{2} + x^{2} + 3 - x - x - 2x - 3$ | $x^{2} - 4x$ | 2 | constants, degree:2, more_like, negatives |
| 6 | $\text{Simplify: } 3x^{2} + 4 + 4x + x^{2} + 2x$ | $4x^{2} + 6x + 4$ | 2 | constants, degree:2 |
| 6 | $\text{Simplify: } -2x + 2x^{2} - x^{3} + 2x^{2} + 2x^{3} + 2x + 2x + 2x^{2} + 2x^{3} + 3 + 3x^{3} + 3x^{2} + 3 + 2x$ | $6x^{3} + 9x^{2} + 4x + 6$ | 3 | constants, degree:3, many_terms, more_like, negatives |
| 10 | $\text{Simplify: } 4x^{2} + 2 + x - 3x^{2} - 2x^{2} + x - 3 + x$ | $-x^{2} + 3x - 1$ | 2 | constants, degree:2, more_like, negatives |
| 10 | $\text{Simplify: } 1 + 1 - x + 2x + 2x^{3} + 2 + x + 3x^{2} - 2x^{2} + 2x^{2} + 3x^{3} - 2x^{3} - 3x^{2} + x + x^{3}$ | $4x^{3} + 3x + 4$ | 3 | constants, degree:3, many_terms, more_like, negatives, second_variable |
| 10 | $\text{Simplify: } 3x^{3} + 3x^{3} + 2x^{2} + 3x + 2x^{3} + 2x^{2} + 2 + 3x - x + 3x^{3} - 2x^{2} - 3x - 2x^{2}$ | $11x^{3} + 2x + 2$ | 3 | constants, degree:3, many_terms, more_like, negatives |
| 14 | $\text{Simplify: } 3x^{2} - 3x + 3x^{3} - x^{3} + x^{2} + 1 - 3 - 2x + 2x^{2} + x^{2} - x + x + 3x^{3} - 2x^{3}$ | $3x^{3} + 7x^{2} - 5x - 2$ | 3 | constants, degree:3, many_terms, more_like, negatives, second_variable |
| 14 | $\text{Simplify: } x^{2} + 3x + x^{2} + 3x + 6x + 2 + 5x^{2} + 2$ | $7x^{2} + 12x + 4$ | 2 | constants, degree:2, more_like, negatives |
| 14 | $\text{Simplify: } 2x^{2} - 2x^{3} - 3x^{3} + x - 1 + 3x + x^{2} + x^{2} + x^{2} - x^{3} - x + x^{3} + 2x$ | $-5x^{3} + 5x^{2} + 5x - 1$ | 3 | constants, degree:3, many_terms, more_like, negatives, second_variable |
| 20 | $\text{Simplify: } 3x^{2} + 2x^{2} + 4x^{2} - 5x + 5x - x + 2x - 3x^{3} + x^{3} + 5 + 2x^{3} + 2x^{3} - 3x^{2}$ | $2x^{3} + 6x^{2} + x + 5$ | 3 | constants, degree:3, many_terms, more_like, negatives, second_variable |
| 20 | $\text{Simplify: } 2x - 2x^{3} + 1 + x^{2} - x^{3} - 3 + 2x + 3x + x + x^{2} + 2x^{2} - x^{3} + 3x^{2} - x^{3}$ | $-5x^{3} + 7x^{2} + 8x - 2$ | 3 | constants, degree:3, many_terms, more_like, negatives, second_variable |
| 20 | $\text{Simplify: } 3x^{2} + 2x + 1 + 3 + 2x^{3} + x - 3x^{2} - 2x^{3} + x^{2} - 3x + 2 + x^{3} + x + 2x^{2} + 2x^{3}$ | $3x^{3} + 3x^{2} + x + 6$ | 3 | constants, degree:3, many_terms, more_like, negatives, second_variable |
