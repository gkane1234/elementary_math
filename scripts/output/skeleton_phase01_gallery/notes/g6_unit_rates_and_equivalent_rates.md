# Notes — `g6_unit_rates_and_equivalent_rates` (`g6_unit_rates_and_equivalent_rates`)

- **Display name:** Unit rates and equivalent rates
- **Catalog chapter:** Grade 6 — Rates
- **Generator key:** `g6_unit_rates`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Unit rates and equivalent rates
- **D=0:** Unit rate from a small 'pages in minutes' or 'miles in hours' with integer answer.
- **High D (≈16–22):** Scale a rate to a non-multiple time/quantity (e.g. $312$ for 24 lb → cost for 17 lb).
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Find the unit rate or an equivalent rate.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{A car travels 6 miles in 3 hours. Find the unit rate in miles per hour.}` | `2` | D=0 easy |
| 8 | 41 | `\text{A car travels 18 miles in 6 hours. At the same rate, how many miles in 24 hours?}` | `72` | mid |
| 16 | 41 | `\text{A car travels 32 miles in 8 hours. At the same rate, how many miles in 13 hours?}` | `52` | high D |
| 22 | 41 | `\text{A car travels 64 miles in 16 hours. At the same rate, how many miles in 10 hours?}` | `40` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_unit_rates_and_equivalent_rates/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.6 Ratios and Rate** Ex 5.63: Bob drove $525$ miles in $9$ hours. Write this rate as a fraction. | | |
| OpenStax also wants unit rates (mph, $/lb) in 5.6 Try-Its after Ex 5.63. | | |

## Variety notes / UNCLEAR flag

Three Mad-Libs (read pages, car miles, fruit $/lb). Better than one template; OpenStax 5.6 has more vehicles (drive, wages, heartbeats). Not dump-stub.

## Limitations

- Flags: **UNCLEAR**.
- Three Mad-Libs (read pages, car miles, fruit $/lb). Better than one template; OpenStax 5.6 has more vehicles (drive, wages, heartbeats). Not dump-stub.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `UnitRateFramework`. Optional WP frame pack (OpenStax 5.6 rates) — **proportion/wp family**, not a new number engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
