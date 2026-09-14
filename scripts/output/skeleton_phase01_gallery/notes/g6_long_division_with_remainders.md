# Notes — `g6_long_division_with_remainders` (`g6_long_division_with_remainders`)

- **Display name:** Long division with remainders
- **Catalog chapter:** Grade 6 — Decimal Arithmetic
- **Generator key:** `g6_long_division_with_remainders`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Long division with remainders
- **D=0:** 2-digit ÷ 1-digit with remainder ($37\div 3 = 12$ R $1$).
- **High D (≈16–22):** 5-digit ÷ 2-digit, remainder near the divisor.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Divide. Write the quotient and remainder.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `35 \div 8` | `4 \text{ R } 3` | D=0 easy |
| 8 | 41 | `339 \div 8` | `42 \text{ R } 3` | mid |
| 16 | 41 | `4551 \div 15` | `303 \text{ R } 6` | high D |
| 22 | 41 | `39319 \div 31` | `1268 \text{ R } 11` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_long_division_with_remainders/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§1.5 Divide Whole Numbers** — https://openstax.org/books/prealgebra-2e/pages/1-5-divide-whole-numbers | | |
| Ex 1.61: Divide $2596\div 4$ (exact). Remainder form is elementary long division; 1.5 also has $4\overline{)28}$ notation. | | |

## Variety notes / UNCLEAR flag

Always $a\div b$ with R. OpenStax 1.5 is mostly exact division + properties of 0/1; remainder is still the right G6 skill.

## Limitations

- Flags: **UNCLEAR**.
- Always $a\div b$ with R. OpenStax 1.5 is mostly exact division + properties of 0/1; remainder is still the right G6 skill.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse existing G6 long-division generator (**number**). No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
