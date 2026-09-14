# Notes — `a2_linear_relations_and_functions_writing_linear_equations`

> **UNCLEAR** — A2 type_id samples differ from A1 alias at same D/seeds — verify intended divergence.

- **Display name:** Writing linear equations
- **Category:** Algebra 2 — Linear Relations and Functions
- **Generator:** `writing_linear_equations`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice writing linear equations (catalog: writing_linear_equations).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Write } 12x - 4y = 8 \text{ in slope-intercept form.}$ | $y = 3x - 2$ | — |
| 0 | 207 | $\text{Write } y + 1 = 2(x + 3) \text{ in slope-intercept form.}$ | $y = 2x + 5$ | — |
| 8 | 101 | $\text{Write } -3x - y = -3 \text{ in slope-intercept form.}$ | $y = -3x + 3$ | — |
| 8 | 207 | $\text{Write } y + 33 = 4(x + 8) \text{ in slope-intercept form.}$ | $y = 4x - 1$ | — |
| 16 | 101 | $\text{Write } -16x - 4y = -20 \text{ in slope-intercept form.}$ | $y = -4x + 5$ | — |
| 16 | 207 | $\text{Write } y + 113 = 9(x + 12) \text{ in slope-intercept form.}$ | $y = 9x - 5$ | — |
| 22 | 101 | $\text{Write } -16x - 4y = -20 \text{ in slope-intercept form.}$ | $y = -4x + 5$ | — |
| 22 | 207 | $\text{Write } y + 113 = 9(x + 12) \text{ in slope-intercept form.}$ | $y = 9x - 5$ | — |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `writing_linear_equations` (same generator `writing_linear_equations` unless noted).
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.
  - D=0.0 seed=101: A2 `\text{Write } 12x - 4y = 8 \text{ in slope-intercept form.}` ≠ A1 `\text{Write the slope-intercept equation of the line with slope } 1 \text{ and …`
  - D=0.0 seed=207: A2 `\text{Write } y + 1 = 2(x + 3) \text{ in slope-intercept form.}` ≠ A1 `\text{Write the slope-intercept equation of the line with slope } 3 \text{ and …`
  - D=8.0 seed=101: A2 `\text{Write } -3x - y = -3 \text{ in slope-intercept form.}` ≠ A1 `\text{Write an equation of the line through } (-2, -2) \text{ and } (0, 0).`
  - D=8.0 seed=207: A2 `\text{Write } y + 33 = 4(x + 8) \text{ in slope-intercept form.}` ≠ A1 `\text{Write an equation of the line through } (2, 6) \text{ and } (4, 12).`
  - D=16.0 seed=101: A2 `\text{Write } -16x - 4y = -20 \text{ in slope-intercept form.}` ≠ A1 `\text{Write an equation of the line through } (-1, 1) \text{ and } (1, 5).`
  - D=16.0 seed=207: A2 `\text{Write } y + 113 = 9(x + 12) \text{ in slope-intercept form.}` ≠ A1 `\text{Write an equation of the line through } (2, 6) \text{ and } (4, 12).`
  - D=22.0 seed=101: A2 `\text{Write } -16x - 4y = -20 \text{ in slope-intercept form.}` ≠ A1 `\text{Write an equation of the line through } (-1, 1) \text{ and } (1, 5).`
  - D=22.0 seed=207: A2 `\text{Write } y + 113 = 9(x + 12) \text{ in slope-intercept form.}` ≠ A1 `\text{Write an equation of the line through } (2, 6) \text{ and } (4, 12).`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §3.1 | https://openstax.org/books/intermediate-algebra-2e/pages/3-1-use-a-general-strategy-to-solve-linear-equations | 3.1 Use a General Strategy to Solve Linear Equations — e.g. Example 2.1: Determine whether the values are solutions to the equation: $5 y + 3 = 10 y - 4 .$ ⓐ $y = \frac{3}{5}$ ⓑ $y = \frac{7}{5}$; Example 2.2: How to Solve a Linear Equation Using a General Strategy Solve: $7 (n - 3) - 8 = −15$ . |
| Intermediate Algebra 2e §3.4 | https://openstax.org/books/intermediate-algebra-2e/pages/3-4-graph-linear-equations-in-two-variables | 3.4 Graph Linear Equations in Two Variables |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

A2 type_id samples differ from A1 alias at same D/seeds — verify intended divergence.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `UNCLEAR`.

- **UNCLEAR gold:** old path and OpenStax skill intent diverge, or dump/wrong-skill shapes — do not wire a new core until notes lock.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Share A1 `writing_linear_equations` generator; wire A2 catalog id when skeleton lands.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `writing_linear_equations`; equations/WP agent owns solve/WP siblings._
