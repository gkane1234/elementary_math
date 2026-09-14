# `coin_word_problems` — Coin word problems

- **Course:** Algebra 1 (A1 catalog)
- **Category:** Algebra 1 — Equations
- **Generator:** `wp_coin`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Nickels/dimes/quarters value. D=0: two coin types, small counts. High D: three types or a “k more dimes than nickels” clause. Not a dumped value equation.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Taylor has only quarters and nickels in a pocket. There are 4 nickels. The coins are worth \$1.95 in total. How many quarters are there?}`
  - answer: `7`
- seed 207:
  - prompt: `\text{Riley's piggy bank holds only quarters and nickels. There are 4 nickels. The coins are worth \$1.45 in total. How many quarters are there?}`
  - answer: `5`

### D=8

- seed 101:
  - prompt: `\text{A jar contains only quarters and pennies. There are 6 more quarters than pennies. The coins are worth \$2.54 in total. How many quarters are there?}`
  - answer: `10`
- seed 207:
  - prompt: `\text{A jar contains 18 coins, all quarters, dimes, and nickels. There are as many nickels as dimes. The coins are worth \$2.75 in total. How many quarters are there?}`
  - answer: `8`

### D=16

- seed 101:
  - prompt: `\text{A jar contains 20 coins, all quarters and pennies. There are 6 more quarters than pennies. What is the total value of the coins?}`
  - answer: `\$3.32`
- seed 207:
  - prompt: `\text{A jar contains 18 coins, all quarters, dimes, and nickels. There are as many nickels as dimes. The coins are worth \$2.75 in total. How many quarters are there?}`
  - answer: `8`

### D=22

- seed 101:
  - prompt: `\text{A jar contains 20 coins, all quarters and pennies. There are 6 more quarters than pennies. What is the total value of the coins?}`
  - answer: `\$3.32`
- seed 207:
  - prompt: `\text{A jar contains 32 coins, all quarters, dimes, and nickels. There are as many nickels as dimes. The coins are worth \$4.85 in total. How many quarters are there?}`
  - answer: `14`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 3.3 Solve Mixture Applications

- https://openstax.org/books/elementary-algebra-2e/pages/3-3-solve-mixture-applications
- Shape: Coin/ticket value as a mixture application (0.05n+0.10d=…).

### Prealgebra 2e — 9.2 Solve Money Applications

- https://openstax.org/books/prealgebra-2e/pages/9-2-solve-money-applications
- Shape: PA money/tickets/coins — same algebra, simpler numbers at D=0.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `coin_word_problems` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse CoinProblemFramework / narrative_wp. Several coin-type frames.

_Proposal only. No engine implementation in this notes pass._
