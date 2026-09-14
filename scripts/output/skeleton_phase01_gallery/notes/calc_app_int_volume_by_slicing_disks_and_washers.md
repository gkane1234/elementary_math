# Notes — `calc_app_int_volume_by_slicing_disks_and_washers`

- **Display name:** Volume by slicing, disks and washers
- **Category:** Calculus — Applications of Integration
- **Generator:** `volume_disk_washer`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `volume_disk_washer`
- **Remaining limits:** Constructive app generators with continuous-D structure knobs. Gaps: story frame banks thinner than OpenStax for related rates / growth; volumes mostly axis-of-rotation textbook templates; no interactive figures.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice volume by slicing, disks and washers.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,4]\text{ about the }x\text{-axis (disk method).}$ | $\frac{64\pi}{3}$ | — |
| 0 | 207 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,4]\text{ about the }x\text{-axis (disk method).}$ | $\frac{64\pi}{3}$ | — |
| 8 | 101 | $\text{Find the volume of the solid formed by rotating }y=x^{2}\text{ on }[0,4]\text{ about the }x\text{-axis (disk method).}$ | $\frac{1024\pi}{5}$ | — |
| 8 | 207 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,5]\text{ about the }x\text{-axis (disk method).}$ | $\frac{125\pi}{3}$ | — |
| 16 | 101 | $\text{Find the volume of the solid formed by rotating the region between }y=5\text{ and }y=x\text{ on }[0,5]\text{ about the }x\text{-axis (washer method).}$ | $\frac{250\pi}{3}$ | — |
| 16 | 207 | $\text{Find the volume of the solid formed by rotating the region between }y=2\text{ and }y=x\text{ on }[0,2]\text{ about the }x\text{-axis (washer method).}$ | $\frac{16\pi}{3}$ | — |
| 22 | 101 | $\text{Find the volume of the solid formed by rotating the region between }y=6\text{ and }y=x\text{ on }[0,6]\text{ about the }x\text{-axis (washer method).}$ | $144\pi$ | — |
| 22 | 207 | $\text{Find the volume of the solid formed by rotating the region between }y=4\text{ and }y=x\text{ on }[0,4]\text{ about the }x\text{-axis (washer method).}$ | $\frac{128\pi}{3}$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §6.2 | https://openstax.org/books/calculus-volume-1/pages/6-2-determining-volumes-by-slicing | disk/washer about axis — e.g. Example 6.6: Deriving the Formula for the Volume of a Pyramid We know from geometry that the formula for the volume of a pyramid is $V = \frac{1}{3} A h .$ If the pyramid has a square base, …; Example 6.7: Using the Slicing Method to find the Volume of a Solid of Revolution Use the slicing method to find the volume of the solid of revolution bounded by the graphs of $f (x) = x^{2}… |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep constructive integral-application builders; optional Integral skeleton for shared definite-integral cores.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `volume_disk_washer`; limits/differentiation owned by other agent._
