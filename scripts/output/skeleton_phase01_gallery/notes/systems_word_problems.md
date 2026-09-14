# `systems_word_problems` — Word problems

- **Course:** Algebra 1 (A1 catalog)
- **Category:** Algebra 1 — Systems of Equations and Inequalities
- **Generator:** `wp_systems`
- **Already on skeleton?** yes (`SystemsWP`; shared with `pa_systems_word_problems`)
- **Old-path extra settings: `{"use_legacy_systems": true}`.**

## What the question should look like (D=0 vs high D)

OpenStax EA 5.4: number, money/tickets, geometry, uniform motion. D=0 one easy number or tickets frame. Do **not** dump the system into the prompt.

## What old path actually produced

- **Course:** Algebra 1 (A1 catalog)
- **Category:** Algebra 1 — Systems of Equations and Inequalities
- **Generator:** `wp_systems`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_legacy_systems": true}`.**

## What the question should look like (D=0 vs high D)

OpenStax EA 5.4: number, money/tickets, geometry, uniform motion. D=0 one easy number or tickets frame. Do **not** dump the system into the prompt.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Riley buys two items. The costs satisfy } \begin{cases} x + 3y = -4 \\ -x + y = 0 \end{cases}`
  - answer: `x = -1,\ y = -1`
- seed 207:
  - prompt: `\text{Sam buys two items. The costs satisfy } \begin{cases} 3x - 3y = 9 \\ -4x + y = -6 \end{cases}`
  - answer: `x = 1,\ y = -2`

### D=8

- seed 101:
  - prompt: `\text{Taylor buys two items. The costs satisfy } \begin{cases} 2x + 5y = 3 \\ 4x + 10y = 8 \end{cases}`
  - answer: `\text{no solution}`
- seed 207:
  - prompt: `\text{Alex buys two items. The costs satisfy } \begin{cases} 3x + 2y = 4 \\ 12x + 8y = 14 \end{cases}`
  - answer: `\text{no solution}`

### D=16

- seed 101:
  - prompt: `\text{Taylor buys two items. The costs satisfy } \begin{cases} 2x + 5y = 3 \\ 4x + 10y = 8 \end{cases}`
  - answer: `\text{no solution}`
- seed 207:
  - prompt: `\text{Alex buys two items. The costs satisfy } \begin{cases} 3x + 2y = 4 \\ 12x + 8y = 14 \end{cases}`
  - answer: `\text{no solution}`

### D=22

- seed 101:
  - prompt: `\text{Taylor buys two items. The costs satisfy } \begin{cases} 2x + 5y = 3 \\ 4x + 10y = 8 \end{cases}`
  - answer: `\text{no solution}`
- seed 207:
  - prompt: `\text{Alex buys two items. The costs satisfy } \begin{cases} 3x + 2y = 4 \\ 12x + 8y = 14 \end{cases}`
  - answer: `\text{no solution}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 5.4 Solve Applications with Systems of Equations

- https://openstax.org/books/elementary-algebra-2e/pages/5-4-solve-applications-with-systems-of-equations
- Mined examples:
  - Example 5.35: How to Translate to a System of Equations Translate to a system of equations: The sum of two numbers is negative fourteen. One number is four less than the other. Find the numbers.
  - Example 5.36: Translate to a system of equations: A married couple together earns $110,000 a year. The wife earns $16,000 less than twice what her husband earns. What does the husband earn?
  - Example 5.37: Translate to a system of equations and then solve: Devon is 26 years older than his son Cooper. The sum of their ages is 50. Find their ages.
  - Example 5.38: Translate to a system of equations and then solve: When Jenna spent 10 minutes on the elliptical trainer and then did circuit training for 20 minutes, her fitness app says she burned 278 calories. When she spent 20 minutes on the elliptical trainer and 30 minutes circuit train…

## Variety notes

Live default is OpenStax EA §5.4 number / tickets / geometry / motion frames (shared with `pa_systems_word_problems`). Opt out with `use_legacy_systems=True` to the dump stub.

## Limitations

- LIMITATIONS: WP frames on `pa_systems_wp`; must not dump a system into the stem (use_legacy_systems opt-out).

## Proposed engine (reuse vs new)

**Shipped:** SystemsWP + `wp_packaging` frames. Old dump is opt-out only.
