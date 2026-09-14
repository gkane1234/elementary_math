# `age_word_problems` — Age word problems

- **Course:** Algebra 1 (A1 catalog)
- **Category:** Algebra 1 — Equations
- **Generator:** `wp_age`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Now / in-n-years / n-years-ago. D=0: one is k years older; sum is S. High D: both-in-the-future. Story, not “the equation is $x+(x+k)=S$”.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Taylor is 7 years older than Riley. The sum of their ages is 23 years. How old is Riley?}`
  - answer: `8`
- seed 207:
  - prompt: `\text{Riley is 2 years older than Taylor. The sum of their ages is 22 years. How old is Taylor?}`
  - answer: `10`

### D=8

- seed 101:
  - prompt: `\text{Quinn is 5 years older than Alex. 6 years ago, the sum of their ages was 49 years. How old is Alex?}`
  - answer: `28`
- seed 207:
  - prompt: `\text{Sam is twice as old as Alex. The sum of their ages is 54 years. How old is Alex?}`
  - answer: `18`

### D=16

- seed 101:
  - prompt: `\text{Quinn is 5 years older than Alex. 6 years ago, the sum of their ages was 49 years. How old is Quinn?}`
  - answer: `33`
- seed 207:
  - prompt: `\text{Sam is 3 years older than Alex. Taylor is 7 years older than Alex. The sum of their ages is 79 years. How old is Alex?}`
  - answer: `23`

### D=22

- seed 101:
  - prompt: `\text{Quinn is 5 years older than Alex. 6 years ago, the sum of their ages was 49 years. How old is Quinn?}`
  - answer: `33`
- seed 207:
  - prompt: `\text{Sam is 3 years older than Alex. Taylor is 7 years older than Alex. The sum of their ages is 79 years. How old is Alex?}`
  - answer: `23`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 3.1 Use a Problem-Solving Strategy

- https://openstax.org/books/elementary-algebra-2e/pages/3-1-use-a-problem-solving-strategy
- Shape: Number/age translate-then-solve (one equation).

### Elementary Algebra 2e — 5.4 Solve Applications with Systems of Equations

- https://openstax.org/books/elementary-algebra-2e/pages/5-4-solve-applications-with-systems-of-equations
- Mined examples:
  - Example 5.35: How to Translate to a System of Equations Translate to a system of equations: The sum of two numbers is negative fourteen. One number is four less than the other. Find the numbers.
  - Example 5.36: Translate to a system of equations: A married couple together earns $110,000 a year. The wife earns $16,000 less than twice what her husband earns. What does the husband earn?
  - Example 5.37: Translate to a system of equations and then solve: Devon is 26 years older than his son Cooper. The sum of their ages is 50. Find their ages.
  - Example 5.38: Translate to a system of equations and then solve: When Jenna spent 10 minutes on the elliptical trainer and then did circuit training for 20 minutes, her fitness app says she burned 278 calories. When she spent 20 minutes on the elliptical trainer and 30 minutes circuit train…
- Shape: Example 5.37 is an age *system* — keep two-variable ages on systems WP.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `age_word_problems` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse AgeProblemFramework / narrative_wp. One equation, not systems.

_Proposal only. No engine implementation in this notes pass._
