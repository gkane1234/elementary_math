# Algebra 1 difficulty-learning roadmap

Prepared for the mine → score → export loop **after** Pre-Algebra first tranche.
Source of truth for catalog leaves: `question_engine/catalogs/algebra_1.py`.
Bucket audit: `scripts/output/_continuous_d_buckets.json` (A1 rows).

**Status (2026-07-28):** **73** labeled types / **6570** rows; forward r≈**0.91** RMSE≈**2.03**.
WP age/coin/consecutive/percent unblocked; graph UX abs / systems-ineq / quadratic /
exponential / solve-by-graphing + scatter / visualizing scored.
Still missing (no gens): quadratic apps (EA2e §10.4) / higher roots (§9.7) — do not invent.

## Bucket counts (Algebra 1, 86 types)

| Bucket | Count | Notes |
|--------|------:|-------|
| `already_continuous` | 53 | Includes enrichment/profile continuous-D for all leaves |
| `extend_primitive` | 9 | WP adapters, some quadratic/radical/rational extensions |
| `new_generator` | 17 | Functions, growth/decay, radicals, quadratic methods, trig sides |
| `hard` | 5 | Sets of numbers, variation, stats/diagram UX |
| `knob_retarget` | 0 | geo trig flipped or deferred |
| `thin_wrapper` | 0 | None on A1 |

**Hard requirement (2026-07-28):** every A1 catalog leaf exposes continuous numeric
`difficulty` (via `common_enrichment` + domain profiles). Scaffold/hard types still
show the field; ladders may be coarse. Legacy `difficulty_tier` remains for EMH
preset fallback (hidden in UI when continuous D is present).


## Recommended mine source

**OpenStax Elementary Algebra 2e** (`elementary-algebra-2e`)

- Local HTML under `textbooks/openstax/html/` (see `scripts/output/example_mining/README.md`)
- **Stage 1 inventories (2026-07-28):** [`scripts/output/example_mining/elementary-algebra-2e/stage1/`](../example_mining/elementary-algebra-2e/stage1/) — **55** priority sections (Ch 2, 4–10) with catalog `type_id` mappings + effort drivers in [`INDEX.md`](../example_mining/elementary-algebra-2e/stage1/INDEX.md)
- Section → prereq DAG: `scripts/example_mining/prerequisites/elementary-algebra-2e.json`
- Spine context: `scripts/output/example_mining/progression/g6_prealg_alg1.*`
- Gaps / unwired leaves: `scripts/output/curriculum_gaps/algebra_1.md`

Mine → paraphrase stems → effort features → register scorers → export JSONL
(same pattern as G6 ratios / PA first tranche). Prefer Elementary Algebra chapter
order over catalog “Pre-Algebra — …” shared leaves when labeling A1 families.

### EA2e mining follow-ups applied (2026-07-28)

From [`INDEX.md`](../example_mining/elementary-algebra-2e/stage1/INDEX.md) highest-priority list:

| Follow-up | Status |
|-----------|--------|
| A1 aliases → PA `effort_slope` / `effort_linear_write` / `effort_systems` | **done** (`slope`, `more_on_slope`, `writing_linear_equations`, `systems_*`) |
| Factoring beyond GCF (grouping / special / quadratic / general / factor-to-solve) | **done** (`effort_poly_grouping`, `effort_poly_special`, `effort_quadratic_factoring`, `effort_poly_general_strategy`, `effort_quadratic_factor_solve`) |
| Continuous `difficulty` on those type_ids | **checked** (linear / systems / graphing / quadratic / poly-factoring profiles) |
| Literals + inequality ladder (+ compound / abs) | **done** (`effort_literal_equations`, `effort_equations` aliases, `effort_compound_inequalities`, `effort_absolute_value`) |
| Rational ×÷ expressions + radical ± | **done** (`effort_rational_expression_ops`, `effort_radical_add_subtract`) |
| Quadratic methods beyond factoring (10.1–10.3) | **done** (`effort_quadratic_square_roots`, `effort_completing_square_*`, `effort_quadratic_formula`, `effort_quadratic_discriminant`) |
| Radical ×÷ / equations + rational equations | **done** (`effort_radical_multiply`, `effort_radical_divide`, `effort_radical_equations`, `effort_rational_equations`) |
| Orphans deferred | ~~`polynomial_long_division`, `radical_simplification`~~ **done**; quadratic apps (10.4), higher roots (9.7) still **missing** (no type/gen) — do not invent |

## Ordered families for effort scorers (after PA)

Do **not** start A1 scorers until PA first-tranche export/labels stabilize.
Suggested order once PA is green:

1. **Rational number arithmetic** — `rational_add_subtract`, `rational_multiply`, `rational_divide` — **done** (`effort_fraction_ops`)
2. **Percents (A1 surface)** — `percents`, `percent_of_change` — **done**
3. **Scientific notation** — `scientific_notation_*` — **done**
4. **Verbal / expression foundations** — `verbal_expressions`, `order_of_operations`, `distributive_property` — **done**
5. **Linear equation ladder** — `one_step_equations` → `two_step` → `multi_step` → `literal_equations`  
   **Done** (`effort_equations` + `effort_literal_equations`).
6. **Properties of exponents** — `properties_of_exponents` — **done** (`effort_properties_of_exponents`)
7. **Polynomial ops** — naming → ± → simplify → × → special products — **done** (`effort_polynomials` + naming mode); factoring GCF **done** (`effort_poly_gcf`)
8. **Factoring ladder** — grouping / special / quadratic / general / factor-to-solve — **done** (EA2e Ch 7 scorers)
9. **Inequalities / proportions** — `solving_proportions` **done** (`effort_proportions`); one-/two-/multi-step + compound + abs **done**
10. **Systems / linear graphs** — slope / writing / systems_* **aliased** to PA scorers; `graphing_linear_equations` + `evaluating_graphing_functions` **done**; abs / systems-ineq / quadratic graph **done** (prompt + continuous D)
11. **Quadratics / radicals / rationals** — simplify **done**; rational ×÷ + radical ± **done**; square-root / CTS / formula / discriminant **done**; radical ×÷ / equations + rational equations **done**; `radical_simplification` + `polynomial_long_division` **done**; quadratic apps / higher roots **missing**
12. **WP stems** — mixture / DRT / work / age / coin / consecutive / percent **done** (narrative frameworks; stubs removed)
13. **Trig / sets / variation** — defer (`hard` / geo). Stats leaves (`visualizing_data`, `scatter_plots`) **done**.

## Scorer reuse vs new

| type_id / family | Reuse G6/PA scorers? | Notes |
|------------------|----------------------|-------|
| `verbal_expressions` | **Reuse** PA/G6 verbal | Same generator path |
| `order_of_operations`, `distributive_property` | **Reuse** G6 OOO / distributive | Shared primitives |
| `one_step_equations`, `two_step_equations`, `multi_step_equations` | **Reuse** `effort_equations` | Two-step shape + `\left` inequality fix |
| `percents` | **Partial reuse** | G6 intro/formulas scorers; A1 modes differ |
| `percent_of_change` | **New** | Change direction / original base |
| `rational_add_subtract` / `multiply` / `divide` | **Partial reuse** | G6 fraction cancel features; A1 signed / mixed |
| `scientific_notation_*` | **New** (light) | Mantissa + exponent ops |
| `solving_proportions` | **Reuse** `effort_proportions` | + linear slot `(y+2)/6` |
| `properties_of_exponents` | **New** | Product/quotient/power/negative/sum ladder |
| `polynomial_naming` / ± / simplify / × / special | **Reuse+extend** `effort_polynomials` | Naming mode + special-product flag |
| `polynomial_factoring_common_factor` | **New** `effort_poly_gcf` | GCF coef + var power |
| `polynomial_factoring_grouping` | **New** `effort_poly_grouping` | 4-term + GCF-first (EA2e §7.1) |
| `polynomial_factoring_special_cases` | **New** `effort_poly_special` | DOS / PST / cubes (EA2e §7.4) |
| `quadratic_factoring` | **New** `effort_quadratic_factoring` | monic vs ac + signs (EA2e §7.2–7.3) |
| `polynomial_factoring_general_strategy` | **New** `effort_poly_general_strategy` | method-choice premium (EA2e §7.5) |
| `quadratic_factoring_equations` | **New** `effort_quadratic_factor_solve` | factor + zero-product (EA2e §7.6) |
| `slope`, `more_on_slope` | **Reuse** `effort_slope` | A1 alias of PA |
| `writing_linear_equations` | **Reuse** `effort_linear_write` | A1 alias of PA |
| `systems_graphing` / `substitution` / `elimination` / `word_problems` | **Reuse** `effort_systems` | A1 alias of PA |
| `literal_equations` | **New** `effort_literal_equations` | Form depth + isolate cost |
| `one_step_inequalities` / `two_step` / `multi_step` | **Reuse** `effort_equations` | Inequality flag in equations scorer |
| `compound_inequalities` | **New** `effort_compound_inequalities` | and / or / interval |
| `absolute_value_equations` / `inequalities` | **New** `effort_absolute_value` | Nesting + branching |
| `rational_expression_multiply_divide` | **New** `effort_rational_expression_ops` | ×÷ / complex + expand |
| `radical_add_subtract` | **New** `effort_radical_add_subtract` | Like vs unsimplified |
| `quadratic_square_roots` | **New** `effort_quadratic_square_roots` | ±√; vertex / expand-first (EA2e §10.1) |
| `quadratic_completing_square_constant` | **New** `effort_completing_square_constant` | half-b square (EA2e §10.2) |
| `quadratic_completing_square_solve` | **New** `effort_completing_square_solve` | a≠1 + half-b (EA2e §10.2) |
| `quadratic_formula` | **New** `effort_quadratic_formula` | a,b,c + radical simplify (EA2e §10.3) |
| `quadratic_discriminant` | **New** `effort_quadratic_discriminant` | D classify ± perfect-square (EA2e §10.3) |
| `radical_multiply` | **New** `effort_radical_multiply` | simple / coeff / FOIL (EA2e §9.4) |
| `radical_divide` | **New** `effort_radical_divide` | cancel / rationalize / conjugate (EA2e §9.5) |
| `radical_equations` | **New** `effort_radical_equations` | isolate / √=linear / extraneous (EA2e §9.6) |
| `rational_expressions_equations` | **New** `effort_rational_equations` | clear dens + extraneous (EA2e §8.6) |
| `rational_simplification`, `rational_expression_simplification` | **New** | Degree / excluded / multi-addend |
| `polynomial_long_division` | **New** `effort_poly_long_division` | Degree gap + remainder |
| `radical_simplification` | **New** `effort_radical_simplification` | Perfect-square factor size |
| mixture / DRT / work / age / coin / consecutive WP | **New** WP scorers | Story mode + numeric awkwardness |
| `percent_word_problems` / PA markup | **Reuse** `effort_markup_discount` | Narrative `PercentWordProblemFramework` |
| `evaluating_graphing_functions` / `graphing_linear_equations` | **New** prompt-based | Eval family / equation form |
| abs / systems-ineq / quadratic graph | **Reuse+extend** `effort_graph_transform` / `effort_graph_linear` | Continuous D knobs on abs + quadratic |
| Quadratic apps (10.4) / higher roots (9.7) | **Missing** | No type_id / generator — document only |
| Trig / sets / variation | **Defer** | `hard` / geo |
| `visualizing_data` / `scatter_plots` | **Done** | Prompt-based scorers |

## Export stub (pipeline path)

`--algebra-1` is wired in `scripts/export_generation_dataset.py` and loads
[`a1_export_types.json`](a1_export_types.json).

```powershell
$env:PYTHONPATH='.'
python scripts/export_generation_dataset.py `
  --algebra-1 --n-per 15 --out scripts/output/ml/a1_labeled_tranche.jsonl
python scripts/train_forward_effort_model.py `
  --data scripts/output/ml/a1_labeled_tranche.jsonl `
  --out scripts/output/ml/a1_forward_effort_model
```

Earlier stub (n_per=3): **432** rows, **198** labeled / **234** null (first family only).
Full labeled re-export (2026-07-28, n_per=15, 24 types): **2160** rows, **2160** labeled, 0 errors.
EA2e follow-up expands `a1_export_types.json` past 36 (aliases + factoring) to **45** types
(literals / inequalities / abs + rational ×÷ + radical ±).
Full re-export (2026-07-28, n_per=15, 45 types): **4050** rows / **4050** labeled / 0 errors.
Forward train: `a1_forward_effort_model` (GBR) — RMSE ≈ **1.58**, Pearson r ≈ **0.95**
(n_train **3240** / n_test **810**). Prior (24-type) RMSE ≈ 1.24 / r ≈ 0.97.

Ch 8–10 quadratic / radical / rational-eq batch expands to **54** types (+9).
Full re-export (2026-07-28, n_per=15, 54 types): **4860** rows / **4860** labeled / 0 errors.
Forward retrain: `a1_forward_effort_model` (GBR) — RMSE ≈ **1.78**, Pearson r ≈ **0.94**
(n_train **3888** / n_test **972**). Prior (45-type) RMSE ≈ 1.58 / r ≈ 0.95.
Also fixed API resolve so schema form defaults no longer freeze easy mode under continuous D.

**Orphans + WP + prompt-graph batch** expands to **61** types (+7:
`polynomial_long_division`, `radical_simplification`, mixture / DRT / work WP,
`evaluating_graphing_functions`, `graphing_linear_equations`). Also fixed
`wp_work` so narrative `WorkProblemFramework` is not overridden by the
primitive equation stub; curriculum `polynomials_dividing` now maps to
`polynomial_long_division` (was miswired to `radical_divide`).

Full re-export (2026-07-28, n_per=15, 61 types): **5490** rows / **5490** labeled / 0 errors.
Forward retrain: `a1_forward_effort_model` (GBR) — RMSE ≈ **1.82**, Pearson r ≈ **0.93**
(n_train **4392** / n_test **1098**). Prior (54-type) RMSE ≈ 1.78 / r ≈ 0.94.

**WP age/coin/consec/% + graph UX batch** expands to **69** types (+8:
`age_word_problems`, `coin_word_problems`, `consecutive_integers_word_problems`,
`percent_word_problems`, `graphing_absolute_value_equations`,
`graphing_systems_of_inequalities`, `graphing_quadratic_functions`,
`graphing_quadratic_inequalities`). Unblocked narrative frameworks for age/coin/
consecutive/percent (same stub-override fix as `wp_work`); added
`apply_quadratic_graph_continuous_knobs` so quadratic graph forms deepen with D;
abs already used transform knobs; systems-ineq uses primitive continuous policy.

Full re-export (2026-07-28, n_per=15, 69 types): **6210** rows / **6210** labeled / 0 errors.
Forward retrain: `a1_forward_effort_model` (GBR) — RMSE ≈ **1.86**, Pearson r ≈ **0.93**
(n_train **4968** / n_test **1242**). Prior (61-type) RMSE ≈ 1.82 / r ≈ 0.93.

Coverage finish (2026-07-28): added `graphing_exponential_functions`,
`quadratic_solve_by_graphing`, `visualizing_data`, `scatter_plots` to export list.
Full re-export (n_per=15, **73** types): **6570** rows / **6570** labeled / 0 errors.
Forward retrain: RMSE ≈ **2.03**, Pearson r ≈ **0.91** (n_train **5256** / n_test **1314**).

**Still missing (do not invent):** quadratic applications / modeling (EA2e §10.4) and
higher roots (EA2e §9.7) — no catalog type_id / generator; thin wrap not obvious.

**A2 note (do not edit A2 tranche here):** A2 aliases in `effort.py` and entries in
`a2_export_types.json` already cover √ / CTS / formula / discriminant + radical ×÷ /
equations + rational equations. A2 tranche prose may still list some as deferred —
leave re-export / retrain / doc sync to the A2 agent.

## Remaining A1 effort-scorer gaps (ordered)

**Done** (registered in `question_engine/ml/effort.py`):

| Family | type_ids | Scorer |
|--------|----------|--------|
| Rational ±×÷ | `rational_add_subtract`, `rational_multiply`, `rational_divide` | `effort_fraction_ops` |
| Percents | `percents`, `percent_of_change` | `effort_formulas` / `effort_percent_of_change` |
| Scientific notation | `scientific_notation_{write,operations,add_subtract}` | `effort_scientific_notation` |
| Verbal / OOO / distributive | `verbal_expressions`, `order_of_operations`, `distributive_property` | dedicated + G6 aliases |
| Linear equations | `one_step_equations`, `two_step_equations`, `multi_step_equations` | `effort_equations` |
| Proportions | `solving_proportions` | `effort_proportions` |
| Exponent laws | `properties_of_exponents` | `effort_properties_of_exponents` |
| Polynomial ops | naming / ± / simplify / × / special / **long division** | `effort_polynomials` / `effort_poly_long_division` |
| Factor GCF | `polynomial_factoring_common_factor` | `effort_poly_gcf` |
| Factoring ladder | grouping / special / `quadratic_factoring` / general / factor-solve | `effort_poly_grouping` / `effort_poly_special` / `effort_quadratic_factoring` / `effort_poly_general_strategy` / `effort_quadratic_factor_solve` |
| Slope / write / systems | `slope`, `more_on_slope`, `writing_linear_equations`, `systems_*` | PA aliases (`effort_slope` / `effort_linear_write` / `effort_systems`) |
| Literals / inequalities / abs | `literal_equations`, `*_inequalities`, `absolute_value_*` | `effort_literal_equations` / `effort_equations` / `effort_compound_inequalities` / `effort_absolute_value` |
| Rational expressions | simplify + `rational_expression_multiply_divide` + equations | `effort_rational_simplification` / `effort_rational_expression_ops` / `effort_rational_equations` |
| Radical simplify / ±×÷ / equations | `radical_simplification`, `radical_add_subtract`, ×÷, equations | `effort_radical_simplification` / ± / × / ÷ / eq scorers |
| Quadratic methods | square roots / CTS / formula / discriminant | `effort_quadratic_square_roots` / `effort_completing_square_*` / `effort_quadratic_formula` / `effort_quadratic_discriminant` |
| WP stems | mixture / DRT / work / age / coin / consecutive / percent | `effort_wp_*` / `effort_markup_discount` |
| Prompt-graph | eval f(a) / linear / abs / systems-ineq / quadratic (± ineq) / exponential / solve-by-graphing | `effort_evaluating_functions` / `effort_graph_*` / `effort_solve_by_graphing` |
| Stats leaves | `visualizing_data`, `scatter_plots` | prompt-based scorers |

Still open (priority order):

1. Quadratic apps / modeling (10.4) and higher roots (9.7) — **missing** (no type_id / generator); document only — do not invent
2. Trig / sets / variation deferred (`hard` / geo) — stats leaves above are scored

## 2026-07-28 A1 migration batch (this pass)

| Change | type_ids |
|--------|----------|
| Bucket reclass (schema already continuous) | `rational_add_subtract`, `rational_multiply`, `rational_divide`, `percents`, `percent_of_change` |
| `polynomial_settings` + continuous D | poly naming / ± / simplify / × / special (+ factoring profiles inheriting poly) |
| Exponent ladder in generator | `properties_of_exponents` |
| **Effort scorers (first family)** | rational ±×÷, percents / % change, sci-notation_*, verbal / OOO / distributive |
| **Effort scorers (second family)** | equations ladder, `solving_proportions`, exponents, poly ops + GCF, rational simplify |
| Skipped | geo trig, hard stats/sets, scaffold graphs, radical/quadratic `new_generator` |

See also [`CONTINUOUS_D_MIGRATION.md`](CONTINUOUS_D_MIGRATION.md).
