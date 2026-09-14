# Notes — `a2_rational_expressions_simplifying`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Rational Expressions
- **Generator:** `rational_simplification`
- **Suggested family:** `rational`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Factor quadratic num/den; cancel; state excluded values.
- **D=0:** Factor quadratic num/den; cancel; state excluded values.
- **High D (≈16–22):** Multi-factor cancel; leftover unsimplified at D=22.
- **Must not:** Add/subtract rationals; equation solve.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `use_constructive_rational=True`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Simplify: } \frac{2x^{2} - 4x - 6}{x^{2} - 4x + 3}$ | $\frac{2x + 2}{x - 1},\; x \neq 3$ | form=simplify_cancel |
| 0 | 207 | $\text{Simplify: } \frac{x^{2} - 5x + 6}{x^{2} + x - 6}$ | $\frac{x - 3}{x + 3},\; x \neq 2$ | form=simplify_cancel |
| 8 | 101 | $\text{Simplify: } \frac{4z^{2} - 8z - 12}{z^{2} - 4z + 3}$ | $\frac{4z + 4}{z - 1},\; z \neq 3$ | form=simplify_cancel |
| 8 | 207 | $\text{Simplify: } \frac{3\left(z - 7\right)\left(z + 7\right)\left(z\right)}{z^{2} - 2z}$ | $\frac{3z^{2} - 147}{z - 2},\; z \neq 0$ | form=simplify_cancel |
| 16 | 101 | $\text{Simplify: } \frac{8\left(v - 7\right)\left(v - 3\right)\left(v - 5\right)}{\left(v + 2\right)\left(v - 3\right)\left(v - 5\right)}$ | $\frac{8v - 56}{v + 2},\; v \neq 3, 5$ | form=simplify_cancel |
| 16 | 207 | $\text{Simplify: } \frac{8\left(z + 9\right)\left(z - 5\right)\left(z - 6\right)\left(z - 8\right)}{\left(z - 1\right)\left(z - 6\right)\left(z - 8\right)}$ | $\frac{8z^{2} + 32z - 360}{z - 1},\; z \neq 6, 8$ | form=simplify_cancel |
| 22 | 101 | $\text{Simplify: } \frac{8\left(\tau - 5\right)\left(\tau - 3\right)\left(\tau - 7\right)}{\left(\tau + 4\right)\left(\tau - 3\right)\left(\tau - 7\right)}$ | $\frac{8\tau - 40}{\tau + 4},\; \tau \neq 3, 7$ | form=simplify_cancel |
| 22 | 207 | $\text{Simplify: } \frac{\left((\frac{20}{5})\right)\left(-1\left(t + 13\right)\left(t - 13\right)\left(t + 4\right)\right)}{\left((\frac{20}{5})\right)\left(\left(t - 2\right)\left(t - 5\right)\left(t - 13\right)\left(t + 4\right)\right)}$ | $\frac{-t - 13}{t^{2} - 7t + 10},\; t \neq -4, 13$ | form=simplify_cancel |

Opt-out flag used: `use_constructive_rational=True`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §8.1 | https://openstax.org/books/elementary-algebra-2e/pages/8-1-simplify-rational-expressions | Factor and cancel; excluded values |
| OpenStax Intermediate Algebra 2e §7.1 | https://openstax.org/books/intermediate-algebra-2e/pages/7-1-multiply-and-divide-rational-expressions | IA simplify rationals |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SimplifyCancel (rational_skeleton).
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
