# Notes — `g6_decimal_subtraction` (`g6_decimal_subtraction`)

- **Display name:** Decimal subtraction
- **Catalog chapter:** Grade 6 — Decimal Arithmetic
- **Generator key:** `g6_decimal_subtraction`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Decimal subtraction
- **D=0:** One-place subtract, maybe one regroup.
- **High D (≈16–22):** Unequal decimal places, four-decimal subtraction, rare negatives.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Subtract.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `6.6 - 3.3` | `3.3` | D=0 easy |
| 8 | 41 | `17.4 - 12.5` | `4.86` | mid |
| 16 | 41 | `18.9 - 8.393` | `10.507` | high D |
| 22 | 41 | `24.9445 - 0.4081` | `24.5364` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_decimal_subtraction/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.2 Decimal Operations** — subtract decimals (place-align). | | |

## Variety notes / UNCLEAR flag

Bare $a-b$. On-topic vs OpenStax 5.2.

## Limitations

- Flags: **UNCLEAR**.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `DecimalArithmeticFramework('-')`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
