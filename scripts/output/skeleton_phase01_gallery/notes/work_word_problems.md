# `work_word_problems` — Work word problems

- **Course:** Algebra 1 (A1 catalog)
- **Category:** Algebra 1 — Equations
- **Generator:** `wp_work`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Together / one-rate / pipes. D=0: two people finish a job in integer hours. High D: starts-later or three workers. Story first; not a dumped $1/a+1/b=1/t$.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Owen can finish a job in 6 hr. Working with Wade, they finish in 4 hr. How many hr would it take Wade working alone?}`
  - answer: `12 hr`
- seed 207:
  - prompt: `\text{Aisha can finish a job in 12 hr and Maya can finish the same job in 6 hr. Working together, how many hr will it take them to finish the job?}`
  - answer: `4 hr`

### D=8

- seed 101:
  - prompt: `\text{Owen and Wade can finish a job in 3 and 10 hr. With Gwen helping, the three finish in 2 hr. How many hr would Gwen need alone?}`
  - answer: `15 hr`
- seed 207:
  - prompt: `\text{Aisha, Maya, and Yves can finish a job in 3, 10, and 15 hr respectively. Working together, how many hr will it take them?}`
  - answer: `2 hr`

### D=16

- seed 101:
  - prompt: `\text{Pipe A fills a tank in 3 hr, pipe B fills it in 6 hr, and a drain empties it in 6 hr. With all three open, how many hr to fill the tank?}`
  - answer: `3 hr`
- seed 207:
  - prompt: `\text{Aisha can finish a job in 10 hr and Maya in 5 hr. Aisha works alone for 4 hr, then Maya joins. How many hr from the start until the job is done?}`
  - answer: `6 hr`

### D=22

- seed 101:
  - prompt: `\text{Pipe A fills a tank in 3 hr, pipe B fills it in 6 hr, and a drain empties it in 6 hr. With all three open, how many hr to fill the tank?}`
  - answer: `3 hr`
- seed 207:
  - prompt: `\text{Aisha can finish a job in 10 hr and Maya in 5 hr. Aisha works alone for 4 hr, then Maya joins. How many hr from the start until the job is done?}`
  - answer: `6 hr`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 8.8 Solve Uniform Motion and Work Applications

- https://openstax.org/books/elementary-algebra-2e/pages/8-8-solve-uniform-motion-and-work-applications
- Mined examples:
  - Example 8.81: An airplane can fly 200 miles into a 30 mph headwind in the same amount of time it takes to fly 300 miles with a 30 mph tailwind. What is the speed of the airplane?
  - Example 8.82: Jazmine trained for 3 hours on Saturday. She ran 8 miles and then biked 24 miles. Her biking speed is 4 mph faster than her running speed. What is her running speed?
  - Example 8.83: Hamilton rode his bike downhill 12 miles on the river trail from his house to the ocean and then rode uphill to return home. His uphill speed was 8 miles per hour slower than his downhill speed. It took him 2 hours longer to get home than it took him to get to the ocean. Find …
  - Example 8.84: The weekly gossip magazine has a big story about the Princess’ baby and the editor wants the magazine to be printed as soon as possible. She has asked the printer to run an extra printing press to get the printing done more quickly. Press #1 takes 6 hours to do the job and Pre…

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- LIMITATIONS: stay on work frames; do not dump onto one-step leaves.

## Proposed engine (reuse vs new)

Reuse WorkProblemFramework. Optional later wrap in wp_packaging frames. Leave on dedicated work core — do not dump onto one-step SolveLinear.

_Proposal only. No engine implementation in this notes pass._
