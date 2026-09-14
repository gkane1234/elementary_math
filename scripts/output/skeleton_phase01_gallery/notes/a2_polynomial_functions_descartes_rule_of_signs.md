# Notes — `a2_polynomial_functions_descartes_rule_of_signs`

> **UNCLEAR** — Sign-variation rule — verify prompt asks for sign changes vs root count.

- **Display name:** Descartes' Rule of Signs
- **Category:** Algebra 2 — Polynomial Functions
- **Generator:** `descartes_rule_of_signs`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice descartes' rule of signs (catalog: descartes_rule_of_signs).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Use Descartes' Rule of Signs for } f(x)=x^{3} + 3x^{2} - x + 2.$ | $\text{positive: } 2, 0, \ldots; \text{negative: } 1, -1, \ldots$ | — |
| 0 | 207 | $\text{Use Descartes' Rule of Signs for } f(x)=-x^{3} + 4x^{2} - 2x - 3.$ | $\text{positive: } 2, 0, \ldots; \text{negative: } 1, -1, \ldots$ | — |
| 8 | 101 | $\text{Use Descartes' Rule of Signs for } f(x)=-6x^{4} + 2x^{3} + 6x^{2} - 4x + 5.$ | $\text{positive: } 3, 1, \ldots; \text{negative: } 1, -1, \ldots$ | — |
| 8 | 207 | $\text{Use Descartes' Rule of Signs for } f(x)=-x^{3} + 6x^{2} + 4x - 2.$ | $\text{positive: } 2, 0, \ldots; \text{negative: } 1, -1, \ldots$ | — |
| 16 | 101 | $\text{Use Descartes' Rule of Signs for } f(x)=-4x^{5} + 4x^{4} + x^{3} - 7x^{2} + 3x + 6.$ | $\text{positive: } 3, 1, \ldots; \text{negative: } 2, 0, \ldots$ | — |
| 16 | 207 | $\text{Use Descartes' Rule of Signs for } f(x)=3x^{5} + 3x^{4} + 3x^{3} + 5x^{2} + 3x - 2.$ | $\text{positive: } 1, -1, \ldots; \text{negative: } 4, 2, \ldots$ | — |
| 22 | 101 | $\text{Use Descartes' Rule of Signs for } f(x)=-3x^{5} + 6x^{4} + 6x^{3} - x^{2} + 6x + 6.$ | $\text{positive: } 3, 1, \ldots; \text{negative: } 2, 0, \ldots$ | — |
| 22 | 207 | $\text{Use Descartes' Rule of Signs for } f(x)=6x^{6} + 5x^{5} - 4x^{4} - 4x^{3} + 10x^{2} - 5x - 10.$ | $\text{positive: } 3, 1, \ldots; \text{negative: } 3, 1, \ldots$ | — |

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

Sign-variation rule — verify prompt asks for sign changes vs root count.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `UNCLEAR`.

- **UNCLEAR gold:** old path and OpenStax skill intent diverge, or dump/wrong-skill shapes — do not wire a new core until notes lock.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `descartes_rule_of_signs` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `descartes_rule_of_signs`; equations/WP agent owns solve/WP siblings._
