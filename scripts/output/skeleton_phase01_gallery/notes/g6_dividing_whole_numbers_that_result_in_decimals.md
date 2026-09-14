# Notes — `g6_dividing_whole_numbers_that_result_in_decimals` (`g6_dividing_whole_numbers_that_result_in_decimals`)

- **Display name:** Dividing whole numbers that result in decimals
- **Catalog chapter:** Grade 6 — Decimal Arithmetic
- **Generator key:** `g6_dividing_whole_numbers_that_result_in_decimals`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Dividing whole numbers that result in decimals
- **D=0:** Friendly terminating: $9\div 10=0.9$ or $6\div 4=1.5$.
- **High D (≈16–22):** Two-place / three-place terminating quotients ($53\div 40$).
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Divide.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `6 \div 10` | `0.6` | D=0 easy |
| 8 | 41 | `22 \div 25` | `0.88` | mid |
| 16 | 41 | `22 \div 16` | `1.375` | high D |
| 22 | 41 | `40 \div 125` | `0.32` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_dividing_whole_numbers_that_result_in_decimals/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.2 Decimal Operations** (divide whole numbers that do not terminate as whole quotients) and **§5.3** fraction→decimal. | | |

## Variety notes / UNCLEAR flag

Bare $a\div b$. On-topic.

## Limitations

- Flags: **UNCLEAR**.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** decimal-divide whole÷whole. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
