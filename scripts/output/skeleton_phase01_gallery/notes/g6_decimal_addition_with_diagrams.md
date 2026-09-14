# Notes — `g6_decimal_addition_with_diagrams` (`g6_decimal_addition_with_diagrams`)

- **Display name:** Decimal addition with diagrams
- **Catalog chapter:** Grade 6 — Decimal Arithmetic
- **Generator key:** `g6_decimal_addition`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Decimal addition with diagrams
- **D=0:** Add two one-place decimals ($2.1+3.8$).
- **High D (≈16–22):** More places / regrouping — **same arithmetic as** `g6_decimal_addition`.
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

topic_fit: `scripts/output/topic_fit/by_topic/g6_decimal_addition_with_diagrams/` **not present** (live table is the record).

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.2 Decimal Operations** Ex 5.11: Add $3.7+12.4$. | | |
| OpenStax 5.1/5.2 do not require grid diagrams; G6 'with diagrams' is an IM extra. No mined diagram bank. | | |

## Variety notes / UNCLEAR flag

**UNCLEAR:** catalog generator is `g6_decimal_addition` (same as the non-diagram leaf). Live prompt is $a+b$ with no tenths-grid. D=22 on this seed emitted **subtraction** ($10.5-9.5225$) — off-skill for an addition leaf.

## Limitations

- Flags: **UNCLEAR**.
- **UNCLEAR:** catalog generator is `g6_decimal_addition` (same as the non-diagram leaf). Live prompt is $a+b$ with no tenths-grid. D=22 on this seed emitted **subtraction** ($10.5-9.5225$) — off-skill for an addition leaf.
- Diagram-named leaf: stem/latex often lacks a readable diagram (or diagram is metadata-only).
- Possible miswire / off-skill emission at some D.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `DecimalArithmeticFramework('+')`. Diagram UI is not a new engine. Do not invent a diagram skeleton.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
