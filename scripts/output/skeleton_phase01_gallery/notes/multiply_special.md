# Notes — `multiply_special` (`polynomial_multiply_special`)

Also covers: `polynomial_multiply_special`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Multiply special products: $(a\pm b)^2$ and difference of squares.
- **D=0:** $(x\pm b)^2$ or $(x-a)(x+a)$ with small ints.
- **High D (≈16–22):** $(ax\pm b)^2$; larger coeffs. Keep the identity visible — not a generic FOIL mixer.
- **Must not:** Generic multiply; factoring the result as the prompt.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_factor_poly=True`.

- **D=0 seed=101:** $\text{Multiply: } \left(x + 1\right)\left(x - 1\right)$ → $x^{2} - 1$
- **D=0 seed=207:** $\text{Multiply: } \left(x + 3\right)\left(x - 3\right)$ → $x^{2} - 9$
- **D=8 seed=101:** $\text{Multiply: } \left(3x + 3\right)\left(3x - 3\right)$ → $9x^{2} - 9$
- **D=8 seed=207:** $\text{Multiply: } \left(2x + 1\right)\left(2x - 1\right)$ → $4x^{2} - 1$
- **D=16 seed=101:** $\text{Multiply: } \left(2x + 4\right)^{2}$ → $4x^{2} + 16x + 16$
- **D=16 seed=207:** $\text{Multiply: } \left(2x + 1\right)\left(2x - 1\right)$ → $4x^{2} - 1$
- **D=22 seed=101:** $\text{Multiply: } \left(2x + 4\right)^{2}$ → $4x^{2} + 16x + 16$
- **D=22 seed=207:** $\text{Multiply: } \left(2x + 1\right)\left(2x - 1\right)$ → $4x^{2} - 1$

Opt-out flag used: `use_factor_poly=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Multiply: } \left(x + 4\right)^{2}$ → $x^{2} + 8x + 16$ — form_id=special_product_square, pattern=FactorProduct
- **D=0 seed=207:** $\text{Multiply: } \left(x + 3\right)^{2}$ → $x^{2} + 6x + 9$ — form_id=special_product_square, pattern=FactorProduct
- **D=8 seed=101:** $\text{Multiply: } \left(x + 8\right)^{2}$ → $x^{2} + 16x + 64$ — form_id=special_product_square, pattern=FactorProduct
- **D=8 seed=207:** $\text{Multiply: } \left(x + 6\right)^{2}$ → $x^{2} + 12x + 36$ — form_id=special_product_square, pattern=FactorProduct
- **D=16 seed=101:** $\text{Multiply: } 5x^{2}\left(x - 4\right)$ → $5x^{3} - 20x^{2}$ — form_id=special_product_square, pattern=FactorProduct
- **D=16 seed=207:** $\text{Multiply: } 5x^{2}\left(3x + 8\right)$ → $15x^{3} + 40x^{2}$ — form_id=special_product_square, pattern=FactorProduct
- **D=22 seed=101:** $\text{Multiply: } \left(3x - 11\right)\left(x - 1\right)\left(2x - 1\right)$ → $6x^{3} - 31x^{2} + 36x - 11$ — form_id=special_product_square, pattern=FactorProduct
- **D=22 seed=207:** $\text{Multiply: } \left(3x + 2\right)\left(x - 1\right)\left(2x + 9\right)$ → $6x^{3} + 25x^{2} - 13x - 18$ — form_id=special_product_square, pattern=FactorProduct

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §6.4 | https://openstax.org/books/elementary-algebra-2e/pages/6-4-special-products | $(a+b)^2$, $(a-b)^2$, $(a-b)(a+b)$. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP. Algebra shapes follow the old path; default is the live skeleton.
Flag UNCLEAR only if old path is a dump stub or the skill is wrong.

## Limitations

- UNCLEAR: gold look not fully locked — keep red gallery header; do not invent a new engine.
- Gallery section slug: `multiply_special` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** FactorProduct special multiply / poly_skeleton (already wired). Opt-out: `use_factor_poly`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `other`

_Catalog:_ Algebra 1 — Polynomials — Multiplying special cases. Generator `polynomial_multiply_special`.
