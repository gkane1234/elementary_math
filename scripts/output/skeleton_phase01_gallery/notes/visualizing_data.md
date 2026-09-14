# `visualizing_data` — Visualizing data

> **UNCLEAR** — No EA/IA stats chapter. Gold is old path + G6 display notes, not an OpenStax algebra section.

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Statistics
- **Generator:** `stats_dot_plot_read`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Read a dot plot / bar / simple display. D=0: count a category. High D: compare two bars.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{The dot plot shows the data set below. How many dots are at } 6\text{?}\\\text{Data: } \{4,\ 6,\ 8,\ 1,\ 4,\ 4\}`
  - answer: `1`
- seed 207:
  - prompt: `\text{The dot plot shows the data set below. How many dots are at } 1\text{?}\\\text{Data: } \{4,\ 3,\ 1,\ 6,\ 3,\ 8\}`
  - answer: `1`

### D=8

- seed 101:
  - prompt: `\text{The dot plot shows the data set below. How many dots are at } 17\text{?}\\\text{Data: } \{7,\ 18,\ 12,\ 15,\ 2,\ 22,\ 17,\ 7,\ 20\}`
  - answer: `1`
- seed 207:
  - prompt: `\text{The dot plot shows the data set below. How many more dots are at } 22\text{ than at } 1\text{?}\\\text{Data: } \{22,\ 22,\ 20,\ 8,\ 6,\ 1,\ 22,\ 12,\ 5\}`
  - answer: `2`

### D=16

- seed 101:
  - prompt: `\text{The dot plot shows the data set below. How many dots are there in all?}\\\text{Data: } \{35,\ 23,\ 30,\ 4,\ 33,\ 14,\ 15,\ 19,\ 32,\ 14,\ 22\}`
  - answer: `11`
- seed 207:
  - prompt: `\text{The dot plot shows the data set below. What value has the most dots?}\\\text{Data: } \{15,\ 11,\ 2,\ 23,\ 10,\ 32,\ 6,\ 4,\ 21,\ 24,\ 9\}`
  - answer: `15`

### D=22

- seed 101:
  - prompt: `\text{The dot plot shows the data set below. What is the mean?}\\\text{Data: } \{35,\ 23,\ 30,\ 4,\ 43,\ 33,\ 14,\ 39,\ 15,\ 19,\ 32,\ 45\}`
  - answer: `27.67`
- seed 207:
  - prompt: `\text{The dot plot shows the data set below. What is the median?}\\\text{Data: } \{39,\ 15,\ 11,\ 2,\ 44,\ 23,\ 10,\ 45,\ 32,\ 6,\ 4,\ 21\}`
  - answer: `18`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 1.1 Introduction to Whole Numbers

- https://openstax.org/books/prealgebra-2e/pages/1-1-introduction-to-whole-numbers
- Shape: EA/PA do not have a dedicated stats chapter; G6 notes cover displays.

## Variety notes

No EA/IA stats chapter. Gold is old path + G6 display notes, not an OpenStax algebra section.

## Limitations

- UNCLEAR / LIMITATIONS: diagram-named skill; verify live path actually draws/reads plots.

## Proposed engine (reuse vs new)

Reuse stats_dot_plot_read. Copy old display type; do not invent regression.

_Proposal only. No engine implementation in this notes pass._
