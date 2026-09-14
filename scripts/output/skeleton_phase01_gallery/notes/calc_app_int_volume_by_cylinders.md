# Notes — `calc_app_int_volume_by_cylinders` (`Volume by cylinders`)

- **Display name:** Volume by cylinders
- **Category:** Calculus — Applications of Integration
- **Generator:** `volume_shell`
- **Suggested family:** other (text rotate-about-\(y\)-axis; no figure bank)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Find the volume of a solid of revolution by cylindrical shells about the \(y\)-axis.
- **D=0:** Shell leftover \(y=x\) on \([0,n]\) with \(n\in\{2,3,4\}\) (old easy).
- **Mid D (≈8):** \(y=x\) leftover still allowed, plus shell \(y=x^{2}\).
- **High D (≈16):** Lock out \(y=x\). \(y=x^{2}\) leftover plus \(y=n-x\) on \([0,n]\).
- **Expert (≈22):** \(y=n-x\) only.
- **Must not:** Disk / washer / known-cross-section stems (sibling leaves); padded `difficulty_costs`; new cores (\(1/x\), \(2x-x^{2}\), \(x\)-axis shells, rotate about \(x=k\)).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Exclusive cliffs (`if band == easy/medium/hard`), so D=8 was \(y=x^{2}\) only and high D never mixed leftover \(y=x\). `generator` / `form_id` unstamped. No `spec_snapshot`. 40-seed counts: D=0 all \(y=x\); D=8 exclusive \(y=x^{2}\); D=16 \(y=n-x\) only; D=22 \(y=n-x\) only.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,4]\text{ about the }y\text{-axis (shell method).}$ | $\frac{128\pi}{3}$ | \(y=x\) only |
| 0 | 0 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,2]\text{ about the }y\text{-axis (shell method).}$ | $\frac{16\pi}{3}$ | \(n\in\{2,3,4\}\) |
| 8 | 101 | $\text{Find the volume of the solid formed by rotating }y=x^{2}\text{ on }[0,3]\text{ about the }y\text{-axis (shell method).}$ | $\frac{81\pi}{2}$ | exclusive \(x^{2}\), no leftover \(y=x\) |
| 8 | 1 | $\text{Find the volume of the solid formed by rotating }y=x^{2}\text{ on }[0,2]\text{ about the }y\text{-axis (shell method).}$ | $8\pi$ | exclusive cliff |
| 16 | 101 | $\text{Find the volume of the solid formed by rotating }y=4-x\text{ on }[0,4]\text{ about the }y\text{-axis (shell method).}$ | $\frac{64\pi}{3}$ | \(y=n-x\) only |
| 16 | 207 | $\text{Find the volume of the solid formed by rotating }y=3-x\text{ on }[0,3]\text{ about the }y\text{-axis (shell method).}$ | $9\pi$ | no leftover |
| 22 | 101 | $\text{Find the volume of the solid formed by rotating }y=7-x\text{ on }[0,7]\text{ about the }y\text{-axis (shell method).}$ | $\frac{343\pi}{3}$ | bound grows |
| 22 | 0 | $\text{Find the volume of the solid formed by rotating }y=2-x\text{ on }[0,2]\text{ about the }y\text{-axis (shell method).}$ | $\frac{8\pi}{3}$ | \(y=n-x\) only |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same three builders. D=0 stays old \(y=x\). Gallery seeds 101/207/313 can collide on one form at mid D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,2]\text{ about the }y\text{-axis (shell method).}$ | $\frac{16\pi}{3}$ | `vsh_linear` |
| 0 | 0 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,3]\text{ about the }y\text{-axis (shell method).}$ | $18\pi$ | old easy |
| 8 | 1 | $\text{Find the volume of the solid formed by rotating }y=x\text{ on }[0,2]\text{ about the }y\text{-axis (shell method).}$ | $\frac{16\pi}{3}$ | \(y=x\) leftover |
| 8 | 101 | $\text{Find the volume of the solid formed by rotating }y=x^{2}\text{ on }[0,3]\text{ about the }y\text{-axis (shell method).}$ | $\frac{81\pi}{2}$ | `vsh_quadratic` |
| 16 | 1 | $\text{Find the volume of the solid formed by rotating }y=x^{2}\text{ on }[0,2]\text{ about the }y\text{-axis (shell method).}$ | $8\pi$ | \(x^{2}\) leftover |
| 16 | 101 | $\text{Find the volume of the solid formed by rotating }y=3-x\text{ on }[0,3]\text{ about the }y\text{-axis (shell method).}$ | $9\pi$ | no \(y=x\) leftover |
| 22 | 101 | $\text{Find the volume of the solid formed by rotating }y=3-x\text{ on }[0,3]\text{ about the }y\text{-axis (shell method).}$ | $9\pi$ | `vsh_line` only |
| 22 | 207 | $\text{Find the volume of the solid formed by rotating }y=7-x\text{ on }[0,7]\text{ about the }y\text{-axis (shell method).}$ | $\frac{343\pi}{3}$ | bound grows |

40-seed counts **after**: D=0 `vsh_linear` only; D=8 leftover `vsh_linear` + `vsh_quadratic` (19/21); D=16 leftover `vsh_quadratic` + `vsh_line` (19/21, no `vsh_linear`); D=22 `vsh_line` only.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §6.3 Volumes of Revolution: Cylindrical Shells | https://openstax.org/books/calculus-volume-1/pages/6-3-volumes-of-revolution-cylindrical-shells | Shell \(V=2\pi\int x\,f(x)\,dx\) about the \(y\)-axis |
| OpenStax Calculus Volume 1 §6.3 Example 6.12 | https://openstax.org/books/calculus-volume-1/pages/6-3-volumes-of-revolution-cylindrical-shells | Region under \(1/x\) on \([1,b]\) — richer than old \(y=x\) / \(y=x^{2}\); not invented here |
| OpenStax Calculus Volume 1 §6.3 Example 6.13 | https://openstax.org/books/calculus-volume-1/pages/6-3-volumes-of-revolution-cylindrical-shells | Region under \(2x-x^{2}\) — not invented here; old high D is \(y=n-x\) on \([0,n]\) |
| OpenStax Calculus Volume 1 §6.3 \(x\)-axis shells | https://openstax.org/books/calculus-volume-1/pages/6-3-volumes-of-revolution-cylindrical-shells | Shells about the \(x\)-axis (\(dy\)) — not on this leaf; no figure bank |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (6-3). Disk/washer stays on `calc_app_int_volume_by_slicing_disks_and_washers`.

## Variety notes

Not a WP. D=0 one easy shell \(y=x\) (old). Same-D rotation at mid D: leftover \(y=x\) vs shell \(y=x^{2}\). High D keeps the old \(y=n-x\) builder (do not invent \(1/x\) / \(2x-x^{2}\) / \(x\)-axis). Three old forms, so D=16 mixes \(x^{2}\) leftover + \(y=n-x\) and D=22 is \(y=n-x\)-only.

## Limitations

- **Status:** shipped — leftover lockout of exclusive cliffs / D=0 \(y=x\). Remaining `LIMITATIONS`: three frozen old builders (shell \(y=x\), shell \(y=x^{2}\), shell \(y=n-x\) on \([0,n]\)); no Ex. 6.12 \(1/x\) / Ex. 6.13 \(2x-x^{2}\) / \(x\)-axis shells / rotate about \(x=k\); no figure / solid-of-revolution SVG; D=16 can still emit \(y=x^{2}\) leftover (intentional).
- **Live pairwise:** each item stamps `form_id`, shared `generator=volume_shell`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `volume_shell`

## Proposed engine (reuse vs new)

- **Reuse:** existing shell-linear / shell-quadratic / shell-line builders (now in `calc_app_diff.py`). Depth = real structure (lock out \(y=x\); mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** \(1/x\) / \(2x-x^{2}\) shells; \(x\)-axis shells; rotate about \(x=k\); disk / washer / known-cross-section stems; solid SVG.
