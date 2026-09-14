# Notes — `calc_app_diff_slope_tangent_and_normal_lines`

- **Display name:** Slope, tangent, and normal lines
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `tangent_normal_line`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `tangent_normal_line`
- **Remaining limits:** Constructive app generators with continuous-D structure knobs. Gaps: story frame banks thinner than OpenStax for related rates / growth; volumes mostly axis-of-rotation textbook templates; no interactive figures.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice slope, tangent, and normal lines.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the tangent line to }y=\ln(2x)\text{ at }x=1.$ | $y-\ln(2)=1\left(x-1\right)$ | — |
| 0 | 207 | $\text{Find the tangent line to }y=\ln(2x)\text{ at }x=1.$ | $y-\ln(2)=1\left(x-1\right)$ | — |
| 8 | 101 | $\text{Find the normal line to }y=\sin(x)\text{ at }x=0.$ | $y-0=-1\left(x-0\right)$ | — |
| 8 | 207 | $\text{Find the tangent line to }y=\sin(x)\text{ at }x=0.$ | $y-0=1\left(x-0\right)$ | — |
| 16 | 101 | $\text{Find the tangent line to }y=\sin(x^{2})\text{ at }x=0.$ | $y=0$ | — |
| 16 | 207 | $\text{Find the tangent line to }y=\frac{x+3}{x+2}\text{ at }x=0.$ | $y-\frac{3}{2}=-\frac{1}{4}\left(x-0\right)$ | — |
| 22 | 101 | $\text{Find the tangent line to }y=\sin(x^{2})\text{ at }x=0.$ | $y=0$ | — |
| 22 | 207 | $\text{Find the tangent line to }y=\frac{x+3}{x+2}\text{ at }x=0.$ | $y-\frac{3}{2}=-\frac{1}{4}\left(x-0\right)$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.1 | https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative | tangent line from f'(a) — e.g. Example 3.1: Finding a Tangent Line Find an equation of the line tangent to the graph of $f (x) = x^{2}$ at $x = 3 .$; Example 3.2: The Slope of a Tangent Line Revisited Use Equation 3.4 to find the slope of the line tangent to the graph of $f (x) = x^{2}$ at $x = 3 .$ |
| OpenStax Calculus Volume 1 §4.2 | https://openstax.org/books/calculus-volume-1/pages/4-2-linear-approximations-and-differentials | linearization / tangent approx — e.g. Example 4.5: Linear Approximation of $\sqrt{x}$ Find the linear approximation of $f (x) = \sqrt{x}$ at $x = 9$ and use the approximation to estimate $\sqrt{9.1} .$; Example 4.6: Linear Approximation of $\sin x$ Find the linear approximation of $f (x) = \sin x$ at $x = \frac{\pi}{3}$ and use it to approximate $\sin (62 °) .$ |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep current constructive/pilot generators; reuse Diff only where the student differentiates; apps framing stays separate.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `tangent_normal_line`; limits/differentiation owned by other agent._
