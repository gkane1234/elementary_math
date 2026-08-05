# Curriculum gaps — `pre_algebra` (Pre-Algebra)

Last updated: 2026-07-28

## Sources

| Source | Date | Notes |
|--------|------|-------|
| OpenStax Prealgebra TOC (chs. 1–11) | 2026-07-13 | Mapped against `lib/curriculum.ts` + `question_engine/catalogs/pre_algebra.py` (and shared types PA already lists from the global pool) |
| OpenStax Prealgebra 2e stage-1 mine (chs. 3–6) | 2026-07-28 | Inventories under `scripts/output/example_mining/prealgebra-2e/stage1/` — integers, fractions, decimals 5.1–5.4, percents 6.1–6.4 |

## Already strong (optional)

- Integer ops; GCF/LCM/factoring; simplify/convert fractions & decimals
- One-/two-/multi-step equations (+ word problems); inequality ladder
- Exponents properties, scientific notation, squares/square roots
- Proportions & similar figures; percents, markup/discount/tax, simple/compound interest
- Plotting points, slope, writing/graphing linear eqns, systems (graph + substitution + WP)
- Plane figures (angles, triangles, quads, circles, transformations), solids, Pythagorean
- Beginning polynomials: add/subtract, multiply

## Candidate additions

| Topic / skill | Status | Effort | Suggested catalog chapter | Evidence / notes |
|---------------|--------|--------|---------------------------|------------------|
| Multiply / add / subtract fractions (if PA owns remediation) | `unwired` | `S` | Integers, Decimals, and Fractions | Same `g6_fraction_*` generators; currently neither G6 nor PA lists them — decide home (G6 vs PA) before wiring both |
| Mixed-number arithmetic (×÷ and ±) | `missing` | `M` | Integers, Decimals, and Fractions | OpenStax 4.3 / 4.6; format helpers exist; no selectable type |
| Numeric complex fractions | `partial` | `M` | Integers, Decimals, and Fractions | A2 has algebraic `complex_fractions`; not PA-level numeric |
| Equations with fraction coefficients (dedicated) | `partial` | `M` | Equations | Partially via multi-step; OpenStax 4.7 / 8.4 want an explicit mode |
| Equations with decimal coefficients (dedicated) | `partial` | `M` | Equations | OpenStax 5.4; same note as fractions |
| Rational vs irrational numbers | `partial` | `S` | Factors and Exponents or Beginning Algebra | Algebra 1 `sets_of_numbers` covers this; not exposed on PA |
| Money applications (non-percent) | `missing` | `M` | Equations or Percents | OpenStax 9.2; tax/interest nearby but no general money WP type |
| Irregular / composite figures area | `partial` | `M` | Plane Figures | Circles + polygon area exist; OpenStax 9.5 irregular figures not covered |
| Solve a formula for a variable (literal equations) | `partial` | `S` | Equations | `literal_equations` exists under Algebra 1 only — wire or clone into PA |
| Divide monomials | `missing` | `M` | Beginning Polynomials | OpenStax 10.4; PA has poly add/sub/mul only |
| Introduction to factoring polynomials (GCF) | `partial` | `S` | Beginning Polynomials | A1 has `polynomial_factoring_common_factor`; natural PA extension from OpenStax 10.6 |
| Graphing with intercepts (dedicated) | `partial` | `S` | Linear Equations and Inequalities | Likely folded into `graphing_linear_equations`; confirm presets cover intercept-focused prompts |
| Commission applications (explicit) | `partial` | `S` | Percents | Markup/discount/tax WP exists; OpenStax 6.3 also names commission — extend modes if missing |
| Basic averages & probability | `partial` | `M` | Statistics | Center/spread/plots exist; simple probability missing (shared with G6 note) |

## Example mining notes (2026-07-28)

Stage-1 inventories mined for OpenStax Prealgebra 2e §§3.1–3.5, 4.1–4.7, 5.1–5.4, 6.1–6.4 (see INDEX + per-section PA mapping). Confirmed:

- **Integers ±×÷** map cleanly to `pa_integers_*` — effort beyond magnitude is sign patterns, chain length, abs-value nesting, applications.
- **Fraction ±×÷ still the main PA hole** — dense banks in 4.2 / 4.4 / 4.5; generators exist on G6 path but PA catalog does not list them.
- **Mixed-number ±×÷ + numeric complex fractions** (4.3, 4.6) remain `missing`.
- **Decimals/percents** mostly wired (`pa_naming_*`, convert, `percents`, markup/tax, interest); decimal *ops* live on G6; eqns with fraction/decimal coeffs still `partial`.

## Out of scope / defer

| Topic | Reason |
|-------|--------|
| Whole-number arithmetic (OpenStax 1.x) | Below Pre-Algebra band |
| Visualize fractions with heavy diagram UI | Prefer G6 if done; UI-heavy — see DEFERRED patterns |
| Advanced polynomial factoring (grouping, special cases, quadratics) | Algebra 1 |

## Related files

- Curriculum UI: `lib/curriculum.ts` (`pre_algebra`)
- Catalog: `question_engine/catalogs/pre_algebra.py`
- Literal equations (A1): `question_engine/catalogs/algebra_1.py` (`literal_equations`)
- Poly factoring GCF (A1): `polynomial_factoring_common_factor`
- Fraction ops (unwired): `g6_fraction_multiply`, `g6_fraction_add_*`, `g6_fraction_subtract_*`
