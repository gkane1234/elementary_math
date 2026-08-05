# Curriculum gaps — `algebra_2` (Algebra 2)

Last updated: 2026-07-13

## Sources

| Source | Date | Notes |
|--------|------|-------|
| OpenStax Intermediate Algebra TOC (chs. 1–12) | 2026-07-13 | Mapped against `lib/curriculum.ts` (`algebra_2`) + `question_engine/catalogs/algebra_2.py`; shared generators that live only on A1/Geo/PC noted as `unwired` / `partial` |

## Already strong (optional)

- Equations & inequalities: multi-step, abs value eq/ineq, compound ineq, mixture / DRT / work WPs
- Relations & functions intro; linear graphing/writing; graphing linear & abs-value inequalities
- Systems (2-var graph/elim/sub + WP; 3-var; graphing systems of inequalities); matrices (ops, det, inverse, Cramer, equations)
- Complex numbers; quadratics (factor, square roots, complete square, formula, discriminant, graphing)
- Polynomials (ops, divide, grouping, cubes, all-techniques, advanced root theorems, graphing)
- Radicals & rational exponents; rational expressions (ops, complex fractions, equations)
- Exp/log (graph, properties, equations, growth/decay); conics (parab/circle/ellipse/hyperbola + classify)
- Sequences & series (arith/geo + series); trig; probability & counting

## Candidate additions

| Topic / skill | Status | Effort | Suggested catalog chapter | Evidence / notes |
|---------------|--------|--------|---------------------------|------------------|
| Solve a formula for a specific variable (literal equations) | `unwired` | `S` | Equations and Inequalities | OpenStax 2.3; `literal_equations` exists under Algebra 1 only |
| Slope of a line (dedicated) | `unwired` | `S` | Linear Relations and Functions | OpenStax 3.2; A1 has `slope` / `more_on_slope`; A2 only graphing/writing lines |
| Properties of exponents + scientific notation | `unwired` | `S` | Polynomial Functions or Radical Functions | OpenStax 5.2; A2 has exponent props under radicals; sci-notation types are A1/PA (`scientific_notation_*`) |
| Greatest common factor (polynomials) as distinct skill | `unwired` | `S` | Polynomial Functions | OpenStax 6.1; A1 `polynomial_factoring_common_factor`; A2 has grouping + all-techniques |
| Distance formula (A2 / conics prep) | `unwired` | `S` | Conic Sections | OpenStax 11.1; `radical_distance_formula` on A1 / Geometry, not A2 |
| Midpoint formula (A2 / conics prep) | `unwired` | `S` | Conic Sections | OpenStax 11.1; `radical_midpoint_formula` on A1 / Geometry, not A2 |
| Applications with rational equations | `missing` | `M` | Rational Expressions | OpenStax 7.5; work/mixture WPs are linear-framed, not rational-eq apps |
| Rational inequalities | `missing` | `M` | Rational Expressions | OpenStax 7.6; Precalculus has curriculum stub `pc_rational_inequalities` (no shared selectable A2 type) |
| Solve equations in quadratic form | `partial` | `M` | Quadratic Functions and Inequalities | OpenStax 9.4; A2 has *factoring* quadratic form only (`a2_polynomial_functions_factoring_quadratic_form`) |
| Applications of quadratic equations | `missing` | `M` | Quadratic Functions and Inequalities | OpenStax 9.5; no dedicated quadratic WP / apps type on A2 |
| Graph quadratic functions using transformations | `partial` | `M` | Quadratic Functions and Inequalities | OpenStax 9.7; graphing exists; no transformations-focused type/presets |
| Solve quadratic inequalities (1-variable / interval) | `partial` | `M` | Quadratic Functions and Inequalities | OpenStax 9.8; we graph 2-var regions (`…_graphing_quadratic_inequalities`), not solve/interval form |
| Composite functions (explicit) | `partial` | `M` | General Functions | OpenStax 10.1; `a2_general_functions_operations` is only `(f±g)(x)` eval — no `(f∘g)` / find inverse pair composition |
| Language of algebra / verbal expressions | `unwired` | `S` | Beginning Algebra | OpenStax 1.1; A1 `verbal_expressions`; A2 only order-of-ops + simplifying |

## Out of scope / defer

| Topic | Reason |
|-------|--------|
| Integers / Fractions / Decimals (OpenStax 1.2–1.4) | Below Algebra 2 band — Grade 6 / Pre-Algebra |
| Properties of real numbers (OpenStax 1.5) | Below Algebra 2 band — belongs with A1 beginning algebra / PA |
| Binomial Theorem under Sequences chapter | Already shipped under Polynomial Functions (`a2_polynomial_functions_the_binomial_theorem`) |
| Re-adding full A1 linear/systems ladder as “new” A2 topics | Already covered under A2 (often shared generators) |

## Related files

- Curriculum UI: `lib/curriculum.ts` (`algebra_2`)
- Catalog: `question_engine/catalogs/algebra_2.py`
- Literal equations (A1): `literal_equations`
- Slope (A1): `slope`, `more_on_slope`
- Sci notation (A1/PA): `scientific_notation_write`, `scientific_notation_operations`, `scientific_notation_add_subtract`
- Poly GCF (A1): `polynomial_factoring_common_factor`
- Distance / midpoint: `radical_distance_formula`, `radical_midpoint_formula`
- Rational inequalities stub (PC): `pc_rational_inequalities`
