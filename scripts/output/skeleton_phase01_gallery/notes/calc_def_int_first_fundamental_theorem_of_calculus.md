# Notes — `calc_def_int_first_fundamental_theorem_of_calculus`

- **Display name:** First Fundamental Theorem of Calculus
- **Category:** Calculus — Definite Integration
- **Generator:** `first_fundamental_theorem`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `first_fundamental_theorem`
- **Remaining limits:** Reuse `integrals.py` / FTC / Riemann constructive cores. Gaps: curve families still thin vs OpenStax §5–6 (mostly poly); trig-sub / PFD / multi-trick are catalog-shaped but not full textbook exercise breadth.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice first fundamental theorem of calculus.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int_{0}^{2} 3x^{2}\,dx$ | $8$ | pattern=ftc, form=quad |
| 0 | 207 | $\int_{0}^{4} x\,dx$ | $8$ | pattern=ftc, form=linear |
| 8 | 101 | $\int_{0}^{2} 3x^{2}\,dx$ | $8$ | pattern=ftc, form=quad |
| 8 | 207 | $\int_{0}^{4} x\,dx$ | $8$ | pattern=ftc, form=linear |
| 16 | 101 | $\int_{0}^{2} 3x^{2}\,dx$ | $8$ | pattern=ftc, form=quad |
| 16 | 207 | $\int_{0}^{4} x\,dx$ | $8$ | pattern=ftc, form=linear |
| 22 | 101 | $\int_{0}^{2} 3x^{2}\,dx$ | $8$ | pattern=ftc, form=quad |
| 22 | 207 | $\int_{0}^{4} x\,dx$ | $8$ | pattern=ftc, form=linear |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.3 | https://openstax.org/books/calculus-volume-1/pages/5-3-the-fundamental-theorem-of-calculus | d/dx ∫_a^{g(x)} f = f(g(x)) g'(x) — e.g. Example 5.15: Finding the Average Value of a Function Find the average value of the function $f (x) = 8 - 2 x$ over the interval $\left[\right. 0 , 4 \left]\right.$ and find c such that $f (c…; Example 5.16: Finding the Point Where a Function Takes on Its Average Value Given $\int_{0}^{3} x^{2} d x = 9 ,$ find c such that $f (c)$ equals the average value of $f (x) = x^{2}$ over $\le… |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Reuse `question_engine/frameworks/primitives/integrals.py` + OpenStax form catalogs; harden difficulty via real technique structure (not Diff).
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `first_fundamental_theorem`; limits/differentiation owned by other agent._
