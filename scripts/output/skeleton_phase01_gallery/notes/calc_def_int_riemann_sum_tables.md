# Notes — `calc_def_int_riemann_sum_tables`

- **Display name:** Riemann sum tables
- **Category:** Calculus — Definite Integration
- **Generator:** `riemann_sum_tables`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `riemann_sum_tables`
- **Remaining limits:** Reuse `integrals.py` / FTC / Riemann constructive cores. Gaps: curve families still thin vs OpenStax §5–6 (mostly poly); trig-sub / PFD / multi-trick are catalog-shaped but not full textbook exercise breadth.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice riemann sum tables.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $f(0)=2, f(1)=5, f(2)=2.\quad\text{Approximate }\int_{0}^{2} f(x)\,dx\text{ with a left Riemann sum.}$ | $7$ | — |
| 0 | 207 | $f(0)=3, f(1)=1, f(2)=5.\quad\text{Approximate }\int_{0}^{2} f(x)\,dx\text{ with a left Riemann sum.}$ | $4$ | — |
| 8 | 101 | $f(0)=1, f(1)=3, f(2)=3.\quad\text{Approximate }\int_{0}^{2} f(x)\,dx\text{ with a left Riemann sum.}$ | $4$ | — |
| 8 | 207 | $f(0)=6, f(1)=2, f(2)=4, f(3)=3.\quad\text{Approximate }\int_{0}^{3} f(x)\,dx\text{ with a left Riemann sum.}$ | $12$ | — |
| 16 | 101 | $f(0)=5, f(1)=4, f(2)=3, f(3)=6.\quad\text{Approximate }\int_{0}^{3} f(x)\,dx\text{ with a right Riemann sum.}$ | $13$ | — |
| 16 | 207 | $f(0)=6, f(1)=3, f(2)=4, f(3)=3.\quad\text{Approximate }\int_{0}^{3} f(x)\,dx\text{ with a left Riemann sum.}$ | $13$ | — |
| 22 | 101 | $\text{On }[0,4]\text{ with }\Delta x=2,\text{ the midpoint values are }f(1)=2\text{ and }f(3)=2.\quad\text{Find the midpoint Riemann sum.}$ | $8$ | — |
| 22 | 207 | $\text{On }[0,4]\text{ with }\Delta x=2,\text{ the midpoint values are }f(1)=5\text{ and }f(3)=3.\quad\text{Find the midpoint Riemann sum.}$ | $16$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.1 | https://openstax.org/books/calculus-volume-1/pages/5-1-approximating-areas | table values → Riemann sum — e.g. Example 5.1: Using Sigma Notation Write in sigma notation and evaluate the sum of terms $3^{i}$ for $i = 1 , 2 , 3 , 4 , 5 .$ Write the sum in sigma notation: $1 + \frac{1}{4} + \frac{1}{9} …; Example 5.2: Evaluation Using Sigma Notation Write using sigma notation and evaluate: The sum of the terms $(i - 3)^{2}$ for $i = 1 , 2 ,\ldots, 200 .$ The sum of the terms $\left(\right. i^… |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep constructive integral-application builders; optional Integral skeleton for shared definite-integral cores.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `riemann_sum_tables`; limits/differentiation owned by other agent._
