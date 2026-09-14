# Notes — `g6_number_line_word_problems` (`g6_number_line_word_problems`)

- **Display name:** Number line word problems
- **Catalog chapter:** Grade 6 — Negative Numbers and Absolute Value
- **Generator key:** `wp_number_line`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `LOW_VARIETY`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Number line word problems
- **D=0:** Temperature starts small and rises/drops to a non-negative result.
- **High D (≈16–22):** Cross zero; two-step (rose then dropped); elevation or bank as alternate frames.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Solve the problem.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{The temperature was 6\textdegree{}F and dropped 4\textdegree{}F. What is the new temperature?}` | `2` | D=0 easy |
| 8 | 41 | `\text{The temperature was 0\textdegree{}F and dropped 7\textdegree{}F. What is the new temperature?}` | `-7` | mid |
| 16 | 41 | `\text{A hiker was at 8 meters, descended 11 meters, then climbed 13 meters. What is the new elevation?}` | `10` | high D |
| 22 | 41 | `\text{A hiker was at 6 meters, descended 11 meters, then climbed 10 meters. What is the new elevation?}` | `5` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_number_line_word_problems/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§3.1 Introduction to Integers** — translate word phrases to integers; later **§3.2/3.3** add/subtract apps (temperature, elevation, money). | | |

## Variety notes / UNCLEAR flag

**LOW_VARIETY:** three Mad-Libs (temperature, hiker elevation, bank balance). Better than a dump stub, thinner than OpenStax 3.2–3.3 app mix.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** three Mad-Libs (temperature, hiker elevation, bank balance). Better than a dump stub, thinner than OpenStax 3.2–3.3 app mix.
- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse `wp_number_line`. Upgrade = **wp packaging frames** (OpenStax integer apps), not a new solve engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
