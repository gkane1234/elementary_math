# Notes — `g6_ordering_numbers` (`g6_ordering_numbers`)

- **Display name:** Ordering numbers
- **Catalog chapter:** Grade 6 — Negative Numbers and Absolute Value
- **Generator key:** `g6_ordering_numbers`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Ordering numbers
- **D=0:** Order three small integers.
- **High D (≈16–22):** Mix of signed decimals and fractions in a longer list.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Order the numbers.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{Order from least to greatest: } -3, 2, 5` | `-3, 2, 5` | D=0 easy |
| 8 | 41 | `\text{Order from least to greatest: } -0.2, 0.4, 0.96, 1` | `-0.2, 0.4, 0.96, 1` | mid |
| 16 | 41 | `\text{Order from least to greatest: } -\frac{20}{9}, -1.929, -1.67, -1.498, -\frac{11}{9}` | `-\frac{20}{9}, -1.929, -1.67, -1.498, -\frac{11}{9}` | high D |
| 22 | 41 | `\text{Order from least to greatest: } -\frac{19}{7}, -2.45, -2.158, -1.9, -\frac{5}{3}` | `-\frac{19}{7}, -2.45, -2.158, -1.9, -\frac{5}{3}` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_ordering_numbers/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§3.1 Introduction to Integers** (order positive and negative numbers). | | |

## Variety notes / UNCLEAR flag

List-order. On-topic.

## Limitations

- Flags: **UNCLEAR**.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `g6_ordering_numbers`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
