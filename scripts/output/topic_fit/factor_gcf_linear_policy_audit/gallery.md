# Factor GCF (linear policy)

Primitive-linear audit for `factor_gcf` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0].

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $\text{Factor: } 2 + 2x$ | $2\left(x + 1\right)$ | — |
| 0 | $\text{Factor: } 6x + 3$ | $3\left(2x + 1\right)$ | — |
| 0 | $\text{Factor: } 2 + 4x$ | $2\left(2x + 1\right)$ | — |
| 3 | $\text{Factor: } 6x + 6 + 3$ | $3\left(2x + 2 + 1\right)$ | three_terms |
| 3 | $\text{Factor: } -3 - 3x$ | $3\left(-x - 1\right)$ | signed_terms |
| 3 | $\text{Factor: } 2x + 6 + 4$ | $2\left(x + 2 + 3\right)$ | three_terms |
| 6 | $\text{Factor: } 4 + 4x - 4$ | $4\left(x + 1 - 1\right)$ | signed_terms, three_terms |
| 6 | $\text{Factor: } 16x + 4 - 8$ | $4\left(4x - 2 + 1\right)$ | signed_terms, three_terms |
| 6 | $\text{Factor: } 10x - 20 - 15$ | $5\left(2x - 4 - 3\right)$ | signed_terms, three_terms |
| 10 | $\text{Factor: } -18x + 45 + 36$ | $9\left(-2x + 5 + 4\right)$ | signed_terms, three_terms |
| 10 | $\text{Factor: } 9 + 6x + 9$ | $3\left(2x + 3 + 3\right)$ | three_terms |
| 10 | $\text{Factor: } 12 - 12 - 18x$ | $6\left(-3x - 2 + 2\right)$ | signed_terms, three_terms |
| 14 | $\text{Factor: } 12 + 8 + 8x$ | $4\left(2x + 3 + 2\right)$ | signed_terms, three_terms |
| 14 | $\text{Factor: } -6 - 18x - 24$ | $6\left(-3x - 1 - 4\right)$ | signed_terms, three_terms |
| 14 | $\text{Factor: } -4 + 2x + 2$ | $2\left(x + 1 - 2\right)$ | signed_terms, three_terms |
| 20 | $\text{Factor: } 30 + 10 + 5x$ | $5\left(x + 6 + 2\right)$ | signed_terms, three_terms |
| 20 | $\text{Factor: } 10x + 35 + 15$ | $5\left(2x + 7 + 3\right)$ | signed_terms, three_terms |
| 20 | $\text{Factor: } -49x + 21 + 28$ | $7\left(-7x + 4 + 3\right)$ | signed_terms, three_terms |
