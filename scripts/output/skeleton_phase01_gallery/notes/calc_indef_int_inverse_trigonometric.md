# Notes — `calc_indef_int_inverse_trigonometric`

- **Display name:** Inverse trigonometric
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_inverse_trig`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `integral_inverse_trig`
- **Remaining limits:** Reuse `integrals.py` / FTC / Riemann constructive cores. Gaps: curve families still thin vs OpenStax §5–6 (mostly poly); trig-sub / PFD / multi-trick are catalog-shaped but not full textbook exercise breadth.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice inverse trigonometric.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | pattern=invtrig, form=arctan_basic |
| 0 | 207 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | pattern=invtrig, form=arctan_basic |
| 8 | 101 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | pattern=invtrig, form=arctan_basic |
| 8 | 207 | $\int \frac{1}{\sqrt{16-4x^{2}}}\,dx$ | $\frac{1}{2}\arcsin\left(\frac{2x}{4}\right)+C$ | pattern=invtrig, form=arcsin_scaled |
| 16 | 101 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | pattern=invtrig, form=arctan_basic |
| 16 | 207 | $\int \frac{1}{\sqrt{16-4x^{2}}}\,dx$ | $\frac{1}{2}\arcsin\left(\frac{2x}{4}\right)+C$ | pattern=invtrig, form=arcsin_scaled |
| 22 | 101 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | pattern=invtrig, form=arctan_basic |
| 22 | 207 | $\int \frac{1}{\sqrt{16-4x^{2}}}\,dx$ | $\frac{1}{2}\arcsin\left(\frac{2x}{4}\right)+C$ | pattern=invtrig, form=arcsin_scaled |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.7 | https://openstax.org/books/calculus-volume-1/pages/5-7-integrals-resulting-in-inverse-trigonometric-functions | ∫ 1/√(a²−x²) etc. — e.g. Example 5.49: Evaluating a Definite Integral Using Inverse Trigonometric Functions Evaluate the definite integral $\int_{0}^{\frac{1}{2}} \frac{d x}{\sqrt{1 - x^{2}}} .$; Example 5.50: Finding an Antiderivative Involving an Inverse Trigonometric Function Evaluate the integral $\int \frac{d x}{\sqrt{4 - 9 x^{2}}} .$ |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Reuse `question_engine/frameworks/primitives/integrals.py` + OpenStax form catalogs; harden difficulty via real technique structure (not Diff).
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `integral_inverse_trig`; limits/differentiation owned by other agent._
