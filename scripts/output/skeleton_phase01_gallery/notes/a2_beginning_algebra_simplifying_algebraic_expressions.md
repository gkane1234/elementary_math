# Notes — `a2_beginning_algebra_simplifying_algebraic_expressions`

> **LOW_VARIETY** — One template across seeds at D=0.

- **Display name:** Simplifying algebraic expressions
- **Category:** Algebra 2 — Beginning Algebra
- **Generator:** `expand_simplify`
- **Already on skeleton?** yes (`distribute`)
- **Suggested family:** `affine`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Expand and simplify an algebraic expression (distribute, combine).
- **D=0:** $2(x+3)$ or $3x+2x$.
- **High D (≈16–22):** Two binomials; more terms before simplify.
- **Must not:** Solve equations; factor-only prompts.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `{"use_sample_distributive": true}`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $2\left(x + 1\right)$ | $2x + 2$ | pattern=AffineInflate, form=expand_affine |
| 0 | 207 | $2\left(x + 2\right)$ | $2x + 4$ | pattern=AffineInflate, form=expand_affine |
| 8 | 101 | $\left(x - 4\right)2$ | $2x - 8$ | pattern=AffineInflate, form=expand_affine |
| 8 | 207 | $3 * \left(x - 2\right)$ | $3x - 6$ | pattern=AffineInflate, form=expand_affine |
| 16 | 101 | $4 - 3x + 2$ | $-3x + 6$ | pattern=AffineInflate, form=expand_affine |
| 16 | 207 | $-2\left(-3x + 3\right)$ | $6x - 6$ | pattern=AffineInflate, form=expand_affine |
| 22 | 101 | $1 - 3x + 11$ | $-3x + 12$ | pattern=AffineInflate, form=expand_affine |
| 22 | 207 | $-2\left(x - 1\right) + 8x - 11$ | $6x - 9$ | pattern=AffineInflate, form=expand_affine |

Opt-out flag used: `{"use_sample_distributive": true}`

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

- **Reuse:** Existing skeleton slug `distribute` / shared `expand_simplify` family.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `expand_simplify`; equations/WP agent owns solve/WP siblings._
