# Calculus difficulty learning — continuous-D tranche

**Date:** 2026-07-28

## Hard requirement

Every Calculus catalog type exposes continuous numeric ``difficulty``
(not EMH-only), including foundations / thin scaffolds.

## OpenStax mine

| Book | Stage-1 INDEX | Sections | Items |
|------|---------------|---------:|------:|
| Calculus Volume 1 | [`…/calculus-volume-1/stage1/INDEX.md`](../example_mining/calculus-volume-1/stage1/INDEX.md) | 34 (chs 2–6 core) | 2150 |
| Calculus Volume 2 | [`…/calculus-volume-2/stage1/INDEX.md`](../example_mining/calculus-volume-2/stage1/INDEX.md) | 10 (∫ + volumes) | 734 |
| Calculus Volume 3 | [`…/calculus-volume-3/stage1/INDEX.md`](../example_mining/calculus-volume-3/stage1/INDEX.md) | 6 (parametric/polar/vectors) | 457 |

Vol 1 extends beyond the §§2.1–2.3 pilot through derivatives, applications, and integration.

## Continuous-D wiring

Same profile-level continuous D as precalc for `limits` / `derivatives` / `integrals`
(plus shared graph/equation profiles where reused).

| Generator path | Continuous behavior |
|----------------|---------------------|
| `calculus_params_from_settings` | D→ term/power/coef/approach knobs |
| `calculus.py` + `calculus_derivative_rules.py` `_difficulty_tier` | D→ easy/medium/hard family ladder via `settings_difficulty_band` |

Bucket audit: all 64 Calc rows → `already_continuous`.

## Effort scorers (`question_engine/ml/effort_calc.py`)

| Scorer family | Example type_ids |
|---------------|------------------|
| `effort_limit` | direct / jump / removable / essential / infinity / continuity |
| `effort_derivative_power` / `effort_derivative_rules` | power + product/quotient/chain/trig/ln-exp |
| `effort_def_of_derivative` / `effort_implicit_log_diff` / table | definition, implicit, log-diff, inverse |
| `effort_curve_analysis_calc` / `effort_lhopital` / motion | Rolle/MVT/extrema/opt/Newton/L'Hôpital |
| `effort_integral_*` / `effort_ibp_sub_integral` / `effort_definite_ftc` | indef + sub + IBP + FTC |
| `effort_area_volume` / `effort_diff_eq` | area/volumes + DE |

## ML pipeline

| Step | Path | Result |
|------|------|--------|
| Export `--calculus` | `calc_labeled_tranche.jsonl` | **5760** rows / **5760** labeled / 0 errors (**64** types × 6 D × 15) |
| Forward train | `calc_forward_effort_model.{json,pkl}` | GBR RMSE ≈ **1.22**, Pearson r ≈ **0.93** (n_train 4608 / n_test 1152) |
| Type list | `calc_export_types.json` | Load via `--calculus` |

## Coverage / blockers

**Schema continuous-D:** 64/64 Calc types.

**Labeled scorers this tranche:** **64** export types (full catalog — all have scorers).

**Thin stems still worth upgrading later:**

- `calc_app_diff_curve_sketching` / graphical comparison (currently power-rule stubs)
- Table / slope-field UX when richer generators land
- Stage-2 EMH tagging on Vol 1 Ch 3–5 mine

## Next

1. Richer curve-sketch / f–f'–f'' comparison prompts (replace stubs).
2. Stage-2 EMH tagging on Vol 1 Ch 3–5 mine.
3. Inverse ladders for power / product / chain / FTC.
