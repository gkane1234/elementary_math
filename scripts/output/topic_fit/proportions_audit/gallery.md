# Proportions

Primitive-linear audit for `solving_proportions` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0].

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $\text{Solve: } \frac{2}{3} = \frac{x}{1}$ | $x = \frac{2}{3}$ | — |
| 0 | $\text{Solve: } \frac{3}{1} = \frac{x}{2}$ | $x = 6$ | — |
| 0 | $\text{Solve: } \frac{3}{3} = \frac{x}{2}$ | $x = 2$ | — |
| 3 | $\text{Solve: } \frac{2}{1} = \frac{x}{2}$ | $x = 4$ | — |
| 3 | $\text{Solve: } \frac{1}{1} = \frac{x}{3}$ | $x = 3$ | — |
| 3 | $\text{Solve: } \frac{1}{x} = \frac{1}{1}$ | $x = 1$ | variable_in_denom |
| 6 | $\text{Solve: } \frac{3}{2} = \frac{x}{4}$ | $x = 6$ | — |
| 6 | $\text{Solve: } \frac{2}{x} = \frac{1}{3}$ | $x = 6$ | multi_step_clear, variable_in_denom |
| 6 | $\text{Solve: } \frac{1}{x} = \frac{1}{2}$ | $x = 2$ | variable_in_denom |
| 10 | $\text{Solve: } \frac{1}{x} = \frac{2}{1}$ | $x = \frac{1}{2}$ | multi_step_clear, variable_in_denom |
| 10 | $\text{Solve: } \frac{4}{x} = \frac{1}{5}$ | $x = 20$ | variable_in_denom |
| 10 | $\text{Solve: } \frac{2}{x} = \frac{2}{3}$ | $x = 3$ | multi_step_clear, variable_in_denom |
| 14 | $\text{Solve: } \frac{3}{x} = \frac{4}{3}$ | $x = \frac{9}{4}$ | multi_step_clear, variable_in_denom |
| 14 | $\text{Solve: } \frac{3}{x} = \frac{5}{3}$ | $x = \frac{9}{5}$ | multi_step_clear, variable_in_denom |
| 14 | $\text{Solve: } \frac{4}{x} = \frac{1}{2}$ | $x = 8$ | multi_step_clear, variable_in_denom |
| 20 | $\text{Solve: } \frac{2}{x} = \frac{3}{1}$ | $x = \frac{2}{3}$ | multi_step_clear, variable_in_denom |
| 20 | $\text{Solve: } \frac{4}{x} = \frac{3}{1}$ | $x = \frac{4}{3}$ | multi_step_clear, variable_in_denom |
| 20 | $\text{Solve: } \frac{5}{x} = \frac{2}{5}$ | $x = \frac{25}{2}$ | variable_in_denom |
