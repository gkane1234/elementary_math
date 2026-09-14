# Notes — `g6_opposites_of_numbers` (`g6_opposites_of_numbers`)

- **Display name:** Opposites of numbers
- **Catalog chapter:** Grade 6 — Negative Numbers and Absolute Value
- **Generator key:** `g6_opposites_of_numbers`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Opposites of numbers
- **D=0:** Opposite of a small whole ($7\to -7$).
- **High D (≈16–22):** Opposite of a negative or a fraction/decimal.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Find the opposite.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{Find the opposite of } 4` | `-4` | D=0 easy |
| 8 | 41 | `\text{Find the opposite of } 8` | `-8` | mid |
| 16 | 41 | `\text{Find the opposite of } -2` | `2` | high D |
| 22 | 41 | `\text{Find the opposite of } 36` | `-36` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_opposites_of_numbers/` **not present** (live table is the record).

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§3.1 Introduction to Integers** Ex 3.3: Find the opposite of $7$ and $−10$. | | |
| Ex 3.4: opposite notation $−(−10)$. | | |

## Variety notes / UNCLEAR flag

Single skill. OpenStax also has $-(-n)$ notation; check live samples. Disabled in the picker but still in the catalog.

## Limitations

- Flags: **UNCLEAR**.
- Single skill. OpenStax also has $-(-n)$ notation; check live samples. Disabled in the picker but still in the catalog.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `g6_opposites_of_numbers`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
