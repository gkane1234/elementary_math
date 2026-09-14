# `quadratic_square_roots` — Solving equations by taking square roots

- **Course:** Algebra 1
- **Category:** Algebra 1 — Quadratic Functions
- **Generator:** `quadratic_square_roots`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Solve by square-root property. D=0: x²=9 → ±3. High D: (x−h)²=k, then a(x−h)²=k.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `x^{2} = 4`
  - answer: `x = \pm 2`
- seed 207:
  - prompt: `(x + 1)^{2} = 4`
  - answer: `x = -1 \pm 2`

### D=8

- seed 101:
  - prompt: `(x + 1)^{2} = 25`
  - answer: `x = -1 \pm 5`
- seed 207:
  - prompt: `(x + 1)^{2} - 9 = 0`
  - answer: `x = -1 \pm 3`

### D=16

- seed 101:
  - prompt: `6(x + 1)^{2} = 120`
  - answer: `x = -1 \pm 2\sqrt{5}`
- seed 207:
  - prompt: `3(x + 6)^{2} = 24`
  - answer: `x = -6 \pm 2\sqrt{2}`

### D=22

- seed 101:
  - prompt: `6(x + 1)^{2} = 120`
  - answer: `x = -1 \pm 2\sqrt{5}`
- seed 207:
  - prompt: `3(x + 6)^{2} = 24`
  - answer: `x = -6 \pm 2\sqrt{2}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 10.1 Solve Quadratic Equations Using the Square Root Property

- https://openstax.org/books/elementary-algebra-2e/pages/10-1-solve-quadratic-equations-using-the-square-root-property
- Mined examples:
  - Example 10.1: Solve: $x^{2} = 169$ .
  - Example 10.2: How to Solve a Quadratic Equation of the Form $\left(a x\right)^{2} = k$ Using the Square Root Property Solve: $x^{2} - 48 = 0$ .
  - Example 10.3: Solve: $5 m^{2} = 80$ .
  - Example 10.4: Solve: $q^{2} + 24 = 0$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `quadratic_square_roots` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse quadratic_square_roots. Do not fold into FactorProduct-solve or quadratic formula.

_Proposal only. No engine implementation in this notes pass._
