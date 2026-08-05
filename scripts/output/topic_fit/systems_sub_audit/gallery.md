# Systems (substitution)

Primitive-linear audit for `systems_substitution` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0].

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $\text{Solve: } \begin{cases} y = x - 6 \\ x - 3y = 12 \end{cases}\quad \text{(substitution)}$ | $x = 3,\ y = -3$ | substitution, unique |
| 0 | $\text{Solve: } \begin{cases} y = -\frac{4}{3}x - \frac{8}{3} \\ 4x + y = 0 \end{cases}\quad \text{(substitution)}$ | $x = 1,\ y = -4$ | substitution, unique |
| 0 | $\text{Solve: } \begin{cases} y = \frac{1}{2}x + \frac{11}{2} \\ 3x - 4y = -25 \end{cases}\quad \text{(substitution)}$ | $x = -3,\ y = 4$ | substitution, unique |
| 3 | $\text{Solve: } \begin{cases} y = x - 1 \\ 5x + y = -31 \end{cases}\quad \text{(substitution)}$ | $x = -5,\ y = -6$ | messy_coeffs, substitution, unique |
| 3 | $\text{Solve: } \begin{cases} y = 4x + 17 \\ 5x + 2y = -18 \end{cases}\quad \text{(substitution)}$ | $x = -4,\ y = 1$ | messy_coeffs, substitution, unique |
| 3 | $\text{Solve: } \begin{cases} y = 5x + 31 \\ 5x + 6y = -24 \end{cases}\quad \text{(substitution)}$ | $x = -6,\ y = 1$ | messy_coeffs, substitution, unique |
| 6 | $\text{Solve: } \begin{cases} y = -\frac{1}{6}x + \frac{37}{6} \\ 3x - 6y = -33 \end{cases}\quad \text{(substitution)}$ | $x = 1,\ y = 6$ | messy_coeffs, substitution, unique |
| 6 | $\text{Solve: } \begin{cases} y = 2x + 5 \\ x + 4y = -7 \end{cases}\quad \text{(substitution)}$ | $x = -3,\ y = -1$ | messy_coeffs, substitution, unique |
| 6 | $\text{Solve: } \begin{cases} y = \frac{1}{2}x + 1 \\ 2x - 3y = -2 \end{cases}\quad \text{(substitution)}$ | $x = 2,\ y = 2$ | substitution, unique |
| 10 | $\text{Solve: } \begin{cases} y = x + 7 \\ 2x - 4y = -22 \end{cases}\quad \text{(substitution)}$ | $x = -3,\ y = 4$ | substitution, unique |
| 10 | $\text{Solve: } \begin{cases} y = -\frac{2}{3}x + \frac{5}{3} \\ x - 3y = -11 \end{cases}\quad \text{(substitution)}$ | $x = -2,\ y = 3$ | substitution, unique |
| 10 | $\text{Solve: } \begin{cases} y = -\frac{1}{4}x + \frac{5}{4} \\ 4x + 16y = 18 \end{cases}\quad \text{(substitution)}$ | $\text{no solution}$ | messy_coeffs, none, special_none, substitution |
| 14 | $\text{Solve: } \begin{cases} y = -2x + 1 \\ 8x + 4y = 6 \end{cases}\quad \text{(substitution)}$ | $\text{no solution}$ | messy_coeffs, none, special_infinite, special_none, substitution |
| 14 | $\text{Solve: } \begin{cases} y = -\frac{4}{3}x + \frac{2}{3} \\ 16x + 12y = 7 \end{cases}\quad \text{(substitution)}$ | $\text{no solution}$ | messy_coeffs, none, special_infinite, special_none, substitution |
| 14 | $\text{Solve: } \begin{cases} y = 2x - 3 \\ x + 3y = -2 \end{cases}\quad \text{(substitution)}$ | $x = 1,\ y = -1$ | messy_coeffs, substitution, unique |
| 20 | $\text{Solve: } \begin{cases} y = -\frac{1}{6}x + \frac{2}{3} \\ 3x + 18y = 10 \end{cases}\quad \text{(substitution)}$ | $\text{no solution}$ | messy_coeffs, none, special_infinite, special_none, substitution |
| 20 | $\text{Solve: } \begin{cases} y = -2x + \frac{1}{3} \\ 18x + 9y = 4 \end{cases}\quad \text{(substitution)}$ | $\text{no solution}$ | messy_coeffs, none, special_infinite, special_none, substitution |
| 20 | $\text{Solve: } \begin{cases} y = -\frac{1}{2}x + \frac{1}{2} \\ 2x + 4y = 3 \end{cases}\quad \text{(substitution)}$ | $\text{no solution}$ | messy_coeffs, none, special_infinite, special_none, substitution |
