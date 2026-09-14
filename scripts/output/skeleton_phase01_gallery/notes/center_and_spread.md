# `center_and_spread` — Center and spread

> **UNCLEAR** — No EA/IA cite for center/spread. Copy old path; do not invent box-plot IQRs unless old has them.

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Statistics
- **Generator:** `stats_center_spread`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Mean / median / mode / range on a small list. D=0: mean of 3–5 small ints. High D: even-n median.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Find the range of the data set: } \{4,\ 6,\ 8,\ 1,\ 4,\ 4\}.`
  - answer: `7`
- seed 207:
  - prompt: `\text{Find the range of the data set: } \{4,\ 3,\ 1,\ 6,\ 3,\ 8\}.`
  - answer: `7`

### D=8

- seed 101:
  - prompt: `\text{Find the median of the data set: } \{7,\ 18,\ 12,\ 15,\ 2,\ 22,\ 17,\ 7,\ 20\}.`
  - answer: `15`
- seed 207:
  - prompt: `\text{Find the mean of the data set: } \{22,\ 22,\ 20,\ 8,\ 6,\ 1,\ 22,\ 12,\ 5\}.`
  - answer: `13.11`

### D=16

- seed 101:
  - prompt: `\text{Find the mean of the data set: } \{35,\ 23,\ 30,\ 4,\ 33,\ 14,\ 15,\ 19,\ 32,\ 14,\ 22\}.`
  - answer: `21.91`
- seed 207:
  - prompt: `\text{Find the mean of the data set: } \{15,\ 11,\ 2,\ 23,\ 10,\ 32,\ 6,\ 4,\ 21,\ 24,\ 9\}.`
  - answer: `14.27`

### D=22

- seed 101:
  - prompt: `\text{Find the mean of the data set: } \{35,\ 23,\ 30,\ 4,\ 43,\ 33,\ 14,\ 39,\ 15,\ 19,\ 32,\ 45\}.`
  - answer: `27.67`
- seed 207:
  - prompt: `\text{Find the mean of the data set: } \{39,\ 15,\ 11,\ 2,\ 44,\ 23,\ 10,\ 45,\ 32,\ 6,\ 4,\ 12\}.`
  - answer: `20.25`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 1.1 Introduction to Whole Numbers

- https://openstax.org/books/prealgebra-2e/pages/1-1-introduction-to-whole-numbers
- Shape: No PA/EA section for mean/median; Introductory Statistics is the textbook home.

## Variety notes

No EA/IA cite for center/spread. Copy old path; do not invent box-plot IQRs unless old has them.

## Limitations

- UNCLEAR / LIMITATIONS: stats leaf — confirm mean/median/IQR vs miswire.

## Proposed engine (reuse vs new)

Reuse stats_center_spread. Number engine, not algebra.

_Proposal only. No engine implementation in this notes pass._
