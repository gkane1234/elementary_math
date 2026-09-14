# Notes — `calc_indef_int_trigonometric_with_substitution`

- **Display name:** Trigonometric substitution
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_trig_substitution`
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Integrate using a trigonometric substitution \(x=a\sin\theta\), \(x=a\tan\theta\), or \(x=a\sec\theta\) (OpenStax Vol. 2 §3.3).
- **D=0:** Old easy leftover is catalog \(\int\sqrt{a^{2}-x^{2}}\,dx\) (`sqrt_a2_minus_x2`).
- **Mid D (≈8):** EMH `auto` — catalog `d_min` unlocks \(\sqrt{a^{2}+x^{2}}\) / \(\sqrt{x^{2}-a^{2}}\), \(1/\sqrt{\,\cdot\,}\), \(x^{2}/\sqrt{\,\cdot\,}\). D=0 minus leftover is already rare.
- **High D (≈16–22):** EMH `trig_sub_form_preset=bc_bank` — \(x^{2}/\sqrt{\,\cdot\,}\), \((\,\cdot\,)^{\pm 3/2}\), optional linear wrap \(u=x+b\). No `sqrt_a2_minus_x2`.
- **Must not:** Plain power u-sub \(\int x(x^{2}+1)^{n}\,dx\); frozen bank LaTeX \(\sqrt{9-x^{2}}\); \(\sqrt{a^{2}-x^{2}}/x\) without a closed form; \(x^{3}/\sqrt{\,\cdot\,}\) (u-sub rewrite); padded `difficulty_costs`; leftover-lock named `trig_sub_preset_bc_bank` empty at expert.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**. Live path is `calculus_integrals` → `_sample_trig_sub`. EMH presets already band leftover families: easy/medium `trig_sub_form_preset=auto` / catalog `d_min`; hard `bc_bank` (excludes `sqrt_a2_minus_x2`). `form_id` / `generator=integral_trig_substitution` already stamped on metadata and `spec_snapshot` (40/40). Catalog `d_min` already makes D=0 minus rare at D=8.

40-seed counts: D=0 `sqrt_a2_minus_x2` 40; D=8 leftover minus 1 / `x2_over_sqrt_*` 19 / `one_over_sqrt_*` 15 / `sqrt_a2_plus_x2` 4 / `sqrt_x2_minus_a2` 1; D=16/22 identical (`pow_m3_2_a2_minus` 7 / `x2_over_sqrt_*` 10 / `pow_3_2_*` 7 / `pow_m3_2_a2_plus` 4 / `one_over_sqrt_*` 5 / `sqrt_a2_plus_x2` 3 / `sqrt_x2_minus_a2` 3 / `pow_m3_2_x2_minus` 1). No `sqrt_a2_minus_x2` at D≥16.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \sqrt{4-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{4-x^{2}}+2\arcsin\left(\frac{x}{2}\right)+C$ | `sqrt_a2_minus_x2`, preset=`auto` |
| 0 | 207 | $\int \sqrt{16-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | same D=0 leftover |
| 0 | 313 | $\int \sqrt{9-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)+C$ | lookalike \(a\) varies |
| 8 | 101 | $\int \sqrt{4+x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{4+x^{2}}+2\ln\left\lvert x+\sqrt{4+x^{2}}\right\rvert+C$ | `sqrt_a2_plus_x2` |
| 8 | 207 | $\int \sqrt{16-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | rare leftover minus (1/40) |
| 16 | 101 | $\int \left(16+\left(x - 3\right)^{2}\right)^{\frac{3}{2}}\,dx$ | wrap + `(a²+x²)^{3/2}` | `u_sub`+`trig_sub`; bank preset |
| 16 | 207 | $\int \sqrt{x^{2}-16}\,dx$ | $\frac{1}{2}x\sqrt{x^{2}-16}-8\ln\left\lvert x+\sqrt{x^{2}-16}\right\rvert+C$ | `sqrt_x2_minus_a2` leftover in `bc_bank` |
| 16 | 313 | $\int \frac{x^{2}}{\sqrt{4-x^{2}}}\,dx$ | $-\frac{1}{2}x\sqrt{4-x^{2}}+2\arcsin\left(\frac{x}{2}\right)+C$ | `x2_over_sqrt_a2_minus_x2` |
| 22 | 207 | $\int \sqrt{x^{2}-16}\,dx$ | $\frac{1}{2}x\sqrt{x^{2}-16}-8\ln\left\lvert x+\sqrt{x^{2}-16}\right\rvert+C$ | same hard preset as D=16; not leftover \(\sqrt{a^{2}-x^{2}}\) |

Opt-out flag used: _(none — live generator is the old path)_

## Live now — skip further leftover lockout

Already rich enough: leftover mix + stamps. Exclusive bands on `auto` would not change live `_generate_for_type` at D≥16 (named `bc_bank`). D=8 already drops `sqrt_a2_minus_x2` almost entirely (1/40 via catalog `d_min`). Lockout *under* named `bc_bank` would empty `trig_sub_preset_bc_bank` of \(\sqrt{a^{2}+x^{2}}\) / \(\sqrt{x^{2}-a^{2}}\) leftovers that *are* the named mix. `sqrt_x2_minus_a2` leftover at D≥16 stays in `bc_bank` (same as cubic leftover on the power-u-sub host). Did not invent cores. `select_form_id` / `live_quality_form_weights` already apply inside each preset.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 2 §3.3 | https://openstax.org/books/calculus-volume-2/pages/3-3-trigonometric-substitution | √(a²−x²) sin-sub — e.g. Example 3.21 \(\int\sqrt{9-x^{2}}\,dx\); Example 3.24 \(1/\sqrt{x^{2}+a^{2}}\); Checkpoint-style \(x^{2}/\sqrt{a^{2}-x^{2}}\). Example 3.22 \(\sqrt{4-x^{2}}/x\) stays deferred (no closed template). |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-2/` · `question_engine/frameworks/primitives/openstax_form_catalogs/trig_substitution.json`.

Catalog forms (implemented lookalikes, not frozen bank coeffs): `sqrt_a2_minus_x2` (D=0 leftover), `sqrt_a2_plus_x2`, `sqrt_x2_minus_a2`, `one_over_sqrt_x2_plus_a2` / `_minus_a2`, `x2_over_sqrt_a2_minus_x2` / `_x2_plus_a2` / `_x2_minus_a2`, `pow_3_2_*`, `pow_m3_2_a2_plus` / `_a2_minus` / `_x2_minus`. Named preset `trig_sub_form_preset=bc_bank`.

## Variety notes

Not a WP. D=0 one easy OpenStax frame. Mid D rotates §3.3 algebraic radicals (catalog `d_min`). High D is named `bc_bank` (no D=0 minus leftover). Coefficients vary (`a=2,3,4,…`) — not a frozen \(\sqrt{9-x^{2}}\) bank copy. D=16 and D=22 share the hard preset (intentional skip of a fourth EMH band).

## Limitations

- **Status:** skipped further leftover lockout — live already stamps `form_id` + `generator=integral_trig_substitution`; EMH presets already drop `sqrt_a2_minus_x2` at D≥16 (`bc_bank`). Remaining `LIMITATIONS`: D=0 frozen `sqrt_a2_minus_x2`; D=8 can still emit rare minus leftover (1/40); D=16 and D=22 are the same `bc_bank` mix (`sqrt_x2_minus_a2` leftover stays at expert); \(\int\sqrt{a^{2}-x^{2}}/x\,dx\) (`sqrt_over_x_a2_minus`) stub — no honest ln+sqrt template; \(\int x/\sqrt{x^{2}-a^{2}}\) and \(\int x^{3}/\sqrt{x^{2}\pm a^{2}}\) deferred (u-sub / rewrite, wrong leaf); \(\int 1/\sqrt{a^{2}-x^{2}}\) deferred (arcsin table on the invtrig leaf); hyperbolic \(x=\sinh\theta\) deferred; named showcase `trig_sub_preset_bc_bank` stays full family.
- **Live pairwise:** each item stamps `form_id`, `generator=integral_trig_substitution`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `integral_trig_substitution`

## Proposed engine (reuse vs new)

- **Reuse:** existing `_sample_trig_sub` + `trig_substitution.json` + named preset `bc_bank`. Depth = document skip, not a new exclusive-band overlay on named presets.
- **Not this pass:** exclusive leftover bands; new expert EMH preset; locking `sqrt_x2_minus_a2` out of `bc_bank` (that *is* the named mix); inventing a closed template for Example 3.22 \(\sqrt{a^{2}-x^{2}}/x\).
