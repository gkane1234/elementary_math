# Notes — `a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Systems of Equations and Inequalities
- **Generator:** `systems_substitution`
- **Suggested family:** `systems`

---

## What the question should look like (D=0 vs high D)

- **Skill:** One equation solved for $y$ ($y=x+5$).
- **D=0:** One equation solved for $y$ ($y=x+5$).
- **High D (≈16–22):** Solve first equation for a variable; larger coeffs.
- **Must not:** Three-variable; elimination-only.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (LinearSystem skeleton)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\begin{cases} y = x + 5 \\ -5x + 5y = 25 \end{cases}$ | $(x, y) = (-2, 3)$ |  |
| 0 | 207 | $\begin{cases} y = 5x - 41 \\ -3x - 5y = -19 \end{cases}$ | $(x, y) = (8, -1)$ |  |
| 8 | 101 | $\begin{cases} y = x + 5 \\ -9x + 6y = 36 \end{cases}$ | $(x, y) = (-2, 3)$ |  |
| 8 | 207 | $\begin{cases} y = 5x - 41 \\ -5x - 10y = -30 \end{cases}$ | $(x, y) = (8, -1)$ |  |
| 16 | 101 | $\begin{cases} y = x + 5 \\ -14x + 6y = 46 \end{cases}$ | $(x, y) = (-2, 3)$ |  |
| 16 | 207 | $\begin{cases} y = 5x - 41 \\ -10x - 15y = -65 \end{cases}$ | $(x, y) = (8, -1)$ |  |
| 22 | 101 | $\begin{cases} y = x + 5 \\ -14x + 6y = 46 \end{cases}$ | $(x, y) = (-2, 3)$ |  |
| 22 | 207 | $\begin{cases} y = 5x - 41 \\ -10x - 15y = -65 \end{cases}$ | $(x, y) = (8, -1)$ |  |

Opt-out flag used: `none (LinearSystem skeleton)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §5.2 | https://openstax.org/books/elementary-algebra-2e/pages/5-2-solve-systems-of-equations-by-substitution | One equation isolated |
| OpenStax Intermediate Algebra 2e §4.2 | https://openstax.org/books/intermediate-algebra-2e/pages/4-2-solve-systems-of-equations-by-substitution | IA substitution |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** LinearSystem substitution — alias `systems_substitution`.
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
