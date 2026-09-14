# Notes — `g6_numeric_expressions_with_exponents` (`g6_numeric_expressions_with_exponents`)

- **Display name:** Numeric expressions with exponents
- **Catalog chapter:** Grade 6 — Numeric Expressions, Exponents, and the Order of Operations
- **Generator key:** `g6_numeric_expressions_with_exponents`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Numeric expressions with exponents
- **D=0:** Short power-minus-product ($5^2-2\times 12$).
- **High D (≈16–22):** Long OOO chains that include powers and grouping — overlaps the OOO leaf.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Evaluate.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `3^{2} \times 2 - 2 \times 9` | `0` | D=0 easy |
| 8 | 41 | `4^{3} \times 2 - 4 \times 3 + 8 \div 4 - 116` | `2` | mid |
| 16 | 41 | `5^{3} \times 2 - 5 \times 3 - 2^{2} \times 3 + 20 \div 5 + 5 \times 5 + 4 \times 4 - 267` | `1` | high D |
| 22 | 41 | `8^{2} \div 4 - 3 \times 5^{2} + 4^{2} - 6 \times 5^{3} - 3 \times 6 - \left(4 - 2\right) \times 3^{2} + 30 \div 6 + 10 \div 5 + 823` | `1` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_numeric_expressions_with_exponents/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§2.1 Use the Language of Algebra** — simplify expressions with exponents; order of operations. | | |
| Ex 2.5–2.6 exponential notation; later 2.1 examples evaluate $2^4$, $3^2+5$, etc. | | |

## Variety notes / UNCLEAR flag

Live high-D looks like the OOO generator with a power somewhere. Topic still G6 OOO+exponents. Watch that D=22 does not become a different topic (algebra).

## Limitations

- Flags: **UNCLEAR**.
- Live high-D looks like the OOO generator with a power somewhere. Topic still G6 OOO+exponents. Watch that D=22 does not become a different topic (algebra).

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `OrderOfOperationsFramework` / exponents mode. No new engine. Affine skeleton is for *algebraic* evaluate.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
