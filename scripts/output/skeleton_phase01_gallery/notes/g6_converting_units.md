# Notes — `g6_converting_units` (`g6_converting_units`)

- **Display name:** Converting units
- **Catalog chapter:** Grade 6 — Rates
- **Generator key:** `g6_converting_units`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Converting units
- **D=0:** Metric place-value (30 mm, 10 mm = 1 cm → 3 cm).
- **High D (≈16–22):** Approximate mixed-system rates (5 m ≈ 16 ft) with non-integer answers.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Convert each measurement using the given equivalence. A double number line is provided.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{A desk is 200 cm wide. Given that 100 cm $=$ 1 m. What is the width in m?}` | `2` | D=0 easy |
| 8 | 41 | `\text{A package has a mass of 3000 g. Given that 1000 g $=$ 1 kg. What is the mass in kg?}` | `3` | mid |
| 16 | 41 | `\text{A hike is 40 km long. Given that 8 km }\approx\text{ 5 miles. About how many miles is that?}` | `25` | high D |
| 22 | 41 | `\text{A hike is 72 km long. Given that 8 km }\approx\text{ 5 miles. About how many miles is that?}` | `45` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_converting_units/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§7.5 Systems of Measurement** — https://openstax.org/books/prealgebra-2e/pages/7-5-systems-of-measurement | | |
| Ex 7.44: Mary Anne is $66$ inches tall. Height in feet? | | |
| Ex 7.45: elephant $3.2$ tons → pounds; Ex 7.48 mixed oz/lb steaks. | | |

## Variety notes / UNCLEAR flag

**UNCLEAR:** catalog instruction says a double number line is provided; live prompt is given-equivalence text only. OpenStax 7.5 has US customary chains and mixed units we only partly cover.

## Limitations

- Flags: **UNCLEAR**.
- **UNCLEAR:** catalog instruction says a double number line is provided; live prompt is given-equivalence text only. OpenStax 7.5 has US customary chains and mixed units we only partly cover.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `ConvertingUnitsFramework`. No new engine. Double-number-line is display.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
