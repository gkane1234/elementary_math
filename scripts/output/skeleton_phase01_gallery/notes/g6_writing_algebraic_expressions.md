# `g6_writing_algebraic_expressions` — Writing algebraic expressions

> RED HEADER: **UNCLEAR**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** one operation, small integer, one variable (`x`). Phrases like “twice a number”, “the quotient of a number and 5”, “6 fewer than a number”.

**High D:** still *translate words → expression*, not evaluate/solve. OpenStax 2.2 stays linear (sum/product/quotient, “less than”, grouping). Old high-D unlocks squares/cubes (`x^2`, `x^3`), which is **beyond G6** (that is PA polynomials / A1). Keep grouping (`2(x+5)-11`) before powers.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{the quotient of a number and } 5$` | `$\frac{x}{5}$` |
| 8 | `$\text{} 11 \text{ less than twice the quantity of a number plus } 5$` | `$2(x + 5) - 11$` |
| 16 | `$\text{the quotient of the sum of a number and } 11\text{, and } 15$` | `$\frac{x + 11}{15}$` |
| 22 | `$\text{} 11 \text{ times the quantity of a number squared plus } 15$` | `$11(x^{2} + 15)$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{twice a number}$` → `$2x$`
- D=22: `$\text{the cube of a number increased by } 14$` → `$x^{3} + 14$`

## OpenStax examples + chapter/section

**OpenStax Prealgebra 2e §2.2** *Evaluate, Simplify, and Translate Expressions* ([link](https://openstax.org/books/prealgebra-2e/pages/2-2-evaluate-simplify-and-translate-expressions)).

- Table 2.7: “the quotient of *a* and *b*” → `a/b`; “*b* less than *a*” → `a-b`; “the product of *a* and *b*” → `ab`.
- Example: “The height of a rectangular window is 6 inches less than the width. Let *w* represent the width. Write an expression for the height.” → `w-6`.
- Example: “The length of a rectangle is 5 inches less than the width.” → `w-5`.
- Grouping: “3 times the quantity of a number plus 8” → `3(x+8)` (same chapter + §2.1 language).

Evaluate-by-substituting is a **different leaf** (`g6_evaluating_algebraic_expressions`). Do not merge them.

## Variety notes

Phrase bank is real (quotient / twice / less than / groups of / quantity). **UNCLEAR:** D=22 old path jumps to cubes/squares. That is not G6 and not OpenStax 2.2. Implementation should stay linear unless we explicitly split a later leaf.

## Limitations

- Flags: **UNCLEAR**.
- Phrase bank is real (quotient / twice / less than / groups of / quantity). **UNCLEAR:** D=22 old path jumps to cubes/squares. That is not G6 and not OpenStax 2.2. Implementation should stay linear unless we explicitly split a later leaf.

## Proposed engine (proposal only)

Reuse verbal-expression / AffineInflate *translate* mode. Do not use SolveLinear. New engine only if phrase frames need a typed table (OpenStax Table 2.7).

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
