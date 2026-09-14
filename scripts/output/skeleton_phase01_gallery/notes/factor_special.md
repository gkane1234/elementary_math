# Notes — `factor_special` (`polynomial_factoring_special_cases`)

Also covers: `polynomial_factoring_special_cases`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Factor difference of squares or a perfect-square trinomial.
- **D=0:** $x^2-c^2$ or $x^2\pm 2bx+b^2$ (a=1).
- **High D (≈16–22):** $a^2x^2-c^2$ / non-monic perfect squares. Cubes are A2, not this A1 leaf.
- **Must not:** Generic $x^2+bx+c$ that is not a special product; grouping four-terms.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_factor_poly=True`.

- **D=0 seed=101:** $x^{2} - 16$ → $\left(x + 4\right)\left(x - 4\right)$ — form_id=difference_of_squares
- **D=0 seed=207:** $x^{2} - 1$ → $\left(x + 1\right)\left(x - 1\right)$ — form_id=difference_of_squares
- **D=8 seed=101:** $x^{2} - 49$ → $\left(x + 7\right)\left(x - 7\right)$ — form_id=difference_of_squares
- **D=8 seed=207:** $x^{2} - 9$ → $\left(x + 3\right)\left(x - 3\right)$ — form_id=difference_of_squares
- **D=16 seed=101:** $-3x^{2} + 4x^{2} - 49$ → $\left(x + 7\right)\left(x - 7\right)$ — form_id=difference_of_squares
- **D=16 seed=207:** $-x^{2} - 11 + 2\left(x^{2} + 1\right)$ → $\left(x + 3\right)\left(x - 3\right)$ — form_id=difference_of_squares
- **D=22 seed=101:** $3 - 54 + 2 + x^{2}$ → $\left(x + 7\right)\left(x - 7\right)$ — form_id=difference_of_squares
- **D=22 seed=207:** $x^{2} - 11 + 2x^{2} - 2\left(x^{2} - 1\right)$ → $\left(x + 3\right)\left(x - 3\right)$ — form_id=difference_of_squares

Opt-out flag used: `use_factor_poly=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $x^{2} - 16$ → $\left(x + 4\right)\left(x - 4\right)$ — form_id=difference_of_squares, pattern=FactorProduct
- **D=0 seed=207:** $x^{2} - 9$ → $\left(x + 3\right)\left(x - 3\right)$ — form_id=difference_of_squares, pattern=FactorProduct
- **D=8 seed=101:** $x^{2} - 1$ → $\left(x - 1\right)\left(x + 1\right)$ — form_id=difference_of_squares, pattern=FactorProduct
- **D=8 seed=207:** $x^{2} - 81$ → $\left(x - 9\right)\left(x + 9\right)$ — form_id=difference_of_squares, pattern=FactorProduct
- **D=16 seed=101:** $x^{2} - 1$ → $\left(x - 1\right)\left(x + 1\right)$ — form_id=difference_of_squares, pattern=FactorProduct
- **D=16 seed=207:** $x^{2} - 121$ → $\left(x - 11\right)\left(x + 11\right)$ — form_id=difference_of_squares, pattern=FactorProduct
- **D=22 seed=101:** $x^{2} + 6 - 7$ → $\left(x - 1\right)\left(x + 1\right)$ — form_id=difference_of_squares, pattern=FactorProduct
- **D=22 seed=207:** $3x^{2} - 2x^{2} - 121$ → $\left(x - 11\right)\left(x + 11\right)$ — form_id=difference_of_squares, pattern=FactorProduct

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §7.4 | https://openstax.org/books/elementary-algebra-2e/pages/7-4-factor-special-products | Difference of squares; perfect-square trinomials. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP. Algebra shapes follow the old path; default is the live skeleton.
Flag UNCLEAR only if old path is a dump stub or the skill is wrong.

## Limitations

- UNCLEAR: gold look not fully locked — keep red gallery header; do not invent a new engine.
- Gallery section slug: `factor_special` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** FactorProduct special factor / poly_skeleton (already wired). Opt-out: `use_factor_poly`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `other`

_Catalog:_ Algebra 1 — Polynomials — Special cases. Generator `polynomial_factoring_special_cases`.
