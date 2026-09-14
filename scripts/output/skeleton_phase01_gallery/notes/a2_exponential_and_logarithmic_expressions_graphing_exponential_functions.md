# Notes — `a2_exponential_and_logarithmic_expressions_graphing_exponential_functions`

> **UNCLEAR / LOW_VARIETY / NOT_IMPLEMENTED** — Graph exponential — transformations/base not locked to OpenStax §10.2.

- **Display name:** Graphing exponential functions
- **Category:** Algebra 2 — Exponential and Logarithmic Expressions
- **Generator:** `graph_exponential`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice graphing exponential functions (catalog: graph_exponential).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $y = 2^{x}$ | $y = 2^{x}$ | figure |
| 0 | 207 | $y = 2^{x}$ | $y = 2^{x}$ | figure |
| 8 | 101 | $y = 3 \cdot \left(\frac{1}{4}\right)^{x} + 3$ | $y = 3 \cdot \left(\frac{1}{4}\right)^{x} + 3$ | figure |
| 8 | 207 | $y = 3 \cdot \left(\frac{1}{4}\right)^{x - 1} + 1$ | $y = 3 \cdot \left(\frac{1}{4}\right)^{x - 1} + 1$ | figure |
| 16 | 101 | $y = -3^{x + 1} - 1$ | $y = -3^{x + 1} - 1$ | figure |
| 16 | 207 | $y = -3 \cdot \left(\frac{1}{3}\right)^{x - 1} + 1$ | $y = -3 \cdot \left(\frac{1}{3}\right)^{x - 1} + 1$ | figure |
| 22 | 101 | $y = -3^{x + 1} - 1$ | $y = -3^{x + 1} - 1$ | figure |
| 22 | 207 | $y = -3 \cdot \left(\frac{1}{3}\right)^{x - 1} + 1$ | $y = -3 \cdot \left(\frac{1}{3}\right)^{x - 1} + 1$ | figure |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `graph_exponential` (same generator `graph_exponential` unless noted).
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §10.2 | https://openstax.org/books/intermediate-algebra-2e/pages/10-2-evaluate-and-graph-exponential-functions | 10.2 Evaluate and Graph Exponential Functions — e.g. Example 10.10: On the same coordinate system graph $f (x) = 2^{x}$ and $g (x) = 3^{x} .$; Example 10.11: On the same coordinate system, graph $f (x) = \left(\right. \frac{1}{2} \left.\right)^{x}$ and $g (x) = \left(\right. \frac{1}{3} \left.\right)^{x} .$ |
| Intermediate Algebra 2e §10.3 | https://openstax.org/books/intermediate-algebra-2e/pages/10-3-evaluate-and-graph-logarithmic-functions | 10.3 Evaluate and Graph Logarithmic Functions — e.g. Example 10.18: Convert to logarithmic form: ⓐ $2^{3} = 8 ,$ ⓑ $5^{\frac{1}{2}} = \sqrt{5} ,$ and ⓒ $\left(\right. \frac{1}{2} \left.\right)^{4} = \frac{1}{16} .$; Example 10.19: Convert to exponential form: ⓐ $2 = \log_{8} 64 ,$ ⓑ $0 = \log_{4} 1 ,$ and ⓒ $- 3 = \log_{10} \frac{1}{1000} .$ |
| Intermediate Algebra 2e §10.4 | https://openstax.org/books/intermediate-algebra-2e/pages/10-4-use-the-properties-of-logarithms | 10.4 Use the Properties of Logarithms — e.g. Example 10.28: Evaluate using the properties of logarithms: ⓐ $\log_{8} 1$ and ⓑ $\log_{6} 6 .$; Example 10.29: Evaluate using the properties of logarithms: ⓐ $4^{\log_{4} 9}$ and ⓑ $\log_{3} 3^{5} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Graph exponential — transformations/base not locked to OpenStax §10.2.
Flags: `UNCLEAR`, `LOW_VARIETY`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`, `LOW_VARIETY`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Variety:** one template / Mad-Lib across seeds at easy D — rotate OpenStax-derived frames or algebraic shapes before claiming shipped variety.
- **Difficulty scaling:** Variety thin at fixed D; D may still bump coeffs — check live ladder.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).
- **Diagram:** figure/stimulus may be named in answers — verify SVG/stimulus actually renders on worksheets.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Share A1 `graph_exponential` generator; wire A2 catalog id when skeleton lands.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `graph_exponential`; equations/WP agent owns solve/WP siblings._
