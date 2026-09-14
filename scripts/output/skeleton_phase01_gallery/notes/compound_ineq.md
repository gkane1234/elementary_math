# Notes — `compound_ineq` (`compound_inequalities`)

Also covers: `compound_inequalities`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve a compound inequality and graph the solution on a number line.
- **D=0:** Already isolated: $-1<x<2$ or $x<-1$ or $x>1$ (prompt ≈ answer) on a blank number line.
- **High D (≈16–22):** Solve a linear compound first, then graph the isolated form.
- **Must not:** Single (non-compound) inequalities; abs-value compounds belong on the abs-ineq leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_compound_inequality=True`.

- **D=0 seed=101:** $\text{Solve: } x \ge -2 \text{ and } x \le 0$ → $-2 \le x \le 0$ — has_figure
- **D=0 seed=207:** $\text{Solve: } x > -3 \text{ and } x < 1$ → $-3 < x < 1$ — has_figure
- **D=8 seed=101:** $\text{Solve: } x > 1 \text{ and } x < 3$ → $1 < x < 3$ — has_figure
- **D=8 seed=207:** $\text{Solve: } x > 1 \text{ and } x \le 2$ → $x > 1 \text{ and } x \le 2$ — has_figure
- **D=16 seed=101:** $\text{Solve: } x \ge -1 \text{ and } x < 3$ → $x \ge -1 \text{ and } x < 3$ — has_figure
- **D=16 seed=207:** $\text{Solve: } x > 1 \text{ and } x \le 2$ → $x > 1 \text{ and } x \le 2$ — has_figure
- **D=22 seed=101:** $\text{Solve: } x \ge -1 \text{ and } x < 3$ → $x \ge -1 \text{ and } x < 3$ — has_figure
- **D=22 seed=207:** $\text{Solve: } x > 1 \text{ and } x \le 2$ → $x > 1 \text{ and } x \le 2$ — has_figure

Opt-out flag used: `use_sample_compound_inequality=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $0 < x < 2$ → $0 < x < 2$ — form_id=compound_inequality, pattern=CompoundInequality, has_figure
- **D=0 seed=207:** $0 < x < 2$ → $0 < x < 2$ — form_id=compound_inequality, pattern=CompoundInequality, has_figure
- **D=8 seed=101:** $-73 \leq 10x - 3 \leq 7$ → $-7 \leq x \leq 1$ — form_id=compound_inequality, pattern=CompoundInequality, has_figure
- **D=8 seed=207:** $-191 < 13x - 9 \leq 134$ → $-14 < x \leq 11$ — form_id=compound_inequality, pattern=CompoundInequality, has_figure
- **D=16 seed=101:** $16x + 13 < 333 \text{ and } 3x + 3 \geq -66$ → $-23 \leq x < 20$ — form_id=compound_inequality, pattern=CompoundInequality, has_figure
- **D=16 seed=207:** $-22 \leq 2(x + 6) - 20 \leq 24$ → $-7 \leq x \leq 16$ — form_id=compound_inequality, pattern=CompoundInequality, has_figure
- **D=22 seed=101:** $16x + 11 < 331 \text{ and } 3x + 1 \geq -53$ → $-18 \leq x < 20$ — form_id=compound_inequality, pattern=CompoundInequality, has_figure
- **D=22 seed=207:** $-10 \leq 2(x + 6) - 22 \leq 48$ → $0 \leq x \leq 29$ — form_id=compound_inequality, pattern=CompoundInequality, has_figure

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Intermediate Algebra 2e §2.6 | https://openstax.org/books/intermediate-algebra-2e/pages/2-6-solve-compound-inequalities | And vs or; isolated three-part; then linear sides to isolate. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes

Not a WP. Old opt-out stays already-isolated “and” compounds at D=0–22 in these seeds
(no linear sides to solve). Default D=0 is isolated three-part; D≥8 solves a linear
compound then graphs — that matches OpenStax IA §2.6 better than the flat old ladder.

## Limitations

- Gallery section slug: `compound_ineq` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** CompoundInequality (already wired). Opt-out: `use_sample_compound_inequality`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `solve`

_Catalog:_ Algebra 1 — Inequalities — Compound inequalities. Generator `compound_inequalities`.
