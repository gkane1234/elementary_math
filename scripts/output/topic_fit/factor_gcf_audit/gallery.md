# Factor GCF / reverse distributive audit

Open **[gallery.html](gallery.html)** in a browser for KaTeX-rendered math (markdown preview leaves `$...$` as raw LaTeX).

Reverse of distributive: factor a numeric (or variable) GCF from a sum.

## default

`{}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $2 + 4x$ | $2\left(2x + 1\right)$ | — |
| 0 | $2x + 2$ | $2\left(x + 1\right)$ | — |
| 0 | $2 + 4x$ | $2\left(2x + 1\right)$ | — |
| 0 | $2x + 4$ | $2\left(x + 2\right)$ | — |
| 2 | $-2 + 2x$ | $2\left(x - 1\right)$ | signed_terms |
| 2 | $6x + 3$ | $3\left(2x + 1\right)$ | — |
| 2 | $2 + 4x + 2$ | $2\left(2x + 1 + 1\right)$ | three_terms |
| 2 | $3 + 3x$ | $3\left(x + 1\right)$ | signed_terms |
| 4 | $8 + 8x - 4$ | $4\left(2x - 1 + 2\right)$ | signed_terms, three_terms |
| 4 | $6x + 9 + 3$ | $3\left(2x + 3 + 1\right)$ | signed_terms, three_terms |
| 4 | $3 + 3x - 6$ | $3\left(x - 2 + 1\right)$ | signed_terms, three_terms |
| 4 | $-2x - 2 + 2$ | $2\left(-x + 1 - 1\right)$ | signed_terms, three_terms |
| 6 | $4y + 2$ | $2\left(2y + 1\right)$ | — |
| 6 | $9x + 6 + 9$ | $3\left(3x + 3 + 2\right)$ | signed_terms, three_terms |
| 6 | $4x + 4 - 2$ | $2\left(2x + 2 - 1\right)$ | signed_terms, three_terms |
| 6 | $-3 + 6x$ | $3\left(2x - 1\right)$ | signed_terms |
| 8 | $-6t - 3$ | $3\left(-2t - 1\right)$ | signed_terms |
| 8 | $2 + 4z + 4$ | $2\left(2z + 1 + 2\right)$ | three_terms |
| 8 | $-15x + 15 + 10$ | $5\left(-3x + 2 + 3\right)$ | signed_terms, three_terms |
| 8 | $2y + 2 + 2z$ | $2\left(y + z + 1\right)$ | signed_terms, three_terms |
| 10 | $6 + 30x + 6$ | $6\left(5x + 1 + 1\right)$ | signed_terms, three_terms |
| 10 | $-6t - 2b + 4$ | $2\left(-b - 3t + 2\right)$ | signed_terms, three_terms |
| 10 | $3 - 6z - 3x$ | $3\left(-2z - x + 1\right)$ | signed_terms, three_terms |
| 10 | $5 - 5 - 10x$ | $5\left(-2x - 1 + 1\right)$ | signed_terms, three_terms |
| 12 | $25y - 5z + 20$ | $5\left(-z + 5y + 4\right)$ | signed_terms, three_terms |
| 12 | $7v - 14 - 14t$ | $7\left(-2t + v - 2\right)$ | signed_terms, three_terms |
| 12 | $-3 + 9w + 9z$ | $3\left(3z + 3w - 1\right)$ | signed_terms, three_terms |
| 12 | $-20z + 5 + 10x$ | $5\left(2x - 4z + 1\right)$ | signed_terms, three_terms |
| 14 | $-24 + 24x + 12$ | $12\left(2x - 2 + 1\right)$ | signed_terms, three_terms |
| 14 | $40x - 24z + 8$ | $8\left(-3z + 5x + 1\right)$ | signed_terms, three_terms |
| 14 | $36x + 60 + 24$ | $12\left(3x + 5 + 2\right)$ | signed_terms, three_terms |
| 14 | $32 - 24y + 8x$ | $8\left(x - 3y + 4\right)$ | signed_terms, three_terms |

## integers_only

`{"integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $3 + 6x$ | $3\left(2x + 1\right)$ | — |
| 0 | $3x + 3$ | $3\left(x + 1\right)$ | — |
| 0 | $6x + 3$ | $3\left(2x + 1\right)$ | — |
| 0 | $2 + 2x$ | $2\left(x + 1\right)$ | — |
| 2 | $2 + 2x + 2$ | $2\left(x + 1 + 1\right)$ | three_terms |
| 2 | $3x + 3 + 3$ | $3\left(x + 1 + 1\right)$ | three_terms |
| 2 | $2x + 4$ | $2\left(x + 2\right)$ | — |
| 2 | $3 + 3x$ | $3\left(x + 1\right)$ | — |
| 4 | $4 + 4x + 2$ | $2\left(2x + 2 + 1\right)$ | three_terms |
| 4 | $-8 - 4x - 8$ | $4\left(-x - 2 - 2\right)$ | signed_terms, three_terms |
| 4 | $10 + 5x + 10$ | $5\left(x + 2 + 2\right)$ | signed_terms, three_terms |
| 4 | $2 + 2 + 2x$ | $2\left(x + 1 + 1\right)$ | three_terms |
| 6 | $-4x + 4 + 6$ | $2\left(-2x + 2 + 3\right)$ | signed_terms, three_terms |
| 6 | $16 - 16x + 4$ | $4\left(-4x + 4 + 1\right)$ | signed_terms, three_terms |
| 6 | $6 + 4 + 4x$ | $2\left(2x + 2 + 3\right)$ | signed_terms, three_terms |
| 6 | $24 + 24x - 18$ | $6\left(4x + 4 - 3\right)$ | signed_terms, three_terms |
| 8 | $12y - 8 + 12z$ | $4\left(3y + 3z - 2\right)$ | signed_terms, three_terms |
| 8 | $2 + 4x + 6z$ | $2\left(2x + 3z + 1\right)$ | three_terms |
| 8 | $20 + 16x + 4$ | $4\left(4x + 1 + 5\right)$ | signed_terms, three_terms |
| 8 | $3 + 3x + 3$ | $3\left(x + 1 + 1\right)$ | three_terms |
| 10 | $2 + 2x - 2y$ | $2\left(x - y + 1\right)$ | signed_terms, three_terms |
| 10 | $-10y + 10 - 15$ | $5\left(-2y - 3 + 2\right)$ | signed_terms, three_terms |
| 10 | $24 - 24x - 18$ | $6\left(-4x - 3 + 4\right)$ | signed_terms, three_terms |
| 10 | $8 + 40 + 32x$ | $8\left(4x + 5 + 1\right)$ | signed_terms, three_terms |
| 12 | $15 + 5 + 5y$ | $5\left(y + 1 + 3\right)$ | signed_terms, three_terms |
| 12 | $21y - 7 + 7$ | $7\left(3y - 1 + 1\right)$ | signed_terms, three_terms |
| 12 | $9 + 9x + 9$ | $9\left(x + 1 + 1\right)$ | signed_terms, three_terms |
| 12 | $6 + 10z - 2$ | $2\left(5z - 1 + 3\right)$ | signed_terms, three_terms |
| 14 | $11 - 33 - 22x$ | $11\left(-2x - 3 + 1\right)$ | signed_terms, three_terms |
| 14 | $-3x + 6y + 3$ | $3\left(-x + 2y + 1\right)$ | signed_terms, three_terms |
| 14 | $-6 + 6x + 36$ | $6\left(x - 1 + 6\right)$ | signed_terms, three_terms |
| 14 | $20y + 16 + 16z$ | $4\left(5y + 4z + 4\right)$ | signed_terms, three_terms |

## lock_x

`{"lock_variable": "x", "integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $3 + 3x$ | $3\left(x + 1\right)$ | — |
| 0 | $2x + 4$ | $2\left(x + 2\right)$ | — |
| 0 | $3x + 3$ | $3\left(x + 1\right)$ | — |
| 0 | $4 + 2x$ | $2\left(x + 2\right)$ | — |
| 2 | $3 + 3x$ | $3\left(x + 1\right)$ | — |
| 2 | $4x + 4 + 2$ | $2\left(2x + 2 + 1\right)$ | three_terms |
| 2 | $3 + 3x + 3$ | $3\left(x + 1 + 1\right)$ | three_terms |
| 2 | $-2 + 2x$ | $2\left(x - 1\right)$ | signed_terms |
| 4 | $6x + 3 + 9$ | $3\left(2x + 1 + 3\right)$ | signed_terms, three_terms |
| 4 | $2x - 4$ | $2\left(x - 2\right)$ | signed_terms |
| 4 | $-4 - 8 + 12x$ | $4\left(3x - 1 - 2\right)$ | signed_terms, three_terms |
| 4 | $6 + 4x + 6$ | $2\left(2x + 3 + 3\right)$ | signed_terms, three_terms |
| 6 | $3 + 6 + 3x$ | $3\left(x + 1 + 2\right)$ | three_terms |
| 6 | $9x + 3 - 3$ | $3\left(3x - 1 + 1\right)$ | signed_terms, three_terms |
| 6 | $-5 + 10x + 15$ | $5\left(2x + 3 - 1\right)$ | signed_terms, three_terms |
| 6 | $-8x + 4 + 12$ | $4\left(-2x + 3 + 1\right)$ | signed_terms, three_terms |
| 8 | $-9 - 12 + 12x$ | $3\left(4x - 4 - 3\right)$ | signed_terms, three_terms |
| 8 | $3x + 6 - 6$ | $3\left(x - 2 + 2\right)$ | signed_terms, three_terms |
| 8 | $-20 + 4x + 16$ | $4\left(x - 5 + 4\right)$ | signed_terms, three_terms |
| 8 | $18 + 18 + 24x$ | $6\left(4x + 3 + 3\right)$ | signed_terms, three_terms |
| 10 | $-7 + 21 + 28x$ | $7\left(4x - 1 + 3\right)$ | signed_terms, three_terms |
| 10 | $-15x + 5 - 15$ | $5\left(-3x + 1 - 3\right)$ | signed_terms, three_terms |
| 10 | $6 + 6 + 3x$ | $3\left(x + 2 + 2\right)$ | three_terms |
| 10 | $25 + 30 + 15x$ | $5\left(3x + 6 + 5\right)$ | signed_terms, three_terms |
| 12 | $9 + 6 + 6x$ | $3\left(2x + 2 + 3\right)$ | three_terms |
| 12 | $15 + 9x + 3$ | $3\left(3x + 1 + 5\right)$ | signed_terms, three_terms |
| 12 | $6 + 15 + 15x$ | $3\left(5x + 5 + 2\right)$ | signed_terms, three_terms |
| 12 | $6x + 3$ | $3\left(2x + 1\right)$ | — |
| 14 | $2x + 4 + 6$ | $2\left(x + 2 + 3\right)$ | three_terms |
| 14 | $-14 - 14x - 35$ | $7\left(-2x - 5 - 2\right)$ | signed_terms, three_terms |
| 14 | $-8x + 12 + 8$ | $4\left(-2x + 3 + 2\right)$ | signed_terms, three_terms |
| 14 | $-12 - 12x + 3$ | $3\left(-4x - 4 + 1\right)$ | signed_terms, three_terms |
