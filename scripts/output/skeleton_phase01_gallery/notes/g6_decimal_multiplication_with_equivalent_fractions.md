# Notes — `g6_decimal_multiplication_with_equivalent_fractions` (`g6_decimal_multiplication_with_equivalent_fractions`)

- **Display name:** Decimal multiplication with equivalent fractions
- **Catalog chapter:** Grade 6 — Decimal Arithmetic
- **Generator key:** `g6_decimal_multiplication`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_ (named method is now visible: decimal = unreduced place-value fractions)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Decimal multiplication with equivalent fractions
- **D=0:** One-place × one-place ($0.5\cdot 0.3$).
- **High D (≈16–22):** Three-place factors. Prompt still shows decimal × decimal, not $\frac{5}{10}\times\frac{3}{10}$.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Multiply.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `0.5 \cdot 0.4` | `0.2` | D=0 easy |
| 8 | 41 | `5.4 \cdot 7.8` | `42.12` | mid |
| 16 | 41 | `0.84 \cdot 1.08` | `0.9072` | high D |
| 22 | 41 | `0.048 \cdot 0.048` | `0.002304` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_decimal_multiplication_with_equivalent_fractions/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.2 Decimal Operations** Ex 5.15: Multiply $(3.9)(4.075)$. | | |
| OpenStax Prealgebra 2e **§5.3 / §4.2** Be Prepared 5.5: Multiply $\frac310\cdot\frac910$ as the fraction view of tenths. | | |

## Variety notes / UNCLEAR flag

**Named method:** live latex now shows the equivalent-fraction rewrite
($0.5\cdot 0.4=\frac{5}{10}\cdot\frac{4}{10}$).

## Limitations

- Flags: **UNCLEAR**.
- **Named method:** live latex now shows the equivalent-fraction rewrite
- ($0.5\cdot 0.4=\frac{5}{10}\cdot\frac{4}{10}$).

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `DecimalArithmeticFramework('*', via_equivalent_fractions=True)` if that flag actually changes the prompt; if not, this is a display/method bug, not a new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
