# Curriculum gaps — `calculus` (Calculus)

Last updated: 2026-07-28

## Sources

| Source | Date | Notes |
|--------|------|-------|
| OpenStax Calculus Vol. 1–2 TOC (functions → parametric/polar) | 2026-07-13 | Mapped against `lib/curriculum.ts` (`calculus`) + `question_engine/catalogs/calculus.py`. Precalc/A2 cousins noted where relevant. |
| OpenStax Calc Vol 1–3 stage-1 mine | 2026-07-28 | Vol1 chs 2–6 (34§/2150), Vol2 ∫+volumes (10§/734), Vol3 parametric/vectors pilot (6§/457) under `scripts/output/example_mining/` |
| Continuous-D + effort tranche | 2026-07-28 | All Calc types expose continuous `difficulty`; labeled export for 21 limits/derivative/integral types — see `scripts/output/ml/CALC_DIFFICULTY_TRANCHE.md` |

## Already strong (optional)

- Limits: direct eval, jump/removable/essential discontinuities, limits at infinity
- Continuity classifying; definition of derivative; power/product/quotient/chain; trig/inv trig; ln/exp/other bases; implicit; inverse functions
- Applications of differentiation: tangent/normal, Rolle/MVT, increase/decrease, concavity, extrema, optimization, curve sketching, related rates, differentials, Newton, L’Hôpital, motion
- Indefinite: power, log/exp, trig, inv trig; substitution variants; integration by parts
- Definite: Riemann approx, limit of sums, FTC I/II, substitution, MVT for integrals
- Apps of integration: area under/between curves; disks/washers; shells; known cross sections; motion revisited
- DE: slope fields, intro, separable, exponential growth/decay

## Candidate additions

| Topic / skill | Status | Effort | Suggested catalog chapter | Evidence / notes |
|---------------|--------|--------|---------------------------|------------------|
| Preview of Calculus (tangent/area motivation) | `missing` | `M` | Limits | OpenStax 2.1; conceptual / compare secant→tangent, Riemann foreshadowing |
| Limit Laws (dedicated) | `partial` | `M` | Limits | Folded into direct evaluation; no explicit “apply limit laws step-by-step” type |
| Precise definition of a limit (ε–δ) | `missing` | `L` | Limits | OpenStax 2.5; needs specialized prompts / scaffolding |
| Antiderivatives (as applications/intro topic) | `partial` | `S` | Indefinite Integration or Applications of Differentiation | OpenStax 4.10; we have indefinite rules but not a dedicated “find general/particular F” app-diff chapter type |
| Net Change Theorem | `missing` | `M` | Definite Integration | OpenStax 5.4; related to FTC / motion but not named |
| Trigonometric integrals | `partial` | `L` | Indefinite Integration | OpenStax Vol. 2 §3.2 form catalog + sampler (`openstax_form_catalogs/trig_integrals.json`); stubs remain for sec⁵ reduction / sin·sin product / Weierstrass — see `scripts/output/ml/OPENSTAX_FORM_CATALOG.md` |
| Trigonometric substitution | `missing` | `L` | Indefinite Integration | Distinct from u-sub; no calc type |
| Partial fractions (integration) | `partial` | `M` | Indefinite Integration | Precalc has `pc_partial_fraction_decomposition`; not wired as ∫ via PF |
| Other integration strategies | `missing` | `L` | Indefinite Integration | Catch-all after parts/trig/PF |
| Numerical integration (Trapezoid / Simpson) | `partial` | `M` | Definite Integration | Riemann left/right/mid + tables exist; not Trapezoid/Simpson as named skills |
| Improper integrals | `missing` | `L` | Definite Integration | OpenStax Vol. 2; infinite limits / discontinuous integrands |
| Arc length of a curve | `missing` | `L` | Applications of Integration | OpenStax 6.4 |
| Surface area of revolution | `missing` | `L` | Applications of Integration | OpenStax 6.4 |
| Physical applications (work, force, hydrostatic, etc.) | `missing` | `L` | Applications of Integration | OpenStax 6.5 |
| Moments and centers of mass | `missing` | `L` | Applications of Integration | OpenStax 6.6 |
| Integrals with exponential/log (applications chapter) | `partial` | `S` | Applications of Integration | Indefinite/definite log-exp exist; OpenStax 6.7 framed as apps |
| Calculus of hyperbolic functions | `missing` | `L` | Differentiation / Indefinite Integration | OpenStax 6.9; no hyperbolics in calc catalog |
| Logistic equation | `missing` | `M` | Differential Equations | OpenStax Vol. 2 DE ch.; growth/decay sibling exists |
| First-order linear differential equations | `missing` | `L` | Differential Equations | OpenStax Vol. 2; integrating factor |
| Sequences (limits of sequences) | `missing` | `L` | Sequences and Series *(new chapter)* | OpenStax Vol. 2; A2/Precalc sequences are arithmetic/geometric only |
| Infinite series (partial sums, geometric converge) | `partial` | `L` | Sequences and Series *(new chapter)* | A2/Precalc geometric series exist; not calc convergence framing |
| Divergence and Integral Tests | `missing` | `L` | Sequences and Series *(new chapter)* | Full BC gap |
| Comparison Tests | `missing` | `L` | Sequences and Series *(new chapter)* | |
| Alternating Series | `missing` | `L` | Sequences and Series *(new chapter)* | |
| Ratio and Root Tests | `missing` | `L` | Sequences and Series *(new chapter)* | |
| Power series and functions | `partial` | `L` | Power Series *(new chapter)* | Thin Precalc stub `pc_power_series` — not calc power-series ops |
| Properties of power series | `missing` | `L` | Power Series *(new chapter)* | termwise diff/int, radius/interval |
| Taylor and Maclaurin series | `missing` | `L` | Power Series *(new chapter)* | |
| Working with Taylor series | `missing` | `L` | Power Series *(new chapter)* | approximations, error, known expansions |
| Calculus of parametric curves | `partial` | `L` | Parametric & Polar *(new chapter)* | Precalc `pc_parametric_equations` is coordinate/graph, not dy/dx, arc length |
| Polar coordinates (calc framing) | `partial` | `M` | Parametric & Polar *(new chapter)* | Precalc polar convert/graph/conics exist |
| Area and arc length in polar coordinates | `missing` | `L` | Parametric & Polar *(new chapter)* | |
| Conic sections (calc/polar apps) | `partial` | `M` | Parametric & Polar *(new chapter)* | Precalc `pc_polar_forms_of_conic_sections`; not calc area/length context |

## Out of scope / defer

| Topic | Reason |
|-------|--------|
| OpenStax Vol. 1 Ch. 1 Functions review (1.1–1.5) | Belongs on Precalculus; do not duplicate under Calculus |
| Chapter Review / Key Terms / Key Equations / Review Exercises | Meta textbook sections, not generators |
| Multivariable calculus | Outside current single-variable Calculus course band |

## Related files

- Curriculum UI: `lib/curriculum.ts` (`calculus`)
- Catalog: `question_engine/catalogs/calculus.py`
- Generators: `question_engine/generators/calculus.py`
- Precalc cousins: `pc_partial_fraction_decomposition`, `pc_parametric_equations`, `pc_polar_*`, `pc_power_series`
- A2/Precalc series: `a2_sequences_and_series_*`
