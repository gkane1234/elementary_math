# Grade-level consistency QA

Date: 2026-07-12

## Wave 1 — Wrong-skill rewires

| type_id | Was | Now |
|---------|-----|-----|
| G6 decimal diagram / area / whole÷decimal | fraction gens | decimal / `g6_whole_by_decimal_divide` |
| `pa_naming_decimal_places_and_rounding` | `polynomial_naming` | `place_value_and_rounding` |
| `pa_writing_numbers_with_words` | `verbal_expressions` | `writing_numbers_with_words` |
| `pa_integers_*` | `rational_*` | `g6_integer_*` |
| `pa_simplifying_fractions` | `rational_simplification` | `simplifying_numeric_fractions` |
| `a2_complex_numbers_rationalizing_denominators` | `radical_simplification` | `complex_rationalize_denominator` |
| A2 sum/double-angle identities | `trig_basic_identities` | `trig_sum_difference` / `trig_multiple_angle` |
| `geo_trig_trigonometry_and_area` | `geo_triangle_area` | `trigonometry_and_area` (½ab sin C) |
| `scatter_plots` | `stats_histogram_read` | `scatter_plot_interpret` |
| Geo permutations / combinations | counting principle | `stats_permutations` / `combinations` |
| `g6_solutions_to_equations` | solve one-step | `check_equation_solution` |
| `g6_constant_rate_equations` / other relationships | two/multi-step solve | `write_one_step_equation` |
| `g6_distributive_property_algebraic` | numeric distributive | `distributive_property_algebraic` |
| `find_missing_sides_of_triangles` | Pythagorean | `geo_right_triangle_trig_side` |

## Wave 2 — Course-tiered presets

- Geo review radicals softer than A1; A2 radicals slightly harder.
- G6 order of operations / distributive / distance presets.
- PA integer ranges via `num_min`/`num_max`.
- A2/PC rational equations structurally harder than A1.
- Synced in `presets.py` and `lib/difficulty-presets.ts`.

## Wave 3 — Generator modes

- `axis_aligned_only` on `CoordinateDistanceFramework` (G6 distance).
- Algebraic distributive registered.
- Check/write equation generators for G6.

## Sample checks

- Geo review hard `coef_max` 5 < A2 hard 10; geo review radicand_max < A2.
- G6 distance samples are horizontal or vertical only.
- Rewired types emit topic-correct prompts (no √ under complex rationalize; no poly naming under place value).
- Verification script: 14 key type_ids PASS.

## PDF

Regenerated `scripts/output/all_types_examples.pdf` (589/589 E/M/H; ~6.4 MB; 2026-07-12).

## Still deferred

- True diagram UI for G6 decimal/area models (math is now decimal ops, not fractions).
- Richer scatter SVG (text association/prediction for now).
- See `scripts/output/DEFERRED.md`.
