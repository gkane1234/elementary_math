# Notes — `calc_indef_int_inverse_trigonometric_with_substitution`

- **Display name:** Inverse trigonometric with substitution
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_invtrig_substitution`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `integral_invtrig_substitution`
- **Remaining limits:** Catalog `arctan_of_linear` at D=0–8; reverse-chain `invtrig_arctan` / `invtrig_arcsin` at D≥16 (affine/quad inner, no nested arctan∘arctan). Gaps: Diff AST latex; flavor still mixes `power_linear_du` if construction is catalog-only at mid D.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice inverse trigonometric with substitution.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{2}{1+(2x + 2)^{2}}\,dx$ | $\arctan(2x + 2)+C$ | catalog `arctan_of_linear` |
| 0 | 207 | $\int \frac{2}{1+(2x + 2)^{2}}\,dx$ | $\arctan(2x + 2)+C$ | catalog `arctan_of_linear` |
| 8 | 101 | $\int \frac{3}{1+(3x + 4)^{2}}\,dx$ | $\arctan(3x + 4)+C$ | catalog `arctan_of_linear` |
| 8 | 207 | $\int \frac{4}{1+(4x + 3)^{2}}\,dx$ | $\arctan(4x + 3)+C$ | catalog `arctan_of_linear` |
| 16 | 101 | $\int \frac{1}{1+(-5x^{2} + 2x + 3)^{2}}\left(2x^{1}\left(-5\right) + 2\right)\,dx$ | $\arctan\left(-5x^{2} + 2x + 3\right)+C$ | reverse-chain `invtrig_arctan` |
| 16 | 207 | $\int \frac{1}{\sqrt{1-(-5x - 4)^{2}}}\,dx$ | $-\frac{1}{5}\arcsin\left(-5x - 4\right)+C$ | reverse-chain `invtrig_arcsin` |
| 22 | 101 | $\int \frac{1}{1+(-5x^{2} + 2x + 3)^{2}}\left(2x^{1}\left(-5\right) + 2\right)\,dx$ | $\arctan\left(-5x^{2} + 2x + 3\right)+C$ | reverse-chain `invtrig_arctan` |
| 22 | 207 | $\int \frac{1}{\sqrt{1-(-5x - 4)^{2}}}\,dx$ | $-\frac{1}{5}\arcsin\left(-5x - 4\right)+C$ | reverse-chain `invtrig_arcsin` |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.5 | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | u-sub into invtrig forms — e.g. Example 5.30: Using Substitution to Find an Antiderivative Use substitution to find the antiderivative $\int 6 x \left(\right. 3 x^{2} + 4 \left.\right)^{4} d x .$; Example 5.31: Using Substitution with Alteration Use substitution to find $\int z \sqrt{z^{2} - 5} d z .$ |
| OpenStax Calculus Volume 1 §5.7 | https://openstax.org/books/calculus-volume-1/pages/5-7-integrals-resulting-in-inverse-trigonometric-functions | invtrig antiderivative after sub — e.g. Example 5.49: Evaluating a Definite Integral Using Inverse Trigonometric Functions Evaluate the definite integral $\int_{0}^{\frac{1}{2}} \frac{d x}{\sqrt{1 - x^{2}}} .$; Example 5.50: Finding an Antiderivative Involving an Inverse Trigonometric Function Evaluate the integral $\int \frac{d x}{\sqrt{4 - 9 x^{2}}} .$ |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Reuse `question_engine/frameworks/primitives/integrals.py` + OpenStax form catalogs; harden difficulty via real technique structure (not Diff).
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `integral_invtrig_substitution`; limits/differentiation owned by other agent._
