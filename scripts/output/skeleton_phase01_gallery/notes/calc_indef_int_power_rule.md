# Notes — `calc_indef_int_power_rule`

- **Display name:** Power Rule
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_power_rule`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `integral_power_rule`
- **Remaining limits:** Reuse `integrals.py` / FTC / Riemann constructive cores. Gaps: curve families still thin vs OpenStax §5–6 (mostly poly); trig-sub / PFD / multi-trick are catalog-shaped but not full textbook exercise breadth.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice power rule.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int 3 \, dx$ | $3x+C$ | pattern=power, form=poly_sum |
| 0 | 207 | $\int \sqrt{x}\,dx$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | pattern=power, form=sqrt_x |
| 8 | 101 | $\int -3x^{4} + 3 \, dx$ | $3x-\frac{3}{5}x^{5}+C$ | pattern=power, form=poly_sum |
| 8 | 207 | $\int \frac{x^{2}+5\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+15x^{\frac{1}{3}}+C$ | pattern=power, form=rewrite_over_x |
| 16 | 101 | $\int 6x^{4} + 2 \, dx$ | $2x+\frac{6}{5}x^{5}+C$ | pattern=power, form=poly_sum |
| 16 | 207 | $\int \frac{x^{2}+5\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+15x^{\frac{1}{3}}+C$ | pattern=power, form=rewrite_over_x |
| 22 | 101 | $\int 3x^{4} - 2 \, dx$ | $-2x+\frac{3}{5}x^{5}+C$ | pattern=power, form=poly_sum |
| 22 | 207 | $\int \frac{x^{2}+5\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+15x^{\frac{1}{3}}+C$ | pattern=power, form=rewrite_over_x |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.10 | https://openstax.org/books/calculus-volume-1/pages/4-10-antiderivatives | ∫ x^n dx power rule + C — e.g. Example 4.50: Finding Antiderivatives For each of the following functions, find all antiderivatives. $f (x) = 3 x^{2}$ $f (x) = \frac{1}{x}$ $f (x) = \cos x$ $f (x) = e^{x}$; Example 4.51: Verifying an Indefinite Integral Each of the following statements is of the form $\int f (x) d x = F (x) + C .$ Verify that each statement is correct by showing that $F^{'} (x) … |
| OpenStax Calculus Volume 1 §5.4 | https://openstax.org/books/calculus-volume-1/pages/5-4-integration-formulas-and-the-net-change-theorem | basic antiderivative formulas — e.g. Example 5.23: Integrating a Function Using the Power Rule Use the power rule to integrate the function $\int_{1}^{4} \sqrt{t} (1 + t) d t .$; Example 5.24: Finding Net Displacement Given a velocity function $v (t) = 3 t - 5$ (in meters per second) for a particle in motion from time $t = 0$ to time $t = 3 ,$ find the net displacemen… |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Reuse `question_engine/frameworks/primitives/integrals.py` + OpenStax form catalogs; harden difficulty via real technique structure (not Diff).
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `integral_power_rule`; limits/differentiation owned by other agent._
