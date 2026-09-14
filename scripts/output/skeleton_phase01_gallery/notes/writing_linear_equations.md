# `writing_linear_equations` — Writing linear equations

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Linear Equations and Inequalities
- **Generator:** `writing_linear_equations`
- **Already on skeleton?** yes (`WriteLinear`; shared with `pa_writing_linear_equations`)
- **Old-path extra settings:** none (live is linear_forms).

## What the question should look like (D=0 vs high D)

Write the equation of a line. D=0: given m and b → y=mx+b. High D: two points / point-slope / parallel.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Write } 12x - 4y = 8 \text{ in slope-intercept form.}`
  - answer: `y = 3x - 2`
- seed 207:
  - prompt: `\text{Write } y + 1 = 2(x + 3) \text{ in slope-intercept form.}`
  - answer: `y = 2x + 5`

### D=8

- seed 101:
  - prompt: `\text{Write } -3x - y = -3 \text{ in slope-intercept form.}`
  - answer: `y = -3x + 3`
- seed 207:
  - prompt: `\text{Write } y + 33 = 4(x + 8) \text{ in slope-intercept form.}`
  - answer: `y = 4x - 1`

### D=16

- seed 101:
  - prompt: `\text{Write } -16x - 4y = -20 \text{ in slope-intercept form.}`
  - answer: `y = -4x + 5`
- seed 207:
  - prompt: `\text{Write } y + 113 = 9(x + 12) \text{ in slope-intercept form.}`
  - answer: `y = 9x - 5`

### D=22

- seed 101:
  - prompt: `\text{Write } -16x - 4y = -20 \text{ in slope-intercept form.}`
  - answer: `y = -4x + 5`
- seed 207:
  - prompt: `\text{Write } y + 113 = 9(x + 12) \text{ in slope-intercept form.}`
  - answer: `y = 9x - 5`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 4.6 Find the Equation of a Line

- https://openstax.org/books/elementary-algebra-2e/pages/4-6-find-the-equation-of-a-line
- Mined examples:
  - Example 4.57: Find an equation of a line with slope $−7$ and y -intercept $(0 , −1)$ .
  - Example 4.58: Find the equation of the line shown.
  - Example 4.59: Find an Equation of a Line Given the Slope and a Point Find an equation of a line with slope $m = \frac{2}{5}$ that contains the point $(10 , 3)$ . Write the equation in slope–intercept form.
  - Example 4.60: Find an equation of a line with slope $m = - \frac{1}{3}$ that contains the point $(6 , −4)$ . Write the equation in slope–intercept form.

### Elementary Algebra 2e — 4.5 Use the Slope-Intercept Form of an Equation of a Line

- https://openstax.org/books/elementary-algebra-2e/pages/4-5-use-the-slope-intercept-form-of-an-equation-of-a-line
- Mined examples:
  - Example 4.40: Use the graph to find the slope and y -intercept of the line, $y = 2 x + 1$ . Compare these values to the equation $y = m x + b$ .
  - Example 4.41: Identify the slope and y -intercept of the line with equation $y = −3 x + 5$ .
  - Example 4.42: Identify the slope and y -intercept of the line with equation $x + 2 y = 6$ .
  - Example 4.43: How to Graph a Line Using its Slope and Intercept Graph the line of the equation $y = 4 x - 2$ using its slope and y -intercept.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- LIMITATIONS: shared with `pa_writing_linear_equations`. A2 write-linear converts forms; keep A1 as write-from-m/b/points.

## Proposed engine (reuse vs new)

Reuse writing_linear_equations. Not SolveLinear.

_Proposal only. No engine implementation in this notes pass._
