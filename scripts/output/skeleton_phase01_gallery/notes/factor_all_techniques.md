# Notes — `factor_all_techniques` (`polynomial_factoring_general_strategy`)

Also covers: `polynomial_factoring_general_strategy`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Choose a factoring method and factor completely (GCF, trinomial, special, grouping).
- **D=0:** GCF-only or a simple monic trinomial — one obvious method.
- **High D (≈16–22):** D-weighted mix; GCF then a pattern; grouping. Still A1 methods (no cubes-only A2).
- **Must not:** A dedicated single-method leaf’s exclusive shape at every D (mixer must actually mix at high D).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_factor_poly=True`.

- **D=0 seed=101:** $x^{2} + 7x + 12$ → $\left(x + 3\right)\left(x + 4\right)$ — form_id=trinomial_x2_bx_c
- **D=0 seed=207:** $x^{2} - 4$ → $\left(x + 2\right)\left(x - 2\right)$ — form_id=difference_of_squares
- **D=8 seed=101:** $x^{2} + 2x - 3$ → $\left(x + 3\right)\left(x - 1\right)$ — form_id=trinomial_x2_bx_c
- **D=8 seed=207:** $x^{2} + 2x + 1$ → $\left(x + 1\right)^{2}$ — form_id=perfect_square_trinomial
- **D=16 seed=101:** $7x^{2} - 10x + 6 - 3x^{2}$ → $2\left(x - 1\right)\left(2x - 3\right)$ — form_id=trinomial_ax2_bx_c
- **D=16 seed=207:** $10x^{2} - 90x + 77 + 3$ → $10\left(x - 1\right)\left(x - 8\right)$ — form_id=gcf_then_pattern
- **D=22 seed=101:** $22x^{2} - 7x - 3x + 6$ → $2\left(x - 1\right)\left(2x - 3\right)$ — form_id=trinomial_ax2_bx_c
- **D=22 seed=207:** $10y^{2} - 90y + 82 + 1 - 3$ → $10\left(y - 1\right)\left(y - 8\right)$ — form_id=gcf_then_pattern

Opt-out flag used: `use_factor_poly=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $3x + 6$ → $3\left(x + 2\right)$ — form_id=gcf_monomial, pattern=FactorGcf
- **D=0 seed=207:** $x^{2} - 2x - 15$ → $\left(x + 3\right)\left(x - 5\right)$ — form_id=trinomial_x2_bx_c, pattern=FactorProduct
- **D=8 seed=101:** $2x^{3} + 12x^{2} - 9x - 54$ → $\left(x + 6\right)\left(2x^{2} - 9\right)$ — form_id=factor_by_grouping, pattern=FactorProduct
- **D=8 seed=207:** $x^{2} - 2x - 63$ → $\left(x + 7\right)\left(x - 9\right)$ — form_id=trinomial_x2_bx_c, pattern=FactorProduct
- **D=16 seed=101:** $3x^{2} - 16x + 13$ → $\left(3x - 13\right)\left(x - 1\right)$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct
- **D=16 seed=207:** $2x^{2} - 15x + 13$ → $\left(2x - 13\right)\left(x - 1\right)$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct
- **D=22 seed=101:** $-16x + 13 - 2x^{2} + 5x^{2}$ → $\left(3x - 13\right)\left(x - 1\right)$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct
- **D=22 seed=207:** $-x - 4 - 2x^{2} + 5x^{2}$ → $\left(x + 1\right)\left(3x - 4\right)$ — form_id=trinomial_ax2_bx_c, pattern=FactorProduct

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §7.5 | https://openstax.org/books/elementary-algebra-2e/pages/7-5-general-strategy-for-factoring-polynomials | Choose method / factor completely — GCF first, then pattern. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP. Algebra shapes follow the old path; default is the live skeleton.
Flag UNCLEAR only if old path is a dump stub or the skill is wrong.

## Limitations

- UNCLEAR: gold look not fully locked — keep red gallery header; do not invent a new engine.
- Gallery section slug: `factor_all_techniques` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** FactorProduct all-techniques mixer / poly_skeleton (already wired). Opt-out: `use_factor_poly`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `other`

_Catalog:_ Algebra 1 — Polynomials — General strategy. Generator `polynomial_factoring_general_strategy`.
