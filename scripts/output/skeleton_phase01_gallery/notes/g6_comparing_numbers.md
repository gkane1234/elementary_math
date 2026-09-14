# Notes — `g6_comparing_numbers` (`g6_comparing_numbers`)

- **Display name:** Comparing numbers
- **Catalog chapter:** Grade 6 — Negative Numbers and Absolute Value
- **Generator key:** `g6_comparing_numbers`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Comparing numbers
- **D=0:** Compare a positive whole to $0$ or a negative ($4\,?\,-1$).
- **High D (≈16–22):** Signed decimals vs fractions ($-2$ vs $-20/9$).
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Compare the numbers.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `-3 \; ? \; 2` | `<` | D=0 easy |
| 8 | 41 | `10.3 \; ? \; 5` | `>` | mid |
| 16 | 41 | `-2.54 \; ? \; -2.18` | `<` | high D |
| 22 | 41 | `8.59 \; ? \; 9.66` | `<` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_comparing_numbers/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§3.1 Introduction to Integers** Ex 3.2: Order pairs with $<$ or $>$ including $−1$ vs $−4$. | | |

## Variety notes / UNCLEAR flag

Always fill $<,>,=$. Number class (int/decimal/fraction) ramps. Matches 3.1.

## Limitations

- Flags: **UNCLEAR**.
- Always fill $<,>,=$. Number class (int/decimal/fraction) ramps. Matches 3.1.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `g6_comparing_numbers`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
