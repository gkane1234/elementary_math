# Equations audit (one- and two-step)

Open **[gallery.html](gallery.html)** in a browser for KaTeX-rendered math (markdown preview leaves `$...$` as raw LaTeX).

Forced step count by catalog leaf; D drives number/variable complexity.

## one_step/one_step

`{"integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $x + 3 = 3$ | $x = 0$ | — |
| 0 | $x + 3 = 6$ | $x = 3$ | — |
| 0 | $x + 1 = 2$ | $x = 1$ | — |
| 0 | $x - 3 = -6$ | $x = -3$ | — |
| 2 | $x + 1 = 2$ | $x = 1$ | — |
| 2 | $x + 2 = 3$ | $x = 1$ | — |
| 2 | $x - 2 = 0$ | $x = 2$ | — |
| 2 | $\frac{x}{3} = 0$ | $x = 0$ | multiply_divide |
| 4 | $x - 1 = 4$ | $x = 5$ | — |
| 4 | $x + 1 = 2$ | $x = 1$ | multiply_divide |
| 4 | $x - 3 = -8$ | $x = -5$ | multiply_divide |
| 4 | $\frac{x}{2} = 0$ | $x = 0$ | multiply_divide |
| 6 | $x - 3 = -3$ | $x = 0$ | — |
| 6 | $\frac{x}{3} = \frac{2}{3}$ | $x = 2$ | multiply_divide |
| 6 | $\frac{x}{3} = \frac{7}{3}$ | $x = 7$ | multiply_divide |
| 6 | $x - 2 = 4$ | $x = 6$ | — |
| 8 | $x - 3 = -3$ | $x = 0$ | multiply_divide, negative_coeff |
| 8 | $x + 2 = 2$ | $x = 0$ | multiply_divide, negative_coeff |
| 8 | $z - 2 = 4$ | $z = 6$ | — |
| 8 | $\frac{x}{3} = \frac{7}{3}$ | $x = 7$ | multiply_divide, negative_coeff |
| 10 | $\frac{z}{3} = \frac{2}{3}$ | $z = 2$ | multiply_divide |
| 10 | $2z = 2$ | $z = 1$ | multiply_divide |
| 10 | $-3x = 18$ | $x = -6$ | multiply_divide, negative_coeff |
| 10 | $2z = -10$ | $z = -5$ | multiply_divide, negative_coeff |
| 12 | $\frac{x}{3} = \frac{10}{3}$ | $x = 10$ | multiply_divide, negative_coeff |
| 12 | $-2x = -12$ | $x = 6$ | multiply_divide, negative_coeff |
| 12 | $\frac{x}{2} = \frac{3}{2}$ | $x = 3$ | multiply_divide, negative_coeff |
| 12 | $\frac{z}{4} = \frac{1}{2}$ | $z = 2$ | multiply_divide, negative_coeff |
| 14 | $k + 3 = 8$ | $k = 5$ | multiply_divide, negative_coeff |
| 14 | $4z = -4$ | $z = -1$ | multiply_divide, negative_coeff |
| 14 | $\frac{x}{-1} = -6$ | $x = 6$ | multiply_divide, negative_coeff |
| 14 | $\frac{x}{3} = \frac{4}{3}$ | $x = 4$ | multiply_divide, negative_coeff |

## one_step/one_step_lock_x

`{"integers_only": true, "lock_variable": "x"}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $x + 3 = 6$ | $x = 3$ | — |
| 0 | $x - 2 = -5$ | $x = -3$ | — |
| 0 | $x + 3 = 0$ | $x = -3$ | — |
| 0 | $x - 2 = 1$ | $x = 3$ | — |
| 2 | $x + 3 = 2$ | $x = -1$ | — |
| 2 | $x + 3 = 6$ | $x = 3$ | — |
| 2 | $x - 3 = 0$ | $x = 3$ | — |
| 2 | $x + 1 = 4$ | $x = 3$ | — |
| 4 | $x - 1 = -1$ | $x = 0$ | multiply_divide |
| 4 | $x - 1 = 3$ | $x = 4$ | — |
| 4 | $\frac{x}{-3} = \frac{4}{3}$ | $x = -4$ | multiply_divide, negative_coeff |
| 4 | $2x = 4$ | $x = 2$ | multiply_divide |
| 6 | $2x = 4$ | $x = 2$ | multiply_divide |
| 6 | $\frac{x}{1} = 0$ | $x = 0$ | multiply_divide |
| 6 | $x + 3 = -5$ | $x = -8$ | multiply_divide |
| 6 | $\frac{x}{1} = 1$ | $x = 1$ | multiply_divide |
| 8 | $x - 3 = -6$ | $x = -3$ | — |
| 8 | $-2x = 14$ | $x = -7$ | multiply_divide, negative_coeff |
| 8 | $-2x = -10$ | $x = 5$ | multiply_divide, negative_coeff |
| 8 | $4x = 20$ | $x = 5$ | multiply_divide |
| 10 | $x - 4 = 3$ | $x = 7$ | multiply_divide, negative_coeff |
| 10 | $2x = 12$ | $x = 6$ | multiply_divide, negative_coeff |
| 10 | $\frac{x}{-2} = -5$ | $x = 10$ | multiply_divide, negative_coeff |
| 10 | $3x = -3$ | $x = -1$ | multiply_divide |
| 12 | $x - 1 = -11$ | $x = -10$ | multiply_divide, negative_coeff |
| 12 | $-2x = 4$ | $x = -2$ | multiply_divide, negative_coeff |
| 12 | $\frac{x}{-2} = -4$ | $x = 8$ | multiply_divide, negative_coeff |
| 12 | $\frac{x}{1} = -6$ | $x = -6$ | multiply_divide, negative_coeff |
| 14 | $5x = -40$ | $x = -8$ | multiply_divide, negative_coeff |
| 14 | $\frac{x}{-2} = -1$ | $x = 2$ | multiply_divide, negative_coeff |
| 14 | $2x = 12$ | $x = 6$ | multiply_divide |
| 14 | $\frac{x}{-3} = 0$ | $x = 0$ | multiply_divide, negative_coeff |

## two_step/two_step

`{"integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $x + 1 = 1$ | $x = 0$ | two_step |
| 0 | $2x + 2 = 4$ | $x = 1$ | two_step |
| 0 | $x + 2 = 0$ | $x = -2$ | two_step |
| 0 | $3x + 1 = 7$ | $x = 2$ | two_step |
| 2 | $2x + 3 = 7$ | $x = 2$ | multiply_divide, two_step |
| 2 | $2x + 1 = 1$ | $x = 0$ | multiply_divide, two_step |
| 2 | $x + 1 = -2$ | $x = -3$ | multiply_divide, two_step |
| 2 | $x + 3 = 6$ | $x = 3$ | two_step |
| 4 | $x + 1 = 5$ | $x = 4$ | multiply_divide, two_step |
| 4 | $-3x - 1 = -16$ | $x = 5$ | multiply_divide, negative_coeff, two_step |
| 4 | $x + 1 = 1$ | $x = 0$ | multiply_divide, two_step |
| 4 | $3x + 4 = 16$ | $x = 4$ | multiply_divide, two_step |
| 6 | $2x + 2 = 4$ | $x = 1$ | two_step |
| 6 | $2x + 1 = -11$ | $x = -6$ | multiply_divide, two_step |
| 6 | $x + 1 = 3$ | $x = 2$ | multiply_divide, two_step |
| 6 | $x + 2 = 2$ | $x = 0$ | multiply_divide, two_step |
| 8 | $4x + 3 = -17$ | $x = -5$ | two_step |
| 8 | $3x + 6 = 9$ | $x = 1$ | multiply_divide, two_step |
| 8 | $4z + 3 = -9$ | $z = -3$ | two_step |
| 8 | $-x + 2 = 3$ | $x = -1$ | multiply_divide, negative_coeff, two_step |
| 10 | $3x + 1 = -8$ | $x = -3$ | multiply_divide, negative_coeff, two_step |
| 10 | $z + 4 = 9$ | $z = 5$ | two_step |
| 10 | $3x + 1 = 1$ | $x = 0$ | multiply_divide, negative_coeff, two_step |
| 10 | $2x + 2 = 8$ | $x = 3$ | multiply_divide, two_step |
| 12 | $y + 2 = 2$ | $y = 0$ | two_step |
| 12 | $-3x - 2 = -20$ | $x = 6$ | multiply_divide, negative_coeff, two_step |
| 12 | $2h + 5 = 7$ | $h = 1$ | two_step |
| 12 | $-3y + 1 = -5$ | $y = 2$ | multiply_divide, negative_coeff, two_step |
| 14 | $5y - 1 = 34$ | $y = 7$ | multiply_divide, negative_coeff, two_step |
| 14 | $-3y + 2 = 8$ | $y = -2$ | multiply_divide, negative_coeff, two_step |
| 14 | $x - 2 = 9$ | $x = 11$ | multiply_divide, negative_coeff, two_step |
| 14 | $3x - 4 = -22$ | $x = -6$ | multiply_divide, negative_coeff, two_step |

## two_step/two_step_lock_x

`{"integers_only": true, "lock_variable": "x"}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $2x + 2 = 4$ | $x = 1$ | two_step |
| 0 | $2x + 3 = -3$ | $x = -3$ | two_step |
| 0 | $2x + 3 = 5$ | $x = 1$ | two_step |
| 0 | $3x + 2 = 2$ | $x = 0$ | two_step |
| 2 | $2x + 1 = -1$ | $x = -1$ | multiply_divide, two_step |
| 2 | $3x + 1 = 4$ | $x = 1$ | multiply_divide, two_step |
| 2 | $2x + 2 = 2$ | $x = 0$ | multiply_divide, two_step |
| 2 | $3x + 1 = 4$ | $x = 1$ | two_step |
| 4 | $2x - 1 = -11$ | $x = -5$ | multiply_divide, negative_coeff, two_step |
| 4 | $x - 3 = -8$ | $x = -5$ | multiply_divide, negative_coeff, two_step |
| 4 | $2x + 1 = 9$ | $x = 4$ | multiply_divide, two_step |
| 4 | $x + 1 = 2$ | $x = 1$ | two_step |
| 6 | $x + 2 = 7$ | $x = 5$ | two_step |
| 6 | $-4x + 4 = 12$ | $x = -2$ | multiply_divide, negative_coeff, two_step |
| 6 | $3x + 1 = 1$ | $x = 0$ | multiply_divide, two_step |
| 6 | $x + 3 = 5$ | $x = 2$ | two_step |
| 8 | $x - 1 = -8$ | $x = -7$ | multiply_divide, negative_coeff, two_step |
| 8 | $4x + 1 = -3$ | $x = -1$ | multiply_divide, two_step |
| 8 | $2x + 2 = 8$ | $x = 3$ | multiply_divide, two_step |
| 8 | $3x + 1 = 19$ | $x = 6$ | two_step |
| 10 | $3x + 3 = 12$ | $x = 3$ | two_step |
| 10 | $x + 2 = 5$ | $x = 3$ | multiply_divide, negative_coeff, two_step |
| 10 | $-x + 2 = 7$ | $x = -5$ | multiply_divide, negative_coeff, two_step |
| 10 | $-x + 2 = 1$ | $x = 1$ | multiply_divide, negative_coeff, two_step |
| 12 | $4x + 4 = 28$ | $x = 6$ | multiply_divide, two_step |
| 12 | $-3x + 2 = -16$ | $x = 6$ | multiply_divide, negative_coeff, two_step |
| 12 | $3x + 1 = 1$ | $x = 0$ | two_step |
| 12 | $-3x + 2 = -10$ | $x = 4$ | multiply_divide, negative_coeff, two_step |
| 14 | $5x + 5 = 20$ | $x = 3$ | two_step |
| 14 | $3x + 3 = -15$ | $x = -6$ | multiply_divide, negative_coeff, two_step |
| 14 | $-x - 1 = -4$ | $x = 3$ | multiply_divide, negative_coeff, two_step |
| 14 | $-2x - 2 = 6$ | $x = -4$ | multiply_divide, negative_coeff, two_step |
