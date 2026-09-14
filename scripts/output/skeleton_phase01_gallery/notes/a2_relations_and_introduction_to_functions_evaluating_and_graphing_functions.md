# Notes — `a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions`

> **UNCLEAR / NOT_IMPLEMENTED** — see Limitations.


- **Display name:** Evaluating and graphing functions
- **Category:** Algebra 2 — Relations and Introduction to Functions
- **Generator:** `evaluating_graphing_functions`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice evaluating and graphing functions (catalog: evaluating_graphing_functions).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Given } f(x) = 3x - 2, \text{ find } f(3).$ | $7$ | figure |
| 0 | 207 | $\text{Given } f(x) = 2x - 1, \text{ find } f(-3).$ | $-7$ | figure |
| 8 | 101 | $\text{Given } f(x) = 3x - 2, \text{ find } f(3).$ | $7$ | figure |
| 8 | 207 | $\text{Given } f(x) = 2x - 1, \text{ find } f(-3).$ | $-7$ | figure |
| 16 | 101 | $\text{Given } f(x) = 3x - 2, \text{ find } f(3).$ | $7$ | figure |
| 16 | 207 | $\text{Given } f(x) = 2x - 1, \text{ find } f(-3).$ | $-7$ | figure |
| 22 | 101 | $\text{Given } f(x) = 3x - 2, \text{ find } f(3).$ | $7$ | figure |
| 22 | 207 | $\text{Given } f(x) = 2x - 1, \text{ find } f(-3).$ | $-7$ | figure |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `evaluating_graphing_functions` (same generator `evaluating_graphing_functions` unless noted).
- **Old path vs A1:** Identical prompts at all sampled D/seeds (shared generator).

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §3.5 | https://openstax.org/books/intermediate-algebra-2e/pages/3-5-graphs-of-functions | 3.5 Graphs of Functions |
| Intermediate Algebra 2e §3.6 | https://openstax.org/books/intermediate-algebra-2e/pages/3-6-graphs-of-functions | 3.6 Graphs of Functions |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP leaf unless the generator is story-based. Algebra shapes follow old path samples above.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D-scaling may be flat — D=0 and D=16 prompts look identical in notes samples.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).
- **Diagram:** figure/stimulus may be named in answers — verify SVG/stimulus actually renders on worksheets.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Share A1 `evaluating_graphing_functions` generator; wire A2 catalog id when skeleton lands.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `evaluating_graphing_functions`; equations/WP agent owns solve/WP siblings._
