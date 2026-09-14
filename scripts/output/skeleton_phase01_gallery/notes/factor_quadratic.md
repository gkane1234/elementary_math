# Notes — `factor_quadratic` (`quadratic_factoring`)

Also covers: `quadratic_factoring`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Factor a quadratic trinomial.
- **D=0:** Monic $x^2+bx+c$ with small factor pairs.
- **High D (≈16–22):** $a\neq 1$ (ac method); unsimplified stems later. Always degree 2.
- **Must not:** Four-term grouping; solve-by-factoring equations (that is `quadratic_factoring_equations`).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_factor_poly=True`.

- **D=0 seed=101:** $x^{2} + 6x + 8$ → $\left(x + 4\right)\left(x + 2\right)$ — form_id=trinomial_x2_bx_c
- **D=0 seed=207:** $x^{2} + 4x + 3$ → $\left(x + 1\right)\left(x + 3\right)$ — form_id=trinomial_x2_bx_c
- **D=8 seed=101:** $x^{2} + 2x - 8$ → $\left(x + 4\right)\left(x - 2\right)$ — form_id=trinomial_x2_bx_c
- **D=8 seed=207:** $x^{2} - 3x + 2$ → $\left(x - 1\right)\left(x - 2\right)$ — form_id=trinomial_x2_bx_c
- **D=16 seed=101:** $2\left(-28x + 32\right) + 12x^{2}$ → $4\left(x - 2\right)\left(3x - 8\right)$ — form_id=trinomial_ax2_bx_c
- **D=16 seed=207:** $-x^{2} + 3x^{2} + 12 - 14x$ → $2\left(x - 6\right)\left(x - 1\right)$ — form_id=trinomial_ax2_bx_c
- **D=22 seed=101:** $-2\left(-6x^{2}\right) + 64 - 56x$ → $4\left(x - 2\right)\left(3x - 8\right)$ — form_id=trinomial_ax2_bx_c
- **D=22 seed=207:** $5x + 7 - 2\left(x + 2\right) - 17x + 9 + 2x^{2}$ → $2\left(x - 6\right)\left(x - 1\right)$ — form_id=trinomial_ax2_bx_c

Opt-out flag used: `use_factor_poly=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $x^{2} - 4$ → $\left(x - 2\right)\left(x + 2\right)$ — form_id=trinomial_x2_bx_c, pattern=FactorProduct
- **D=0 seed=207:** $x^{2} - 2x - 15$ → $\left(x + 3\right)\left(x - 5\right)$ — form_id=trinomial_x2_bx_c, pattern=FactorProduct
- **D=8 seed=101:** $x^{2} - 16$ → $\left(x - 4\right)\left(x + 4\right)$ — form_id=trinomial_x2_bx_c, pattern=FactorProduct
- **D=8 seed=207:** $x^{2} - 2x - 63$ → $\left(x + 7\right)\left(x - 9\right)$ — form_id=trinomial_x2_bx_c, pattern=FactorProduct
- **D=16 seed=101:** $3x^{2} - 16x + 13$ → $\left(3x - 13\right)\left(x - 1\right)$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct
- **D=16 seed=207:** $2x^{2} - 15x + 13$ → $\left(2x - 13\right)\left(x - 1\right)$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct
- **D=22 seed=101:** $-16x + 13 - 2x^{2} + 5x^{2}$ → $\left(3x - 13\right)\left(x - 1\right)$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct
- **D=22 seed=207:** $-x - 4 - 2x^{2} + 5x^{2}$ → $\left(x + 1\right)\left(3x - 4\right)$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §7.2 | https://openstax.org/books/elementary-algebra-2e/pages/7-2-factor-trinomials-of-the-form-x2-bx-c | $x^2+bx+c$ with $a=1$. |
| OpenStax Elementary Algebra 2e §7.3 | https://openstax.org/books/elementary-algebra-2e/pages/7-3-factor-trinomials-of-the-form-ax2-bx-c | $ax^2+bx+c$ with $a\neq 1$. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP. Algebra shapes follow the old path; default is the live skeleton.
Flag UNCLEAR only if old path is a dump stub or the skill is wrong.

## Limitations

- UNCLEAR: gold look not fully locked — keep red gallery header; do not invent a new engine.
- Gallery section slug: `factor_quadratic` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** FactorProduct quadratic / poly_skeleton (already wired). Opt-out: `use_factor_poly`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `other`

_Catalog:_ Algebra 1 — Polynomials — Quadratic expressions. Generator `quadratic_factoring`.
