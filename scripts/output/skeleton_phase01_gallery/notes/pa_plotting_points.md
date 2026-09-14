# `pa_plotting_points` — Plotting points

> **UNCLEAR** — Old prompt is a bare ordered pair `(4, -2)` (prompt = answer). OpenStax 11.1 / EA 4.1 also name quadrants and plot several points.

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Linear Equations and Inequalities
- **Generator:** `plotting_points`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: plot one or two points in Q1 with integer coords. High D: other quadrants, axes, several points. Identify quadrant language from PA 11.1 / EA 4.1.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `(4, -2)`
  - answer: `(4, -2)`
- seed 207:
  - prompt: `(3, 5)`
  - answer: `(3, 5)`

### D=8

- seed 101:
  - prompt: `(-2, 3)`
  - answer: `(-2, 3)`
- seed 207:
  - prompt: `(8, -1)`
  - answer: `(8, -1)`

### D=16

- seed 101:
  - prompt: `(6, -6)`
  - answer: `(6, -6)`
- seed 207:
  - prompt: `(4, 9)`
  - answer: `(4, 9)`

### D=22

- seed 101:
  - prompt: `(6, -6)`
  - answer: `(6, -6)`
- seed 207:
  - prompt: `(4, 9)`
  - answer: `(4, 9)`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 11.1 Use the Rectangular Coordinate System

- https://openstax.org/books/prealgebra-2e/pages/11-1-use-the-rectangular-coordinate-system
- Shape: Plot (3,5); name the quadrant of (−2,4).

### Elementary Algebra 2e — 4.1 Use the Rectangular Coordinate System

- https://openstax.org/books/elementary-algebra-2e/pages/4-1-use-the-rectangular-coordinate-system
- Mined examples:
  - Example 4.1: Plot each point in the rectangular coordinate system and identify the quadrant in which the point is located: ⓐ $(−5 , 4)$ ⓑ $(−3 , −4)$ ⓒ $(2 , −3)$ ⓓ $(−2 , 3)$ ⓔ $\left(\right. 3 , \frac{5}{2} \left.\right)$ .
  - Example 4.2: Plot each point: ⓐ $(0 , 5)$ ⓑ $(4 , 0)$ ⓒ $(−3 , 0)$ ⓓ $(0 , 0)$ ⓔ $(0 , −1)$ .
  - Example 4.3: Name the ordered pair of each point shown in the rectangular coordinate system.
  - Example 4.4: Determine which ordered pairs are solutions to the equation $x + 4 y = 8$ . ⓐ $(0 , 2)$ ⓑ $(2 , −4)$ ⓒ $(−4 , 3)$

## Variety notes

Worksheet instruction is “Plot the following points,” so a bare pair may be enough with a grid. OpenStax also asks which quadrant and to plot a list. High D did not add more points or quadrant language in these samples.

## Limitations

- Flags: **UNCLEAR**.
- Worksheet instruction is “Plot the following points,” so a bare pair may be enough with a grid. OpenStax also asks which quadrant and to plot a list. High D did not add more points or quadrant language in these samples.

## Proposed engine (reuse vs new)

Reuse plotting_points (geometry/coordinate). Not SolveLinear.

_Proposal only. No engine implementation in this notes pass._
