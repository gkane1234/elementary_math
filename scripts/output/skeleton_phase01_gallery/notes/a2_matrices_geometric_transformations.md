# Notes — `a2_matrices_geometric_transformations`

> **UNCLEAR** — Matrix transformation UX (apply 2×2 to polygon) — verify diagram fidelity.

- **Display name:** Geometric transformations
- **Category:** Algebra 2 — Matrices
- **Generator:** `matrix_transformation`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice geometric transformations (catalog: matrix_transformation).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Apply reflection across the x-axis to } (-4, 2) \text{ using } \begin{pmatrix}1 & 0 \\ 0 & -1\end{pmatrix}.$ | $(-4, -2)$ | — |
| 0 | 207 | $\text{Apply a 180^\circ rotation to } (-2, 3) \text{ using } \begin{pmatrix}-1 & 0 \\ 0 & -1\end{pmatrix}.$ | $(2, -3)$ | — |
| 8 | 101 | $\text{Apply a 180^\circ rotation to } (-2, -2) \text{ using } \begin{pmatrix}-1 & 0 \\ 0 & -1\end{pmatrix}.$ | $(2, 2)$ | — |
| 8 | 207 | $\text{Apply reflection across the y-axis to } (1, 5) \text{ using } \begin{pmatrix}-1 & 0 \\ 0 & 1\end{pmatrix}.$ | $(-1, 5)$ | — |
| 16 | 101 | $\text{Apply a 180^\circ rotation to } (-4, 8) \text{ using } \begin{pmatrix}-1 & 0 \\ 0 & -1\end{pmatrix}.$ | $(4, -8)$ | — |
| 16 | 207 | $\text{Apply reflection across the x-axis to } (-1, 1) \text{ using } \begin{pmatrix}1 & 0 \\ 0 & -1\end{pmatrix}.$ | $(-1, -1)$ | — |
| 22 | 101 | $\text{Apply a 90^\circ counterclockwise rotation to } (-6, -9) \text{ using } \begin{pmatrix}0 & -1 \\ 1 & 0\end{pmatrix}.$ | $(9, -6)$ | — |
| 22 | 207 | $\text{Apply a 90^\circ counterclockwise rotation to } (-9, 6) \text{ using } \begin{pmatrix}0 & -1 \\ 1 & 0\end{pmatrix}.$ | $(-6, -9)$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| College Algebra 2e §7.5 | https://openstax.org/books/college-algebra-2e/pages/7-5-matrices-and-matrix-operations | 7.5 Matrices and Matrix Operations |
| College Algebra 2e §7.6 | https://openstax.org/books/college-algebra-2e/pages/7-6-solving-systems-with-gaussian-elimination | 7.6 Solving Systems with Gaussian Elimination |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Matrix transformation UX (apply 2×2 to polygon) — verify diagram fidelity.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `UNCLEAR`.

- **UNCLEAR gold:** old path and OpenStax skill intent diverge, or dump/wrong-skill shapes — do not wire a new core until notes lock.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `matrix_transformation` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `matrix_transformation`; equations/WP agent owns solve/WP siblings._
