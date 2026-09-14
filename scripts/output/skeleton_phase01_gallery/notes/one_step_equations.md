# Notes — `one_step` (`one_step_equations`)

Also covers: `one_step_equations`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve a one-step linear equation (add/sub or mul/div).
- **D=0:** $x\pm a=b$ or $ax=b$ with small positive integers; no fractions.
- **High D (≈16–22):** Larger |coeffs|; negatives; later $x/a=b$ fractions (numeric first).
- **Must not:** Two-step $ax\pm b=c$, distribute, or a story dump.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_equation=True`.

- **D=0 seed=101:** $x + 2 = 2$ → $x = 0$ — steps=one
- **D=0 seed=207:** $x - 1 = -4$ → $x = -3$ — steps=one
- **D=8 seed=101:** $x + 2 = 8$ → $x = 6$ — steps=one
- **D=8 seed=207:** $2x = -18$ → $x = -9$ — steps=one
- **D=16 seed=101:** $x + 4 = 19$ → $x = 15$ — steps=one
- **D=16 seed=207:** $2x = -28$ → $x = -14$ — steps=one
- **D=22 seed=101:** $x + 4 = 14$ → $x = 10$ — steps=one
- **D=22 seed=207:** $2x = -40$ → $x = -20$ — steps=one

## Current default (same D/seeds)

- **D=0 seed=101:** $x - 4 = 2$ → $x = 6$ — form_id=one_step_add_sub, steps=one
- **D=0 seed=207:** $2x = 6$ → $x = 3$ — form_id=one_step_mul_div, steps=one
- **D=8 seed=101:** $-2x = -24$ → $x = 12$ — form_id=one_step_mul_div, steps=one
- **D=8 seed=207:** $x - 11 = -17$ → $x = -6$ — form_id=one_step_add_sub, steps=one
- **D=16 seed=101:** $\frac{x}{-3} = \frac{7}{3}$ → $x = -7$ — form_id=one_step_mul_div, steps=one
- **D=16 seed=207:** $x - 3 = -14$ → $x = -11$ — form_id=one_step_add_sub, steps=one
- **D=22 seed=101:** $-9x = -207$ → $x = 23$ — form_id=one_step_mul_div, steps=one
- **D=22 seed=207:** $x - 5 = -16$ → $x = -11$ — form_id=one_step_add_sub, steps=one

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.1** — $x+a=b$ / $x-a=b$ (addition/subtraction property) — https://openstax.org/books/elementary-algebra-2e/pages/2-1-solve-equations-using-the-subtraction-and-addition-properties-of-equality
- **OpenStax Elementary Algebra 2e §2.2** — $ax=b$ or $x/a=b$ — https://openstax.org/books/elementary-algebra-2e/pages/2-2-solve-equations-using-the-division-and-multiplication-properties-of-equality
- **OpenStax Prealgebra 2e §3.5 / §4.7 / §5.4** — Integer / fraction / decimal coefficients on the same one-step skill — https://openstax.org/books/prealgebra-2e/pages/3-5-solve-equations-using-integers-the-division-property-of-equality

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Not a WP. Old and default stay one-step. Default D=0 avoids negatives (old D=0 seed 207 is $x-1=-4$). Default D=16 can show $x/a=b$ fractions.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveLinear / equation_skeleton (already wired). Opt-out: `use_sample_linear_equation`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `solve`
