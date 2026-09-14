# `pa_fractions_divide` — Dividing fractions

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `g6_fraction_divide`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: ÷ a unit fraction (multiply by reciprocal). High D: cancel across the reciprocal.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\frac{1}{3} \div \frac{1}{6}`
  - answer: `2`
- seed 207:
  - prompt: `\frac{1}{3} \div \frac{1}{6}`
  - answer: `2`

### D=8

- seed 101:
  - prompt: `\frac{6}{35} \div \frac{2}{21}`
  - answer: `\frac{9}{5}`
- seed 207:
  - prompt: `\left(\frac{21}{10}\right) / \left(\frac{14}{10}\right)`
  - answer: `\frac{3}{2}`

### D=16

- seed 101:
  - prompt: `\frac{\frac{8}{42}}{\frac{14}{18}}`
  - answer: `\frac{12}{49}`
- seed 207:
  - prompt: `\frac{78}{70} \div \frac{91}{28}`
  - answer: `\frac{12}{35}`

### D=22

- seed 101:
  - prompt: `\frac{\frac{20}{24}}{\frac{12}{16}}`
  - answer: `\frac{10}{9}`
- seed 207:
  - prompt: `\frac{26}{108} \div \frac{78}{126}`
  - answer: `\frac{7}{18}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 4.2 Multiply and Divide Fractions

- https://openstax.org/books/prealgebra-2e/pages/4-2-multiply-and-divide-fractions
- Mined examples:
  - Example 4.19: Simplify: $\frac{10}{15} .$
  - Example 4.20: Simplify: $- \frac{18}{24} .$
  - Example 4.21: Simplify: $- \frac{56}{32} .$
  - Example 4.22: Simplify: $\frac{210}{385} .$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse g6_fraction_divide (number).

_Proposal only. No engine implementation in this notes pass._
