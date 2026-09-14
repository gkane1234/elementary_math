# Notes — `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`

- **Display name:** Logarithmic rule and exponentials with subs.
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_log_exp_substitution`
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Indefinite ln/exp antiderivative after u-sub \(+C\) (OpenStax Vol. 1 §5.5–5.6).
- **D=0:** Old easy leftover is the EMH `du_over_u` mix \(\int a/(ax+b)\) / \(\int\sin/\cos^{3}\) (catalog `du_over_u_linear` / `du_over_u_trig`).
- **Mid D (≈8):** EMH `exp_chain` — \(\int e^{\sin x}\cos x\), \(\int e^{ax+b}\), Checkpoint 5.33 quartic / Example 5.39 cubic.
- **High D (≈16–22):** EMH `challenging` ∩ ln/exp flavor (cubic/quartic leftover + Ex. 5.38 root-chain / Checkpoint 5.32 power-of-exp / \(\ln^{2}\) / nested \(e^{\sin(kx)}\)).
- **Must not:** Table \(\int 1/x\) / \(\int e^{x}\) (non-sub sibling); padded `difficulty_costs`; new cores; leftover-lock named showcases empty at expert.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**. Live path is `calculus_integrals` → `_sample_u_sub_derivative_backed` flavor `ln_exp`. EMH presets already band leftover families: easy `u_sub_form_preset=du_over_u` / catalog; medium `exp_chain` / catalog; hard `challenging` / auto. Catalog `d_max` already locks `du_over_u_linear` at D>12 and `exp_of_poly` at D>14. `form_id` / `generator=integral_log_exp_substitution` already stamped on metadata and `spec_snapshot` (40/40). Stale notes that showed `du_over_u_trig` at D=16–22 were from before the challenging preset; live 40-seed D=16/22 has **no** `du_over_u_trig`.

40-seed counts: D=0 `du_over_u_trig` 23 / `du_over_u_linear` 17; D=8 `exp_of_trig` 15 / `exp_of_quartic` 11 / `exp_of_cubic` 8 / `exp_of_poly` 6; D=16/22 identical (`ln_squared_chain` 9 / `exp_of_quartic` 8 / `exp_power_of_exp` 8 / `exp_of_cubic` 7 / `nested_trig_exp` 5 / `exp_root_chain` 3).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{2}{2x + 2}\,dx$ | $\ln|2x + 2|+C$ | `du_over_u_linear` (easy preset `du_over_u`) |
| 0 | 207 | $\int \frac{\sin(x)}{\cos^{3}(x)}\,dx$ | $\frac{1}{2}\sec^{2}(x)+C$ | `du_over_u_trig` leftover at D=0 (`d_min=6`; `select_form_id` fallback) |
| 8 | 101 | $\int e^{\sin(x)}\cos(x)\,dx$ | $e^{\sin(x)}+C$ | `exp_of_trig` (medium `exp_chain`) |
| 8 | 207 | $\int 2x^{3}e^{-2x^{4}}\,dx$ | $-\frac{1}{4}e^{-2x^{4}}+C$ | `exp_of_quartic` Checkpoint 5.33 family |
| 16 | 101 | $\int x^{2}e^{-x^{3}}\,dx$ | $-\frac{1}{3}e^{-x^{3}}+C$ | `exp_of_cubic` leftover in `challenging` |
| 16 | 207 | $\int e^{\cos(2x)}\sin(2x)\,dx$ | $-\frac{1}{2}e^{\cos(2x)}+C$ | `nested_trig_exp` |
| 22 | 101 | $\int x^{2}e^{-x^{3}}\,dx$ | $-\frac{1}{3}e^{-x^{3}}+C$ | same hard preset as D=16 |
| 22 | 207 | $\int e^{\cos(2x)}\sin(2x)\,dx$ | $-\frac{1}{2}e^{\cos(2x)}+C$ | no `du_over_u_trig` |

Exact OpenStax Checkpoint 5.33 (`exp_chain`, D=8): \(\int 2x^{3}e^{x^{4}}\,dx\) → \(\frac{1}{2}e^{x^{4}}+C\). High format (D≥16) omits the 2: \(\int x^{3}e^{x^{4}}\,dx\) → \(\frac{1}{4}e^{x^{4}}+C\).

Opt-out flag used: _(none — live generator is the old path)_

## Live now — skip further leftover lockout

Already rich enough: EMH leftover mix + stamps. Exclusive bands on `auto` would not change live `_generate_for_type` (named presets). Lockout *under* named presets would empty `u_sub_preset_du_over_u` / `u_sub_preset_challenging_ln_exp` at expert. Did not invent cores. `select_form_id` / `live_quality_form_weights` already apply inside each preset.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.5 | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | u-sub into ln/exp — linear \(du/u\); Example 5.32 / Checkpoint 5.27 trig \(du/u\) warmup is `du_over_u_trig`. |
| OpenStax Calculus Volume 1 §5.6 | https://openstax.org/books/calculus-volume-1/pages/5-6-integrals-involving-exponential-and-logarithmic-functions | ln/exp after sub — Example 5.38 \(\int e^{x}\sqrt{1+e^{x}}\) (`exp_root_chain`); Example 5.39 \(\int 3x^{2}e^{2x^{3}}\) (`exp_of_cubic`); Checkpoint 5.33 \(\int 2x^{3}e^{x^{4}}\) (`exp_of_quartic`). |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-5, 5-6).

## Variety notes

Not a WP. D=0 is the named `du_over_u` mix (old easy). Mid D is `exp_chain`. High D is `challenging` ∩ ln/exp (six implemented builders). Do not invent a new exp-of-log / Weierstrass core. D=16 and D=22 share the hard preset (intentional skip of a fourth EMH band).

## Limitations

- **Status:** skipped further leftover lockout — live already stamps `form_id` + `generator=integral_log_exp_substitution`; EMH presets already drop `du_over_u_trig` at D≥16. Remaining `LIMITATIONS`: D=0 majority `du_over_u_trig` (`d_min=6`, no `d_max`; `select_form_id` fallback at D=0); D=16 and D=22 are the same `challenging` mix (cubic/quartic leftover stays at expert); reverse-chain nested F∘g still richer than §5.6 drills when `u_sub_construction=auto` at format_tier≥1 (live 40-seed stayed catalog); BC-bank §1 ln/exp families unlock via named `bc_bank`, not the hard default; named showcases `u_sub_preset_*` / `u_sub_reverse_chain_ln_exp` stay full family.
- **Live pairwise:** each item stamps `form_id`, `generator=integral_log_exp_substitution`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `integral_log_exp_substitution`

## Proposed engine (reuse vs new)

- **Reuse:** existing `_sample_u_sub_derivative_backed` flavor `ln_exp` + `u_substitution.json` presets (`du_over_u`, `exp_chain`, `challenging`, `bc_bank`) + reverse-chain. Depth = document skip, not a new exclusive-band overlay on named presets.
- **Not this pass:** exclusive leftover bands; new expert EMH preset; locking `du_over_u_trig` out of D=0 (that *is* the easy named mix).
