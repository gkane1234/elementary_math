# Notes — `a2_equations_and_inequalities_multi_step_equations`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Equations and Inequalities
- **Generator:** `multi_step_equations`
- **Suggested family:** `solve`

---

## What the question should look like (D=0 vs high D)

- **Skill:** One distribute or both-sides linear equation with small integer coeffs.
- **D=0:** One distribute or both-sides linear equation with small integer coeffs.
- **High D (≈16–22):** Nested distribute, both sides, fractions at high D.
- **Must not:** D=0 already a 6-paren nest; literal-formula shapes.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `use_sample_linear_equation=True`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $5 + 2\left(x - 2\right) = 11x + 4 - 3\left(x + 1\right)$ | $x = 0$ |  |
| 0 | 207 | $3x - 3 + \left(x - 3\right)\left(-2\right) = 7x + 17 + \left(x + 1\right)\left(-2\right)$ | $x = -3$ |  |
| 8 | 101 | $-x + \frac{1}{2} = -\frac{4}{5}x + \frac{57}{70}$ | $x = -\frac{11}{7}$ |  |
| 8 | 207 | $3\left(x + 3\right) - 11 = 2\left(2x - 2\right) - 5x + \frac{18}{7}$ | $x = \frac{1}{7}$ |  |
| 16 | 101 | $-4x + 2 + 3\left(x - 1\right) + \left(-2x + 1 + 4\left(x + 1\right)\right) = 2x + \frac{12}{5} + 3\left(x + 2\right) + \left(-6x - 8 + 4\left(x + 2\right)\right)$ | $x = -\frac{11}{5}$ |  |
| 16 | 207 | $3 * \left(2x - 2\right) - 3x + 7 + \left(-2 * \left(x - 1\right)\right) = 2 * \left(x + 3\right) + x - 5 + \left(3 * \left(x + 2\right) - 4x - \frac{53}{13}\right)$ | $x = \frac{1}{13}$ |  |
| 22 | 101 | $2x + 2 + \left(x + 1\right)\left(-3\right) + \left(3x + 8 + \left(-x - 2\right)2\right) + \left(-x + 3 + \left(x - 1\right)2\right) = -6x - 4 + \left(x + 2\right)3 + \left(-4x - 15 + \left(x + 2\right)4\right) + \left(-3x - 8 + \left(x + 3\right)2\right)$ | $x = -\frac{11}{5}$ |  |
| 22 | 207 | $\left(x - 1\right) * 3 - 5x + 5 + \left(\left(-x + 2\right) * (-3) - 2x + 5\right) + \left(\left(x + 3\right) * 3 - x - 7\right) = \left(x + 2\right) * (-2) + 3x + 5 + \left(\left(x - 2\right) * 3 + 5\right) + \left(\left(-x + 3\right) * (-2) - 4x + \frac{116}{13}\right)$ | $x = \frac{1}{13}$ |  |

Opt-out flag used: `use_sample_linear_equation=True`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §2.3 | https://openstax.org/books/elementary-algebra-2e/pages/2-3-solve-equations-with-variables-and-constants-on-both-sides | Both sides: $3x+2=x+8$ |
| OpenStax Elementary Algebra 2e §2.4 | https://openstax.org/books/elementary-algebra-2e/pages/2-4-use-a-general-strategy-to-solve-linear-equations | Distribute: $2(x+1)=8$ |
| OpenStax Intermediate Algebra 2e §2.1 | https://openstax.org/books/intermediate-algebra-2e/pages/2-1-use-a-general-strategy-to-solve-equations | Review multi-step at IA level |

## Variety notes / UNCLEAR flag

Old D=0 is already nested multi-paren — harder than OpenStax easy.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveLinear (equation_skeleton) — alias of `multi_step_equations`.
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
