# Notes — `calc_app_diff_linear_approximations`

- **Display name:** Linear approximations
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `linear_approximation`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `linear_approximation`
- **Remaining limits:** Constructive app generators with continuous-D structure knobs. Gaps: story frame banks thinner than OpenStax for related rates / growth; volumes mostly axis-of-rotation textbook templates; no interactive figures.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice linear approximations.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=4.$ | $L(x)=2+\frac{1}{4}(x-4)$ | — |
| 0 | 207 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $L(x)=4+4(x-2)$ | — |
| 8 | 101 | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=4.$ | $L(x)=2+\frac{1}{4}(x-4)$ | — |
| 8 | 207 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $L(x)=4+4(x-2)$ | — |
| 16 | 101 | $\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=5.$ | $L(x)=\frac{1}{5}-\frac{1}{25}(x-5)$ | — |
| 16 | 207 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $L(x)=4+4(x-2)$ | — |
| 22 | 101 | $\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=5.$ | $L(x)=\frac{1}{5}-\frac{1}{25}(x-5)$ | — |
| 22 | 207 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $L(x)=4+4(x-2)$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.2 | https://openstax.org/books/calculus-volume-1/pages/4-2-linear-approximations-and-differentials | L(x)=f(a)+f'(a)(x-a) — e.g. Example 4.5: Linear Approximation of $\sqrt{x}$ Find the linear approximation of $f (x) = \sqrt{x}$ at $x = 9$ and use the approximation to estimate $\sqrt{9.1} .$; Example 4.6: Linear Approximation of $\sin x$ Find the linear approximation of $f (x) = \sin x$ at $x = \frac{\pi}{3}$ and use it to approximate $\sin (62 °) .$ |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep current constructive/pilot generators; reuse Diff only where the student differentiates; apps framing stays separate.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `linear_approximation`; limits/differentiation owned by other agent._
