# Multi-step inequalities audit

Open **[gallery.html](gallery.html)** in a browser for KaTeX-rendered math (markdown preview leaves `$...$` as raw LaTeX).

Mirrors multi-step equations with the same <code>n_ops = 3 + floor(log2(1 + D/2))</code> formula; flips the inequality when the net variable coefficient is negative.

## default

`{"integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $-4x + 9 + \left(x - 3\right)3 > 2$ | $x < -2$ | compose_simplify, ops:3, groups:1, nested |
| 0 | $5x - 8 - 3\left(x - 3\right) > 1$ | $x > 0$ | compose_simplify, ops:3, groups:1, nested |
| 0 | $\left(x + 1\right)2 > 8$ | $x > 3$ | compose_simplify, ops:3, groups:1, nested |
| 0 | $5x + 3 + \left(x + 2\right)\left(-2\right) > 8$ | $x > 3$ | compose_simplify, ops:3, groups:1, nested |
| 1 | $-6 + 3\left(x + 2\right) > -9$ | $x > -3$ | compose_simplify, ops:3, groups:1, nested |
| 1 | $-5x + 3 + \left(x - 3\right)2 > -12$ | $x < 3$ | compose_simplify, ops:3, groups:1, nested |
| 1 | $\left(x + 2\right)\left(-2\right) + 3x + 2 > -2$ | $x > 0$ | compose_simplify, ops:3, groups:1, nested |
| 1 | $-2x - 4 + 3\left(x + 2\right) < -1$ | $x < -3$ | compose_simplify, ops:3, groups:1, nested |
| 2 | $4x - 5 - 3\left(x - 2\right) > 2$ | $x > 1$ | compose_simplify, ops:3, groups:1, nested |
| 2 | $2\left(x - 2\right) + x + 5 < 10$ | $x < 3$ | compose_simplify, ops:3, groups:1, nested |
| 2 | $x + 4 + 2\left(x - 3\right) < 7$ | $x < 3$ | compose_simplify, ops:3, groups:1, nested |
| 2 | $\left(x + 3\right)3 - x - 6 > 9$ | $x > 3$ | compose_simplify, ops:3, groups:1, nested |
| 4 | $2\left(x + 3\right) - x - 3 > 3\left(x + 3\right) - 10$ | $x < 2$ | compose_simplify, ops:4, groups:1, nested, both_sides, right_groups:1 |
| 4 | $-5 + \left(x + 2\right)2 > 6x - 1 + \left(x - 3\right)2$ | $x < 1$ | compose_simplify, ops:4, groups:1, nested, both_sides, right_groups:1 |
| 4 | $2\left(x + 2\right) - 3x - 3 < 1$ | $x > 0$ | compose_simplify, ops:3, groups:1, nested |
| 4 | $-2x + 8 + 3\left(x - 2\right) < 10x - 21 - 2\left(x - 1\right)$ | $x > 3$ | compose_simplify, ops:4, groups:1, nested, both_sides, right_groups:1 |
| 6 | $-2x + 8 + 3\left(x - 2\right) > -2\left(-3x + 4\right)$ | $x < 2$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 6 | $-5 + 3\left(x + 2\right) < -3x - 2 + 3\left(x - 1\right)$ | $x < -2$ | compose_simplify, ops:4, groups:1, nested, both_sides, right_groups:1 |
| 6 | $-3\left(x - 1\right) \ge 3\left(x - 2\right) - 10x + 5$ | $x \ge -1$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 6 | $-6x + 8 + 3\left(x - 2\right) < -12x - 25 + 2\left(x + 3\right)$ | $x < -3$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 8 | $\left(-x + 1\right)2 \le x + 24 + \left(x - 2\right)4$ | $x \ge -2$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 8 | $-5y - 5 + \left(y + 1\right)3 < -7y + 4 + \left(y - 2\right)3$ | $y < 0$ | compose_simplify, ops:4, groups:1, nested, both_sides, right_groups:1 |
| 8 | $2\left(x - 1\right) + x + 5 \le 3\left(x + 1\right) - 4x + 4$ | $x \le 1$ | compose_simplify, ops:6, groups:1, nested, both_sides, right_groups:1 |
| 8 | $3\left(z + 1\right) < 2\left(-2z - 9\right)$ | $z < -3$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 10 | $3 * \left(-x + 2\right) + 5x - 4 < -3 * \left(x + 3\right) + 4x + 12$ | $x < 1$ | compose_simplify, ops:7, groups:1, nested, both_sides, right_groups:1 |
| 10 | $4\left(y + 1\right) \le 7y + 10 + 2\left(y - 3\right)$ | $y \ge 0$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 10 | $\left(x - 1\right)3 - 2x - 2 < \left(x - 2\right)5 - 9x + 15$ | $x < 2$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 10 | $4y - 3 + \left(y - 3\right)\left(-2\right) < 3y - 2 + \left(y - 1\right)3$ | $y > 2$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 14 | $4x - 5 - 3\left(x - 2\right) < -7x - 3 + 3\left(x - 2\right)$ | $x < -2$ | compose_simplify, ops:8, groups:1, nested, both_sides, right_groups:1 |
| 14 | $\left(h + 1\right)3 < 9h - 3 + \left(h - 1\right)\left(-2\right)$ | $h > 1$ | compose_simplify, ops:6, groups:1, nested, both_sides, right_groups:1 |
| 14 | $-5 * \left(x - 2\right) + 4x - 9 \le 5 * \left(x - 1\right) - 12x + 12$ | $x \le 1$ | compose_simplify, ops:7, groups:1, nested, both_sides, right_groups:1 |
| 14 | $-4z - 8 + 3\left(z + 3\right) < 9z - 8 - 3\left(z - 3\right)$ | $z > 0$ | compose_simplify, ops:7, groups:1, nested, both_sides, right_groups:1 |
| 18 | $-7z + 17 + \left(z - 3\right)4 > -2z - 5 + \left(z - 2\right)3$ | $z < 4$ | compose_simplify, ops:8, groups:1, nested, both_sides, right_groups:1 |
| 18 | $2\left(y - 3\right) + 2y + 3 > 4\left(y + 1\right) + 6y - 13$ | $y < 1$ | compose_simplify, ops:9, groups:1, nested, both_sides, right_groups:1 |
| 18 | $\left(-z + 2\right) * 5 + 6z - 16 \le \left(z + 1\right) * 3 - z - 8$ | $z \ge -1$ | compose_simplify, ops:8, groups:1, nested, both_sides, right_groups:1 |
| 18 | $2 * \left(x - 1\right) - x + 3 > 3 * \left(-x + 3\right) + 8x$ | $x < -2$ | compose_simplify, ops:10, groups:2, nested, both_sides, right_groups:1 |
| 22 | $5\lambda + 7 + \left(\lambda + 1\right)\left(-2\right) < -11\lambda + 19 + \left(\lambda + 1\right)7$ | $\lambda < 3$ | compose_simplify, ops:4, groups:1, nested, both_sides, right_groups:1 |
| 22 | $-3\left(v - 3\right) + 7v - 8 > -3\left(v - 3\right) + 10v - 14$ | $v < 2$ | compose_simplify, ops:8, groups:1, nested, both_sides, right_groups:1 |
| 22 | $4 * \left(x + 2\right) - 3x - 7 > 4 * \left(x + 3\right) - 2x - 17$ | $x < 6$ | compose_simplify, ops:11, groups:2, nested, both_sides, right_groups:1 |
| 22 | $2\left(\psi + 2\right) + \psi + 1 \le -4\left(\psi + 1\right) + 12\psi - 6$ | $\psi \ge 3$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 24 | $\left(2g - 2\right)2 \le \left(g + 2\right)5 + 2g - 17$ | $g \ge 1$ | compose_simplify, ops:7, groups:1, nested, both_sides, right_groups:1 |
| 24 | $\left(\tau - 3\right)\left(-2\right) + 3\tau - 3 \le \left(\tau - 1\right)3$ | $\tau \ge 3$ | compose_simplify, ops:7, groups:1, nested, both_sides, right_groups:1 |
| 24 | $\left(n + 1\right)3 - 7n + 2 \ge \left(-n - 1\right)3 - 7n + 26$ | $n \ge 3$ | compose_simplify, ops:10, groups:1, nested, both_sides, right_groups:1 |
| 24 | $2 * \left(n + 1\right) \ge -3 * \left(-n - 2\right)$ | $n \le -4$ | compose_simplify, ops:10, groups:1, nested, both_sides, right_groups:1 |

## lock_x

`{"integers_only": true, "lock_variable": "x"}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $-2\left(x - 3\right) + 3x - 6 < 1$ | $x < 1$ | compose_simplify, ops:3, groups:1, nested |
| 0 | $2\left(x + 1\right) > 2$ | $x > 0$ | compose_simplify, ops:3, groups:1, nested |
| 0 | $x + 5 + 2\left(x - 1\right) < 12$ | $x < 3$ | compose_simplify, ops:3, groups:1, nested |
| 0 | $\left(x + 1\right)2 > 8$ | $x > 3$ | compose_simplify, ops:3, groups:1, nested |
| 1 | $\left(x - 2\right)2 - 5x + 3 < -4$ | $x > 1$ | compose_simplify, ops:3, groups:1, nested |
| 1 | $3\left(x - 2\right) - x + 8 > -4$ | $x > -3$ | compose_simplify, ops:3, groups:1, nested |
| 1 | $\left(-x + 1\right)2 > 4$ | $x < -1$ | compose_simplify, ops:3, groups:1, nested |
| 1 | $-2\left(x - 2\right) + x - 2 < 0$ | $x > 2$ | compose_simplify, ops:3, groups:1, nested |
| 2 | $-x + 2\left(x - 1\right) > -2$ | $x > 0$ | compose_simplify, ops:3, groups:1, nested |
| 2 | $-x - 3 + 3\left(x + 1\right) < 2$ | $x < 1$ | compose_simplify, ops:3, groups:1, nested |
| 2 | $\left(x + 2\right)2 - x - 2 < 2$ | $x < 0$ | compose_simplify, ops:3, groups:1, nested |
| 2 | $\left(x + 1\right)3 - x - 3 < 6$ | $x < 3$ | compose_simplify, ops:3, groups:1, nested |
| 4 | $\left(x + 1\right)2 + x > 2$ | $x > 0$ | compose_simplify, ops:3, groups:1, nested |
| 4 | $-x + 4 + 3\left(x - 1\right) < -4x + 4 + 3\left(x + 1\right)$ | $x < 2$ | compose_simplify, ops:4, groups:1, nested, both_sides, right_groups:1 |
| 4 | $x + 7 + 3\left(x - 1\right) < 12$ | $x < 2$ | compose_simplify, ops:3, groups:1, nested |
| 4 | $-2x - 1 + 4\left(x + 1\right) < -3$ | $x < -3$ | compose_simplify, ops:3, groups:1, nested |
| 6 | $6 - 3\left(-x + 2\right) \le -3\left(-2x + 1\right)$ | $x \ge 1$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 6 | $-7 + 3\left(x + 2\right) \le -7x + 22 + 3\left(x - 3\right)$ | $x \le 2$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 6 | $\left(x + 3\right)2 + x - 4 \ge \left(2x + 1\right)2$ | $x \le 0$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 6 | $\left(x + 2\right)\left(-2\right) + 3x + 2 < \left(x - 1\right)2 + 5x$ | $x > 0$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 8 | $x - 1 + \left(x + 1\right)2 > \left(-2x + 11\right)2$ | $x > 3$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 8 | $3\left(x + 3\right) - 6x - 5 > 3\left(x - 3\right) - 9x + 13$ | $x > 0$ | compose_simplify, ops:4, groups:1, nested, both_sides, right_groups:1 |
| 8 | $\left(x + 1\right)2 \ge -4x - 10 + \left(x + 3\right)3$ | $x \ge -1$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 8 | $-3\left(x + 2\right) - x + 9 > -5$ | $x < 2$ | compose_simplify, ops:3, groups:1, nested |
| 10 | $-3\left(x + 2\right) + 5x + 8 \le 2\left(x - 1\right) + 3x + 1$ | $x \ge 1$ | compose_simplify, ops:6, groups:1, nested, both_sides, right_groups:1 |
| 10 | $9x - 5 + \left(x - 2\right)\left(-4\right) < 18$ | $x < 3$ | compose_simplify, ops:3, groups:1, nested |
| 10 | $3\left(x + 3\right) - 2x - 6 \ge 2\left(x - 3\right) + 5x - 9$ | $x \le 3$ | compose_simplify, ops:6, groups:1, nested, both_sides, right_groups:1 |
| 10 | $\left(x + 1\right)2 + x - 2 \ge \left(x - 3\right)2 + 5x - 2$ | $x \le 2$ | compose_simplify, ops:6, groups:1, nested, both_sides, right_groups:1 |
| 14 | $\left(x + 3\right)2 - x - 3 \le \left(x - 1\right)3 - x + 8$ | $x \ge -2$ | compose_simplify, ops:7, groups:1, nested, both_sides, right_groups:1 |
| 14 | $-2x + 9 + 3\left(x - 3\right) < -7x - 2 + 2\left(x + 1\right)$ | $x < 0$ | compose_simplify, ops:5, groups:1, nested, both_sides, right_groups:1 |
| 14 | $\left(-x + 3\right)2 + x - 6 \ge \left(-x + 3\right)\left(-2\right)$ | $x \le 2$ | compose_simplify, ops:9, groups:1, nested, both_sides, right_groups:1 |
| 14 | $\left(x + 3\right) * 3 - 5x - 9 \le \left(x + 1\right) * 3 - 3$ | $x \ge 0$ | compose_simplify, ops:9, groups:1, nested, both_sides, right_groups:1 |
| 18 | $2\left(x + 3\right) + x - 5 < -3\left(x - 2\right) + 11x - 5$ | $x > 0$ | compose_simplify, ops:6, groups:1, nested, both_sides, right_groups:1 |
| 18 | $-2x + 13 + \left(x + 2\right)\left(-4\right) \le -9x + 4 + \left(x - 1\right)5$ | $x \ge 3$ | compose_simplify, ops:9, groups:1, nested, both_sides, right_groups:1 |
| 18 | $12x - 8 + \left(x - 1\right)\left(-10\right) < 4$ | $x < 1$ | compose_simplify, ops:3, groups:1, nested |
| 18 | $3\left(-x + 1\right) < -7x + 8 - 3\left(x - 3\right)$ | $x < 2$ | compose_simplify, ops:8, groups:1, nested, both_sides, right_groups:1 |
| 22 | $-3\left(x - 1\right) + 6x + 1 \ge 2\left(x + 8\right) - 2x$ | $x \ge 4$ | compose_simplify, ops:11, groups:2, nested, both_sides, right_groups:1 |
| 22 | $3\left(x - 2\right) - x + 6 < 3\left(x - 1\right) - 4x + 3$ | $x < 0$ | compose_simplify, ops:10, groups:1, nested, both_sides, right_groups:1 |
| 22 | $-x - 7 + \left(x + 3\right) * 3 > 4x + \left(x - 1\right) * 5$ | $x < 1$ | compose_simplify, ops:8, groups:1, nested, both_sides, right_groups:1 |
| 22 | $5 * \left(x + 2\right) - 6x - 10 < -5 * \left(x + 2\right) + 2x + 6$ | $x < -2$ | compose_simplify, ops:8, groups:1, nested, both_sides, right_groups:1 |
| 24 | $\left(x - 2\right)\left(-3\right) + 13x + 3 > \left(x - 2\right)5 - 2x + 61$ | $x > 6$ | compose_simplify, ops:4, groups:1, nested, both_sides, right_groups:1 |
| 24 | $10x + 14 + \left(2x + 3\right)\left(-3\right) \ge -2x + 3 + \left(x + 1\right)4$ | $x \ge 1$ | compose_simplify, ops:9, groups:1, nested, both_sides, right_groups:1 |
| 24 | $4\left(x + 2\right) - 5 \le 2\left(-x + 3\right) + 12x - 21$ | $x \ge 3$ | compose_simplify, ops:9, groups:1, nested, both_sides, right_groups:1 |
| 24 | $\left(x + 3\right) * (-2) - 4x + 9 > \left(x - 3\right) * 7 - 8x + 44$ | $x < -4$ | compose_simplify, ops:9, groups:1, nested, both_sides, right_groups:1 |
