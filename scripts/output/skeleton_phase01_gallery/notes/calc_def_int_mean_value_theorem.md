# Notes — `calc_def_int_mean_value_theorem` (`Mean Value Theorem`)

- **Display name:** Mean Value Theorem
- **Category:** Calculus — Definite Integration
- **Generator:** `def_int_mean_value`
- **Suggested family:** other (integral MVT / average value of \(f\) on \([0,b]\); no figure)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Find the average value \(f_{\mathrm{avg}}=\frac{1}{b-a}\int_a^b f\) (Mean Value Theorem for Integrals) on a closed interval.
- **D=0:** Linear leftover \(f(x)=x\) on \([0,b]\) with \(b\in\{2,3\}\) (old easy).
- **Mid D (≈8):** \(f(x)=x\) leftover still allowed, plus \(f(x)=x^{2}\).
- **High D (≈16):** Lock out \(f(x)=x\). \(f(x)=x^{2}\) leftover plus \(f(x)=kx^{2}\) (\(k\in\{2,3,4\}\)).
- **Expert (≈22):** \(f(x)=kx^{2}\) only.
- **Must not:** Differential MVT (\(f'(c)=\frac{f(b)-f(a)}{b-a}\)) — that is `calc_app_diff_mean_value_theorem`; find-\(c\) stems; padded `difficulty_costs`; new cores (\(\sin x\), \(e^x\), \(f(x)=8-2x\), start at \(a\neq 0\)).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. `_pick_family` accumulated unlocks, so high D still mixed \(f(x)=x\). `generator` / `form_id` unstamped. No `spec_snapshot`. 40-seed counts: D=0 all \(f(x)=x\); D=8 leftover \(x\) + \(x^{2}\) (17/23); D=16 still \(f(x)=x\) (14) + \(x^{2}\) (15) + \(kx^{2}\) (11); D=22 still \(f(x)=x\) (10) + \(x^{2}\) (19) + \(kx^{2}\) (11).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the average value of }f(x)=x\text{ on }[0,2].$ | $1$ | \(f(x)=x\) only |
| 0 | 0 | $\text{Find the average value of }f(x)=x\text{ on }[0,3].$ | $\frac{3}{2}$ | \(b\in\{2,3\}\) |
| 8 | 101 | $\text{Find the average value of }f(x)=x\text{ on }[0,3].$ | $\frac{3}{2}$ | \(f(x)=x\) leftover |
| 8 | 7 | $\text{Find the average value of }f(x)=x^{2}\text{ on }[0,3].$ | $3$ | \(x^{2}\) |
| 16 | 101 | $\text{Find the average value of }f(x)=x^{2}\text{ on }[0,6].$ | $12$ | still mixes easy leftover |
| 16 | 207 | $\text{Find the average value of }f(x)=x\text{ on }[0,2].$ | $1$ | \(f(x)=x\) at D=16 |
| 16 | 7 | $\text{Find the average value of }f(x)=4x^{2}\text{ on }[0,2].$ | $\frac{16}{3}$ | \(kx^{2}\) |
| 22 | 101 | $\text{Find the average value of }f(x)=x\text{ on }[0,3].$ | $\frac{3}{2}$ | \(f(x)=x\) leftover at expert |
| 22 | 2 | $\text{Find the average value of }f(x)=3x^{2}\text{ on }[0,3].$ | $9$ | \(kx^{2}\) |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same three builders. D=0 stays old \(f(x)=x\). Gallery seeds 101/207/313 can collide on one form at mid D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the average value of }f(x)=x\text{ on }[0,2].$ | $1$ | `dimvt_linear` |
| 0 | 0 | $\text{Find the average value of }f(x)=x\text{ on }[0,3].$ | $\frac{3}{2}$ | old easy |
| 8 | 1 | $\text{Find the average value of }f(x)=x\text{ on }[0,2].$ | $1$ | \(f(x)=x\) leftover |
| 8 | 101 | $\text{Find the average value of }f(x)=x^{2}\text{ on }[0,3].$ | $3$ | `dimvt_quad` |
| 16 | 1 | $\text{Find the average value of }f(x)=x^{2}\text{ on }[0,2].$ | $\frac{4}{3}$ | \(x^{2}\) leftover |
| 16 | 101 | $\text{Find the average value of }f(x)=4x^{2}\text{ on }[0,3].$ | $12$ | no \(f(x)=x\) leftover |
| 22 | 0 | $\text{Find the average value of }f(x)=2x^{2}\text{ on }[0,5].$ | $\frac{50}{3}$ | `dimvt_quad_coef` only |
| 22 | 101 | $\text{Find the average value of }f(x)=4x^{2}\text{ on }[0,3].$ | $12$ | `dimvt_quad_coef` only |
| 22 | 207 | $\text{Find the average value of }f(x)=2x^{2}\text{ on }[0,6].$ | $24$ | `dimvt_quad_coef` only |

40-seed counts **after**: D=0 `dimvt_linear` only; D=8 leftover `dimvt_linear` + `dimvt_quad` (19/21); D=16 leftover `dimvt_quad` + `dimvt_quad_coef` (19/21, no `dimvt_linear`); D=22 `dimvt_quad_coef` only.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.2 The Definite Integral | https://openstax.org/books/calculus-volume-1/pages/5-2-the-definite-integral | Average value of a function (obj. 5.2.6). Ex. 5.14 linear \(f(x)=x+1\) on \([0,5]\); Checkpoint 5.13 \(f(x)=6-2x\) on \([0,3]\) — old path is monomial \(x\) / \(x^{2}\) / \(kx^{2}\) on \([0,b]\), not these linears |
| OpenStax Calculus Volume 1 §5.3 The Fundamental Theorem of Calculus | https://openstax.org/books/calculus-volume-1/pages/5-3-the-fundamental-theorem-of-calculus | Mean Value Theorem for Integrals (obj. 5.3.1). Ex. 5.15 average of \(f(x)=8-2x\) on \([0,4]\) *and* find \(c\) with \(f(c)=f_{\mathrm{avg}}\); Checkpoint \(f(x)=x/2\) on \([0,6]\) — do **not** invent find-\(c\) on this leaf (old is average-value only) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-2 / 5-3).

## Variety notes

Not a WP. D=0 one easy linear \(f(x)=x\) (old). Same-D rotation at mid D: leftover \(f(x)=x\) vs \(f(x)=x^{2}\). High D keeps the old \(f(x)=kx^{2}\) builder (do not invent \(\sin x\) / \(e^x\) / Ex. 5.14 \(x+1\) / find-\(c\)). Three old forms, so D=16 mixes \(x^{2}\) leftover + \(kx^{2}\) and D=22 is \(kx^{2}\)-only.

## Limitations

- **Status:** shipped — leftover lockout of \(f(x)=x\). Remaining `LIMITATIONS`: three frozen nonnegative monomials on \([0,b]\) (no \(\sin x\) / \(e^x\) / \(\sqrt{x}\), no start at \(a\neq 0\), no Ex. 5.14 \(x+1\) / Ex. 5.15 \(8-2x\)); no find-\(c\) such that \(f(c)=f_{\mathrm{avg}}\); no figure; D=16 can still emit \(f(x)=x^{2}\) leftover (intentional).
- **Live pairwise:** each item stamps `form_id`, `generator=def_int_mean_value`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `def_int_mean_value`

## Proposed engine (reuse vs new)

- **Reuse:** existing linear / quad / quad-coef average-value builders (now in `calc_app_diff.py`). Depth = real structure (lock out \(f(x)=x\); mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** find-\(c\) MVT-for-integrals; OpenStax linears \(x+1\) / \(8-2x\); trig/exp/root integrands; shaded SVG.
