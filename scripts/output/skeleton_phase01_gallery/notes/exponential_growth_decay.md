# `exponential_growth_decay` — Discrete exponential growth and decay word problems

> **UNCLEAR** — Not in Elementary Algebra TOC. Old path already rotates account / bacteria / half-life / find-rate / first-exceed — keep those frames; IA/CA apps are still the gold for wording.

- **Course:** Algebra 1
- **Category:** Algebra 1 — Exponents
- **Generator:** `exponential_growth_decay`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Discrete growth/decay story (population, compound-ish, half-life lite). D=0: one easy growth frame. Several OpenStax contexts — not one vehicle.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{An account with \$50 changes by 10\% growth each year. Find the amount after 3 years.}`
  - answer: `66.55`
- seed 207:
  - prompt: `\text{A bacterial culture of 800 changes by 5\% growth each hour. Find the amount after 2 hours.}`
  - answer: `882`

### D=8

- seed 101:
  - prompt: `\text{A sample of 800 grams becomes 491.30 grams after 3 years of discrete decay. Find the percent decay rate per year.}`
  - answer: `15`
- seed 207:
  - prompt: `\text{An account with \$200 becomes 295.49 dollars after 8 years of discrete growth. Find the percent growth rate per year.}`
  - answer: `5`

### D=16

- seed 101:
  - prompt: `\text{A sample of 512 grams decays by half every 2 years (discrete half-life). How much remains after 8 years?}`
  - answer: `32`
- seed 207:
  - prompt: `\text{A population of 100 grows by 5\% each year. After how many years does it first exceed 149.86 people?}`
  - answer: `9`

### D=22

- seed 101:
  - prompt: `\text{A sample of 512 grams decays by half every 2 years (discrete half-life). How much remains after 8 years?}`
  - answer: `32`
- seed 207:
  - prompt: `\text{A bacterial culture of 50 grows by 5\% each hour. After how many hours does it first exceed 64.73 cells?}`
  - answer: `6`

## OpenStax examples + chapter/section cites

### Intermediate Algebra 2e — 10.2 Evaluate and Graph Exponential Functions

- https://openstax.org/books/intermediate-algebra-2e/pages/10-2-evaluate-and-graph-exponential-functions
- Mined examples:
  - Example 10.10: On the same coordinate system graph $f (x) = 2^{x}$ and $g (x) = 3^{x} .$
  - Example 10.11: On the same coordinate system, graph $f (x) = \left(\right. \frac{1}{2} \left.\right)^{x}$ and $g (x) = \left(\right. \frac{1}{3} \left.\right)^{x} .$
  - Example 10.12: On the same coordinate system graph $f (x) = 2^{x}$ and $g (x) = 2^{x + 1} .$
  - Example 10.13: On the same coordinate system graph $f (x) = 3^{x}$ and $g (x) = 3^{x} - 2 .$
- Shape: Evaluate A=A0 b^t in a context (bacteria, investment).

### College Algebra 2e — 6.1 Exponential Functions

- https://openstax.org/books/college-algebra-2e/pages/6-1-exponential-functions
- Shape: Growth/decay applications; EA has no dedicated exponential-app section.

## Variety notes

**UNCLEAR** — Not in Elementary Algebra TOC. Old path already rotates account / bacteria / half-life / find-rate / first-exceed — keep those frames; IA/CA apps are still the gold for wording.

## Limitations

- UNCLEAR / LIMITATIONS: not in EA TOC; old path already rotates account/bacteria/half-life — keep frames, do not dump equations.

## Proposed engine (reuse vs new)

Need OpenStax-style frames on the existing exponential sampler (wp_packaging-like), not a new math core.

_Proposal only. No engine implementation in this notes pass._
