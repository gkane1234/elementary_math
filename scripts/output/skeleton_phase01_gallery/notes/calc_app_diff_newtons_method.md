# Notes — `calc_app_diff_newtons_method`

- **Display name:** Newton's Method
- **Generator:** `newtons_method`

## Limitations

- **Status:** shipped
- **Remaining:** One quadratic step at low D; two cubic steps at D≥16. Not the full §4.9 mix.

## Live samples

| D | seed | prompt_latex | answer_latex | form |
|---|------|--------------|--------------|------|
| 0 | 101 | $\text{Use one Newton step for }f(x)=x^{2}-3\text{ from }x_0=2.$ | $x_1=\frac{7}{4}$ | newton_one_quad |
| 0 | 207 | $\text{Use one Newton step for }f(x)=x^{2}-3\text{ from }x_0=1.$ | $x_1=2$ | newton_one_quad |
| 16 | 101 | $\text{Use two Newton steps for }f(x)=x^{3}-10\text{ from }x_0=1.$ | $x_2=\frac{23}{8}$ | newton_two_cubic |

OpenStax Vol 1 §4.9: https://openstax.org/books/calculus-volume-1/pages/4-9-newtons-method
