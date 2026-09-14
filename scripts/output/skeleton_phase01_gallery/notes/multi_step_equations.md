# Notes — `multi_step` (`multi_step_equations`)

Also covers: `multi_step_equations`, `pa_equations_multi_step_equations`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve a multi-step linear equation (distribute and/or variables both sides).
- **D=0:** One extra structure: $2(x+1)=8$ **or** $3x+2=x+8$ — not nested junk.
- **High D (≈16–22):** Both distribute and both-sides; nested leftover later (D≈22).
- **Must not:** D=0 already a 6-paren nest (old path).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_equation=True`.

- **D=0 seed=101:** $5 + 2\left(x - 2\right) = 11x + 4 - 3\left(x + 1\right)$ → $x = 0$ — steps=multi
- **D=0 seed=207:** $3x - 3 + \left(x - 3\right)\left(-2\right) = 7x + 17 + \left(x + 1\right)\left(-2\right)$ → $x = -3$ — steps=multi
- **D=8 seed=101:** $4x + 3 - 2 * \left(x + 1\right) = -11 + 2 * \left(2x + 2\right)$ → $x = 4$ — steps=multi
- **D=8 seed=207:** $-2x + 6 + \left(x - 1\right) * 3 = 9x + 57 + \left(x - 3\right) * (-2)$ → $x = -10$ — steps=multi
- **D=16 seed=101:** $4x + 1 + 2 * \left(-x + 1\right) + \left(-x - 2 - 2 * \left(x - 1\right)\right) = 3x + 3 + 2 * \left(-x - 2\right) + \left(-2x + 2 * \left(x - 10\right)\right)$ → $x = 12$ — steps=multi
- **D=16 seed=207:** $-2\left(x + 3\right) + 4x + 9 + \left(3\left(x + 1\right) - 4x - 4\right) = 2\left(x - 1\right) - 3x + 5 + \left(-3x - 81\right)$ → $x = -16$ — steps=multi
- **D=22 seed=101:** $-7x - 12 + 4\left(x + 3\right) + \left(-2\left(x + 1\right)\right) + \left(-4x - 7 + 4\left(2x + 3\right)\right) = 10x - 28 - 4\left(x - 3\right) + \left(-5x + 1 + 3\left(x + 1\right)\right) + \left(-3\left(x - 1\right)\right)$ → $x = 6$ — steps=multi
- **D=22 seed=207:** $\left(x - 1\right) * 3 - 5x + 5 + \left(\left(-x + 2\right) * (-3) - 2x + 3\right) + \left(\left(x + 3\right) * 3 - x - 6\right) = \left(x + 2\right) * (-2) + 3x + 5 + \left(\left(x - 2\right) * 3 + 5\right) + \left(\left(x - 12\right) * (-2)\right)$ → $x = -22$ — steps=multi

## Current default (same D/seeds)

- **D=0 seed=101:** $3(x + 2) = 24$ → $x = 6$ — form_id=multi_step_distribute, steps=multi
- **D=0 seed=207:** $2x + 1 = x + 4$ → $x = 3$ — form_id=vars_both_sides, steps=multi
- **D=8 seed=101:** $-5x + 15 = -4x + 3$ → $x = 12$ — form_id=vars_both_sides, steps=multi
- **D=8 seed=207:** $-2(x - 4) = 20$ → $x = -6$ — form_id=multi_step_distribute, steps=multi
- **D=16 seed=101:** $-3\left(x - 3\right) = -6x - 12$ → $x = -7$ — form_id=multi_step_distribute, steps=multi
- **D=16 seed=207:** $-3\left(x - 8\right) + 7 = -2\left(x + 3\right) + 48$ → $x = -11$ — form_id=multi_step_distribute, steps=multi
- **D=22 seed=101:** $5 + \left(x + 1\right) * (-2) + \left(2x + 2 + \left(x + 1\right) * (-3)\right) + \left(3x + 3 + \left(x - 1\right) * 4\right) = 2x - 5 + \left(x - 2\right) * (-3) + \left(6 + \left(-x - 2\right) * 3\right) + \left(\left(x + 10\right) * 3\right)$ → $x = 6$ — form_id=multi_step_distribute, steps=multi
- **D=22 seed=207:** $-5x + 3 + \left(-x + 2\right)\left(-3\right) + \left(-4x - 13 + \left(x + 3\right)3\right) + \left(3x + 2 + \left(x + 3\right)2\right) = -5x + 5 + \left(x - 2\right)3 + \left(\left(-x - 2\right)\left(-2\right)\right) + \left(-26 + 8x\right)$ → $x = 4$ — form_id=multi_step_distribute, steps=multi

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.3** — Easy both-sides: $3x+2=x+8$ — https://openstax.org/books/elementary-algebra-2e/pages/2-3-solve-equations-with-variables-and-constants-on-both-sides
- **OpenStax Elementary Algebra 2e §2.4** — Easy distribute: $2(x+1)=8$; Example 2.29+ — https://openstax.org/books/elementary-algebra-2e/pages/2-4-use-a-general-strategy-to-solve-linear-equations
- **OpenStax Elementary Algebra 2e §2.5** — Fraction/decimal coeffs at high D (skipped when integers_only) — https://openstax.org/books/elementary-algebra-2e/pages/2-5-solve-equations-with-fractions-or-decimals

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Default D=0 matches OpenStax easy. Old D=0 is already a nested multi-paren identity — too hard vs gold.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveLinear multi species (already wired). Alias `pa_equations_multi_step_equations`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `solve`
