# Notes — `calc_app_int_volume_of_solids_with_known_cross_sections` (`Volume of solids with known cross sections`)

- **Display name:** Volume of solids with known cross sections
- **Category:** Calculus — Applications of Integration
- **Generator:** `volume_cross_sections`
- **Suggested family:** other (text square / equilateral / semicircle; no figure bank)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Find the volume of a solid whose cross sections are a given shape (integrate area).
- **D=0:** Square leftover of side \(x\) on \([0,n]\) with \(n\in\{2,3,4\}\) (old easy).
- **Mid D (≈8):** Square leftover still allowed, plus equilateral-triangle of side \(x\).
- **High D (≈16):** Lock out squares. Equilateral leftover plus semicircles with diameter \(x\).
- **Expert (≈22):** Semicircle only.
- **Must not:** Disk / washer / shell stems (sibling leaves); padded `difficulty_costs`; new cores (pyramid, circular-base squares, triangular-base semicircles, isosceles slices, \(a\neq 0\)).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Exclusive cliffs (`if band == easy/medium/hard`), so D=8 was equilateral only and high D never mixed leftover squares. `generator` / `form_id` unstamped. No `spec_snapshot`. 40-seed counts: D=0 all square; D=8 exclusive equilateral; D=16 semicircle only; D=22 semicircle only.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{A solid has square cross sections of side length }x\text{ for }0\le x\le 2.\text{ Find its volume.}$ | $\frac{8}{3}$ | square only |
| 0 | 0 | $\text{A solid has square cross sections of side length }x\text{ for }0\le x\le 3.\text{ Find its volume.}$ | $9$ | \(n\in\{2,3,4\}\) |
| 8 | 101 | $\text{A solid has equilateral-triangle cross sections of side }x\text{ for }0\le x\le 4.\text{ Find its volume.}$ | $\frac{64\sqrt{3}}{12}$ | exclusive equilateral, no leftover square |
| 8 | 1 | $\text{A solid has equilateral-triangle cross sections of side }x\text{ for }0\le x\le 2.\text{ Find its volume.}$ | $\frac{8\sqrt{3}}{12}$ | exclusive cliff (unreduced \(n^{3}/12\)) |
| 16 | 101 | $\text{Cross sections perpendicular to the }x\text{-axis on }[0,4]\text{ are semicircles with diameter }x.\text{ Find the volume.}$ | $\frac{8\pi}{3}$ | semicircle only |
| 16 | 1 | $\text{Cross sections perpendicular to the }x\text{-axis on }[0,2]\text{ are semicircles with diameter }x.\text{ Find the volume.}$ | $\frac{\pi}{3}$ | no leftover |
| 22 | 101 | $\text{Cross sections perpendicular to the }x\text{-axis on }[0,5]\text{ are semicircles with diameter }x.\text{ Find the volume.}$ | $\frac{125\pi}{24}$ | bound grows |
| 22 | 0 | $\text{Cross sections perpendicular to the }x\text{-axis on }[0,3]\text{ are semicircles with diameter }x.\text{ Find the volume.}$ | $\frac{9\pi}{8}$ | semicircle only |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same three builders. D=0 stays old square. Gallery seeds 101/207/313 can collide on one form at mid D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{A solid has square cross sections of side length }x\text{ for }0\le x\le 2.\text{ Find its volume.}$ | $\frac{8}{3}$ | `vcs_square` |
| 0 | 0 | $\text{A solid has square cross sections of side length }x\text{ for }0\le x\le 3.\text{ Find its volume.}$ | $9$ | old easy |
| 8 | 1 | $\text{A solid has square cross sections of side length }x\text{ for }0\le x\le 2.\text{ Find its volume.}$ | $\frac{8}{3}$ | square leftover |
| 8 | 101 | $\text{A solid has equilateral-triangle cross sections of side }x\text{ for }0\le x\le 3.\text{ Find its volume.}$ | $\frac{27\sqrt{3}}{12}$ | `vcs_equilateral` |
| 16 | 1 | $\text{A solid has equilateral-triangle cross sections of side }x\text{ for }0\le x\le 2.\text{ Find its volume.}$ | $\frac{8\sqrt{3}}{12}$ | equilateral leftover |
| 16 | 101 | $\text{Cross sections perpendicular to the }x\text{-axis on }[0,3]\text{ are semicircles with diameter }x.\text{ Find the volume.}$ | $\frac{9\pi}{8}$ | no square leftover |
| 22 | 101 | $\text{Cross sections perpendicular to the }x\text{-axis on }[0,3]\text{ are semicircles with diameter }x.\text{ Find the volume.}$ | $\frac{9\pi}{8}$ | `vcs_semicircle` only |
| 22 | 207 | $\text{Cross sections perpendicular to the }x\text{-axis on }[0,7]\text{ are semicircles with diameter }x.\text{ Find the volume.}$ | $\frac{343\pi}{24}$ | bound grows |

40-seed counts **after**: D=0 `vcs_square` only; D=8 leftover `vcs_square` + `vcs_equilateral` (19/21); D=16 leftover `vcs_equilateral` + `vcs_semicircle` (19/21, no `vcs_square`); D=22 `vcs_semicircle` only.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §6.2 Determining Volumes by Slicing | https://openstax.org/books/calculus-volume-1/pages/6-2-determining-volumes-by-slicing | Integrate \(A(x)\) of a known cross-section (Ex. 6.6 pyramid with square base is richer than old side \(x\) on \([0,n]\)) |
| OpenStax Calculus Volume 1 §6.2 Ex. 68 / 70 | https://openstax.org/books/calculus-volume-1/pages/6-2-determining-volumes-by-slicing | Base a circle / region under \(y=1-x^{2}\); slices perpendicular to the base are squares — not invented here |
| OpenStax Calculus Volume 1 §6.2 Ex. 69 | https://openstax.org/books/calculus-volume-1/pages/6-2-determining-volumes-by-slicing | Triangular base; slices perpendicular to the \(x\)-axis are semicircles — old high D is diameter \(x\) on \([0,n]\), not a triangular base |
| OpenStax Calculus Volume 1 §6.2 Ex. 72 | https://openstax.org/books/calculus-volume-1/pages/6-2-determining-volumes-by-slicing | Right isosceles triangles on the region between \(y=x^{2}\) and \(y=9\) — not on this leaf |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (6-2). Disk/washer stays on `calc_app_int_volume_by_slicing_disks_and_washers`; shells on `calc_app_int_volume_by_cylinders`.

## Variety notes

Not a WP. D=0 one easy square of side \(x\) (old). Same-D rotation at mid D: leftover square vs equilateral. High D keeps the old semicircle-diameter-\(x\) builder (do not invent pyramid / circular-base / triangular-base / isosceles). Three old forms, so D=16 mixes equilateral leftover + semicircle and D=22 is semicircle-only.

## Limitations

- **Status:** shipped — leftover lockout of exclusive cliffs / D=0 square. Remaining `LIMITATIONS`: three frozen old builders (square of side \(x\), equilateral of side \(x\), semicircle of diameter \(x\) on \([0,n]\)); no Ex. 6.6 pyramid / Ex. 68 circular-base squares / Ex. 69 triangular-base semicircles / Ex. 72 isosceles; no figure / solid SVG; D=16 can still emit equilateral leftover (intentional); equilateral answers keep the old unreduced \(n^{3}\sqrt{3}/12\).
- **Live pairwise:** each item stamps `form_id`, shared `generator=volume_cross_sections`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `volume_cross_sections`

## Proposed engine (reuse vs new)

- **Reuse:** existing square / equilateral / semicircle builders (now in `calc_app_diff.py`). Depth = real structure (lock out squares; mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** pyramid / circular-base squares / triangular-base semicircles / isosceles slices; disk / washer / shell stems; solid SVG.
