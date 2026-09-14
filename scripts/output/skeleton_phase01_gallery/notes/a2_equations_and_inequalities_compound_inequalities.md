# Notes — `a2_equations_and_inequalities_compound_inequalities`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Equations and Inequalities
- **Generator:** `compound_inequalities`
- **Suggested family:** `solve`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Already-isolated and/or ($x\ge -2$ and $x\le 0$) on number line.
- **D=0:** Already-isolated and/or ($x\ge -2$ and $x\le 0$) on number line.
- **High D (≈16–22):** Solve linear compound then graph isolated form; OR inequalities.
- **Must not:** Absolute value on this leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `use_sample_compound_inequality=True`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Solve: } x \ge -2 \text{ and } x \le 0$ | $-2 \le x \le 0$ |  |
| 0 | 207 | $\text{Solve: } x > -3 \text{ and } x < 1$ | $-3 < x < 1$ |  |
| 8 | 101 | $\text{Solve: } x > 1 \text{ and } x < 3$ | $1 < x < 3$ |  |
| 8 | 207 | $\text{Solve: } x > 1 \text{ and } x \le 2$ | $x > 1 \text{ and } x \le 2$ |  |
| 16 | 101 | $\text{Solve: } x \ge -1 \text{ and } x < 3$ | $x \ge -1 \text{ and } x < 3$ |  |
| 16 | 207 | $\text{Solve: } x > 1 \text{ and } x \le 2$ | $x > 1 \text{ and } x \le 2$ |  |
| 22 | 101 | $\text{Solve: } x \ge -1 \text{ and } x < 3$ | $x \ge -1 \text{ and } x < 3$ |  |
| 22 | 207 | $\text{Solve: } x > 1 \text{ and } x \le 2$ | $x > 1 \text{ and } x \le 2$ |  |

Opt-out flag used: `use_sample_compound_inequality=True`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §2.8 | https://openstax.org/books/elementary-algebra-2e/pages/2-8-solve-compound-inequalities | And / or; number line |
| OpenStax Intermediate Algebra 2e §2.4 | https://openstax.org/books/intermediate-algebra-2e/pages/2-4-solve-compound-inequalities | IA compound |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** CompoundInequality (compound_inequalities framework).
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
