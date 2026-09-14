# Notes — `one_step_ineq` (`one_step_inequalities`)

Also covers: `one_step_inequalities`, `g6_solving_and_graphing_one_step_inequalities`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve a one-step inequality; flip when multiplying/dividing by a negative.
- **D=0:** $x\pm a<b$ or $ax>b$ with **positive** $a$ (no required flip).
- **High D (≈16–22):** Negatives (flip); later $x/a$.
- **Must not:** Two-step $ax\pm b<c$ on this leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_inequality=True`.

- **D=0 seed=101:** $x - 3 < -3$ → $x < 0$ — steps=one
- **D=0 seed=207:** $x - 1 > -4$ → $x > -3$ — steps=one
- **D=8 seed=101:** $\frac{x}{-2} > 0$ → $x < 0$ — steps=one
- **D=8 seed=207:** $3x \le -9$ → $x \le -3$ — steps=one
- **D=16 seed=101:** $\frac{x}{-2} > -\frac{3}{2}$ → $x < 3$ — steps=one
- **D=16 seed=207:** $\frac{x}{-2} \le \frac{3}{2}$ → $x \ge -3$ — steps=one
- **D=22 seed=101:** $\frac{x}{-5} > -\frac{3}{5}$ → $x < 3$ — steps=one
- **D=22 seed=207:** $\frac{x}{-4} \le \frac{3}{4}$ → $x \ge -3$ — steps=one

## Current default (same D/seeds)

- **D=0 seed=101:** $2x > 12$ → $x > 6$ — form_id=one_step_ineq_mul_div, steps=one
- **D=0 seed=207:** $x - 1 \le 2$ → $x \le 3$ — form_id=one_step_ineq_add_sub, steps=one
- **D=8 seed=101:** $-4x \ge -48$ → $x \le 12$ — form_id=one_step_ineq_mul_div, steps=one
- **D=8 seed=207:** $x - 15 > -21$ → $x > -6$ — form_id=one_step_ineq_add_sub, steps=one
- **D=16 seed=101:** $x - 9 \ge -16$ → $x \ge -7$ — form_id=one_step_ineq_add_sub, steps=one
- **D=16 seed=207:** $x + 11 > 0$ → $x > -11$ — form_id=one_step_ineq_add_sub, steps=one
- **D=22 seed=101:** $\frac{x}{-3} \ge -\frac{23}{3}$ → $x \le 23$ — form_id=one_step_ineq_mul_div, steps=one
- **D=22 seed=207:** $x + 21 > 10$ → $x > -11$ — form_id=one_step_ineq_add_sub, steps=one

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.7** — Graph + solve; add/sub property; mul/div with flip — https://openstax.org/books/elementary-algebra-2e/pages/2-7-solve-linear-inequalities

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Not a WP. Default D=0 has no flip; old D=0 already uses negatives.

## Limitations

- Gallery section slug: `one_step_ineq` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveInequality (already wired). Alias `g6_solving_and_graphing_one_step_inequalities`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `solve`
