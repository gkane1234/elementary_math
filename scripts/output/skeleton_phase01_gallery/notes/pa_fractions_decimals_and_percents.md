# `pa_fractions_decimals_and_percents` — Fractions, decimals, and percents

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Percents
- **Generator:** `fractions_decimals_and_percents`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Conversion triad. D=0: 25% ↔ 1/4 ↔ 0.25. High D: percents >100 or repeating decimals.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Write } 0.7 \text{ as a fraction in simplest form.}`
  - answer: `\frac{7}{10}`
- seed 207:
  - prompt: `\text{Write } \frac{3}{10} \text{ as a decimal.}`
  - answer: `0.3`

### D=8

- seed 101:
  - prompt: `\text{Write } \frac{4}{5} \text{ as a decimal.}`
  - answer: `0.8`
- seed 207:
  - prompt: `\text{Write } 0.1 \text{ as a fraction in simplest form.}`
  - answer: `\frac{1}{10}`

### D=16

- seed 101:
  - prompt: `\text{Write } 80\% \text{ as a decimal.}`
  - answer: `0.8`
- seed 207:
  - prompt: `\text{Write } 44\% \text{ as a decimal.}`
  - answer: `0.44`

### D=22

- seed 101:
  - prompt: `\text{Write } 45\% \text{ as a fraction in simplest form.}`
  - answer: `\frac{9}{20}`
- seed 207:
  - prompt: `\text{Write } 0.0625 \text{ as a fraction in simplest form.}`
  - answer: `\frac{1}{16}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 6.1 Understand Percent

- https://openstax.org/books/prealgebra-2e/pages/6-1-understand-percent
- Mined examples:
  - Example 6.1: According to the Public Policy Institute of California $(2010) , \text{44}\%$ of parents of public school children would like their youngest child to earn a graduate degree. Write this percent as a ratio.
  - Example 6.2: In $2007 ,$ according to a U.S. Department of Education report, $21$ out of every $100$ first-time freshmen college students at $\text{4}-\text{year}$ public institutions took at least one remedial course. Write this as a ratio and then as a percent.
  - Example 6.3: Convert each percent to a fraction: ⓐ $\text{36}\%$ ⓑ $\text{125}\%$
  - Example 6.4: Convert each percent to a fraction: ⓐ $\text{24}.\text{5}\%$ ⓑ $33 \frac{1}{3} \%$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse fractions_decimals_and_percents (number). No new engine.

_Proposal only. No engine implementation in this notes pass._
