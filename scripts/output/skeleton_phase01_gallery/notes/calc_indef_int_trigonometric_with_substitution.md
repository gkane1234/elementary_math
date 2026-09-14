# Notes — `calc_indef_int_trigonometric_with_substitution`

- **Display name:** Trigonometric substitution
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_trig_substitution`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `integral_trig_substitution`
- **Remaining limits:** Reuse `integrals.py` / FTC / Riemann constructive cores. Gaps: curve families still thin vs OpenStax §5–6 (mostly poly); trig-sub / PFD / multi-trick are catalog-shaped but not full textbook exercise breadth.

## What the question should look like (D=0 vs high D)

- **Skill:** Integrate using a trigonometric substitution.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \sqrt{4-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{4-x^{2}}+2\arcsin\left(\frac{x}{2}\right)+C$ | pattern=trig_sub, form=sqrt_a2_minus_x2 |
| 0 | 207 | $\int \sqrt{16-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | pattern=trig_sub, form=sqrt_a2_minus_x2 |
| 8 | 101 | $\int \sqrt{4+x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{4+x^{2}}+2\ln\left|x+\sqrt{4+x^{2}}\right|+C$ | pattern=trig_sub, form=sqrt_a2_plus_x2 |
| 8 | 207 | $\int \sqrt{16-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | pattern=trig_sub, form=sqrt_a2_minus_x2 |
| 16 | 101 | $\int \left(16-\left(x - 3\right)^{2}\right)^{\frac{3}{2}}\,dx$ | $\frac{\left(x - 3\right)}{8}\left(2\left(x - 3\right)^{2}+16\right)\sqrt{16-\left(x - 3\right)^{2}}+\frac{256}{8}\arcsin\left(\frac{x - 3}{4}\right)+C$ | pattern=u_sub+trig_sub, form=pow_3_2_a2_minus |
| 16 | 207 | $\int \sqrt{16+x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{16+x^{2}}+8\ln\left|x+\sqrt{16+x^{2}}\right|+C$ | pattern=trig_sub, form=sqrt_a2_plus_x2 |
| 22 | 101 | $\int \left(16-\left(x - 3\right)^{2}\right)^{\frac{3}{2}}\,dx$ | $\frac{\left(x - 3\right)}{8}\left(2\left(x - 3\right)^{2}+16\right)\sqrt{16-\left(x - 3\right)^{2}}+\frac{256}{8}\arcsin\left(\frac{x - 3}{4}\right)+C$ | pattern=u_sub+trig_sub, form=pow_3_2_a2_minus |
| 22 | 207 | $\int \sqrt{16+x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{16+x^{2}}+8\ln\left|x+\sqrt{16+x^{2}}\right|+C$ | pattern=trig_sub, form=sqrt_a2_plus_x2 |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 2 §3.3 | https://openstax.org/books/calculus-volume-2/pages/3-3-trigonometric-substitution | √(a²±x²) trig sub — e.g. Example 3.21: Integrating an Expression Involving $\sqrt{a^{2} - x^{2}}$ Evaluate $\int^{​} \sqrt{9 - x^{2}} d x .$; Example 3.22: Integrating an Expression Involving $\sqrt{a^{2} - x^{2}}$ Evaluate $\int \frac{\sqrt{4 - x^{2}}}{x} d x .$ |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.
Note: Catalog name says trig substitution; generator is `integral_trig_substitution` (Calc 2 §3.3).

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Reuse `integrals.py` / OpenStax trig-sub form catalog.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `integral_trig_substitution`; limits/differentiation owned by other agent._
