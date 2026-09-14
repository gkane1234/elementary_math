# `pa_factoring` — Factoring

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `g6_factoring`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

This is **numeric** factoring, not polynomial GCF. Live old path is **prime factorization** (OpenStax 2.5), not “list all factor pairs” (2.4). D=0: small n like 10=2·5. High D: larger n with repeated primes.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Write the prime factorization of } 10`
  - answer: `2 \cdot 5`
- seed 207:
  - prompt: `\text{Write the prime factorization of } 15`
  - answer: `3 \cdot 5`

### D=8

- seed 101:
  - prompt: `\text{Write the prime factorization of } 63`
  - answer: `3^{2} \cdot 7`
- seed 207:
  - prompt: `\text{Write the prime factorization of } 30`
  - answer: `2 \cdot 3 \cdot 5`

### D=16

- seed 101:
  - prompt: `\text{Write the prime factorization of } 234`
  - answer: `2 \cdot 3^{2} \cdot 13`
- seed 207:
  - prompt: `\text{Write the prime factorization of } 210`
  - answer: `2 \cdot 3 \cdot 5 \cdot 7`

### D=22

- seed 101:
  - prompt: `\text{Write the prime factorization of } 168`
  - answer: `2^{3} \cdot 3 \cdot 7`
- seed 207:
  - prompt: `\text{Write the prime factorization of } 300`
  - answer: `2^{2} \cdot 3 \cdot 5^{2}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 2.4 Find Multiples and Factors

- https://openstax.org/books/prealgebra-2e/pages/2-4-find-multiples-and-factors
- Shape: List all factors of 24; multiples; prime vs composite. **Not** what the old path emits.

### Prealgebra 2e — 2.5 Prime Factorization and the Least Common Multiple

- https://openstax.org/books/prealgebra-2e/pages/2-5-prime-factorization-and-the-least-common-multiple
- Shape: Write the prime factorization of 48; 36 = 2²·3². This matches the live leaf.

## Variety notes

Old path is prime factorization (2.5), not list-all-factors (2.4). Difficulty ramps |n|. Do not confuse with polynomial FactorProduct.

## Limitations

- Old path is prime factorization (2.5), not list-all-factors (2.4). Difficulty ramps |n|. Do not confuse with polynomial FactorProduct.

## Proposed engine (reuse vs new)

Reuse g6_factoring (number). Do not wire FactorProduct / poly skeleton.

_Proposal only. No engine implementation in this notes pass._
