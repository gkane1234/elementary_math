# Notes — `a2_linear_relations_and_functions_graphing_linear_equations`

> **LOW_VARIETY / UNCLEAR / NOT_IMPLEMENTED** — One template across seeds at D=0.

- **Display name:** Graphing linear equations
- **Category:** Algebra 2 — Linear Relations and Functions
- **Generator:** `graph_linear_equation`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice graphing linear equations (catalog: graph_linear_equation).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Graph: } y = 2x$ | $y = 2x$ | pattern=GraphLinear, figure |
| 0 | 207 | $\text{Graph: } y = 3x$ | $y = 3x$ | pattern=GraphLinear, figure |
| 8 | 101 | $\text{Graph: } y = -2x$ | $y = -2x$ | pattern=GraphLinear, figure |
| 8 | 207 | $\text{Graph: } y = -x$ | $y = -x$ | pattern=GraphLinear, figure |
| 16 | 101 | $\text{Graph: } y = -2x + 3$ | $y = -2x + 3$ | pattern=GraphLinear, figure |
| 16 | 207 | $\text{Graph: } y = -x - 5$ | $y = -x - 5$ | pattern=GraphLinear, figure |
| 22 | 101 | $\text{Graph: } y = 2$ | $y = 2$ | pattern=GraphLinear, figure |
| 22 | 207 | $\text{Graph: } y = -x - 4$ | $y = -x - 4$ | pattern=GraphLinear, figure |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `graph_linear_equation` (same generator `graph_linear_equation` unless noted).
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §3.1 | https://openstax.org/books/intermediate-algebra-2e/pages/3-1-use-a-general-strategy-to-solve-linear-equations | 3.1 Use a General Strategy to Solve Linear Equations — e.g. Example 2.1: Determine whether the values are solutions to the equation: $5 y + 3 = 10 y - 4 .$ ⓐ $y = \frac{3}{5}$ ⓑ $y = \frac{7}{5}$; Example 2.2: How to Solve a Linear Equation Using a General Strategy Solve: $7 (n - 3) - 8 = −15$ . |
| Intermediate Algebra 2e §3.4 | https://openstax.org/books/intermediate-algebra-2e/pages/3-4-graph-linear-equations-in-two-variables | 3.4 Graph Linear Equations in Two Variables |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

One template across seeds at D=0.
Flags: `LOW_VARIETY`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`, `LOW_VARIETY`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Variety:** one template / Mad-Lib across seeds at easy D — rotate OpenStax-derived frames or algebraic shapes before claiming shipped variety.
- **Difficulty scaling:** Variety thin at fixed D; D may still bump coeffs — check live ladder.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).
- **Diagram:** figure/stimulus may be named in answers — verify SVG/stimulus actually renders on worksheets.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Share A1 `graph_linear_equation` generator; wire A2 catalog id when skeleton lands.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `graph_linear_equation`; equations/WP agent owns solve/WP siblings._
