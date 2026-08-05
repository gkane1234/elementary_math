# Word problems (systems)

Primitive-linear audit for `wp_systems` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0].

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $\text{Alex buys two items. The costs satisfy } \begin{cases} x + 3y = 1 \\ -3x - 3y = -3 \end{cases}$ | $x = 1,\ y = 0$ | elimination, unique |
| 0 | $\text{Jordan buys two items. The costs satisfy } \begin{cases} 3x + y = -7 \\ 2x - 3y = 10 \end{cases}$ | $x = -1,\ y = -4$ | elimination, unique |
| 0 | $\text{Jordan buys two items. The costs satisfy } \begin{cases} 3x - 3y = 3 \\ -2x - 3y = 18 \end{cases}$ | $x = -3,\ y = -4$ | elimination, unique |
| 3 | $\text{Alex buys two items. The costs satisfy } \begin{cases} 4x + 2y = 6 \\ -2x + 3y = -15 \end{cases}$ | $x = 3,\ y = -3$ | elimination, messy_coeffs, unique |
| 3 | $\text{Sam buys two items. The costs satisfy } \begin{cases} -x + y = -4 \\ -x - 3y = 16 \end{cases}$ | $x = -1,\ y = -5$ | elimination, messy_coeffs, unique |
| 3 | $\text{Jordan buys two items. The costs satisfy } \begin{cases} x + 2y = 3 \\ -2x - 3y = -3 \end{cases}$ | $x = -3,\ y = 3$ | elimination, unique |
| 6 | $\text{Riley buys two items. The costs satisfy } \begin{cases} -2x - 5y = 27 \\ 5x + 5y = -30 \end{cases}$ | $x = -1,\ y = -5$ | elimination, messy_coeffs, unique |
| 6 | $\text{Sam buys two items. The costs satisfy } \begin{cases} x - 3y = -12 \\ x - y = -8 \end{cases}$ | $x = -6,\ y = 2$ | elimination, messy_coeffs, unique |
| 6 | $\text{Riley buys two items. The costs satisfy } \begin{cases} 6x + y = 5 \\ 18x + 3y = 17 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_none |
| 10 | $\text{Taylor buys two items. The costs satisfy } \begin{cases} 4x + 4y = 4 \\ 16x + 16y = 17 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_none |
| 10 | $\text{Alex buys two items. The costs satisfy } \begin{cases} 5x + 6y = 4 \\ 15x + 18y = 13 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_none |
| 10 | $\text{Alex buys two items. The costs satisfy } \begin{cases} 2x + 6y = 3 \\ 6x + 18y = 8 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_none |
| 14 | $\text{Casey buys two items. The costs satisfy } \begin{cases} 3x + 4y = 1 \\ 6x + 8y = 0 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_none |
| 14 | $\text{Sam buys two items. The costs satisfy } \begin{cases} 4x + 3y = 4 \\ 8x + 6y = 9 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_none |
| 14 | $\text{Riley buys two items. The costs satisfy } \begin{cases} 3x + 6y = 3 \\ 9x + 18y = 7 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_infinite, special_none |
| 20 | $\text{Sam buys two items. The costs satisfy } \begin{cases} x + y = 6 \\ 4x + 4y = 26 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_infinite, special_none |
| 20 | $\text{Sam buys two items. The costs satisfy } \begin{cases} x + 4y = 3 \\ 4x + 16y = 14 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_infinite, special_none |
| 20 | $\text{Sam buys two items. The costs satisfy } \begin{cases} 5x + 3y = 1 \\ 20x + 12y = 5 \end{cases}$ | $\text{no solution}$ | elimination, messy_coeffs, none, special_infinite, special_none |
