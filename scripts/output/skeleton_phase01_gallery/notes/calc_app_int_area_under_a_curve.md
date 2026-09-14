# Notes — `calc_app_int_area_under_a_curve` (`Area under a curve`)

- **Display name:** Area under a curve
- **Category:** Calculus — Applications of Integration
- **Generator:** `area_under_curve`
- **Suggested family:** other (FTC area \(\int_0^b f(x)\,dx\); no figure bank)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Find the area under \(y=f(x)\) from \(x=0\) to \(x=b\) via the definite integral (FTC).
- **D=0:** Linear leftover \(y=x\) on \([0,b]\) with \(b\in\{2,3\}\) (old easy).
- **Mid D (≈8):** \(y=x\) leftover still allowed, plus \(y=x^{2}\).
- **High D (≈16):** Lock out \(y=x\). \(y=x^{2}\) leftover plus \(y=kx^{2}\) (\(k\in\{2,3,4\}\)).
- **Expert (≈22):** \(y=kx^{2}\) only.
- **Must not:** Riemann-limit / \(\sum\) stems (that is the sibling limit-of-sums leaf); padded `difficulty_costs`; new cores (\(\sin x\), \(e^x\), \(y=\sqrt{x}\), area between two curves, start at \(a\neq 0\)).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. `_pick_family` accumulated unlocks, so high D still mixed \(y=x\). `generator` / `form_id` unstamped. No `spec_snapshot`. 40-seed counts: D=0 all \(y=x\); D=8 leftover \(x\) + \(x^{2}\) (21/19); D=16 still \(y=x\) (16) + \(x^{2}\) (14) + \(kx^{2}\) (10); D=22 still \(y=x\) (20) + \(x^{2}\) (11) + \(kx^{2}\) (9).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the area under }y=x\text{ from }x=0\text{ to }x=3.$ | $\frac{9}{2}$ | \(y=x\) only |
| 0 | 0 | $\text{Find the area under }y=x\text{ from }x=0\text{ to }x=2.$ | $2$ | \(b\in\{2,3\}\) |
| 8 | 101 | $\text{Find the area under }y=x^{2}\text{ from }x=0\text{ to }x=5.$ | $\frac{125}{3}$ | \(x^{2}\) |
| 8 | 0 | $\text{Find the area under }y=x\text{ from }x=0\text{ to }x=4.$ | $8$ | \(y=x\) leftover |
| 16 | 101 | $\text{Find the area under }y=x^{2}\text{ from }x=0\text{ to }x=3.$ | $9$ | still mixes easy leftover |
| 16 | 1 | $\text{Find the area under }y=x\text{ from }x=0\text{ to }x=3.$ | $\frac{9}{2}$ | \(y=x\) at D=16 |
| 22 | 101 | $\text{Find the area under }y=3x^{2}\text{ from }x=0\text{ to }x=2.$ | $8$ | \(kx^{2}\) |
| 22 | 7 | $\text{Find the area under }y=x\text{ from }x=0\text{ to }x=3.$ | $\frac{9}{2}$ | \(y=x\) leftover at expert |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same three builders. D=0 stays old \(y=x\). Gallery seeds 101/207/313 can collide on one form at mid D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the area under }y=x\text{ from }x=0\text{ to }x=2.$ | $2$ | `auc_linear` |
| 0 | 0 | $\text{Find the area under }y=x\text{ from }x=0\text{ to }x=3.$ | $\frac{9}{2}$ | old easy |
| 8 | 1 | $\text{Find the area under }y=x\text{ from }x=0\text{ to }x=2.$ | $2$ | \(y=x\) leftover |
| 8 | 101 | $\text{Find the area under }y=x^{2}\text{ from }x=0\text{ to }x=3.$ | $9$ | `auc_quad` |
| 16 | 1 | $\text{Find the area under }y=x^{2}\text{ from }x=0\text{ to }x=2.$ | $\frac{8}{3}$ | \(x^{2}\) leftover |
| 16 | 101 | $\text{Find the area under }y=4x^{2}\text{ from }x=0\text{ to }x=3.$ | $36$ | no \(y=x\) leftover |
| 22 | 0 | $\text{Find the area under }y=2x^{2}\text{ from }x=0\text{ to }x=5.$ | $\frac{250}{3}$ | `auc_quad_coef` only |
| 22 | 101 | $\text{Find the area under }y=4x^{2}\text{ from }x=0\text{ to }x=3.$ | $36$ | `auc_quad_coef` only |
| 22 | 207 | $\text{Find the area under }y=2x^{2}\text{ from }x=0\text{ to }x=6.$ | $144$ | `auc_quad_coef` only |

40-seed counts **after**: D=0 `auc_linear` only; D=8 leftover `auc_linear` + `auc_quad` (19/21); D=16 leftover `auc_quad` + `auc_quad_coef` (19/21, no `auc_linear`); D=22 `auc_quad_coef` only.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.2 The Definite Integral | https://openstax.org/books/calculus-volume-1/pages/5-2-the-definite-integral | Area as a definite integral; polynomial on \([0,b]\) (Ex. 5.7 \(\int_0^2 x^{2}\,dx\) is the limit-of-sums sibling — FTC eval is this leaf) |
| OpenStax Calculus Volume 1 §5.3 The Fundamental Theorem of Calculus | https://openstax.org/books/calculus-volume-1/pages/5-3-the-fundamental-theorem-of-calculus | FTC Part 2: \(\int_a^b f=F(b)-F(a)\) for area under a nonnegative graph |
| OpenStax Calculus Volume 1 §6.1 Areas Between Curves | https://openstax.org/books/calculus-volume-1/pages/6-1-areas-between-curves | Area under one curve as the special case \(g=0\) — two-curve stems stay on `calc_app_int_area_between_curves` |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-2 / 5-3 / 6-1).

## Variety notes

Not a WP. D=0 one easy linear \(y=x\) (old). Same-D rotation at mid D: leftover \(y=x\) vs \(y=x^{2}\). High D keeps the old \(y=kx^{2}\) builder (do not invent \(\sin x\) / \(e^x\)). Three old forms, so D=16 mixes \(x^{2}\) leftover + \(kx^{2}\) and D=22 is \(kx^{2}\)-only. Shared generator `area_under_curve` also serves `calc_def_int_area_under_a_curve_by_limit_of_sums` (still FTC wording, not a Riemann \(\lim\sum\)).

## Limitations

- **Status:** shipped — leftover lockout of \(y=x\). Remaining `LIMITATIONS`: three frozen nonnegative monomials on \([0,b]\) (no \(\sin x\) / \(e^x\) / \(\sqrt{x}\), no start at \(a\neq 0\)); no figure / shaded region; D=16 can still emit \(y=x^{2}\) leftover (intentional); sibling `calc_def_int_area_under_a_curve_by_limit_of_sums` skipped (same FTC stem; no \(\lim\sum\) core).
- **Live pairwise:** each item stamps `form_id`, shared `generator=area_under_curve`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `area_under_curve`

## Proposed engine (reuse vs new)

- **Reuse:** existing linear / quad / quad-coef builders (now in `calc_app_diff.py`). Depth = real structure (lock out \(y=x\); mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** Riemann-limit stems; two-curve area; trig/exp/root integrands; shaded SVG.
