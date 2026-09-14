# `radical_midpoint_formula` — The Midpoint Formula

> **UNCLEAR** — No EA midpoint section; gold is College Algebra 2.1 + old path.

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Linear Equations and Inequalities
- **Generator:** `radical_midpoint_formula`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Midpoint of a segment. D=0: integer midpoint. High D: odd sums → halves.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Find the midpoint of } (-2, 3) \text{ and } (6, -7).`
  - answer: `\left(2, -2\right)`
- seed 207:
  - prompt: `\text{Find the midpoint of } (8, -1) \text{ and } (-3, -8).`
  - answer: `\left(2.5, -4.5\right)`

### D=8

- seed 101:
  - prompt: `\text{Find the midpoint of } (-2, 3) \text{ and } (6, -7).`
  - answer: `\left(2, -2\right)`
- seed 207:
  - prompt: `\text{Find the midpoint of } (8, -1) \text{ and } (-3, -8).`
  - answer: `\left(2.5, -4.5\right)`

### D=16

- seed 101:
  - prompt: `\text{Find the midpoint of } (-2, 3) \text{ and } (6, -7).`
  - answer: `\left(2, -2\right)`
- seed 207:
  - prompt: `\text{Find the midpoint of } (8, -1) \text{ and } (-3, -8).`
  - answer: `\left(2.5, -4.5\right)`

### D=22

- seed 101:
  - prompt: `\text{Find the midpoint of } (-2, 3) \text{ and } (6, -7).`
  - answer: `\left(2, -2\right)`
- seed 207:
  - prompt: `\text{Find the midpoint of } (8, -1) \text{ and } (-3, -8).`
  - answer: `\left(2.5, -4.5\right)`

## OpenStax examples + chapter/section cites

### College Algebra 2e — 2.1 The Rectangular Coordinate Systems and Graphs

- https://openstax.org/books/college-algebra-2e/pages/2-1-the-rectangular-coordinate-systems-and-graphs
- Shape: M=((x1+x2)/2,(y1+y2)/2).

### Elementary Algebra 2e — 4.1 Use the Rectangular Coordinate System

- https://openstax.org/books/elementary-algebra-2e/pages/4-1-use-the-rectangular-coordinate-system
- Mined examples:
  - Example 4.1: Plot each point in the rectangular coordinate system and identify the quadrant in which the point is located: ⓐ $(−5 , 4)$ ⓑ $(−3 , −4)$ ⓒ $(2 , −3)$ ⓓ $(−2 , 3)$ ⓔ $\left(\right. 3 , \frac{5}{2} \left.\right)$ .
  - Example 4.2: Plot each point: ⓐ $(0 , 5)$ ⓑ $(4 , 0)$ ⓒ $(−3 , 0)$ ⓓ $(0 , 0)$ ⓔ $(0 , −1)$ .
  - Example 4.3: Name the ordered pair of each point shown in the rectangular coordinate system.
  - Example 4.4: Determine which ordered pairs are solutions to the equation $x + 4 y = 8$ . ⓐ $(0 , 2)$ ⓑ $(2 , −4)$ ⓒ $(−4 , 3)$

## Variety notes

No EA midpoint section; gold is College Algebra 2.1 + old path.

## Limitations

- UNCLEAR / LIMITATIONS: no EA midpoint section; College Algebra §2.1 + old path.

## Proposed engine (reuse vs new)

Reuse radical_midpoint_formula (geometry). Not a radical leaf despite the prefix.

_Proposal only. No engine implementation in this notes pass._
