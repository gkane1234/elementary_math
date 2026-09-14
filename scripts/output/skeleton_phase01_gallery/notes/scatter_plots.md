# `scatter_plots` — Scatter plots

> **UNCLEAR / LOW_VARIETY** — No EA scatter-plot section. Old path is one Mad-Lib (hours studied vs test score) plus predict-from-y=mx+b.

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Statistics
- **Generator:** `scatter_plot_interpret`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Read a scatter plot: association direction, or identify a point. D=0: positive/negative/none.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{A scatter plot of hours studied vs. test score shows a negative linear trend. What type of association is this?}`
  - answer: `\text{negative association}`
- seed 207:
  - prompt: `\text{A linear model for a scatter plot is } y = 3x + 22. \text{Predict } y \text{ when } x = 5.`
  - answer: `37`

### D=8

- seed 101:
  - prompt: `\text{A scatter plot of hours studied vs. test score shows a no clear linear trend. What type of association is this?}`
  - answer: `\text{none association}`
- seed 207:
  - prompt: `\text{A scatter plot of hours studied vs. test score shows a positive linear trend. What type of association is this?}`
  - answer: `\text{positive association}`

### D=16

- seed 101:
  - prompt: `\text{A linear model for a scatter plot is } y = 2x + 26. \text{Predict } y \text{ when } x = 8.`
  - answer: `42`
- seed 207:
  - prompt: `\text{A scatter plot of hours studied vs. test score shows a no clear linear trend. What type of association is this?}`
  - answer: `\text{none association}`

### D=22

- seed 101:
  - prompt: `\text{A scatter plot of hours studied vs. test score shows a negative linear trend. What type of association is this?}`
  - answer: `\text{negative association}`
- seed 207:
  - prompt: `\text{A linear model for a scatter plot is } y = 5x + 30. \text{Predict } y \text{ when } x = 8.`
  - answer: `70`

## OpenStax examples + chapter/section cites

### College Algebra 2e — 2.1 The Rectangular Coordinate Systems and Graphs

- https://openstax.org/books/college-algebra-2e/pages/2-1-the-rectangular-coordinate-systems-and-graphs
- Shape: Nearest algebra text is plotting pairs — not scatter association.

## Variety notes

**UNCLEAR / LOW_VARIETY** — No EA scatter-plot section. Old path is one Mad-Lib (hours studied vs test score) plus predict-from-y=mx+b.

## Limitations

- LOW_VARIETY / LIMITATIONS: interpretation variety may be thin; flag if one Mad-Lib stem.

## Proposed engine (reuse vs new)

Reuse scatter_plot_interpret. Not linear-regression modeling (curriculum gap).

_Proposal only. No engine implementation in this notes pass._
