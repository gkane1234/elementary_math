# Notes — `a2_equations_and_inequalities_absolute_value_equations`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Equations and Inequalities
- **Generator:** `absolute_value_equations`
- **Suggested family:** `solve`

---

## What the question should look like (D=0 vs high D)

- **Skill:** $|x|=k$ or $|x+b|=k$ (shifted, $a=1$).
- **D=0:** $|x|=k$ or $|x+b|=k$ (shifted, $a=1$).
- **High D (≈16–22):** $|ax+b|=k$ with $|a|\ge 2$; two-abs-equals at medium+.
- **Must not:** Quadratic inner; graph-only.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `use_sample_absolute_value_equation=True`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Solve: } \|x - 2\| = 2$ | $x = 0 \text{ or } x = 4$ |  |
| 0 | 207 | $\text{Solve: } \|x + 1\| = 2$ | $x = -3 \text{ or } x = 1$ |  |
| 8 | 101 | $\text{Solve: } \|-x + 1\| = \|2x + 3\|$ | $x = -4 \text{ or } x = -\frac{2}{3}$ |  |
| 8 | 207 | $\text{Solve: } \|-3x + 2\| = \|x\|$ | $x = \frac{1}{2} \text{ or } x = 1$ |  |
| 16 | 101 | $\text{Solve: } \|2x + 1\| = \|4x + 3\|$ | $x = -1 \text{ or } x = -\frac{2}{3}$ |  |
| 16 | 207 | $\text{Solve: } \|2x + 3\| = \|x + 3\|$ | $x = -2 \text{ or } x = 0$ |  |
| 22 | 101 | $\text{Solve: } \|2x + 1\| = \|4x + 3\|$ | $x = -1 \text{ or } x = -\frac{2}{3}$ |  |
| 22 | 207 | $\text{Solve: } \|2x + 3\| = \|x + 3\|$ | $x = -2 \text{ or } x = 0$ |  |

Opt-out flag used: `use_sample_absolute_value_equation=True`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Intermediate Algebra 2e §3.1 | https://openstax.org/books/intermediate-algebra-2e/pages/3-1-use-a-general-strategy-to-solve-equations | IA absolute value equations |
| OpenStax Elementary Algebra 2e §3.7 | https://openstax.org/books/elementary-algebra-2e/pages/3-7-solve-absolute-value-equations | EA $|x|=k$, $|x+b|=k$ |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** AbsEquation (equation_skeleton).
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
