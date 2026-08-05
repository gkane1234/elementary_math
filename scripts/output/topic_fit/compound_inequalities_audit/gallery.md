# Compound inequalities

Primitive-linear audit for `compound_inequalities` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0].

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $\text{Solve: } x \ge 1 \text{ and } x \le 4$ | $1 \le x \le 4$ | — |
| 0 | $\text{Solve: } x > 1 \text{ and } x < 3$ | $1 < x < 3$ | — |
| 0 | $\text{Solve: } x > -2 \text{ and } x \le 0$ | $x > -2 \text{ and } x \le 0$ | — |
| 3 | $\text{Solve: } x \ge -3 \text{ and } x \le -2$ | $-3 \le x \le -2$ | — |
| 3 | $\text{Solve: } x > -2 \text{ and } x \le 0$ | $x > -2 \text{ and } x \le 0$ | two_step_sides |
| 3 | $\text{Solve: } x > -1 \text{ and } x < 1$ | $-1 < x < 1$ | two_step_sides |
| 6 | $\text{Solve: } x < -2 \text{ or } x > 0$ | $x < -2 \text{ or } x > 0$ | or_style, two_step_sides |
| 6 | $\text{Solve: } x < 1 \text{ or } x > 3$ | $x < 1 \text{ or } x > 3$ | or_style |
| 6 | $\text{Solve: } x \ge 2 \text{ and } x \le 3$ | $2 \le x \le 3$ | — |
| 10 | $\text{Solve: } -5 < 4x + 3 < 1$ | $-2 < x < -\frac{1}{2}$ | chain, or_style, two_step_sides |
| 10 | $\text{Solve: } x \ge 0 \text{ and } x \le 2$ | $0 \le x \le 2$ | two_step_sides |
| 10 | $\text{Solve: } -3 < 2x + 3 < 3$ | $-3 < x < 0$ | chain, or_style, two_step_sides |
| 14 | $\text{Solve: } -1 < x < 7$ | $-1 < x < 7$ | chain, or_style, two_step_sides |
| 14 | $\text{Solve: } -6 < x + 1 < 2$ | $-7 < x < 1$ | chain, or_style, two_step_sides |
| 14 | $\text{Solve: } -4 < x + 3 < 0$ | $-7 < x < -3$ | chain, or_style, two_step_sides |
| 20 | $\text{Solve: } 1 < 4x + 1 < 7$ | $0 < x < \frac{3}{2}$ | chain, or_style, two_step_sides |
| 20 | $\text{Solve: } 0 < 2x + 5 < 6$ | $-\frac{5}{2} < x < \frac{1}{2}$ | chain, or_style, two_step_sides |
| 20 | $\text{Solve: } 3 < 6x - 2 < 9$ | $\frac{5}{6} < x < \frac{11}{6}$ | chain, or_style, two_step_sides |
