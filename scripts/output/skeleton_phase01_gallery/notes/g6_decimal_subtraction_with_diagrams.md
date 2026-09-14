# Notes — `g6_decimal_subtraction_with_diagrams` (`g6_decimal_subtraction_with_diagrams`)

- **Display name:** Decimal subtraction with diagrams
- **Catalog chapter:** Grade 6 — Decimal Arithmetic
- **Generator key:** `g6_decimal_subtraction`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Decimal subtraction with diagrams
- **D=0:** One-place subtract ($3.6-2.9$).
- **High D (≈16–22):** Same as non-diagram subtraction (more places / regroup).
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

topic_fit: `scripts/output/topic_fit/by_topic/g6_decimal_subtraction_with_diagrams/` **not present** (live table is the record).

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.2 Decimal Operations** (add or subtract decimals, same section as Ex 5.11). | | |

## Variety notes / UNCLEAR flag

**UNCLEAR:** generator `g6_decimal_subtraction` — no diagram in the prompt.

## Limitations

- Flags: **UNCLEAR**.
- **UNCLEAR:** generator `g6_decimal_subtraction` — no diagram in the prompt.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `DecimalArithmeticFramework('-')`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
