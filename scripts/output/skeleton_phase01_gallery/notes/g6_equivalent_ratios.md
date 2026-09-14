# Notes — `g6_equivalent_ratios` (`g6_equivalent_ratios`)

- **Display name:** Equivalent ratios
- **Catalog chapter:** Grade 6 — Ratios
- **Generator key:** `g6_equivalent_ratios`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Equivalent ratios
- **D=0:** Missing-value $a:b = c:x$ with tiny integers, scale factor 2.
- **High D (≈16–22):** Larger coprime-ish parts; mixed colon vs fraction notation; scale not obvious (need reduce then multiply).
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Find an equivalent ratio.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{Find the missing value: } 4:3 = 8:x` | `6` | D=0 easy |
| 8 | 41 | `\frac{8}{6} = \frac{32}{x}` | `24` | mid |
| 16 | 41 | `\text{Find the missing value: } 28:24 = 21:x` | `18` | high D |
| 22 | 41 | `\text{Find the missing value: } 112:96 = 560:x` | `480` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_equivalent_ratios/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.6 Ratios and Rate** (equivalent fractions / missing term) and **§6.5 Solve Proportions** — https://openstax.org/books/prealgebra-2e/pages/6-5-solve-proportions-and-their-applications | | |
| §5.6 Ex 5.58 shape is write-as-fraction; missing-value equivalent ratios match proportion $a/b = c/x$. | | |

## Variety notes / UNCLEAR flag

Stem is almost always 'find the missing value'. OpenStax 6.5 adds table/word proportion apps; G6 leaf stays numeric missing-term (WP rates live on rate types).

## Limitations

- Flags: **UNCLEAR**.
- Stem is almost always 'find the missing value'. OpenStax 6.5 adds table/word proportion apps; G6 leaf stays numeric missing-term (WP rates live on rate types).

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `RatioFramework(equivalent=True)`. Do not invent a proportion skeleton here — `solving_proportions` is a different leaf.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
