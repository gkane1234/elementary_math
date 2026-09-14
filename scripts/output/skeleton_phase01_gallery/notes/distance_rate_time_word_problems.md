# `distance_rate_time_word_problems` — Distance, rate, time word problems

- **Course:** Algebra 1 (A1 catalog)
- **Category:** Algebra 1 — Equations
- **Generator:** `wp_distance_rate_time`
- **Already on skeleton?** yes (OpenStax EA 3.4 vehicle frames on DistanceRateTimeFramework)
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

d=rt stories. D=0: one easy missing-piece (find distance or time) with small ints. High D: round-trip / opposite / catch-up. Several vehicles (bike / drive / walk / bus / train) — not one Mad-Lib. Never dump $d=rt$.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Owen travels 156 mi in 3 hr. What is the average speed in mi/hr?}`
  - answer: `52 mi/hr`
- seed 207:
  - prompt: `\text{Aisha travels at 29 mi/hr for 5 hr. How many mi does Aisha travel?}`
  - answer: `145 mi`

### D=8

- seed 101:
  - prompt: `\text{A slow bus leaves a station traveling at an unknown speed. 5 hr later a faster bus leaves the same station at 72 mi/hr and catches up after 3 hr. What is the slow bus's speed?}`
  - answer: `27 mi/hr`
- seed 207:
  - prompt: `\text{A slow bus leaves a station traveling at an unknown speed. 4 hr later a faster bus leaves the same station at 75 mi/hr and catches up after 2 hr. What is the slow bus's speed?}`
  - answer: `25 mi/hr`

### D=16

- seed 101:
  - prompt: `\text{A slow bus leaves a station traveling at an unknown speed. 2 hr later a faster bus leaves the same station at 70 mi/hr and catches up after 2 hr. What is the slow bus's speed?}`
  - answer: `35 mi/hr`
- seed 207:
  - prompt: `\text{Aisha drives to a destination at 91 mi/hr and returns at 39 mi/hr, taking 7 hr on the way back. How long did the trip there take?}`
  - answer: `3 hr`

### D=22

- seed 101:
  - prompt: `\text{A slow bus leaves a station traveling at an unknown speed. 2 hr later a faster bus leaves the same station at 70 mi/hr and catches up after 2 hr. What is the slow bus's speed?}`
  - answer: `35 mi/hr`
- seed 207:
  - prompt: `\text{Aisha drives to a destination at 91 mi/hr and returns at 39 mi/hr, taking 7 hr on the way back. How long did the trip there take?}`
  - answer: `3 hr`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 3.4 Solve Uniform Motion Applications

- https://openstax.org/books/elementary-algebra-2e/pages/3-4-solve-uniform-motion-applications
- Shape: Opposite direction, same direction, round trip. Several vehicles.

### Intermediate Algebra 2e — 2.4 Solve Mixture and Uniform Motion Applications

- https://openstax.org/books/intermediate-algebra-2e/pages/2-4-solve-mixture-and-uniform-motion-applications
- Shape: Uniform-motion half of §2.4 (the mined JSON leads with coin/stamp/mix examples — those belong on coin/mixture leaves). Motion: two vehicles, opposite or same direction, round trip.

## Variety notes

Live path now rotates OpenStax EA 3.4 vehicles (bike / drive / walk / bus / train) and motion kinds (missing piece, round-trip, catch-up, opposite). Catch-up is not one “slow bus” script.

## Limitations

- LIMITATIONS: rate WP needs several OpenStax d=rt vehicles (bike/drive/walk/bus/train), not bike-only.

## Proposed engine (reuse vs new)

Reuse DistanceRateTimeFramework + several OpenStax d=rt frames. Algebra shapes follow old path (missing piece → two-motion).
