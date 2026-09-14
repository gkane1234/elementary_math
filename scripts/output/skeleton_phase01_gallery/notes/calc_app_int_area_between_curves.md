# Notes — `calc_app_int_area_between_curves`

- **Display name:** Area between curves
- **Category:** Calculus — Applications of Integration
- **Generator:** `area_between_curves`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `area_between_curves`
- **Remaining limits:** Constructive app generators with continuous-D structure knobs. Gaps: story frame banks thinner than OpenStax for related rates / growth; volumes mostly axis-of-rotation textbook templates; no interactive figures.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice area between curves.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the area between }y=x\text{ and }y=0\text{ from }x=0\text{ to }x=4.$ | $8$ | — |
| 0 | 207 | $\text{Find the area between }y=x\text{ and }y=0\text{ from }x=0\text{ to }x=3.$ | $\frac{9}{2}$ | — |
| 8 | 101 | $\text{Find the area between }y=x^{2}\text{ and }y=0\text{ from }x=0\text{ to }x=5.$ | $\frac{125}{3}$ | — |
| 8 | 207 | $\text{Find the area between }y=x^{2}\text{ and }y=0\text{ from }x=0\text{ to }x=5.$ | $\frac{125}{3}$ | — |
| 16 | 101 | $\text{Find the area of the region bounded by }y=x\text{ and }y=x^{2}.$ | $\frac{1}{6}$ | — |
| 16 | 207 | $\text{Find the area of the region bounded by }y=x\text{ and }y=x^{2}.$ | $\frac{1}{6}$ | — |
| 22 | 101 | $\text{Find the area between }y=3-x\text{ and }y=0\text{ from }x=0\text{ to }x=3.$ | $\frac{9}{2}$ | — |
| 22 | 207 | $\text{Find the area of the region bounded by }y=x\text{ and }y=x^{2}.$ | $\frac{1}{6}$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §6.1 | https://openstax.org/books/calculus-volume-1/pages/6-1-areas-between-curves | ∫ (top−bottom) dx or dy — e.g. Example 6.1: Finding the Area of a Region between Two Curves 1 If R is the region bounded above by the graph of the function $f (x) = x + 4$ and below by the graph of the function $g (x) = 3…; Example 6.2: Finding the Area of a Region between Two Curves 2 If $R$ is the region bounded above by the graph of the function $f (x) = 9 - (x / 2)^{2}$ and below by the graph of the functio… |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep constructive integral-application builders; optional Integral skeleton for shared definite-integral cores.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `area_between_curves`; limits/differentiation owned by other agent._
