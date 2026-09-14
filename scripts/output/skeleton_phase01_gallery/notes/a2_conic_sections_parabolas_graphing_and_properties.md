# Notes — `a2_conic_sections_parabolas_graphing_and_properties`

> **UNCLEAR / NOT_IMPLEMENTED** — Conic graph/properties reuse quadratic graph engine — may not distinguish focus/directrix.

- **Display name:** Parabolas graphing & properties
- **Category:** Algebra 2 — Conic Sections
- **Generator:** `quadratic_graph_vertex`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice parabolas graphing & properties (catalog: quadratic_graph_vertex).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Graph } y = x^2 - 1$ | $\text{vertex } (0, -1)$ | — |
| 0 | 207 | $\text{Graph } y = (x - 2)^2$ | $\text{vertex } (2, 0)$ | — |
| 8 | 101 | $\text{Graph } y = 2x^{2} + 8x + 13$ | $\text{vertex } (-2, 5)$ | — |
| 8 | 207 | $\text{Graph } y = -(x - 3)^2 + 3$ | $\text{vertex } (3, 3)$ | — |
| 16 | 101 | $\text{Graph } y = -3(x - 2)^2 + 2$ | $\text{vertex } (2, 2)$ | — |
| 16 | 207 | $\text{Graph } y + 2 = 3(x + 2)^2$ | $\text{vertex } (-2, -2)$ | — |
| 22 | 101 | $\text{Graph } x^{2} - 6x + y = -14$ | $\text{vertex } (3, -5)$ | — |
| 22 | 207 | $\text{Graph } y = -3(x + 6)^2 + 7$ | $\text{vertex } (-6, 7)$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| College Algebra 2e §11.1 | https://openstax.org/books/college-algebra-2e/pages/11-1-distance-and-midpoint-formulas-circles | 11.1 Distance and Midpoint Formulas; Circles |
| College Algebra 2e §11.2 | https://openstax.org/books/college-algebra-2e/pages/11-2-parabolas | 11.2 Parabolas |
| College Algebra 2e §11.3 | https://openstax.org/books/college-algebra-2e/pages/11-3-ellipses | 11.3 Ellipses |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Conic graph/properties reuse quadratic graph engine — may not distinguish focus/directrix.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `quadratic_graph_vertex` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `quadratic_graph_vertex`; equations/WP agent owns solve/WP siblings._
