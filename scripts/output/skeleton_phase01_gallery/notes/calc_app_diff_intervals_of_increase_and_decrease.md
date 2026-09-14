# Notes — `calc_app_diff_intervals_of_increase_and_decrease`

- **Display name:** Intervals of increase and decrease
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `intervals_increase_decrease`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `intervals_increase_decrease`
- **Remaining limits:** Constructive app generators with continuous-D structure knobs. Gaps: story frame banks thinner than OpenStax for related rates / growth; volumes mostly axis-of-rotation textbook templates; no interactive figures.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice intervals of increase and decrease.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the intervals where } f(x) = x^{2} + 3x+ 1 \text{ is increasing.}$ | $(-1.5, \infty)$ | — |
| 0 | 207 | $\text{Find the intervals where } f(x) = x^{2} + 3x- 2 \text{ is increasing.}$ | $(-1.5, \infty)$ | — |
| 8 | 101 | $\text{Find the intervals where } f(x) = x^{2} - 1x- 2 \text{ is increasing.}$ | $(0.5, \infty)$ | — |
| 8 | 207 | $\text{Find the intervals where } f(x) = x^{2} + 8x+ 3 \text{ is increasing.}$ | $(-4, \infty)$ | — |
| 16 | 101 | $\text{Find the intervals where } f(x) = x^{2} + 1x+ 3 \text{ is increasing.}$ | $(-0.5, \infty)$ | — |
| 16 | 207 | $\text{Find the intervals where } f(x) = x^{2} + 8x+ 4 \text{ is increasing.}$ | $(-4, \infty)$ | — |
| 22 | 101 | $\text{Find the intervals where } f(x) = x^{2} + 2x \text{ is increasing.}$ | $(-1, \infty)$ | — |
| 22 | 207 | $\text{Find the intervals where } f(x) = x^{2} + 8x+ 2 \text{ is increasing.}$ | $(-4, \infty)$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.5 | https://openstax.org/books/calculus-volume-1/pages/4-5-derivatives-and-the-shape-of-a-graph | sign chart of f' — e.g. Example 4.17: Using the First Derivative Test to Find Local Extrema Use the first derivative test to find the location of all local extrema for $f (x) = x^{3} - 3 x^{2} - 9 x - 1 .$ Use a gra…; Example 4.18: Using the First Derivative Test Use the first derivative test to find the location of all local extrema for $f (x) = 5 x^{1 / 3} - x^{5 / 3} .$ Use a graphing utility to confirm… |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep current constructive/pilot generators; reuse Diff only where the student differentiates; apps framing stays separate.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `intervals_increase_decrease`; limits/differentiation owned by other agent._
