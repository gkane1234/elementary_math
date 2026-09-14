# Notes — `evaluate_affine` (`g6_evaluating_algebraic_expressions`)

Also covers: `g6_evaluating_algebraic_expressions`, `evaluate_algebraic_expressions`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate an affine expression by substituting a given $x=k$.
- **D=0:** $3+x$ or $1-3x$ when $x=k$ — **not** $2(x+3)$.
- **High D (≈16–22):** Leftover distribute inside the expression, still evaluate.
- **Must not:** Ask to expand without substituting.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_evaluate=True`.

- **D=0 seed=101:** $3 + x \text{ when } x = -1$ → $2$
- **D=0 seed=207:** $1 - 3x \text{ when } x = 3$ → $-8$
- **D=8 seed=101:** $-2x + 6 + \left(x - 1\right)3 \text{ when } x = -1$ → $2$
- **D=8 seed=207:** $-y + 3 + \left(y + 1\right)\left(-2\right) \text{ when } y = 3$ → $-8$
- **D=16 seed=101:** $5x + \left(-x + 1\right)3 \text{ when } x = 0$ → $3$
- **D=16 seed=207:** $-7y + 5 + \left(2y - 2\right)2 \text{ when } y = 3$ → $-8$
- **D=22 seed=101:** $-2x - 9 + \left(x + 3\right)4 \text{ when } x = 0$ → $3$
- **D=22 seed=207:** $-9y + 7 + \left(2y - 2\right)3 \text{ when } y = 3$ → $-8$

## Current default (same D/seeds)

- **D=0 seed=101:** $x + 3 \text{ when } x = 1$ → $4$ — form_id=evaluate_affine
- **D=0 seed=207:** $1 + 2x \text{ when } x = 3$ → $7$ — form_id=evaluate_affine
- **D=8 seed=101:** $2\left(x + 2\right) - 3x - 7 \text{ when } x = 2$ → $-5$ — form_id=evaluate_affine
- **D=8 seed=207:** $4y - 4 - 3 * \left(y - 2\right) \text{ when } y = 3$ → $5$ — form_id=evaluate_affine
- **D=16 seed=101:** $3 * \left(x + 2\right) - 6 \text{ when } x = 1$ → $3$ — form_id=evaluate_affine
- **D=16 seed=207:** $5y - 4 - 2 * \left(y - 1\right) \text{ when } y = 3$ → $7$ — form_id=evaluate_affine
- **D=22 seed=101:** $3 * \left(x + 2\right) - 6 \text{ when } x = 1$ → $3$ — form_id=evaluate_affine
- **D=22 seed=207:** $5y - 4 - 2 * \left(y - 1\right) \text{ when } y = 3$ → $7$ — form_id=evaluate_affine

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §1.1 (evaluate) / Be Prepared 2.1 cites Example 1.54** — Evaluate $x+4$ when $x=-3$ — https://openstax.org/books/elementary-algebra-2e/pages/1-1-use-the-language-of-algebra

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Default D=0 is $x+3$ when $x=1$; old $3+x$ when $x=-1$. Both match gold.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** AffineInflate evaluate (already wired).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `affine`
