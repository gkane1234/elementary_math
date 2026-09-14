# Notes — `check_equation` (`g6_solutions_to_equations`)

Also covers: `g6_solutions_to_equations`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Decide whether $x=k$ is a solution of a given equation (yes/no).
- **D=0:** One-step $3x=24$ / $x+4=6$.
- **High D (≈16–22):** Two-step, both-sides, then fractions.
- **Must not:** Ask to *solve* instead of check.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_equation=True`.

- **D=0 seed=101:** $\text{Is } x = 6 \text{ a solution of } 3x = 18\text{?}$ → $\text{yes}$
- **D=0 seed=207:** $\text{Is } x = 3 \text{ a solution of } 3x = 9\text{?}$ → $\text{yes}$
- **D=8 seed=101:** $\text{Is } x = 7 \text{ a solution of } 6x + 9 = 33\text{?}$ → $\text{no}$
- **D=8 seed=207:** $\text{Is } x = -7 \text{ a solution of } 6x + 4 = 64\text{?}$ → $\text{no}$
- **D=16 seed=101:** $\text{Is } x = -3 \text{ a solution of } 12x + 19 = -5\text{?}$ → $\text{no}$
- **D=16 seed=207:** $\text{Is } x = 13 \text{ a solution of } 11x + 23 = 166\text{?}$ → $\text{yes}$
- **D=22 seed=101:** $\text{Is } x = 5 \text{ a solution of } \frac{5}{2}x + 8 = \frac{41}{2}\text{?}$ → $\text{yes}$
- **D=22 seed=207:** $\text{Is } x = 1 \text{ a solution of } \frac{5}{4}x + 3 = \frac{17}{4}\text{?}$ → $\text{yes}$

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Is } x = 4 \text{ a solution of } x - 4 = 0\text{?}$ → $\text{yes}$ — form_id=one_step_add_sub, steps=one
- **D=0 seed=207:** $\text{Is } x = 1 \text{ a solution of } x + 3 = 4\text{?}$ → $\text{yes}$ — form_id=one_step_add_sub, steps=one
- **D=8 seed=101:** $\text{Is } x = 8 \text{ a solution of } -3x - 15 = -39\text{?}$ → $\text{yes}$ — form_id=two_step, steps=two
- **D=8 seed=207:** $\text{Is } y = -1 \text{ a solution of } -4y - 3 = 5\text{?}$ → $\text{no}$ — form_id=two_step, steps=two
- **D=16 seed=101:** $\text{Is } x = -7 \text{ a solution of } -11x + 15 + 2x = -4x + 50\text{?}$ → $\text{yes}$ — form_id=vars_both_sides, steps=multi
- **D=16 seed=207:** $\text{Is } z = 4 \text{ a solution of } -6z - 15 + 2z = 6z + 5\text{?}$ → $\text{no}$ — form_id=vars_both_sides, steps=multi
- **D=22 seed=101:** $\text{Is } x = \frac{16}{5} \text{ a solution of } \frac{1}{2}\left(-2x - 35\right) = -\frac{207}{10}\text{?}$ → $\text{yes}$ — form_id=fraction_or_decimal_coeffs, steps=multi
- **D=22 seed=207:** $\text{Is } y = -3 \text{ a solution of } \frac{1}{3}\left(-4y + 26\right) = \frac{38}{3}\text{?}$ → $\text{yes}$ — form_id=fraction_or_decimal_coeffs, steps=multi

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.1 Example 2.1** — Determine whether $x=3/2$ is a solution of $4x-2=2x+1$ — https://openstax.org/books/elementary-algebra-2e/pages/2-1-solve-equations-using-the-subtraction-and-addition-properties-of-equality

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Old and default both check a candidate. Default D=0 is one-step add/sub; old D=0 is $3x=k$.

## Limitations

- Old and default both check a candidate. Default D=0 is one-step add/sub; old D=0 is $3x=k$.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveLinear check-solution packaging (already wired).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `solve`
