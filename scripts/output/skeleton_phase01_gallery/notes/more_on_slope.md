# `more_on_slope` — More on slope

- **Course:** Algebra 1
- **Category:** Algebra 1 — Linear Equations and Inequalities
- **Generator:** `more_on_slope`
- **Already on skeleton?** yes (`MoreOnSlope`)
- **Old-path extra settings:** none (old slope-from-points clone is gone; live is parallel/perp).

## What the question should look like (D=0 vs high D)

- **Skill:** Parallel / perpendicular slopes (OpenStax EA §4.6), not “find m from two points.”
- **D=0:** Obvious parallel — same integer `m`, or “what is the slope of a line parallel to it?”
- **High D (≈16–22):** Perpendicular negative-reciprocal; then write a parallel/perp line through a point.
- **Must not:** Duplicate the `slope` leaf (two points / read `m` from `y=mx+b`).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` **before** this wiring (seeds 101 and 207). Same skill as `slope`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | Find the slope of the line through $(1, 0)$ and $(3, 4)$. | $2$ | two points |
| 0 | 207 | Find the slope of the line through $(3, -3)$ and $(4, -1)$. | $2$ | two points |
| 8 | 101 | Find the slope of the line $y = -\frac{1}{2}x + 1$. | $-\frac{1}{2}$ | from equation |
| 16 | 101 | Find the slope of the line $y = -\frac{2}{3}x - 1$. | $-\frac{2}{3}$ | from equation |

Opt-out flag used: none (old live default).

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §4.6 | https://openstax.org/books/elementary-algebra-2e/pages/4-6-find-the-equation-of-a-line | Parallel slopes equal; perpendicular $-1/m$; write a line parallel/perp to a given line through a point |

## Variety notes

Live default is parallel/perp. D=0 stays obvious parallel. Perp and write-through-a-point unlock with format tier.

## Limitations

- LIMITATIONS: historically duplicated `slope` (two-points / from equation); live now is parallel/perp only (EA §4.6).
- Keep separate from `slope` — do not reintroduce find-m-from-points here.
- D climbs parallel → perpendicular → write line through a point; verify gallery ladder stays distinct from `pa_slope`.

## Proposed engine (reuse vs new)

**Shipped:** `sample_more_on_slope` on the linear-forms core. Not `sample_slope`.
