# Notes — `graph_ineq` (`graphing_single_variable_inequalities`)

Also covers: `graphing_single_variable_inequalities`, `g6_solutions_to_inequalities`, `g6_writing_and_graphing_inequalities`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Graph a one-variable inequality on a number line (isolated at D=0; solve then graph later).
- **D=0:** Already isolated $x<3$ — prompt is the inequality to graph (prompt ≈ answer).
- **High D (≈16–22):** Solve a one- or two-step inequality, then graph the isolated form.
- **Must not:** Opt-out falling back to *solve* one-step inequalities with no graph prompt.

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

- **D=0 seed=101:** $x \le 4$ → $x \le 4$ — form_id=one_step_ineq_add_sub, steps=one
- **D=0 seed=207:** $x < 1$ → $x < 1$ — form_id=one_step_ineq_add_sub, steps=one
- **D=8 seed=101:** $x \le 4$ → $x \le 4$ — form_id=one_step_ineq_add_sub, steps=one
- **D=8 seed=207:** $x < -1$ → $x < -1$ — form_id=one_step_ineq_add_sub, steps=one
- **D=16 seed=101:** $-3x - 6 \le 15$ → $x \ge -7$ — form_id=two_step_ineq, steps=two
- **D=16 seed=207:** $-3x - 15 < 18$ → $x > -11$ — form_id=two_step_ineq, steps=two
- **D=22 seed=101:** $-9x - 13 \ge -220$ → $x \le 23$ — form_id=two_step_ineq, steps=two
- **D=22 seed=207:** $-3x - 30 < 3$ → $x > -11$ — form_id=two_step_ineq, steps=two

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.7** — Learning objective: graph inequalities on the number line, then solve — https://openstax.org/books/elementary-algebra-2e/pages/2-7-solve-linear-inequalities

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Default D=0 is isolated $x\le 4$ (graph skill). Old opt-out `use_sample_linear_inequality` **does not graph** — it solves $x-3<-3$. That is expected opt-out, not gold.

## Limitations

- Default D=0 is isolated $x\le 4$ (graph skill). Old opt-out `use_sample_linear_inequality` **does not graph** — it solves $x-3<-3$. That is expected opt-out, not gold.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveInequality `sample_graph_inequality` (already wired). Aliases: `g6_solutions_to_inequalities`, `g6_writing_and_graphing_inequalities`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `solve`
