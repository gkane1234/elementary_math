# Notes — `a2_rational_expressions_complex_fractions`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Rational Expressions
- **Generator:** `complex_fractions`
- **Suggested family:** `rational`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Numeric-over-numeric or $\frac{\frac{a}{x}+b}{c}$.
- **D=0:** Numeric-over-numeric or $\frac{\frac{a}{x}+b}{c}$.
- **High D (≈16–22):** Rational expressions in num and den; LCD clear.
- **Must not:** Rational equation (= sign).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `use_hand_complex_frac=True`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\frac{\frac{2}{x} + 5}{4}$ | $\frac{5x+2}{4x},\; x \neq 0$ |  |
| 0 | 207 | $\frac{\frac{5}{x} + 2}{3}$ | $\frac{2x+5}{3x},\; x \neq 0$ |  |
| 8 | 101 | $\frac{\frac{4}{x} - 8}{-\frac{4}{x} + 5}$ | $\frac{-8x+4}{5x-4},\; x \neq 0$ |  |
| 8 | 207 | $\frac{-\frac{4}{x} + 1}{\frac{3}{x} - 2}$ | $\frac{-x+4}{2x-3},\; x \neq 0$ |  |
| 16 | 101 | $\frac{\frac{3}{x + 8} - \frac{1}{x - 4}}{\frac{5}{x + 7}}$ | $\frac{2x^{2}-6x-140}{5x^{2}+20x-160},\; x \neq -8, -7, 4$ |  |
| 16 | 207 | $\frac{\frac{-6}{x + 6} + \frac{1}{x + 9}}{\frac{2}{x - 3}}$ | $\frac{-5x^{2}-33x+144}{2x^{2}+30x+108},\; x \neq -9, -6, 3$ |  |
| 22 | 101 | $\frac{\frac{3}{x + 8} - \frac{1}{x - 4}}{\frac{5}{x + 7}}$ | $\frac{2x^{2}-6x-140}{5x^{2}+20x-160},\; x \neq -8, -7, 4$ |  |
| 22 | 207 | $\frac{\frac{-6}{x + 6} + \frac{1}{x + 9}}{\frac{2}{x - 3}}$ | $\frac{-5x^{2}-33x+144}{2x^{2}+30x+108},\; x \neq -9, -6, 3$ |  |

Opt-out flag used: `use_hand_complex_frac=True`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §8.5 | https://openstax.org/books/elementary-algebra-2e/pages/8-5-simplify-complex-rational-expressions | Complex fraction simplify |
| OpenStax Intermediate Algebra 2e §7.3 | https://openstax.org/books/intermediate-algebra-2e/pages/7-3-simplify-complex-rational-expressions | IA complex fractions |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** ComplexFracCancel (rational_skeleton).
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
