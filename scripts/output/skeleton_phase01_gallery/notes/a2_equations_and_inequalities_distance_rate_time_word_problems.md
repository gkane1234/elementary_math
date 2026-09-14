# Notes — `a2_equations_and_inequalities_distance_rate_time_word_problems`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Equations and Inequalities
- **Generator:** `wp_distance_rate_time`
- **Suggested family:** `wp`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Find distance, rate, or time — one missing piece.
- **D=0:** Find distance, rate, or time — one missing piece.
- **High D (≈16–22):** Catch-up, opposite direction, round trip.
- **Must not:** Dump $d=rt$; one vehicle only.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (DistanceRateTime live default)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Owen takes a train 114 mi in 3 hr. What is the average speed in mi/hr?}$ | $38 mi/hr$ | pattern=DistanceRateTime |
| 0 | 207 | $\text{Aisha drives at 32 mi/hr for 2 hr. How many mi does Aisha travel?}$ | $64 mi$ | pattern=DistanceRateTime |
| 8 | 101 | $\text{A slow train leaves a station traveling at an unknown speed. 2 hr later a faster train leaves the same station at 70 mi/hr and catches up after 2 hr. What is the slow train's speed?}$ | $35 mi/hr$ | pattern=DistanceRateTime |
| 8 | 207 | $\text{Finn drives at 30 mi/hr. Willow leaves later from the same place at 45 mi/hr in the same direction and catches up 2 hr after starting. How long had Finn been traveling when caught?}$ | $3 hr$ | pattern=DistanceRateTime |
| 16 | 101 | $\text{Lucia and Brian leave two towns at the same time and travel toward each other at 48 mi/hr and 73 mi/hr for 3 hr. How many mi apart were the towns?}$ | $363 mi$ | pattern=DistanceRateTime |
| 16 | 207 | $\text{Finn and Willow leave two towns 250 mi apart at the same time and travel toward each other at 69 mi/hr and 56 mi/hr. How many hr until they meet?}$ | $2 hr$ | pattern=DistanceRateTime |
| 22 | 101 | $\text{Lucia and Brian leave two towns at the same time and travel toward each other at 48 mi/hr and 73 mi/hr for 3 hr. How many mi apart were the towns?}$ | $363 mi$ | pattern=DistanceRateTime |
| 22 | 207 | $\text{Finn and Willow leave two towns 250 mi apart at the same time and travel toward each other at 69 mi/hr and 56 mi/hr. How many hr until they meet?}$ | $2 hr$ | pattern=DistanceRateTime |

Opt-out flag used: `none (DistanceRateTime live default)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §3.4 | https://openstax.org/books/elementary-algebra-2e/pages/3-4-solve-uniform-motion-applications | Bike/drive/walk/bus/train; missing piece |
| OpenStax Intermediate Algebra 2e §2.4 | https://openstax.org/books/intermediate-algebra-2e/pages/2-4-solve-mixture-and-uniform-motion-applications | IA uniform motion |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** DistanceRateTime (wp_packaging) — OpenStax vehicle frames.
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
