# Notes — `a2_equations_and_inequalities_multi_step_inequalities`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Equations and Inequalities
- **Generator:** `multi_step_inequalities`
- **Suggested family:** `solve`

---

## What the question should look like (D=0 vs high D)

- **Skill:** One distribute or both-sides; no flip at easy.
- **D=0:** One distribute or both-sides; no flip at easy.
- **High D (≈16–22):** Both sides + distribute; multiply/divide by negative (flip).
- **Must not:** Compound / absolute on this leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `use_sample_linear_inequality=True`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $-x + 6 + \left(x - 2\right)2 < 2$ | $x < 0$ |  |
| 0 | 207 | $-x + 12 + \left(x - 3\right)3 > -3$ | $x > -3$ |  |
| 8 | 101 | $-x + 6 + \left(x - 2\right)2 > 5x + \left(x + 1\right)2$ | $x < 0$ |  |
| 8 | 207 | $-x + 12 + \left(x - 3\right)3 \le x + 8 + \left(x - 1\right)2$ | $x \ge -3$ |  |
| 16 | 101 | $-5x + 14 + \left(x - 3\right)4 > -x + 2 + \left(x - 3\right)2$ | $x < 3$ |  |
| 16 | 207 | $-2x + 6 + \left(x - 1\right) * 3 \le \left(-3x - 9\right) * 2$ | $x \le -3$ |  |
| 22 | 101 | $-5x + 14 + \left(x - 3\right)4 > -3x + 16 + \left(x + 1\right)\left(-2\right)$ | $x > 3$ |  |
| 22 | 207 | $-2x + 9 + \left(-x + 2\right) * (-3) \le \left(2x + 6\right) * 2$ | $x \ge -3$ |  |

Opt-out flag used: `use_sample_linear_inequality=True`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §2.7 | https://openstax.org/books/elementary-algebra-2e/pages/2-7-solve-inequalities | Multi-step linear inequalities |
| OpenStax Intermediate Algebra 2e §2.3 | https://openstax.org/books/intermediate-algebra-2e/pages/2-3-solve-inequalities | IA inequalities |

## Variety notes / UNCLEAR flag

Old D=0 already multi-step distribute — match skeleton D=0 simplification.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveInequality (equation_skeleton).
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
