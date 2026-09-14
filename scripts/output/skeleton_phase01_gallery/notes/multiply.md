# Notes — `multiply` (`polynomial_multiply`)

Also covers: `polynomial_multiply`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Multiply polynomials (distribute / FOIL) and write the expanded product.
- **D=0:** Monomial×binomial or two linear binomials.
- **High D (≈16–22):** Binomial×trinomial; larger coeffs. Special-product identities stay on the special-multiply leaf.
- **Must not:** Factoring prompts; PolyAddSub.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_factor_poly=True`.

- **D=0 seed=101:** $\text{Multiply: } \left(-x - 3\right)\left(x\right)$ → $-x^{2} - 3x$
- **D=0 seed=207:** $\text{Multiply: } \left(x + 1\right)\left(x + 3\right)$ → $x^{2} + 4x + 3$
- **D=8 seed=101:** $\text{Multiply: } \left(2x^{2} + x + 2\right)\left(-x\right)$ → $-2x^{3} - x^{2} - 2x$
- **D=8 seed=207:** $\text{Multiply: } \left(x^{2} + 3\right)\left(-2x + 1\right)$ → $-2x^{3} + x^{2} - 6x + 3$
- **D=16 seed=101:** $\text{Multiply: } \left(4x^{2} + 2x + 4\right)\left(x^{2}\right)$ → $4x^{4} + 2x^{3} + 4x^{2}$
- **D=16 seed=207:** $\text{Multiply: } \left(x^{2} + 3\right)\left(2x + 1\right)$ → $2x^{3} + x^{2} + 6x + 3$
- **D=22 seed=101:** $\text{Multiply: } \left(4x^{2} + 2x + 4\right)\left(x^{2}\right)$ → $4x^{4} + 2x^{3} + 4x^{2}$
- **D=22 seed=207:** $\text{Multiply: } \left(x^{2} + 3\right)\left(2x + 1\right)$ → $2x^{3} + x^{2} + 6x + 3$

Opt-out flag used: `use_factor_poly=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Multiply: } x^{2}\left(x + 3\right)$ → $x^{3} + 3x^{2}$ — form_id=mono_times_poly, pattern=FactorProduct
- **D=0 seed=207:** $\text{Multiply: } 4x^{2}\left(x - 4\right)$ → $4x^{3} - 16x^{2}$ — form_id=mono_times_poly, pattern=FactorProduct
- **D=8 seed=101:** $\text{Multiply: } 5x^{2}\left(x - 3\right)$ → $5x^{3} - 15x^{2}$ — form_id=mono_times_poly, pattern=FactorProduct
- **D=8 seed=207:** $\text{Multiply: } 4x^{2}\left(x - 1\right)$ → $4x^{3} - 4x^{2}$ — form_id=mono_times_poly, pattern=FactorProduct
- **D=16 seed=101:** $\text{Multiply: } 5x^{2}\left(x - 4\right)$ → $5x^{3} - 20x^{2}$ — form_id=binomial_times_binomial, pattern=FactorProduct
- **D=16 seed=207:** $\text{Multiply: } 5x^{2}\left(3x + 8\right)$ → $15x^{3} + 40x^{2}$ — form_id=binomial_times_binomial, pattern=FactorProduct
- **D=22 seed=101:** $\text{Multiply: } \left(3x - 11\right)\left(x - 1\right)\left(2x - 1\right)$ → $6x^{3} - 31x^{2} + 36x - 11$ — form_id=binomial_times_binomial, pattern=FactorProduct
- **D=22 seed=207:** $\text{Multiply: } \left(3x + 2\right)\left(x - 1\right)\left(2x + 9\right)$ → $6x^{3} + 25x^{2} - 13x - 18$ — form_id=binomial_times_binomial, pattern=FactorProduct

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §6.3 | https://openstax.org/books/elementary-algebra-2e/pages/6-3-multiply-polynomials | Monomial×poly; FOIL two binomials; then (binomial)(trinomial). |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP. Algebra shapes follow the old path; default is the live skeleton.
Flag UNCLEAR only if old path is a dump stub or the skill is wrong.

## Limitations

- UNCLEAR: gold look not fully locked — keep red gallery header; do not invent a new engine.
- Gallery section slug: `multiply` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** FactorProduct multiply task / poly_skeleton (already wired). Opt-out: `use_factor_poly`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `other`

_Catalog:_ Algebra 1 — Polynomials — Multiplying. Generator `polynomial_multiply`.
