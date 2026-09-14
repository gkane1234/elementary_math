# Notes — `a2_systems_of_equations_and_inequalities_planes`

> **UNCLEAR / NOT_IMPLEMENTED** — Plane identification in 3D — supplemental skill.

- **Display name:** Planes
- **Category:** Algebra 2 — Systems of Equations and Inequalities
- **Generator:** `planes`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice planes (catalog: planes).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Does } (-2, 3, -3) \text{ lie on the plane } 3x - 2y + z=-15\text{?}$ | $\text{Yes}$ | — |
| 0 | 207 | $\text{Does } (3, -2, 2) \text{ lie on the plane } -x - 3y + z=5\text{?}$ | $\text{Yes}$ | — |
| 8 | 101 | $\text{Does } (2, 5, -3) \text{ lie on the plane } -4x + 5y - z=20\text{?}$ | $\text{Yes}$ | — |
| 8 | 207 | $\text{Does } (0, 4, 2) \text{ lie on the plane } x - y - 5z=-14\text{?}$ | $\text{Yes}$ | — |
| 16 | 101 | $\text{Does } (-1, 5, -1) \text{ lie on the plane } -x + 4y - z=22\text{?}$ | $\text{Yes}$ | — |
| 16 | 207 | $\text{Does } (6, 5, -3) \text{ lie on the plane } 6x - y + 5z=16\text{?}$ | $\text{Yes}$ | — |
| 22 | 101 | $\text{Does } (8, 1, 8) \text{ lie on the plane } -x - y + 8z=55\text{?}$ | $\text{Yes}$ | — |
| 22 | 207 | $\text{Does } (8, 7, -2) \text{ lie on the plane } 8x + 2y + 2z=74\text{?}$ | $\text{Yes}$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §4.1 | https://openstax.org/books/intermediate-algebra-2e/pages/4-1-use-the-rectangular-coordinate-system | 4.1 Use the Rectangular Coordinate System |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Plane identification in 3D — supplemental skill.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `planes` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `planes`; equations/WP agent owns solve/WP siblings._
