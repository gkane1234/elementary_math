# Notes — `a2_beginning_algebra_order_of_operations`

> **LOW_VARIETY** — One template across seeds at D=0.

- **Display name:** Order of operations
- **Category:** Algebra 2 — Beginning Algebra
- **Generator:** `order_of_operations`
- **Already on skeleton?** no
- **Suggested family:** `number`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate a numeric expression using order of operations.
- **D=0:** Four ops, no nested parens; small ints.
- **High D (≈16–22):** Nested parens / exponents; larger operands.
- **Must not:** Algebraic variables; equation solving.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $2 \times 2 - 3$ | $1$ | pattern=OrderOfOperations |
| 0 | 207 | $2 \times 2 - 1$ | $3$ | pattern=OrderOfOperations |
| 8 | 101 | $2 \times 3 - 8 \div 4 - 2 \times 2 + 1$ | $1$ | pattern=OrderOfOperations |
| 8 | 207 | $4 \div 2 + 3 \times 2 + 2 \times 2 - 3 \times 3$ | $3$ | pattern=OrderOfOperations |
| 16 | 101 | $9 \div 3 - 3 \times 3 - 8^{2} \div 2 + \left(4 - 2\right) \times 2 - 2 - 3 \times 3 + 46$ | $1$ | pattern=OrderOfOperations |
| 16 | 207 | $12 \div 6 + 2 \times 3 + 18 \div 6 - 2 \times 2 - 12^{2} \div 6 - 3 \times 2 + 26$ | $3$ | pattern=OrderOfOperations |
| 22 | 101 | $9 \div 3 - 4 \times 4 - \left(4 - 2\right) \times 2 - 3 \times 2 + 24 \div 6 + 2 \times 4 + 15 \div 5 + 6 \div 3 + 7$ | $1$ | pattern=OrderOfOperations |
| 22 | 207 | $\left(3 - 2\right) \times 2 + 18 \div 6 - 2 \times 2 - 12^{2} \div 6 - 3 \times 2 - 2 \times 2 - 3 \times 3 + \left(2 + 3\right) \times 2 + 2 \times 3 + 29$ | $3$ | pattern=OrderOfOperations |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `order_of_operations` (same generator `order_of_operations` unless noted).
- **Old path vs A1:** Identical prompts at all sampled D/seeds (shared generator).

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §1.1 | https://openstax.org/books/intermediate-algebra-2e/pages/1-1-use-the-language-of-algebra | 1.1 Use the Language of Algebra |
| Intermediate Algebra 2e §5.2 | https://openstax.org/books/intermediate-algebra-2e/pages/5-2-properties-of-exponents-and-scientific-notation | 5.2 Properties of Exponents and Scientific Notation — e.g. Example 5.12: Simplify each expression: ⓐ $y^{5} \cdot y^{6}$ ⓑ $2^{x} \cdot 2^{3 x}$ ⓒ $2 a^{7} \cdot 3 a .$ ⓓ $d^{4} \cdot d^{5} \cdot d^{2}$; Example 5.13: Simplify each expression: ⓐ $\frac{x^{9}}{x^{7}}$ ⓑ $\frac{3^{10}}{3^{2}}$ ⓒ $\frac{b^{8}}{b^{12}}$ ⓓ $\frac{7^{3}}{7^{5}} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

One template across seeds at D=0.
Flags: `LOW_VARIETY`.

## Limitations

Flags for gallery red header: `LOW_VARIETY`.

- **Variety:** one template / Mad-Lib across seeds at easy D — rotate OpenStax-derived frames or algebraic shapes before claiming shipped variety.
- **Difficulty scaling:** Variety thin at fixed D; D may still bump coeffs — check live ladder.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Share A1 `order_of_operations` generator; wire A2 catalog id when skeleton lands.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `order_of_operations`; equations/WP agent owns solve/WP siblings._
