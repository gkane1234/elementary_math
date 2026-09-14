# Notes — `a2_systems_of_equations_and_inequalities_points_in_three_dimensions`

> **UNCLEAR / NOT_IMPLEMENTED** — 3D point identification — supplemental; sparse OpenStax IA coverage.

- **Display name:** Points in three dimensions
- **Category:** Algebra 2 — Systems of Equations and Inequalities
- **Generator:** `points_three_dimensions`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice points in three dimensions (catalog: points_three_dimensions).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{State the coordinates of point } P \text{ in three dimensions: } P=(1, 2, 2).$ | $(1, 2, 2)$ | — |
| 0 | 207 | $\text{State the coordinates of point } P \text{ in three dimensions: } P=(1, 3, -2).$ | $(1, 3, -2)$ | — |
| 8 | 101 | $\text{State the coordinates of point } P \text{ in three dimensions: } P=(-3, -5, 5).$ | $(-3, -5, 5)$ | — |
| 8 | 207 | $\text{State the coordinates of point } P \text{ in three dimensions: } P=(0, -3, 2).$ | $(0, -3, 2)$ | — |
| 16 | 101 | $\text{State the coordinates of point } P \text{ in three dimensions: } P=(-5, -6, -1).$ | $(-5, -6, -1)$ | — |
| 16 | 207 | $\text{State the coordinates of point } P \text{ in three dimensions: } P=(-1, -4, -4).$ | $(-1, -4, -4)$ | — |
| 22 | 101 | $\text{State the coordinates of point } P \text{ in three dimensions: } P=(-6, 2, 6).$ | $(-6, 2, 6)$ | — |
| 22 | 207 | $\text{State the coordinates of point } P \text{ in three dimensions: } P=(-2, 4, 4).$ | $(-2, 4, 4)$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §4.1 | https://openstax.org/books/intermediate-algebra-2e/pages/4-1-use-the-rectangular-coordinate-system | 4.1 Use the Rectangular Coordinate System |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

3D point identification — supplemental; sparse OpenStax IA coverage.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `points_three_dimensions` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `points_three_dimensions`; equations/WP agent owns solve/WP siblings._
