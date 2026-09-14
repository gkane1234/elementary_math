# Notes — `a2_systems_of_equations_and_inequalities_solving_systems_with_three_variables`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Systems of Equations and Inequalities
- **Generator:** `system_three_variables`
- **Suggested family:** `systems`

---

## What the question should look like (D=0 vs high D)

- **Skill:** 3×3 integer system; unique solution.
- **D=0:** 3×3 integer system; unique solution.
- **High D (≈16–22):** Larger coeffs; elimination chain.
- **Must not:** 2×2 only; matrices leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (hand generator)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Solve } \begin{cases} 2x - 2y - 3z=-8\\ -2x + 3y + 2z=8\\ -3x + 2y + 2z=5\end{cases}$ | $(1, 2, 2)$ |  |
| 0 | 207 | $\text{Solve } \begin{cases} 2x + 3y - 3z=7\\ 3x + 3y + 2z=-1\\ -3x + 2y - 3z=-2\end{cases}$ | $(2, -1, -2)$ |  |
| 8 | 101 | $\text{Solve } \begin{cases} -3x - 3y - 4z=15\\ -3x + 4y - 3z=15\\ -4x - 3y + 3z=20\end{cases}$ | $(-5, 0, 0)$ |  |
| 8 | 207 | $\text{Solve } \begin{cases} -2x + y + z=6\\ x - y - 2z=-8\\ x - 2y - z=-10\end{cases}$ | $(0, 4, 2)$ |  |
| 16 | 101 | $\text{Solve } \begin{cases} -5x - y - 6z=37\\ -x + 6y - 5z=35\\ -6x - 5y + z=4\end{cases}$ | $(-3, 2, -4)$ |  |
| 16 | 207 | $\text{Solve } \begin{cases} 5x - 5y - z=-16\\ -5x + y + 5z=-24\\ -x + 5y + 5z=8\end{cases}$ | $(2, 6, -4)$ |  |
| 22 | 101 | $\text{Solve } \begin{cases} 4x + y - 7z=35\\ x + 7y + 4z=33\\ -7x + 4y - z=32\end{cases}$ | $(0, 7, -4)$ |  |
| 22 | 207 | $\text{Solve } \begin{cases} 3x + 3y + 3z=36\\ 3x - 3y + 3z=0\\ 3x + 3y - 3z=18\end{cases}$ | $(3, 6, 3)$ |  |

Opt-out flag used: `none (hand generator)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Intermediate Algebra 2e §4.4 | https://openstax.org/books/intermediate-algebra-2e/pages/4-4-solve-systems-of-equations-with-three-variables | Elimination on 3×3 |
| OpenStax College Algebra 2e §11.1 | https://openstax.org/books/college-algebra-2e/pages/11-1-systems-of-linear-equations-two-variables | CA extends to three variables |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Variety:** Unique integer solutions only in samples — OpenStax §4.4 also has no-solution / infinite; not yet in ladder.
- **Difficulty scaling:** Real — coeffs grow D=0→22; elimination chain length is the hardness (honest).
- **OpenStax:** IA §4.4 cite matches; CA §11.1 is two-var — keep IA as primary.
- **Shipped:** Gallery `a2_system_three_variables` / `LinearSystem3` — clear enough; no graph deferral.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** `LinearSystem3` / systems engine (gallery wired).
- **New:** not required for unique-solution spine.
- **Optional later:** special-case systems (0 / ∞ solutions) as format unlock.
