# Slope

Primitive-linear audit for `slope` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0].

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $\text{Find the slope of the line through } (-2, 3) \text{ and } (1, 12).$ | $3$ | — |
| 0 | $\text{Find the slope of the line through } (2, 2) \text{ and } (3, -1).$ | $-3$ | — |
| 0 | $\text{Find the slope of the line through } (1, -1) \text{ and } (3, 5).$ | $3$ | — |
| 3 | $\text{Find the slope of the line through } (0, -3) \text{ and } (1, -5).$ | $-2$ | negative_slope |
| 3 | $\text{Find the slope of the line through } (0, 0) \text{ and } (1, -2).$ | $-2$ | negative_slope |
| 3 | $\text{Find the slope of the line through } (3, -4) \text{ and } (4, -1).$ | $3$ | — |
| 6 | $\text{Find the slope of the line } y = -x - 1.$ | $-1$ | from_equation, negative_slope |
| 6 | $\text{Find the slope of the line through } (0, 4) \text{ and } (3, -5).$ | $-3$ | negative_slope |
| 6 | $\text{Find the slope of the line } y = 4x + 4.$ | $4$ | from_equation |
| 10 | $\text{Find the slope of the line } y = -3x + 1.$ | $-3$ | from_equation, negative_slope |
| 10 | $\text{Find the slope of the line } y = -\frac{1}{2}x - 2.$ | $-\frac{1}{2}$ | fraction_slope, from_equation, negative_slope |
| 10 | $\text{Find the slope of the line } y = -3x + 2.$ | $-3$ | fraction_slope, from_equation, negative_slope |
| 14 | $\text{Find the slope of the line } y = -x + 3.$ | $-1$ | fraction_slope, from_equation, negative_slope |
| 14 | $\text{Find the slope of the line } y = -2x + 3.$ | $-2$ | fraction_slope, from_equation, negative_slope |
| 14 | $\text{Find the slope of the line } y = -\frac{3}{2}x + 3.$ | $-\frac{3}{2}$ | fraction_slope, from_equation, negative_slope |
| 20 | $\text{Find the slope of the line } y = -x.$ | $-1$ | fraction_slope, from_equation, negative_slope |
| 20 | $\text{Find the slope of the line } y = -\frac{1}{2}x.$ | $-\frac{1}{2}$ | fraction_slope, from_equation, negative_slope |
| 20 | $\text{Find the slope of the line } y = -\frac{5}{4}x + 1.$ | $-\frac{5}{4}$ | fraction_slope, from_equation, negative_slope |
