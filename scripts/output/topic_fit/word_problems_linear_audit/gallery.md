# Word problems (mixture→equation)

Primitive-linear audit for `wp_mixture` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0].

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $\text{Jordan mixes two solutions. The amounts satisfy $2x + 1 = -3$. Find $x$.}$ | $x = -2$ | two_step |
| 0 | $\text{Casey mixes two solutions. The amounts satisfy $x + 2 = 2$. Find $x$.}$ | $x = 0$ | two_step |
| 0 | $\text{Casey mixes two solutions. The amounts satisfy $2x + 3 = 7$. Find $x$.}$ | $x = 2$ | two_step |
| 3 | $\text{Casey mixes two solutions. The amounts satisfy $2x + 2 = 8$. Find $x$.}$ | $x = 3$ | multiply_divide, two_step |
| 3 | $\text{Jordan mixes two solutions. The amounts satisfy $x + 1 = 2$. Find $x$.}$ | $x = 1$ | multiply_divide, two_step |
| 3 | $\text{Riley mixes two solutions. The amounts satisfy $3x + 2 = -7$. Find $x$.}$ | $x = -3$ | multiply_divide, two_step |
| 6 | $\text{Taylor mixes two solutions. The amounts satisfy $4x + 3 = -1$. Find $x$.}$ | $x = -1$ | multiply_divide, two_step |
| 6 | $\text{Jordan mixes two solutions. The amounts satisfy $2x + 2 = 6$. Find $x$.}$ | $x = 2$ | multiply_divide, two_step |
| 6 | $\text{Alex mixes two solutions. The amounts satisfy $x + 1 = 3$. Find $x$.}$ | $x = 2$ | two_step |
| 10 | $\text{Taylor mixes two solutions. The amounts satisfy $x + 4 = 8$. Find $x$.}$ | $x = 4$ | two_step |
| 10 | $\text{Casey mixes two solutions. The amounts satisfy $3x - 1 = -7$. Find $x$.}$ | $x = -2$ | multiply_divide, negative_coeff, two_step |
| 10 | $\text{Sam mixes two solutions. The amounts satisfy $-5x - 4 = -19$. Find $x$.}$ | $x = 3$ | multiply_divide, negative_coeff, two_step |
| 14 | $\text{Casey mixes two solutions. The amounts satisfy $2x + 3 = 9$. Find $x$.}$ | $x = 3$ | multiply_divide, negative_coeff, two_step |
| 14 | $\text{Casey mixes two solutions. The amounts satisfy $2x + 2 = 4$. Find $x$.}$ | $x = 1$ | multiply_divide, negative_coeff, two_step |
| 14 | $\text{Alex mixes two solutions. The amounts satisfy $3x + 2 = 11$. Find $x$.}$ | $x = 3$ | multiply_divide, negative_coeff, two_step |
| 20 | $\text{Casey mixes two solutions. The amounts satisfy $-3x - 1 = -4$. Find $x$.}$ | $x = 1$ | multiply_divide, negative_coeff, two_step |
| 20 | $\text{Casey mixes two solutions. The amounts satisfy $x + 4 = 4$. Find $x$.}$ | $x = 0$ | multiply_divide, negative_coeff, two_step |
| 20 | $\text{Casey mixes two solutions. The amounts satisfy $6x + 5 = 5$. Find $x$.}$ | $x = 0$ | multiply_divide, two_step |
