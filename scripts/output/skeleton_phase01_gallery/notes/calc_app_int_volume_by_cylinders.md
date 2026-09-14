# Notes — `calc_app_int_volume_by_cylinders`

- **Display name:** Volume by cylinders
- **Category:** Calculus — Applications of Integration
- **Generator:** `volume_shell`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `volume_shell`
- **Remaining limits:** Constructive app generators with continuous-D structure knobs. Gaps: story frame banks thinner than OpenStax for related rates / growth; volumes mostly axis-of-rotation textbook templates; no interactive figures.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice volume by cylinders.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,3]\text{ about the }y\text{-axis (shell method).}$ | $18\pi$ | — |
| 0 | 207 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,3]\text{ about the }y\text{-axis (shell method).}$ | $18\pi$ | — |
| 8 | 101 | $\text{Find the volume of the solid formed by rotating }y=x^{2}\text{ on }[0,4]\text{ about the }y\text{-axis (shell method).}$ | $128\pi$ | — |
| 8 | 207 | $\text{Find the volume of the solid formed by rotating }y=x^{2}\text{ on }[0,5]\text{ about the }y\text{-axis (shell method).}$ | $\frac{625\pi}{2}$ | — |
| 16 | 101 | $\text{Find the volume of the solid formed by rotating }y=4-x\text{ on }[0,4]\text{ about the }y\text{-axis (shell method).}$ | $\frac{64\pi}{3}$ | — |
| 16 | 207 | $\text{Find the volume of the solid formed by rotating }y=3-x\text{ on }[0,3]\text{ about the }y\text{-axis (shell method).}$ | $9\pi$ | — |
| 22 | 101 | $\text{Find the volume of the solid formed by rotating }y=7-x\text{ on }[0,7]\text{ about the }y\text{-axis (shell method).}$ | $\frac{343\pi}{3}$ | — |
| 22 | 207 | $\text{Find the volume of the solid formed by rotating }y=3-x\text{ on }[0,3]\text{ about the }y\text{-axis (shell method).}$ | $9\pi$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §6.3 | https://openstax.org/books/calculus-volume-1/pages/6-3-volumes-of-revolution-cylindrical-shells | shell method 2π∫ x f(x) dx — e.g. Example 6.12: The Method of Cylindrical Shells 1 Define $R$ as the region bounded above by the graph of $f (x) = 1 / x$ and below by the $x -\text{axis}$ over the interval $\left[\right. 1 , …; Example 6.13: The Method of Cylindrical Shells 2 Define R as the region bounded above by the graph of $f (x) = 2 x - x^{2}$ and below by the $x -\text{axis}$ over the interval $\left[\right. … |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep constructive integral-application builders; optional Integral skeleton for shared definite-integral cores.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `volume_shell`; limits/differentiation owned by other agent._
