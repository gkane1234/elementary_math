# Notes — `abs_ineq` (`absolute_value_inequalities`)

Also covers: `absolute_value_inequalities`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve an absolute-value inequality; write a compound and graph it.
- **D=0:** $|x|<k$ or $|x+b|<k$ with $a=1$.
- **High D (≈16–22):** $|ax+b|\ge k$ with $|a|\ge 2$; number line on the answer.
- **Must not:** Abs-value *equations*; quadratic inners.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_absolute_value_inequality=True`.

- **D=0 seed=101:** $\text{Solve: } |x| < 2$ → $-2 < x < 2$ — has_figure
- **D=0 seed=207:** $\text{Solve: } |x| > 1$ → $x < -1 \text{ or } x > 1$ — has_figure
- **D=8 seed=101:** $\text{Solve: } |x| < 2$ → $-2 < x < 2$ — has_figure
- **D=8 seed=207:** $\text{Solve: } |x| > 1$ → $x < -1 \text{ or } x > 1$ — has_figure
- **D=16 seed=101:** $\text{Solve: } |x| > 3$ → $x < -3 \text{ or } x > 3$ — has_figure
- **D=16 seed=207:** $\text{Solve: } |x| > 1$ → $x < -1 \text{ or } x > 1$ — has_figure
- **D=22 seed=101:** $\text{Solve: } |x| > 3$ → $x < -3 \text{ or } x > 3$ — has_figure
- **D=22 seed=207:** $\text{Solve: } |x| > 1$ → $x < -1 \text{ or } x > 1$ — has_figure

Opt-out flag used: `use_sample_absolute_value_inequality=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Solve: } \left|x - 1\right| < 1$ → $(0, 2)$ — form_id=absolute_value_inequality, pattern=AbsInequality, has_figure
- **D=0 seed=207:** $\text{Solve: } \left|x - 2\right| < 5$ → $(-3, 7)$ — form_id=absolute_value_inequality, pattern=AbsInequality, has_figure
- **D=8 seed=101:** $\text{Solve: } \left|-2x + 2\right| < 8$ → $(-3, 5)$ — form_id=absolute_value_inequality, pattern=AbsInequality, has_figure
- **D=8 seed=207:** $\text{Solve: } \left|-3x + 6\right| < 15$ → $(-3, 7)$ — form_id=absolute_value_inequality, pattern=AbsInequality, has_figure
- **D=16 seed=101:** $\text{Solve: } \left|3x - 3\right| \ge 9$ → $(-\infty,-2] \cup [4,\infty)$ — form_id=absolute_value_inequality, pattern=AbsInequality, has_figure
- **D=16 seed=207:** $\text{Solve: } \left|-3x + 6\right| < 27$ → $(-7, 11)$ — form_id=absolute_value_inequality, pattern=AbsInequality, has_figure
- **D=22 seed=101:** $\text{Solve: } \left|3x - 3\right| \ge 6$ → $(-\infty,-1] \cup [3,\infty)$ — form_id=absolute_value_inequality, pattern=AbsInequality, has_figure
- **D=22 seed=207:** $\text{Solve: } \left|-3x + 6\right| < 27$ → $(-7, 11)$ — form_id=absolute_value_inequality, pattern=AbsInequality, has_figure

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Intermediate Algebra 2e §2.7 | https://openstax.org/books/intermediate-algebra-2e/pages/2-7-solve-absolute-value-inequalities | Less-than → and; greater-than → or. $|x|<2$ then $|ax+b|\ge k$. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes

Not a WP. Old path stays $|x|<k$ / $|x|>k$ at every D in these seeds (no $a\neq 1$).
Default climbs: D=0 $|x+b|<k$, D≥8 $|ax+b|$ with $|a|\ge 2$, matching OpenStax IA §2.7.

## Limitations

- Gallery section slug: `abs_ineq` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** AbsInequality / equation_skeleton (already wired). Opt-out: `use_sample_absolute_value_inequality`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `solve`

_Catalog:_ Algebra 1 — Inequalities — Absolute value inequalities. Generator `absolute_value_inequalities`.
