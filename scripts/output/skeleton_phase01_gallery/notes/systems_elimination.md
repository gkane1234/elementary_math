# `systems_elimination` — Solving by elimination

- **Course:** Algebra 1 (A1 catalog)
- **Category:** Algebra 1 — Systems of Equations and Inequalities
- **Generator:** `systems_elimination`
- **Already on skeleton?** yes (`LinearSystem`)
- **Old-path extra settings:** none (live is the systems skeleton).

## What the question should look like (D=0 vs high D)

D=0: already opposite coeffs ($x+y=5$, $x-y=1$) or one add. High D: multiply one/both equations first; later no-solution / infinite. Prompt is the system, not a story.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\begin{cases} 2x - 5y = -19 \\ 5x + 3y = -1 \end{cases}`
  - answer: `(x, y) = (-2, 3)`
- seed 207:
  - prompt: `\begin{cases} -3x - 5y = -19 \\ 5x - 3y = 43 \end{cases}`
  - answer: `(x, y) = (8, -1)`

### D=8

- seed 101:
  - prompt: `\begin{cases} 4x - 9y = -35 \\ 6x - 4y = -24 \end{cases}`
  - answer: `(x, y) = (-2, 3)`
- seed 207:
  - prompt: `\begin{cases} -5x - 10y = -30 \\ x - 6y = 14 \end{cases}`
  - answer: `(x, y) = (8, -1)`

### D=16

- seed 101:
  - prompt: `\begin{cases} -x - 14y = -40 \\ 6x + y = -9 \end{cases}`
  - answer: `(x, y) = (-2, 3)`
- seed 207:
  - prompt: `\begin{cases} 8x - 10y = 74 \\ -15x + 6y = -126 \end{cases}`
  - answer: `(x, y) = (8, -1)`

### D=22

- seed 101:
  - prompt: `\begin{cases} -x - 14y = -40 \\ 6x + y = -9 \end{cases}`
  - answer: `(x, y) = (-2, 3)`
- seed 207:
  - prompt: `\begin{cases} 8x - 10y = 74 \\ -15x + 6y = -126 \end{cases}`
  - answer: `(x, y) = (8, -1)`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 5.3 Solve Systems of Equations by Elimination

- https://openstax.org/books/elementary-algebra-2e/pages/5-3-solve-systems-of-equations-by-elimination
- Mined examples:
  - Example 5.25: How to Solve a System of Equations by Elimination Solve the system by elimination. $\left{\right. 2 x + y = 7 \\ x - 2 y = 6$
  - Example 5.26: Solve the system by elimination. $\left{\right. x + y = 10 \\ x - y = 12$
  - Example 5.27: Solve the system by elimination. $\left{\right. 3 x - 2 y = −2 \\ 5 x - 6 y = 10$
  - Example 5.28: Solve the system by elimination. $\left{\right. 4 x - 3 y = 9 \\ 7 x + 2 y = −6$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `systems_elimination` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse systems_elimination. New LinearSystem skeleton only if later A1 unification needs it — not this notes pass.

_Proposal only. No engine implementation in this notes pass._
