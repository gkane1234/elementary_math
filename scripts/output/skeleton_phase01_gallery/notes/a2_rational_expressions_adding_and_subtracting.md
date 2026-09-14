# Notes — `a2_rational_expressions_adding_and_subtracting`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Rational Expressions
- **Generator:** `rational_expression_simplification`
- **Suggested family:** `rational`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Common denominator already ($\frac1{x+1}+\frac2{x+1}$).
- **D=0:** Common denominator already ($\frac1{x+1}+\frac2{x+1}$).
- **High D (≈16–22):** Unlike denominators; factor LCD; 3-term at D=16+.
- **Must not:** Multiply/divide only; equation.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `use_constructive_rational=True`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Combine and simplify: } \frac{1}{x + 1} + \frac{2}{x + 1}$ | $\frac{3}{x + 1},\; x \neq -1$ | form=add_common_den |
| 0 | 207 | $\text{Combine and simplify: } \frac{-3}{x - 3} + \frac{1}{x - 3}$ | $\frac{-2}{x - 3},\; x \neq 3$ | form=add_common_den |
| 8 | 101 | $\text{Combine and simplify: } \frac{2z - 2}{z^{2} - 5z + 4}+\frac{4}{z - 2}$ | $\frac{6z - 20}{z^{2} - 6z + 8},\; z \neq 1$ | form=add_unlike_dens |
| 8 | 207 | $\text{Combine and simplify: } \frac{3}{z + 5}+\frac{2z - 14}{z^{2} - 13z + 42}$ | $\frac{5z - 8}{z^{2} - z - 30},\; z \neq 7$ | form=add_unlike_dens |
| 16 | 101 | $\text{Combine and simplify: } \frac{8v - 32}{v^{2} - 3v - 4}+\frac{4v - 12}{v^{2} - 10v + 21}+\frac{8v - 32}{v^{2} - 2v - 8}$ | $\frac{20v^{2} - 76v - 160}{v^{3} - 4v^{2} - 19v - 14},\; v \neq 3, 4$ | form=add_unlike_with_cancel |
| 16 | 207 | $\text{Combine and simplify: } \frac{2z - 12}{z^{2} + z - 42}+\frac{\left(\left(2 + 6\right)\right)}{z + 9}+\frac{7z - 56}{z^{2} - 13z + 40}$ | $\frac{17z^{2} + 136z + 71}{z^{3} + 11z^{2} - 17z - 315},\; z \neq 6, 8$ | form=add_unlike_with_cancel |
| 22 | 101 | $\text{Combine and simplify: } \frac{8\tau + 24}{\tau^{2} - 6\tau - 27}+\frac{4\tau^{2} + 8\tau - 12}{\left(\tau - 4\right)\left(\tau - 1\right)\left(\tau + 3\right)}+\frac{8\tau + 24}{\tau^{2} - 9}$ | $\frac{20\tau^{2} - 208\tau + 492}{\tau^{3} - 16\tau^{2} + 75\tau - 108},\; \tau \neq -3, 1$ | form=add_unlike_with_cancel |
| 22 | 207 | $\text{Combine and simplify: } \frac{6}{t - 7}+\frac{-t + 8}{t^{2} + 5t - 104}+\frac{14t + 56}{t^{2} + 2t - 8}$ | $\frac{19t^{2} + 159t - 1444}{t^{3} + 4t^{2} - 103t + 182},\; t \neq -4, 8$ | form=add_unlike_with_cancel |

Opt-out flag used: `use_constructive_rational=True`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §8.3 | https://openstax.org/books/elementary-algebra-2e/pages/8-3-add-and-subtract-rational-expressions-with-common-denominators | Common denom |
| OpenStax Elementary Algebra 2e §8.4 | https://openstax.org/books/elementary-algebra-2e/pages/8-4-add-and-subtract-rational-expressions-with-unlike-denominators | Unlike denom / LCD |
| OpenStax Intermediate Algebra 2e §7.2 | https://openstax.org/books/intermediate-algebra-2e/pages/7-2-add-and-subtract-rational-expressions | IA add/subtract |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** AddSubCancel (rational_skeleton).
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
