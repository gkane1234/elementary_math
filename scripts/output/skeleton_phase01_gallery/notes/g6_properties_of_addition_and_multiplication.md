# Notes — `g6_properties_of_addition_and_multiplication` (`g6_properties_of_addition_and_multiplication`)

- **Display name:** Properties of addition and multiplication
- **Catalog chapter:** Grade 6 — Numeric Expressions, Exponents, and the Order of Operations
- **Generator key:** `g6_properties_of_addition_and_multiplication`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `UNCLEAR`, `LOW_VARIETY`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Properties of addition and multiplication
- **D=0:** Identify commutative/associative/identity on a tiny numeric rewrite.
- **High D (≈16–22):** Same identify-the-name task; numbers or grouping slightly messier — should not become algebraic like-terms.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Identify the property.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `1 \cdot 7 = 7` | `\text{identity property of multiplication}` | D=0 easy |
| 8 | 41 | `0 \cdot 7 = 0` | `\text{zero property of multiplication}` | mid |
| 16 | 41 | `0 \cdot 7 = 0` | `\text{zero property of multiplication}` | high D |
| 22 | 41 | `0 \cdot 7 = 0` | `\text{zero property of multiplication}` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_properties_of_addition_and_multiplication/` **not present** (live table is the record).

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§7.2 Commutative and Associative Properties** — https://openstax.org/books/prealgebra-2e/pages/7-2-commutative-and-associative-properties | | |
| Ex 7.5: rewrite $−1+3$ and $4\cdot 9$ using commutative properties. | | |
| Ex 7.6: associative $(3+0.6)+0.4$. Also §7.4 identity/inverse/zero. | | |

## Variety notes / UNCLEAR flag

**UNCLEAR:** OpenStax 7.2 *rewrites* with a property; we *name* it (instruction: identify). Live answers are property names (good), not operation names. **LOW_VARIETY:** D=8/16/22 all sampled as $0\cdot 7=0$ (zero property); commutative/associative barely appear at high D.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **UNCLEAR:** OpenStax 7.2 *rewrites* with a property; we *name* it (instruction: identify). Live answers are property names (good), not operation names. **LOW_VARIETY:** D=8/16/22 all sampled as $0\cdot 7=0$ (zero property); commutative/associative barely appear at high D.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Keep identify-property **number** generator. Do not reuse affine like-terms. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
