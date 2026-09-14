# Notes — `calc_app_diff_mean_value_theorem`

- **Display name:** Mean Value Theorem
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `mean_value_theorem`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `mean_value_theorem`
- **Remaining limits:** Constructive app generators with continuous-D structure knobs. Gaps: story frame banks thinner than OpenStax for related rates / growth; volumes mostly axis-of-rotation textbook templates; no interactive figures.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice mean value theorem.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{2}\text{ on }[0,2].$ | $1$ | — |
| 0 | 207 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{2}\text{ on }[0,2].$ | $1$ | — |
| 8 | 101 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=x^{2}\text{ on }[0,4].$ | $2$ | — |
| 8 | 207 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=2x^{3}\text{ on }[0,3].$ | $\frac{3}{\sqrt{3}}$ | — |
| 16 | 101 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=2x^{3}\text{ on }[0,3].$ | $\frac{3}{\sqrt{3}}$ | — |
| 16 | 207 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=3x^{3}\text{ on }[0,2].$ | $\frac{2}{\sqrt{3}}$ | — |
| 22 | 101 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=3x^{3}\text{ on }[0,5].$ | $\frac{5}{\sqrt{3}}$ | — |
| 22 | 207 | $\text{Find }c\text{ guaranteed by the Mean Value Theorem for }f(x)=3x^{3}\text{ on }[0,4].$ | $\frac{4}{\sqrt{3}}$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.4 | https://openstax.org/books/calculus-volume-1/pages/4-4-the-mean-value-theorem | find c with f'(c)=(f(b)-f(a))/(b-a) — e.g. Example 4.14: Using Rolle’s Theorem For each of the following functions, verify that the function satisfies the criteria stated in Rolle’s theorem and find all values $c$ in the given interva…; Example 4.15: Verifying that the Mean Value Theorem Applies For $f (x) = \sqrt{x}$ over the interval $\left[\right. 0 , 9 \left]\right. ,$ show that $f$ satisfies the hypothesis of the Mean V… |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep current constructive/pilot generators; reuse Diff only where the student differentiates; apps framing stays separate.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `mean_value_theorem`; limits/differentiation owned by other agent._
