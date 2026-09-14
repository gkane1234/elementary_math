# Notes — `a2_rational_expressions_graphing`

> **UNCLEAR / NOT_IMPLEMENTED** — Rational function graphing (asymptotes/holes) — no skeleton core yet.

- **Display name:** Graphing rational functions
- **Category:** Algebra 2 — Rational Expressions
- **Generator:** `graph_rational`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice graphing rational functions (catalog: graph_rational).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $y = \frac{1}{x + 2}$ | $y = \frac{1}{x + 2}$ | figure |
| 0 | 207 | $y = \frac{1}{x - 5}$ | $y = \frac{1}{x - 5}$ | figure |
| 8 | 101 | $y = \frac{3}{x}$ | $y = \frac{3}{x}$ | figure |
| 8 | 207 | $y = \frac{3}{x} - 2$ | $y = \frac{3}{x} - 2$ | figure |
| 16 | 101 | $y = \frac{2}{x}$ | $y = \frac{2}{x}$ | figure |
| 16 | 207 | $y = \frac{2}{x} - 1$ | $y = \frac{2}{x} - 1$ | figure |
| 22 | 101 | $y = \frac{2}{x}$ | $y = \frac{2}{x}$ | figure |
| 22 | 207 | $y = \frac{2}{x} - 1$ | $y = \frac{2}{x} - 1$ | figure |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §7.1 | https://openstax.org/books/intermediate-algebra-2e/pages/7-1-multiply-and-divide-rational-expressions | 7.1 Multiply and Divide Rational Expressions — e.g. Example 7.1: Determine the value for which each rational expression is undefined: ⓐ $\frac{8 a^{2} b}{3 c}$ ⓑ $\frac{4 b - 3}{2 b + 5}$ ⓒ $\frac{x + 4}{x^{2} + 5 x + 6} .$; Example 7.2: How to Simplify a Rational Expression Simplify: $\frac{x^{2} + 5 x + 6}{x^{2} + 8 x + 12}$ . |
| Intermediate Algebra 2e §7.2 | https://openstax.org/books/intermediate-algebra-2e/pages/7-2-add-and-subtract-rational-expressions | 7.2 Add and Subtract Rational Expressions — e.g. Example 7.13: Add: $\frac{11 x + 28}{x + 4} + \frac{x^{2}}{x + 4} .$; Example 7.14: Subtract: $\frac{5 x^{2} - 7 x + 3}{x^{2} - 3 x - 18} - \frac{4 x^{2} + x - 9}{x^{2} - 3 x - 18} .$ |
| Intermediate Algebra 2e §7.3 | https://openstax.org/books/intermediate-algebra-2e/pages/7-3-simplify-complex-rational-expressions | 7.3 Simplify Complex Rational Expressions — e.g. Example 7.24: Simplify the complex rational expression by writing it as division: $\frac{\frac{6}{x - 4}}{\frac{3}{x^{2} - 16}} .$; Example 7.25: Simplify the complex rational expression by writing it as division: $\frac{\frac{1}{3} + \frac{1}{6}}{\frac{1}{2} - \frac{1}{3}} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Rational function graphing (asymptotes/holes) — no skeleton core yet.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).
- **Diagram:** figure/stimulus may be named in answers — verify SVG/stimulus actually renders on worksheets.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `graph_rational` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `graph_rational`; equations/WP agent owns solve/WP siblings._
