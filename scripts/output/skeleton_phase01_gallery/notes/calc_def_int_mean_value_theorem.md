# Notes — `calc_def_int_mean_value_theorem`

- **Display name:** Mean Value Theorem
- **Category:** Calculus — Definite Integration
- **Generator:** `def_int_mean_value`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `def_int_mean_value`
- **Remaining limits:** Reuse `integrals.py` / FTC / Riemann constructive cores. Gaps: curve families still thin vs OpenStax §5–6 (mostly poly); trig-sub / PFD / multi-trick are catalog-shaped but not full textbook exercise breadth.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice mean value theorem.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the average value of }f(x)=x\text{ on }[0,2].$ | $1$ | — |
| 0 | 207 | $\text{Find the average value of }f(x)=x\text{ on }[0,2].$ | $1$ | — |
| 8 | 101 | $\text{Find the average value of }f(x)=x^{2}\text{ on }[0,3].$ | $3$ | — |
| 8 | 207 | $\text{Find the average value of }f(x)=x\text{ on }[0,2].$ | $1$ | — |
| 16 | 101 | $\text{Find the average value of }f(x)=x^{2}\text{ on }[0,4].$ | $\frac{16}{3}$ | — |
| 16 | 207 | $\text{Find the average value of }f(x)=x\text{ on }[0,3].$ | $\frac{3}{2}$ | — |
| 22 | 101 | $\text{Find the average value of }f(x)=x^{2}\text{ on }[0,2].$ | $\frac{4}{3}$ | — |
| 22 | 207 | $\text{Find the average value of }f(x)=x^{2}\text{ on }[0,6].$ | $12$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.2 | https://openstax.org/books/calculus-volume-1/pages/5-2-the-definite-integral | mean value for integrals / average value — e.g. Example 5.7: Evaluating an Integral Using the Definition Use the definition of the definite integral to evaluate $\int_{0}^{2} x^{2} d x .$ Use a right-endpoint approximation to generate the…; Example 5.8: Using Geometric Formulas to Calculate Definite Integrals Use the formula for the area of a circle to evaluate $\int_{3}^{6} \sqrt{9 - (x - 3)^{2}} d x .$ |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep constructive integral-application builders; optional Integral skeleton for shared definite-integral cores.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `def_int_mean_value`; limits/differentiation owned by other agent._
