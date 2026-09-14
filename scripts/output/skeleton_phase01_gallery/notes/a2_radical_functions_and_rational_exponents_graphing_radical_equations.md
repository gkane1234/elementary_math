# Notes — `a2_radical_functions_and_rational_exponents_graphing_radical_equations`

> **UNCLEAR / NOT_IMPLEMENTED** — Graph radical functions — verify domain/range vs graph prompt.

- **Display name:** Graphing radical equations
- **Category:** Algebra 2 — Radical Functions and Rational Exponents
- **Generator:** `graph_radical`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice graphing radical equations (catalog: graph_radical).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $y = \sqrt{x + 2}$ | $y = \sqrt{x + 2}$ | figure |
| 0 | 207 | $y = \sqrt{x - 5}$ | $y = \sqrt{x - 5}$ | figure |
| 8 | 101 | $y = \sqrt{x} + 3$ | $y = \sqrt{x} + 3$ | figure |
| 8 | 207 | $y = \sqrt{x} - 3$ | $y = \sqrt{x} - 3$ | figure |
| 16 | 101 | $y = -\sqrt{x} + 3$ | $y = -\sqrt{x} + 3$ | figure |
| 16 | 207 | $y = -\sqrt{x} + 3$ | $y = -\sqrt{x} + 3$ | figure |
| 22 | 101 | $y = -\sqrt{x} + 3$ | $y = -\sqrt{x} + 3$ | figure |
| 22 | 207 | $y = -\sqrt{x} + 3$ | $y = -\sqrt{x} + 3$ | figure |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §8.1 | https://openstax.org/books/intermediate-algebra-2e/pages/8-1-simplify-expressions-with-roots | 8.1 Simplify Expressions with Roots — e.g. Example 8.1: Simplify: ⓐ $\sqrt{144}$ ⓑ $− \sqrt{289} .$; Example 8.2: Simplify: ⓐ $\sqrt{−196}$ ⓑ $− \sqrt{64} .$ |
| Intermediate Algebra 2e §8.2 | https://openstax.org/books/intermediate-algebra-2e/pages/8-2-simplify-radical-expressions | 8.2 Simplify Radical Expressions — e.g. Example 8.13: Simplify Square Roots Using the Product Property of Roots Simplify: $\sqrt{98} .$; Example 8.14: Simplify: ⓐ $\sqrt{500}$ ⓑ $\sqrt[3]{16}$ ⓒ $\sqrt[4]{243} .$ |
| Intermediate Algebra 2e §8.3 | https://openstax.org/books/intermediate-algebra-2e/pages/8-3-simplify-rational-exponents | 8.3 Simplify Rational Exponents — e.g. Example 8.26: Write as a radical expression: ⓐ $x^{\frac{1}{2}}$ ⓑ $y^{\frac{1}{3}}$ ⓒ $z^{\frac{1}{4}} .$; Example 8.27: Write with a rational exponent: ⓐ $\sqrt{5 y}$ ⓑ $\sqrt[3]{4 x}$ ⓒ $3 \sqrt[4]{5 z} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Graph radical functions — verify domain/range vs graph prompt.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).
- **Diagram:** figure/stimulus may be named in answers — verify SVG/stimulus actually renders on worksheets.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `graph_radical` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `graph_radical`; equations/WP agent owns solve/WP siblings._
