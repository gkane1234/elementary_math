# Notes — `calc_app_diff_relative_extrema`

- **Display name:** Relative extrema
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `relative_extrema`

---

## Limitations

- **Status:** shipped — constructive `calc_app_diff`
- **Remaining:** Cubic family is one OpenStax shape (`x^3-3a^2 x`); not the full §4.5 exercise mix (roots, fractional powers).

## What the question should look like (D=0 vs high D)

- **Skill:** Locate relative max/min via vertex or first-derivative test.
- **D=0:** Parabola `(x-h)^2-k` (old-path shape).
- **High D:** Cubic `x^3-3a^2 x+c` with crit `±a`.

## What live path produced (D=0/8/16/22)

| D | seed | prompt_latex | answer_latex | form |
|---|------|--------------|--------------|------|
| 0 | 101 | $\text{Find the relative minimum of }f(x)=(x-5)^{2}-2.$ | $\text{relative minimum }-2\text{ at }x=5$ | parabola_vertex |
| 0 | 207 | $\text{Find the relative minimum of }f(x)=(x-5)^{2}-6.$ | $\text{relative minimum }-6\text{ at }x=5$ | parabola_vertex |
| 8 | 101 | $\text{Find the relative extrema of }f(x)=x^{3}-12x-2.$ | $\text{rel max }14\text{ at }x=-2;\text{ rel min }-18\text{ at }x=2$ | cubic_first_derivative_test |
| 16 | 207 | $\text{Find the relative extrema of }f(x)=x^{3}-12x+1.$ | $\text{rel max }17\text{ at }x=-2;\text{ rel min }-15\text{ at }x=2$ | cubic_first_derivative_test |

OpenStax Calculus Volume 1 §4.3 / §4.5: https://openstax.org/books/calculus-volume-1/pages/4-3-maxima-and-minima
