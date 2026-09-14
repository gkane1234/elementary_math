# Notes — `calc_app_diff_absolute_extrema`

- **Display name:** Absolute extrema
- **Generator:** `absolute_extrema`

## Limitations

- **Status:** shipped
- **Remaining:** Closed-interval cubic can have a repeated abs-min (endpoint = local min); we report one location.

## Live samples

| D | seed | prompt_latex | answer_latex |
|---|------|--------------|--------------|
| 0 | 101 | $\text{Find the absolute extrema of }f(x)=x^{2}\text{ on }[0,3].$ | $\text{abs min }0\text{ at }x=0;\text{ abs max }9\text{ at }x=3$ |
| 8 | 101 | $\text{Find the absolute extrema of }f(x)=x^{3}-12x-2\text{ on }[-4,4].$ | $\text{abs min }-18\text{ at }x=-4;\text{ abs max }14\text{ at }x=-2$ |

OpenStax Vol 1 §4.3 EVT / closed interval.
