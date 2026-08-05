# Inequalities audit (one- and two-step)

Open **[gallery.html](gallery.html)** in a browser for KaTeX-rendered math (markdown preview leaves `$...$` as raw LaTeX).

Same as equations with inequality ops; negative coeffs flip the relation.

## one_step/one_step

`{"integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $x - 2 > 0$ | $x > 2$ | — |
| 0 | $x + 1 < 4$ | $x < 3$ | — |
| 0 | $x - 3 > -6$ | $x > -3$ | — |
| 0 | $x + 2 < 4$ | $x < 2$ | — |
| 2 | $x + 3 \le 4$ | $x \le 1$ | non_strict |
| 2 | $2x < 6$ | $x < 3$ | multiply_divide |
| 2 | $x + 3 \ge 2$ | $x \ge -1$ | non_strict |
| 2 | $x - 1 > 1$ | $x > 2$ | multiply_divide |
| 4 | $x + 1 < 3$ | $x < 2$ | multiply_divide, non_strict |
| 4 | $2x > -2$ | $x > -1$ | multiply_divide, non_strict |
| 4 | $x - 2 \ge -1$ | $x \ge 1$ | multiply_divide, non_strict |
| 4 | $x + 2 \ge 2$ | $x \ge 0$ | multiply_divide, non_strict |
| 6 | $x - 1 > 1$ | $x > 2$ | — |
| 6 | $\frac{x}{3} \le 1$ | $x \le 3$ | multiply_divide, non_strict |
| 6 | $\frac{x}{3} < 0$ | $x < 0$ | multiply_divide, non_strict |
| 6 | $x + 1 \ge 5$ | $x \ge 4$ | multiply_divide, non_strict |
| 8 | $x - 1 \ge 1$ | $x \ge 2$ | multiply_divide, non_strict |
| 8 | $3x > 6$ | $x > 2$ | multiply_divide, non_strict |
| 8 | $x - 2 < -2$ | $x < 0$ | multiply_divide, non_strict |
| 8 | $3x \le 9$ | $x \le 3$ | multiply_divide, negative_coeff, non_strict |
| 10 | $x + 1 > -1$ | $x > -2$ | — |
| 10 | $\frac{x}{-2} \ge \frac{1}{2}$ | $x \le -1$ | multiply_divide, negative_coeff, non_strict |
| 10 | $2x < 4$ | $x < 2$ | multiply_divide, negative_coeff, non_strict |
| 10 | $\frac{x}{2} \le \frac{5}{2}$ | $x \le 5$ | multiply_divide, non_strict |
| 12 | $3x \le 3$ | $x \le 1$ | multiply_divide, negative_coeff, non_strict |
| 12 | $x - 3 > -8$ | $x > -5$ | multiply_divide, negative_coeff |
| 12 | $\frac{x}{-2} < \frac{3}{2}$ | $x > -3$ | multiply_divide, negative_coeff, non_strict |
| 12 | $\frac{x}{4} \ge 1$ | $x \ge 4$ | multiply_divide, negative_coeff, non_strict |
| 14 | $\frac{x}{3} \ge -\frac{2}{3}$ | $x \ge -2$ | multiply_divide, negative_coeff, non_strict |
| 14 | $\frac{z}{3} > \frac{1}{3}$ | $z > 1$ | multiply_divide, negative_coeff, non_strict |
| 14 | $-2x > -4$ | $x < 2$ | multiply_divide, negative_coeff, non_strict |
| 14 | $-4x \le -16$ | $x \ge 4$ | multiply_divide, negative_coeff, non_strict |

## one_step/one_step_lock_x

`{"integers_only": true, "lock_variable": "x"}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $x + 2 < 4$ | $x < 2$ | — |
| 0 | $x - 2 > -2$ | $x > 0$ | — |
| 0 | $x - 2 < -5$ | $x < -3$ | — |
| 0 | $x - 3 < -3$ | $x < 0$ | — |
| 2 | $2x < 0$ | $x < 0$ | multiply_divide |
| 2 | $x - 2 < -3$ | $x < -1$ | — |
| 2 | $\frac{x}{2} > 1$ | $x > 2$ | multiply_divide, non_strict |
| 2 | $x + 3 > 3$ | $x > 0$ | multiply_divide |
| 4 | $\frac{x}{2} \ge -\frac{3}{2}$ | $x \ge -3$ | multiply_divide, non_strict |
| 4 | $2x > 4$ | $x > 2$ | multiply_divide, non_strict |
| 4 | $\frac{x}{2} > 1$ | $x > 2$ | multiply_divide, non_strict |
| 4 | $2x \le 4$ | $x \le 2$ | multiply_divide, non_strict |
| 6 | $x - 1 > 2$ | $x > 3$ | — |
| 6 | $x + 1 < 3$ | $x < 2$ | multiply_divide, non_strict |
| 6 | $x - 3 < -2$ | $x < 1$ | non_strict |
| 6 | $\frac{x}{3} < 1$ | $x < 3$ | multiply_divide, non_strict |
| 8 | $\frac{x}{3} \le 1$ | $x \le 3$ | multiply_divide, non_strict |
| 8 | $\frac{x}{3} \ge -1$ | $x \ge -3$ | multiply_divide, negative_coeff, non_strict |
| 8 | $\frac{x}{3} < -\frac{1}{3}$ | $x < -1$ | multiply_divide, non_strict |
| 8 | $\frac{x}{4} > \frac{5}{4}$ | $x > 5$ | multiply_divide, non_strict |
| 10 | $\frac{x}{2} > \frac{1}{2}$ | $x > 1$ | multiply_divide, negative_coeff, non_strict |
| 10 | $-3x < 6$ | $x > -2$ | multiply_divide, negative_coeff, non_strict |
| 10 | $x - 1 < 0$ | $x < 1$ | multiply_divide |
| 10 | $7x > 0$ | $x > 0$ | multiply_divide, non_strict |
| 12 | $\frac{x}{3} \le 1$ | $x \le 3$ | multiply_divide, non_strict |
| 12 | $\frac{x}{-3} < -\frac{2}{3}$ | $x > 2$ | multiply_divide, negative_coeff, non_strict |
| 12 | $-2x > 0$ | $x < 0$ | multiply_divide, negative_coeff, non_strict |
| 12 | $\frac{x}{-2} > 1$ | $x < -2$ | multiply_divide, negative_coeff |
| 14 | $4x \ge 4$ | $x \ge 1$ | multiply_divide, negative_coeff, non_strict |
| 14 | $\frac{x}{-2} \le -\frac{3}{2}$ | $x \ge 3$ | multiply_divide, negative_coeff, non_strict |
| 14 | $x - 6 < -1$ | $x < 5$ | non_strict |
| 14 | $\frac{x}{5} \le -\frac{3}{5}$ | $x \le -3$ | multiply_divide, non_strict |

## two_step/two_step

`{"integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $3x + 2 > 8$ | $x > 2$ | two_step |
| 0 | $2x + 2 < 2$ | $x < 0$ | two_step |
| 0 | $x + 1 < 4$ | $x < 3$ | two_step |
| 0 | $2x + 3 < 9$ | $x < 3$ | two_step |
| 2 | $x + 1 > 4$ | $x > 3$ | multiply_divide, two_step |
| 2 | $x + 1 < 2$ | $x < 1$ | multiply_divide, two_step |
| 2 | $2x + 3 \ge 5$ | $x \ge 1$ | multiply_divide, non_strict, two_step |
| 2 | $x + 2 > 5$ | $x > 3$ | multiply_divide, non_strict, two_step |
| 4 | $2x + 2 < 2$ | $x < 0$ | multiply_divide, non_strict, two_step |
| 4 | $3x + 1 \ge 4$ | $x \ge 1$ | multiply_divide, non_strict, two_step |
| 4 | $2x + 2 > 2$ | $x > 0$ | two_step |
| 4 | $2x + 1 < 5$ | $x < 2$ | multiply_divide, non_strict, two_step |
| 6 | $x + 2 \ge 1$ | $x \ge -1$ | multiply_divide, non_strict, two_step |
| 6 | $2x + 1 < -1$ | $x < -1$ | two_step |
| 6 | $x + 2 > 2$ | $x > 0$ | multiply_divide, two_step |
| 6 | $3x + 3 > 9$ | $x > 2$ | multiply_divide, non_strict, two_step |
| 8 | $3x - 1 \le 5$ | $x \le 2$ | multiply_divide, negative_coeff, non_strict, two_step |
| 8 | $x - 2 > 1$ | $x > 3$ | multiply_divide, negative_coeff, non_strict, two_step |
| 8 | $-x + 1 < -1$ | $x > 2$ | multiply_divide, negative_coeff, non_strict, two_step |
| 8 | $2x + 2 \le 4$ | $x \le 1$ | non_strict, two_step |
| 10 | $4x + 1 \ge 9$ | $x \ge 2$ | non_strict, two_step |
| 10 | $v + 1 \le 1$ | $v \le 0$ | multiply_divide, non_strict, two_step |
| 10 | $x - 1 \ge 0$ | $x \ge 1$ | multiply_divide, negative_coeff, non_strict, two_step |
| 10 | $2x + 3 < 5$ | $x < 1$ | multiply_divide, two_step |
| 12 | $x + 3 < 6$ | $x < 3$ | multiply_divide, negative_coeff, non_strict, two_step |
| 12 | $2z + 1 \ge 3$ | $z \ge 1$ | multiply_divide, non_strict, two_step |
| 12 | $-3x + 5 \ge -10$ | $x \le 5$ | multiply_divide, negative_coeff, non_strict, two_step |
| 12 | $-2z - 3 < -11$ | $z > 4$ | multiply_divide, negative_coeff, two_step |
| 14 | $2y + 2 > -2$ | $y > -2$ | multiply_divide, non_strict, two_step |
| 14 | $2p + 4 < 2$ | $p < -1$ | multiply_divide, two_step |
| 14 | $4x + 2 \ge 6$ | $x \ge 1$ | multiply_divide, non_strict, two_step |
| 14 | $5x - 1 \le 9$ | $x \le 2$ | multiply_divide, negative_coeff, non_strict, two_step |

## two_step/two_step_lock_x

`{"integers_only": true, "lock_variable": "x"}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $2x + 1 > 3$ | $x > 1$ | two_step |
| 0 | $x + 1 > 0$ | $x > -1$ | two_step |
| 0 | $2x + 1 > 7$ | $x > 3$ | two_step |
| 0 | $x + 1 > 4$ | $x > 3$ | two_step |
| 2 | $3x + 2 < -7$ | $x < -3$ | multiply_divide, two_step |
| 2 | $2x + 1 > 3$ | $x > 1$ | multiply_divide, non_strict, two_step |
| 2 | $3x + 2 > 5$ | $x > 1$ | non_strict, two_step |
| 2 | $x + 3 < 3$ | $x < 0$ | multiply_divide, two_step |
| 4 | $2x + 3 < 5$ | $x < 1$ | multiply_divide, non_strict, two_step |
| 4 | $2x + 1 > 5$ | $x > 2$ | non_strict, two_step |
| 4 | $x + 2 > 4$ | $x > 2$ | multiply_divide, two_step |
| 4 | $3x + 2 \ge 2$ | $x \ge 0$ | multiply_divide, non_strict, two_step |
| 6 | $3x + 2 < 8$ | $x < 2$ | two_step |
| 6 | $x + 1 > 4$ | $x > 3$ | two_step |
| 6 | $x + 3 < 1$ | $x < -2$ | non_strict, two_step |
| 6 | $3x + 4 < 10$ | $x < 2$ | two_step |
| 8 | $x + 4 \ge 6$ | $x \ge 2$ | non_strict, two_step |
| 8 | $x + 2 > 5$ | $x > 3$ | multiply_divide, negative_coeff, two_step |
| 8 | $2x + 2 \le 2$ | $x \le 0$ | multiply_divide, non_strict, two_step |
| 8 | $-2x - 2 \le -2$ | $x \ge 0$ | multiply_divide, negative_coeff, non_strict, two_step |
| 10 | $3x + 6 > 21$ | $x > 5$ | two_step |
| 10 | $3x + 2 \ge 8$ | $x \ge 2$ | multiply_divide, negative_coeff, non_strict, two_step |
| 10 | $-3x - 1 \le -1$ | $x \ge 0$ | multiply_divide, negative_coeff, non_strict, two_step |
| 10 | $-3x - 4 < 2$ | $x > -2$ | multiply_divide, negative_coeff, non_strict, two_step |
| 12 | $-2x + 2 < -2$ | $x > 2$ | multiply_divide, negative_coeff, two_step |
| 12 | $x + 3 > 5$ | $x > 2$ | multiply_divide, negative_coeff, two_step |
| 12 | $3x + 8 \le 26$ | $x \le 6$ | multiply_divide, non_strict, two_step |
| 12 | $-x + 1 \le 0$ | $x \ge 1$ | multiply_divide, negative_coeff, non_strict, two_step |
| 14 | $x - 1 < -2$ | $x < -1$ | multiply_divide, negative_coeff, non_strict, two_step |
| 14 | $-2x - 2 < -4$ | $x > 1$ | multiply_divide, negative_coeff, non_strict, two_step |
| 14 | $5x + 1 > 26$ | $x > 5$ | non_strict, two_step |
| 14 | $x + 1 < 2$ | $x < 1$ | multiply_divide, non_strict, two_step |
