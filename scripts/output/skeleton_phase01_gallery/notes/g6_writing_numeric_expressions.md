# Notes — `g6_writing_numeric_expressions` (`g6_writing_numeric_expressions`)

- **Display name:** Writing numeric expressions
- **Catalog chapter:** Grade 6 — Numeric Expressions, Exponents, and the Order of Operations
- **Generator key:** `writing_numeric_expressions`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Writing numeric expressions
- **D=0:** One operation from words: difference of 3 and 3; twice 10.
- **High D (≈16–22):** Nested words: quotient of a sum; $n$ more than a square.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Write the expression.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{Write an expression for } 5 \text{ decreased by } 2.` | `5 - 2` | D=0 easy |
| 8 | 41 | `\text{Write an expression for } 6 \text{ groups of the sum of } 7 \text{ and } 4.` | `6(7 + 4)` | mid |
| 16 | 41 | `\text{Write an expression for } 8 \text{ squared plus } 6.` | `8^{2} + 6` | high D |
| 22 | 41 | `\text{Write an expression for the square of } 3.` | `3^{2}` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_writing_numeric_expressions/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§2.1 Use the Language of Algebra** — https://openstax.org/books/prealgebra-2e/pages/2-1-use-the-language-of-algebra | | |
| Ex 2.1: translate $12+14$, $(30)(5)$, $64\div 8$ to words (reverse of our leaf). | | |
| Ex 2.5: write $16\cdot 16\cdots$ in exponential form. | | |

## Variety notes / UNCLEAR flag

We go words→expression; OpenStax 2.1 also does expression→words and expression vs equation (Ex 2.4). Direction we implement is the G6 skill.

## Limitations

- Flags: **UNCLEAR**.
- We go words→expression; OpenStax 2.1 also does expression→words and expression vs equation (Ex 2.4). Direction we implement is the G6 skill.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse `writing_numeric_expressions` (**number** / language). Not the affine evaluate skeleton.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
