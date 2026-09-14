# `polynomial_long_division` — Dividing

> **UNCLEAR** — OpenStax splits 6.5 monomial ÷ vs 6.6 long division; one A1 leaf covers both. Confirm old-path mix.

- **Course:** Algebra 1
- **Category:** Algebra 1 — Polynomials
- **Generator:** `polynomial_long_division`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Divide polynomials. D=0: linear÷linear or monomial÷monomial if old path is that easy; else quadratic÷linear with no remainder. High D: missing terms, remainder.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\frac{15x^{2}+25x+10}{5x+5}`
  - answer: `3x+2`
- seed 207:
  - prompt: `\frac{12x^{2}-12}{3x-3}`
  - answer: `4x+4`

### D=8

- seed 101:
  - prompt: `\frac{14x^{2}+14x-28}{2x^{2}+2x-4}`
  - answer: `7`
- seed 207:
  - prompt: `\frac{45x^{2}-33x-42}{9x+6}`
  - answer: `5x-7`

### D=16

- seed 101:
  - prompt: `\frac{15x^{4}-3x^{3}-157x^{2}-56x+158}{5x^{2}+9x-11}`
  - answer: `3x^{2}-6x-14+\frac{4x+4}{5x^{2}+9x-11}`
- seed 207:
  - prompt: `\frac{8x^{4}+54x^{3}+114x^{2}+55x-40}{4x^{2}+7x-4}`
  - answer: `2x^{2}+10x+13+\frac{4x+12}{4x^{2}+7x-4}`

### D=22

- seed 101:
  - prompt: `\frac{117x^{4}-207x^{3}+20x^{2}+88x-82}{9x^{2}-9x+5}`
  - answer: `13x^{2}-10x-15+\frac{3x-7}{9x^{2}-9x+5}`
- seed 207:
  - prompt: `\frac{24x^{5}+119x^{4}+66x^{3}-100x^{2}-193x-40}{3x^{2}+13x+2}`
  - answer: `8x^{3}+5x^{2}-5x-15+\frac{12x-10}{3x^{2}+13x+2}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 6.5 Divide Monomials

- https://openstax.org/books/elementary-algebra-2e/pages/6-5-divide-monomials
- Mined examples:
  - Example 6.59: Simplify: ⓐ $\frac{x^{9}}{x^{7}}$ ⓑ $\frac{3^{10}}{3^{2}} .$
  - Example 6.60: Simplify: ⓐ $\frac{b^{8}}{b^{12}}$ ⓑ $\frac{7^{3}}{7^{5}} .$
  - Example 6.61: Simplify: ⓐ $\frac{a^{5}}{a^{9}}$ ⓑ $\frac{x^{11}}{x^{7}} .$
  - Example 6.62: Simplify: ⓐ $9^{0}$ ⓑ $n^{0} .$
- Shape: OpenStax splits monomial ÷ from long division.

### Elementary Algebra 2e — 6.6 Divide Polynomials

- https://openstax.org/books/elementary-algebra-2e/pages/6-6-divide-polynomials
- Mined examples:
  - Example 6.77: Find the quotient: $\frac{7 y^{2} + 21}{7} .$
  - Example 6.78: Find the quotient: $\left(\right. 18 x^{3} - 36 x^{2} \left.\right) \div 6 x .$
  - Example 6.79: Find the quotient: $\frac{12 d^{2} - 16 d}{−4} .$
  - Example 6.80: Find the quotient: $\frac{105 y^{5} + 75 y^{3}}{5 y^{2}} .$

## Variety notes

OpenStax splits 6.5 monomial ÷ vs 6.6 long division; one A1 leaf covers both. Confirm old-path mix.

## Limitations

- UNCLEAR / LIMITATIONS: one leaf covers EA §6.5 monomial ÷ and §6.6 long division.
- Confirm D ladder mixes both honestly; do not fake difficulty with bigger dividends alone.

## Proposed engine (reuse vs new)

Reuse polynomial_long_division. New engine only if old path cannot match 6.6 honestly — leave the leaf if stuck.

_Proposal only. No engine implementation in this notes pass._
