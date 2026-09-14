# `pa_simple_and_compound_interest` — Simple and compound interest

> **LOW_VARIETY** — OpenStax 6.4 solves for I, P, r, or t; old path may only earn-interest. Compound is not in PA 6.4.

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Percents
- **Generator:** `wp_simple_and_compound_interest`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

OpenStax PA 6.4 is **simple** interest I=Prt (and solve for P/r/t). Compound is extra. D=0: find I given P,r,t in years. High D: months/days; solve for principal.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Sofia invests \$1500 in an account that pays 4\% interest compounded annually for 2 years. How much interest is earned?}`
  - answer: `\$122.40`
- seed 207:
  - prompt: `\text{Queenie invests \$400 at 8\% simple interest for 2 years. How much interest is earned?}`
  - answer: `\$64`

### D=8

- seed 101:
  - prompt: `\text{Sofia invests \$2800 in an account that pays 5\% interest compounded annually for 5 years. How much interest is earned?}`
  - answer: `\$773.59`
- seed 207:
  - prompt: `\text{Queenie invests \$4200 in an account that pays 4\% interest compounded annually for 3 years. What is the balance at the end of the term?}`
  - answer: `\$4724.43`

### D=16

- seed 101:
  - prompt: `\text{Sofia invests \$6300 at 8\% interest compounded monthly for 5 years. How much interest is earned?}`
  - answer: `\$3086.03`
- seed 207:
  - prompt: `\text{Queenie invests \$14400 at 6\% interest compounded semiannually for 6 years. What is the balance at the end of the term?}`
  - answer: `\$20530.96`

### D=22

- seed 101:
  - prompt: `\text{Sofia invests \$7350 at 8\% interest compounded monthly for 5 years. How much interest is earned?}`
  - answer: `\$3600.37`
- seed 207:
  - prompt: `\text{Queenie invests \$16800 at 6\% interest compounded semiannually for 6 years. What is the balance at the end of the term?}`
  - answer: `\$23952.78`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 6.4 Solve Simple Interest Applications

- https://openstax.org/books/prealgebra-2e/pages/6-4-solve-simple-interest-applications
- Mined examples:
  - Example 6.33: Find the simple interest earned after $3$ years on $\$\text{500}$ at an interest rate of $\text{6}\%.$
  - Example 6.34: Find the principal invested if $\$\text{178}$ interest was earned in $2$ years at an interest rate of $\text{4}\%.$
  - Example 6.35: Find the rate if a principal of $\$\text{8},\text{200}$ earned $\$\text{3},\text{772}$ interest in $4$ years.
  - Example 6.36: Nathaly deposited $\$\text{12},\text{500}$ in her bank account where it will earn $\text{4}\%$ interest. How much interest will Nathaly earn in $5$ years?

## Variety notes

OpenStax 6.4 solves for I, P, r, or t; old path may only earn-interest. Compound is not in PA 6.4.

## Limitations

- Flags: **LOW_VARIETY**.
- OpenStax 6.4 solves for I, P, r, or t; old path may only earn-interest. Compound is not in PA 6.4.

## Proposed engine (reuse vs new)

Reuse wp_simple_and_compound_interest. Prefer OpenStax simple-interest ask-kinds over a single earn-I template.

_Proposal only. No engine implementation in this notes pass._
