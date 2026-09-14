# Notes — `factor_grouping` (`polynomial_factoring_grouping`)

Also covers: `polynomial_factoring_grouping`

Flags:

- `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Factor a four-term polynomial by grouping.
- **D=0:** Four terms, small ints, obvious pair GCFs (OpenStax grouping — not a trinomial).
- **High D (≈16–22):** Larger coeffs; degree up to 3. Not a quadratic trinomial.
- **Must not:** Monic $x^2+bx+c$; GCF-only binomials.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_factor_poly=True`.

- **D=0 seed=101:** $3x^{2} + 10x + 8$ → $\left(x + 2\right)\left(3x + 4\right)$
- **D=0 seed=207:** $x^{2} + 4x + 3$ → $\left(x + 3\right)\left(x + 1\right)$
- **D=8 seed=101:** $3x^{3} - 6x^{2} + 4x - 8$ → $\left(x - 2\right)\left(3x^{2} + 4\right)$
- **D=8 seed=207:** $x^{3} - 2x^{2} - x + 2$ → $\left(x - 2\right)\left(x^{2} - 1\right)$
- **D=16 seed=101:** $22x - 8 - 6x^{2} + 3x^{3}$ → $\left(x - 2\right)\left(3x^{2} + 4\right)$
- **D=16 seed=207:** $-2x^{2} + 2 - x + x^{3}$ → $\left(x - 2\right)\left(x^{2} - 1\right)$
- **D=22 seed=101:** $-x^{3} - 6x^{2} + 4x + 4\left(x^{3} - 2\right)$ → $\left(x - 2\right)\left(3x^{2} + 4\right)$
- **D=22 seed=207:** $x^{3} + 2\left(x^{3} + 1\right) - 2x^{3} - x - 2x^{2}$ → $\left(x - 2\right)\left(x^{2} - 1\right)$

Opt-out flag used: `use_factor_poly=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $x^{3} - x^{2} + 3x - 3$ → $\left(x - 1\right)\left(x^{2} + 3\right)$ — form_id=factor_by_grouping, pattern=FactorProduct
- **D=0 seed=207:** $x^{3} - 5x^{2} - x + 5$ → $\left(x - 5\right)\left(x^{2} - 1\right)$ — form_id=factor_by_grouping, pattern=FactorProduct
- **D=8 seed=101:** $2x^{3} + 12x^{2} - 9x - 54$ → $\left(x + 6\right)\left(2x^{2} - 9\right)$ — form_id=factor_by_grouping, pattern=FactorProduct
- **D=8 seed=207:** $2x^{3} - 6x^{2} + 2x - 6$ → $\left(x - 3\right)\left(2x^{2} + 2\right)$ — form_id=factor_by_grouping, pattern=FactorProduct
- **D=16 seed=101:** $3x^{3} + 27x^{2} - 13x - 117$ → $\left(x + 9\right)\left(3x^{2} - 13\right)$ — form_id=factor_by_grouping, pattern=FactorProduct
- **D=16 seed=207:** $3x^{3} - 12x^{2} + 2x - 8$ → $\left(x - 4\right)\left(3x^{2} + 2\right)$ — form_id=factor_by_grouping, pattern=FactorProduct
- **D=22 seed=101:** $29x^{2} - 117 - 2x^{2} - 13x + 3x^{3}$ → $\left(x + 9\right)\left(3x^{2} - 13\right)$ — form_id=factor_by_grouping, pattern=FactorProduct
- **D=22 seed=207:** $3x^{3} - 12 + 3x - 12x^{2}$ → $\left(x - 4\right)\left(3x^{2} + 3\right)$ — form_id=factor_by_grouping, pattern=FactorProduct

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §7.1 | https://openstax.org/books/elementary-algebra-2e/pages/7-1-greatest-common-factor-and-factor-by-grouping | Four-term grouping after (optional) monomial GCF. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes / UNCLEAR flag

`UNCLEAR` — old D=0 is a quadratic trinomial ($3x^2+10x+8$), not grouping. Old D≥8
is four-term grouping. Default D=0 is already grouping ($x^3-x^2+3x-3$). Gold is
OpenStax EA §7.1 four-term grouping at every D; do not copy old D=0 trinomials onto
this leaf.

## Limitations

- UNCLEAR: gold look not fully locked — keep red gallery header; do not invent a new engine.
- Gallery section slug: `factor_grouping` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** FactorProduct grouping / poly_skeleton (already wired). Opt-out: `use_factor_poly`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `other`

_Catalog:_ Algebra 1 — Polynomials — By grouping. Generator `polynomial_factoring_grouping`.
