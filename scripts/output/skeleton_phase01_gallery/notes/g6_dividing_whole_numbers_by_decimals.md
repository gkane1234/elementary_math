# Notes — `g6_dividing_whole_numbers_by_decimals` (`g6_dividing_whole_numbers_by_decimals`)

- **Display name:** Dividing whole numbers by decimals
- **Catalog chapter:** Grade 6 — Decimal Arithmetic
- **Generator key:** `g6_whole_by_decimal_divide`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Dividing whole numbers by decimals
- **D=0:** Whole ÷ one-place decimal that is a place-value unit ($1\div 0.1=10$).
- **High D (≈16–22):** Awkward decimals; occasional negatives (OpenStax 5.2 signed divide).
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Divide.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `6 \div 0.5` | `12` | D=0 easy |
| 8 | 41 | `24 \div 1.6` | `15` | mid |
| 16 | 41 | `-42 \div (-1.75)` | `24` | high D |
| 22 | 41 | `-77 \div (-1.75)` | `44` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_dividing_whole_numbers_by_decimals/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.2 Decimal Operations** Ex 5.23: Divide $4\div 0.05$. Try It 5.45: $6\div 0.03$. | | |

## Variety notes / UNCLEAR flag

Bare $n\div 0.d$. Matches Ex 5.23 well.

## Limitations

- Flags: **UNCLEAR**.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `g6_whole_by_decimal_divide`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
