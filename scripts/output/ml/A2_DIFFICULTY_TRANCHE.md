# Algebra 2 difficulty learning — labeled spine

**Date:** 2026-07-28

## Hard requirement: continuous numeric difficulty

Every Algebra 2 catalog leaf exposes continuous ``difficulty`` in the settings
schema (via ``common_enrichment`` + domain profiles). Scaffold / ``hard`` /
``new_generator`` types still show the field; ladders may be coarse until
generator wiring catches up. Legacy ``difficulty_tier`` remains for EMH preset
fallback (hidden in UI when continuous D is present).

## OpenStax mine

Stage-1 inventories (priority chapters):  
[`scripts/output/example_mining/intermediate-algebra-2e/stage1/INDEX.md`](../example_mining/intermediate-algebra-2e/stage1/INDEX.md)

Covered: Ch 2 (eq/ineq), 5–6 (polys/factoring), 7 (rationals), 8 (radicals),
9 (quadratics), 10 (exp/log).

## Bucket inventory (145 A2 types)

From `scripts/output/_continuous_d_buckets.json` after schema-continuous flip of
thin / knob_retarget / already_or_thin:

| Bucket | Count | Notes |
|--------|------:|-------|
| `already_continuous` | 52 | Schema continuous; includes easy-win flips |
| `new_generator` | 54 | Graph UX, conics, sequences, … |
| `extend_primitive` | 19 | 3-var systems, WP adapters, … |
| `hard` | 19 | Conics writing, classify, variation, … |

**Schema check:** 0 A2 types missing continuous ``difficulty`` field.

## Effort scorers

Registered A2 aliases in `question_engine/ml/effort.py` (shared A1/PA/G6/PC stems
plus dedicated quadratic / radical / exp-log / gap-fill / thin-leaf / final-gap
scorers):

| Family | example type_ids | Scorer |
|--------|------------------|--------|
| Multi-step eq/ineq | `a2_…_multi_step_equations`, `…_multi_step_inequalities` | `effort_equations` |
| Literal equations | `a2_…_literal_equations` | `effort_literal_equations` (A1 generator) |
| Compound / abs | `a2_…_compound_inequalities`, `…_absolute_value_*` | `effort_compound_inequalities` / `effort_absolute_value` |
| Linear write | `a2_…_writing_linear_equations` | `effort_linear_write` |
| Graph UX (parseable) | linear / abs / quad / radical / rational / exp / log / trig | `effort_graph_linear(_equation)` / `effort_graph_transform` / `effort_graph_trig` |
| Relations UX | discrete / continuous relations | `effort_relations` |
| Systems (2-var) | substitution / elimination / graphing / WP | `effort_systems` |
| Systems (3-var) / planes / 3D points | `…_three_variables`, `…_planes`, `…_points_in_three_dimensions` | `effort_systems_three`, `effort_planes`, `effort_points_3d` |
| Factoring | quadratic / special / grouping / solve-by-factor | dedicated poly factor scorers |
| Quadratic methods | square roots / CTS / formula / discriminant / solve-by-graphing | quadratic scorers + `effort_solve_by_graphing` |
| Poly theory | binomial / remainder / Descartes / RZT / FTA / writing / end-behavior | dedicated poly-theory scorers |
| Rational simplify ± ×÷ / eqns / complex fractions | `a2_rational_expressions_*` | rational scorers |
| Radical ± ×÷ / simplify / eqns / domain–range | radical chapter leaves | `effort_radical_*`, `effort_radical_domain_range` |
| Exponent props | radical-chapter exponent leaves | `effort_properties_of_exponents` |
| Exp/log equations + evaluate | `a2_exponential_and_logarithmic_expressions_*` | `effort_a2_exp_equation`, `effort_a2_log_equation`, `effort_log_evaluate` |
| Growth–decay WP / inverses | discrete + continuous WP; exp/log inverses | `effort_growth_decay`, `effort_inverse_exp_log` |
| General function inverses | `a2_general_functions_inverses` | `effort_inverse_function` |
| Matrices | ops / det / inverse / Cramer / geometric transforms | `effort_matrix_*`, `effort_transformation` |
| Conics | circle/ellipse/hyperbola/parabola graph+write; classify; quadratic systems | `effort_conic`, `effort_quadratic_system` |
| Sequences / series | arithmetic / geometric nth + series + mean | `effort_sequence` |
| Trig evaluate | any-angle / radians / coterminal / eqns | `effort_trig_evaluate` (PC) |
| Law of sines / cosines / area | `a2_trigonometry_the_law_*`, `…_area_and_laws_*` | `effort_law_of_sines_cosines` |
| Complex | ops / graph / abs / rationalize | `effort_complex_ops` |
| Stats / counting | counting, indep/ME prob, perm/comb | `effort_stats_counting`, `effort_stats_probability`, `effort_stats_perm_comb` |
| Variation | `a2_direct_and_inverse_variation_*` | `effort_variation` (geo) |
| OOO | `a2_beginning_algebra_order_of_operations` | `effort_order_of_operations` |

Continuous-D ladders deepened for: graph transforms, growth/decay ask-modes,
trig graph structure, sequences, inverse exp/log shifts, matrices, conics,
systems/planes, complex entries, triangle laws, variation mix, counting n/r,
**relations slope/table rows, solve-by-graphing root/degree, poly theory
(binomial/Descartes/FTA/…), radical domain stretch/reflection**.

## ML pipeline

| Step | Path | Result |
|------|------|--------|
| Export `--algebra-2` n_per=15 | `a2_labeled_tranche.jsonl` | **13050** rows, **13050** labeled, 0 errors (**145** types) |
| Forward train | `a2_forward_effort_model` | GBR — RMSE ≈ **1.97**, Pearson r ≈ **0.91** (n_train 10440 / n_test 2610) |
| Inverse pilot | `a2_inverse_difficulty.json` | `a2_radical_functions_and_rational_exponents_radical_equations` |

Prior spines: 9450 / 105 types / r≈0.92 → 11430 / 127 types / r≈0.91 → **full catalog**.

```powershell
$env:PYTHONPATH='.'
python scripts/export_generation_dataset.py `
  --algebra-2 --n-per 15 --out scripts/output/ml/a2_labeled_tranche.jsonl
python scripts/train_forward_effort_model.py `
  --data scripts/output/ml/a2_labeled_tranche.jsonl `
  --out scripts/output/ml/a2_forward_effort_model
python scripts/optimize_inverse_difficulty.py `
  --model scripts/output/ml/a2_forward_effort_model `
  --type-id a2_radical_functions_and_rational_exponents_radical_equations `
  --out scripts/output/ml/a2_inverse_difficulty.json
```

Type list: [`a2_export_types.json`](a2_export_types.json).

## Remaining gaps

| Area | Status |
|------|--------|
| A2 literal equations alias | **done** |
| Exp/log growth–decay WP / inverses / graph UX | **done** (scorers + continuous ladders) |
| Conics / matrices / trig / sequences | **done** for wired generators |
| 3-var systems / planes / law of sines/cosines / complex / stats / variation | **done** |
| Relations UX / 3D points / geometric transforms / solve-by-graphing | **done** |
| Binomial / remainder / Descartes / RZT / FTA / poly writing / end-behavior | **done** |
| General inverses / radical domain–range / parabola write / quadratic systems | **done** |
| **Effort scorers** | **145 / 145** catalog leaves labeled — **0 remaining** |
| Inverse difficulty ladder | **pilot done** (`a2_inverse_difficulty.json`) — predicted effort band still narrow (~8–9) for some types |
| Area leaf still wired to `law_of_sines` (not dedicated area generator) | catalog debt |
| Some continuous ladders still coarse (FTA is degree-only; 3D points are echo stems) | generator depth debt |
| **Precalculus / Calculus** | spines done separately — see tranche docs |

See also [`A1_DIFFICULTY_ROADMAP.md`](A1_DIFFICULTY_ROADMAP.md), [`CONTINUOUS_D_MIGRATION.md`](CONTINUOUS_D_MIGRATION.md),
[`PRECALC_DIFFICULTY_TRANCHE.md`](PRECALC_DIFFICULTY_TRANCHE.md), [`CALC_DIFFICULTY_TRANCHE.md`](CALC_DIFFICULTY_TRANCHE.md).
