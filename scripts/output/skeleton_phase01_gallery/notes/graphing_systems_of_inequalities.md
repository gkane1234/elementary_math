# `graphing_systems_of_inequalities` — Graphing systems of inequalities

- **Course:** Algebra 1
- **Category:** Algebra 1 — Systems of Equations and Inequalities
- **Generator:** `graph_system_inequalities`
- **Already on skeleton?** yes (`GraphSystemIneq`)
- **Old-path extra settings:** none (live is the graph-systems-ineq skeleton).

## What the question should look like (D=0 vs high D)

Graph two linear inequalities; shade the overlap. D=0: y>x and y<2. High D: mixed solid/dashed.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Graph the system: } \begin{cases} y \ge -\frac{1}{3}x - \frac{4}{3} \\ y < x \end{cases}`
  - answer: `\begin{cases} y \ge -\frac{1}{3}x - \frac{4}{3} \\ y < x \end{cases}`
- seed 207:
  - prompt: `\text{Graph the system: } \begin{cases} y \le x - 3 \\ y > 4x - 6 \end{cases}`
  - answer: `\begin{cases} y \le x - 3 \\ y > 4x - 6 \end{cases}`

### D=8

- seed 101:
  - prompt: `\text{Graph the system: } \begin{cases} y \ge -\frac{1}{3}x - \frac{4}{3} \\ y < x \end{cases}`
  - answer: `\begin{cases} y \ge -\frac{1}{3}x - \frac{4}{3} \\ y < x \end{cases}`
- seed 207:
  - prompt: `\text{Graph the system: } \begin{cases} y \le x - 3 \\ y > 4x - 6 \end{cases}`
  - answer: `\begin{cases} y \le x - 3 \\ y > 4x - 6 \end{cases}`

### D=16

- seed 101:
  - prompt: `\text{Graph the system: } \begin{cases} y \ge -\frac{1}{3}x - \frac{4}{3} \\ y < x \end{cases}`
  - answer: `\begin{cases} y \ge -\frac{1}{3}x - \frac{4}{3} \\ y < x \end{cases}`
- seed 207:
  - prompt: `\text{Graph the system: } \begin{cases} y \le x - 3 \\ y > 4x - 6 \end{cases}`
  - answer: `\begin{cases} y \le x - 3 \\ y > 4x - 6 \end{cases}`

### D=22

- seed 101:
  - prompt: `\text{Graph the system: } \begin{cases} y \ge -\frac{1}{3}x - \frac{4}{3} \\ y < x \end{cases}`
  - answer: `\begin{cases} y \ge -\frac{1}{3}x - \frac{4}{3} \\ y < x \end{cases}`
- seed 207:
  - prompt: `\text{Graph the system: } \begin{cases} y \le x - 3 \\ y > 4x - 6 \end{cases}`
  - answer: `\begin{cases} y \le x - 3 \\ y > 4x - 6 \end{cases}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 5.6 Graphing Systems of Linear Inequalities

- https://openstax.org/books/elementary-algebra-2e/pages/5-6-graphing-systems-of-linear-inequalities
- Shape: Overlap of two half-planes; test a point in the feasible region.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `graphing_systems_of_inequalities` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse graph_system_inequalities.

_Proposal only. No engine implementation in this notes pass._
