# Absolute value equations

Primitive-linear audit for `absolute_value_equations` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0].

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $\text{Solve: } \|x - 3\| = 0$ | $x = 3$ | — |
| 0 | $\text{Solve: } \|x + 3\| = 3$ | $x = -6 \text{ or } x = 0$ | — |
| 0 | $\text{Solve: } \|x - 2\| = 0$ | $x = 2$ | — |
| 3 | $\text{Solve: } \|2x - 2\| = 2$ | $x = 0 \text{ or } x = 2$ | linear_inner |
| 3 | $\text{Solve: } \|x + 2\| = 3$ | $x = -5 \text{ or } x = 1$ | linear_inner |
| 3 | $\text{Solve: } \|-3x + 1\| = 1$ | $x = 0 \text{ or } x = \frac{2}{3}$ | linear_inner |
| 6 | $\text{Solve: } 2\|x + 3\| = 12$ | $x = -9 \text{ or } x = 3$ | coeff_outside, linear_inner |
| 6 | $\text{Solve: } 2\|x - 3\| = 4$ | $x = 1 \text{ or } x = 5$ | coeff_outside, linear_inner |
| 6 | $\text{Solve: } \|2x + 1\| = 9$ | $x = -5 \text{ or } x = 4$ | linear_inner |
| 10 | $\text{Solve: } \|3x + 1\| = \|5x - 1\|$ | $x = 0 \text{ or } x = 1$ | abs_equals_abs, coeff_outside, linear_inner |
| 10 | $\text{Solve: } 2\|x - 3\| = 4$ | $x = 1 \text{ or } x = 5$ | coeff_outside, linear_inner, no_solution |
| 10 | $\text{Solve: } \|-2x + 3\| = \|2x + 2\|$ | $x = \frac{1}{4}$ | abs_equals_abs, coeff_outside, linear_inner |
| 14 | $\text{Solve: } \|-2x - 3\| = 7$ | $x = -5 \text{ or } x = 2$ | linear_inner |
| 14 | $\text{Solve: } \|x + 1\| = \|x - 1\|$ | $x = 0$ | abs_equals_abs, coeff_outside, linear_inner |
| 14 | $\text{Solve: } \|x + 2\| = -1$ | $\text{no solution}$ | abs_equals_abs, coeff_outside, linear_inner, no_solution |
| 20 | $\text{Solve: } \|2x + 3\| = \|-4x + 1\|$ | $x = -\frac{1}{3} \text{ or } x = 2$ | abs_equals_abs, coeff_outside, linear_inner, no_solution |
| 20 | $\text{Solve: } \|x + 2\| = \|2x\|$ | $x = -\frac{2}{3} \text{ or } x = 2$ | abs_equals_abs, coeff_outside, linear_inner, no_solution |
| 20 | $\text{Solve: } \|x + 1\| = \|-x + 1\|$ | $x = 0$ | abs_equals_abs, coeff_outside, linear_inner |
