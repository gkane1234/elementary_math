# Notes — `g6_comparing_ratios` (`g6_comparing_ratios`)

- **Display name:** Comparing ratios
- **Catalog chapter:** Grade 6 — Ratios
- **Generator key:** `g6_comparing_ratios`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `LOW_VARIETY`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Comparing ratios
- **D=0:** Which is greater: two tiny ratios with a shared part (1:2 vs 2:2).
- **High D (≈16–22):** Both ratios need reducing; larger composites; colon or fraction display.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Compare the ratios.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{Which ratio is greater: } 4:3 \text{ or } 3:3\text{?}` | `4:3` | D=0 easy |
| 8 | 41 | `\text{Which ratio is greater: } 24:30 \text{ or } 36:42\text{?}` | `36:42` | mid |
| 16 | 41 | `\text{Which ratio is greater: } 84:72 \text{ or } 96:80\text{?}` | `96:80` | high D |
| 22 | 41 | `\text{Which ratio is greater: } 168:144 \text{ or } 192:168\text{?}` | `168:144` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_comparing_ratios/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.6 Ratios and Rate** Ex 5.61: compare a ratio to a benchmark (5 to 1). | | |
| OpenStax Prealgebra 2e **§6.5** / unit-rate compare also in **§5.6 Rate** (Ex 5.63 Bob drove 525 miles in 9 hours). | | |

## Variety notes / UNCLEAR flag

**LOW_VARIETY:** one stem ('Which ratio is greater: A or B?'). OpenStax compares to a guideline, mixed units, and rates-as-fractions — not just two abstract ratios.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** one stem ('Which ratio is greater: A or B?'). OpenStax compares to a guideline, mixed units, and rates-as-fractions — not just two abstract ratios.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `ComparingRatiosFramework`. Variety fix is extra OpenStax 5.6 frames, not a new engine family.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
