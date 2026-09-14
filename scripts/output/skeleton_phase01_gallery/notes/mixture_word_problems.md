# `mixture_word_problems` — Mixture word problems

- **Course:** Algebra 1 (A1 catalog)
- **Category:** Algebra 1 — Equations
- **Generator:** `wp_mixture`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Story first: two concentrations / ticket prices / dry mix. D=0 one easy percent-mix or ticket frame with small ints. High D: find an amount given the blend percent. Never dump the equation. Not a systems leaf (EA 5.5).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Quinn mixes 6 fl oz of a 75\% alcohol solution with 4 fl oz of a 10\% alcohol solution. What is the concentration of the new mixture?}`
  - answer: `49\%`
- seed 207:
  - prompt: `\text{Finn mixes 2 cubic yards of soil that is 50\% sand with 3 cubic yards of soil that is 25\% sand. What percent of the mixture is sand?}`
  - answer: `35\%`

### D=8

- seed 101:
  - prompt: `\text{Lena mixes 6 fl oz of a 15\% alcohol solution with 4 fl oz of a 75\% alcohol solution. What is the concentration of the new mixture?}`
  - answer: `39\%`
- seed 207:
  - prompt: `\text{Maya mixes 4 lb of nuts that are 60\% peanuts with 6 lb of nuts that are 25\% peanuts. What percent of the new mixture is peanuts?}`
  - answer: `39\%`

### D=16

- seed 101:
  - prompt: `\text{Quinn mixes 21 fl oz of a 35\% alcohol solution with 15 fl oz of a 10\% alcohol solution. What is the concentration of the new mixture?}`
  - answer: `24.6\%`
- seed 207:
  - prompt: `\text{Wesley mixes 9 cubic yards of soil that is 50\% sand with 4 cubic yards of soil that is 25\% sand. What percent of the mixture is sand?}`
  - answer: `42.3\%`

### D=22

- seed 101:
  - prompt: `\text{Quinn mixes 21 fl oz of a 35\% alcohol solution with 15 fl oz of a 10\% alcohol solution. What is the concentration of the new mixture?}`
  - answer: `24.6\%`
- seed 207:
  - prompt: `\text{Wesley mixes 9 cubic yards of soil that is 50\% sand with 4 cubic yards of soil that is 25\% sand. What percent of the mixture is sand?}`
  - answer: `42.3\%`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 3.3 Solve Mixture Applications

- https://openstax.org/books/elementary-algebra-2e/pages/3-3-solve-mixture-applications
- Shape: Coins / tickets / percent solutions as one linear equation.

### Intermediate Algebra 2e — 2.4 Solve Mixture and Uniform Motion Applications

- https://openstax.org/books/intermediate-algebra-2e/pages/2-4-solve-mixture-and-uniform-motion-applications
- Mined examples:
  - Example 2.39: Jesse has $3.02 worth of pennies and nickels in his piggy bank. The number of nickels is three more than eight times the number of pennies. How many nickels and how many pennies does Jesse have?
  - Example 2.40: Danny paid $15.75 for stamps. The number of 49-cent stamps was five less than three times the number of 35-cent stamps. How many 49-cent stamps and how many 35-cent stamps did Danny buy?
  - Example 2.41: A whale-watching ship had 40 paying passengers on board. The total revenue collected from tickets was $1,196. Full-fare passengers paid $32 each and reduced-fare passengers paid $26 each. How many full-fare passengers and how many reduced-fare passengers were on the ship?
  - Example 2.42: Henning is mixing raisins and nuts to make 25 pounds of trail mix. Raisins cost $4.50 a pound and nuts cost $8 a pound. If Henning wants his cost for the trail mix to be $6.60 a pound, how many pounds of raisins and how many pounds of nuts should he use?

## Variety notes

Stories are real (alcohol / soil / nuts) — not a dump. Ask-kind is only “what is the blend percent?”; OpenStax IA 2.4 / EA 3.3 also solve for an unknown amount given a target mix. Keep coins/tickets on the coin leaf; two-variable mix on systems WP (EA 5.5).

## Limitations

- LIMITATIONS: WP frames must rotate OpenStax mixture contexts; algebra shapes follow old path.
- Must not dump "the equation is …" stubs.

## Proposed engine (reuse vs new)

Reuse MixtureProblemFramework + OpenStax story frames (wp_packaging style). Algebra stays one linear mix equation — not systems.

_Proposal only. No engine implementation in this notes pass._
