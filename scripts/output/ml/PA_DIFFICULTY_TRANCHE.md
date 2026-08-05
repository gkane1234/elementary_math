# Pre-Algebra difficulty learning — first + second tranche

**Date:** 2026-07-28 (updated integration)

## OpenStax mine cross-link

Stage-1 inventories (Ch 3–6): [`scripts/output/example_mining/prealgebra-2e/stage1/INDEX.md`](../example_mining/prealgebra-2e/stage1/INDEX.md)

Use that INDEX for section → PA `type_id` mappings and non-magnitude effort drivers. Scorer alignment notes below.

### Scorer ↔ OpenStax effort-driver alignment

| OpenStax section | PA type_id(s) | Scorer | Aligns? | Notes |
|---|---|---|---|---|
| 3.2 / 3.3 Add/subtract integers | `pa_integers_adding_and_subtracting` | `effort_integer_ops` | **mostly** | Unlike signs + digit work yes; 3+ addends / applications not fully modeled |
| 3.4 Mul/div integers | `pa_integers_{multiplying,dividing}` | `effort_integer_ops` | **yes** | Signs + non-int quotient; multi-factor products thin |
| 4.1 / simplify | `pa_simplifying_fractions` | `effort_simplify_fractions` | **yes** | Meaningful cancel steps (Ω), not |n| |
| 4.2 ×÷ fractions | `pa_fractions_{multiply,divide}` | `effort_fraction_ops` | **yes** (new) | Cancel-before-multiply + reciprocal ÷; mixed/complex still **missing** |
| 4.4 / 4.5 ± fractions | `pa_fractions_{add,subtract}_{like,unlike}` | `effort_fraction_ops` | **yes** (new) | Like vs LCD; 3+ terms thin |
| 4.3 / 4.6 mixed numbers | — | — | **gap** | No PA catalog leaf / generator |
| 5.1 Decimals name/round | `pa_naming_*`, `pa_writing_*` | place / words | **yes** | Place depth + magnitude bands |
| 5.3 F↔D | `pa_converting_fractions_and_decimals` | `effort_fraction_decimal_convert` | **yes** | Terminating-awkward banks |
| 6.1 FDP | `pa_fractions_decimals_and_percents` | `effort_relating` | **yes** | Conversion triad |
| 6.3 Tax/discount | `pa_markup_discount_and_tax` | `effort_markup_discount` | **ready** | Narrative `PercentWordProblemFramework` (`wp_percent` unblocked) |
| 6.4 Simple interest | `pa_simple_and_compound_interest` | `effort_interest` | **partial mismatch** | Compound / horizon yes; **solve-for-P/r/t** not distinguished (OpenStax Example 6.34 ≈ same score as earn-interest) |

### Spot-checks (OpenStax stems → `score_effort`)

Not expected to be perfect matches — directional only.

| Stem (paraphrased from mine) | type_id | y_effort | Observation |
|---|---|---|---|
| `5 + 3` vs `-15 + (-7)` (Ex 3.14 / 3.18-ish) | `pa_integers_adding_and_subtracting` | 2.0 → 6.5 | Unlike / both-negative raises effort as intended |
| Simplify `10/15` vs `-56/32` (Ex 4.19 / 4.21) | `pa_simplifying_fractions` | 6.5 → 14.0 | More cancel steps → higher effort |
| Simple interest earn \$500 @ 6% / 3y vs solve-for-principal (Ex 6.33 / 6.34) | `pa_simple_and_compound_interest` | 6.0 / 6.0 | **Mismatch** — ask-kind not detected |
| Multiply `3/4 · 1/5` vs `-14/15 · 20/21` (§4.2) | `pa_fractions_multiply` | cancel raises score | Aligns with cancel-before-multiply driver |

## Bucket inventory (41 original PA types + 6 fraction aliases)

From `scripts/output/_continuous_d_buckets.json` (pre-alias audit):

| Bucket | Count | Examples |
|---|---|---|
| `knob_retarget` | 12 | integers ±×÷, factoring, GCF/LCM, simplify, F↔D, FDP, interest, place/words |
| `already_continuous` | 15 | equations WP, multi-step eq/ineq, proportions, systems, polys, slope, markup* |
| `new_generator` | 2 | `pa_divisibility`, `pa_squares_and_square_roots` |
| `extend_primitive` | 3 | similar figures (± WP), plotting points |
| `hard` | 9 | plane/solid geometry, transformations, Pythagorean |

\* `pa_markup_discount_and_tax` is schema-continuous but **blocked** on topic fit (see below).

**New catalog aliases (second tranche):** `pa_fractions_{add,subtract}_{like,unlike}`, `pa_fractions_multiply`, `pa_fractions_divide` → `g6_fraction_*` generators + `rational` profile.

## Migrated this tranche

### Continuous-D wiring
- **`pa_converting_fractions_and_decimals`**: non-percent F↔D path now uses the same easy/medium/hard terminating-decimal banks as FDP, keyed by continuous `difficulty` (`FractionDecimalConvertFramework._build_fd_prompt`).
- **`pa_squares_and_square_roots`**: continuous `difficulty` added to settings schema; generator maps D → base range / perfect-only / extract forms.
- Explicit PA type_id rows in `generator_profiles.py` for aliases (integers ×÷, factoring, GCF/LCM, simplify, F↔D, place, words, divisibility, **fraction ±×÷**).

### Already working (verified generate @ D=0/12/25)
All 12 `knob_retarget` types already exposed continuous `difficulty` via shared `integer` / `factor` / `rational` / `decimal` / `percent` / `word_problem` profiles. Smoke generation succeeded for each.

## Effort scorers (`question_engine/ml/effort.py`)

### First tranche (13)

| Scorer | type_ids |
|---|---|
| `effort_integer_ops` | `pa_integers_{adding_and_subtracting,multiplying,dividing}` |
| `effort_factoring` | `pa_factoring`, `g6_factoring` |
| `effort_gcf` | `pa_greatest_common_factor`, `g6_greatest_common_factor` |
| `effort_lcm` | `pa_least_common_multiple`, `g6_least_common_multiple` |
| `effort_simplify_fractions` | `pa_simplifying_fractions` |
| `effort_fraction_decimal_convert` | `pa_converting_fractions_and_decimals` |
| `effort_relating` (alias) | `pa_fractions_decimals_and_percents` |
| `effort_interest` | `pa_simple_and_compound_interest` |
| `effort_place_value_rounding` | `pa_naming_decimal_places_and_rounding` |
| `effort_writing_numbers_words` | `pa_writing_numbers_with_words` |
| `effort_squares_roots` | `pa_squares_and_square_roots` |

### Second tranche (20)

| Scorer | type_ids |
|---|---|
| `effort_fraction_ops` | `pa_fractions_{add,subtract}_{like,unlike}`, `pa_fractions_{multiply,divide}` |
| `effort_equations` | `pa_equations_{one,two}_step_word_problems`, `pa_equations_multi_step_equations`, `pa_multi_step_inequalities` |
| `effort_proportions` | `pa_checking_for_a_proportion`, `pa_proportions_word_problems` |
| `effort_slope` | `pa_slope` |
| `effort_linear_write` | `pa_writing_linear_equations` |
| `effort_systems` | `pa_graphing_systems_of_equations`, `pa_systems_substitution`, `pa_systems_word_problems` |
| `effort_polynomials` | `pa_polynomials_{simplifying,adding_and_subtracting,multiplying}` |

Tests: `question_engine/tests/test_pa_effort_difficulty.py`.

## ML pipeline outputs

| Step | Path | Result |
|---|---|---|
| Export first tranche `--pre-algebra` (earlier) | `scripts/output/ml/pa_first_tranche.jsonl` | 1170 rows, 1170 labeled, 0 errors |
| Forward train (first) | `scripts/output/ml/pa_forward_effort_model.{json,pkl}` | GBR RMSE ≈ **1.45**, Pearson r ≈ **0.95** |
| Inverse pilot | `scripts/output/ml/pa_inverse_difficulty.json` | `pa_simplifying_fractions` ladder |
| Export expanded (smoke) | `scripts/output/ml/pa_expanded_tranche.jsonl` | smoke: **297** rows / **297** labeled (n_per=3, diffs 0/12/25) → r ≈ **0.86** |
| **Export expanded full** | `scripts/output/ml/pa_expanded_tranche.jsonl` | **2970** rows, **2970** labeled, 0 errors (n_per=15, diffs 0/5/…/25; 33 types) |
| **Forward retrain (full)** | `scripts/output/ml/pa_forward_effort_model.{json,pkl}` | GBR **n=2970** → train 2376 / test 594; RMSE ≈ **1.51**, Pearson r ≈ **0.94** |
| A1 labeled `--algebra-1` | `scripts/output/ml/a1_labeled_tranche.jsonl` | **4860** rows / **4860** labeled (54 types, n_per=15); forward RMSE ≈ **1.78**, r ≈ **0.94** |

Tracking scaffold: `scripts/output/topic_fit/pa_difficulty/TRACKING.{md,json}`

## Remaining gaps

### Unblocked (generator fixed)
- **`pa_markup_discount_and_tax`** (`wp_percent`): narrative markup/discount/tax/tip via `PercentWordProblemFramework`. Scorer registered; include in next PA re-export if desired.

### Still missing from mine
- Mixed-number arithmetic (OpenStax 4.3 ×÷, 4.6 ±) — no generator
- Dedicated fraction/decimal coefficient equation modes (4.7, 5.4) — folded into multi-step
- Decimal ops as PA surface (5.2) — live on G6 only

### extend_primitive
- `pa_similar_figures`, `pa_similar_figures_word_problems`, `pa_plotting_points`

### new_generator / structural
- **`pa_divisibility`**: continuous schema via `factor` profile; sampling still magnitude-only — needs divisor/rule ladder + scorer.

### hard (geometry deferrals)
- `pa_drawing_and_measuring_angles`, `pa_angle_relationships`, `pa_plane_figures_triangles`, `pa_quadrilaterals`, `pa_area_of_triangles_and_quadrilaterals`, `pa_circles`, `pa_transformations`, `pa_classifying_volume_and_surface_area`, `pythagorean_theorem`

### A1 effort scorers
See [`A1_DIFFICULTY_ROADMAP.md`](A1_DIFFICULTY_ROADMAP.md). First + second family batches registered
(rational ±×÷, percents, sci-notation, verbal/OOO, equations, proportions, exponents, polys, rational simplify).

## Commands

```powershell
$env:PYTHONPATH='.'
python scripts/export_generation_dataset.py --pre-algebra --n-per 15 --out scripts/output/ml/pa_expanded_tranche.jsonl
python scripts/train_forward_effort_model.py --data scripts/output/ml/pa_expanded_tranche.jsonl --out scripts/output/ml/pa_forward_effort_model
python scripts/optimize_inverse_difficulty.py --model scripts/output/ml/pa_forward_effort_model --type-id pa_simplifying_fractions --out scripts/output/ml/pa_inverse_difficulty.json
python scripts/export_generation_dataset.py --algebra-1 --n-per 15 --out scripts/output/ml/a1_labeled_tranche.jsonl
python scripts/train_forward_effort_model.py --data scripts/output/ml/a1_labeled_tranche.jsonl --out scripts/output/ml/a1_forward_effort_model
python -m pytest question_engine/tests/test_pa_effort_difficulty.py question_engine/tests/test_a1_effort_difficulty.py -q
```
