# Notes — `a2_matrices_inverses`

- **Display name:** Inverses
- **Category:** Algebra 2 — Matrices
- **Generator:** `matrix_inverse`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice inverses (catalog: matrix_inverse).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the inverse of } \begin{pmatrix}-1 & 1 \\ 2 & 2\end{pmatrix}.$ | $\frac{1}{-4}\begin{pmatrix}2 & -1 \\ -2 & -1\end{pmatrix}$ | — |
| 0 | 207 | $\text{Find the inverse of } \begin{pmatrix}1 & -2 \\ 2 & -1\end{pmatrix}.$ | $\frac{1}{3}\begin{pmatrix}-1 & 2 \\ -2 & 1\end{pmatrix}$ | — |
| 8 | 101 | $\text{Find the inverse of } \begin{pmatrix}-1 & -1 \\ 4 & 3\end{pmatrix}.$ | $\frac{1}{1}\begin{pmatrix}3 & 1 \\ -4 & -1\end{pmatrix}$ | — |
| 8 | 207 | $\text{Find the inverse of } \begin{pmatrix}-4 & -3 \\ 1 & 1\end{pmatrix}.$ | $\frac{1}{-1}\begin{pmatrix}1 & 3 \\ -1 & -4\end{pmatrix}$ | — |
| 16 | 101 | $\text{Find the inverse of } \begin{pmatrix}7 & -3 \\ 3 & -1\end{pmatrix}.$ | $\frac{1}{2}\begin{pmatrix}-1 & 3 \\ -3 & 7\end{pmatrix}$ | — |
| 16 | 207 | $\text{Find the inverse of } \begin{pmatrix}3 & 0 \\ -4 & 3\end{pmatrix}.$ | $\frac{1}{9}\begin{pmatrix}3 & 0 \\ 4 & 3\end{pmatrix}$ | — |
| 22 | 101 | $\text{Find the inverse of } \begin{pmatrix}7 & -3 \\ 5 & -3\end{pmatrix}.$ | $\frac{1}{-6}\begin{pmatrix}-3 & 3 \\ -5 & 7\end{pmatrix}$ | — |
| 22 | 207 | $\text{Find the inverse of } \begin{pmatrix}2 & 1 \\ -4 & 2\end{pmatrix}.$ | $\frac{1}{8}\begin{pmatrix}2 & -1 \\ 4 & 2\end{pmatrix}$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| College Algebra 2e §7.5 | https://openstax.org/books/college-algebra-2e/pages/7-5-matrices-and-matrix-operations | 7.5 Matrices and Matrix Operations |
| College Algebra 2e §7.6 | https://openstax.org/books/college-algebra-2e/pages/7-6-solving-systems-with-gaussian-elimination | 7.6 Solving Systems with Gaussian Elimination |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP leaf unless the generator is story-based. Algebra shapes follow old path samples above.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `matrix_inverse` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `matrix_inverse`; equations/WP agent owns solve/WP siblings._
