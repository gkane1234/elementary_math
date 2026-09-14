# Notes — `calc_app_int_volume_by_slicing_disks_and_washers` (`Volume by slicing, disks and washers`)

- **Display name:** Volume by slicing, disks and washers
- **Category:** Calculus — Applications of Integration
- **Generator:** `volume_disk_washer`
- **Suggested family:** other (text rotate-about-\(x\)-axis; no figure bank)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Find the volume of a solid of revolution by disks or washers about the \(x\)-axis.
- **D=0:** Disk leftover \(y=x\) on \([0,n]\) with \(n\in\{2,3,4\}\) (old easy).
- **Mid D (≈8):** \(y=x\) leftover still allowed, plus disk \(y=x^{2}\).
- **High D (≈16–22):** Lock out disk \(y=x\) (and disk \(y=x^{2}\)). Washer between \(y=n\) and \(y=x\) on \([0,n]\) only — this is what `volume_methods` already did, not an 8/16/20 leftover-mix.
- **Must not:** Shell / known-cross-section stems (sibling leaves); padded `difficulty_costs`; new cores (\(\sqrt{x}\), \(1/x\), \(y\)-axis, rotate about \(y=k\)).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before pairwise stamps. `volume_methods` already dropped `disk_linear` at \(d\ge 10\) and `disk_quadratic` at \(d\ge 16\); `shell` / `cross_semi` aliases all emitted the washer builder. `generator` / `form_id` unstamped. No `spec_snapshot`. 40-seed counts: D=0 all disk \(y=x\); D=8 leftover linear + \(x^{2}\) (20/20); D=16 washer only; D=22 washer only.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,2]\text{ about the }x\text{-axis (disk method).}$ | $\frac{8\pi}{3}$ | disk \(y=x\) only |
| 0 | 0 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,4]\text{ about the }x\text{-axis (disk method).}$ | $\frac{64\pi}{3}$ | \(n\in\{2,3,4\}\) |
| 8 | 101 | $\text{Find the volume of the solid formed by rotating }y=x^{2}\text{ on }[0,4]\text{ about the }x\text{-axis (disk method).}$ | $\frac{1024\pi}{5}$ | disk \(x^{2}\) |
| 8 | 207 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,2]\text{ about the }x\text{-axis (disk method).}$ | $\frac{8\pi}{3}$ | \(y=x\) leftover |
| 16 | 101 | $\text{Find the volume of the solid formed by rotating the region between }y=4\text{ and }y=x\text{ on }[0,4]\text{ about the }x\text{-axis (washer method).}$ | $\frac{128\pi}{3}$ | washer only |
| 16 | 207 | $\text{Find the volume of the solid formed by rotating the region between }y=2\text{ and }y=x\text{ on }[0,2]\text{ about the }x\text{-axis (washer method).}$ | $\frac{16\pi}{3}$ | no disk leftover |
| 22 | 101 | $\text{Find the volume of the solid formed by rotating the region between }y=3\text{ and }y=x\text{ on }[0,3]\text{ about the }x\text{-axis (washer method).}$ | $18\pi$ | washer only |
| 22 | 207 | $\text{Find the volume of the solid formed by rotating the region between }y=2\text{ and }y=x\text{ on }[0,2]\text{ about the }x\text{-axis (washer method).}$ | $\frac{16\pi}{3}$ | washer only |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Same three builders; leftover cliffs unchanged. Pairwise stamps `form_id` + `generator=volume_disk_washer` via `select_form_id`. Gallery seeds 101/207/313 can collide on one form at mid D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,2]\text{ about the }x\text{-axis (disk method).}$ | $\frac{8\pi}{3}$ | `vdw_disk_linear` |
| 0 | 0 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,3]\text{ about the }x\text{-axis (disk method).}$ | $9\pi$ | old easy |
| 8 | 1 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,2]\text{ about the }x\text{-axis (disk method).}$ | $\frac{8\pi}{3}$ | \(y=x\) leftover |
| 8 | 101 | $\text{Find the volume of the solid formed by rotating }y=x^{2}\text{ on }[0,3]\text{ about the }x\text{-axis (disk method).}$ | $\frac{243\pi}{5}$ | `vdw_disk_quadratic` |
| 16 | 101 | $\text{Find the volume of the solid formed by rotating the region between }y=3\text{ and }y=x\text{ on }[0,3]\text{ about the }x\text{-axis (washer method).}$ | $18\pi$ | no disk leftover |
| 16 | 1 | $\text{Find the volume of the solid formed by rotating the region between }y=2\text{ and }y=x\text{ on }[0,2]\text{ about the }x\text{-axis (washer method).}$ | $\frac{16\pi}{3}$ | `vdw_washer` |
| 22 | 101 | $\text{Find the volume of the solid formed by rotating the region between }y=3\text{ and }y=x\text{ on }[0,3]\text{ about the }x\text{-axis (washer method).}$ | $18\pi$ | `vdw_washer` only |
| 22 | 207 | $\text{Find the volume of the solid formed by rotating the region between }y=7\text{ and }y=x\text{ on }[0,7]\text{ about the }x\text{-axis (washer method).}$ | $\frac{686\pi}{3}$ | bound grows |

40-seed counts **after**: D=0 `vdw_disk_linear` only; D=8 leftover `vdw_disk_linear` + `vdw_disk_quadratic` (19/21); D=16 `vdw_washer` only; D=22 `vdw_washer` only.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §6.2 Determining Volumes by Slicing | https://openstax.org/books/calculus-volume-1/pages/6-2-determining-volumes-by-slicing | Disk about \(x\)-axis (Ex. 6.8 \(\sqrt{x}\) on \([1,4]\) is richer than old \(y=x\) / \(y=x^{2}\); Ex. 6.7 \(x^{2}-4x+5\) on \([1,4]\)) |
| OpenStax Calculus Volume 1 §6.2 washer | https://openstax.org/books/calculus-volume-1/pages/6-2-determining-volumes-by-slicing | Washer about \(x\)-axis (Ex. 6.10 \(x\) vs \(1/x\) on \([1,4]\)); old path is \(y=n\) vs \(y=x\) on \([0,n]\) |
| OpenStax Calculus Volume 1 §6.2 \(y\)-axis | https://openstax.org/books/calculus-volume-1/pages/6-2-determining-volumes-by-slicing | Disk about \(y\)-axis (Ex. 6.9 \(g(y)=\sqrt{4-y}\)) and washer about \(y=-2\) (Ex. 6.11) — not on this leaf; no figure bank |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (6-2). Pyramid slicing (Ex. 6.6) is the known-cross-section sibling.

## Variety notes

Not a WP. D=0 one easy disk \(y=x\) (old). Same-D rotation at mid D: leftover \(y=x\) vs disk \(y=x^{2}\). High D keeps the old washer \(y=n\) vs \(y=x\) builder (do not invent \(\sqrt{x}\) / \(1/x\) / \(y\)-axis). Three old forms, so D=16/22 are washer-only — leftover lockout already lived in `volume_methods`, unlike FTC area which had to stop accumulating \(y=x\). Shell method stays on `calc_app_int_volume_by_cylinders`.

## Limitations

- **Status:** shipped — leftover lockout of disk \(y=x\). Remaining `LIMITATIONS`: three frozen old builders (disk \(y=x\), disk \(y=x^{2}\), washer \(y=n\) vs \(y=x\) on \([0,n]\)); no Ex. 6.8 \(\sqrt{x}\) / Ex. 6.7 shifted quad / Ex. 6.10 \(1/x\) washer / \(y\)-axis / rotate about \(y=k\); no figure / solid-of-revolution SVG; D=10–15 can still emit disk \(x^{2}\) leftover (intentional `volume_methods` cliff).
- **Live pairwise:** each item stamps `form_id`, shared `generator=volume_disk_washer`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `volume_disk_washer`

## Proposed engine (reuse vs new)

- **Reuse:** existing disk-linear / disk-quadratic / washer builders (now in `calc_app_diff.py`). Depth = real structure (lock out disk \(y=x\); mix leftover at D=8; washer-only at D=16/22) — not padded `difficulty_costs`.
- **Not this pass:** \(\sqrt{x}\) / \(1/x\) washers; \(y\)-axis disks; rotate about \(y=k\); shell / known-cross-section stems; solid SVG.
