# Notes — `a2_polynomial_functions_the_binomial_theorem`

> **LOW_VARIETY** — One template across seeds at D=0.

- **Display name:** The Binomial Theorem
- **Category:** Algebra 2 — Polynomial Functions
- **Generator:** `binomial_theorem`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice the binomial theorem (catalog: binomial_theorem).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the coefficient of } x^{1} \text{ in } (1 + x)^{3}.$ | $3$ | — |
| 0 | 207 | $\text{Find the coefficient of } x^{3} \text{ in } (1 + x)^{4}.$ | $4$ | — |
| 8 | 101 | $\text{Find the coefficient of } x^{1} \text{ in } (1 + x)^{4}.$ | $4$ | — |
| 8 | 207 | $\text{Find the coefficient of } x^{1} \text{ in } (2 + x)^{4}.$ | $32$ | — |
| 16 | 101 | $\text{Find the coefficient of } x^{3} \text{ in } (1 + x)^{5}.$ | $10$ | — |
| 16 | 207 | $\text{Find the coefficient of } x^{4} \text{ in } (2 + x)^{6}.$ | $60$ | — |
| 22 | 101 | $\text{Find the coefficient of } x^{5} \text{ in } (2 + x)^{6}.$ | $12$ | — |
| 22 | 207 | $\text{Find the coefficient of } x^{3} \text{ in } (1 + x)^{5}.$ | $10$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §5.1 | https://openstax.org/books/intermediate-algebra-2e/pages/5-1-add-and-subtract-polynomials | 5.1 Add and Subtract Polynomials — e.g. Example 5.1: Determine whether each polynomial is a monomial, binomial, trinomial, or other polynomial. Then, find the degree of each polynomial. ⓐ $7 y^{2} - 5 y + 3$ ⓑ $−2 a^{4} b^{2}$ ⓒ $3 x^{5} - 4 x^{3} - …; Example 5.2: Add or subtract: ⓐ $25 y^{2} + 15 y^{2}$ ⓑ $16 p q^{3} - \left(\right. −7 p q^{3} \left.\right) .$ |
| Intermediate Algebra 2e §5.3 | https://openstax.org/books/intermediate-algebra-2e/pages/5-3-multiply-polynomials | 5.3 Multiply Polynomials — e.g. Example 5.25: Multiply: ⓐ $\left(\right. 3 x^{2} \left.\right) \left(\right. −4 x^{3} \left.\right)$ ⓑ $\left(\right. \frac{5}{6} x^{3} y \left.\right) \left(\right. 12 x y^{2} \left.\right) .$; Example 5.26: Multiply: ⓐ $−2 y \left(\right. 4 y^{2} + 3 y - 5 \left.\right)$ ⓑ $3 x^{3} y \left(\right. x^{2} - 8 x y + y^{2} \left.\right) .$ |
| Intermediate Algebra 2e §5.4 | https://openstax.org/books/intermediate-algebra-2e/pages/5-4-dividing-polynomials | 5.4 Divide Polynomials — e.g. Example 5.36: Find the quotient: $54 a^{2} b^{3} \div \left(\right. −6 a b^{5} \left.\right) .$; Example 5.37: Find the quotient: $\frac{14 x^{7} y^{12}}{21 x^{11} y^{6}} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

One template across seeds at D=0.
Flags: `LOW_VARIETY`.

## Limitations

Flags for gallery red header: `LOW_VARIETY` · `LIMITATIONS`.

- **Variety:** Coefficient-of-$x^k$ in $(1+x)^n$ / $(a+x)^n$ only — no expand-all / Pascal-row stems.
- **Difficulty scaling:** $n$ and $a\neq 1$ grow with D; template shape is fixed.
- **OpenStax gap:** Notes table cites IA §5.1 add/subtract and §5.3 multiply — **wrong chapter family** for binomial theorem. Prefer College Algebra binomial / Pascal (or IA special-products only if that is the gold).
- **Shipped?** Gallery samples exist; do not treat OpenStax alignment as done until cites are fixed.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `binomial_theorem` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `binomial_theorem`; equations/WP agent owns solve/WP siblings._
