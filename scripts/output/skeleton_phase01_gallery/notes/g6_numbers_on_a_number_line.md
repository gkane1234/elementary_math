# Notes — `g6_numbers_on_a_number_line` (`g6_numbers_on_a_number_line`)

- **Display name:** Numbers on a number line
- **Catalog chapter:** Grade 6 — Negative Numbers and Absolute Value
- **Generator key:** `number_line_plot`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Numbers on a number line
- **D=0:** Plot a small whole number (prompt is the number; instruction is plot).
- **High D (≈16–22):** Negatives and halves ($\pm 15/2$). Still a single plotted value.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Plot the following numbers on the number line.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `6` | `6` | D=0 easy |
| 8 | 41 | `2` | `2` | mid |
| 16 | 41 | `\frac{15}{4}` | `\frac{15}{4}` | high D |
| 22 | 41 | `\frac{15}{4}` | `\frac{15}{4}` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_numbers_on_a_number_line/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§3.1 Introduction to Integers** — https://openstax.org/books/prealgebra-2e/pages/3-1-introduction-to-integers | | |
| Ex 3.1: Plot $3$, $−3$, $−2$ on a number line. | | |

## Variety notes / UNCLEAR flag

**UNCLEAR:** live prompt is often a bare $5$ (answer = same). Plotting is in `instruction_latex`, not the item. OpenStax 3.1 plots several signed values together.

## Limitations

- Flags: **UNCLEAR**.
- **UNCLEAR:** live prompt is often a bare $5$ (answer = same). Plotting is in `instruction_latex`, not the item. OpenStax 3.1 plots several signed values together.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse `number_line_plot` (**other** / graphing). Not an equation skeleton. Stimulus/number-line UI, not a new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
