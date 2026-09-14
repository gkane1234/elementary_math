# Notes — `calc_app_diff_differentials`

- **Display name:** Differentials
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `differentials`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `differentials`
- **Remaining limits:** Constructive app generators with continuous-D structure knobs. Gaps: story frame banks thinner than OpenStax for related rates / growth; volumes mostly axis-of-rotation textbook templates; no interactive figures.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice differentials.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{For }y=\log(x),\text{ find }dy.$ | $dy=\frac{1}{x}\,dx$ | — |
| 0 | 207 | $\text{For }y=\log(x),\text{ find }dy.$ | $dy=\frac{1}{x}\,dx$ | — |
| 8 | 101 | $\text{For }y=x^{-1},\text{ find }dy.$ | $dy=-\frac{1}{x^{2}}\,dx$ | — |
| 8 | 207 | $\text{For }y=\frac{1}{x},\text{ find }dy.$ | $dy=-\frac{1}{x^{2}}\,dx$ | — |
| 16 | 101 | $\text{For }y=\exp(x^{2}),\text{ find }dy.$ | $dy=2xe^{x^{2}}\,dx$ | — |
| 16 | 207 | $\text{For }y=\frac{x}{x+1},\text{ find }dy.$ | $dy=\frac{1}{\left(x+1\right)^{2}}\,dx$ | — |
| 22 | 101 | $\text{For }y=\exp(x^{2}),\text{ find }dy.$ | $dy=2xe^{x^{2}}\,dx$ | — |
| 22 | 207 | $\text{For }y=\frac{x}{x+1},\text{ find }dy.$ | $dy=\frac{1}{\left(x+1\right)^{2}}\,dx$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.2 | https://openstax.org/books/calculus-volume-1/pages/4-2-linear-approximations-and-differentials | dy = f'(x) dx; estimate Δy — e.g. Example 4.5: Linear Approximation of $\sqrt{x}$ Find the linear approximation of $f (x) = \sqrt{x}$ at $x = 9$ and use the approximation to estimate $\sqrt{9.1} .$; Example 4.6: Linear Approximation of $\sin x$ Find the linear approximation of $f (x) = \sin x$ at $x = \frac{\pi}{3}$ and use it to approximate $\sin (62 °) .$ |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep current constructive/pilot generators; reuse Diff only where the student differentiates; apps framing stays separate.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `differentials`; limits/differentiation owned by other agent._
