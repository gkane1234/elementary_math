# Like terms (linear gate)

Linear control audit for `combining_like_terms` — must stay degree ≤ 1.

| D | Prompt | Answer | Degree | Upgrades |
|--:|--------|--------|--------|----------|
| 0 | $\text{Simplify: } x + 3x$ | $4x$ | — | — |
| 0 | $\text{Simplify: } 2 + 2x + 3x$ | $5x + 2$ | — | — |
| 0 | $\text{Simplify: } 3x + 2x + 1$ | $5x + 1$ | — | — |
| 3 | $\text{Simplify: } 2x + 2 + 2x + 3x$ | $7x + 2$ | — | constants, more_like |
| 3 | $\text{Simplify: } x + 2 + 3x + 3x$ | $7x + 2$ | — | more_like |
| 3 | $\text{Simplify: } 3 + x + x + x$ | $3x + 3$ | — | constants, more_like |
| 6 | $\text{Simplify: } 3x - 3 + 2 + x + 2x$ | $6x - 1$ | — | constants, more_like, negatives |
| 6 | $\text{Simplify: } 3 + 2x - 3x - x - 2x - 3x + 2$ | $-7x + 5$ | — | constants, many_terms, more_like, negatives |
| 6 | $\text{Simplify: } 2x + x - x + 2x + 2x + 3 + 2 + 2$ | $6x + 7$ | — | constants, many_terms, more_like, negatives |
| 10 | $\text{Simplify: } 3x + x + 3x + 3x + 3 + 3 + 1 - 2x$ | $8x + 7$ | — | constants, many_terms, more_like, negatives, second_variable |
| 10 | $\text{Simplify: } x - 2 + x - 2x + 2x + 3x + 1$ | $5x - 1$ | — | constants, many_terms, more_like, negatives |
| 10 | $\text{Simplify: } 3 + 2x - 1 + 3x - 2x - 2x + 2 + 3x$ | $4x + 4$ | — | constants, many_terms, more_like, negatives, second_variable |
| 14 | $\text{Simplify: } -3x - 2x - 1 + 4x + 5 - 1 + 4x + 4x$ | $7x + 3$ | — | constants, many_terms, more_like, negatives |
| 14 | $\text{Simplify: } 2x - 3 + 2x + 3x + 2x + 1 + 2 + x$ | $10x$ | — | constants, many_terms, more_like, negatives, second_variable |
| 14 | $\text{Simplify: } 2x - 2 + x - x + 3 + 2x - 2x$ | $2x + 1$ | — | constants, many_terms, more_like, negatives, second_variable |
| 20 | $\text{Simplify: } 2 + 4x - 5 + 4 + x - x + x - x$ | $4x + 1$ | — | constants, many_terms, more_like, negatives, second_variable |
| 20 | $\text{Simplify: } x + x - 2x + 3 + 3x + 3x$ | $6x + 3$ | — | constants, many_terms, more_like, negatives, second_variable |
| 20 | $\text{Simplify: } 2 - x + 2x + 3 + x + 2x - 2x$ | $2x + 5$ | — | constants, many_terms, more_like, negatives, second_variable |
