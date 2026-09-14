# Notes — `distribute` (`g6_distributive_property_algebraic`)

Also covers: `g6_distributive_property_algebraic`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Expand using the distributive property (then combine if leftover).
- **D=0:** $2(x+3)$.
- **High D (≈16–22):** 3 terms inside one factor, then two binomials — not an 8-term sum.
- **Must not:** Old $x(3+1)$ constant-sum with unsimplified $x\cdot1+x\cdot3$ as the key.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_distributive=True`.

- **D=0 seed=101:** $x\left(3 + 1\right)$ → $x\cdot 1 + x\cdot 3$ — form_id=scaled_sum
- **D=0 seed=207:** $x\left(1 + 3\right)$ → $x\cdot 3 + x\cdot 1$ — form_id=scaled_sum
- **D=8 seed=101:** $z\left(3 + 2 + 1\right)$ → $z\cdot 2 + z\cdot 1 + z\cdot 3$ — form_id=scaled_sum
- **D=8 seed=207:** $\left(-2 + 3 + 1\right)x$ → $x\cdot 3 - x\cdot 2 + x\cdot 1$ — form_id=scaled_sum
- **D=16 seed=101:** $\left(3 + 3\right) * \left(2 + x\right)$ → $x\cdot 3 + x\cdot 3 + 2\cdot 3 + 2\cdot 3$ — form_id=two_binomials
- **D=16 seed=207:** $y\left(3 + 1 + 1\right)$ → $y\cdot 1 + y\cdot 3 + y\cdot 1$ — form_id=scaled_sum
- **D=22 seed=101:** $\left(3 + 3\right) * \left(2 + x\right)$ → $x\cdot 3 + x\cdot 3 + 2\cdot 3 + 2\cdot 3$ — form_id=two_binomials
- **D=22 seed=207:** $y\left(3 + 1 + 1\right)$ → $y\cdot 1 + y\cdot 3 + y\cdot 1$ — form_id=scaled_sum

## Current default (same D/seeds)

- **D=0 seed=101:** $2\left(x + 3\right)$ → $2x + 6$ — form_id=distribute_binomial
- **D=0 seed=207:** $2\left(x + 1\right)$ → $2x + 2$ — form_id=distribute_binomial
- **D=8 seed=101:** $2\left(x - 4 - 2\right)$ → $2x - 12$ — form_id=distribute_trinomial
- **D=8 seed=207:** $2\left(y - 2 + 3\right)$ → $2y + 2$ — form_id=distribute_trinomial
- **D=16 seed=101:** $\left(x - 2\right)\left(4 - 5\right)$ → $-x + 2$ — form_id=two_binomials
- **D=16 seed=207:** $\left(y + 3\right)\left(4 - 2\right)$ → $2y + 6$ — form_id=two_binomials
- **D=22 seed=101:** $\left(x - 2\right)\left(4 - 5\right)$ → $-x + 2$ — form_id=two_binomials
- **D=22 seed=207:** $\left(y + 3\right)\left(4 - 2\right)$ → $2y + 6$ — form_id=two_binomials

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §1.5 Properties of Real Numbers** — Distributive: $a(b+c)=ab+ac$ — https://openstax.org/books/elementary-algebra-2e/pages/1-5-properties-of-real-numbers
- **OpenStax Elementary Algebra 2e §6.3** — Monomial × polynomial (harder cousin; keep G6 on affine $k(x+b)$) — https://openstax.org/books/elementary-algebra-2e/pages/6-3-multiply-polynomials

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Default D=0 is OpenStax $2(x+3)$. Old D=0 is $x(3+1)$ with a distributed-but-not-combined answer key.

## Limitations

- Default D=0 is OpenStax $2(x+3)$. Old D=0 is $x(3+1)$ with a distributed-but-not-combined answer key.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** AffineInflate distribute (already wired).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `affine`
