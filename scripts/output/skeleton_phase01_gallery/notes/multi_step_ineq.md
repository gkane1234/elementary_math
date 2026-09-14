# Notes — `multi_step_ineq` (`multi_step_inequalities`)

Also covers: `multi_step_inequalities`, `pa_multi_step_inequalities`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Multi-step inequality: simple distribute XOR both sides at D=0.
- **D=0:** $2(x+1)<8$ or $3x+2<x+8$ (no flip).
- **High D (≈16–22):** Both structures; negatives/flips later.
- **Must not:** D=0 nested parens like old path.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_inequality=True`.

- **D=0 seed=101:** $-x + 6 + \left(x - 2\right)2 < 2$ → $x < 0$ — steps=multi
- **D=0 seed=207:** $-x + 12 + \left(x - 3\right)3 > -3$ → $x > -3$ — steps=multi
- **D=8 seed=101:** $-x + 6 + \left(x - 2\right)2 > 5x + \left(x + 1\right)2$ → $x < 0$ — steps=multi
- **D=8 seed=207:** $-x + 12 + \left(x - 3\right)3 \le x + 8 + \left(x - 1\right)2$ → $x \ge -3$ — steps=multi
- **D=16 seed=101:** $-5x + 14 + \left(x - 3\right)4 > -x + 2 + \left(x - 3\right)2$ → $x < 3$ — steps=multi
- **D=16 seed=207:** $-2x + 6 + \left(x - 1\right) * 3 \le \left(-3x - 9\right) * 2$ → $x \le -3$ — steps=multi
- **D=22 seed=101:** $-5x + 14 + \left(x - 3\right)4 > -3x + 16 + \left(x + 1\right)\left(-2\right)$ → $x > 3$ — steps=multi
- **D=22 seed=207:** $-2x + 9 + \left(-x + 2\right) * (-3) \le \left(2x + 6\right) * 2$ → $x \ge -3$ — steps=multi

## Current default (same D/seeds)

- **D=0 seed=101:** $3x + 3 > x + 15$ → $x > 6$ — form_id=vars_both_sides_ineq, steps=multi
- **D=0 seed=207:** $2(x + 1) \le 8$ → $x \le 3$ — form_id=multi_step_ineq_distribute, steps=multi
- **D=8 seed=101:** $-2x - 12 \le -3x$ → $x \le 12$ — form_id=vars_both_sides_ineq, steps=multi
- **D=8 seed=207:** $4(x - 4) > -40$ → $x > -6$ — form_id=multi_step_ineq_distribute, steps=multi
- **D=16 seed=101:** $-6\left(x + 2\right) + 7 \ge -7x - 12$ → $x \ge -7$ — form_id=multi_step_ineq_distribute, steps=multi
- **D=16 seed=207:** $7\left(x - 8\right) + 7 > -2\left(x + 3\right) - 142$ → $x > -11$ — form_id=multi_step_ineq_distribute, steps=multi
- **D=22 seed=101:** $-3\left(x - 3\right) \le -6x + 78$ → $x \le 23$ — form_id=multi_step_ineq_distribute, steps=multi
- **D=22 seed=207:** $7\left(x - 8\right) + 13 > -2\left(x + 3\right) - 136$ → $x > -11$ — form_id=multi_step_ineq_distribute, steps=multi

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.7** — Inequalities that require simplification — https://openstax.org/books/elementary-algebra-2e/pages/2-7-solve-linear-inequalities

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Default D=0 is OpenStax-simple. Old D=0 already nested.

## Limitations

- Gallery section slug: `multi_step_ineq` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveInequality multi. Alias `pa_multi_step_inequalities`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `solve`
