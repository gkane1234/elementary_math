# Notes — `a2_polynomial_functions_graphing`

> **UNCLEAR / NOT_IMPLEMENTED** — Uses `graph_quadratic` generator for general polynomial graphing — may not match degree>2 OpenStax shapes.

- **Display name:** Graphing
- **Category:** Algebra 2 — Polynomial Functions
- **Generator:** `graph_quadratic`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice graphing (catalog: graph_quadratic).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $y = x^2$ | $y = x^2$ | pattern=GraphQuadratic, figure |
| 0 | 207 | $y = x^2 + 1$ | $y = x^2 + 1$ | pattern=GraphQuadratic, figure |
| 8 | 101 | $y = -(x - 2)(x - 4)$ | $y = -(x - 2)(x - 4)$ | pattern=GraphQuadratic, figure |
| 8 | 207 | $y = -2x^{2} + 16x - 34$ | $y = -2x^{2} + 16x - 34$ | pattern=GraphQuadratic, figure |
| 16 | 101 | $y = 2(x - 2)(x - 4)$ | $y = 2(x - 2)(x - 4)$ | pattern=GraphQuadratic, figure |
| 16 | 207 | $y = -3x^{2} - 6x - 6$ | $y = -3x^{2} - 6x - 6$ | pattern=GraphQuadratic, figure |
| 22 | 101 | $y = -\frac{3}{2}x^{2} + 9x - \frac{15}{2}$ | $y = -\frac{3}{2}x^{2} + 9x - \frac{15}{2}$ | pattern=GraphQuadratic, figure |
| 22 | 207 | $y = -\frac{3}{2}x^{2} - 9x - \frac{43}{2}$ | $y = -\frac{3}{2}x^{2} - 9x - \frac{43}{2}$ | pattern=GraphQuadratic, figure |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `graph_quadratic` (same generator `graph_quadratic` unless noted).
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §5.1 | https://openstax.org/books/intermediate-algebra-2e/pages/5-1-add-and-subtract-polynomials | 5.1 Add and Subtract Polynomials — e.g. Example 5.1: Determine whether each polynomial is a monomial, binomial, trinomial, or other polynomial. Then, find the degree of each polynomial. ⓐ $7 y^{2} - 5 y + 3$ ⓑ $−2 a^{4} b^{2}$ ⓒ $3 x^{5} - 4 x^{3} - …; Example 5.2: Add or subtract: ⓐ $25 y^{2} + 15 y^{2}$ ⓑ $16 p q^{3} - \left(\right. −7 p q^{3} \left.\right) .$ |
| Intermediate Algebra 2e §5.3 | https://openstax.org/books/intermediate-algebra-2e/pages/5-3-multiply-polynomials | 5.3 Multiply Polynomials — e.g. Example 5.25: Multiply: ⓐ $\left(\right. 3 x^{2} \left.\right) \left(\right. −4 x^{3} \left.\right)$ ⓑ $\left(\right. \frac{5}{6} x^{3} y \left.\right) \left(\right. 12 x y^{2} \left.\right) .$; Example 5.26: Multiply: ⓐ $−2 y \left(\right. 4 y^{2} + 3 y - 5 \left.\right)$ ⓑ $3 x^{3} y \left(\right. x^{2} - 8 x y + y^{2} \left.\right) .$ |
| Intermediate Algebra 2e §5.4 | https://openstax.org/books/intermediate-algebra-2e/pages/5-4-dividing-polynomials | 5.4 Divide Polynomials — e.g. Example 5.36: Find the quotient: $54 a^{2} b^{3} \div \left(\right. −6 a b^{5} \left.\right) .$; Example 5.37: Find the quotient: $\frac{14 x^{7} y^{12}}{21 x^{11} y^{6}} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Uses `graph_quadratic` generator for general polynomial graphing — may not match degree>2 OpenStax shapes.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).
- **Diagram:** figure/stimulus may be named in answers — verify SVG/stimulus actually renders on worksheets.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Share A1 `graph_quadratic` generator; wire A2 catalog id when skeleton lands.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `graph_quadratic`; equations/WP agent owns solve/WP siblings._
