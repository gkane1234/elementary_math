# Notes — `calc_app_int_volume_of_solids_with_known_cross_sections`

- **Display name:** Volume of solids with known cross sections
- **Category:** Calculus — Applications of Integration
- **Generator:** `volume_cross_sections`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `volume_cross_sections`
- **Remaining limits:** Constructive app generators with continuous-D structure knobs. Gaps: story frame banks thinner than OpenStax for related rates / growth; volumes mostly axis-of-rotation textbook templates; no interactive figures.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice volume of solids with known cross sections.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{A solid has square cross sections of side length }x\text{ for }0\le x\le 2.\text{ Find its volume.}$ | $\frac{8}{3}$ | — |
| 0 | 207 | $\text{A solid has square cross sections of side length }x\text{ for }0\le x\le 4.\text{ Find its volume.}$ | $\frac{64}{3}$ | — |
| 8 | 101 | $\text{A solid has equilateral-triangle cross sections of side }x\text{ for }0\le x\le 4.\text{ Find its volume.}$ | $\frac{64\sqrt{3}}{12}$ | — |
| 8 | 207 | $\text{A solid has equilateral-triangle cross sections of side }x\text{ for }0\le x\le 4.\text{ Find its volume.}$ | $\frac{64\sqrt{3}}{12}$ | — |
| 16 | 101 | $\text{Cross sections perpendicular to the }x\text{-axis on }[0,4]\text{ are semicircles with diameter }x.\text{ Find the volume.}$ | $\frac{8\pi}{3}$ | — |
| 16 | 207 | $\text{Cross sections perpendicular to the }x\text{-axis on }[0,5]\text{ are semicircles with diameter }x.\text{ Find the volume.}$ | $\frac{125\pi}{24}$ | — |
| 22 | 101 | $\text{Cross sections perpendicular to the }x\text{-axis on }[0,3]\text{ are semicircles with diameter }x.\text{ Find the volume.}$ | $\frac{9\pi}{8}$ | — |
| 22 | 207 | $\text{Cross sections perpendicular to the }x\text{-axis on }[0,3]\text{ are semicircles with diameter }x.\text{ Find the volume.}$ | $\frac{9\pi}{8}$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §6.2 | https://openstax.org/books/calculus-volume-1/pages/6-2-determining-volumes-by-slicing | known cross-section (square/semi/equil) — e.g. Example 6.6: Deriving the Formula for the Volume of a Pyramid We know from geometry that the formula for the volume of a pyramid is $V = \frac{1}{3} A h .$ If the pyramid has a square base, …; Example 6.7: Using the Slicing Method to find the Volume of a Solid of Revolution Use the slicing method to find the volume of the solid of revolution bounded by the graphs of $f (x) = x^{2}… |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep constructive integral-application builders; optional Integral skeleton for shared definite-integral cores.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `volume_cross_sections`; limits/differentiation owned by other agent._
