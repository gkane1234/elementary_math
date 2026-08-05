# Evaluate polynomials

Polynomial-primitive audit for `evaluate_polynomial` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0]. Degree grows as min(policy.max_degree, 2 + floor(log2(1 + D/4))).

| D | Prompt | Answer | Degree | Upgrades |
|--:|--------|--------|--------|----------|
| 0 | $\text{Evaluate } x^{2} + 1 \text{ when } x = 2$ | $5$ | 2 | terms:2, degree:2 |
| 0 | $\text{Evaluate } x^{2} + 1 \text{ when } x = 1$ | $2$ | 2 | terms:2, degree:2 |
| 0 | $\text{Evaluate } x^{2} + x \text{ when } x = 1$ | $2$ | 2 | terms:2, degree:2 |
| 3 | $\text{Evaluate } 2x^{2} + 2x \text{ when } x = 3$ | $24$ | 2 | terms:2, degree:2 |
| 3 | $\text{Evaluate } 3x^{2} + 4x \text{ when } x = 2$ | $20$ | 2 | terms:2, degree:2 |
| 3 | $\text{Evaluate } x^{2} + 1 \text{ when } x = 3$ | $10$ | 2 | terms:2, degree:2 |
| 6 | $\text{Evaluate } x^{2} + 3 \text{ when } x = -2$ | $7$ | 2 | terms:2, degree:2 |
| 6 | $\text{Evaluate } 3x^{3} - 3 \text{ when } x = 0$ | $-3$ | 3 | terms:2, degree:3 |
| 6 | $\text{Evaluate } 2x^{3} + x + 4 \text{ when } x = 3$ | $61$ | 3 | terms:3, degree:3 |
| 10 | $\text{Evaluate } 2x^{3} + x + 3 \text{ when } x = 0$ | $3$ | 3 | terms:3, degree:3 |
| 10 | $\text{Evaluate } x^{3} - x^{2} + 2x \text{ when } x = 2$ | $8$ | 3 | terms:3, degree:3 |
| 10 | $\text{Evaluate } -3x^{3} + x^{2} - 3 \text{ when } x = 2$ | $-23$ | 3 | terms:3, degree:3 |
| 14 | $\text{Evaluate } 3x^{2} + 6 \text{ when } x = 6$ | $114$ | 2 | terms:2, degree:2 |
| 14 | $\text{Evaluate } 3x^{3} + 3x^{2} - x + 1 \text{ when } x = -1$ | $2$ | 3 | terms:4, degree:3 |
| 14 | $\text{Evaluate } 5x^{3} - x + 4 \text{ when } x = 5$ | $624$ | 3 | terms:3, degree:3 |
| 20 | $\text{Evaluate } 2x^{3} - 2x^{2} + 3x + 3 \text{ when } x = -1$ | $-4$ | 3 | terms:4, degree:3 |
| 20 | $\text{Evaluate } x^{3} + 2x^{2} + 3x + 1 \text{ when } x = 0$ | $1$ | 3 | terms:4, degree:3 |
| 20 | $\text{Evaluate } 6x^{3} - 7x^{2} - 4x \text{ when } x = 2$ | $12$ | 3 | terms:3, degree:3 |
