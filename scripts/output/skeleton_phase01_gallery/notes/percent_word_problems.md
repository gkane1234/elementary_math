# `percent_word_problems` — Percent word problems

- **Course:** Algebra 1 (A1 catalog)
- **Category:** Algebra 1 — Equations
- **Generator:** `wp_percent`
- **Already on skeleton?** yes (OpenStax EA 3.2 percent-of / discount / interest on PercentWordProblemFramework)
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: find the part given percent of a whole (simple interest or discount). High D: mark-up then tax, or solve for the original. Retail/interest stories, not “the equation is $0.2x=12$”.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (pattern=`PercentWP`):
  - prompt: `\text{A store marks up a \$74 item by 10\%. What is the selling price?}`
  - answer: `\$81.40`
- seed 207 (pattern=`PercentWP`):
  - prompt: `\text{A \$109 purchase has 6\% sales tax added. What is the total cost?}`
  - answer: `\$115.54`

### D=8

- seed 101 (pattern=`PercentWP`):
  - prompt: `\text{A store marks up a \$139.99 item by 10\%. What is the selling price?}`
  - answer: `\$153.99`
- seed 207 (pattern=`PercentWP`):
  - prompt: `\text{A \$60.95 purchase has 7\% sales tax added. What is the total cost?}`
  - answer: `\$65.22`

### D=16

- seed 101 (pattern=`PercentWP`):
  - prompt: `\text{A store marks up a \$144.50 item by 22.5\%. What is the selling price?}`
  - answer: `\$177.01`
- seed 207 (pattern=`PercentWP`):
  - prompt: `\text{A \$31.89 purchase has 6.25\% sales tax added. What is the total cost?}`
  - answer: `\$33.88`

### D=22

- seed 101 (pattern=`PercentWP`):
  - prompt: `\text{A store marks up a \$144.50 item by 22.5\%. What is the selling price?}`
  - answer: `\$177.01`
- seed 207 (pattern=`PercentWP`):
  - prompt: `\text{A \$31.89 purchase has 6.25\% sales tax added. What is the total cost?}`
  - answer: `\$33.88`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 3.2 Solve Percent Applications

- https://openstax.org/books/elementary-algebra-2e/pages/3-2-solve-percent-applications
- Shape: Percent of, discount, mark-up, simple interest.

### Intermediate Algebra 2e — 2.2 Use a Problem Solving Strategy

- https://openstax.org/books/intermediate-algebra-2e/pages/2-2-use-a-problem-solving-strategy
- Shape: Percent applications subsection (discount, mark-up, simple interest). Early mined examples in this JSON are number WPs — not this leaf.

## Variety notes

Live A1 path uses OpenStax EA 3.2 percent-of, discount, and simple interest at D=0. Markup/tax/original unlock later. PA retail markup stays on `pa_markup_discount_and_tax`.

## Limitations

- Gallery section slug: `percent_word_problems` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse PercentWordProblemFramework. Keep A1 as EA 3.2 percent applications, not a new engine.
