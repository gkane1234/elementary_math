# Notes — `g6_part_part_whole_ratios` (`g6_part_part_whole_ratios`)

- **Display name:** Part-part-whole ratios
- **Catalog chapter:** Grade 6 — Ratios
- **Generator key:** `g6_part_part_whole_ratios`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Part-part-whole ratios
- **D=0:** Two small parts; write part:part only (already simple).
- **High D (≈16–22):** Part:whole and all:part in simplest form, or split a collection given a ratio $a:b$ (find one color's count).
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Write part-to-part and part-to-whole ratios.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{There are 4 red apples and 3 orange apples. Write the ratio of red to orange.}` | `4:3` | D=0 easy |
| 8 | 41 | `\text{There are 20 green students and 15 orange students. Write the ratio of all students to orange students in simplest form.}` | `7:3` | mid |
| 16 | 41 | `\text{There are 28 blue students and 24 orange students. Write the ratio of blue to orange, and the ratio of blue to all students, both in simplest form.}` | `7:6, 7:13` | high D |
| 22 | 41 | `\text{A collection of 208 students is split in the ratio 7:6 (red to yellow). How many are yellow?}` | `96` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_part_part_whole_ratios/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.6 Ratios and Rate** — part-to-whole is the 'to' language in Ex 5.58 / 5.61. | | |
| No dedicated OpenStax 'part-part-whole' section; IM-style G6 curriculum unit. Closest: 5.6 applications + fraction-of-a-group language in §4.2. | | |

## Variety notes / UNCLEAR flag

Stories stay two-color counts (apples/stickers/students/marbles). OpenStax cholesterol/ramp apps are richer; flag not LOW_VARIETY because tasks (part:part vs part:whole vs split) do change.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- Stories stay two-color counts (apples/stickers/students/marbles). OpenStax cholesterol/ramp apps are richer; flag not LOW_VARIETY because tasks (part:part vs part:whole vs split) do change.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `PartPartWholeRatioFramework`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
