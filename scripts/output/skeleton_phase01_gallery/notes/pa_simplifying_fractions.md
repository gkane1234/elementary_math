# `pa_simplifying_fractions` — Simplifying fractions

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `simplifying_numeric_fractions`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: cancel a small GCF (10/15 → 2/3). High D: larger GCF / improper leftover, signed fractions. OpenStax 4.1 also has improper↔mixed and models — those are extra.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Simplify } \frac{6}{9}.`
  - answer: `\frac{2}{3}`
- seed 207:
  - prompt: `\text{Simplify } \frac{3}{6}.`
  - answer: `\frac{1}{2}`

### D=8

- seed 101:
  - prompt: `\text{Simplify } \frac{15}{6}.`
  - answer: `\frac{5}{2}`
- seed 207:
  - prompt: `\text{Simplify } \frac{16}{8}.`
  - answer: `2`

### D=16

- seed 101:
  - prompt: `\text{Simplify } \frac{80}{112}.`
  - answer: `\frac{5}{7}`
- seed 207:
  - prompt: `\text{Simplify } \frac{72}{12}.`
  - answer: `6`

### D=22

- seed 101:
  - prompt: `\text{Simplify } \frac{216}{48}.`
  - answer: `\frac{9}{2}`
- seed 207:
  - prompt: `\text{Simplify } \frac{72}{168}.`
  - answer: `\frac{3}{7}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 4.1 Visualize Fractions

- https://openstax.org/books/prealgebra-2e/pages/4-1-visualize-fractions
- Mined examples:
  - Example 4.1: Name the fraction of the shape that is shaded in each of the figures.
  - Example 4.2: Shade $\frac{3}{4}$ of the circle.
  - Example 4.3: Use fraction circles to make wholes using the following pieces: ⓐ $4$ fourths ⓑ $5$ fifths ⓒ $6$ sixths
  - Example 4.4: Use fraction circles to make wholes using the following pieces: ⓐ $3$ halves ⓑ $8$ fifths ⓒ $7$ thirds

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse simplifying_numeric_fractions (number). Mixed/improper conversion is a catalog gap.

_Proposal only. No engine implementation in this notes pass._
