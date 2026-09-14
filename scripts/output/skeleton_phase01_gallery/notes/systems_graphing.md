# `systems_graphing` — Solving by graphing

- **Course:** Algebra 1
- **Category:** Algebra 1 — Systems of Equations and Inequalities
- **Generator:** `graph_system`
- **Already on skeleton?** yes (`LinearSystem`; shared with `pa_graphing_systems_of_equations`)
- **Old-path extra settings:** none (live is the systems skeleton).

## What the question should look like (D=0 vs high D)

Two lines; read the intersection. D=0: integer intercepts, unique solution. High D: parallel / coincident.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (pattern=`LinearSystem`):
  - prompt: `\text{Solve: } \begin{cases} x + 3y = -4 \\ -x + y = 0 \end{cases}\quad \text{Solve by graphing.}`
  - answer: `x = -1,\ y = -1`
- seed 207 (pattern=`LinearSystem`):
  - prompt: `\text{Solve: } \begin{cases} 3x - 3y = 9 \\ -4x + y = -6 \end{cases}\quad \text{Solve by graphing.}`
  - answer: `x = 1,\ y = -2`

### D=8

- seed 101 (pattern=`LinearSystem`):
  - prompt: `\text{Solve: } \begin{cases} 2x + 5y = 3 \\ 4x + 10y = 8 \end{cases}\quad \text{Solve by graphing.}`
  - answer: `\text{no solution}`
- seed 207 (pattern=`LinearSystem`):
  - prompt: `\text{Solve: } \begin{cases} 3x + 2y = 4 \\ 12x + 8y = 14 \end{cases}\quad \text{Solve by graphing.}`
  - answer: `\text{no solution}`

### D=16

- seed 101 (pattern=`LinearSystem`):
  - prompt: `\text{Solve: } \begin{cases} 2x + 5y = 3 \\ 4x + 10y = 8 \end{cases}\quad \text{Solve by graphing.}`
  - answer: `\text{no solution}`
- seed 207 (pattern=`LinearSystem`):
  - prompt: `\text{Solve: } \begin{cases} 3x + 2y = 4 \\ 12x + 8y = 14 \end{cases}\quad \text{Solve by graphing.}`
  - answer: `\text{no solution}`

### D=22

- seed 101 (pattern=`LinearSystem`):
  - prompt: `\text{Solve: } \begin{cases} 2x + 5y = 3 \\ 4x + 10y = 8 \end{cases}\quad \text{Solve by graphing.}`
  - answer: `\text{no solution}`
- seed 207 (pattern=`LinearSystem`):
  - prompt: `\text{Solve: } \begin{cases} 3x + 2y = 4 \\ 12x + 8y = 14 \end{cases}\quad \text{Solve by graphing.}`
  - answer: `\text{no solution}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 5.1 Solve Systems of Equations by Graphing

- https://openstax.org/books/elementary-algebra-2e/pages/5-1-solve-systems-of-equations-by-graphing
- Mined examples:
  - Example 5.1: Determine whether the ordered pair is a solution to the system: $\left{\right. x - y = −1 \\ 2 x - y = −5$ ⓐ $(−2 , −1)$ ⓑ $(−4 , −3)$
  - Example 5.2: How to Solve a System of Linear Equations by Graphing Solve the system by graphing: $\left{\right. 2 x + y = 7 \\ x - 2 y = 6 .$
  - Example 5.3: Solve the system by graphing: $\left{\right. y = 2 x + 1 \\ y = 4 x - 1 .$
  - Example 5.4: Solve the system by graphing: $\left{\right. 3 x + y = −1 \\ 2 x + y = 0 .$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- LIMITATIONS: gallery primarily under `pa_graph_systems`; diagram fidelity vs algebraic intersection answer.

## Proposed engine (reuse vs new)

Reuse graph_system. Graph engine, not substitution algebra.

_Proposal only. No engine implementation in this notes pass._
