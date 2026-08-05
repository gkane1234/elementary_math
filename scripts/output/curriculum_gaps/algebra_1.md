# Curriculum gaps — `algebra_1` (Algebra 1)

Last updated: 2026-07-28

## Sources

| Source | Date | Notes |
|--------|------|-------|
| OpenStax Elementary Algebra TOC (chs. 1–10) | 2026-07-13 | Mapped against `lib/curriculum.ts` (`algebra_1`) + `question_engine/catalogs/algebra_1.py` (and shared A1 type files under `question_engine/types/algebra_1/`) |
| OpenStax Elementary Algebra 2e §7.5 (General Strategy for Factoring Polynomials) | 2026-07-16 | Example-mining smoke test; see capture under Candidate additions |
| OpenStax Elementary Algebra 2e Stage 1 mine (Ch 2, 4–10) | 2026-07-28 | **55 sections** → [`scripts/output/example_mining/elementary-algebra-2e/stage1/`](../example_mining/elementary-algebra-2e/stage1/) ([INDEX](../example_mining/elementary-algebra-2e/stage1/INDEX.md) has A1 `type_id` mappings + effort drivers). Grounds A1 difficulty scorers; see also [`A1_DIFFICULTY_ROADMAP.md`](../ml/A1_DIFFICULTY_ROADMAP.md). |

## Already strong (optional)

- Equation ladder (one-/two-/multi-step, absolute value) + literal equations
- Inequality ladder (graph, one-/two-/multi-step, compound, absolute value)
- Linear graphs: slope, writing/graphing lines, linear inequalities, absolute-value graphs
- Systems: graph / elimination / substitution / systems of inequalities / systems WP
- Polynomials: name, ±, ×, special products; factoring GCF / grouping / special cases
- Quadratics: graph, solve by graphing / square roots / factoring / formula / discriminant / completing the square
- Radicals: ± × ÷ and equations; rational expressions: simplify / ×÷ / ± / equations
- DRT, mixture, work, direct & inverse variation; scientific notation; exponential growth/decay

## Candidate additions

| Topic / skill | Status | Effort | Suggested catalog chapter | Evidence / notes |
|---------------|--------|--------|---------------------------|------------------|
| Dividing polynomials (OpenStax 6.5–6.6) | `done` | `S` | Polynomials | Catalog + curriculum wired to `polynomial_long_division`; continuous D + `effort_poly_long_division` |
| Factoring quadratic expressions (7.2–7.3) | `done` | `S` | Polynomials → Factoring | Catalog leaf `quadratic_factoring` + effort scorer |
| Simplifying single radicals (9.1–9.2) | `done` | `S` | Radical Expressions | Catalog + curriculum `radical_simplification`; `effort_radical_simplification` |
| Age / coin / consecutive-integer / percent word problems | `done` | `S` | Equations | Narrative frameworks wired (`wp_age` / `wp_coin` / `wp_consecutive_integers` / `wp_percent`); A1 export + scorers |
| Properties of real numbers (1.9) | `unwired` | `S` | Beginning Algebra | Only `distributive_property` on A1; G6 `g6_properties_of_addition_and_multiplication` + `IdentifyPropertyFramework` already cover commute/associate/identity/zero |
| Applications with linear inequalities (3.6) | `unwired` | `S` | Inequalities or Equations | Gen `wp_inequality` exists (wired on Grade 6); no A1 inequality-application type |
| Complex rational expressions (8.5) | `unwired` | `S` | Rational Expressions | Gen `complex_fractions` exists (A2 `a2_rational_expressions_complex_fractions`); not on A1 |
| Geometry applications: triangles, rectangles, Pythagorean (3.4) | `partial` | `M` | Equations or Beginning Trigonometry | Pythagorean lives on Pre-Algebra / Geometry; A1 has trig ratios/sides/angles but not OpenStax-style perimeter/area/Pythagorean WP |
| Proportion & similar-figure applications (8.7) | `partial` | `S` | Rational Expressions or Proportions | `solving_proportions` on A1 tree; similar-figures WP is Pre-Algebra only (`pa_similar_figures*`) |
| Equations with fractions or decimals (2.5) | `partial` | `M` | Equations | Likely folded into multi-step; OpenStax wants an explicit section |
| Graph with intercepts / slope-intercept emphasis (4.3, 4.5) | `partial` | `S` | Linear Equations and Inequalities | Folded into `graphing_linear_equations` + `writing_linear_equations`; confirm presets cover intercept- and slope-intercept-focused prompts |
| Mixture applications with systems (5.5) | `partial` | `S` | Systems of Equations and Inequalities | Likely inside `systems_word_problems`; not a dedicated mode |
| Divide monomials (6.5) as its own skill | `partial` | `M` | Polynomials or Exponents | Partially via `properties_of_exponents`; OpenStax separates monomial ÷ from polynomial long division |
| Rational ± with common vs unlike denominators (8.3 vs 8.4) | `partial` | `M` | Rational Expressions | Single `rational_expression_simplification` covers both |
| Uniform motion & work via rational equations (8.8) | `partial` | `M` | Rational Expressions or Equations | DRT/work WP exist as linear models; not clearly rational-equation apps |
| General strategy for factoring polynomials (7.5) | `done` (catalog) / effort open | `M` | Polynomials → Factoring | Catalog leaf `polynomial_factoring_general_strategy` now wired; Stage 1 mine in [`elementary-algebra-2e/stage1`](../example_mining/elementary-algebra-2e/stage1/); effort scorer still open — see **Example mining** below |
| Quadratic applications / modeling (10.4) | `missing` | `M` | Quadratic Functions | Solve methods exist; no quadratic word-problem / modeling type |
| Higher roots (9.7) | `missing` | `M` | Radical Expressions | No cube/nth-root simplify-or-evaluate type on A1 |
| Rational exponents (9.8) | `defer` | `S` | Radical Expressions | Primary home is Algebra 2 (`a2_radical_functions_and_rational_exponents_*`); wire on A1 only if product wants Elementary-Algebra parity |
| Whole numbers / visualize fractions / decimals / measurement (1.1, 1.5, 1.7, 1.10) | `defer` | — | — | Below A1 band; covered (or tracked) under Grade 6 / Pre-Algebra |

### Example mining — General strategy for factoring polynomials

- **Source:** OpenStax Elementary Algebra 2e, §7.5 ([General Strategy for Factoring Polynomials](https://openstax.org/books/elementary-algebra-2e/pages/7-5-general-strategy-for-factoring-polynomials)); consulted 2026-07-16
- **Paraphrased stems:**
  1. Factor completely: a binomial that is a difference of squares (after optional GCF).
  2. Factor completely: a trinomial with leading coefficient ≠ 1 (trial/`ac` method).
  3. Factor completely: a four-term polynomial that factors by grouping (or a sum/difference of cubes after GCF).
- **Pattern:** Prompt is always “factor completely”; student must pick method from a decision tree — GCF first, then by term count (binomial patterns / trinomial `x²+bx+c` or `ax²+bx+c` / grouping). Params: term count, GCF present, special-product flag, leading coeff, whether factors are “complete.” Constraints: factors (other than monomials) must be prime; product checks back to original.
- **Answer form:** Fully factored polynomial (product of primes / monomials).
- **EMH sketch:**
  - Easy: one clear pattern (e.g. difference of squares or monic trinomial); small integers; GCF optional/absent.
  - Medium: GCF required then a second pattern; or `ax²+bx+c` with modest coeffs; or perfect-square trinomials.
  - Hard: mixed item bank across patterns in one type; multi-step complete factoring (e.g. difference of squares that factors again); grouping with four terms; larger coeffs.
- **progression_next:** Quadratic applications / modeling (10.4) — using factoring to solve applied problems (separate skill, not Hard of this type). Prior single-method factoring types (GCF, grouping, special products, `quadratic_factoring`) remain prerequisite leaves, not EMH steps of this type.
- **Suggested:** status=`missing`; effort=`M`; chapter=Polynomials → Factoring
- **Forbidden drifts:** Prompting a named single method only (“factor by grouping”); solving by quadratic formula / completing the square; graphing; word-problem modeling.

## Out of scope / defer

| Topic | Reason |
|-------|--------|
| OpenStax Ch.1 arithmetic foundations (whole numbers, visualize fractions, decimals, measurement) | Remediation — Grade 6 / Pre-Algebra |
| Higher roots & rational exponents as A1-first topics | Prefer Algebra 2 unless we deliberately mirror Elementary Algebra Ch.9 end |
| Beginning trigonometry (A1 already has it) | Extra vs OpenStax TOC, not a gap — do not remove |

## Related files

- Curriculum UI: `lib/curriculum.ts` (`algebra_1`)
- Catalog: `question_engine/catalogs/algebra_1.py`
- Orphan curriculum type_ids (now cataloged): `polynomial_long_division`, `quadratic_factoring`, `radical_simplification`
- Still missing (no gen): quadratic apps / modeling (10.4), higher roots (9.7)
- Properties framework: `IdentifyPropertyFramework` in `question_engine/frameworks/number.py`; G6 gen `g6_properties_of_addition_and_multiplication`
- Complex fractions (A2): `complex_fractions` / `a2_rational_expressions_complex_fractions`
- Inequality WP gen: `wp_inequality` (Grade 6)
