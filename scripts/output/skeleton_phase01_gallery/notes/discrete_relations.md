# `discrete_relations` — Discrete relations

> **UNCLEAR / LOW_VARIETY** — Old path is “complete the table for y=mx+b” (one missing cell). That is not a discrete relation (ordered pairs / domain-range / function test). IA 3.5 is the gold; old path is a linear-evaluate table.

- **Course:** Algebra 1
- **Category:** Algebra 1 — Relations and Introduction to Functions
- **Generator:** `discrete_relations`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Relation as a set of pairs: evaluate, domain/range, or function yes/no. D=0: 3–4 pairs. High D: mapping diagram language.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Complete the table for } y = x - 1. \\ \begin{array}{|c|c|} \hline x & y \\ \hline 0 & ? \\ 2 & 1 \\ 3 & 2 \\ \hline \end{array}`
  - answer: `-1`
- seed 207:
  - prompt: `\text{Complete the table for } y = x - 1. \\ \begin{array}{|c|c|} \hline x & y \\ \hline -5 & ? \\ -3 & -4 \\ 0 & -1 \\ \hline \end{array}`
  - answer: `-6`

### D=8

- seed 101:
  - prompt: `\text{Complete the table for } y = 3x - 2. \\ \begin{array}{|c|c|} \hline x & y \\ \hline -8 & -26 \\ 2 & ? \\ 3 & 7 \\ 6 & 16 \\ \hline \end{array}`
  - answer: `4`
- seed 207:
  - prompt: `\text{Complete the table for } y = 2x - 1. \\ \begin{array}{|c|c|} \hline x & y \\ \hline -8 & -17 \\ -3 & ? \\ 2 & 3 \\ 8 & 15 \\ \hline \end{array}`
  - answer: `-7`

### D=16

- seed 101:
  - prompt: `\text{Complete the table for } y = -2x + 3. \\ \begin{array}{|c|c|} \hline x & y \\ \hline -7 & 17 \\ -5 & 13 \\ 0 & 3 \\ 2 & -1 \\ 6 & ? \\ \hline \end{array}`
  - answer: `-9`
- seed 207:
  - prompt: `\text{Complete the table for } y = 8x - 1. \\ \begin{array}{|c|c|} \hline x & y \\ \hline -8 & -65 \\ -6 & -49 \\ -3 & -25 \\ 2 & ? \\ 8 & 63 \\ \hline \end{array}`
  - answer: `15`

### D=22

- seed 101:
  - prompt: `\text{Complete the table for } y = 8x - 4. \\ \begin{array}{|c|c|} \hline x & y \\ \hline -9 & -76 \\ -4 & -36 \\ 1 & 4 \\ 4 & 28 \\ 6 & ? \\ 7 & 52 \\ \hline \end{array}`
  - answer: `44`
- seed 207:
  - prompt: `\text{Complete the table for } y = 6x + 9. \\ \begin{array}{|c|c|} \hline x & y \\ \hline -10 & ? \\ -6 & -27 \\ -5 & -21 \\ -3 & -9 \\ 1 & 15 \\ 5 & 39 \\ \hline \end{array}`
  - answer: `-51`

## OpenStax examples + chapter/section cites

### Intermediate Algebra 2e — 3.5 Relations and Functions

- https://openstax.org/books/intermediate-algebra-2e/pages/3-5-relations-and-functions
- Shape: Domain/range of {(1,2),(3,4)}; vertical-line / function test.

### Elementary Algebra 2e — 4.1 Use the Rectangular Coordinate System

- https://openstax.org/books/elementary-algebra-2e/pages/4-1-use-the-rectangular-coordinate-system
- Mined examples:
  - Example 4.1: Plot each point in the rectangular coordinate system and identify the quadrant in which the point is located: ⓐ $(−5 , 4)$ ⓑ $(−3 , −4)$ ⓒ $(2 , −3)$ ⓓ $(−2 , 3)$ ⓔ $\left(\right. 3 , \frac{5}{2} \left.\right)$ .
  - Example 4.2: Plot each point: ⓐ $(0 , 5)$ ⓑ $(4 , 0)$ ⓒ $(−3 , 0)$ ⓓ $(0 , 0)$ ⓔ $(0 , −1)$ .
  - Example 4.3: Name the ordered pair of each point shown in the rectangular coordinate system.
  - Example 4.4: Determine which ordered pairs are solutions to the equation $x + 4 y = 8$ . ⓐ $(0 , 2)$ ⓑ $(2 , −4)$ ⓒ $(−4 , 3)$
- Shape: EA 4.1 is plotting; relations/functions are IA 3.5.

## Variety notes

**UNCLEAR / LOW_VARIETY** — Old path is “complete the table for y=mx+b” (one missing cell). That is not a discrete relation (ordered pairs / domain-range / function test). IA 3.5 is the gold; old path is a linear-evaluate table.

## Limitations

- UNCLEAR / LOW_VARIETY / LIMITATIONS: old path is complete-a-table for y=mx+b, not ordered-pairs / function test (IA §3.5).
- NOT_IMPLEMENTED as discrete-relation skill until gold locked.

## Proposed engine (reuse vs new)

Reuse discrete_relations. Not graphing a continuous line.

_Proposal only. No engine implementation in this notes pass._
