# Notes — `calc_diff_eq_introduction`

- **Display name:** Introduction
- **Generator:** `de_introduction`

## Limitations

- **Status:** shipped — verify-solution (OpenStax Vol 2 §4.1).
- **Remaining:** Classify order / linear vs nonlinear not yet.

## Live samples

| D | seed | prompt_latex | answer_latex | form |
|---|------|--------------|--------------|------|
| 0 | 101 | $\text{Verify that }y=Ce^{3x}\text{ solves }y'=3y.$ | $y'=3Ce^{3x}=3y$ | verify_exp |
| 8 | 101 | $\text{Verify that }y=Cx^{4}\text{ solves }x\,y'=4y\text{ for }x>0.$ | $y'=4Cx^{3}\Rightarrow x y'=4y$ | verify_euler |

OpenStax Calculus Volume 2 §4.1: https://openstax.org/books/calculus-volume-2/pages/4-1-basics-of-differential-equations
