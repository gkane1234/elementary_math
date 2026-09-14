# Notes — `poly_add_sub` (`polynomial_add_subtract`)

Also covers: `polynomial_add_subtract`, `pa_polynomials_adding_and_subtracting`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Add or subtract polynomials (combine like terms; distribute a minus).
- **D=0:** Degree 1: $(2x+1)+(x+3)$.
- **High D (≈16–22):** Degree 2–3, then subtract with an inner distribute leftover.
- **Must not:** FactorProduct / multiply polynomials.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_polynomial_add_subtract=True`.

- **D=0 seed=101:** $\text{Simplify: } \left(x^{2} + 2\right) + \left(2x^{2} + 2\right)$ → $3x^{2} + 4$
- **D=0 seed=207:** $\text{Simplify: } \left(2x^{2} + 3\right) + \left(-2x + 1\right)$ → $2x^{2} - 2x + 4$
- **D=8 seed=101:** $\text{Simplify: } \left(2x^{3} + x^{2} + 2\right) + \left(x^{2} + 2\right)$ → $2x^{3} + 2x^{2} + 4$
- **D=8 seed=207:** $\text{Simplify: } \left(x^{3} + 2x^{2} + 2\right) - \left(3x^{3} + 3\right)$ → $-2x^{3} + 2x^{2} - 1$
- **D=16 seed=101:** $\text{Simplify: } \left(3x^{4} + 2x^{3} + x + 4\right) - \left(x^{4} + x^{2} + 1\right)$ → $2x^{4} + 2x^{3} - x^{2} + x + 3$
- **D=16 seed=207:** $\text{Simplify: } \left(x^{4} + 3x^{3} + x - 1\right) + \left(3x^{4} + 3x^{3} + 1\right)$ → $4x^{4} + 6x^{3} + x$
- **D=22 seed=101:** $\text{Simplify: } \left(3x^{4} + 2x^{3} + x + 4\right) - \left(x^{4} + x^{2} + 1\right)$ → $2x^{4} + 2x^{3} - x^{2} + x + 3$
- **D=22 seed=207:** $\text{Simplify: } \left(x^{4} + 3x^{3} + x - 1\right) + \left(3x^{4} + 3x^{3} + 1\right)$ → $4x^{4} + 6x^{3} + x$

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Simplify: } \left(2x + 4\right) + \left(3x + 2\right)$ → $5x + 6$ — form_id=poly_add_sub
- **D=0 seed=207:** $\text{Simplify: } \left(x + 1\right) + \left(2x + 3\right)$ → $3x + 4$ — form_id=poly_add_sub
- **D=8 seed=101:** $\text{Simplify: } \left(x + 2\right) + \left(-2x + 2\right)$ → $-x + 4$ — form_id=poly_add_sub
- **D=8 seed=207:** $\text{Simplify: } \left(2x + 1\right) + \left(3x + 1\right)$ → $5x + 2$ — form_id=poly_add_sub
- **D=16 seed=101:** $\text{Simplify: } \left(3x^{3} + 2x^{2} + x + 4\right) - \left(x^{3} + 3x^{2} + x + 2\right)$ → $2x^{3} - x^{2} + 2$ — form_id=poly_add_sub
- **D=16 seed=207:** $\text{Simplify: } \left(3x^{3} + 3x^{2} - 2x + 1\right) - \left(x^{3} - x^{2} + 3x + 1\right)$ → $2x^{3} + 4x^{2} - 5x$ — form_id=poly_add_sub
- **D=22 seed=101:** $\text{Simplify: } \left(2x^{2} + x + 7 + 3\left(x^{3} - 1\right)\right) - \left(x^{3} + 3x^{2} + x + 2\right)$ → $2x^{3} - x^{2} + 2$ — form_id=poly_add_sub
- **D=22 seed=207:** $\text{Simplify: } \left(-2x + 1 + 3x^{2} + 3x^{3}\right) - \left(x^{3} - x^{2} + 3x + 1\right)$ → $2x^{3} + 4x^{2} - 5x$ — form_id=poly_add_sub

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §6.1** — Add/subtract polynomials; combine like terms — https://openstax.org/books/elementary-algebra-2e/pages/6-1-add-and-subtract-polynomials

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Default D=0 is degree 1 (simpler than old D=0 quadratics). Old D=0 already uses $x^2$. Gold for G6/PA easy is linear; old A1-ish degree 2 at D=0.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** PolyAddSub (already wired). Alias `pa_polynomials_adding_and_subtracting`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `other`
