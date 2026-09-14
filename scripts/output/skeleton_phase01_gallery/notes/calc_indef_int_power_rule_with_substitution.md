# Notes — `calc_indef_int_power_rule_with_substitution`

- **Display name:** Power rule with substitution
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_substitution`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `integral_substitution`
- **Remaining limits:** Named `u_sub_form_preset` families (from `u_substitution.json`) and reverse-chain (`expr_skeleton` Diff → integrand \(F'(g)g'\)) are live. `power_cubic_x2_du` (OpenStax Checkpoint 5.25/5.26) is now in the power flavor and the `challenging` preset. Reverse-chain elides Diff AST `x^{1}` on this consumer. Gaps: reverse-chain still shows unsimplified juxtaposition (`2x(-4)`); `challenging` on this leaf stays algebraic (cubic / root-quad / alteration) — trig/exp challenging lives on the ln/exp host; BC bank §1 algebraic families (`power_quad_neg`, …) unlock via `bc_bank` / mid-high D, not D=0; OpenStax §5.5 exercise breadth is still not the full textbook set.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice power rule with substitution.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int 2\left(2x + 2\right)^{2}\,dx$ | $\frac{1}{3}\left(2x + 2\right)^{3}+C$ | catalog `power_linear_du` |
| 0 | 207 | $\int 2\left(2x + 2\right)^{2}\,dx$ | $\frac{1}{3}\left(2x + 2\right)^{3}+C$ | catalog `power_linear_du` |
| 8 | 101 | $\int 3\left(3x + 4\right)^{2}\,dx$ | $\frac{1}{3}\left(3x + 4\right)^{3}+C$ | catalog `power_linear_du` |
| 8 | 207 | $\int \frac{2x+1}{x^{2}+x+2}\,dx$ | $\ln|x^{2}+x+2|+C$ | catalog `du_over_u_quadratic` (BC bank §1.17) |
| 16 | 101 | $\int 2x\left(x^{2}+9\right)^{2}\,dx$ | $\frac{1}{3}\left(x^{2}+9\right)^{3}+C$ | catalog `power_quad_x_du` |
| 16 | 207 | $\int \frac{x^{5}}{\left(x^{6}+2\right)^{4}}\,dx$ | $-\frac{1}{18\left(x^{6}+2\right)^{3}}+C$ | catalog `power_hex_neg` (BC bank §1.24) |
| 22 | 101 | $\int 2x\left(x^{2}+1\right)^{4}\,dx$ | $\frac{1}{5}\left(x^{2}+1\right)^{5}+C$ | catalog `power_quad_x_du` |
| 22 | 207 | $\int \frac{x^{5}}{\left(x^{6}+6\right)^{2}}\,dx$ | $-\frac{1}{6\left(x^{6}+6\right)}+C$ | catalog `power_hex_neg` |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.5 | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | u-sub on power compositions — e.g. Example 5.30: Using Substitution to Find an Antiderivative Use substitution to find the antiderivative $\int 6 x \left(\right. 3 x^{2} + 4 \left.\right)^{4} d x .$; Example 5.31: Using Substitution with Alteration Use substitution to find $\int z \sqrt{z^{2} - 5} d z .$ |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Reuse `integrals.py` + `u_substitution.json` form presets; reverse-chain via Diff `expr_skeleton` (`sample_reverse_chain_integral`).
- **Presets:** `auto` / `power_linear` / `power_quadratic` / `challenging` / … on `u_sub_form_preset`; `u_sub_construction` = `auto` | `catalog` | `reverse_chain`.
- **Reuse Diff?** Yes — only as reverse chain (sample F∘g, prompt is F′).

_Catalog generator `integral_substitution`; limits/differentiation owned by other agent._
