# Notes — `a2_rational_expressions_multiplying_and_dividing`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Rational Expressions
- **Generator:** `rational_expression_multiply_divide`
- **Suggested family:** `rational`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Binomial factors; ÷ as multiply by reciprocal.
- **D=0:** Binomial factors; ÷ as multiply by reciprocal.
- **High D (≈16–22):** Degree-2 trinomials; complex fraction style at D=16.
- **Must not:** Add/subtract; equation.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `use_constructive_rational=True`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\frac{\left(x-4\right)\left(x+3\right)}{x+4} \div \frac{\left(x-1\right)\left(x+3\right)}{x+1}$ | $\frac{x^{2}-3x-4}{x^{2}+3x-4},\; x \neq -4, -3, -1, 1$ | form=divide_rationals |
| 0 | 207 | $\frac{\left(x+1\right)\left(x-4\right)}{x-2} \div \frac{\left(x+3\right)\left(x-4\right)}{x-3}$ | $\frac{x^{2}-2x-3}{x^{2}+x-6},\; x \neq -3, 2, 3, 4$ | form=divide_rationals |
| 8 | 101 | $\frac{\left(5x-1\right)\left(4x-7\right)}{\left(3x+7\right)\left(5x-2\right)} \div \frac{\left(3x-2\right)\left(4x-7\right)}{\left(4x+3\right)\left(5x-2\right)}$ | $\frac{20x^{2}+11x-3}{9x^{2}+15x-14},\; x \neq -\frac{7}{3}, -\frac{3}{4}, \frac{2}{5}, \frac{2}{3}, \frac{7}{4}$ | form=divide_rationals |
| 8 | 207 | $\frac{\left(5x-4\right)\left(3x-4\right)}{\left(x+8\right)\left(x+2\right)} \div \frac{\left(2x-5\right)\left(3x-4\right)}{\left(3x+7\right)\left(x+2\right)}$ | $\frac{15x^{2}+23x-28}{2x^{2}+11x-40},\; x \neq -8, -\frac{7}{3}, -2, \frac{4}{3}, \frac{5}{2}$ | form=divide_rationals |
| 16 | 101 | $\frac{20x^{2}-57x+27}{15x^{2}+13x-20} \div \frac{4x^{2}-17x+18}{10x^{2}-33x+20}$ | $\frac{10x^{2}-31x+15}{3x^{2}-x-10},\; x \neq -\frac{5}{3}, \frac{4}{5}, 2, \frac{9}{4}, \frac{5}{2}$ | form=divide_rationals |
| 16 | 207 | $\frac{\frac{x^{2}+9x+8}{4x^{2}+4x-35}}{\frac{2x^{2}-5x-7}{2x^{2}-9x+10}}$ | $\frac{x^{2}+6x-16}{4x^{2}-49},\; x \neq -\frac{7}{2}, -1, 2, \frac{5}{2}, \frac{7}{2}$ | form=divide_rationals |
| 22 | 101 | $\frac{20x^{2}-57x+27}{15x^{2}+13x-20} \div \frac{4x^{2}-17x+18}{10x^{2}-33x+20}$ | $\frac{10x^{2}-31x+15}{3x^{2}-x-10},\; x \neq -\frac{5}{3}, \frac{4}{5}, 2, \frac{9}{4}, \frac{5}{2}$ | form=divide_rationals |
| 22 | 207 | $\frac{\frac{x^{2}+9x+8}{4x^{2}+4x-35}}{\frac{2x^{2}-5x-7}{2x^{2}-9x+10}}$ | $\frac{x^{2}+6x-16}{4x^{2}-49},\; x \neq -\frac{7}{2}, -1, 2, \frac{5}{2}, \frac{7}{2}$ | form=divide_rationals |

Opt-out flag used: `use_constructive_rational=True`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §8.2 | https://openstax.org/books/elementary-algebra-2e/pages/8-2-multiply-and-divide-rational-expressions | Multiply / divide; cancel |
| OpenStax Intermediate Algebra 2e §7.1 | https://openstax.org/books/intermediate-algebra-2e/pages/7-1-multiply-and-divide-rational-expressions | IA multiply/divide |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** MulDivCancel (rational_skeleton).
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
