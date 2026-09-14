# Notes — `a2_trigonometry_graphing_trig_functions`

> **UNCLEAR / NOT_IMPLEMENTED** — Trig graph transforms — College Algebra §7.6; old amplitude/period shapes TBD.

- **Display name:** Graphing trig functions
- **Category:** Algebra 2 — Trigonometry
- **Generator:** `graphing_trig_functions`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice graphing trig functions (catalog: graphing_trig_functions).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Graph } y=\sin x\text{ over one period.}$ | $\text{amplitude }1,\ \text{period }2\pi,\ \text{midline }y=0$ | — |
| 0 | 207 | $\text{Graph } y=\cos x\text{ over one period.}$ | $\text{amplitude }1,\ \text{period }2\pi,\ \text{midline }y=0$ | — |
| 8 | 101 | $\text{Graph } y=3\cos x\text{ over one period.}$ | $\text{amplitude }3,\ \text{period }2\pi,\ \text{midline }y=0$ | — |
| 8 | 207 | $\text{Graph } y=-3\sin x\text{ over one period.}$ | $\text{amplitude }3,\ \text{period }2\pi,\ \text{midline }y=0,\ \text{reflection over the x-axis}$ | — |
| 16 | 101 | $\text{Graph } y=2\cos\left(2x\right)\text{ over one period.}$ | $\text{amplitude }2,\ \text{period }\pi,\ \text{midline }y=0$ | — |
| 16 | 207 | $\text{Graph } y=2\cos\left(2x-\pi\right)\text{ over one period.}$ | $\text{amplitude }2,\ \text{period }\pi,\ \text{midline }y=0$ | — |
| 22 | 101 | $\text{Graph } y=3\cos\left(2x-\pi\right)\text{ over one period.}$ | $\text{amplitude }3,\ \text{period }\pi,\ \text{midline }y=0$ | — |
| 22 | 207 | $\text{Graph } y=4\sin\left(2x-\pi\right)\text{ over one period.}$ | $\text{amplitude }4,\ \text{period }\pi,\ \text{midline }y=0$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| College Algebra 2e §5.1 | https://openstax.org/books/college-algebra-2e/pages/5-1-angles | 5.1 Angles |
| College Algebra 2e §7.1 | https://openstax.org/books/college-algebra-2e/pages/7-1-right-triangle-trigonometry | 7.1 Right Triangle Trigonometry |
| College Algebra 2e §7.2 | https://openstax.org/books/college-algebra-2e/pages/7-2-non-right-triangles-law-of-sines | 7.2 Non-right Triangles: Law of Sines |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Trig graph transforms — College Algebra §7.6; old amplitude/period shapes TBD.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `graphing_trig_functions` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `graphing_trig_functions`; equations/WP agent owns solve/WP siblings._
