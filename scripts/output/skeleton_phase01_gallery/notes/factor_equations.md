# Notes — `factor_equations` (`quadratic_factoring_equations`)

Also covers: `quadratic_factoring_equations`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve a quadratic equation by factoring (zero-product property).
- **D=0:** Monic $x^2+bx+c=0$ already set to zero.
- **High D (≈16–22):** $a\neq 1$; rearrange to $=0$ first; unsimplified stems later. Always degree 2.
- **Must not:** Grouping four-terms; quadratic formula; graphing.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_factor_poly=True`.

- **D=0 seed=101:** $x^{2} + 7x + 12 = 0$ → $x = -4, x = -3$
- **D=0 seed=207:** $x^{2} + 3x + 2 = 0$ → $x = -2, x = -1$
- **D=8 seed=101:** $4x^{2} - 24x + 32 = 0$ → $x = 2, x = 4$
- **D=8 seed=207:** $2x^{2} - 18x + 16 = 0$ → $x = 1, x = 8$
- **D=16 seed=101:** $2\left(-24x + 32\right) + 8x^{2} = 0$ → $x = 2, x = 4$
- **D=16 seed=207:** $-2\left(-x^{2} + 6x - 9\right) = 0$ → $x = 3$
- **D=22 seed=101:** $8x^{2} + 3x^{2} - 3x^{2} + 64 - 48x = 0$ → $x = 2, x = 4$
- **D=22 seed=207:** $-3\left(x^{2} + 1\right) + 3x^{2} + 2x^{2} - 12x + 21 = 0$ → $x = 3$

Opt-out flag used: `use_factor_poly=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $x^{2} + 4x + 3 = 0$ → $x = -3, x = -1$ — form_id=quadratic_equation_factor, pattern=FactorProduct
- **D=0 seed=207:** $x^{2} + 5x + 4 = 0$ → $x = -4, x = -1$ — form_id=quadratic_equation_factor, pattern=FactorProduct
- **D=8 seed=101:** $6x^{2} - 19x + 8 = 0$ → $x = \frac{1}{2}, x = \frac{8}{3}$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct
- **D=8 seed=207:** $9x^{2} - 3x - 2 = 0$ → $x = -\frac{1}{3}, x = \frac{2}{3}$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct
- **D=16 seed=101:** $1 + 191 - 144x + 24x^{2} = 0$ → $x = 2, x = 4$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct
- **D=16 seed=207:** $-12 + 6 - 9x + 6x^{2} = 0$ → $x = -\frac{1}{2}, x = 2$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct
- **D=22 seed=101:** $2\left(12x^{2} - 72x + 96\right) = 0$ → $x = 2, x = 4$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct
- **D=22 seed=207:** $-9 + 1 + 2 - 9x + 6x^{2} = 0$ → $x = -\frac{1}{2}, x = 2$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §7.6 | https://openstax.org/books/elementary-algebra-2e/pages/7-6-quadratic-equations | Set $=0$, factor, zero-product. $x^2+7x+12=0$ then $a\neq 1$. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP. Algebra shapes follow the old path; default is the live skeleton.
Flag UNCLEAR only if old path is a dump stub or the skill is wrong.

## Limitations

- UNCLEAR: gold look not fully locked — keep red gallery header; do not invent a new engine.
- Gallery section slug: `factor_equations` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** FactorProduct solve-by-factoring / poly_skeleton (already wired). Opt-out: `use_factor_poly`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `other`

_Catalog:_ Algebra 1 — Quadratic Functions — Solving equations by factoring. Generator `quadratic_factoring_equations`.
