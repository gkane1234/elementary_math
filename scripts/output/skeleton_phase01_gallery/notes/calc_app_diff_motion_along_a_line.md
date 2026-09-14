# Notes — `calc_app_diff_motion_along_a_line`

- **Display name:** Motion along a line
- **Generator:** `motion_along_a_line`

## Limitations

- **Status:** shipped
- **Remaining:** Quadratic `s(t)=t^2-nt` only; no piecewise / trig motion.

## Live samples

| D | seed | prompt_latex | answer_latex | form |
|---|------|--------------|--------------|------|
| 0 | 101 | $s(t)=t^{2}-6t.\quad\text{Find }v(6).$ | $6$ | eval_velocity |
| 8 | 101 | $s(t)=t^{2}-2t.\quad\text{When is the particle at rest?}$ | $t=1$ | particle_at_rest |
| 16 | 101 | $s(t)=t^{2}-6t.\quad\text{Find }a(t).$ | $2$ | acceleration_const |

OpenStax Vol 1 §3.4.
