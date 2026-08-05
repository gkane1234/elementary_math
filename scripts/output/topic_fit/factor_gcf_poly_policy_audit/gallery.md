# Factor GCF (poly policy)

Polynomial-primitive audit for `polynomial_factoring_common_factor` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0]. Degree grows as min(policy.max_degree, 2 + floor(log2(1 + D/4))).

| D | Prompt | Answer | Degree | Upgrades |
|--:|--------|--------|--------|----------|
| 0 | $\text{Factor: } 2x + 2$ | $2\left(x + 1\right)$ | 1 | — |
| 0 | $\text{Factor: } 2 + 2x$ | $2\left(x + 1\right)$ | 1 | — |
| 0 | $\text{Factor: } 2 + 2x$ | $2\left(x + 1\right)$ | 1 | — |
| 3 | $\text{Factor: } 3 + 6x^{2} + 3x$ | $3\left(2x^{2} + x + 1\right)$ | 2 | three_terms |
| 3 | $\text{Factor: } 3 + 3x$ | $3\left(x + 1\right)$ | 1 | — |
| 3 | $\text{Factor: } 6x + 2x^{2} + 6$ | $2\left(x^{2} + 3x + 3\right)$ | 2 | signed_terms, three_terms |
| 6 | $\text{Factor: } 7x^{2} - 42x$ | $7x\left(x - 6\right)$ | 2 | signed_terms, three_terms, variable_gcf |
| 6 | $\text{Factor: } -9x + 9x^{2}$ | $3x\left(3x - 3\right)$ | 2 | signed_terms, three_terms, variable_gcf |
| 6 | $\text{Factor: } 2x + 2$ | $2\left(x + 1\right)$ | 1 | signed_terms |
| 10 | $\text{Factor: } 2x + 12x^{2}$ | $2x\left(6x + 1\right)$ | 2 | signed_terms, three_terms, variable_gcf |
| 10 | $\text{Factor: } 3x + 3$ | $3\left(x + 1\right)$ | 1 | — |
| 10 | $\text{Factor: } 3x + 3x^{2}$ | $3x\left(x + 1\right)$ | 2 | signed_terms, three_terms, variable_gcf |
| 14 | $\text{Factor: } 9x^{2}$ | $9x\left(x\right)$ | 2 | signed_terms, three_terms, variable_gcf |
| 14 | $\text{Factor: } 4x^{2} + 16x$ | $4x\left(x + 4\right)$ | 2 | signed_terms, three_terms, variable_gcf |
| 14 | $\text{Factor: } 5x + 15x^{2}$ | $5x\left(3x + 1\right)$ | 2 | signed_terms, three_terms, variable_gcf |
| 20 | $\text{Factor: } 70x + 70x^{2}$ | $10x\left(7x + 7\right)$ | 2 | signed_terms, three_terms, variable_gcf |
| 20 | $\text{Factor: } 24x + 15x^{2}$ | $3x\left(5x + 8\right)$ | 2 | signed_terms, three_terms, variable_gcf |
| 20 | $\text{Factor: } 18x + 30x^{2}$ | $6x\left(5x + 3\right)$ | 2 | signed_terms, three_terms, variable_gcf |
