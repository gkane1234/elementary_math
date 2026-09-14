# Notes — `a2_rational_expressions_equations`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Rational Expressions
- **Generator:** `rational_equations`
- **Suggested family:** `solve`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Proportion or one-denominator linear ($\frac{x-1}{6}=-2$).
- **D=0:** Proportion or one-denominator linear ($\frac{x-1}{6}=-2$).
- **High D (≈16–22):** LCD, two+ linear denominators; extraneous roots.
- **Must not:** Expression simplify only; systems.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `use_hand_rational_equations=True`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\frac{x - 1}{6} = -2$ | $x = -11$ |  |
| 0 | 207 | $\frac{7}{x} = 1$ | $x = 7$ |  |
| 8 | 101 | $\frac{-4}{x + 10} + \frac{4}{x - 6} = -1$ | $x = -2$ |  |
| 8 | 207 | $\frac{-6}{x + 9} - \frac{7}{x + 7} = -5$ | $x = -5$ |  |
| 16 | 101 | $\frac{-4}{x + 10} + \frac{4}{x - 6} = -1$ | $x = -2$ |  |
| 16 | 207 | $\frac{-3}{x + 7} - \frac{5}{x - 1} = 2$ | $x = -9 \text{ or } x = -1$ |  |
| 22 | 101 | $\frac{-4}{x + 10} + \frac{4}{x - 6} = -1$ | $x = -2$ |  |
| 22 | 207 | $\frac{-3}{x + 7} - \frac{5}{x - 1} = 2$ | $x = -9 \text{ or } x = -1$ |  |

Opt-out flag used: `use_hand_rational_equations=True`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §8.6 | https://openstax.org/books/elementary-algebra-2e/pages/8-6-solve-rational-equations | Proportion → LCD → check extraneous |
| OpenStax Intermediate Algebra 2e §7.5 | https://openstax.org/books/intermediate-algebra-2e/pages/7-5-solve-rational-equations | IA rational equations |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** EqCancel (rational_skeleton) — alias of `rational_expressions_equations`.
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
