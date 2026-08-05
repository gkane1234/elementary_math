# Continuous-D migration batch (2026-07-28)

Moved these catalog types from EMH-only / thin-wrapper buckets to continuous
``difficulty`` in the settings schema, with generator wiring:

| type_id | change |
|---------|--------|
| `scientific_notation_write` | `scientific_notation_profile` + D→exp/mantissa/normalize knobs |
| `scientific_notation_operations` | same |
| `scientific_notation_add_subtract` | same |
| `g6_writing_numeric_expressions` | profile + D→expression_complexity |
| `writing_numeric_expressions` | same |
| `verbal_expressions` | `algebra_expression_profile` now exposes continuous D (generator already used it) |
| `pa_verbal_expressions` | same |
| `g6_writing_algebraic_expressions` | same |

Bucket audit (`scripts/output/_continuous_d_buckets.json`) updated to
`already_continuous` for the rows above.

### Algebra 1 follow-on batch (same day)

| type_id / profile | change |
|-------------------|--------|
| `rational_add_subtract`, `rational_multiply`, `rational_divide` | Audit → `already_continuous` (schema+`RationalFramework` already live) |
| `percents`, `percent_of_change` | Audit → `already_continuous` (schema+`PercentFramework` already live) |
| `polynomial_settings` | Added `continuous_difficulty_settings`; drives `primitive_polynomial` / `build_context` |
| `properties_of_exponents` | Continuous exponent bounds + pattern unlock ladder in `misc.py` |

Skipped: geo trig, hard stats/sets, graph scaffolds, radical/quadratic new generators.

A1 mine→score→export plan: [`A1_DIFFICULTY_ROADMAP.md`](A1_DIFFICULTY_ROADMAP.md).
Stub export type list (no `--algebra-1` flag; avoids PA conflict on
`export_generation_dataset.py`): [`a1_export_types.json`](a1_export_types.json).

### Pre-Algebra first tranche (same day)

| type_id | change |
|---------|--------|
| `pa_converting_fractions_and_decimals` | F↔D-only path uses continuous FDP banks (`_build_fd_prompt`) |
| `pa_squares_and_square_roots` | continuous D in schema + D→base/form ladder |

PA effort scorers + `--pre-algebra` export + forward/inverse:
[`PA_DIFFICULTY_TRANCHE.md`](PA_DIFFICULTY_TRANCHE.md),
[`../topic_fit/pa_difficulty/TRACKING.md`](../topic_fit/pa_difficulty/TRACKING.md).

Remaining high-value migration targets (from bucket audit): leftover
`extend_primitive` / `new_generator` **generator ladders** (schema continuous is
already universal via `common_enrichment`); see `LINEAR_TO_POLY_PLAN.md` and the
A1 / A2 roadmaps. PA: algebra scorers, divisibility ladder, markup WP fix, hard
geo deferrals.

### Universal continuous-D schema (2026-07-28, hard requirement)

| Change | detail |
|--------|--------|
| `common_enrichment_profile` | Adds `continuous_difficulty_settings` alongside legacy `difficulty_tier` |
| Domain profiles | equation / inequality / graphing / systems / radical / quadratic / variation / relations / number_sets / number_line / coordinate_geometry / sequence / polynomial_division |
| EMH presets | `_COMMON_TERMS` seeds `difficulty` 3/8/14 for tier-only clients |
| Verification | All 84 A1 + 144 A2 catalog types expose numeric `difficulty` |
| Docs | [`A1_DIFFICULTY_ROADMAP.md`](A1_DIFFICULTY_ROADMAP.md), [`A2_DIFFICULTY_TRANCHE.md`](A2_DIFFICULTY_TRANCHE.md) |


### Precalculus + Calculus (same day)

**Hard rule:** every PC/Calc catalog type exposes continuous numeric
``difficulty`` (profile-level ``continuous_difficulty_settings``; scaffolds
included). Docs: [`PRECALC_DIFFICULTY_TRANCHE.md`](PRECALC_DIFFICULTY_TRANCHE.md),
[`CALC_DIFFICULTY_TRANCHE.md`](CALC_DIFFICULTY_TRANCHE.md).

| Area | change |
|------|--------|
| Profiles | continuous D on trig/log/exp/limits/derivatives/integrals + graphing/relations/linear/coordinate_plane/quadratic_graph/exponential_graph/absolute_value_graph/polynomial_division/equation |
| Generators | D→knobs via `apply_*_continuous_knobs`; EMH ladders via `settings_difficulty_band` |
| Scorers | `question_engine/ml/effort_calc.py` (registered from `effort.py`) |
| Export | `precalc_export_types.json` / `calc_export_types.json` + `--precalculus` / `--calculus` |
| Forward | precalc r≈0.97 RMSE≈0.70; calc r≈0.96 RMSE≈0.87 |
