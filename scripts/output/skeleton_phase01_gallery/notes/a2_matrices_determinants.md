# Notes — `a2_matrices_determinants`

- **Display name:** Determinants
- **Category:** Algebra 2 — Matrices
- **Generator:** `matrix_operations`
- **Already on skeleton?** no
- **Suggested family:** `number`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice determinants (catalog: matrix_operations).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\begin{pmatrix}3 & -1 \\ 1 & -2\end{pmatrix} + \begin{pmatrix}-2 & -2 \\ 0 & -3\end{pmatrix}$ | $\begin{pmatrix}1 & -3 \\ 1 & -5\end{pmatrix}$ | — |
| 0 | 207 | $\begin{pmatrix}2 & -3 \\ -1 & -2\end{pmatrix} + \begin{pmatrix}-1 & 0 \\ -3 & 1\end{pmatrix}$ | $\begin{pmatrix}1 & -3 \\ -4 & -1\end{pmatrix}$ | — |
| 8 | 101 | $\begin{pmatrix}5 & -1 \\ 3 & -3\end{pmatrix} + \begin{pmatrix}-3 & 0 \\ 4 & 5\end{pmatrix}$ | $\begin{pmatrix}2 & -1 \\ 7 & 2\end{pmatrix}$ | — |
| 8 | 207 | $\begin{pmatrix}0 & 3 \\ 5 & 2\end{pmatrix} + \begin{pmatrix}4 & -4 \\ 2 & -1\end{pmatrix}$ | $\begin{pmatrix}4 & -1 \\ 7 & 1\end{pmatrix}$ | — |
| 16 | 101 | $6 \cdot \begin{pmatrix}-6 & 7 \\ -2 & 1\end{pmatrix}$ | $\begin{pmatrix}-36 & 42 \\ -12 & 6\end{pmatrix}$ | — |
| 16 | 207 | $-7 \cdot \begin{pmatrix}-3 & 5 \\ -1 & -4\end{pmatrix}$ | $\begin{pmatrix}21 & -35 \\ 7 & 28\end{pmatrix}$ | — |
| 22 | 101 | $\begin{pmatrix}-8 & -7 \\ 2 & 7\end{pmatrix} + \begin{pmatrix}3 & -8 \\ -1 & -5\end{pmatrix}$ | $\begin{pmatrix}-5 & -15 \\ 1 & 2\end{pmatrix}$ | — |
| 22 | 207 | $\begin{pmatrix}1 & -5 \\ -6 & -2\end{pmatrix} + \begin{pmatrix}-5 & -8 \\ -3 & -7\end{pmatrix}$ | $\begin{pmatrix}-4 & -13 \\ -9 & -9\end{pmatrix}$ | — |

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

- **Reuse:** Existing `matrix_operations` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `matrix_operations`; equations/WP agent owns solve/WP siblings._
