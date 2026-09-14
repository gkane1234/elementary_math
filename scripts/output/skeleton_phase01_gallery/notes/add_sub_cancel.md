# Notes — `add_sub_cancel` (`rational_expression_simplification`)

Also covers: `rational_expression_simplification`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Add or subtract rational expressions and simplify.
- **D=0:** Like denominators, linear; combine numerators.
- **High D (≈16–22):** Unlike dens / LCD of polynomials; cancel after combining.
- **Must not:** Single-fraction simplify-only; multiply/divide.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_constructive_rational=True`.

- **D=0 seed=101:** $\frac{-3}{x} + \frac{-2}{x}$ → $\frac{-5}{x}$
- **D=0 seed=207:** $\frac{4}{x-1} + \frac{1}{x-1}$ → $\frac{5}{x-1}$
- **D=8 seed=101:** $\frac{2}{9x^{2}+12x-5} + \frac{-17x-9}{(4x-3)(3x-1)(3x+5)}$ → $\frac{-3}{(4x-3)(3x-1)},\; x \neq -\frac{5}{3}$
- **D=8 seed=207:** $\frac{-x-23}{6x^{2}-13x-5} + \frac{-4}{3x+1}$ → $\frac{-3}{2x-5},\; x \neq -\frac{1}{3}$
- **D=16 seed=101:** $\frac{1}{(2x-1)(4x+5)(2x+3)(3x-1)(4x+3)} + \frac{30x^{2}+35x-16}{(2x-1)(4x+5)(2x+3)(3x-1)(4x+3)}$ → $\frac{5}{(2x-1)(4x+5)(4x+3)},\; x \neq -\frac{3}{2}, \frac{1}{3}$
- **D=16 seed=207:** $\frac{-2}{6x^{2}+7x+2} + \frac{18x^{2}+27x+14}{(3x+2)(3x+4)(2x+1)}$ → $\frac{3}{3x+4},\; x \neq -\frac{2}{3}, -\frac{1}{2}$
- **D=22 seed=101:** $\frac{-18x^{2}+30x-16}{(4x-1)(3x-4)(3x+2)(3x+4)(2x-1)(2x-5)} + \frac{1}{(4x-1)(3x-4)(3x+2)(2x-1)(2x-5)}$ → $\frac{-3}{(4x-1)(3x+2)(3x+4)(2x-5)},\; x \neq \frac{1}{2}, \frac{4}{3}$
- **D=22 seed=207:** $\frac{1}{3x-1} + \frac{-6x^{2}+4x+5}{(3x-1)(3x-2)(2x+5)}$ → $\frac{5}{(3x-2)(2x+5)},\; x \neq \frac{1}{3}, \frac{3}{2}$

Opt-out flag used: `use_constructive_rational=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Combine and simplify: } 3 + \frac{3}{x + 1} + \frac{-3}{x + 1}$ → $\frac{3x + 3}{x + 1}$ — pattern=AddSubCancel
- **D=0 seed=207:** $\text{Combine and simplify: } \frac{6}{x + 4} + \frac{1}{x - 3}$ → $\frac{7x - 14}{\left(x - 3\right)\left(x + 4\right)}$ — pattern=AddSubCancel
- **D=8 seed=101:** $\text{Combine and simplify: } 4 + \frac{-1}{x - 1} + \frac{1}{x - 1}$ → $4,\; x \neq 1$ — pattern=AddSubCancel
- **D=8 seed=207:** $\text{Combine and simplify: } 7 + \frac{2}{y - 5} + \frac{17}{2y - 3} + \frac{-14}{\left(y - 5\right)\left(2y - 3\right)}$ → $\frac{14y}{2y - 3},\; y \neq 5$ — pattern=AddSubCancel
- **D=16 seed=101:** $\text{Combine and simplify: } 28 + \frac{-21}{v - 1} + \frac{3}{v - 3} + \frac{152}{3v - 2} + \frac{-42}{3v^{3} - 14v^{2} + 17v - 6}$ → $\frac{84v + 42}{3v - 2},\; v \neq 1, 3$ — pattern=AddSubCancel
- **D=16 seed=207:** $\text{Combine and simplify: } 5 + \frac{1}{3x - 2} + \frac{-3x - 1}{\left(3x - 2\right)\left(3x + 1\right)}$ → $5,\; x \neq \frac{2}{3}, -\frac{1}{3}$ — pattern=AddSubCancel
- **D=22 seed=101:** $\text{Combine and simplify: } \frac{4032}{4y + 3} + \frac{-675}{3y - 5} + \frac{-5626}{2y - 1} + \frac{5075}{y + 1} + \frac{24360y}{24y^{4} - 10y^{3} - 53y^{2} - 4y + 15}$ → $\frac{6090y - 12180}{\left(y + 1\right)\left(2y - 1\right)},\; y \neq -\frac{3}{4}, \frac{5}{3}$ — pattern=AddSubCancel
- **D=22 seed=207:** $\text{Combine and simplify: } 120 + \frac{-35}{3l - 2} + \frac{8}{3l + 1} + \frac{-51}{l + 2} + \frac{240l + 120}{9l^{3} + 15l^{2} - 8l - 4}$ → $\frac{120l + 180}{l + 2},\; l \neq -\frac{1}{3}, \frac{2}{3}$ — pattern=AddSubCancel

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §8.3 | https://openstax.org/books/elementary-algebra-2e/pages/8-3-add-and-subtract-rational-expressions-with-a-common-denominator | Common denominator; combine numerators. |
| OpenStax Elementary Algebra 2e §8.4 | https://openstax.org/books/elementary-algebra-2e/pages/8-4-add-and-subtract-rational-expressions-with-unlike-denominators | LCD of polynomial dens; then simplify. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP. Algebra shapes follow the old path; default is the live skeleton.
Flag UNCLEAR only if old path is a dump stub or the skill is wrong.

## Limitations

- UNCLEAR: gold look not fully locked — keep red gallery header; do not invent a new engine.
- Gallery section slug: `add_sub_cancel` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** AddSubCancel / rational_skeleton (already wired). Opt-out: `use_constructive_rational`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `other`

_Catalog:_ Algebra 1 — Rational Expressions — Adding and subtracting rational expressions. Generator `rational_expression_simplification`.
