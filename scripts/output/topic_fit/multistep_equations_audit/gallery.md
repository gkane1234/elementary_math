# Multi-step equations audit

Open **[gallery.html](gallery.html)** in a browser for KaTeX-rendered math (markdown preview leaves `$...$` as raw LaTeX).

Composes shared expand/simplify expressions on each side (<code>LHS = RHS</code>). Op count grows as <code>n_ops = 3 + floor(log2(1 + D/2))</code>; expression structure (groups / nesting) scales with the same D via <code>sample_linear_expression_to_simplify</code>.

## default

`{"integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $-4x - 3 + 3\left(x + 1\right) = 7x - 9 - 3\left(x + 2\right)$ | $x = 3$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 0 | $2\left(x + 3\right) - 4x - 3 = -3\left(x - 2\right)$ | $x = 3$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 0 | $4x - 5 + \left(x - 2\right)\left(-3\right) = \left(2x - 1\right)2$ | $x = 1$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 0 | $4x - 2 - 3\left(x - 1\right) = -8x + 13 + 3\left(x - 2\right)$ | $x = 1$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 1 | $-4x + 11 + \left(x - 3\right)3 = -7x - 7 + \left(x + 2\right)3$ | $x = -1$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 1 | $2\left(-x - 1\right) = -2\left(3x - 5\right)$ | $x = 3$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 1 | $3\left(x + 2\right) - 6 = 2\left(2x - 1\right)$ | $x = 2$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 1 | $-2\left(x + 2\right) + 3x + 4 = -2\left(x + 3\right) + 6x + 9$ | $x = -1$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 2 | $\left(-x + 1\right)\left(-2\right) + 2 = 8x - 30$ | $x = 5$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 2 | $\left(x + 2\right)3 - 6x - 5 = \left(x - 3\right)3 - 11x + 25$ | $x = 3$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 2 | $-4x - 4 + 3\left(x + 2\right) = -4x + 13 + 2\left(x - 3\right)$ | $x = 5$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 2 | $2\left(x - 3\right) - 5x + 3 = 2\left(x + 3\right) - x - 5$ | $x = -1$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 4 | $-2x - 6 + 3\left(x + 3\right) = 5x - 31 + 2\left(x + 2\right)$ | $x = 5$ | compose_simplify, ops:5, chunks:1, groups:1, both_sides, right_chunks:1 |
| 4 | $\frac{1}{2}x + \frac{3}{4} = \frac{1}{3}x + \frac{7}{4}$ | $x = 6$ | clear_fractions, both_sides, ops:5 |
| 4 | $2\left(x - 2\right) + 4 = 3\left(x - 1\right) + x + 1$ | $x = 1$ | compose_simplify, ops:5, chunks:1, groups:1, both_sides, right_chunks:1 |
| 4 | $3\left(x - 2\right) - 2x + 7 = -2\left(-2x + 7\right)$ | $x = 5$ | compose_simplify, ops:5, chunks:1, groups:1, both_sides, right_chunks:1 |
| 6 | $\left(x - 3\right)3 - 2x + 11 = \left(x + 2\right)2 + x - 6$ | $x = 2$ | compose_simplify, ops:6, chunks:1, groups:1, both_sides, right_chunks:1 |
| 6 | $\left(x - 1\right)\left(-3\right) + 4x - 1 = \left(x + 3\right)2 - 4x - 1$ | $x = 1$ | compose_simplify, ops:6, chunks:1, groups:1, both_sides, right_chunks:1 |
| 6 | $-y - 1 + \left(y + 1\right)3 = \left(2y - 8\right)2$ | $y = 9$ | compose_simplify, ops:6, chunks:1, groups:1, both_sides, right_chunks:1 |
| 6 | $-1 + 2\left(z + 2\right) = 6z - 7 - 2\left(z - 3\right)$ | $z = 2$ | compose_simplify, ops:6, chunks:1, groups:1, both_sides, right_chunks:1 |
| 8 | $\left(x - 2\right)4 - 2x + 6 = \left(-2x - 1\right)\left(-2\right)$ | $x = -2$ | compose_simplify, ops:7, chunks:1, groups:1, both_sides, right_chunks:1 |
| 8 | $3x - 7 - 2 * \left(x - 3\right) = x - 4 + 3 * \left(x + 2\right)$ | $x = -1$ | compose_simplify, ops:7, chunks:1, groups:1, both_sides, right_chunks:1 |
| 8 | $-2\left(x - 2\right) - 5 = -2\left(x + 2\right) - 2x + 15$ | $x = 6$ | compose_simplify, ops:7, chunks:1, groups:1, both_sides, right_chunks:1 |
| 8 | $-2\left(x - 1\right) = 2\left(x - 2\right) - 9x + 11$ | $x = 1$ | compose_simplify, ops:7, chunks:1, groups:1, both_sides, right_chunks:1 |
| 10 | $3\left(x + 3\right) - 2x - 9 = 3\left(-x - 3\right) + 5x + 7$ | $x = 2$ | compose_simplify, ops:8, chunks:1, groups:1, both_sides, right_chunks:1 |
| 10 | $\left(y + 2\right)2 + y - 1 = \left(3y - 1\right)3$ | $y = 1$ | compose_simplify, ops:8, chunks:1, groups:1, both_sides, right_chunks:1 |
| 10 | $3x + 1 + 2\left(-x - 1\right) = -2x - 37 - 3\left(x - 2\right)$ | $x = -5$ | compose_simplify, ops:8, chunks:1, groups:1, both_sides, right_chunks:1 |
| 10 | $4z + 4 - 3\left(z + 1\right) = 3z - 55 + 4\left(z + 2\right)$ | $z = 8$ | compose_simplify, ops:8, chunks:1, groups:1, both_sides, right_chunks:1 |
| 14 | $\left(x + 1\right) * (-3) + \left(-x - 2 + \left(x + 2\right) * 3\right) = \left(-x + 2\right) * 2 + \left(2x + 4 + \left(x + 3\right) * 3\right)$ | $x = -4$ | compose_simplify, ops:10, chunks:2, groups:2, both_sides, right_chunks:2 |
| 14 | $\left(x + 2\right) * 3 - x - 5 + \left(\left(x + 2\right) * 2 - 3x - 4\right) = \left(x + 3\right) * 2 + 3x - 3 + \left(\left(-x - 1\right) * 3\right)$ | $x = 1$ | compose_simplify, ops:10, chunks:2, groups:2, both_sides, right_chunks:2 |
| 14 | $4z - 2 - 3\left(z - 2\right) + \left(1 + 2\left(z - 1\right)\right) = -4z - 5 + 3\left(z + 2\right) + \left(4z - 43 + 3\left(z + 3\right)\right)$ | $z = 12$ | compose_simplify, ops:10, chunks:2, groups:2, both_sides, right_chunks:2 |
| 14 | $-4x - 3 + 2\left(x + 3\right) + \left(x - 11 + 3\left(x + 2\right)\right) = 13x - 39 - 3\left(x - 3\right) + \left(-x - 3 - 2\left(x - 3\right)\right)$ | $x = 5$ | compose_simplify, ops:10, chunks:2, groups:2, both_sides, right_chunks:2 |
| 18 | $5x - 8 - 2\left(x - 3\right) + \left(-8x - 1 + 2\left(x + 3\right)\right) = -10x - 23 + 2\left(2x + 1\right) + \left(-x - 2 - 2\left(x - 1\right)\right)$ | $x = -4$ | compose_simplify, ops:12, chunks:2, groups:2, both_sides, right_chunks:2 |
| 18 | $-2 * \left(x - 2\right) + 5x + \left(3 * \left(x - 2\right) - 4x + 3\right) = 2 * \left(x + 3\right) - 49 + \left(-3 * \left(x + 2\right) + 6x + 2\right)$ | $x = 16$ | compose_simplify, ops:12, chunks:2, groups:2, both_sides, right_chunks:2 |
| 18 | $-2 * \left(z - 2\right) - 2z - 5 + \left(2 * \left(z - 1\right) + z + 2\right) = 4 * \left(-z + 2\right) + z + 4 + \left(3 * \left(-z - 1\right)\right)$ | $z = 2$ | compose_simplify, ops:12, chunks:2, groups:2, both_sides, right_chunks:2 |
| 18 | $-2\left(z - 2\right) + z - 5 + \left(3\left(z + 3\right) - 5\right) = 2\left(2z + 2\right) - z - 1 + \left(-7z + 84\right)$ | $z = 14$ | compose_simplify, ops:12, chunks:2, groups:2, both_sides, right_chunks:2 |
| 22 | $-3 * \left(h + 2\right) + 5h + 5 + \left(3 * \left(h - 2\right) - 6h + 10\right) + \left(-4 * \left(-h - 2\right) - 2h - 10\right) = -2 * \left(h - 1\right) + 3h - 1 + \left(2 * \left(h + 1\right)\right) + \left(4 * \left(h - 2\right) - h - 69\right)$ | $h = 15$ | compose_simplify, ops:14, chunks:3, groups:3, both_sides, right_chunks:3 |
| 22 | $-12x + 23 + \left(x - 3\right)4 + \left(-4x - 13 + \left(2x + 3\right)3\right) + \left(-x + 4 + \left(x - 1\right)3\right) = x - 96 + \left(-10x + 6 + \left(x - 1\right)8\right) + \left(-x - 10 + \left(x + 2\right)4\right)$ | $x = 18$ | compose_simplify, ops:14, chunks:3, groups:3, both_sides, right_chunks:3 |
| 22 | $3\left(\psi + 2\right) - 11\psi - 4 + \left(-2\left(\psi + 3\right) + 5\psi + 5\right) + \left(2\left(-\psi + 3\right) + 5\psi - 4\right) = -3\left(\psi + 3\right) - 37 + \left(3\left(2\psi - 2\right) - 8\psi + 6\right) + \left(-3\left(2\psi + 3\right) + 5\psi + 10\right)$ | $\psi = -12$ | compose_simplify, ops:14, chunks:3, groups:3, both_sides, right_chunks:3 |
| 22 | $-2\left(2x + 1\right) + 6x + 1 + \left(3\left(x + 1\right) - 4x - 5\right) + \left(2\left(-x - 2\right) - 3x + 6\right) = 2\left(x + 3\right) - 7 + \left(-3\left(x - 3\right) + 5x - 9\right) + \left(2\left(-x + 3\right)\right)$ | $x = -1$ | compose_simplify, ops:14, chunks:3, groups:3, both_sides, right_chunks:3 |
| 24 | $\left(x + 3\right) * 7 - 4x - 23 + \left(\left(x + 3\right) * 3 - 7\right) + \left(\left(x - 3\right) * 7 - 14x + 32\right) = \left(x - 2\right) * (-2) + 3x - 6 + \left(\left(x - 3\right) * (-3) + x + 28\right) + \left(\left(x + 1\right) * (-3)\right)$ | $x = 7$ | compose_simplify, ops:15, chunks:3, groups:3, both_sides, right_chunks:3 |
| 24 | $\left(a - 3\right) * 3 + 8 + \left(\left(2a + 2\right) * 3 - 5a - 8\right) + \left(\left(-a - 2\right) * 4 + 4a + 11\right) = \left(a - 3\right) * 3 - 4a + 9 + \left(\left(-a + 2\right) * 4 + 7a - 4\right) + \left(\left(-3a + 10\right) * (-2)\right)$ | $a = 4$ | compose_simplify, ops:15, chunks:3, groups:3, both_sides, right_chunks:3 |
| 24 | $-4m - 14 + 6 * \left(m + 2\right) + \left(-5m - 19 + 8 * \left(m + 2\right)\right) + \left(-15m - 12 + 6 * \left(m + 2\right)\right) = m - 7 - 2 * \left(2m - 2\right) + \left(m - 8 + 3 * \left(-m + 2\right)\right) + \left(-2m + 24 - 3 * \left(m + 2\right)\right)$ | $m = 3$ | compose_simplify, ops:15, chunks:3, groups:3, both_sides, right_chunks:3 |
| 24 | $-5f + 7 + \left(f - 3\right)3 + \left(\left(f + 1\right)2\right) + \left(3f - 8 + \left(-f + 3\right)2\right) = 5f + 6 + \left(f + 2\right)\left(-3\right) + \left(\left(f - 1\right)3\right) + \left(-17 + \left(f + 3\right)2\right)$ | $f = 2$ | compose_simplify, ops:15, chunks:3, groups:3, both_sides, right_chunks:3 |

## lock_x

`{"integers_only": true, "lock_variable": "x"}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $\left(x - 1\right)\left(-3\right) + 5x - 1 = \left(x + 1\right)\left(-3\right) + 8x + 5$ | $x = 0$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 0 | $6x + 10 - 3\left(x + 3\right) = 5x - 5 + 3\left(x + 2\right)$ | $x = 0$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 0 | $6x - 7 - 3\left(x - 3\right) = 6x - 1 + 3\left(x + 3\right)$ | $x = -1$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 0 | $\left(x + 2\right)2 + x - 7 = \left(x + 1\right)3 - x - 3$ | $x = 3$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 1 | $-2x + 3\left(x - 1\right) = 7x - 7 - 2\left(x + 2\right)$ | $x = 2$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 1 | $-2\left(x - 2\right) - x - 4 = -2\left(x - 3\right) + x + 2$ | $x = -4$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 1 | $-2x + 3 + 3\left(x - 1\right) = 3x - 22 + 2\left(x + 3\right)$ | $x = 4$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 1 | $4x - 1 - 2\left(x - 1\right) = 10x + 5 - 2\left(x + 2\right)$ | $x = 0$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 2 | $2\left(-x - 1\right) + 2 = -2\left(x + 1\right) - x - 3$ | $x = -5$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 2 | $\left(x - 1\right)2 + x - 1 = \left(x - 2\right)2 - x + 9$ | $x = 4$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 2 | $3x - 7 + \left(x - 3\right)\left(-2\right) = 9x - 20 + \left(x + 2\right)\left(-3\right)$ | $x = 5$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 2 | $-2\left(x + 1\right) + 5x + 3 = 2\left(x - 2\right)$ | $x = -5$ | compose_simplify, ops:4, chunks:1, groups:1, both_sides, right_chunks:1 |
| 4 | $3\left(x - 2\right) - x + 7 = 3\left(x - 1\right) + 4x - 26$ | $x = 6$ | compose_simplify, ops:5, chunks:1, groups:1, both_sides, right_chunks:1 |
| 4 | $2\left(x - 3\right) + 9 = 2\left(x - 2\right) + 2x + 9$ | $x = -1$ | compose_simplify, ops:5, chunks:1, groups:1, both_sides, right_chunks:1 |
| 4 | $3\left(x - 3\right) - 2x + 6 = 3\left(x + 2\right) - 7x + 16$ | $x = 5$ | compose_simplify, ops:5, chunks:1, groups:1, both_sides, right_chunks:1 |
| 4 | $-\frac{3}{2}x + \frac{7}{5} = 2x - \frac{28}{5}$ | $x = 2$ | clear_fractions, both_sides, ops:5 |
| 6 | $3 - 3\left(-x + 1\right) = -5x + 2 + 3\left(x + 1\right)$ | $x = 1$ | compose_simplify, ops:6, chunks:1, groups:1, both_sides, right_chunks:1 |
| 6 | $-\frac{5}{4}x - \frac{2}{5} = \frac{5}{3}x - \frac{356}{15}$ | $x = 8$ | clear_fractions, both_sides, ops:6 |
| 6 | $3\left(x - 1\right) = -3\left(-3x + 3\right)$ | $x = 1$ | compose_simplify, ops:6, chunks:1, groups:1, both_sides, right_chunks:1 |
| 6 | $2\left(x - 1\right) = 4\left(x + 1\right) + 2x + 30$ | $x = -9$ | compose_simplify, ops:6, chunks:1, groups:1, both_sides, right_chunks:1 |
| 8 | $2\left(x - 2\right) + x + 6 = 2\left(x + 2\right) - 5x + 28$ | $x = 5$ | compose_simplify, ops:7, chunks:1, groups:1, both_sides, right_chunks:1 |
| 8 | $2 + 2\left(2x - 1\right) = 4x - 24 + 3\left(x - 3\right)$ | $x = 11$ | compose_simplify, ops:7, chunks:1, groups:1, both_sides, right_chunks:1 |
| 8 | $\left(2x + 2\right)\left(-3\right) + 12x + 8 = \left(x + 3\right)\left(-5\right) + 16x - 33$ | $x = 10$ | compose_simplify, ops:7, chunks:1, groups:1, both_sides, right_chunks:1 |
| 8 | $3\left(-x + 1\right) = -3\left(x - 1\right) + 4x$ | $x = 0$ | compose_simplify, ops:7, chunks:1, groups:1, both_sides, right_chunks:1 |
| 10 | $\left(-x + 1\right) * 3 = \left(x - 2\right) * 2 - 7x + 27$ | $x = 10$ | compose_simplify, ops:8, chunks:1, groups:1, both_sides, right_chunks:1 |
| 10 | $-2\left(x - 2\right) + 3x - 3 = 3\left(-x + 11\right)$ | $x = 8$ | compose_simplify, ops:8, chunks:1, groups:1, both_sides, right_chunks:1 |
| 10 | $\frac{1}{2}x + \frac{1}{3} = \frac{7}{5}x - \frac{25}{6}$ | $x = 5$ | clear_fractions, both_sides, ops:8 |
| 10 | $x + 7 + \left(x - 2\right)2 = 9x + 5 + \left(-x + 3\right)2$ | $x = -2$ | compose_simplify, ops:8, chunks:1, groups:1, both_sides, right_chunks:1 |
| 14 | $\left(x - 1\right) * 3 - 7x + 5 + \left(\left(x - 1\right) * 3 - 4x + 5\right) = \left(2x - 1\right) * 3 - 4x + \left(\left(x + 11\right) * (-3)\right)$ | $x = 10$ | compose_simplify, ops:10, chunks:2, groups:2, both_sides, right_chunks:2 |
| 14 | $6\left(-x + 2\right) + 7x - 14 + \left(-4\left(x + 3\right) + 5x + 16\right) = 5\left(x + 1\right) - 8x - 4 + \left(2\left(2x - 1\right)\right)$ | $x = -3$ | compose_simplify, ops:10, chunks:2, groups:2, both_sides, right_chunks:2 |
| 14 | $3\left(x + 1\right) - x - 3 + \left(2\left(2x + 3\right) - 5x - 4\right) = 4x + 46 + \left(-4\left(2x - 2\right) + 10x - 7\right)$ | $x = -9$ | compose_simplify, ops:10, chunks:2, groups:2, both_sides, right_chunks:2 |
| 14 | $-2x + 2 + 3 * \left(x - 1\right) + \left(-4x - 3 + 2 * \left(x + 2\right)\right) = -x - 16 - 2 * \left(2x + 3\right) + \left(-3x + 3 + 2 * \left(x - 3\right)\right)$ | $x = -5$ | compose_simplify, ops:10, chunks:2, groups:2, both_sides, right_chunks:2 |
| 18 | $-2\left(x + 2\right) + 4x + 7 + \left(4\left(x - 2\right) - 2x + 4\right) = -2\left(x - 1\right) + 3x - 2 + \left(4\left(x - 3\right) + x - 11\right)$ | $x = 11$ | compose_simplify, ops:12, chunks:2, groups:2, both_sides, right_chunks:2 |
| 18 | $-8x + 3 + 3 * \left(2x - 2\right) + \left(x + 5 - 2 * \left(-x + 1\right)\right) = x - 3 * \left(x - 1\right) + \left(-4x + 58 + 3 * \left(x + 1\right)\right)$ | $x = 16$ | compose_simplify, ops:12, chunks:2, groups:2, both_sides, right_chunks:2 |
| 18 | $\left(x - 1\right) * 2 - x + 4 + \left(\left(x + 1\right) * 3 - x - 3\right) = \left(x - 2\right) * 3 - x + 4 + \left(\left(x + 5\right) * 2 - 2x\right)$ | $x = 6$ | compose_simplify, ops:12, chunks:2, groups:2, both_sides, right_chunks:2 |
| 18 | $2x - 5 + 3\left(x + 2\right) + \left(2 + 2\left(-x - 1\right)\right) = -5x + 6 + 3\left(x - 3\right) + \left(10x - 3 - 2\left(2x + 3\right)\right)$ | $x = 13$ | compose_simplify, ops:12, chunks:2, groups:2, both_sides, right_chunks:2 |
| 22 | $4\left(x - 2\right) - 5x + 9 + \left(4\left(x + 3\right) - 7x - 14\right) + \left(-3\left(x - 1\right) + 13x - 1\right) = 6\left(-x + 1\right) + 9x - 3 + \left(2\left(2x - 3\right) - 2x + 3\right) + \left(2\left(x + 3\right) - 15\right)$ | $x = 10$ | compose_simplify, ops:14, chunks:3, groups:3, both_sides, right_chunks:3 |
| 22 | $\left(x - 2\right) * 2 - 3x + 11 + \left(\left(x + 2\right) * 2 - 3x - 7\right) + \left(\left(2x - 2\right) * 4 - 5x + 8\right) = \left(-x - 2\right) * 2 + \left(\left(-x + 2\right) * (-2) - 5x + 44\right) + \left(\left(x + 3\right) * 3 - x - 9\right)$ | $x = 8$ | compose_simplify, ops:14, chunks:3, groups:3, both_sides, right_chunks:3 |
| 22 | $7 + 3\left(-x - 2\right) + \left(4x - 5 - 2\left(x - 2\right)\right) + \left(x - 3 - 3\left(x - 2\right)\right) = 2\left(-x - 1\right) + \left(2x - 119\right) + \left(7 + 3\left(x - 1\right)\right)$ | $x = 20$ | compose_simplify, ops:14, chunks:3, groups:3, both_sides, right_chunks:3 |
| 22 | $3 * \left(x + 2\right) - x - 4 + \left(4 * \left(x - 1\right) - 2x + 4\right) + \left(5 * \left(x - 1\right) - 7x + 6\right) = 4 * \left(x - 2\right) - 7x + 7 + \left(3 * \left(-x - 2\right) + 4x + 8\right) + 102$ | $x = 25$ | compose_simplify, ops:14, chunks:3, groups:3, both_sides, right_chunks:3 |
| 24 | $\left(x + 2\right)3 - 4 + \left(\left(x - 2\right)\left(-3\right) + 2x - 4\right) + \left(\left(x - 2\right)3 - 2x + 3\right) = \left(x + 1\right)2 + \left(\left(-x + 2\right)\left(-3\right) - 4x + 7\right) + \left(\left(x + 2\right)\left(-2\right) + 3x + 14\right)$ | $x = 12$ | compose_simplify, ops:15, chunks:3, groups:3, both_sides, right_chunks:3 |
| 24 | $3 * \left(2x - 2\right) - 5x + 7 + \left(5 * \left(x + 3\right) - 7x - 12\right) + \left(2 * \left(-x + 3\right) + 8x - 17\right) = 5 * \left(x + 2\right) - 4x - 14 + \left(-7 * \left(x + 3\right) + 8x + 25\right) + \left(-5 * \left(x - 3\right) + 4x + 6\right)$ | $x = 7$ | compose_simplify, ops:15, chunks:3, groups:3, both_sides, right_chunks:3 |
| 24 | $4\left(x - 1\right) - x + 5 + \left(3\left(-x + 1\right) + x - 6\right) + \left(3\left(x - 2\right) + 7\right) = 3\left(x + 3\right) - 2x - 5 + \left(4\left(x - 3\right) - x + 84\right) + \left(3\left(x - 2\right) - 6x + 4\right)$ | $x = 25$ | compose_simplify, ops:15, chunks:3, groups:3, both_sides, right_chunks:3 |
| 24 | $-6 + \left(-x + 2\right)3 + \left(x + 6 + \left(x + 2\right)\left(-2\right)\right) + \left(\left(3x - 2\right)3\right) = 4x + 7 + \left(x + 1\right)\left(-3\right) + \left(2 + \left(x - 2\right)3\right) + \left(-8x - 86 + \left(x + 2\right)5\right)$ | $x = -18$ | compose_simplify, ops:15, chunks:3, groups:3, both_sides, right_chunks:3 |
