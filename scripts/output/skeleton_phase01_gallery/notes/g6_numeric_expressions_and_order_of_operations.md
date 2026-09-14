# Notes — `g6_numeric_expressions_and_order_of_operations` (`g6_numeric_expressions_and_order_of_operations`)

- **Display name:** Numeric expressions and the order of operations
- **Catalog chapter:** Grade 6 — Numeric Expressions, Exponents, and the Order of Operations
- **Generator key:** `order_of_operations`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Numeric expressions and the order of operations
- **D=0:** Two–three ops, no grouping, small integers ($2\times 3-5$).
- **High D (≈16–22):** Many ops, grouping, powers — still numeric evaluate, not solve-for-x.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Evaluate.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `3 \times 2 - 2 \times 3` | `0` | D=0 easy |
| 8 | 41 | `4 \times 2 + 3 + 18 \div 6 - 12` | `2` | mid |
| 16 | 41 | `2 \times 5^{2} - 12 \div 4 + 5 \times 2 + 20 \div 5 + 5 \times 5 + 4 \times 4 - 101` | `1` | high D |
| 22 | 41 | `2 \times 5 + \left(5 - 4\right) \times 6 - 5^{2} \times 3^{3} - 4 \times 2 - 3 \times 3^{2} + 6 \times 2 + 4 + 3 \times 4 + 667` | `1` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_numeric_expressions_and_order_of_operations/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§2.1 Use the Language of Algebra** — simplify using the order of operations. | | |
| Grade 6 curriculum unit 9 (numeric expressions / OOO) maps here; OpenStax 2.1 is the textbook home. | | |

## Variety notes / UNCLEAR flag

Expression length ramps honestly. Matches 2.1. High D stays evaluate (good).

## Limitations

- Flags: **UNCLEAR**.
- Expression length ramps honestly. Matches 2.1. High D stays evaluate (good).

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `OrderOfOperationsFramework`. Not SolveLinear. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
