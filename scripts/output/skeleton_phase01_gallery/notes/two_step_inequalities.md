# Notes — `two_step_ineq` (`two_step_inequalities`)

Also covers: `two_step_inequalities`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve $ax\pm b<c$ (two reverse ops; flip if $a<0$).
- **D=0:** Small positive coeffs; no flip required.
- **High D (≈16–22):** Negative leading coeff (flip) before fractions.
- **Must not:** Collapse to one-step.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_inequality=True`.

- **D=0 seed=101:** $2x + 1 < 1$ → $x < 0$ — steps=two
- **D=0 seed=207:** $x + 3 > 0$ → $x > -3$ — steps=two
- **D=8 seed=101:** $-2x - 1 > -1$ → $x < 0$ — steps=two
- **D=8 seed=207:** $x - 3 \le -6$ → $x \le -3$ — steps=two
- **D=16 seed=101:** $-4x - 2 > -14$ → $x < 3$ — steps=two
- **D=16 seed=207:** $x - 3 \le -6$ → $x \le -3$ — steps=two
- **D=22 seed=101:** $-4x - 2 > -14$ → $x < 3$ — steps=two
- **D=22 seed=207:** $x - 3 \le -6$ → $x \le -3$ — steps=two

## Current default (same D/seeds)

- **D=0 seed=101:** $3x + 4 > 22$ → $x > 6$ — form_id=two_step_ineq, steps=two
- **D=0 seed=207:** $2x + 2 \le 8$ → $x \le 3$ — form_id=two_step_ineq, steps=two
- **D=8 seed=101:** $-5x - 7 \ge -67$ → $x \le 12$ — form_id=two_step_ineq, steps=two
- **D=8 seed=207:** $-2x - 15 < -3$ → $x > -6$ — form_id=two_step_ineq, steps=two
- **D=16 seed=101:** $-3x - 6 \le 15$ → $x \ge -7$ — form_id=two_step_ineq, steps=two
- **D=16 seed=207:** $-3x - 15 < 18$ → $x > -11$ — form_id=two_step_ineq, steps=two
- **D=22 seed=101:** $-9x - 13 \ge -220$ → $x \le 23$ — form_id=two_step_ineq, steps=two
- **D=22 seed=207:** $-3x - 30 < 3$ → $x > -11$ — form_id=two_step_ineq, steps=two

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.7** — Two-step inequalities after one-step; flip when $a<0$ — https://openstax.org/books/elementary-algebra-2e/pages/2-7-solve-linear-inequalities

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Old D=0 seed 207 is one-step $x+3>0$. Default stays $ax\pm b<c$.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveInequality two-step (already wired).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `solve`
