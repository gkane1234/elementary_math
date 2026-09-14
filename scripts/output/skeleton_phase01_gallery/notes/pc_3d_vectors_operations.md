# Notes — `pc_3d_vectors_operations` (`Operations`)

- **Course:** Precalculus
- **Category:** Precalculus — Three-Dimensional Vectors
- **Generator:** `vector_3d_operations`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student add or subtract 3D vectors componentwise.
- **D=0:** 3D vector add with small integer components (OpenStax PC §9.8).
- **High D (≈16–22):** larger component span; mix of add and subtract.
- **Must not:** cross products (those belong on `pc_cross_products`).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` after miswire fix (`vector_3d_operations`).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Find }\langle 1,3,-2\rangle+\langle 1,-1,0\rangle.$` | `$\langle 2,2,-2\rangle$` | add |
| 8 | 101 | `$\text{Find }\langle 4,-2,3\rangle-\langle 0,2,-5\rangle.$` | `$\langle 4,-4,8\rangle$` | subtract |
| 16 | 101 | `$\text{Find }\langle 2,6,-4\rangle+\langle 7,1,7\rangle.$` | `$\langle 9,7,3\rangle$` | larger span |
| 22 | 101 | `$\text{Find }\langle 2,6,-4\rangle+\langle 7,1,7\rangle.$` | `$\langle 9,7,3\rangle$` | larger span |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §9.8 | https://openstax.org/books/precalculus-2e/pages/9-8-vectors | 3D vector add/subtract |

## Variety notes / flags

- Fixed miswire: old `precalc_foundations` routed this leaf to the cross-product branch.

## Proposed engine (reuse vs new)

- **New/named:** `vector_3d_operations` — add/subtract only; cross products stay on `cross_products`.

## Limitations

- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Live catalog generator; no deferred precalc_foundations stub (PC_DEFERRED empty).
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).
