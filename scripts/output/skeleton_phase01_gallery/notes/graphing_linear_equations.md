# `graphing_linear_equations` — Graphing linear equations

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Linear Equations and Inequalities
- **Generator:** `graph_linear_equation`
- **Already on skeleton?** yes (`GraphLinear`)
- **Old-path extra settings:** none (live is the graph-linear skeleton).

## What the question should look like (D=0 vs high D)

Graph a line. D=0: y=mx+b with integer intercepts. High D: Ax+By=C, horizontal/vertical.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Graph: } y = x`
  - answer: `y = x`
- seed 207:
  - prompt: `\text{Graph: } y = 3x`
  - answer: `y = 3x`

### D=8

- seed 101:
  - prompt: `\text{Graph: } y = x`
  - answer: `y = x`
- seed 207:
  - prompt: `\text{Graph: } y = 3x`
  - answer: `y = 3x`

### D=16

- seed 101:
  - prompt: `\text{Graph: } y = 2x + 3`
  - answer: `y = 2x + 3`
- seed 207:
  - prompt: `\text{Graph: } y = 3x`
  - answer: `y = 3x`

### D=22

- seed 101:
  - prompt: `\text{Graph: } y = 2x + 3`
  - answer: `y = 2x + 3`
- seed 207:
  - prompt: `\text{Graph: } y = 3x`
  - answer: `y = 3x`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 4.2 Graph Linear Equations in Two Variables

- https://openstax.org/books/elementary-algebra-2e/pages/4-2-graph-linear-equations-in-two-variables
- Mined examples:
  - Example 4.10: The graph of $y = 2 x - 3$ is shown. For each ordered pair, decide: ⓐ Is the ordered pair a solution to the equation? ⓑ Is the point on the line? A $(0 , −3)$ B $(3 , 3)$ C $(2 , −3)$ D $(−1 , −5)$
  - Example 4.11: How To Graph an Equation By Plotting Points Graph the equation $y = 2 x + 1$ by plotting points.
  - Example 4.12: Graph the equation $y = −3 x$ .
  - Example 4.13: Graph the equation $y = \frac{1}{2} x + 3$ .

### Elementary Algebra 2e — 4.3 Graph with Intercepts

- https://openstax.org/books/elementary-algebra-2e/pages/4-3-graph-with-intercepts
- Mined examples:
  - Example 4.19: Find the x - and y - intercepts on each graph.
  - Example 4.20: Find the intercepts of $2 x + y = 6$ .
  - Example 4.21: Find the intercepts of $4 x – 3 y = 12$ .
  - Example 4.22: How to Graph a Line Using Intercepts Graph $– x + 2 y = 6$ using the intercepts.

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

- Gallery section slug: `graphing_linear_equations` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse graph_linear_equation. Intercept vs slope-intercept is a D/format unlock on the same engine.

_Proposal only. No engine implementation in this notes pass._
