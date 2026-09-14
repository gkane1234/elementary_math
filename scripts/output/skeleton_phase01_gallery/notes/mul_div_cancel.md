# Notes — `mul_div_cancel` (`rational_expression_multiply_divide`)

Also covers: `rational_expression_multiply_divide`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Multiply or divide rational expressions and cancel.
- **D=0:** Linear×linear with an obvious cancel; or divide by taking a reciprocal.
- **High D (≈16–22):** Quadratic factors; cancel across operands. Remain degree ≤ 2.
- **Must not:** Add/subtract; complex fractions.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_hand_muldiv=True`.

- **D=0 seed=101:** $\frac{\left(x-4\right)\left(x+3\right)}{x+4} \div \frac{\left(x-1\right)\left(x+3\right)}{x+1}$ → $\frac{x^{2}-3x-4}{x^{2}+3x-4},\; x \neq -4, -3, -1, 1$
- **D=0 seed=207:** $\frac{\left(x+1\right)\left(x-4\right)}{x-2} \cdot \frac{x+3}{\left(x-3\right)\left(x-4\right)}$ → $\frac{x^{2}+4x+3}{x^{2}-5x+6},\; x \neq 2, 3, 4$
- **D=8 seed=101:** $\frac{\left(5x-1\right)\left(4x-7\right)}{\left(3x+7\right)\left(5x-2\right)} \div \frac{\left(3x-2\right)\left(4x-7\right)}{\left(4x+3\right)\left(5x-2\right)}$ → $\frac{20x^{2}+11x-3}{9x^{2}+15x-14},\; x \neq -\frac{7}{3}, -\frac{3}{4}, \frac{2}{5}, \frac{2}{3}, \frac{7}{4}$
- **D=8 seed=207:** $\frac{\left(5x-4\right)\left(3x-4\right)}{\left(x+8\right)\left(x+2\right)} \cdot \frac{\left(2x-5\right)\left(x+2\right)}{\left(3x+7\right)\left(3x-4\right)}$ → $\frac{10x^{2}-33x+20}{3x^{2}+31x+56},\; x \neq -8, -\frac{7}{3}, -2, \frac{4}{3}$
- **D=16 seed=101:** $\frac{20x^{2}-57x+27}{15x^{2}+13x-20} \div \frac{4x^{2}-17x+18}{10x^{2}-33x+20}$ → $\frac{10x^{2}-31x+15}{3x^{2}-x-10},\; x \neq -\frac{5}{3}, \frac{4}{5}, 2, \frac{9}{4}, \frac{5}{2}$
- **D=16 seed=207:** $\frac{x^{2}+9x+8}{4x^{2}+4x-35} \cdot \frac{4x^{2}-24x+35}{x^{2}-x-2}$ → $\frac{2x^{2}+9x-56}{2x^{2}+3x-14},\; x \neq -\frac{7}{2}, -1, 2, \frac{5}{2}$
- **D=22 seed=101:** $\frac{20x^{2}-57x+27}{15x^{2}+13x-20} \div \frac{4x^{2}-17x+18}{10x^{2}-33x+20}$ → $\frac{10x^{2}-31x+15}{3x^{2}-x-10},\; x \neq -\frac{5}{3}, \frac{4}{5}, 2, \frac{9}{4}, \frac{5}{2}$
- **D=22 seed=207:** $\frac{x^{2}+9x+8}{4x^{2}+4x-35} \cdot \frac{4x^{2}-24x+35}{x^{2}-x-2}$ → $\frac{2x^{2}+9x-56}{2x^{2}+3x-14},\; x \neq -\frac{7}{2}, -1, 2, \frac{5}{2}$

Opt-out flag used: `use_hand_muldiv=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $\frac{\left(x + 4\right)\left(x + 1\right)}{x - 1} \div \frac{x + 1}{1}$ → $\frac{x + 4}{x - 1},\; x \neq -1$ — pattern=MulDivCancel
- **D=0 seed=207:** $\frac{2\left(x - 1\right)\left(x - 3\right)}{x - 2} \cdot \frac{1}{x - 3}$ → $\frac{2\left(x - 1\right)}{x - 2},\; x \neq 3$ — pattern=MulDivCancel
- **D=8 seed=101:** $\left(\frac{2\left(2x - 7\right)\left(x + 7\right)}{\left(2x - 1\right)\left(x + 5\right)}\right) / \left(\frac{x + 7}{x + 5}\right)$ → $\frac{2\left(2x - 7\right)}{2x - 1},\; x \neq -7, -5$ — pattern=MulDivCancel
- **D=8 seed=207:** $\frac{\left(2z - 5\right)\left(z + 3\right)}{\left(z - 5\right)\left(z - 3\right)} \cdot \frac{z - 3}{z + 3}$ → $\frac{2z - 5}{z - 5},\; z \neq -3, 3$ — pattern=MulDivCancel
- **D=16 seed=101:** $\frac{\frac{2n^{2} - n - 45}{3n^{2} - 10n + 8}}{\frac{2n + 9}{n - 2}}$ → $\frac{n - 5}{3n - 4},\; n \neq -\frac{9}{2}, 2$ — pattern=MulDivCancel
- **D=16 seed=207:** $\frac{6q^{2} + 2q - 28}{6q^{2} - 13q - 8} \cdot \frac{3q - 8}{3q + 7}$ → $\frac{2\left(q - 2\right)}{2q + 1},\; q \neq -\frac{7}{3}, \frac{8}{3}$ — pattern=MulDivCancel
- **D=22 seed=101:** $\frac{\frac{-9t^{2} + 24t - 7}{4t^{2} - 19t + 12}}{\frac{3t - 1}{t - 4}}$ → $\frac{-1\left(3t - 7\right)}{4t - 3},\; t \neq \frac{1}{3}, 4$ — pattern=MulDivCancel
- **D=22 seed=207:** $\frac{24e^{2} + 110e + 126}{3e^{2} - 14e + 16} \cdot \frac{3e - 8}{3e + 7}$ → $\frac{2\left(4e + 9\right)}{e - 2},\; e \neq -\frac{7}{3}, \frac{8}{3}$ — pattern=MulDivCancel

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §8.2 | https://openstax.org/books/elementary-algebra-2e/pages/8-2-multiply-and-divide-rational-expressions | Factor, cancel across ×; divide = multiply by reciprocal. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP. Algebra shapes follow the old path; default is the live skeleton.
Flag UNCLEAR only if old path is a dump stub or the skill is wrong.

## Limitations

- UNCLEAR: gold look not fully locked — keep red gallery header; do not invent a new engine.
- Gallery section slug: `mul_div_cancel` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** MulDivCancel / rational_skeleton (already wired). Opt-out: `use_hand_muldiv` (or `use_constructive_rational`).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `other`

_Catalog:_ Algebra 1 — Rational Expressions — Multiplying and dividing rational expressions. Generator `rational_expression_multiply_divide`.
