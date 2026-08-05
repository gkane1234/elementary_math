# Writing linear equations

Primitive-linear audit for `writing_linear_equations` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0].

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $\text{Write the slope-intercept equation of the line with slope } 1 \text{ and } y\text{-intercept } 1.$ | $y = x + 1$ | — |
| 0 | $\text{Write the slope-intercept equation of the line with slope } 2 \text{ and } y\text{-intercept } -1.$ | $y = 2x - 1$ | — |
| 0 | $\text{Write the slope-intercept equation of the line with slope } 2 \text{ and } y\text{-intercept } -3.$ | $y = 2x - 3$ | — |
| 3 | $\text{Write the point-slope equation of the line with slope } 1 \text{ through } (2, 3).$ | $y - 3 = 1(x - 2)$ | point_slope |
| 3 | $\text{Write the point-slope equation of the line with slope } 2 \text{ through } (-1, -1).$ | $y + 1 = 2(x + 1)$ | point_slope |
| 3 | $\text{Write the slope-intercept equation of the line with slope } 2 \text{ and } y\text{-intercept } 2.$ | $y = 2x + 2$ | — |
| 6 | $\text{Write } y = x + 1 \text{ in standard form } Ax + By = C.$ | $x - y = -1$ | point_slope, standard |
| 6 | $\text{Write } y = -2x + 3 \text{ in standard form } Ax + By = C.$ | $2x + y = 3$ | point_slope, standard |
| 6 | $\text{Write } y = -3x + 2 \text{ in standard form } Ax + By = C.$ | $3x + y = 2$ | point_slope, standard |
| 10 | $\text{Write an equation of the line through } (4, 15) \text{ and } (6, 21).$ | $y = 3x + 3$ | from_two_points, point_slope, standard |
| 10 | $\text{Write } y = 4x + 2 \text{ in standard form } Ax + By = C.$ | $4x - y = -2$ | point_slope, standard |
| 10 | $\text{Write } y = x \text{ in standard form } Ax + By = C.$ | $x - y = 0$ | point_slope, standard |
| 14 | $\text{Write the point-slope equation of the line with slope } -7 \text{ through } (2, -11).$ | $y + 11 = -7(x - 2)$ | point_slope |
| 14 | $\text{Write an equation of the line through } (-3, -9) \text{ and } (0, 3).$ | $y = 4x + 3$ | from_two_points, point_slope, standard |
| 14 | $\text{Write an equation of the line through } (2, -3) \text{ and } (4, -9).$ | $y = -3x + 3$ | from_two_points, point_slope, standard |
| 20 | $\text{Write an equation of the line through } (-6, 18) \text{ and } (-4, 12).$ | $y = -3x$ | from_two_points, point_slope, standard |
| 20 | $\text{Write an equation of the line through } (-4, -4) \text{ and } (-1, -1).$ | $y = x$ | from_two_points, point_slope, standard |
| 20 | $\text{Write an equation of the line through } (3, -1) \text{ and } (6, -4).$ | $y = -x + 2$ | from_two_points, point_slope, standard |
