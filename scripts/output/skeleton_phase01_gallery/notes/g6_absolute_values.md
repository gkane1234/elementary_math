# Notes — `g6_absolute_values` (`g6_absolute_values`)

- **Display name:** Absolute values
- **Catalog chapter:** Grade 6 — Negative Numbers and Absolute Value
- **Generator key:** `g6_absolute_values`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Absolute values
- **D=0:** Bare $|4|$.
- **High D (≈16–22):** $|a-(-b)|$ or $|a+(-b)|$ — still one absolute value, not OpenStax nested OOO-with-abs.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Find the absolute value.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\left\| 7 \right\|` | `7` | D=0 easy |
| 8 | 41 | `\left\| -13 \right\|` | `13` | mid |
| 16 | 41 | `\left\| -7 - 6 \right\|` | `13` | high D |
| 22 | 41 | `\left\| -7 - 6 \right\|` | `13` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_absolute_values/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§3.1 Introduction to Integers** | | |
| Simplify $|3|$, $|-44|$, $|0|$; later $|9-3|$; Ex 3.11: $24-|19-3(6-2)|$ (OOO inside abs — richer than our high D). | | |

## Variety notes / UNCLEAR flag

Expression inside abs gets a little arithmetic. We do not reach Ex 3.11 nested OOO. Still the same topic.

## Limitations

- Flags: **UNCLEAR**.
- Expression inside abs gets a little arithmetic. We do not reach Ex 3.11 nested OOO. Still the same topic.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `g6_absolute_values`. Do not bolt on the OOO skeleton.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
