# Notes — `g6_comparing_with_absolute_values` (`g6_comparing_with_absolute_values`)

- **Display name:** Comparing with absolute values
- **Catalog chapter:** Grade 6 — Negative Numbers and Absolute Value
- **Generator key:** `g6_comparing_with_absolute_values`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Comparing with absolute values
- **D=0:** Compare $|a|$ and $|b|$ or a number vs an abs value, small ints.
- **High D (≈16–22):** Signed decimals/fractions inside or beside abs.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Compare the values.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\left\| 7 \right\| \; ? \; \left\| 2 \right\|` | `>` | D=0 easy |
| 8 | 41 | `\left\| 7 \right\| \; ? \; \left\| 10 \right\|` | `<` | mid |
| 16 | 41 | `\left\| 13 \right\| \; ? \; \left\| -15 \right\|` | `<` | high D |
| 22 | 41 | `\left\| 13 \right\| \; ? \; \left\| -15 \right\|` | `<` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_comparing_with_absolute_values/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§3.1** — compare using absolute value (distance from 0), alongside Ex 3.2 order. | | |

## Variety notes / UNCLEAR flag

Compare statements involving abs. Distinct from plain compare.

## Limitations

- Flags: **UNCLEAR**.
- Compare statements involving abs. Distinct from plain compare.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `g6_comparing_with_absolute_values`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
