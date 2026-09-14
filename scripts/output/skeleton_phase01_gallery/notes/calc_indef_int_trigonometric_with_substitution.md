# Notes — `calc_indef_int_trigonometric_with_substitution`

- **Display name:** Trigonometric substitution
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_trig_substitution`
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Integrate using a trigonometric substitution \(x=a\sin\theta\), \(x=a\tan\theta\), or \(x=a\sec\theta\).
- **D=0:** OpenStax easy \(\int\sqrt{a^{2}-x^{2}}\,dx\) only (old easy).
- **Mid D (≈8):** Unlock \(\sqrt{a^{2}+x^{2}}\) / \(\sqrt{x^{2}-a^{2}}\) and \(1/\sqrt{\,\cdot\,}\).
- **High D (≈16–22):** \(x^{2}/\sqrt{\,\cdot\,}\), \((\,\cdot\,)^{\pm 3/2}\), optional linear wrap \(u=x+b\). Named preset `trig_sub_form_preset=bc_bank`.
- **Must not:** Plain power u-sub \(\int x(x^{2}+1)^{n}\,dx\); frozen bank LaTeX \(\sqrt{9-x^{2}}\); \(\sqrt{a^{2}-x^{2}}/x\) without a closed form; \(x^{3}/\sqrt{\,\cdot\,}\) (u-sub rewrite).

## What old / live path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

**Before this pass** (host auto; high D already catalog-shaped):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \sqrt{4-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{4-x^{2}}+2\arcsin\left(\frac{x}{2}\right)+C$ | form=`sqrt_a2_minus_x2` |
| 0 | 207 | $\int \sqrt{16-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | form=`sqrt_a2_minus_x2` |
| 8 | 101 | $\int \sqrt{4+x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{4+x^{2}}+2\ln\left|x+\sqrt{4+x^{2}}\right|+C$ | form=`sqrt_a2_plus_x2` |
| 16 | 101 | $\int \left(16-\left(x - 3\right)^{2}\right)^{\frac{3}{2}}\,dx$ | wrap + `(a²−x²)^{3/2}` | `u_sub`+`trig_sub` |

**Live now** (`_generate_for_type`). EMH-hard at D≥16 stamps `trig_sub_form_preset=bc_bank`. D=0 still \(\sqrt{a^{2}-x^{2}}\).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \sqrt{4-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{4-x^{2}}+2\arcsin\left(\frac{x}{2}\right)+C$ | `sqrt_a2_minus_x2`, preset=`auto` |
| 0 | 207 | $\int \sqrt{16-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | same family |
| 0 | 313 | $\int \sqrt{9-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)+C$ | lookalike \(a\) varies |
| 8 | 101 | $\int \sqrt{4+x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{4+x^{2}}+2\ln\left|x+\sqrt{4+x^{2}}\right|+C$ | `sqrt_a2_plus_x2` |
| 8 | 207 | $\int \sqrt{16-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | still minus family |
| 16 | 101 | $\int \left(16+\left(x - 3\right)^{2}\right)^{\frac{3}{2}}\,dx$ | $\frac{\left(x - 3\right)}{8}\left(2\left(x - 3\right)^{2}+16\right)\sqrt{16+\left(x - 3\right)^{2}}+\frac{256}{8}\ln\left|x - 3+\sqrt{16+\left(x - 3\right)^{2}}\right|+C$ | wrap + `pow_3_2_a2_plus`; bank preset |
| 16 | 207 | $\int \sqrt{x^{2}-16}\,dx$ | $\frac{1}{2}x\sqrt{x^{2}-16}-8\ln\left|x+\sqrt{x^{2}-16}\right|+C$ | `sqrt_x2_minus_a2` |
| 16 | 313 | $\int \frac{x^{2}}{\sqrt{4-x^{2}}}\,dx$ | $-\frac{1}{2}x\sqrt{4-x^{2}}+2\arcsin\left(\frac{x}{2}\right)+C$ | `x2_over_sqrt_a2_minus_x2` |
| 22 | 207 | $\int \sqrt{x^{2}-16}\,dx$ | $\frac{1}{2}x\sqrt{x^{2}-16}-8\ln\left|x+\sqrt{x^{2}-16}\right|+C$ | not leftover \(\sqrt{a^{2}-x^{2}}\) |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 2 §3.3 | https://openstax.org/books/calculus-volume-2/pages/3-3-trigonometric-substitution | √(a²−x²) sin-sub — e.g. Example 3.21 \(\int\sqrt{9-x^{2}}\,dx\); Example 3.24 \(1/\sqrt{x^{2}+a^{2}}\); Checkpoint-style \(x^{2}/\sqrt{a^{2}-x^{2}}\). Example 3.22 \(\sqrt{4-x^{2}}/x\) stays deferred (no closed template). |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-2/` · `question_engine/frameworks/primitives/openstax_form_catalogs/trig_substitution.json`.

Catalog forms (implemented lookalikes, not frozen bank coeffs): `sqrt_a2_minus_x2` (D=0), `sqrt_a2_plus_x2`, `sqrt_x2_minus_a2`, `one_over_sqrt_x2_plus_a2` / `_minus_a2`, `x2_over_sqrt_a2_minus_x2` / `_x2_plus_a2` / `_x2_minus_a2`, `pow_3_2_*`, `pow_m3_2_a2_plus` / `_a2_minus` / `_x2_minus`. Named preset `trig_sub_form_preset=bc_bank`.

## Variety notes

Not a WP. D=0 one easy OpenStax frame. Mid/high D rotate §3.3 / BC §5 algebraic radicals. Coefficients vary (`a=2,3,4,…`) — not a frozen \(\sqrt{9-x^{2}}\) bank copy.

## Limitations

- **Status:** shipped — catalog lookalikes + `trig_sub_form_preset=bc_bank`. Remaining `LIMITATIONS`: \(\int\sqrt{a^{2}-x^{2}}/x\,dx\) (`sqrt_over_x_a2_minus`) stub — no honest ln+sqrt template; \(\int x/\sqrt{x^{2}-a^{2}}\) and \(\int x^{3}/\sqrt{x^{2}\pm a^{2}}\) deferred (u-sub / rewrite, wrong leaf); \(\int 1/\sqrt{a^{2}-x^{2}}\) deferred (arcsin table on the invtrig leaf); hyperbolic \(x=\sinh\theta\) deferred.
- **Generator:** `integral_trig_substitution`

## Proposed engine (reuse vs new)

- **Reuse:** `integrals.py` `_sample_trig_sub` + `trig_substitution.json`. Numeric hardness is \(a\), fractional power, \(x^{2}\) numerator, and optional \(u=x+b\) wrap — not padded `difficulty_costs`.
- **Shipped this pass:** BC bank §5 lookalikes on the existing sampler (`x^{2}/\sqrt{x^{2}\pm a^{2}}\), \((x^{2}-a^{2})^{-3/2}\)); named preset `bc_bank`; `requires_allows: allow_trig_sub`.
