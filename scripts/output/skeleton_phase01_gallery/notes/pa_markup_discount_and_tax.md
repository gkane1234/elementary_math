# `pa_markup_discount_and_tax` — Markup, discount, and tax

> **LOW_VARIETY** — Live old path is markup-or-tax only. OpenStax 6.3 also has commission, discount, and “find the tax/rate” ask-kinds.

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Percents
- **Generator:** `wp_percent`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Retail money: sales tax, commission, discount, mark-up. D=0 one-step (tax on a price). High D: discount-then-tax. Commission is an OpenStax 6.3 mode — include it.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{A store marks up a \$74 item by 10\%. What is the selling price?}`
  - answer: `\$81.40`
- seed 207:
  - prompt: `\text{A \$109 purchase has 6\% sales tax added. What is the total cost?}`
  - answer: `\$115.54`

### D=8

- seed 101:
  - prompt: `\text{A store marks up a \$139.99 item by 10\%. What is the selling price?}`
  - answer: `\$153.99`
- seed 207:
  - prompt: `\text{A \$60.95 purchase has 7\% sales tax added. What is the total cost?}`
  - answer: `\$65.22`

### D=16

- seed 101:
  - prompt: `\text{A store marks up a \$144.50 item by 22.5\%. What is the selling price?}`
  - answer: `\$177.01`
- seed 207:
  - prompt: `\text{A \$31.89 purchase has 6.25\% sales tax added. What is the total cost?}`
  - answer: `\$33.88`

### D=22

- seed 101:
  - prompt: `\text{A store marks up a \$144.50 item by 22.5\%. What is the selling price?}`
  - answer: `\$177.01`
- seed 207:
  - prompt: `\text{A \$31.89 purchase has 6.25\% sales tax added. What is the total cost?}`
  - answer: `\$33.88`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 6.3 Solve Sales Tax, Commission, and Discount Applications

- https://openstax.org/books/prealgebra-2e/pages/6-3-solve-sales-tax-commission-and-discount-applications
- Mined examples:
  - Example 6.25: Cathy bought a bicycle in Washington, where the sales tax rate was $\text{6}.\text{5}\%$ of the purchase price. What was ⓐ the sales tax and ⓑ the total cost of a bicycle if the purchase price of the bicycle was $\$\text{392} ?$
  - Example 6.26: Evelyn bought a new smartphone for $\$\text{499}$ plus tax. She was surprised when she got the receipt and saw that the tax was $\$\text{42}.\text{42} .$ What was the sales tax rate for this purchase?
  - Example 6.27: Helene is a realtor. She receives $\text{3}\%$ commission when she sells a house. How much commission will she receive for selling a house that costs $\$\text{260},\text{000} ?$
  - Example 6.28: Rikki earned $\$\text{87}$ commission when she sold a $\$\text{1},\text{450}$ stove. What rate of commission did she get?

### Prealgebra 2e — 6.2 Solve General Applications of Percent

- https://openstax.org/books/prealgebra-2e/pages/6-2-solve-general-applications-of-percent
- Mined examples:
  - Example 6.14: What number is $\text{35}\%$ of $90 ?$
  - Example 6.15: $\text{125}\%$ of $28$ is what number?
  - Example 6.16: Translate and solve: $36$ is $\text{75}\%$ of what number?
  - Example 6.17: $\text{6}.\text{5}\%$ of what number is $\$\text{1}.\text{17} ?$

## Variety notes

Live samples are real retail stories (not dump stubs) but only markup and sales-tax-on-total. Missing commission, discount, and OpenStax “find the tax amount / find the rate” variants. D=16 and D=22 matched for these seeds.

## Limitations

- Flags: **LOW_VARIETY**.
- Live samples are real retail stories (not dump stubs) but only markup and sales-tax-on-total. Missing commission, discount, and OpenStax “find the tax amount / find the rate” variants. D=16 and D=22 matched for these seeds.
- Old path can dump a bare equation / identity instead of the named skill.

## Proposed engine (reuse vs new)

Reuse PercentWordProblemFramework (wp_percent). Extend frames for commission + discount (OpenStax 6.3) — not a new skeleton.

_Proposal only. No engine implementation in this notes pass._
