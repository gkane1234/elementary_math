# Notes — `a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Systems of Equations and Inequalities
- **Generator:** `systems_elimination`
- **Suggested family:** `systems`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Add/subtract as-is or one multiply.
- **D=0:** Add/subtract as-is or one multiply.
- **High D (≈16–22):** Multiply both equations; larger coeffs.
- **Must not:** Three-variable; substitution-only shapes.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (LinearSystem skeleton)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\begin{cases} 2x - 5y = -19 \\ 5x + 3y = -1 \end{cases}$ | $(x, y) = (-2, 3)$ |  |
| 0 | 207 | $\begin{cases} -3x - 5y = -19 \\ 5x - 3y = 43 \end{cases}$ | $(x, y) = (8, -1)$ |  |
| 8 | 101 | $\begin{cases} 4x - 9y = -35 \\ 6x - 4y = -24 \end{cases}$ | $(x, y) = (-2, 3)$ |  |
| 8 | 207 | $\begin{cases} -5x - 10y = -30 \\ x - 6y = 14 \end{cases}$ | $(x, y) = (8, -1)$ |  |
| 16 | 101 | $\begin{cases} -x - 14y = -40 \\ 6x + y = -9 \end{cases}$ | $(x, y) = (-2, 3)$ |  |
| 16 | 207 | $\begin{cases} 8x - 10y = 74 \\ -15x + 6y = -126 \end{cases}$ | $(x, y) = (8, -1)$ |  |
| 22 | 101 | $\begin{cases} -x - 14y = -40 \\ 6x + y = -9 \end{cases}$ | $(x, y) = (-2, 3)$ |  |
| 22 | 207 | $\begin{cases} 8x - 10y = 74 \\ -15x + 6y = -126 \end{cases}$ | $(x, y) = (8, -1)$ |  |

Opt-out flag used: `none (LinearSystem skeleton)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §5.3 | https://openstax.org/books/elementary-algebra-2e/pages/5-3-solve-systems-of-equations-by-elimination | Ex 5.26 $x+y=10$, $x-y=12$ |
| OpenStax Intermediate Algebra 2e §4.3 | https://openstax.org/books/intermediate-algebra-2e/pages/4-3-solve-systems-of-equations-by-elimination | IA elimination |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** LinearSystem elimination — alias `systems_elimination`.
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
