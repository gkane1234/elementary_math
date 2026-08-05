# Curriculum gaps — `precalculus` (Precalculus)

Last updated: 2026-07-28

## Sources

| Source | Date | Notes |
|--------|------|-------|
| OpenStax Precalculus 2e TOC (chs. 1–12) | 2026-07-13 | Mapped numbered sections against `lib/curriculum.ts` (`precalculus`) + `question_engine/catalogs/precalculus.py` (and A1/A2 types already reused on the PC course) |
| OpenStax Precalculus 2e stage-1 mine (chs 1, 4–7) | 2026-07-28 | Inventories under `scripts/output/example_mining/precalculus-2e/stage1/` — 27 sections / 2280 items |
| Continuous-D + effort tranche | 2026-07-28 | All PC types expose continuous `difficulty`; labeled export for 17 log/trig/exp/limits types — see `scripts/output/ml/PRECALC_DIFFICULTY_TRANCHE.md` |

## Already strong (optional)

- Transformations, average ROC, extrema/increase-decrease, piecewise, inverses
- Polynomial graphs/zeros/division/FTA; rational graphs/equations/inequalities
- Exp/log graphing, properties, equations; compound interest
- Angles, radians/degrees, right-triangle trig, any-angle eval, graphing trig, inverse trig
- Fundamental / sum-diff / multiple-angle / product-to-sum identities; solving trig equations
- Law of Sines/Cosines; polar coords/graphs/forms; complex polar; parametric; vectors (+ 3D)
- Matrices (ops/det/inverses/Cramer via A2 types); partial fractions; multivariable/row ops
- Conics (parabola/ellipse/hyperbola/circle + rotation + polar forms)
- Sequences/series (via A2 types); counting; binomial; probability
- Intro calc: limits (several discontinuity modes), continuity, derivative definition/power rule, area approx/integrals

## Candidate additions

| Topic / skill | Status | Effort | Suggested catalog chapter | Evidence / notes |
|---------------|--------|--------|---------------------------|------------------|
| 1.1 Functions and function notation | `missing` | `M` | Functions | No dedicated type for \(f(x)\) notation / evaluate / identify functions |
| 1.2 Domain and range (general) | `missing` | `M` | Functions | No general D/R; A2 only has `radical_domain_range` |
| 1.4 Composition of functions | `missing` | `M` | Functions | `pc_functions_operations` / `function_operations` is only \(f\pm g\), not \(f\circ g\) |
| 1.6 Absolute value functions | `unwired` | `S` | Functions | A2 `graph_absolute_value` / abs equations exist; not listed under PC |
| 2.1 Linear functions | `unwired` | `S` | New “Linear Functions” or reuse A1/A2 | Linear eqns/functions live on lower courses; not selectable on PC |
| 2.2 Graphs of linear functions | `unwired` | `S` | Linear Functions | Same — graphing linear exists elsewhere |
| 2.3 Modeling with linear functions | `missing` | `M` | Linear Functions | Application / modeling WP type not exposed on PC |
| 2.4 Fitting linear models to data | `missing` | `L` | Linear Functions | No linear regression / line-of-best-fit generator |
| 3.1 Complex numbers (rectangular ops) | `unwired` | `S` | Power/Poly/Rational or new “Complex” | A2 `complex_operations` / graph / abs; PC only has polar form |
| 3.2 Quadratic functions (full unit) | `partial` | `S` | Power/Poly/Rational or Conics | Conic parabolas exist; full A2 quadratic ladder not on PC |
| 3.8 Radical functions (w/ inverses) | `unwired` | `S` | Functions | Inverses covered; radical fn / domain from A2 not on PC |
| 3.9 Modeling using variation | `unwired` | `S` | Power/Poly/Rational | A1 `direct_inverse_variation` exists; not on PC |
| 4.7 Exponential and logarithmic models | `partial` | `M` | Exponential and Logarithmic Expressions | Compound interest only; missing growth/decay/logistic-style models |
| 4.8 Fitting exponential models to data | `missing` | `L` | Exponential and Logarithmic Expressions | No exponential regression / data fit |
| 6.2 Graphs of other trig functions (tan/sec/csc/cot) | `partial` | `M` | Trigonometry | Shared `pc_graphing_trig_functions`; confirm/extend beyond sin/cos |
| 7.1 Verifying trig identities | `partial` | `M` | Trigonometry | Simplify via fundamental IDs; not full verify-LHS=RHS tasks |
| 7.4 Sum-to-product formulas | `missing` | `M` | Trigonometry | `pc_product_to_sum_identities` exists; no sum→product counterpart |
| 7.6 Modeling with trigonometric functions | `missing` | `L` | Trigonometry | No periodic modeling / sinusoidal application WP |
| 8.7 Parametric equations: graphs (dedicated) | `partial` | `M` | Parametric Equations | Single `pc_parametric_equations` type; not a dedicated graphing section |
| 9.1 Systems of linear equations: two variables | `unwired` | `S` | Matrices and Systems | A2 2-var systems (graph/elim/sub/WP) exist; PC jumps to multivariable |
| 9.3 Nonlinear systems and inequalities (2 var) | `unwired` | `S` | Matrices and Systems | A2 `quadratic_system` / related; not listed on PC |
| 12.1 Limits: numerical and graphical approaches | `partial` | `M` | Introduction to Calculus | Algebraic limit types exist; table/graph approaches thin |

## Out of scope / defer

| Topic | Reason |
|-------|--------|
| OpenStax chapter intros / Key Terms / Key Equations / Key Concepts / Review Exercises / Practice Test | Meta TOC — not question families |
| 12.x advanced calc beyond current intro set | Belongs on Calculus course (PC already has a solid intro calc slice) |
| Deep 3D vector calculus / surfaces | Above Precalculus band |

## Related files

- Curriculum UI: `lib/curriculum.ts` (`precalculus`)
- Catalog: `question_engine/catalogs/precalculus.py`
- Function ops (composition gap): `question_engine/generators/algebra2.py` (`function_operations`)
- Abs value (unwired): A2 `graph_absolute_value`, abs equations/inequalities
- Complex rectangular (unwired): A2 `complex_operations`, `complex_graph`, `complex_absolute_value`
- Variation (unwired): A1 `direct_inverse_variation`
- Radical D/R (unwired): A2 `radical_domain_range`
- 2-var systems (unwired): A2 systems-of-equations types
- Nonlinear systems (unwired): A2 `quadratic_system`
