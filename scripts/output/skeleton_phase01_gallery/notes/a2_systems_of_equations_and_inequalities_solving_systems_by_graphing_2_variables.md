# Notes — `a2_systems_of_equations_and_inequalities_solving_systems_by_graphing_2_variables`

> **UNCLEAR / NOT_IMPLEMENTED** — see Limitations.



- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Systems of Equations and Inequalities
- **Generator:** `graph_system`
- **Suggested family:** `systems`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Small-integer coefficients; unique solution.
- **D=0:** Small-integer coefficients; unique solution.
- **High D (≈16–22):** Parallel lines → no solution at D≥16.
- **Must not:** Three-variable; WP dump.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (LinearSystem skeleton)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Solve: } \begin{cases} -x - y = 1 \\ x - y = -3 \end{cases}\quad \text{Solve by graphing.}$ | $x = -2,\ y = 1$ | pattern=LinearSystem |
| 0 | 207 | $\text{Solve: } \begin{cases} 2x - y = 0 \\ -3x - y = 5 \end{cases}\quad \text{Solve by graphing.}$ | $x = -1,\ y = -2$ | pattern=LinearSystem |
| 8 | 101 | $\text{Solve: } \begin{cases} x + 3y = -4 \\ -x + y = 0 \end{cases}\quad \text{Solve by graphing.}$ | $x = -1,\ y = -1$ | pattern=LinearSystem |
| 8 | 207 | $\text{Solve: } \begin{cases} 3x - 3y = 9 \\ -4x + y = -6 \end{cases}\quad \text{Solve by graphing.}$ | $x = 1,\ y = -2$ | pattern=LinearSystem |
| 16 | 101 | $\text{Solve: } \begin{cases} 2x + 3y = 2 \\ 10x + 15y = 11 \end{cases}\quad \text{Solve by graphing.}$ | $\text{no solution}$ | pattern=LinearSystem |
| 16 | 207 | $\text{Solve: } \begin{cases} 6x + 4y = 1 \\ 12x + 8y = 3 \end{cases}\quad \text{Solve by graphing.}$ | $\text{no solution}$ | pattern=LinearSystem |
| 22 | 101 | $\text{Solve: } \begin{cases} 2x + 3y = 6 \\ 10x + 15y = 29 \end{cases}\quad \text{Solve by graphing.}$ | $\text{no solution}$ | pattern=LinearSystem |
| 22 | 207 | $\text{Solve: } \begin{cases} 6x + 4y = 1 \\ 12x + 8y = 3 \end{cases}\quad \text{Solve by graphing.}$ | $\text{no solution}$ | pattern=LinearSystem |

Opt-out flag used: `none (LinearSystem skeleton)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §5.1 | https://openstax.org/books/elementary-algebra-2e/pages/5-1-solve-systems-of-equations-by-graphing | Graph two lines; read intersection |
| OpenStax Intermediate Algebra 2e §4.1 | https://openstax.org/books/intermediate-algebra-2e/pages/4-1-solve-systems-of-equations-by-graphing | IA graphing systems |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** LinearSystem graphing method.
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
