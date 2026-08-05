# Evaluate linear expressions audit

Open **[gallery.html](gallery.html)** in a browser for KaTeX-rendered math (markdown preview leaves `$...$` as raw LaTeX).

Affine (degree-1) expressions only. Term count grows as <code>n_terms = 1 + floor(log2(1 + D/1.5))</code> with no hard cap; parentheses via <code>n_parens = floor(log2(1 + D/3))</code> (budget often concentrated for deeper nesting); ×/÷-by-constant unlock with D. Numbers and the unknown come from Layer 0 lanes.

## default

`{}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $-3x + 2 \text{ when } x = 2$ | $-4$ | seed |
| 0 | $x \text{ when } x = 0$ | $0$ | seed |
| 0 | $x - 1 \text{ when } x = 0$ | $-1$ | seed |
| 0 | $2 + 3x \text{ when } x = 1$ | $5$ | seed |
| 1 | $-3x - 1 \text{ when } x = 3$ | $-10$ | seed |
| 1 | $3x \text{ when } x = 0$ | $0$ | seed |
| 1 | $2x \text{ when } x = -2$ | $-4$ | seed |
| 1 | $2x + 3 \text{ when } x = 1$ | $5$ | seed |
| 2 | $-3x + 2 \text{ when } x = 2$ | $-4$ | seed |
| 2 | $x + 1 \text{ when } x = 1$ | $2$ | seed |
| 2 | $1 + 2x \text{ when } x = 0$ | $1$ | seed |
| 2 | $3x + 1 \text{ when } x = 2$ | $7$ | seed |
| 3 | $2 + 3x \text{ when } x = 2$ | $8$ | seed |
| 3 | $1 - 2x \text{ when } x = -2$ | $5$ | seed |
| 3 | $-2 + x \text{ when } x = 1$ | $-1$ | seed |
| 3 | $-x + 1 \text{ when } x = 2$ | $-1$ | seed |
| 5 | $2x + 2 \text{ when } x = -2$ | $-2$ | seed |
| 5 | $3 + 3x \text{ when } x = -1$ | $0$ | seed |
| 5 | $-1 + 3x \text{ when } x = 2$ | $5$ | seed |
| 5 | $1 + 2x \text{ when } x = 0$ | $1$ | seed |
| 8 | $\left(y + 1\right)3 - 4 \text{ when } y = 3$ | $8$ | seed, distribute_split |
| 8 | $3\left(y - 2\right) - 5y + 9 \text{ when } y = 0$ | $3$ | seed, distribute_split |
| 8 | $\left(y + 2\right)\left(-2\right) + 5y + 7 \text{ when } y = 2$ | $9$ | seed, distribute_split |
| 8 | $-6x + 1 \text{ when } x = 0$ | $1$ | seed |
| 10 | $-3z + 5 + 2\left(z - 2\right) \text{ when } z = 2$ | $-1$ | seed, distribute_split |
| 10 | $2 - 4z \text{ when } z = -3$ | $14$ | seed |
| 10 | $5 + 4y \text{ when } y = 1$ | $9$ | seed |
| 10 | $\left(y - 1\right)\left(-3\right) + 4y - 2 \text{ when } y = 1$ | $2$ | seed, distribute_split |
| 14 | $6z + 1 - 2\left(z + 2\right) \text{ when } z = 1$ | $1$ | seed, distribute_split |
| 14 | $-3 + 3\left(y + 1\right) \text{ when } y = 1$ | $3$ | seed, distribute_split |
| 14 | $\left(y + 2\right)\left(-2\right) + 3y + 5 \text{ when } y = 1$ | $2$ | seed, distribute_split |
| 14 | $6\left(z - 2\right) - 4z + 12 \text{ when } z = \frac{1}{6}$ | $\frac{1}{3}$ | seed, distribute_split |
| 18 | $4 - 3x - 8 \text{ when } x = -3$ | $5$ | seed, distribute_split, split_const |
| 18 | $-5z + 3 + 4\left(z - 1\right) \text{ when } z = -1$ | $0$ | seed, distribute_split |
| 18 | $-3\left(-z - 1\right) - 3 \text{ when } z = 1$ | $3$ | seed, distribute_split |
| 18 | $-y + 11 + \left(y - 3\right) * 3 \text{ when } y = 0$ | $2$ | seed, distribute_split |
| 22 | $\left(-y + 1\right) * (-3) - 5y \text{ when } y = 4$ | $-11$ | seed, distribute_split |
| 22 | $\left(x + 1\right)3 - 8x + 2 \text{ when } x = \frac{1}{4}$ | $\frac{15}{4}$ | seed, distribute_split, distribute_split |
| 22 | $\left(x - 1\right)\left(-2\right) - 3x - 1 \text{ when } x = 1$ | $-4$ | seed, distribute_split |
| 22 | $\left(y - 1\right)2 - 5y + 3 \text{ when } y = -3$ | $10$ | seed, distribute_split |
| 24 | $3\left(x - 1\right) - 5x + 9 \text{ when } x = 0$ | $6$ | seed, distribute_split |
| 24 | $-y - 8 + \left(y + 3\right)3 \text{ when } y = 3$ | $7$ | seed, distribute_split, distribute_split |
| 24 | $2z - 5 + \left(-z - 1\right) * (-2) \text{ when } z = 2$ | $5$ | seed, distribute_split, distribute_split |
| 24 | $\left(2y + 2\right)\left(-3\right) + 7y + 9 \text{ when } y = 4$ | $7$ | seed, distribute_split, distribute_split |

## integers_only

`{"integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $3 - 3x \text{ when } x = 2$ | $-3$ | seed |
| 0 | $1 + 3x \text{ when } x = -2$ | $-5$ | seed |
| 0 | $2x - 3 \text{ when } x = 3$ | $3$ | seed |
| 0 | $3 + 3x \text{ when } x = 1$ | $6$ | seed |
| 1 | $-3x \text{ when } x = -2$ | $6$ | seed |
| 1 | $2x \text{ when } x = 3$ | $6$ | seed |
| 1 | $1 + x \text{ when } x = 2$ | $3$ | seed |
| 1 | $3 + x \text{ when } x = 2$ | $5$ | seed |
| 2 | $x + 3 \text{ when } x = 3$ | $6$ | seed |
| 2 | $x - 2 \text{ when } x = -3$ | $-5$ | seed |
| 2 | $x \text{ when } x = -2$ | $-2$ | seed |
| 2 | $3 + x \text{ when } x = 2$ | $5$ | seed |
| 3 | $3 + 2x \text{ when } x = -3$ | $-3$ | seed |
| 3 | $-3x - 2 \text{ when } x = 1$ | $-5$ | seed |
| 3 | $2 + 2x \text{ when } x = 3$ | $8$ | seed |
| 3 | $x + 1 \text{ when } x = 0$ | $1$ | seed |
| 5 | $2 + x \text{ when } x = 3$ | $5$ | seed |
| 5 | $5x - 4 - 3\left(x - 2\right) \text{ when } x = 3$ | $8$ | seed, distribute_split |
| 5 | $1 - 2x \text{ when } x = 1$ | $-1$ | seed |
| 5 | $\left(-x - 1\right)\left(-2\right) \text{ when } x = 1$ | $4$ | seed, distribute |
| 8 | $2\left(z + 2\right) - 5 \text{ when } z = 2$ | $3$ | seed, distribute_split |
| 8 | $3\left(y + 1\right) - y \text{ when } y = 0$ | $3$ | seed, distribute_split |
| 8 | $\left(z - 1\right)3 + 3 \text{ when } z = -2$ | $-6$ | seed, distribute_split |
| 8 | $4z + 2 \text{ when } z = -3$ | $-10$ | seed |
| 10 | $3\left(x - 2\right) + 8 \text{ when } x = 2$ | $8$ | seed, distribute_split |
| 10 | $y + 2 \text{ when } y = -1$ | $1$ | seed |
| 10 | $-1 + 3x \text{ when } x = 1$ | $2$ | seed |
| 10 | $\left(x + 2\right)3 - 4x - 4 \text{ when } x = 3$ | $-1$ | seed, distribute_split |
| 14 | $4 + 3x \text{ when } x = -6$ | $-14$ | seed |
| 14 | $x + 9 + \left(x - 3\right) * 3 \text{ when } x = 3$ | $12$ | seed, distribute_split |
| 14 | $\left(z + 1\right)2 \text{ when } z = -1$ | $0$ | seed, distribute |
| 14 | $4 + 4x \text{ when } x = 1$ | $8$ | seed |
| 18 | $2 * \left(2y + 3\right) - 2y - 5 \text{ when } y = 1$ | $3$ | seed, distribute_split, distribute_split |
| 18 | $2\left(-2x + 2\right) \text{ when } x = 4$ | $-12$ | seed, distribute |
| 18 | $2 + x \text{ when } x = 0$ | $2$ | seed |
| 18 | $2\left(x + 2\right) - 4 \text{ when } x = 0$ | $0$ | seed, distribute_split |
| 22 | $-x - 2 + \left(x - 1\right)3 \text{ when } x = -1$ | $-7$ | seed, distribute_split |
| 22 | $-6x - 7 + 3\left(x + 2\right) \text{ when } x = 4$ | $-13$ | seed, distribute_split |
| 22 | $7 + 4y \text{ when } y = 5$ | $27$ | seed |
| 22 | $\left(y + 2\right)4 - 7 \text{ when } y = 1$ | $5$ | seed, distribute_split, distribute_split |
| 24 | $-5\left(y - 2\right) + 4y - 4 \text{ when } y = -3$ | $9$ | seed, distribute_split, distribute_split |
| 24 | $12x + 2 \text{ when } x = -6$ | $-70$ | seed |
| 24 | $4y + 3 - 2 * \left(y + 2\right) \text{ when } y = -3$ | $-7$ | seed, distribute_split, distribute_split |
| 24 | $\left(-y + 1\right)2 + 3y \text{ when } y = 0$ | $2$ | seed, distribute_split, distribute_split |

## lock_x

`{"lock_variable": "x", "integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $x - 2 \text{ when } x = -2$ | $-4$ | seed |
| 0 | $-2x \text{ when } x = 0$ | $0$ | seed |
| 0 | $-3x + 1 \text{ when } x = 2$ | $-5$ | seed |
| 0 | $2x \text{ when } x = 3$ | $6$ | seed |
| 1 | $-2x + 3 \text{ when } x = 3$ | $-3$ | seed |
| 1 | $-x \text{ when } x = -3$ | $3$ | seed |
| 1 | $1 + x \text{ when } x = 1$ | $2$ | seed |
| 1 | $2x + 3 \text{ when } x = 2$ | $7$ | seed |
| 2 | $x - 3 \text{ when } x = 2$ | $-1$ | seed |
| 2 | $2x + 2 \text{ when } x = 3$ | $8$ | seed |
| 2 | $2x - 1 \text{ when } x = -1$ | $-3$ | seed |
| 2 | $-2x + 1 \text{ when } x = -3$ | $7$ | seed |
| 3 | $2 - 3x \text{ when } x = 1$ | $-1$ | seed |
| 3 | $2x + 1 \text{ when } x = 1$ | $3$ | seed |
| 3 | $3 + x \text{ when } x = -3$ | $0$ | seed |
| 3 | $-3 + 2x \text{ when } x = 0$ | $-3$ | seed |
| 5 | $-2x + 3 \text{ when } x = 0$ | $3$ | seed |
| 5 | $-3\left(x + 3\right) + 4x + 11 \text{ when } x = -1$ | $1$ | seed, distribute_split |
| 5 | $2 + 3x \text{ when } x = 1$ | $5$ | seed |
| 5 | $-x + 7 + \left(x - 2\right)3 \text{ when } x = -2$ | $-3$ | seed, distribute_split |
| 8 | $3x + 4 \text{ when } x = 2$ | $10$ | seed |
| 8 | $x + 2 \text{ when } x = 1$ | $3$ | seed |
| 8 | $1 + x \text{ when } x = 3$ | $4$ | seed |
| 8 | $x \text{ when } x = 0$ | $0$ | seed |
| 10 | $-5x - 8 + 2\left(x + 3\right) \text{ when } x = 3$ | $-11$ | seed, distribute_split |
| 10 | $-2\left(x + 1\right) + 5x + 4 \text{ when } x = 1$ | $5$ | seed, distribute_split |
| 10 | $-5x \text{ when } x = 7$ | $-35$ | seed |
| 10 | $2\left(x + 2\right) - x - 2 \text{ when } x = -1$ | $1$ | seed, distribute_split |
| 14 | $6 + \left(-x - 2\right)3 \text{ when } x = 2$ | $-6$ | seed, distribute_split |
| 14 | $2 * \left(2x + 3\right) - x - 4 \text{ when } x = 3$ | $11$ | seed, distribute_split |
| 14 | $-3 + \left(x + 1\right) * 3 \text{ when } x = -2$ | $-6$ | seed, distribute_split |
| 14 | $4x + 1 + \left(-x + 1\right)2 \text{ when } x = 1$ | $5$ | seed, distribute_split |
| 18 | $-x - 2 + \left(x + 1\right)2 \text{ when } x = 0$ | $0$ | seed, distribute_split |
| 18 | $3\left(x + 2\right) - 2x - 6 \text{ when } x = 1$ | $1$ | seed, distribute_split |
| 18 | $x + 7 + \left(x - 3\right)3 \text{ when } x = 0$ | $-2$ | seed, distribute_split |
| 18 | $\left(x + 1\right)3 - 3 \text{ when } x = -1$ | $-3$ | seed, distribute_split |
| 22 | $x + 6 + \left(-x - 2\right)3 \text{ when } x = 2$ | $-4$ | seed, distribute_split |
| 22 | $2 * \left(2x + 1\right) - 2 \text{ when } x = 1$ | $4$ | seed, distribute_split |
| 22 | $3\left(x + 3\right) - 4x - 6 \text{ when } x = 3$ | $0$ | seed, distribute_split |
| 22 | $-3 + 3x + 6 \text{ when } x = 2$ | $9$ | seed, distribute, split_const |
| 24 | $4x + 9 + 2\left(-x - 2\right) \text{ when } x = 2$ | $9$ | seed, distribute_split |
| 24 | $10 * \left(x + 1\right) - 8x - 5 \text{ when } x = 4$ | $13$ | seed, distribute_split |
| 24 | $4 + 6x \text{ when } x = 4$ | $28$ | seed |
| 24 | $7 + \left(x - 1\right)3 \text{ when } x = 3$ | $13$ | seed, distribute_split, distribute_split |
