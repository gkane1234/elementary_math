# Notes — `like_terms` (`g6_combining_like_terms`)

Also covers: `g6_combining_like_terms`, `combining_like_terms`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Combine like terms in an affine sum.
- **D=0:** $3x+2x$ (two like terms).
- **High D (≈16–22):** ~4–5 terms at D=8; up to ~8 at D=16; ~10 with a second variable at D=22.
- **Must not:** Degree ≥2 polynomial simplify; distribute-first problems.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_like_terms=True`.

- **D=0 seed=101:** $2 + 2x + x + 1$ → $3x + 3$
- **D=0 seed=207:** $2 + 1 + 2x + x$ → $3x + 3$
- **D=8 seed=101:** $2 - x + x + 4x + 4$ → $4x + 6$
- **D=8 seed=207:** $-3y + y + 2y - 1 + 2$ → $1$
- **D=16 seed=101:** $4x - 1 + 4 + 4x + 2x - x + 2x + 3$ → $11x + 6$
- **D=16 seed=207:** $3z - 3y + 3 + 1 + 2y + 2z + 2y + y + 1 - y$ → $y + 5z + 5$
- **D=22 seed=101:** $4x + 4 - 2x + 4y + 2y + 3 + 2x + 4x - 1 + 2x$ → $10x + 6y + 6$
- **D=22 seed=207:** $3z - 3y + 3 + 1 + 2y + 2z + 2y + y + 1 - y$ → $y + 5z + 5$

## Current default (same D/seeds)

- **D=0 seed=101:** $x + 2x$ → $3x$ — form_id=like_terms_split
- **D=0 seed=207:** $x + 2x$ → $3x$ — form_id=like_terms_split
- **D=8 seed=101:** $5x + 4 - 2 - 4x - 8x$ → $-7x + 2$ — form_id=like_terms_split
- **D=8 seed=207:** $-4 + 8y - 3y - y + 3$ → $4y - 1$ — form_id=like_terms_split
- **D=16 seed=101:** $8x - 3 + 5x + 4 - 8x - 3 - 4x - 4x$ → $-3x - 2$ — form_id=like_terms_split
- **D=16 seed=207:** $6y - 5 - y - 8y - 1 + 8y + 4 - 3y$ → $2y - 2$ — form_id=like_terms_split
- **D=22 seed=101:** $15x - 6 + 10x + 7 - 15x - 6 - 7x - 7x$ → $-4x - 5$ — form_id=like_terms_split
- **D=22 seed=207:** $-4x + 7 - 2y + 11y - 6 + 9x + 16y - 15y + 3 - 5y$ → $5y + 5x + 4$ — form_id=like_terms_split

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §1.1 / §1.5 (simplify expressions)** — Combine like terms before properties / distributive leftover — https://openstax.org/books/elementary-algebra-2e/pages/1-1-use-the-language-of-algebra

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Default D=0 is simpler than old ($x+2x$ vs $2+2x+x+1$). Term counts track the old like-terms sampler at mid/high D.

## Limitations

- Default D=0 is simpler than old ($x+2x$ vs $2+2x+x+1$). Term counts track the old like-terms sampler at mid/high D.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** AffineInflate like_terms (already wired).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `affine`
