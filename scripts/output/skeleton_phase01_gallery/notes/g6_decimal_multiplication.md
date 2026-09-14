# Notes — `g6_decimal_multiplication` (`g6_decimal_multiplication`)

- **Display name:** Decimal multiplication
- **Catalog chapter:** Grade 6 — Decimal Arithmetic
- **Generator key:** `g6_decimal_multiplication`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Decimal multiplication
- **D=0:** One-place factors.
- **High D (≈16–22):** Count of decimal places in the product grows (place-value of the point).
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Multiply.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `8 \cdot 0.4` | `3.2` | D=0 easy |
| 8 | 41 | `3.3 \cdot 6.5` | `21.45` | mid |
| 16 | 41 | `6.43 \cdot 3.22` | `20.7046` | high D |
| 22 | 41 | `6.43 \cdot 3.171` | `20.38953` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_decimal_multiplication/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.2 Decimal Operations** Ex 5.15: $(3.9)(4.075)$; Ex 5.16 signed $(−8.2)(5.19)$. | | |

## Variety notes / UNCLEAR flag

Bare product. OpenStax 5.2 also has money multiply; optional later, not required.

## Limitations

- Flags: **UNCLEAR**.
- Bare product. OpenStax 5.2 also has money multiply; optional later, not required.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `DecimalArithmeticFramework('*')`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
