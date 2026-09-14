# Notes — `a2_radical_functions_and_rational_exponents_multiplying_radical_expressions`

> **LOW_VARIETY** — One template across seeds at D=0.

- **Display name:** Multiplying radical expressions
- **Category:** Algebra 2 — Radical Functions and Rational Exponents
- **Generator:** `radical_multiply`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice multiplying radical expressions (catalog: radical_multiply).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\sqrt{18} \cdot \sqrt{14}$ | $6\sqrt{7}$ | pattern=RadicalMul |
| 0 | 207 | $\sqrt{8} \cdot \sqrt{5}$ | $2\sqrt{10}$ | pattern=RadicalMul |
| 8 | 101 | $\sqrt{12} \cdot 5\sqrt{27}$ | $90$ | pattern=RadicalMul |
| 8 | 207 | $3\sqrt{10} \cdot 2\sqrt{2}$ | $12\sqrt{5}$ | pattern=RadicalMul |
| 16 | 101 | $\left(4\sqrt{14} + \sqrt{10}\right)\left(5\sqrt{14} - 2\sqrt{10}\right)$ | $260 - 6\sqrt{35}$ | pattern=RadicalMul |
| 16 | 207 | $\left(3\sqrt{5} + 2\sqrt{2}\right)\left(4\sqrt{5} - \sqrt{2}\right)$ | $56 + 5\sqrt{10}$ | pattern=RadicalMul |
| 22 | 101 | $\left(4\sqrt{14} + \sqrt{10}\right)\left(5\sqrt{14} - 2\sqrt{10}\right)$ | $260 - 6\sqrt{35}$ | pattern=RadicalMul |
| 22 | 207 | $\left(3\sqrt{5} + 2\sqrt{2}\right)\left(4\sqrt{5} - \sqrt{2}\right)$ | $56 + 5\sqrt{10}$ | pattern=RadicalMul |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `radical_multiply` (same generator `radical_multiply` unless noted).
- **Old path vs A1:** Identical prompts at all sampled D/seeds (shared generator).

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §8.1 | https://openstax.org/books/intermediate-algebra-2e/pages/8-1-simplify-expressions-with-roots | 8.1 Simplify Expressions with Roots — e.g. Example 8.1: Simplify: ⓐ $\sqrt{144}$ ⓑ $− \sqrt{289} .$; Example 8.2: Simplify: ⓐ $\sqrt{−196}$ ⓑ $− \sqrt{64} .$ |
| Intermediate Algebra 2e §8.2 | https://openstax.org/books/intermediate-algebra-2e/pages/8-2-simplify-radical-expressions | 8.2 Simplify Radical Expressions — e.g. Example 8.13: Simplify Square Roots Using the Product Property of Roots Simplify: $\sqrt{98} .$; Example 8.14: Simplify: ⓐ $\sqrt{500}$ ⓑ $\sqrt[3]{16}$ ⓒ $\sqrt[4]{243} .$ |
| Intermediate Algebra 2e §8.3 | https://openstax.org/books/intermediate-algebra-2e/pages/8-3-simplify-rational-exponents | 8.3 Simplify Rational Exponents — e.g. Example 8.26: Write as a radical expression: ⓐ $x^{\frac{1}{2}}$ ⓑ $y^{\frac{1}{3}}$ ⓒ $z^{\frac{1}{4}} .$; Example 8.27: Write with a rational exponent: ⓐ $\sqrt{5 y}$ ⓑ $\sqrt[3]{4 x}$ ⓒ $3 \sqrt[4]{5 z} .$ |

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

- **Reuse:** Share A1 `radical_multiply` generator; wire A2 catalog id when skeleton lands.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `radical_multiply`; equations/WP agent owns solve/WP siblings._
