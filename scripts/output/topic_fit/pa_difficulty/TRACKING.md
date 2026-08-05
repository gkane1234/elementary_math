# Pre-Algebra continuous-difficulty TRACKING

**Date:** 2026-07-28 (second tranche integration)  
**Catalog types:** 47 (`question_engine/catalogs/pre_algebra.py` — 41 prior + 6 fraction aliases)  
**First tranche:** 13 types with continuous D + effort scorers + GenerationRecord export  
**Second tranche:** 20 types (6 fraction aliases + 14 already_continuous algebra/linear/polys)

## Summary counts

| Status | Count |
|---|---|
| verified_ramp (first tranche) | 13 |
| second tranche scorers registered | 20 |
| weak_ramp | 0 (first); second ramp QA pending expanded export |
| failed_ramp | 0 |
| blocked (outside export) | 1 (`pa_markup_discount_and_tax`) |
| **total with scorers** | **33** |

## First tranche type_ids

| type_id | bucket (audit) | status | notes |
|---|---|---|---|
| `pa_naming_decimal_places_and_rounding` | knob_retarget → continuous | verified_ramp | place ladder already continuous |
| `pa_writing_numbers_with_words` | knob_retarget | verified_ramp | magnitude / reverse ladder |
| `pa_integers_adding_and_subtracting` | knob_retarget | verified_ramp | `IntegerArithmeticFramework` |
| `pa_integers_multiplying` | knob_retarget | verified_ramp | aliases `g6_integer_multiply` |
| `pa_integers_dividing` | knob_retarget | verified_ramp | non-int quotient ramp |
| `pa_factoring` | knob_retarget | verified_ramp | aliases `g6_factoring` / Ω effort |
| `pa_greatest_common_factor` | knob_retarget | verified_ramp | aliases G6 GCF |
| `pa_least_common_multiple` | knob_retarget | verified_ramp | aliases G6 LCM |
| `pa_simplifying_fractions` | knob_retarget | verified_ramp | meaningful cancel steps |
| `pa_converting_fractions_and_decimals` | → already_continuous | verified_ramp | F↔D banks wired to continuous D |
| `pa_fractions_decimals_and_percents` | knob_retarget | verified_ramp | aliases `effort_relating` |
| `pa_simple_and_compound_interest` | knob_retarget | verified_ramp | compound / rate / horizon; ask-kind mismatch vs OpenStax |
| `pa_squares_and_square_roots` | → already_continuous | verified_ramp | continuous schema + form ladder |

## Second tranche type_ids

| type_id | source | scorer | status |
|---|---|---|---|
| `pa_fractions_add_like` | alias → `g6_fraction_add_like` | `effort_fraction_ops` | wired + scorer |
| `pa_fractions_subtract_like` | alias → `g6_fraction_subtract_like` | `effort_fraction_ops` | wired + scorer |
| `pa_fractions_add_unlike` | alias → `g6_fraction_add_unlike` | `effort_fraction_ops` | wired + scorer |
| `pa_fractions_subtract_unlike` | alias → `g6_fraction_subtract_unlike` | `effort_fraction_ops` | wired + scorer |
| `pa_fractions_multiply` | alias → `g6_fraction_multiply` | `effort_fraction_ops` | wired + scorer |
| `pa_fractions_divide` | alias → `g6_fraction_divide` | `effort_fraction_ops` | wired + scorer |
| `pa_equations_one_step_word_problems` | already_continuous | `effort_equations` | scorer |
| `pa_equations_two_step_word_problems` | already_continuous | `effort_equations` | scorer |
| `pa_equations_multi_step_equations` | already_continuous | `effort_equations` | scorer |
| `pa_multi_step_inequalities` | already_continuous | `effort_equations` | scorer |
| `pa_checking_for_a_proportion` | already_continuous | `effort_proportions` | scorer |
| `pa_proportions_word_problems` | already_continuous | `effort_proportions` | scorer |
| `pa_slope` | already_continuous | `effort_slope` | scorer |
| `pa_writing_linear_equations` | already_continuous | `effort_linear_write` | scorer |
| `pa_graphing_systems_of_equations` | already_continuous | `effort_systems` | scorer |
| `pa_systems_substitution` | already_continuous | `effort_systems` | scorer |
| `pa_systems_word_problems` | already_continuous | `effort_systems` | scorer |
| `pa_polynomials_simplifying` | already_continuous | `effort_polynomials` | scorer |
| `pa_polynomials_adding_and_subtracting` | already_continuous | `effort_polynomials` | scorer |
| `pa_polynomials_multiplying` | already_continuous | `effort_polynomials` | scorer |

## ML artifacts

| Artifact | Path |
|---|---|
| Export JSONL (first) | `scripts/output/ml/pa_first_tranche.jsonl` |
| Export summary (first) | `scripts/output/ml/pa_first_tranche.summary.json` |
| Export JSONL (expanded) | `scripts/output/ml/pa_expanded_tranche.jsonl` (297 labeled smoke) |
| A1 stub export | `scripts/output/ml/a1_continuous_stub.jsonl` (144 rows, y_effort null) |
| Forward model (first-tranche train) | `scripts/output/ml/pa_forward_effort_model.json` (+ `.pkl`) |
| Inverse pilot | `scripts/output/ml/pa_inverse_difficulty.json` (`pa_simplifying_fractions`) |
| Tranche notes | `scripts/output/ml/PA_DIFFICULTY_TRANCHE.md` |
| OpenStax mine INDEX | `scripts/output/example_mining/prealgebra-2e/stage1/INDEX.md` |
| A1 roadmap / export types | `scripts/output/ml/A1_DIFFICULTY_ROADMAP.md`, `a1_export_types.json` |

## Forward model metrics (GBR) — first tranche only

- n_train / n_test: 936 / 234  
- RMSE ≈ 1.45  
- Pearson r ≈ 0.95  
- **Expanded retrain: pending** (smoke export done at n_per=3; run full export then `train_forward_effort_model.py`)

## Remaining PA (outside scored set)

See `scripts/output/ml/PA_DIFFICULTY_TRANCHE.md` for mixed-number missing, extend_primitive, hard geo, and blocked `pa_markup_discount_and_tax`.

## Next verification batches

| Batch | Focus | Status |
|---|---|---|
| 0 | First tranche (13) | scaffold + export/train done |
| 1 | Fraction aliases + already_continuous algebra | scorers + wiring done; expanded export/retrain pending |
| 2 | extend_primitive (similar figures, plotting) | pending |
| 3 | hard geo (angles, area, solids, Pythagorean) | deferred |
| 4 | `pa_divisibility` structural ladder | pending |
| 5 | Fix `pa_markup_discount_and_tax` (`wp_percent` stubs) | blocked |
| 6 | Mixed-number ±×÷ (OpenStax 4.3 / 4.6) | missing generators |
| 7 | A1 effort scorers | see A1_DIFFICULTY_ROADMAP; `--algebra-1` export ready |
