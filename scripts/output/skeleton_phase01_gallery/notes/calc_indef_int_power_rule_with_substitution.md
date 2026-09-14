# Notes — `calc_indef_int_power_rule_with_substitution`

- **Display name:** Power rule with substitution
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_substitution`
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Indefinite power antiderivative after u-sub \(+C\) (OpenStax Vol. 1 §5.5).
- **D=0:** Old easy leftover is catalog \(\int a(ax+b)^n\,dx\) (`power_linear_du`).
- **Mid D (≈8):** EMH `power_quadratic` — \(\int 2x(x^{2}+c)^n\) / \(\int x\sqrt{x^{2}+c}\) (`power_quad_x_du` / `root_quad_x_du`).
- **High D (≈16–22):** EMH `challenging` ∩ power flavor (Checkpoint 5.25/5.26 cubic / Example 5.31 root-quad leftover / Example 5.31-style alteration).
- **Must not:** Table \(\int x^n\) (non-sub sibling); padded `difficulty_costs`; new cores; leftover-lock named `u_sub_preset_power_linear` / `power_quadratic` / `challenging` showcases empty at expert.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**. Live path is `calculus_integrals` → `_sample_u_sub_derivative_backed` flavor `power`. EMH presets already band leftover families: easy `u_sub_form_preset=power_linear` / catalog; medium `power_quadratic` / catalog; hard `challenging` / auto. Catalog `d_max` already locks `power_linear_du` at D>10. `form_id` / `generator=integral_substitution` already stamped on metadata and `spec_snapshot` (40/40).

40-seed counts: D=0 `power_linear_du` 40; D=8 `root_quad_x_du` 22 / `power_quad_x_du` 18 (no linear); D=16/22 identical (`power_cubic_x2_du` 15 / `alteration_linear_over_root` 14 / `root_quad_x_du` 11). No `power_linear_du` at D≥8.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int 2\left(2x + 2\right)^{2}\,dx$ | $\frac{1}{3}\left(2x + 2\right)^{3}+C$ | `power_linear_du` (easy preset `power_linear`) |
| 0 | 207 | $\int 2\left(2x + 2\right)^{2}\,dx$ | $\frac{1}{3}\left(2x + 2\right)^{3}+C$ | same D=0 leftover |
| 8 | 101 | $\int 2x\left(x^{2}+5\right)^{2}\,dx$ | $\frac{1}{3}\left(x^{2}+5\right)^{3}+C$ | `power_quad_x_du` (medium `power_quadratic`) |
| 8 | 207 | $\int x\sqrt{x^{2}+1}\,dx$ | $\frac{1}{3}\left(x^{2}+1\right)^{\frac{3}{2}}+C$ | `root_quad_x_du` Example 5.31 family |
| 16 | 101 | $\int x^{2}\left(x^{3}+9\right)^{2}\,dx$ | $\frac{1}{9}\left(x^{3}+9\right)^{3}+C$ | `power_cubic_x2_du` Checkpoint 5.25 leftover in `challenging` |
| 16 | 207 | $\int \frac{x}{\sqrt{x-1}}\,dx$ | $\frac{2}{3}\left(x-1\right)^{\frac{3}{2}}+2\sqrt{x-1}+C$ | `alteration_linear_over_root` |
| 22 | 101 | $\int x^{2}\left(x^{3}-1\right)^{4}\,dx$ | $\frac{1}{15}\left(x^{3}-1\right)^{5}+C$ | same hard preset as D=16; numeric_tier 4 |
| 22 | 207 | $\int \frac{x}{\sqrt{x-1}}\,dx$ | $\frac{2}{3}\left(x-1\right)^{\frac{3}{2}}+2\sqrt{x-1}+C$ | no `power_linear_du` |

Opt-out flag used: _(none — live generator is the old path)_

## Live now — skip further leftover lockout

Already rich enough: EMH leftover mix + stamps. Exclusive bands on `auto` would not change live `_generate_for_type` (named presets). Lockout *under* named presets would empty `u_sub_preset_power_linear` / `u_sub_preset_power_quadratic` / `u_sub_preset_challenging` at expert. `root_quad_x_du` leftover at D≥16 is the medium family staying in `challenging` ∩ power (same as cubic leftover on the ln/exp host). Did not invent cores. `select_form_id` / `live_quality_form_weights` already apply inside each preset.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.5 | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | u-sub on power compositions — Example 5.30 \(\int 6x(3x^{2}+4)^{4}\) (`power_quad_x_du`); Example 5.31 \(\int z\sqrt{z^{2}-5}\) (`root_quad_x_du` / alteration); Checkpoint 5.25/5.26 cubic (`power_cubic_x2_du`). Catalog D=0 leftover is linear \(u=ax+b\). |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-5).

## Variety notes

Not a WP. D=0 is the named `power_linear` leftover (old easy). Mid D is `power_quadratic`. High D is `challenging` ∩ power (three implemented algebraic builders). Do not invent a new trig/exp challenging core on this host (those live on the ln/exp sibling). D=16 and D=22 share the hard preset (intentional skip of a fourth EMH band).

## Limitations

- **Status:** skipped further leftover lockout — live already stamps `form_id` + `generator=integral_substitution`; EMH presets already drop `power_linear_du` at D≥8. Remaining `LIMITATIONS`: D=0 frozen `power_linear_du`; D=16 and D=22 are the same `challenging` mix (cubic / root-quad leftover stays at expert); reverse-chain nested F∘g still richer than §5.5 drills when `u_sub_construction=auto` at format_tier≥1 (live 40-seed stayed catalog); BC-bank §1 algebraic families unlock via named `bc_bank`, not the hard default; named showcases `u_sub_preset_*` / `u_sub_reverse_chain` stay full family; reverse-chain still shows unsimplified juxtaposition (`2x(-4)`).
- **Live pairwise:** each item stamps `form_id`, `generator=integral_substitution`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `integral_substitution`

## Proposed engine (reuse vs new)

- **Reuse:** existing `_sample_u_sub_derivative_backed` flavor `power` + `u_substitution.json` presets (`power_linear`, `power_quadratic`, `challenging`, `bc_bank`) + reverse-chain. Depth = document skip, not a new exclusive-band overlay on named presets.
- **Not this pass:** exclusive leftover bands; new expert EMH preset; locking `root_quad_x_du` out of `challenging` (that *is* the named mix).
