# Notes — `a2_equations_and_inequalities_absolute_value_inequalities`

> **LOW_VARIETY**

- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Equations and Inequalities
- **Generator:** `absolute_value_inequalities`
- **Suggested family:** `solve`

---

## What the question should look like (D=0 vs high D)

- **Skill:** $|x|<k$ or $|x|>k$; number-line answer.
- **D=0:** $|x|<k$ or $|x|>k$; number-line answer.
- **High D (≈16–22):** $|ax+b|<k$ / $\ge k$ with $|a|\ge 2$ (old medium).
- **Must not:** Compound and/or on this leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `use_sample_absolute_value_inequality=True`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Solve: } \|x\| < 2$ | $-2 < x < 2$ |  |
| 0 | 207 | $\text{Solve: } \|x\| > 1$ | $x < -1 \text{ or } x > 1$ |  |
| 8 | 101 | $\text{Solve: } \|x\| < 2$ | $-2 < x < 2$ |  |
| 8 | 207 | $\text{Solve: } \|x\| > 1$ | $x < -1 \text{ or } x > 1$ |  |
| 16 | 101 | $\text{Solve: } \|x\| > 3$ | $x < -3 \text{ or } x > 3$ |  |
| 16 | 207 | $\text{Solve: } \|x\| > 1$ | $x < -1 \text{ or } x > 1$ |  |
| 22 | 101 | $\text{Solve: } \|x\| > 3$ | $x < -3 \text{ or } x > 3$ |  |
| 22 | 207 | $\text{Solve: } \|x\| > 1$ | $x < -1 \text{ or } x > 1$ |  |

Opt-out flag used: `use_sample_absolute_value_inequality=True`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §3.8 | https://openstax.org/books/elementary-algebra-2e/pages/3-8-solve-absolute-value-inequalities | $|x|<k$, $|x+b|<k$ |
| OpenStax Intermediate Algebra 2e §3.2 | https://openstax.org/books/intermediate-algebra-2e/pages/3-2-solve-absolute-value-inequalities | Linear inner at IA |

## Variety notes / UNCLEAR flag

**LOW_VARIETY** — Old path repeats $|x|<2$ / $|x|>1$ at D=0–16; no $|ax+b|$ shift until skeleton.

## Limitations

Flags for gallery red header: `LOW_VARIETY`.

- **Variety:** one template / Mad-Lib across seeds at easy D — rotate OpenStax-derived frames or algebraic shapes before claiming shipped variety.
- **Difficulty scaling:** Variety thin at fixed D; D may still bump coeffs — check live ladder.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** AbsInequality (equation_skeleton).
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
