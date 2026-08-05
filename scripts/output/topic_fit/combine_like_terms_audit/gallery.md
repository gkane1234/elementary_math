# Combine like terms audit

Open **[gallery.html](gallery.html)** in a browser for KaTeX-rendered math (markdown preview leaves `$...$` as raw LaTeX).

D buys more like terms, negatives, and (at high D) a second variable family.

## default

`{}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $3 + 2 + 3x + 3x$ | $6x + 5$ | — |
| 0 | $x + 2x + 2 + 3$ | $3x + 5$ | — |
| 0 | $3 + 3 + 3x + x$ | $4x + 6$ | — |
| 0 | $2 + 3x + 3 + 2x$ | $5x + 5$ | — |
| 2 | $2x + 1 + 2 + 3x$ | $5x + 3$ | — |
| 2 | $1 + 3x + 3x$ | $6x + 1$ | — |
| 2 | $x + x + 2 + 2$ | $2x + 4$ | — |
| 2 | $x + x + 2$ | $2x + 2$ | — |
| 4 | $3 + 2 + x + 2x$ | $3x + 5$ | negatives |
| 4 | $1 + x + 2 + 2x$ | $3x + 3$ | — |
| 4 | $x + 3 + 1 - 3x$ | $-2x + 4$ | negatives |
| 4 | $3x - 1 + x + 3$ | $4x + 2$ | negatives |
| 6 | $2x + 2 + x + 3x + 4$ | $6x + 6$ | more_like, negatives |
| 6 | $-2 + 3 - x + 2x + 3x$ | $4x + 1$ | more_like, negatives |
| 6 | $x + 3x + 2 + 3$ | $4x + 5$ | — |
| 6 | $6 + 4x + 4x - 5$ | $8x + 1$ | negatives |
| 8 | $-z - 3 + 1 + 2z$ | $z - 2$ | negatives |
| 8 | $y + 4 + 2 + 4y + 4y$ | $9y + 6$ | more_like, negatives |
| 8 | $3x + 2 - 2 + 4x + x$ | $8x$ | more_like, negatives |
| 8 | $2x - 2x - 1 + x + 2$ | $x + 1$ | more_like, negatives |
| 10 | $x + 1 + x - 3x + 2$ | $-x + 3$ | more_like, negatives |
| 10 | $2z - 3 - 3z + z - 1$ | $-4$ | more_like, negatives |
| 10 | $3y + 2 + y + 3 + 3y$ | $7y + 5$ | more_like, negatives |
| 10 | $4 - 3x + 3 + 2x - 2x$ | $-3x + 7$ | more_like, negatives |
| 12 | $x + x + 5 + 3 + 4x + 5 - 5x + x$ | $2x + 13$ | many_terms, more_like, negatives |
| 12 | $7 + 12x + 4x + 1$ | $16x + 8$ | — |
| 12 | $x + 1 + 3 + 2x$ | $3x + 4$ | — |
| 12 | $3z + 1 + z - 2z + 3$ | $2z + 4$ | more_like, negatives |
| 14 | $y + 2y + 4 + 2y + 1 + 4y + 4 + 4y$ | $13y + 9$ | many_terms, more_like, negatives |
| 14 | $2 + x - 1 - 3x$ | $-2x + 1$ | negatives |
| 14 | $1 + z + 3 + 3z + 2z + 3 + 2z + 3z$ | $11z + 7$ | many_terms, more_like, negatives |
| 14 | $4 + y + 3y + 2 + y$ | $5y + 6$ | more_like, negatives |

## integers_only

`{"integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $2 + 2x + 2x + 1$ | $4x + 3$ | — |
| 0 | $2 + x + x + 2$ | $2x + 4$ | — |
| 0 | $3 + 3x + 2 + 2x$ | $5x + 5$ | — |
| 0 | $2 + x + 3x + 3$ | $4x + 5$ | — |
| 2 | $3x + 1 + x$ | $4x + 1$ | — |
| 2 | $2x + 3 + x$ | $3x + 3$ | — |
| 2 | $1 + 3x + 3x + 2$ | $6x + 3$ | — |
| 2 | $2x + 1 + 2 + 3x$ | $5x + 3$ | — |
| 4 | $1 - x + 4 + x$ | $5$ | negatives |
| 4 | $-x + 1 + 3 - x$ | $-2x + 4$ | negatives |
| 4 | $-x + 2 + x + 3$ | $5$ | negatives |
| 4 | $-1 + 2x + x + 1$ | $3x$ | negatives |
| 6 | $3 - 4x + x + 2 + 3x$ | $5$ | more_like, negatives |
| 6 | $1 + 3x - 2 - x$ | $2x - 1$ | negatives |
| 6 | $-3x + 2x + 1 - 2 + x$ | $-1$ | more_like, negatives |
| 6 | $3x + x - 4x + 1 + 4$ | $5$ | more_like, negatives |
| 8 | $3 + z + 3 + 2z + 3z$ | $6z + 6$ | more_like, negatives |
| 8 | $-4x - 4 - 5x + 4$ | $-9x$ | negatives |
| 8 | $-z - 2z + 1 + 3 - z$ | $-4z + 4$ | more_like, negatives |
| 8 | $4x + 2x + 2 + 4 + x$ | $7x + 6$ | more_like, negatives |
| 10 | $4x + 5x - x + 2 + 2$ | $8x + 4$ | more_like, negatives |
| 10 | $2 - x - 2x + 2 + x$ | $-2x + 4$ | more_like, negatives |
| 10 | $5 - z + 5z + 5 + 3z$ | $7z + 10$ | more_like, negatives |
| 10 | $2y - 3y + y + 2 + 1$ | $3$ | more_like, negatives |
| 12 | $-10 - 9z - 3z + z + 6$ | $-11z - 4$ | more_like, negatives |
| 12 | $-x + 3x - 3x + 1 + 2$ | $-x + 3$ | more_like, negatives |
| 12 | $2x + 4x - 2x + 3 + 4$ | $4x + 7$ | more_like, negatives |
| 12 | $z + 4 + 8z + 3$ | $9z + 7$ | — |
| 14 | $2 - 5x + 5x + 1 + 3x$ | $3x + 3$ | more_like, negatives |
| 14 | $4z + 2z + 4 + 4 + 3 + 2z + 2z + z$ | $11z + 11$ | many_terms, more_like, negatives |
| 14 | $1 + 3y - 4y - 3 + y$ | $-2$ | more_like, negatives |
| 14 | $-3z + 3 - z + 4z + 1$ | $4$ | more_like, negatives |

## lock_x

`{"lock_variable": "x", "integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $3x + 3x + 2 + 2$ | $6x + 4$ | — |
| 0 | $3 + 2x + 3x + 1$ | $5x + 4$ | — |
| 0 | $2 + 3x + 2 + x$ | $4x + 4$ | — |
| 0 | $1 + x + 2 + x$ | $2x + 3$ | — |
| 2 | $2x + 2 + 2x$ | $4x + 2$ | — |
| 2 | $3x + 3x + 1$ | $6x + 1$ | — |
| 2 | $2x + 3x + 1$ | $5x + 1$ | — |
| 2 | $2 + x + 3 + 2x$ | $3x + 5$ | — |
| 4 | $-3x + 3 + x + 1$ | $-2x + 4$ | negatives |
| 4 | $2 + x + 1 + 3x$ | $4x + 3$ | — |
| 4 | $4x - 1 + x + 2$ | $5x + 1$ | negatives |
| 4 | $3 + 2 + x + x$ | $2x + 5$ | — |
| 6 | $3x - 1 - x + 2 + x$ | $3x + 1$ | more_like, negatives |
| 6 | $1 + 2x + 1 - x$ | $x + 2$ | negatives |
| 6 | $-1 + 2x + x + 3$ | $3x + 2$ | negatives |
| 6 | $5x + 4x - 2 + 1$ | $9x - 1$ | negatives |
| 8 | $4x + 5 + 2 + x$ | $5x + 7$ | — |
| 8 | $-1 + 3 + x + x - 2x$ | $2$ | more_like, negatives |
| 8 | $6x + 4 - 2 + 4x$ | $10x + 2$ | negatives |
| 8 | $2 + 1 + 3x + 2x + x$ | $6x + 3$ | more_like, negatives |
| 10 | $-8x - x + 4 + 4x + 8$ | $-5x + 12$ | more_like, negatives |
| 10 | $-x + 2 + 5x + 4 + 5x$ | $9x + 6$ | more_like, negatives |
| 10 | $x - 5 + 1 + 2x + 2x$ | $5x - 4$ | more_like, negatives |
| 10 | $2x + 5 + 4x - 3$ | $6x + 2$ | negatives |
| 12 | $-3x + 2x - x + x - x - 2 + 2 + 2$ | $-2x + 2$ | many_terms, more_like, negatives |
| 12 | $-6x + 5x + 6 + 1 + 6x$ | $5x + 7$ | more_like, negatives |
| 12 | $-x + x + 4x - 4 + 5$ | $4x + 1$ | more_like, negatives |
| 12 | $2x + 5 + 4 + 4x - x$ | $5x + 9$ | more_like, negatives |
| 14 | $2x - 1 + 2x - 1 - 3x$ | $x - 2$ | more_like, negatives |
| 14 | $6x - 2 - 3x + 1 - 2x$ | $x - 1$ | more_like, negatives |
| 14 | $2x + 3 + 2x + 4 + 3 + 4x - 2x + 5x$ | $11x + 10$ | many_terms, more_like, negatives |
| 14 | $1 - 2x - x - 1 + x + 2x + 4 + x$ | $x + 4$ | many_terms, more_like, negatives |
