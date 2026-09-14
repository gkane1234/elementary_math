# `pa_writing_linear_equations` — Writing linear equations

> **LOW_VARIETY** — Old path only rewrites standard / point-slope → slope-intercept. OpenStax 11.5–11.6 / EA 4.6 also write from m and a point or two points.

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Linear Equations and Inequalities
- **Generator:** `writing_linear_equations`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: given slope and y-intercept → y=mx+b. High D: two points, or point-slope then convert.

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

### Prealgebra 2e — 11.5 Use the Slope-Intercept Form of an Equation of a Line

- https://openstax.org/books/prealgebra-2e/pages/11-5-use-the-slope-intercept-form-of-an-equation-of-a-line
- Shape: Write y=mx+b from m and intercept.

### Prealgebra 2e — 11.6 Find the Equation of a Line

- https://openstax.org/books/prealgebra-2e/pages/11-6-find-the-equation-of-a-line
- Shape: Point-slope / two points.

### Elementary Algebra 2e — 4.6 Find the Equation of a Line

- https://openstax.org/books/elementary-algebra-2e/pages/4-6-find-the-equation-of-a-line
- Mined examples:
  - Example 4.57: Find an equation of a line with slope $−7$ and y -intercept $(0 , −1)$ .
  - Example 4.58: Find the equation of the line shown.
  - Example 4.59: Find an Equation of a Line Given the Slope and a Point Find an equation of a line with slope $m = \frac{2}{5}$ that contains the point $(10 , 3)$ . Write the equation in slope–intercept form.
  - Example 4.60: Find an equation of a line with slope $m = - \frac{1}{3}$ that contains the point $(6 , −4)$ . Write the equation in slope–intercept form.

## Variety notes

Old path only converts standard form or point-slope **into** y=mx+b. OpenStax 11.5–11.6 / EA 4.6 also write from slope+intercept, slope+point, and two points. Harder D only grew coefficients.

## Limitations

- Flags: **LOW_VARIETY**.
- Old path only converts standard form or point-slope **into** y=mx+b. OpenStax 11.5–11.6 / EA 4.6 also write from slope+intercept, slope+point, and two points. Harder D only grew coefficients.

## Proposed engine (reuse vs new)

Reuse writing_linear_equations. Not SolveLinear (that solves for x).

_Proposal only. No engine implementation in this notes pass._
