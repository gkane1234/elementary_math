# Notes — `g6_dividing_decimals_by_whole_numbers` (`g6_dividing_decimals_by_whole_numbers`)

- **Display name:** Dividing decimals by whole numbers
- **Catalog chapter:** Grade 6 — Decimal Arithmetic
- **Generator key:** `g6_dividing_decimals_by_whole_numbers`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Dividing decimals by whole numbers
- **D=0:** One-place decimal ÷ small whole.
- **High D (≈16–22):** More decimal places in the dividend; maybe signed.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Divide.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `9.6 \div 4` | `2.4` | D=0 easy |
| 8 | 41 | `42.4 \div 8` | `5.3` | mid |
| 16 | 41 | `191.133 \div 9` | `21.237` | high D |
| 22 | 41 | `513.0744 \div 24` | `21.3781` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_dividing_decimals_by_whole_numbers/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.2 Decimal Operations** — divide decimals (shift/point placement). | | |

## Variety notes / UNCLEAR flag

Bare divide. Matches 5.2.

## Limitations

- Flags: **UNCLEAR**.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `g6_dividing_decimals_by_whole_numbers`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
