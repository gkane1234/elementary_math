# Expand then simplify audit

Open **[gallery.html](gallery.html)** in a browser for KaTeX-rendered math (markdown preview leaves `$...$` as raw LaTeX).

Shared expression-structure engine (algebraic, prefer_distribute). Linear only: distribute then combine to <code>Ax+B</code>. Leaf/group count grows as <code>1 + floor(log2(1 + D/1.5))</code>; nesting via shared nest budget. Same structural DNA as OOO (numeric) and multi-step equation sides.

## default

`{}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $\left(x + 1\right)2 + x$ | $3x + 2$ | seed, distribute_split |
| 0 | $5 + 2\left(x - 2\right)$ | $2x + 1$ | seed, distribute_split |
| 0 | $\left(x - 2\right)3 - 5x + 5$ | $-2x - 1$ | seed, distribute_split |
| 0 | $2\left(x + 2\right) + x - 4$ | $3x$ | seed, distribute_split |
| 1 | $\left(x + 3\right)3 - 4x - 8$ | $-x + 1$ | seed, distribute_split |
| 1 | $4 + \left(x - 2\right)2$ | $2x$ | seed, distribute_split |
| 1 | $2\left(x + 2\right) + x - 5$ | $3x - 1$ | seed, distribute_split |
| 1 | $4 + 2\left(x - 2\right)$ | $2x$ | seed, distribute_split |
| 2 | $x - 1 + 2\left(x + 1\right)$ | $3x + 1$ | seed, distribute_split |
| 2 | $\left(x + 3\right)\left(-3\right) + 5x + 11$ | $2x + 2$ | seed, distribute_split |
| 2 | $3\left(x - 1\right) - 5x + 2$ | $-2x - 1$ | seed, distribute_split |
| 2 | $\left(x + 1\right)2 - x$ | $x + 2$ | seed, distribute_split |
| 3 | $2\left(x - 2\right) + 4$ | $2x$ | seed, distribute_split |
| 3 | $2\left(x - 3\right) + x + 8$ | $3x + 2$ | seed, distribute_split |
| 3 | $-3x - 4 + 2\left(x + 2\right)$ | $-x$ | seed, distribute_split |
| 3 | $3\left(x - 3\right) - x + 6$ | $2x - 3$ | seed, distribute_split |
| 5 | $\left(y - 1\right)2 + 2y + 3$ | $4y + 1$ | seed, distribute_split |
| 5 | $5x - 6 - 2\left(x - 2\right)$ | $3x - 2$ | seed, distribute_split |
| 5 | $x + 7 + \left(x - 2\right)2$ | $3x + 3$ | seed, distribute_split |
| 5 | $2\left(x - 1\right) - 4x + 5$ | $-2x + 3$ | seed, distribute_split |
| 8 | $\left(y + 1\right)3$ | $3y + 3$ | seed, distribute |
| 8 | $\left(x - 2\right)\left(-3\right) + 4x - 4$ | $x + 2$ | seed, distribute_split |
| 8 | $\left(x + 1\right)\left(-2\right) + 3x - 3$ | $x - 5$ | seed, distribute_split |
| 8 | $2\left(x + 1\right) - 2$ | $2x$ | seed, distribute_split |
| 10 | $3\left(x - 1\right) - 2x + 3$ | $x$ | seed, distribute_split |
| 10 | $-x + 6 + \left(x - 1\right)3$ | $2x + 3$ | seed, distribute_split |
| 10 | $10 + 3\left(y - 2\right)$ | $3y + 4$ | seed, distribute_split |
| 10 | $-6 - 3\left(-x - 2\right)$ | $3x$ | seed, distribute_split |
| 14 | $\left(x - 1\right)3 - x + 6$ | $2x + 3$ | seed, distribute_split |
| 14 | $-x - 15 + \left(x + 2\right)5$ | $4x - 5$ | seed, distribute_split |
| 14 | $\left(y - 3\right)\left(-2\right) + 3y - 3$ | $y + 3$ | seed, distribute_split |
| 14 | $\left(x - 2\right)\left(-3\right) + 5x - 9$ | $2x - 3$ | seed, distribute_split |
| 18 | $3\left(x + 1\right) - x - 3$ | $2x$ | seed, distribute_split |
| 18 | $\left(y + 3\right) * (-3) + 5y + 6$ | $2y - 3$ | seed, distribute_split |
| 18 | $-2c + 5 + 3\left(c - 1\right)$ | $c + 2$ | seed, distribute_split |
| 18 | $-8x + 20 + 9\left(x - 2\right)$ | $x + 2$ | seed, distribute_split |
| 22 | $3x + 4 - 2\left(x + 1\right)$ | $x + 2$ | seed, distribute_split |
| 22 | $-2\gamma + 8 + \left(\gamma - 2\right)5$ | $3\gamma - 2$ | seed, distribute_split |
| 22 | $3\left(2x + 3\right) - 4x - 6$ | $2x + 3$ | seed, distribute_split |
| 22 | $\left(-d - 1\right)3$ | $-3d - 3$ | seed, distribute |
| 24 | $\left(t + 1\right) * 2 - 2$ | $2t$ | seed, distribute_split |
| 24 | $-8b - 17 + 6\left(b + 3\right)$ | $-2b + 1$ | seed, distribute_split |
| 24 | $\left(k + 2\right) * 5 - 10k - 8$ | $-5k + 2$ | seed, distribute_split |
| 24 | $3\left(\delta - 1\right) - 2\delta + 4$ | $\delta + 1$ | seed, distribute_split |

## integers_only

`{"integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $-x - 1 + 2\left(x - 1\right)$ | $x - 3$ | seed, distribute_split |
| 0 | $\left(x - 2\right)\left(-3\right) + 6x - 5$ | $3x + 1$ | seed, distribute_split |
| 0 | $-3x - 1 + \left(x + 2\right)2$ | $-x + 3$ | seed, distribute_split |
| 0 | $\left(x + 3\right)2 - x - 7$ | $x - 1$ | seed, distribute_split |
| 1 | $3\left(x + 2\right) - 4x - 9$ | $-x - 3$ | seed, distribute_split |
| 1 | $-7 + \left(x + 2\right)3$ | $3x - 1$ | seed, distribute_split |
| 1 | $\left(x - 2\right)\left(-3\right) + 5x - 3$ | $2x + 3$ | seed, distribute_split |
| 1 | $\left(x + 3\right)2 - x - 5$ | $x + 1$ | seed, distribute_split |
| 2 | $-5x + 7 + 2\left(x - 2\right)$ | $-3x + 3$ | seed, distribute_split |
| 2 | $-3\left(x + 3\right) + 5x + 10$ | $2x + 1$ | seed, distribute_split |
| 2 | $6x - 11 + \left(x - 3\right)\left(-3\right)$ | $3x - 2$ | seed, distribute_split |
| 2 | $-4 + 2\left(x + 2\right)$ | $2x$ | seed, distribute_split |
| 3 | $x + 6 + \left(x - 2\right)2$ | $3x + 2$ | seed, distribute_split |
| 3 | $\left(-x - 1\right)\left(-3\right)$ | $3x + 3$ | seed, distribute |
| 3 | $\left(x - 2\right)\left(-2\right) + 3x - 5$ | $x - 1$ | seed, distribute_split |
| 3 | $3\left(x - 1\right) - 2x + 4$ | $x + 1$ | seed, distribute_split |
| 5 | $5x + 5 - 3\left(x + 1\right)$ | $2x + 2$ | seed, distribute_split |
| 5 | $-2\left(z - 2\right) + 3z - 4$ | $z$ | seed, distribute_split |
| 5 | $-1 + 2\left(x + 1\right)$ | $2x + 1$ | seed, distribute_split |
| 5 | $\left(x + 1\right)3$ | $3x + 3$ | seed, distribute |
| 8 | $2\left(-x + 1\right)$ | $-2x + 2$ | seed, distribute |
| 8 | $\left(x - 1\right)3 - x + 3$ | $2x$ | seed, distribute_split |
| 8 | $3\left(x + 3\right) - x - 6$ | $2x + 3$ | seed, distribute_split |
| 8 | $5x - 3 - 3\left(x - 1\right)$ | $2x$ | seed, distribute_split |
| 10 | $2y + 10 + \left(y + 3\right)\left(-3\right)$ | $-y + 1$ | seed, distribute_split |
| 10 | $\left(x - 2\right)\left(-3\right) + 4x - 3$ | $x + 3$ | seed, distribute_split |
| 10 | $-2\left(-2x - 2\right)$ | $4x + 4$ | seed, distribute |
| 10 | $3x + 6 + \left(x + 2\right)\left(-2\right)$ | $x + 2$ | seed, distribute_split |
| 14 | $\left(-z + 1\right) * (-3)$ | $3z - 3$ | seed, distribute |
| 14 | $2\left(y + 3\right) + 2y - 9$ | $4y - 3$ | seed, distribute_split |
| 14 | $\left(x + 1\right)2$ | $2x + 2$ | seed, distribute |
| 14 | $4\left(x + 3\right) - 7x - 15$ | $-3x - 3$ | seed, distribute_split |
| 18 | $-7m - 6 + \left(m + 2\right)3$ | $-4m$ | seed, distribute_split |
| 18 | $\left(m - 3\right)2 - 7m$ | $-5m - 6$ | seed, distribute_split |
| 18 | $\left(x + 1\right)3$ | $3x + 3$ | seed, distribute |
| 18 | $\left(x + 1\right)3$ | $3x + 3$ | seed, distribute |
| 22 | $\left(t - 2\right)\left(-8\right) + 16t - 14$ | $8t + 2$ | seed, distribute_split |
| 22 | $2\left(-z + 1\right)$ | $-2z + 2$ | seed, distribute, distribute |
| 22 | $\left(t + 3\right)4 - 3t - 9$ | $t + 3$ | seed, distribute_split |
| 22 | $2v - 4 + 3\left(v + 1\right)$ | $5v - 1$ | seed, distribute_split |
| 24 | $15t - 6 - 2\left(t + 1\right)$ | $13t - 8$ | seed, distribute_split |
| 24 | $t + 7 + 2\left(t - 3\right)$ | $3t + 1$ | seed, distribute_split, distribute_split |
| 24 | $8x + 10 - 4\left(x + 2\right)$ | $4x + 2$ | seed, distribute, distribute_split |
| 24 | $-3x + 19 + 5\left(x - 3\right)$ | $2x + 4$ | seed, distribute_split, distribute_split |

## lock_x

`{"lock_variable": "x", "integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $-2\left(x + 3\right) + 4x + 9$ | $2x + 3$ | seed, distribute_split |
| 0 | $\left(x - 3\right)\left(-3\right) + 5x - 7$ | $2x + 2$ | seed, distribute_split |
| 0 | $\left(-x + 1\right)\left(-3\right)$ | $3x - 3$ | seed, distribute |
| 0 | $\left(x - 1\right)\left(-2\right)$ | $-2x + 2$ | seed, distribute |
| 1 | $2\left(x - 1\right)$ | $2x - 2$ | seed, distribute |
| 1 | $2\left(-x - 1\right) + 2$ | $-2x$ | seed, distribute_split |
| 1 | $3x + 8 + \left(x + 3\right)\left(-2\right)$ | $x + 2$ | seed, distribute_split |
| 1 | $-5x + 5 + 2\left(x - 1\right)$ | $-3x + 3$ | seed, distribute_split |
| 2 | $-1 + 2\left(x + 1\right)$ | $2x + 1$ | seed, distribute_split |
| 2 | $-4x - 5 + \left(x + 2\right)2$ | $-2x - 1$ | seed, distribute_split |
| 2 | $\left(x + 1\right)\left(-2\right) + 3x + 1$ | $x - 1$ | seed, distribute_split |
| 2 | $3x - 2\left(x - 1\right)$ | $x + 2$ | seed, distribute_split |
| 3 | $\left(x + 1\right)\left(-2\right) + 4x - 1$ | $2x - 3$ | seed, distribute_split |
| 3 | $\left(x - 1\right)2 + x + 5$ | $3x + 3$ | seed, distribute_split |
| 3 | $2x + 3 - 3\left(x + 2\right)$ | $-x - 3$ | seed, distribute_split |
| 3 | $\left(x + 2\right)\left(-2\right) + 4x + 1$ | $2x - 3$ | seed, distribute_split |
| 5 | $3\left(x + 3\right) - x - 8$ | $2x + 1$ | seed, distribute_split |
| 5 | $-6x - 11 + \left(x + 2\right)4$ | $-2x - 3$ | seed, distribute_split |
| 5 | $3\left(-x + 1\right)$ | $-3x + 3$ | seed, distribute |
| 5 | $-7x - 16 + \left(x + 3\right)4$ | $-3x - 4$ | seed, distribute_split |
| 8 | $2\left(x - 3\right) - x + 9$ | $x + 3$ | seed, distribute_split |
| 8 | $3\left(x + 2\right) - 2x - 6$ | $x$ | seed, distribute_split |
| 8 | $7x + 7 + \left(x + 1\right)\left(-4\right)$ | $3x + 3$ | seed, distribute_split |
| 8 | $-2x + 7 + 4\left(x - 1\right)$ | $2x + 3$ | seed, distribute_split |
| 10 | $2\left(-x + 1\right)$ | $-2x + 2$ | seed, distribute |
| 10 | $-5 + \left(x + 1\right)3$ | $3x - 2$ | seed, distribute_split |
| 10 | $\left(x + 3\right)\left(-2\right) + 3x + 7$ | $x + 1$ | seed, distribute_split |
| 10 | $5x + 8 + \left(x + 3\right)\left(-2\right)$ | $3x + 2$ | seed, distribute_split |
| 14 | $9x - 2 + \left(x - 1\right)\left(-3\right)$ | $6x + 1$ | seed, distribute_split |
| 14 | $3\left(x + 1\right) - 4x$ | $-x + 3$ | seed, distribute_split |
| 14 | $3\left(-x + 1\right)$ | $-3x + 3$ | seed, distribute |
| 14 | $-3x - 1 + 5\left(x + 1\right)$ | $2x + 4$ | seed, distribute_split |
| 18 | $-3\left(x - 3\right) + 5x - 12$ | $2x - 3$ | seed, distribute_split |
| 18 | $5 * \left(x - 2\right) - 3x + 10$ | $2x$ | seed, distribute_split |
| 18 | $2 + \left(x - 1\right) * 2$ | $2x$ | seed, distribute_split |
| 18 | $\left(x + 3\right)3 - 8$ | $3x + 1$ | seed, distribute_split, distribute_split |
| 22 | $-4x + 10 + \left(x - 2\right)3$ | $-x + 4$ | seed, distribute_split |
| 22 | $\left(x + 3\right) * (-4) + 7x + 12$ | $3x$ | seed, distribute_split, distribute_split |
| 22 | $-x + 7 + 2\left(2x - 2\right)$ | $3x + 3$ | seed, distribute_split |
| 22 | $3\left(x - 2\right) - 2x + 2$ | $x - 4$ | seed, distribute_split |
| 24 | $x + 23 - 8\left(x + 2\right)$ | $-7x + 7$ | seed, distribute_split, distribute_split |
| 24 | $-3x - 7 + \left(x + 3\right) * 2$ | $-x - 1$ | seed, distribute_split, distribute_split |
| 24 | $-3\left(x + 3\right) + 10$ | $-3x + 1$ | seed, distribute_split, distribute_split |
| 24 | $5\left(x - 1\right)$ | $5x - 5$ | seed, distribute_split, distribute |
