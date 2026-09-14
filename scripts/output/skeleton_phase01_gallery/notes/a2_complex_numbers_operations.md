# Notes — `a2_complex_numbers_operations`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Complex Numbers
- **Generator:** `complex_operations`
- **Suggested family:** `number`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Add/subtract or multiply small $a+bi$.
- **D=0:** Add/subtract or multiply small $a+bi$.
- **High D (≈16–22):** FOIL multiply; larger coeffs.
- **Must not:** Graphing / polar on this leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (hand generator)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\left(3 - i\right)\left(3 + 2i\right)$ | $11 + 3i$ |  |
| 0 | 207 | $\left(2 - 2i\right) - \left(-2 + i\right)$ | $4 - 3i$ |  |
| 8 | 101 | $\left(4\right)\left(3i\right)$ | $12i$ |  |
| 8 | 207 | $\left(-2 + 5i\right)\left(-3 - 5i\right)$ | $31 - 5i$ |  |
| 16 | 101 | $\left(4 + 3i\right)\left(2 - 2i\right)$ | $14 - 2i$ |  |
| 16 | 207 | $\left(-2 + i\right)\left(1 - 6i\right)$ | $4 + 13i$ |  |
| 22 | 101 | $\left(4 + 8i\right)\left(5 - 7i\right)$ | $76 + 12i$ |  |
| 22 | 207 | $\left(2 - 9i\right)\left(3 - 2i\right)$ | $-12 - 31i$ |  |

Opt-out flag used: `none (hand generator)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax College Algebra 2e §2.4 | https://openstax.org/books/college-algebra-2e/pages/2-4-complex-numbers | Add, subtract, multiply complex numbers |
| OpenStax Intermediate Algebra 2e §8.8 | https://openstax.org/books/intermediate-algebra-2e/pages/8-8-use-the-complex-number-system | IA complex intro |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Variety:** Add/sub/mul of $a+bi$ only — division / powers are other leaves (rationalize, abs).
- **Difficulty scaling:** Real — FOIL multiply and larger coeffs at high D.
- **OpenStax:** CA §2.4 / IA §8.8 cites match operations skill.
- **Shipped:** Gallery `a2_complex_operations` — clear; graphing complex is a separate UNCLEAR leaf.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** `complex_algebra` / `ComplexOp` (gallery wired).
- **New:** not required for ±/× spine.
