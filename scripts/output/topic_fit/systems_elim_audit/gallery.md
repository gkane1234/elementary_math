# Systems (elimination)

Primitive-linear audit for `systems_elimination` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0].

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $\text{Solve: } \begin{cases} x + y = -4 \\ -x + y = -4 \end{cases}$ | $x = 0,\ y = -4$ | elimination, unique |
| 0 | $\text{Solve: } \begin{cases} -x + 2y = -1 \\ 4x + 4y = 4 \end{cases}$ | $x = 1,\ y = 0$ | elimination, unique |
| 0 | $\text{Solve: } \begin{cases} x + 2y = -7 \\ -2x - y = 8 \end{cases}$ | $x = -3,\ y = -2$ | elimination, unique |
| 3 | $\text{Solve: } \begin{cases} 2x + y = 1 \\ -6x - 4y = -8 \end{cases}$ | $x = -2,\ y = 5$ | elimination, messy_coeffs, unique |
| 3 | $\text{Solve: } \begin{cases} -2x - 3y = 3 \\ -4x + y = -15 \end{cases}$ | $x = 3,\ y = -3$ | elimination, unique |
| 3 | $\text{Solve: } \begin{cases} 3x + y = -5 \\ x - 3y = -5 \end{cases}$ | $x = -2,\ y = 1$ | elimination, unique |
| 6 | $\text{Solve: } \begin{cases} -4x + y = 1 \\ -4x - 2y = -2 \end{cases}$ | $x = 0,\ y = 1$ | elimination, messy_coeffs, unique |
| 6 | $\text{Solve: } \begin{cases} -6x - y = 18 \\ -2x - y = 2 \end{cases}$ | $x = -4,\ y = 6$ | elimination, messy_coeffs, unique |
| 6 | $\text{Solve: } \begin{cases} -4x + y = -17 \\ -4x + 2y = -18 \end{cases}$ | $x = 4,\ y = -1$ | elimination, unique |
| 10 | $\text{Solve: } \begin{cases} 4x + 5y = 2 \\ 16x + 20y = 6 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_infinite, special_none |
| 10 | $\text{Solve: } \begin{cases} 3x + 2y = 4 \\ 12x + 8y = 17 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_none |
| 10 | $\text{Solve: } \begin{cases} 2x + 4y = 5 \\ 6x + 12y = 13 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_none |
| 14 | $\text{Solve: } \begin{cases} 3x + y = 3 \\ 9x + 3y = 8 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_infinite, special_none |
| 14 | $\text{Solve: } \begin{cases} 5x + y = 5 \\ 15x + 3y = 16 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_infinite, special_none |
| 14 | $\text{Solve: } \begin{cases} 3x + 4y = 4 \\ 6x + 8y = 9 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_none |
| 20 | $\text{Solve: } \begin{cases} x + 4y = 5 \\ 4x + 16y = 22 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_infinite, special_none |
| 20 | $\text{Solve: } \begin{cases} 4x + y = 3 \\ 12x + 3y = 10 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_none |
| 20 | $\text{Solve: } \begin{cases} 4x + 3y = 1 \\ 8x + 6y = 0 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_infinite, special_none |
