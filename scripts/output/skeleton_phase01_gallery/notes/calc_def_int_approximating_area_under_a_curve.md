# Notes — `calc_def_int_approximating_area_under_a_curve` (`Approximating area under a curve`)

- **Display name:** Approximating area under a curve
- **Category:** Calculus — Definite Integration
- **Generator:** `riemann_approximate_area`
- **Suggested family:** other (finite L/R/mid Riemann on a formula \(f\); existing `function_sketch` + `riemann` rectangles)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Approximate area under \(f\) with a finite left / right / midpoint Riemann sum (not a table, not \(\lim\sum\)).
- **D=0:** Midpoint leftover, 2 equal intervals, \(f(x)=x\) on \([0,4]\) (old easy).
- **Mid D (≈8):** That leftover still allowed, plus affine \(f(x)=x+1\) on \([0,4]\) with \(n\in\{2,4\}\) and L/R/mid.
- **High D (≈16):** Lock out \(f(x)=x\). Affine leftover plus \(f(x)=x^{2}\) with L/R/mid and the old hard \(n\)/\(L\) knobs.
- **Expert (≈22):** \(f(x)=x^{2}\) only.
- **Must not:** Table-value Riemann (that is `calc_def_int_riemann_sum_tables`); definition \(\lim\sum\) (skipped limit-of-sums leaf); padded `difficulty_costs`; a new figure bank or Riemann-sum core (\(\sin x\), \(10-x^{2}\) on \([1,2]\), \(a\neq 0\)).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Curve / method / \(n\) accumulated (`linear` always; `affine` at medium; `quad` at hard), so high D still mixed \(f(x)=x\). `form_id` / `generator` unstamped. Metadata already had `function_sketch` + `riemann` rectangles. 40-seed counts: D=0 all midpoint \(n=2\) \(f(x)=x\) on \([0,4]\); D=8 leftover linear (21) + affine (19); D=16 leftover linear (10) + affine (15) + quad (15); D=22 leftover linear (10) + affine (15) + quad (15).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Use a midpoint Riemann sum with }2\text{ equal intervals to approximate the area under }f(x)=x\text{ on }[0,4].$ | $8$ | midpoint \(n=2\) only |
| 0 | 0 | $\text{Use a midpoint Riemann sum with }2\text{ equal intervals to approximate the area under }f(x)=x\text{ on }[0,4].$ | $8$ | frozen old easy |
| 8 | 101 | $\text{Use a left Riemann sum with }2\text{ equal intervals to approximate the area under }f(x)=x+1\text{ on }[0,4].$ | $8$ | affine |
| 8 | 207 | $\text{Use a midpoint Riemann sum with }2\text{ equal intervals to approximate the area under }f(x)=x\text{ on }[0,4].$ | $8$ | linear leftover |
| 16 | 101 | $\text{Use a left Riemann sum with }4\text{ equal intervals to approximate the area under }f(x)=x^{2}\text{ on }[0,4].$ | $14$ | quad |
| 16 | 2 | $\text{Use a midpoint Riemann sum with }2\text{ equal intervals to approximate the area under }f(x)=x\text{ on }[0,4].$ | $8$ | linear leftover at D=16 |
| 22 | 101 | $\text{Use a left Riemann sum with }4\text{ equal intervals to approximate the area under }f(x)=x^{2}\text{ on }[0,4].$ | $14$ | still mixes leftover |
| 22 | 0 | $\text{Use a midpoint Riemann sum with }7\text{ equal intervals to approximate the area under }f(x)=x+1\text{ on }[0,11].$ | $\frac{143}{2}$ | affine leftover at expert |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same three builders. D=0 stays old midpoint \(f(x)=x\), \(n=2\). Existing `function_sketch` + `riemann` rectangles (no new figure bank). Gallery seeds 101/207/313 can collide on one form at mid D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Use a midpoint Riemann sum with }2\text{ equal intervals to approximate the area under }f(x)=x\text{ on }[0,4].$ | $8$ | `raa_linear` |
| 0 | 0 | $\text{Use a midpoint Riemann sum with }2\text{ equal intervals to approximate the area under }f(x)=x\text{ on }[0,4].$ | $8$ | old easy |
| 8 | 1 | $\text{Use a midpoint Riemann sum with }2\text{ equal intervals to approximate the area under }f(x)=x\text{ on }[0,4].$ | $8$ | linear leftover |
| 8 | 101 | $\text{Use a midpoint Riemann sum with }2\text{ equal intervals to approximate the area under }f(x)=x+1\text{ on }[0,4].$ | $12$ | `raa_affine` |
| 16 | 1 | $\text{Use a right Riemann sum with }2\text{ equal intervals to approximate the area under }f(x)=x+1\text{ on }[0,4].$ | $16$ | affine leftover (no \(f(x)=x\)) |
| 16 | 101 | $\text{Use a midpoint Riemann sum with }4\text{ equal intervals to approximate the area under }f(x)=x^{2}\text{ on }[0,4].$ | $21$ | `raa_quad` |
| 22 | 0 | $\text{Use a left Riemann sum with }7\text{ equal intervals to approximate the area under }f(x)=x^{2}\text{ on }[0,11].$ | $\frac{17303}{49}$ | `raa_quad` only |
| 22 | 101 | $\text{Use a midpoint Riemann sum with }4\text{ equal intervals to approximate the area under }f(x)=x^{2}\text{ on }[0,4].$ | $21$ | `raa_quad` only |

40-seed counts **after**: D=0 `raa_linear` 40; D=8 leftover `raa_affine` 21 / `raa_linear` 19; D=16 leftover `raa_quad` 21 / `raa_affine` 19 (no `raa_linear`); D=22 `raa_quad` 40.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.1 Approximating Areas | https://openstax.org/books/calculus-volume-1/pages/5-1-approximating-areas | Obj. 5.1.2–5.1.3: rectangular areas / Riemann sums. Ex. 5.4 is L/R on \(f(x)=x^{2}\), \(n=4\) (old high-D quad builder; interval stays old \([0,L]\), not a new \([0,2]\) core). Ex. 5.5 \(10-x^{2}\) on \([1,2]\) and Ex. 5.6 \(\sin x\) have **no** existing builder |
| OpenStax Calculus Volume 1 §5.2 The Definite Integral | https://openstax.org/books/calculus-volume-1/pages/5-2-the-definite-integral | Definition \(\lim\sum\) stays skipped on `calc_def_int_area_under_a_curve_by_limit_of_sums`; tables stay on `calc_def_int_riemann_sum_tables` |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-1).

## Variety notes

Not a WP. D=0 one easy midpoint \(f(x)=x\), \(n=2\) (old). Same-D leftover mix at D=8 (that plus affine \(x+1\)). High D keeps the old quad builder (do not invent \(\sin x\) / \(10-x^{2}\)). Three old forms, so D=16 mixes affine leftover + quad and D=22 is quad-only. Shared generator `riemann_approximate_area` also leftover-locks `pc_approximating_area_under_a_curve`.

## Limitations

- **Status:** shipped — leftover lockout of D=0 midpoint \(f(x)=x\), \(n=2\). Remaining `LIMITATIONS`: three frozen old builders (linear midpoint \(n=2\) on \([0,4]\); affine \(x+1\) on \([0,4]\) with \(n\in\{2,4\}\); quad \(x^{2}\) with old hard \(n\)/\(L\)); no OpenStax Ex. 5.5 \(10-x^{2}\) / Ex. 5.6 \(\sin x\) / start at \(a\neq 0\); D=16 can still emit affine leftover (intentional); existing generic `function_sketch` + Riemann rectangles (not a new figure bank; bars are midpoint-height even on left/right stems).
- **Live pairwise:** each item stamps `form_id`, `generator=riemann_approximate_area`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `riemann_approximate_area`

## Proposed engine (reuse vs new)

- **Reuse:** existing linear / affine / quad builders (now in `calc_app_diff.py`) plus the existing `function_sketch` Riemann overlay. Depth = real structure (lock out \(f(x)=x\); mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** new figure bank; \(\sin x\) / \(10-x^{2}\) cores; table Riemann; definition \(\lim\sum\).
