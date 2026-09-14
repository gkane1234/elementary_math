# Notes — `a2_polynomial_functions_dividing`

> **UNCLEAR** — OpenStax splits monomial ÷ poly (§5.4) vs long division (§5.5); one leaf mixes both.

- **Display name:** Dividing
- **Category:** Algebra 2 — Polynomial Functions
- **Generator:** `polynomial_long_division`
- **Already on skeleton?** yes (`polynomial_long_division`)
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice dividing (catalog: polynomial_long_division).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\frac{4x^{2}+13x+10}{4x+5}$ | $x+2$ | pattern=PolyLongDiv |
| 0 | 207 | $\frac{4x^{3}-18x^{2}-5x-25}{x-5}$ | $4x^{2}+2x+5$ | pattern=PolyLongDiv |
| 8 | 101 | $\frac{4x^{3}+9x^{2}-5x-3}{x^{2}+3x+1}$ | $4x-3$ | pattern=PolyLongDiv |
| 8 | 207 | $\frac{36x^{4}+30x^{3}+42x^{2}+28x-6}{6x-1}$ | $6x^{3}+6x^{2}+8x+6$ | pattern=PolyLongDiv |
| 16 | 101 | $\frac{75x^{3}+210x^{2}-111x-23}{5x^{2}+13x-10}$ | $15x+3+\frac{7}{5x^{2}+13x-10}$ | pattern=PolyLongDiv |
| 16 | 207 | $\frac{24x^{5}+119x^{4}+66x^{3}-100x^{2}-193x-40}{3x^{2}+13x+2}$ | $8x^{3}+5x^{2}-5x-15+\frac{12x-10}{3x^{2}+13x+2}$ | pattern=PolyLongDiv |
| 22 | 101 | $\frac{36x^{4}-42x^{3}-22x^{2}+10x+5}{4x-6}$ | $9x^{3}+3x^{2}-x+1+\frac{11}{4x-6}$ | pattern=PolyLongDiv |
| 22 | 207 | $\frac{24x^{3}-88x^{2}+212x-94}{2x^{2}-6x+13}$ | $12x-8+\frac{8x+10}{2x^{2}-6x+13}$ | pattern=PolyLongDiv |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `polynomial_long_division` (same generator `polynomial_long_division` unless noted).
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.
  - D=0.0 seed=101: A2 `\frac{4x^{2}+13x+10}{4x+5}` ≠ A1 `\frac{15x^{2}+13x-20}{5x-4}`
  - D=0.0 seed=207: A2 `\frac{4x^{3}-18x^{2}-5x-25}{x-5}` ≠ A1 `\frac{6x^{3}-12x^{2}+9x-3}{3x-3}`
  - D=8.0 seed=101: A2 `\frac{4x^{3}+9x^{2}-5x-3}{x^{2}+3x+1}` ≠ A1 `\frac{10x^{2}-49x+36}{10x-9}`
  - D=8.0 seed=207: A2 `\frac{36x^{4}+30x^{3}+42x^{2}+28x-6}{6x-1}` ≠ A1 `\frac{63x^{3}+32x^{2}-144x+63}{7x^{2}+9x-9}`
  - D=16.0 seed=101: A2 `\frac{75x^{3}+210x^{2}-111x-23}{5x^{2}+13x-10}` ≠ A1 `\frac{56x^{3}+62x^{2}+141x+54}{4x^{2}+3x+9}`
  - D=16.0 seed=207: A2 `\frac{24x^{5}+119x^{4}+66x^{3}-100x^{2}-193x-40}{3x^{2}+13x+2}` ≠ A1 `\frac{21x^{3}-57x^{2}-75x-126}{3x-12}`
  - D=22.0 seed=101: A2 `\frac{36x^{4}-42x^{3}-22x^{2}+10x+5}{4x-6}` ≠ A1 `\frac{52x^{4}+65x^{3}-169x^{2}+13x+201}{13x+13}`
  - D=22.0 seed=207: A2 `\frac{24x^{3}-88x^{2}+212x-94}{2x^{2}-6x+13}` ≠ A1 `\frac{30x^{3}-103x^{2}+76x-11}{15x^{2}-14x+3}`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §5.1 | https://openstax.org/books/intermediate-algebra-2e/pages/5-1-add-and-subtract-polynomials | 5.1 Add and Subtract Polynomials — e.g. Example 5.1: Determine whether each polynomial is a monomial, binomial, trinomial, or other polynomial. Then, find the degree of each polynomial. ⓐ $7 y^{2} - 5 y + 3$ ⓑ $−2 a^{4} b^{2}$ ⓒ $3 x^{5} - 4 x^{3} - …; Example 5.2: Add or subtract: ⓐ $25 y^{2} + 15 y^{2}$ ⓑ $16 p q^{3} - \left(\right. −7 p q^{3} \left.\right) .$ |
| Intermediate Algebra 2e §5.3 | https://openstax.org/books/intermediate-algebra-2e/pages/5-3-multiply-polynomials | 5.3 Multiply Polynomials — e.g. Example 5.25: Multiply: ⓐ $\left(\right. 3 x^{2} \left.\right) \left(\right. −4 x^{3} \left.\right)$ ⓑ $\left(\right. \frac{5}{6} x^{3} y \left.\right) \left(\right. 12 x y^{2} \left.\right) .$; Example 5.26: Multiply: ⓐ $−2 y \left(\right. 4 y^{2} + 3 y - 5 \left.\right)$ ⓑ $3 x^{3} y \left(\right. x^{2} - 8 x y + y^{2} \left.\right) .$ |
| Intermediate Algebra 2e §5.4 | https://openstax.org/books/intermediate-algebra-2e/pages/5-4-dividing-polynomials | 5.4 Divide Polynomials — e.g. Example 5.36: Find the quotient: $54 a^{2} b^{3} \div \left(\right. −6 a b^{5} \left.\right) .$; Example 5.37: Find the quotient: $\frac{14 x^{7} y^{12}}{21 x^{11} y^{6}} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

OpenStax splits monomial ÷ poly (§5.4) vs long division (§5.5); one leaf mixes both.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `UNCLEAR`.

- **UNCLEAR gold:** old path and OpenStax skill intent diverge, or dump/wrong-skill shapes — do not wire a new core until notes lock.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing skeleton slug `polynomial_long_division` / shared `polynomial_long_division` family.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `polynomial_long_division`; equations/WP agent owns solve/WP siblings._
