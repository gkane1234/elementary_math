# Notes — `g6_introduction_to_percents` (`g6_introduction_to_percents`)

- **Display name:** Introduction to percents
- **Catalog chapter:** Grade 6 — Percents
- **Generator key:** `g6_introduction_to_percents`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `LOW_VARIETY`, `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Introduction to percents
- **D=0:** Shade a 100-square for a benchmark like $10\%$.
- **High D (≈16–22):** Still shade; model may switch (grid / percent bar / circle); percents not nicer.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Shade the figure.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{Shade the 100-square grid to represent } 75\%.` | `75\%` | D=0 easy |
| 8 | 41 | `\text{Shade the 100-square grid to represent } 45\%.` | `45\%` | mid |
| 16 | 41 | `\text{Shade the percent bar to represent } 61\%.` | `61\%` | high D |
| 22 | 41 | `\text{Shade the percent bar to represent } 61\%.` | `61\%` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_introduction_to_percents/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§6.1 Understand Percent** — https://openstax.org/books/prealgebra-2e/pages/6-1-understand-percent | | |
| Ex 6.1: write $44\%$ as a ratio (parents survey). | | |
| Ex 6.2: $21$ out of $100$ freshmen took a remedial course — ratio then percent. | | |
| Ex 6.3: convert $36\%$ and $125\%$ to fractions. | | |

## Variety notes / UNCLEAR flag

**LOW_VARIETY:** only 'shade the figure to represent $p\%$'. **UNCLEAR:** shade task without a guaranteed student-facing grid in the latex (answer is the same percent). OpenStax 6.1 is convert/ratio/definition, not shade-only.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** only 'shade the figure to represent $p\%$'. **UNCLEAR:** shade task without a guaranteed student-facing grid in the latex (answer is the same percent). OpenStax 6.1 is convert/ratio/definition, not shade-only.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Keep **number** percent-intro leaf. Do not invent a skeleton. Real upgrade is OpenStax 6.1 convert/ratio modes (already on `g6_relating_*`), not a new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
