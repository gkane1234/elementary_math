# Notes — `calc_app_diff_mean_value_theorem` (`Mean Value Theorem`)

- **Display name:** Mean Value Theorem
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `mean_value_theorem`
- **Suggested family:** other (find \(c\) with \(f'(c)=(f(b)-f(a))/(b-a)\) on a closed interval)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Find the MVT point \(c\) on \([a,b]\) for an explicit \(f\).
- **D=0:** \(f(x)=x^{2}\) on \([0,b]\) (old easy) — \(c=b/2\).
- **Mid D (≈8):** Quadratic leftover still allowed, plus \(f=kx^{3}\) on \([0,b]\) (already on the core; \(c=b/\sqrt{3}\)).
- **High D (≈16):** Lock out \(x^{2}\). Cubic leftover plus \(\sqrt{x}\) on \([0,b]\) (Ex. 4.15; \(c=b/4\)).
- **Expert (≈22):** Lock out the cubic leftover. \(\sqrt{x}\) only.
- **Must not:** Hypothesis-only true/false with no \(c\); padded `difficulty_costs`; Rolle-only prompts on this leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**. Families accumulated (`_pick_family`), so high D still emitted \(x^{2}\) / \(px^{2}+q\) leftovers. Cubic was already on the core; \(\sqrt{x}\) was **not**. No `form_id` / `generator` stamp.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{2}\text{ on }[0,2].$ | $1$ | quad |
| 0 | 207 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{2}\text{ on }[0,2].$ | $1$ | same |
| 8 | 101 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{2}\text{ on }[0,2].$ | $1$ | leftover quad |
| 8 | 207 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{3}\text{ on }[0,3].$ | $\frac{3}{\sqrt{3}}$ | cubic on core |
| 16 | 101 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{2}\text{ on }[0,3].$ | $\frac{3}{2}$ | quad leftover at high D |
| 16 | 207 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=2x^{2} - 2\text{ on }[0,4].$ | $2$ | `quad_const` leftover (same midpoint) |
| 22 | 101 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{3}\text{ on }[0,5].$ | $\frac{5}{\sqrt{3}}$ | cubic |
| 22 | 207 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{2}\text{ on }[0,6].$ | $3$ | 28/40 seeds still quad at D=22 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the existing quad/cubic core; Ex. 4.15 \(\sqrt{x}\) unlocks at high D. Dropped \(px^{2}+q\) as a fake-hard duplicate of the midpoint quadratic.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{2}\text{ on }[0,2].$ | $1$ | `mvt_x_squared` |
| 8 | 7 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{2}\text{ on }[0,2].$ | $1$ | quad leftover |
| 8 | 101 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{3}\text{ on }[0,6].$ | $\frac{6}{\sqrt{3}}$ | `mvt_k_x_cubed` |
| 16 | 7 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{3}\text{ on }[0,5].$ | $\frac{5}{\sqrt{3}}$ | cubic leftover |
| 16 | 101 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=\sqrt{x}\text{ on }[0,9].$ | $\frac{9}{4}$ | `mvt_sqrt_x` (Ex. 4.15) |
| 22 | 101 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=\sqrt{x}\text{ on }[0,9].$ | $\frac{9}{4}$ | sqrt only |
| 22 | 5 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=\sqrt{x}\text{ on }[0,16].$ | $4$ | \(c=b/4\) |

40-seed counts **after**: D=0 quad-only; D=8 quad/cubic; D=16 cubic leftover + \(\sqrt{x}\) (no quad); D=22 \(\sqrt{x}\) only.

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.4 | https://openstax.org/books/calculus-volume-1/pages/4-4-the-mean-value-theorem | Ex. 4.15 \(f(x)=\sqrt{x}\) on \([0,9]\), \(c=9/4\); find \(c\) with \(f'(c)=(f(b)-f(a))/(b-a)\) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/4-4-the-mean-value-theorem.md`.

## Variety notes

Not a WP. D=0 one easy quadratic. Same-D rotation at mid D: quad leftover vs \(kx^{3}\). High D \(\sqrt{x}\) on a perfect-square right endpoint (4, 9, 16, 25). Algebra stays closed-form (\(c=b/2\), \(b/\sqrt{3}\), \(b/4\)).

## Limitations

- **Status:** shipped — leftover lockout + Ex. 4.15 \(\sqrt{x}\). Remaining `LIMITATIONS`: no interior-only \(\sqrt{x}\) on \([a,b]\) with \(a>0\); no trig/exp MVT; no dropped-rock velocity story (Ex. 4.16); D=16 can still emit the cubic leftover (intentional); \(px^{2}+q\) dropped as a duplicate midpoint leftover.
- **Live pairwise:** each item stamps `form_id`, shared `generator=mean_value_theorem`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `mean_value_theorem`

## Proposed engine (reuse vs new)

- **Reuse:** existing MVT closed forms (quad + \(kx^{3}\)) moved onto the calc_app_diff constructive core. Depth = real structure (lock out \(x^{2}\) leftovers; unlock \(\sqrt{x}\)) — not padded `difficulty_costs`.
- **Not this pass:** Rolle's leftover lockout (same accumulate pattern on `rolles_theorem`); velocity story frames.
