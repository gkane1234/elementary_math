# Notes — `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`

- **Display name:** Logarithmic rule and exponentials with subs.
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_log_exp_substitution`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `integral_log_exp_substitution`
- **Remaining limits:** Named presets + reverse-chain live. `exp_of_cubic` / `exp_of_quartic` / `exp_root_chain` / `exp_power_of_exp` (OpenStax §5.6 Examples 5.38–5.39 / Checkpoints 5.32–5.33) are in the ln/exp flavor and `challenging`. Reverse-chain elides `x^{1}`. Gaps: du/u trig at D=0 is still a bit ahead of “linear only”; BC bank §1 ln/exp families (`ln_power_over_x`, `exp_over_power_of_exp`, nested ln) unlock via `bc_bank` / mid-high D; high-D reverse-chain nested F∘g can be richer than §5.6 drills.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice logarithmic rule and exponentials with subs..
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{2}{2x + 2}\,dx$ | $\ln|2x + 2|+C$ | catalog `du_over_u_linear` |
| 0 | 207 | $\int \frac{\sin(x)}{\cos^{3}(x)}\,dx$ | $\frac{1}{2}\sec^{2}(x)+C$ | catalog `du_over_u_trig` |
| 8 | 101 | $\int \frac{3}{3x + 4}\,dx$ | $\ln|3x + 4|+C$ | catalog `du_over_u_linear` |
| 8 | 207 | $\int 2x^{3}e^{-2x^{4}}\,dx$ | $-\frac{1}{4}e^{-2x^{4}}+C$ | catalog `exp_of_quartic` (Checkpoint 5.33 family) |
| 16 | 101 | $\int \frac{\sin(x)}{\cos^{3}(x)}\,dx$ | $\frac{1}{2}\sec^{2}(x)+C$ | catalog `du_over_u_trig` |
| 16 | 207 | $\int \frac{e^{\sqrt{x}}}{\sqrt{x}}\,dx$ | $2e^{\sqrt{x}}+C$ | catalog `exp_of_sqrt` (BC bank §1.21) |
| 22 | 101 | $\int \frac{\cos(x)}{\sin^{2}(x)}\,dx$ | $-\frac{1}{\sin(x)}+C$ | catalog `du_over_u_trig` |
| 22 | 207 | $\int \frac{e^{\sqrt{x}}}{\sqrt{x}}\,dx$ | $2e^{\sqrt{x}}+C$ | catalog `exp_of_sqrt` |

Exact OpenStax Checkpoint 5.33 (`exp_chain`, D=8, seed=4): $\int 2x^{3}e^{x^{4}}\,dx$ → $\frac{1}{2}e^{x^{4}}+C$. High format (D≥16) omits the 2: $\int x^{3}e^{x^{4}}\,dx$ → $\frac{1}{4}e^{x^{4}}+C$.

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.5 | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | u-sub into ln/exp forms — e.g. Example 5.30: Using Substitution to Find an Antiderivative Use substitution to find the antiderivative $\int 6 x \left(\right. 3 x^{2} + 4 \left.\right)^{4} d x .$; Example 5.31: Using Substitution with Alteration Use substitution to find $\int z \sqrt{z^{2} - 5} d z .$ |
| OpenStax Calculus Volume 1 §5.6 | https://openstax.org/books/calculus-volume-1/pages/5-6-integrals-involving-exponential-and-logarithmic-functions | ln/exp after sub — e.g. Example 5.38 ∫ e^x √(1+e^x); Example 5.39 ∫ 3x² e^{2x³}; Checkpoint 5.33 ∫ 2x³ e^{x⁴}. |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Reuse `integrals.py` + `u_substitution.json` presets (`exp_chain`, `du_over_u`, `challenging`); reverse-chain for nested e^{g}g' when `u_sub_construction=reverse_chain`.

_Catalog generator `integral_log_exp_substitution`; limits/differentiation owned by other agent._
