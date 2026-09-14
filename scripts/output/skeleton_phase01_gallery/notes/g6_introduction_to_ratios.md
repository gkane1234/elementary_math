# Notes — `g6_introduction_to_ratios` (`g6_introduction_to_ratios`)

- **Display name:** Introduction to ratios
- **Catalog chapter:** Grade 6 — Ratios
- **Generator key:** `g6_introduction_to_ratios`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Introduction to ratios
- **D=0:** Write a part:part ratio from a tiny two-color count (already simplified, e.g. 1:2). No cancel work.
- **High D (≈16–22):** Always simplify a shown ratio to a fraction; GCD has several prime leftover steps (not just ÷10).
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Write the ratio.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{There are 4 red apples and 3 orange apples. Write the ratio of red to orange.}` | `4:3` | D=0 easy |
| 8 | 41 | `\text{Write the ratio } 20:15 \text{ as a fraction in simplest form.}` | `\frac{4}{3}` | mid |
| 16 | 41 | `\text{Write the ratio } 28:24 \text{ as a fraction in simplest form.}` | `\frac{7}{6}` | high D |
| 22 | 41 | `\text{Write the ratio } 112:96 \text{ as a fraction in simplest form.}` | `\frac{7}{6}` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_introduction_to_ratios/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.6 Ratios and Rate** — https://openstax.org/books/prealgebra-2e/pages/5-6-ratios-and-rate | | |
| Ex 5.58: Write each ratio as a fraction: $15$ to $27$; $45$ to $18$. | | |
| Ex 5.61 (apps): total cholesterol to HDL; compare to a 5:1 guideline. | | |
| Ex 5.62: ADA ramp rise:run with mixed units (1 in : 1 ft). | | |

## Variety notes / UNCLEAR flag

Old path has two modes (word write-as-given vs simplify). OpenStax also has decimal/mixed ratios and measurement-unit ratios; we do not.

## Limitations

- Flags: **UNCLEAR**.
- Old path has two modes (word write-as-given vs simplify). OpenStax also has decimal/mixed ratios and measurement-unit ratios; we do not.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse existing **number** `RatioFramework` (already wired). No new skeleton. Optional later: extra OpenStax 5.6 frames (decimals, mixed units) as WP packaging, not a new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
