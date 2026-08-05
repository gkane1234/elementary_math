# Precalculus difficulty learning — continuous-D tranche

**Date:** 2026-07-28

## Hard requirement

Every Precalculus catalog type exposes continuous numeric ``difficulty``
(not EMH-only). Scaffold / diagram types included (`scaffold` generator config).

## OpenStax mine

Stage-1 inventories (priority sections):
[`scripts/output/example_mining/precalculus-2e/stage1/INDEX.md`](../example_mining/precalculus-2e/stage1/INDEX.md)

| Chapters | Coverage |
|----------|----------|
| 1 | Functions 1.1–1.7 |
| 4 | Exp/log 4.1–4.8 |
| 5–6 | Trig foundations + graphs / inverse |
| 7 | Identities + solving equations 7.1–7.5 |

**27 sections · 2280 inventoried items.**

## Continuous-D wiring

Profile-level ``continuous_difficulty_settings`` added/confirmed on families used by PC:

- `trigonometry`, `logarithm`, `exponential`, `limits`, `derivatives`, `integrals`
- Graph / plane: `graphing`, `relations`, `linear`, `coordinate_plane`, `quadratic_graph`, `exponential_graph`, `absolute_value_graph`, `polynomial_division`, `equation`
- Explicit `scaffold` generator config with continuous D

Knob maps (when continuous D present; EMH / explicit knobs otherwise):

| Family | Behavior |
|--------|----------|
| Limits / power poly calc | `apply_calculus_continuous_knobs` → term_count / power / coef / approach |
| Log evaluate | `apply_logarithm_continuous_knobs` → base unlock, ln/log10, argument size |
| Trig evaluate | `apply_trigonometry_continuous_knobs` → tan/cot unlock, angle span |
| EMH-tier derivative rules | `_difficulty_tier` → `settings_difficulty_band` |

Bucket audit: all 94 PC rows → `already_continuous`.

## Effort scorers (`question_engine/ml/effort_calc.py`)

Registered from `effort.py` via `register_precalc_calc_scorers`.

| Scorer family | Example type_ids |
|---------------|------------------|
| `effort_log_evaluate` / `effort_trig_evaluate` / `effort_exp_equation` | log / trig / exp core |
| `effort_limit` / `effort_derivative_*` / `effort_integral_*` | intro-calc |
| `effort_trig_identity` / `effort_inverse_trig` / LoS–LoC / graph-trig | identities + laws |
| `effort_vector` / `effort_polar` / `effort_conic_pc` | vectors, polar, conics |
| `effort_poly_zeros_writing` / rational / partial fractions | poly advanced |
| `effort_counting_pc` / perm-comb / probability / binomial | discrete |
| `effort_fn_analysis_pc` / parametric / interest / induction | functions + misc |

Tests: `question_engine/tests/test_precalc_calc_effort_difficulty.py`.

## ML pipeline

| Step | Path | Result |
|------|------|--------|
| Export `--precalculus` | `precalc_labeled_tranche.jsonl` | **8370** rows / **8370** labeled / 0 errors (**93** types × 6 D × 15) |
| Forward train | `precalc_forward_effort_model.{json,pkl}` | GBR RMSE ≈ **1.13**, Pearson r ≈ **0.94** |
| Type list | `precalc_export_types.json` | **94** types (includes `pc_vectors_diagrams`); load via `--precalculus` |

## Coverage / blockers

**Schema continuous-D:** 94/94 PC types.

**Effort scorers:** **94**/94 catalog types scored.

**Labeled export:** **93** types in `precalc_labeled_tranche.jsonl` (pre–`pc_vectors_diagrams`).
Export type list is ready for a 94-type re-export.

**Formerly unscored (now scored):**

- `pc_vectors_diagrams` — real `vector_diagrams` tip-to-tail / resultant / opposite stems + `effort_vector_diagram` (no longer scaffold)

## Next

1. Optional full re-export + retrain including `pc_vectors_diagrams` (n_per=15).
2. Stage-2 family tags on OpenStax mine.
3. Inverse difficulty pilots on log-eval / power-rule / limits.
