# Notes — `calc_indef_int_logarithmic_rule_and_exponentials`

- **Display name:** Logarithmic Rule and Exponentials
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_log_exp`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `integral_log_exp`
- **Remaining limits:** Reuse `integrals.py` / FTC / Riemann constructive cores. Gaps: curve families still thin vs OpenStax §5–6 (mostly poly); trig-sub / PFD / multi-trick are catalog-shaped but not full textbook exercise breadth.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice logarithmic rule and exponentials.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{3}{3x + 3}\,dx$ | $\ln|3x + 3|+C$ | pattern=ln_exp, form=ln_linear |
| 0 | 207 | $\int 3^{x}\,dx$ | $\frac{3^{x}}{\ln 3}+C$ | pattern=ln_exp, form=base_a |
| 8 | 101 | $\int \frac{3}{3x + 3}\,dx$ | $\ln|3x + 3|+C$ | pattern=ln_exp, form=ln_linear |
| 8 | 207 | $\int 3^{x}\,dx$ | $\frac{3^{x}}{\ln 3}+C$ | pattern=ln_exp, form=base_a |
| 16 | 101 | $\int \frac{3}{3x + 2}\,dx$ | $\ln|3x + 2|+C$ | pattern=ln_exp, form=ln_linear |
| 16 | 207 | $\int 3^{x}\,dx$ | $\frac{3^{x}}{\ln 3}+C$ | pattern=ln_exp, form=base_a |
| 22 | 101 | $\int \frac{3}{3x - 2}\,dx$ | $\ln|3x - 2|+C$ | pattern=ln_exp, form=ln_linear |
| 22 | 207 | $\int 3^{x}\,dx$ | $\frac{3^{x}}{\ln 3}+C$ | pattern=ln_exp, form=base_a |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.6 | https://openstax.org/books/calculus-volume-1/pages/5-6-integrals-involving-exponential-and-logarithmic-functions | ∫ e^{kx}, ∫ 1/x — e.g. Example 5.37: Finding an Antiderivative of an Exponential Function Find the antiderivative of the exponential function e − x .; Example 5.38: Square Root of an Exponential Function Find the antiderivative of the exponential function $e^{x} \sqrt{1 + e^{x}} .$ |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Reuse `question_engine/frameworks/primitives/integrals.py` + OpenStax form catalogs; harden difficulty via real technique structure (not Diff).
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `integral_log_exp`; limits/differentiation owned by other agent._
