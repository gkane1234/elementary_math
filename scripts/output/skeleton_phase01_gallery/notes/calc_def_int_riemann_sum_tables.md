# Notes — `calc_def_int_riemann_sum_tables` (`Riemann sum tables`)

- **Display name:** Riemann sum tables
- **Category:** Calculus — Definite Integration
- **Generator:** `riemann_sum_tables`
- **Suggested family:** other (short value table → left / right / midpoint Riemann sum; no figure)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Approximate \(\int_a^b f\) from tabulated values (left / right / midpoint), not a formula \(f\) and not \(\lim\sum\).
- **D=0:** 3-point leftover \(f(0),f(1),f(2)\) on \([0,2]\), left Riemann, \(\Delta x=1\) (old easy).
- **Mid D (≈8):** That leftover still allowed, plus 4-point left or right on \([0,3]\).
- **High D (≈16):** Lock out 3-point left. 4-point leftover plus midpoint on \([0,4]\) with \(\Delta x=2\).
- **Expert (≈22):** Midpoint only.
- **Must not:** Formula-curve finite Riemann (that is `calc_def_int_approximating_area_under_a_curve`); definition \(\lim\sum\) (skipped limit-of-sums leaf); padded `difficulty_costs`; new cores (CO₂ / sea-level story tables, \(L_n\) vs \(R_n\) pair).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. `_pick_family` accumulated `left3` + `left_right4` + `midpoint`, so high D still mixed 3-point left. `form_id` / `generator` unstamped. 40-seed counts: D=0 all 3-point left; D=8 leftover 3-point left (23) + 4-point L/R (17); D=16 leftover 3-point left (10) + 4-point (17) + midpoint (13); D=22 leftover 3-point left (15) + 4-point (14) + midpoint (11).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $f(0)=5, f(1)=4, f(2)=5.\quad\text{Approximate }\int_{0}^{2} f(x)\,dx\text{ with a left Riemann sum.}$ | $9$ | 3-point left only |
| 0 | 207 | $f(0)=1, f(1)=2, f(2)=2.\quad\text{Approximate }\int_{0}^{2} f(x)\,dx\text{ with a left Riemann sum.}$ | $3$ | \(y\in\{1,\ldots,5\}\) |
| 8 | 101 | $f(0)=4, f(1)=5, f(2)=3, f(3)=5.\quad\text{Approximate }\int_{0}^{3} f(x)\,dx\text{ with a right Riemann sum.}$ | $13$ | 4-point right |
| 8 | 207 | $f(0)=5, f(1)=1, f(2)=2.\quad\text{Approximate }\int_{0}^{2} f(x)\,dx\text{ with a left Riemann sum.}$ | $6$ | 3-point leftover |
| 16 | 101 | $\text{On }[0,4]\text{ with }\Delta x=2,\text{ the midpoint values are }f(1)=1\text{ and }f(3)=5.\quad\text{Find the midpoint Riemann sum.}$ | $12$ | midpoint |
| 16 | 1 | $f(0)=1, f(1)=1, f(2)=4.\quad\text{Approximate }\int_{0}^{2} f(x)\,dx\text{ with a left Riemann sum.}$ | $2$ | 3-point leftover at D=16 |
| 22 | 101 | $f(0)=1, f(1)=2, f(2)=2.\quad\text{Approximate }\int_{0}^{2} f(x)\,dx\text{ with a left Riemann sum.}$ | $3$ | 3-point leftover at expert |
| 22 | 0 | $\text{On }[0,4]\text{ with }\Delta x=2,\text{ the midpoint values are }f(1)=1\text{ and }f(3)=4.\quad\text{Find the midpoint Riemann sum.}$ | $10$ | midpoint |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same three builders. D=0 stays old 3-point left. Gallery seeds 101/207/313 can collide on one form at mid D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $f(0)=2, f(1)=5, f(2)=3.\quad\text{Approximate }\int_{0}^{2} f(x)\,dx\text{ with a left Riemann sum.}$ | $7$ | `rst_left3` |
| 0 | 0 | $f(0)=4, f(1)=1, f(2)=3.\quad\text{Approximate }\int_{0}^{2} f(x)\,dx\text{ with a left Riemann sum.}$ | $5$ | old easy |
| 8 | 1 | $f(0)=1, f(1)=3, f(2)=1.\quad\text{Approximate }\int_{0}^{2} f(x)\,dx\text{ with a left Riemann sum.}$ | $4$ | 3-point leftover |
| 8 | 101 | $f(0)=2, f(1)=5, f(2)=3, f(3)=4.\quad\text{Approximate }\int_{0}^{3} f(x)\,dx\text{ with a left Riemann sum.}$ | $10$ | `rst_left_right4` |
| 16 | 1 | $f(0)=1, f(1)=3, f(2)=1, f(3)=4.\quad\text{Approximate }\int_{0}^{3} f(x)\,dx\text{ with a right Riemann sum.}$ | $8$ | 4-point leftover (no left3) |
| 16 | 101 | $\text{On }[0,4]\text{ with }\Delta x=2,\text{ the midpoint values are }f(1)=2\text{ and }f(3)=5.\quad\text{Find the midpoint Riemann sum.}$ | $14$ | `rst_midpoint` |
| 22 | 0 | $\text{On }[0,4]\text{ with }\Delta x=2,\text{ the midpoint values are }f(1)=4\text{ and }f(3)=1.\quad\text{Find the midpoint Riemann sum.}$ | $10$ | `rst_midpoint` only |
| 22 | 101 | $\text{On }[0,4]\text{ with }\Delta x=2,\text{ the midpoint values are }f(1)=2\text{ and }f(3)=5.\quad\text{Find the midpoint Riemann sum.}$ | $14$ | `rst_midpoint` only |

40-seed counts **after**: D=0 `rst_left3` 40; D=8 leftover `rst_left_right4` 21 / `rst_left3` 19; D=16 leftover `rst_midpoint` 21 / `rst_left_right4` 19 (no `rst_left3`); D=22 `rst_midpoint` 40.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.1 Approximating Areas | https://openstax.org/books/calculus-volume-1/pages/5-1-approximating-areas | Table values → Riemann sum (obj. 5.1.3). Ex. 5.1–5.3 are formula-curve L/R/mid (other leaf). Exercises 38–41 are applied tables (CO₂ / sea level / gas / population) — old path is numeric \(f(x_i)\) tables, not those stories |
| OpenStax Calculus Volume 1 §5.2 The Definite Integral | https://openstax.org/books/calculus-volume-1/pages/5-2-the-definite-integral | Definition \(\lim\sum\) stays skipped on `calc_def_int_area_under_a_curve_by_limit_of_sums` |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-1).

## Variety notes

Not a WP. D=0 one easy 3-point left (old). Same-D leftover mix at D=8 (that plus 4-point L/R). High D keeps the old midpoint builder (do not invent story tables or \(L_n\) vs \(R_n\)). Three old forms, so D=16 mixes 4-point leftover + midpoint and D=22 is midpoint-only.

## Limitations

- **Status:** shipped — leftover lockout of D=0 3-point left. Remaining `LIMITATIONS`: three frozen old builders (always \(\Delta x=1\) integer tables on \([0,2]\) / \([0,3]\), or frozen midpoint on \([0,4]\) with \(\Delta x=2\)); no OpenStax story tables (Ex. 38–41); no \(L_n\) and \(R_n\) pair; no unequal \(\Delta x\); D=16 can still emit 4-point leftover (intentional).
- **Live pairwise:** each item stamps `form_id`, `generator=riemann_sum_tables`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `riemann_sum_tables`

## Proposed engine (reuse vs new)

- **Reuse:** existing left3 / left-right4 / midpoint builders (now in `calc_app_diff.py`). Depth = real structure (lock out 3-point left; mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** CO₂ / sea-level story tables; formula-curve Riemann; definition \(\lim\sum\).
