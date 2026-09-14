# Notes — `g6_decimal_addition` (`g6_decimal_addition`)

- **Display name:** Decimal addition
- **Catalog chapter:** Grade 6 — Decimal Arithmetic
- **Generator key:** `g6_decimal_addition`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Decimal addition
- **D=0:** Two one-place addends, little regrouping.
- **High D (≈16–22):** Unequal places, four-decimal addends, occasional signed decimals at the top of the band.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Add.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `6.6 + 3.3` | `9.9` | D=0 easy |
| 8 | 41 | `12.5 + 17.36` | `29.86` | mid |
| 16 | 41 | `10.7 + 36.918` | `47.618` | high D |
| 22 | 41 | `10.5 - 9.5225` | `0.9775` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_decimal_addition/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.2 Decimal Operations** — https://openstax.org/books/prealgebra-2e/pages/5-2-decimal-operations | | |
| Ex 5.11: Add $3.7 + 12.4$. Try It 5.21: $5.7+11.9$. | | |

## Variety notes / UNCLEAR flag

Straight $a+b$. Matches OpenStax 5.2 add. Money apps in 5.2 are extra, not required for this leaf.

## Limitations

- Flags: **UNCLEAR**.
- Straight $a+b$. Matches OpenStax 5.2 add. Money apps in 5.2 are extra, not required for this leaf.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `DecimalArithmeticFramework('+')`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
