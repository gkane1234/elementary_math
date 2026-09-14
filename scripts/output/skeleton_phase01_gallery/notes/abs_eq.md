# Notes — `abs_eq` (`absolute_value_equations`)

Also covers: `absolute_value_equations`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve an absolute-value equation by splitting $|inner|=k$.
- **D=0:** $|x|=k$ or $|x+b|=k$ with $a=1$; small positive $k$.
- **High D (≈16–22):** $|ax+b|=k$ with $|a|\ge 2$; numeric hardness before extra nesting.
- **Must not:** Inequalities, graphs of $y=|x|$, or quadratic inners.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_absolute_value_equation=True`.

- **D=0 seed=101:** $\text{Solve: } |x - 2| = 2$ → $x = 0 \text{ or } x = 4$
- **D=0 seed=207:** $\text{Solve: } |x + 1| = 2$ → $x = -3 \text{ or } x = 1$
- **D=8 seed=101:** $\text{Solve: } |-x + 1| = |2x + 3|$ → $x = -4 \text{ or } x = -\frac{2}{3}$
- **D=8 seed=207:** $\text{Solve: } |-3x + 2| = |x|$ → $x = \frac{1}{2} \text{ or } x = 1$
- **D=16 seed=101:** $\text{Solve: } |2x + 1| = |4x + 3|$ → $x = -1 \text{ or } x = -\frac{2}{3}$
- **D=16 seed=207:** $\text{Solve: } |2x + 3| = |x + 3|$ → $x = -2 \text{ or } x = 0$
- **D=22 seed=101:** $\text{Solve: } |2x + 1| = |4x + 3|$ → $x = -1 \text{ or } x = -\frac{2}{3}$
- **D=22 seed=207:** $\text{Solve: } |2x + 3| = |x + 3|$ → $x = -2 \text{ or } x = 0$

Opt-out flag used: `use_sample_absolute_value_equation=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Solve: } \left|x - 1\right| = 2$ → $x = -1 \text{ or } x = 3$ — form_id=absolute_value_equation, pattern=AbsEquation
- **D=0 seed=207:** $\text{Solve: } \left|x - 2\right| = 5$ → $x = -3 \text{ or } x = 7$ — form_id=absolute_value_equation, pattern=AbsEquation
- **D=8 seed=101:** $\text{Solve: } \left|-2x + 2\right| = 14$ → $x = -6 \text{ or } x = 8$ — form_id=absolute_value_equation, pattern=AbsEquation
- **D=8 seed=207:** $\text{Solve: } \left|-3x + 6\right| = 24$ → $x = -6 \text{ or } x = 10$ — form_id=absolute_value_equation, pattern=AbsEquation
- **D=16 seed=101:** $\text{Solve: } \left|3x - 3\right| = 12$ → $x = -3 \text{ or } x = 5$ — form_id=absolute_value_equation, pattern=AbsEquation
- **D=16 seed=207:** $\text{Solve: } \left|-3x + 6\right| = 21$ → $x = -5 \text{ or } x = 9$ — form_id=absolute_value_equation, pattern=AbsEquation
- **D=22 seed=101:** $\text{Solve: } \left|-2x - 6\right| = 34$ → $x = -20 \text{ or } x = 14$ — form_id=absolute_value_equation, pattern=AbsEquation
- **D=22 seed=207:** $\text{Solve: } \left|-2x + 6\right| = 14$ → $x = -4 \text{ or } x = 10$ — form_id=absolute_value_equation, pattern=AbsEquation

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Intermediate Algebra 2e §2.7 | https://openstax.org/books/intermediate-algebra-2e/pages/2-7-solve-absolute-value-inequalities | $|x|=k$; $|x+b|=k$; later $|ax+b|=k$. Same section also covers inequalities — keep this leaf equations-only. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes

Not a WP. Old D=0 is $|x\pm b|=k$ (shifted, $a=1$), not $|x|=k$. Old D≥8 is
$|ax+b|=|cx+d|$ (two abs). OpenStax IA §2.7 gold is $|x|=k$ then $|ax+b|=k$
(one abs). Default follows the one-abs ladder, not the old two-abs shape.

## Limitations

- Gallery section slug: `abs_eq` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** AbsEquation / equation_skeleton (already wired). Opt-out: `use_sample_absolute_value_equation`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `solve`

_Catalog:_ Algebra 1 — Equations — Absolute value equations. Generator `absolute_value_equations`.
