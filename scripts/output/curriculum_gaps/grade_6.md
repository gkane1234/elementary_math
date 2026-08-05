# Curriculum gaps — `grade_6` (Grade 6 Math)

Last updated: 2026-07-13

## Sources

| Source | Date | Notes |
|--------|------|-------|
| OpenStax Prealgebra TOC (chs. 1–11) | 2026-07-13 | Mapped against `lib/curriculum.ts` + `question_engine/catalogs/grade_6.py`; sections that belong here called out below |

## Already strong (optional)

- Ratios, rates, unit conversion
- Intro percents + relating to fractions/decimals
- Dividing fractions (including group/each interpretations)
- Decimal arithmetic (add/sub/mul/div variants)
- Factoring / GCF / LCM (+ word problems)
- Negatives intro: number line, opposites, compare/order, absolute value
- Coordinate plane points, distances, perimeter
- Numeric/algebraic expressions, order of operations, distributive (incl. area models)
- Equations & inequalities intro (tape/hanger, one-step inequalities)
- Polygons area, polyhedra classify/volume-ish, fraction-side length area/volume
- Data: dot plots, histograms, box plots, center/spread

## Candidate additions

| Topic / skill | Status | Effort | Suggested catalog chapter | Evidence / notes |
|---------------|--------|--------|---------------------------|------------------|
| Multiply fractions | `unwired` | `S` | Dividing Fractions → broaden to “Fraction operations”, or add sibling type | Generator `g6_fraction_multiply` exists + presets; not in G6 catalog/curriculum |
| Add/subtract fractions (like denominators) | `unwired` | `S` | Fraction operations | Generators `g6_fraction_add_like`, `g6_fraction_subtract_like` |
| Add/subtract fractions (unlike denominators) | `unwired` | `S` | Fraction operations | Generators `g6_fraction_add_unlike`, `g6_fraction_subtract_unlike` |
| Visualize / introduce fractions (diagram meaning) | `missing` | `L` | Fraction operations | OpenStax 4.1; no dedicated type; may need diagram UI |
| Basic probability (OpenStax 5.5) | `missing` | `M` | Data Sets and Distributions | We have center/spread & plots; not simple experimental/theoretical probability |
| Systems of measurement / measurement word problems | `partial` | `M` | Rates | `g6_converting_units` covers conversions; not full “systems of measurement” apps |

## Out of scope / defer

| Topic | Reason |
|-------|--------|
| Whole-number add/sub/mul/div (OpenStax 1.x) | Below Grade 6 band |
| Integer operations (±×÷) | Pre-Algebra (G6 only does intro/abs value per our curriculum) |
| Multi-step linear equations; graphing lines / slope | Pre-Algebra |
| Polynomials; scientific notation; Pythagorean as PA chapter | Pre-Algebra |
| Tax / commission / discount / interest applications | Pre-Algebra percents |
| Literal equations; factoring polynomials; divide monomials | Algebra 1 / Pre-Algebra candidates — not G6 |

## Related files

- Curriculum UI: `lib/curriculum.ts` (`grade_6_math`)
- Catalog: `question_engine/catalogs/grade_6.py`
- Unwired fraction generators: `question_engine/generators/grade6.py` (`g6_fraction_*`)
