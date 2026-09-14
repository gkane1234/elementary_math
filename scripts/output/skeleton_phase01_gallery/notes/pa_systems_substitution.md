# `pa_systems_substitution` — Solving systems of equations by substitution

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Linear Equations and Inequalities
- **Generator:** `systems_substitution`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: one equation already solved for y (y=x+1, x+y=5). High D: solve a first equation for a variable, then substitute; maybe fractions later.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\begin{cases} y = x + 5 \\ -5x + 5y = 25 \end{cases}`
  - answer: `(x, y) = (-2, 3)`
- seed 207:
  - prompt: `\begin{cases} y = 5x - 41 \\ -3x - 5y = -19 \end{cases}`
  - answer: `(x, y) = (8, -1)`

### D=8

- seed 101:
  - prompt: `\begin{cases} y = x + 5 \\ -9x + 6y = 36 \end{cases}`
  - answer: `(x, y) = (-2, 3)`
- seed 207:
  - prompt: `\begin{cases} y = 5x - 41 \\ -5x - 10y = -30 \end{cases}`
  - answer: `(x, y) = (8, -1)`

### D=16

- seed 101:
  - prompt: `\begin{cases} y = x + 5 \\ -14x + 6y = 46 \end{cases}`
  - answer: `(x, y) = (-2, 3)`
- seed 207:
  - prompt: `\begin{cases} y = 5x - 41 \\ -10x - 15y = -65 \end{cases}`
  - answer: `(x, y) = (8, -1)`

### D=22

- seed 101:
  - prompt: `\begin{cases} y = x + 5 \\ -14x + 6y = 46 \end{cases}`
  - answer: `(x, y) = (-2, 3)`
- seed 207:
  - prompt: `\begin{cases} y = 5x - 41 \\ -10x - 15y = -65 \end{cases}`
  - answer: `(x, y) = (8, -1)`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 5.2 Solving Systems of Equations by Substitution

- https://openstax.org/books/elementary-algebra-2e/pages/5-2-solving-systems-of-equations-by-substitution
- Mined examples:
  - Example 5.13: How to Solve a System of Equations by Substitution Solve the system by substitution. $\left{\right. 2 x + y = 7 \\ x - 2 y = 6$
  - Example 5.14: Solve the system by substitution. $\left{\right. x + y = −1 \\ y = x + 5$
  - Example 5.15: Solve the system by substitution. $\left{\right. 3 x + y = 5 \\ 2 x + 4 y = −10$
  - Example 5.16: Solve the system by substitution. $\left{\right. x - 2 y = −2 \\ 3 x + 2 y = 34$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse systems_substitution. New systems skeleton only if later A1 unification needs it — not for this notes pass.

_Proposal only. No engine implementation in this notes pass._
