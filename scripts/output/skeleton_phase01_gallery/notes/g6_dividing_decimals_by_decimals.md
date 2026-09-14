# Notes — `g6_dividing_decimals_by_decimals` (`g6_dividing_decimals_by_decimals`)

- **Display name:** Dividing decimals by decimals
- **Catalog chapter:** Grade 6 — Decimal Arithmetic
- **Generator key:** `g6_decimal_divide`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Dividing decimals by decimals
- **D=0:** One-place ÷ one-place.
- **High D (≈16–22):** Both have several places; point-shift work.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Divide.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `1.5 \div 0.5` | `3` | D=0 easy |
| 8 | 41 | `0.5 \div 0.25` | `2` | mid |
| 16 | 41 | `1.375 \div 0.25` | `5.5` | high D |
| 22 | 41 | `12.875 \div 1.25` | `10.3` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_dividing_decimals_by_decimals/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.2 Decimal Operations** (divide decimal by decimal; signed Try Its $−25.65\div(−0.06)$). | | |

## Variety notes / UNCLEAR flag

Bare divide. On-topic vs 5.2.

## Limitations

- Flags: **UNCLEAR**.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `g6_decimal_divide`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
