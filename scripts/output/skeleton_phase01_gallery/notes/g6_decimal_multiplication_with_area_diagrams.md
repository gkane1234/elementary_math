# Notes — `g6_decimal_multiplication_with_area_diagrams` (`g6_decimal_multiplication_with_area_diagrams`)

- **Display name:** Decimal multiplication with area diagrams
- **Catalog chapter:** Grade 6 — Decimal Arithmetic
- **Generator key:** `g6_decimal_multiplication`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Decimal multiplication with area diagrams
- **D=0:** Same one-place product as decimal multiplication.
- **High D (≈16–22):** More decimal places — still $a\cdot b$.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Multiply.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `8 \cdot 0.4` | `3.2` | D=0 easy |
| 8 | 41 | `3.3 \cdot 6.5` | `21.45` | mid |
| 16 | 41 | `6.43 \cdot 3.22` | `20.7046` | high D |
| 22 | 41 | `6.43 \cdot 3.171` | `20.38953` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_decimal_multiplication_with_area_diagrams/` **not present** (live table is the record).

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.2** multiply decimals. Area-model for decimals is IM, not an OpenStax 5.2 example bank. | | |

## Variety notes / UNCLEAR flag

**UNCLEAR:** generator `g6_decimal_multiplication`; no area diagram in latex.

## Limitations

- Flags: **UNCLEAR**.
- **UNCLEAR:** generator `g6_decimal_multiplication`; no area diagram in latex.
- Diagram-named leaf: stem/latex often lacks a readable diagram (or diagram is metadata-only).

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** multiply framework. Area model is UI. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
