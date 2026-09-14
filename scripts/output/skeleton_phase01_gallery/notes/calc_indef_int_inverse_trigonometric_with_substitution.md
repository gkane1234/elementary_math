# Notes — `calc_indef_int_inverse_trigonometric_with_substitution`

- **Display name:** Inverse trigonometric with substitution
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_invtrig_substitution`
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Indefinite inverse-trig antiderivative after u-sub \(+C\) (OpenStax Vol. 1 §5.5 / §5.7).
- **D=0:** Old easy leftover is catalog \(\int a/(1+(ax+b)^{2})\,dx\to\arctan(ax+b)\) (`arctan_of_linear`).
- **Mid D (≈8):** Same `arctan_chain` catalog family; numeric_tier only (larger \(a,b\)).
- **High D (≈16–22):** EMH `reverse_chain` — nested \(F\circ g\) (`invtrig_arctan` / `invtrig_arcsin`).
- **Must not:** Table \(\int 1/(1+x^{2})\) (non-sub sibling); algebraic `power_linear_du` leak; padded `difficulty_costs`; new cores; leftover-lock named `arctan_chain` showcase empty at expert.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**. Live path is `calculus_integrals` → `_sample_u_sub_derivative_backed` flavor `invtrig`. EMH presets already band construction: easy/medium `u_sub_form_preset=arctan_chain` / catalog; hard `arctan_chain` / `reverse_chain`. `form_id` / `generator=integral_invtrig_substitution` already stamped on metadata and `spec_snapshot` (40/40). Catalog `arctan_of_ln` is in the named preset but gated off (`allow_log=False` on this pack). Reverse-chain invtrig `conceptual` cap is \(4.0\), so D=16 and D=22 share the same reverse-chain mix.

40-seed counts: D=0 `arctan_of_linear` 40; D=8 `arctan_of_linear` 40 (numeric_tier 2 vs 0); D=16/22 identical (`invtrig_arctan` 25 / `invtrig_arcsin` 15). No `arctan_of_linear` at D≥16.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{2}{1+(2x + 2)^{2}}\,dx$ | $\arctan(2x + 2)+C$ | catalog `arctan_of_linear` (easy preset `arctan_chain`) |
| 0 | 207 | $\int \frac{2}{1+(2x + 2)^{2}}\,dx$ | $\arctan(2x + 2)+C$ | same D=0 leftover |
| 8 | 101 | $\int \frac{3}{1+(3x + 4)^{2}}\,dx$ | $\arctan(3x + 4)+C$ | same family; larger coeffs (numeric_tier 2) |
| 8 | 207 | $\int \frac{4}{1+(4x + 3)^{2}}\,dx$ | $\arctan(4x + 3)+C$ | medium preset is still `arctan_chain` / catalog |
| 16 | 101 | $\int \frac{1}{1+(\arcsin(x))^{2}}\frac{1}{\sqrt{1-(x)^{2}}}\,dx$ | $\arctan\left(\arcsin(x)\right)+C$ | reverse-chain `invtrig_arctan` |
| 16 | 207 | $\int \frac{1}{\sqrt{1-(\arctan(x))^{2}}}\frac{1}{1+(x)^{2}}\,dx$ | $\arcsin\left(\arctan(x)\right)+C$ | reverse-chain `invtrig_arcsin` |
| 22 | 101 | $\int \frac{1}{1+(\arcsin(x))^{2}}\frac{1}{\sqrt{1-(x)^{2}}}\,dx$ | $\arctan\left(\arcsin(x)\right)+C$ | same hard preset as D=16 |
| 22 | 207 | $\int \frac{1}{\sqrt{1-(\arctan(x))^{2}}}\frac{1}{1+(x)^{2}}\,dx$ | $\arcsin\left(\arctan(x)\right)+C$ | no catalog `arctan_of_linear` |

Opt-out flag used: _(none — live generator is the old path)_

## Live now — skip further leftover lockout

Already stamps + EMH construction bands. Exclusive leftover bands on `auto` would not change live `_generate_for_type` (named `arctan_chain`). Lockout *under* the named catalog preset would empty `u_sub_preset_arctan_chain` at expert. Mixing reverse-chain at D=8 (format_tier 0) is the same linear-arctan skill as catalog `arctan_of_linear`, not a new existing core. `arctan_of_ln` needs `allow_log` (off on this pack); `power_linear_du` is the wrong skill. Did not invent cores. `select_form_id` / `live_quality_form_weights` already apply inside the catalog path.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.5 | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | u-sub into invtrig forms — chain factor \(g'\) with outer \(\arctan\) / \(\arcsin\). |
| OpenStax Calculus Volume 1 §5.7 | https://openstax.org/books/calculus-volume-1/pages/5-7-integrals-resulting-in-inverse-trigonometric-functions | invtrig antiderivative after sub — Example 5.50 \(\int dx/\sqrt{4-9x^{2}}\) (scaled arcsin; table sibling). Catalog `arctan_of_linear` is \(\int a/(1+(ax+b)^{2})\). Nested reverse-chain \(F\circ g\) is richer than §5.7 drills. |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-5, 5-7).

## Variety notes

Not a WP. D=0/8 is the named `arctan_chain` catalog leftover (old easy). High D is reverse-chain `invtrig_arctan` / `invtrig_arcsin`. Do not invent arcsec / nested \(\arctan(\arctan(\cdot))\) / Ex. 5.49 definite cores. D=16 and D=22 share the hard preset (intentional skip of a fourth EMH band).

## Limitations

- **Status:** skipped further leftover lockout — live already stamps `form_id` + `generator=integral_invtrig_substitution`; EMH presets already drop catalog `arctan_of_linear` at D≥16 (`u_sub_construction=reverse_chain`). Remaining `LIMITATIONS`: D=0 and D=8 frozen `arctan_of_linear` (easy===medium named preset; numeric_tier only); D=16 and D=22 are the same reverse-chain mix (invtrig conceptual cap \(4.0\); no nested \(\arctan\circ\arctan\)); `arctan_of_ln` unused (`allow_log=False`); flavor still mixes `power_linear_du` if construction is catalog-only without the named preset; named showcases `u_sub_preset_arctan_chain` / `u_sub_reverse_chain_invtrig` stay full family; no diagram.
- **Live pairwise:** each item stamps `form_id`, `generator=integral_invtrig_substitution`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Catalog form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `integral_invtrig_substitution`

## Proposed engine (reuse vs new)

- **Reuse:** existing `_sample_u_sub_derivative_backed` flavor `invtrig` + `u_substitution.json` preset `arctan_chain` + reverse-chain. Depth = document skip, not a new exclusive-band overlay on named presets.
- **Not this pass:** exclusive leftover bands; new expert EMH preset; enabling `allow_log` for `arctan_of_ln`; locking `arctan_of_linear` out of D=0 (that *is* the easy named mix).
