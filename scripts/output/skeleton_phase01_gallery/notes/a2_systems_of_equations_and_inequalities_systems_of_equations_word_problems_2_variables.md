# Notes — `a2_systems_of_equations_and_inequalities_systems_of_equations_word_problems_2_variables`

> **LOW_VARIETY**

- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Systems of Equations and Inequalities
- **Generator:** `wp_systems`
- **Suggested family:** `wp`

---

## What the question should look like (D=0 vs high D)

- **Skill:** OpenStax number / ticket / geometry / motion story → system.
- **D=0:** OpenStax number / ticket / geometry / motion story → system.
- **High D (≈16–22):** Harder coeffs; inconsistent / dependent cases.
- **Must not:** Dump `\begin{cases}…\end{cases}` without story (old path).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `use_legacy_systems=True`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Taylor buys two items. The costs satisfy } \begin{cases} x - y = -3 \\ -x + 2y = 4 \end{cases}$ | $x = -2,\ y = 1$ |  |
| 0 | 207 | $\text{Alex buys two items. The costs satisfy } \begin{cases} x + y = -3 \\ 2x - y = 0 \end{cases}$ | $x = -1,\ y = -2$ |  |
| 8 | 101 | $\text{Alex buys two items. The costs satisfy } \begin{cases} 2x + y = -3 \\ -2x + 2y = 0 \end{cases}$ | $x = -1,\ y = -1$ |  |
| 8 | 207 | $\text{Sam buys two items. The costs satisfy } \begin{cases} x + 2y = -3 \\ 2x - 2y = 6 \end{cases}$ | $x = 1,\ y = -2$ |  |
| 16 | 101 | $\text{Jordan buys two items. The costs satisfy } \begin{cases} -2x + 3y = 16 \\ -10x + 4y = 36 \end{cases}$ | $x = -2,\ y = 4$ |  |
| 16 | 207 | $\text{Riley buys two items. The costs satisfy } \begin{cases} -4x + y = 0 \\ 2x - 2y = 6 \end{cases}$ | $x = -1,\ y = -4$ |  |
| 22 | 101 | $\text{Jordan buys two items. The costs satisfy } \begin{cases} 2x + 3y = 6 \\ 10x + 15y = 30 \end{cases}$ | $\text{infinitely many solutions}$ |  |
| 22 | 207 | $\text{Jordan buys two items. The costs satisfy } \begin{cases} -7x - 8y = -28 \\ x + 2y = 4 \end{cases}$ | $x = 4,\ y = 0$ |  |

Opt-out flag used: `use_legacy_systems=True`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §5.5 | https://openstax.org/books/elementary-algebra-2e/pages/5-5-solve-mixture-applications-with-systems-of-equations | Number, ticket, geometry, interest frames |
| OpenStax Intermediate Algebra 2e §4.5 | https://openstax.org/books/intermediate-algebra-2e/pages/4-5-solve-applications-with-systems-of-equations | IA application systems |

## Variety notes / UNCLEAR flag

**LOW_VARIETY** — Old path dumps the system (“costs satisfy cases”) — not OpenStax story frames.

## Limitations

Flags for gallery red header: `LOW_VARIETY`.

- **Variety:** one template / Mad-Lib across seeds at easy D — rotate OpenStax-derived frames or algebraic shapes before claiming shipped variety.
- **Difficulty scaling:** Variety thin at fixed D; D may still bump coeffs — check live ladder.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** LinearSystem + wp_packaging OpenStax frames (number, tickets, geometry, motion).
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
