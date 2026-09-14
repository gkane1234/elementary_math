# Notes — `proportion` (`solving_proportions`)

Also covers: `solving_proportions`, `pa_checking_for_a_proportion`, `g6_equivalent_ratio_equations`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve an algebraic proportion $a/b = x/c$ (or unknown in a denominator later).
- **D=0:** $2/3 = x/4$ style — unknown in one numerator.
- **High D (≈16–22):** Larger ints; then $a/b=(x\pm k)/c$.
- **Must not:** Rate/recipe word problems (those are ProportionRate).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_proportion=True`.

- **D=0 seed=101:** $\text{Solve: } \frac{2}{3} = \frac{x}{4}$ → $x = \frac{8}{3}$
- **D=0 seed=207:** $\text{Solve: } \frac{2}{3} = \frac{x}{4}$ → $x = \frac{8}{3}$
- **D=8 seed=101:** $\text{Solve: } \frac{4}{10} = \frac{x - 1}{6}$ → $x = \frac{17}{5}$
- **D=8 seed=207:** $\text{Solve: } \frac{12}{28} = \frac{x + 1}{9}$ → $x = \frac{20}{7}$
- **D=16 seed=101:** $\text{Solve: } \frac{24}{60} = \frac{x + 1}{10}$ → $x = 3$
- **D=16 seed=207:** $\text{Solve: } \frac{24}{56} = \frac{x + 1}{15}$ → $x = \frac{38}{7}$
- **D=22 seed=101:** $\text{Solve: } \frac{32}{80} = \frac{x + 1}{12}$ → $x = \frac{19}{5}$
- **D=22 seed=207:** $\text{Solve: } \frac{72}{168} = \frac{x + 1}{21}$ → $x = 8$

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Solve: } \frac{2}{5} = \frac{x}{4}$ → $\frac{8}{5}$ — form_id=proportion_application, steps=one
- **D=0 seed=207:** $\text{Solve: } \frac{2}{5} = \frac{x}{4}$ → $\frac{8}{5}$ — form_id=proportion_application, steps=one
- **D=8 seed=101:** $\text{Solve: } \frac{3}{5} = \frac{x}{7}$ → $\frac{21}{5}$ — form_id=proportion_application, steps=one
- **D=8 seed=207:** $\text{Solve: } \frac{7}{2} = \frac{x}{2}$ → $7$ — form_id=proportion_application, steps=one
- **D=16 seed=101:** $\text{Solve: } \frac{5}{9} = \frac{x + 3}{5}$ → $-\frac{2}{9}$ — form_id=proportion_application, steps=two
- **D=16 seed=207:** $\text{Solve: } \frac{3}{2} = \frac{x - 3}{7}$ → $\frac{27}{2}$ — form_id=proportion_application, steps=two
- **D=22 seed=101:** $\text{Solve: } \frac{15}{6} = \frac{x - 2}{9}$ → $\frac{49}{2}$ — form_id=proportion_application, steps=two
- **D=22 seed=207:** $\text{Solve: } \frac{14}{3} = \frac{x + 3}{2}$ → $\frac{19}{3}$ — form_id=proportion_application, steps=two

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §8.7 Example 8.71** — Solve $\frac{x}{63}=\frac{4}{7}$ — https://openstax.org/books/elementary-algebra-2e/pages/8-7-solve-proportion-and-similar-figure-applications
- **OpenStax Prealgebra 2e §6.5 (proportions applications) / related §5.6 rates** — PA check/solve proportion skill; stories stay on `pa_proportions_word_problems` — https://openstax.org/books/prealgebra-2e/pages/6-5-solve-proportions-and-their-applications

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Algebraic only. Old and default match OpenStax solve-proportion shape.

## Limitations

- Gallery section slug: `proportion` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Proportion / equation_skeleton (already wired).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `proportion`
