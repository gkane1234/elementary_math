# Linear finish → polynomial-ready architecture

Grounded in `experiment/difficulty-slider` as of 2026-07-17.

**Stack pattern today:** Layer 0 (`numbers`, `variable`) → Layer 1 primitives (`ooo`, `distributive`, `evaluate`, `like_terms`, `expand_simplify`, `equations`, `inequalities`, `factor_gcf`) via `PrimitiveContext` + `prereq_caps` + continuous `D`. Catalog leaves map through `LEAF_TO_PRIMITIVE`; generators live in `primitive_g6` and **override** legacy keys last in `generators/__init__.py`.

---

## Remaining linear inventory

### Done (on primitives / continuous D)

| Family | Leaf / generator examples | Notes |
|--------|---------------------------|--------|
| Layer 0 | `layer0.numbers`, `layer0.variable` | D→lane |
| OOO / distributive | `order_of_operations`, `distributive_property`, G6 aliases | |
| Evaluate linear | `evaluate_algebraic_expressions`, `g6_evaluating_algebraic_expressions` | Affine only |
| Like terms | `combining_like_terms`, `g6_combining_like_terms` | Degree-1 terms (+ optional 2nd var) |
| Expand→simplify | `expand_simplify`, `a2_beginning_algebra_simplifying_algebraic_expressions` | Nested parens; still affine |
| 1/2/multi equations | `one_step_equations`, `two_step_equations`, `multi_step_equations`, `pa_equations_multi_step_equations`, `a2_…_multi_step_equations`, `geo_review_multi_step_equations` | `force_steps`; multi uses log growth |
| 1/2/multi inequalities | `one_step_inequalities`, `two_step_inequalities`, `multi_step_inequalities`, `pa_…`, `a2_…`, `g6_solving_and_graphing_one_step_inequalities` | Same pattern |
| Factor GCF | `factor_gcf`, `g6_factor_gcf`, `polynomial_factoring_common_factor` | **Already leaks degree-2** on `three_terms` / `variable_gcf` |

**Audits present:** `number_profile_audit`, `variable_lane_audit`, `evaluate_linear_expressions_audit`, `combine_like_terms_audit`, `expand_simplify_audit`, `equations_audit`, `multistep_equations_audit`, `inequalities_audit`, `multistep_inequalities_audit`, `factor_gcf_audit`.

### Todo (still legacy frameworks / not on primitive stack)

**Solve-family (single variable, should inherit equations/inequalities):**

| Topic | Leaf / generator ids | Legacy home |
|-------|----------------------|-------------|
| Absolute value equations | `absolute_value_equations`, `a2_equations_and_inequalities_absolute_value_equations` | `AbsoluteValueEquationsFramework` |
| Absolute value inequalities | `absolute_value_inequalities`, `a2_…_absolute_value_inequalities` | `AbsoluteValueInequalitiesFramework` |
| Compound inequalities | `compound_inequalities`, `a2_…_compound_inequalities` | `CompoundInequalitiesFramework` |
| Literal / formulas | `literal_equations` | `LiteralEquationsFramework` |
| Proportions | `solving_proportions`, `pa_checking_for_a_proportion`, G6 equivalent-ratio leaf | `numbers` / proportion profile |
| Special solutions | *no dedicated leaf* | Missing as first-class upgrade on multi-step (identity / no solution); abs already can emit “no solution” |
| Clearing fractions | *no dedicated leaf* | Should be a **structure upgrade** on multi-step (LCD) driven by Layer 0 fraction lanes, not a new degree |

**Two-variable / graph / form (linear geometry of lines):**

| Topic | Leaf / generator ids | Legacy home |
|-------|----------------------|-------------|
| Slope | `slope`, `more_on_slope`, `pa_slope` | `SlopeFramework` |
| Writing linear equations | `writing_linear_equations`, `pa_writing_linear_equations`, A2 writing leaf | `WritingLinearEquationsFramework` |
| Graph lines | `graphing_linear_equations`, `graph_linear_equation`, A2 graph leaf | `GraphLinearEquationFramework` |
| Graph 2-var inequalities | `graphing_linear_inequalities`, `graph_linear_inequality` | `GraphInequalityFramework` |
| Number-line graph | `graphing_single_variable_inequalities` | Number-line mode of inequality graph |
| Graph abs (V-shape) | `graphing_absolute_value_equations`, A2 graph abs | `GraphAbsoluteValueFramework` (piecewise-linear; not poly) |
| Systems elim / sub | `systems_elimination`, `systems_substitution`, PA/A2 aliases | `Systems*Framework` |
| Systems by graphing | `systems_graphing`, `graph_system`, PA/A2 | `GraphSystemFramework` |
| Systems of inequalities | `graphing_systems_of_inequalities`, A2 | `GraphSystemInequalitiesFramework` |
| Variation / relations | `direct_inverse_variation`, `discrete_relations`, `continuous_relations`, `evaluating_graphing_functions` | `linear.py` frameworks |

**Word problems → linear equations (compose, don’t reinvent solve):**

| Topic | Generator ids |
|-------|---------------|
| Mixture / DRT / work / age / coin / consecutive / percent | `wp_mixture`, `wp_distance_rate_time`, `wp_work`, `wp_age`, `wp_coin`, `wp_consecutive_integers`, `wp_percent` (+ A2 aliases) |
| One-/two-step WP | `wp_one_step_equation`, `wp_two_step_equation` |
| Systems WP | `wp_systems` |
| Proportion WP | `wp_proportion` |
| Inequality WP | `wp_inequality` |

**Out of scope for “finish linears” (polynomial / later):** quadratic leaves, matrix 3-var systems beyond linear 2×2, radical/rational/exponential equations.

**Boundary smell:** `factor_gcf` already emits \(x^2\) under upgrades while still registered as a Layer-1 primitive shared with linear catalogs — fix via **expression policy** before expanding poly topics.

---

## Recommended build order (finish linears)

Each phase: inherit listed primitives; reuse Layer 0 lanes/caps; add only topic-specific knobs; ship a `scripts/output/topic_fit/<name>_audit/` sample + topic-fit review.

### Phase 1 — Close gaps inside 1-var solve engine
**Inherits:** `equations` / `inequalities` + Layer 0  
**New knobs:** `allow_special_solutions` (none / identity / no_sol / mixed); `clear_fractions` (bool or D-gated structure); optional `force_lcd`  
**Reuse:** number lanes for fraction density (not a parallel difficulty)  
**Audit:** extend `multistep_equations_audit` / inequalities; assert still degree ≤ 1  
**Why first:** unblocks abs/compound/WP that need richer left/right sides without new engines.

### Phase 2 — Absolute value (eq + ineq)
**Inherits:** Phase-1 equation/inequality builders for *inner* linear expressions; Layer 0  
**New knobs:** form allow-list (already in legacy: `allow_basic`, `allow_abs_equals_abs`, …) mapped to D-gated upgrades instead of flat bools where possible  
**Reuse:** `force_steps`-style structure growth for “how messy is the inner linear”  
**Audit:** `absolute_value_equations_audit`, `absolute_value_inequalities_audit` (cases + no-solution rate)

### Phase 3 — Compound inequalities
**Inherits:** inequality primitive (and/or, chain)  
**New knobs:** `compound_style` (`and`/`or`/`auto`); steps already exist in legacy — retarget to continuous D  
**Reuse:** same multi-step left-hand structures as Phase 1  
**Audit:** `compound_inequalities_audit` + number-line metadata sanity

### Phase 4 — Proportions + literal equations
**Inherits:** equations + Layer 0 (+ multi-letter via `variable` lanes for literals)  
**New knobs:** proportion: cross-multiply vs clear; literal: target variable + formula family  
**Reuse:** coefficients from numbers; **hard** `max_degree=1` / no product of two variables-in-unknown  
**Audit:** `proportions_audit`, `literal_equations_audit`

### Phase 5 — Slope + writing linear forms
**Inherits:** Layer 0 numbers; optional thin “linear form” helper (slope-intercept / point-slope / standard) — **not** the 1-var solve engine  
**New knobs:** mode allow-list (legacy writing modes), slope bounds (can stay settings or D-gated)  
**Reuse:** niceness / integer answers  
**Audit:** `slope_audit`, `writing_linear_equations_audit`

### Phase 6 — Graphing lines & 2-var inequalities (+ number line)
**Inherits:** Phase 5 form helper; existing diagram/stimulus pipeline in `frameworks/graphing.py`  
**New knobs:** mostly presentation (bounds, grid); keep math generation policy-linear  
**Reuse:** same line coefficients as writing/slope  
**Audit:** stimulus-present samples; topic-fit for “graph this line/inequality”

### Phase 7 — Systems (2×2)
**Inherits:** writing linear forms + (for elim/sub) equation-style number sampling  
**New knobs:** method lock; solution type (unique / none / infinite) as D-gated upgrade; coef niceness  
**Reuse:** Layer 0; **two** `variable` samples with distinct names  
**Audit:** `systems_elimination_audit`, `systems_substitution_audit`, `graph_system_audit`

### Phase 8 — Word problems → linear
**Inherits:** Phase 1–7 solve/systems engines for the **equation behind the story**  
**New knobs:** story templates / quantities (mostly existing WP frameworks)  
**Reuse:** do not reimplement solving — sample story → call `sample_linear_equation` / system sampler with fixed structure  
**Audit:** per-family WP audits focused on “maps to intended equation type”

### Phase 9 — Polish / decommission legacy paths
Remove or dead-code `generators/equations.py` one/two/multi bindings once unused; point remaining abs/compound/literal through `primitive_g6`; align `generator_profiles` to `primitive_*` profiles; add CI check that linear leaves resolve to primitives with `expression_family=linear`.

**Suggested deferrals until after Phase 7:** variation/relations, graphing abs V-shapes, 3-var systems (A2) — linear-adjacent but not blocking the 1-var → systems spine.

---

## Polynomial-ready architecture (keep linear pure)

### Expression family / policy (hard constraint)

Introduce a small frozen policy threaded on `PrimitiveContext` (or passed into every `sample_*`):

```text
ExpressionPolicy:
  max_degree: int          # linear leaves → 1
  max_variables: int       # 1-var solve → 1; systems → 2; like-terms upgrade → 2
  allow_var_var_product: bool   # False for linear
  allow_abs: bool
  allowed_ops: ...
```

- **Linear leaves** declare `expression_family="linear"` → policy fixed at `max_degree=1`, `allow_var_var_product=False`.
- **Polynomial leaves** declare `expression_family="polynomial"` → `max_degree` from settings (`min_degree`/`max_degree` already exist in poly domains) and may enable var×var.
- Samplers **assert** policy before emit (and in audits). Difficulty `D` never raises degree on a linear leaf.

### Shared algorithms, parameterized

Keep one implementation of expand / combine / evaluate / “build affine side” / GCF, parameterized by policy:

| Algorithm | Linear behavior | Polynomial inheritance |
|-----------|-----------------|----------------------|
| Expand | constant × (ax+b) only | also (ax+b)(cx+d), higher |
| Like terms | keys = variable letter (deg 1) | keys = monomial `(var → exp)` |
| Evaluate | substitute into affine AST | same AST walker; higher powers OK |
| Factor GCF | numeric GCF of affine; **or** policy-gated poly terms | current `three_terms`/`variable_gcf` move here under poly policy |
| Solve-ish | isolate degree-1 unknown | separate poly solvers; do not extend linear isolate with `x**2` |

“Inherits linear behavior” means: **same budget/caps/lanes/upgrades for structure and number messiness**; only the **monomial alphabet** widens under poly policy.

### Difficulty knobs stay shared

- Layer 0: numbers D→lane, variable D→lane, `prereq_cap_*` unchanged.
- Structure growth (log/exp in `n_ops`, `n_groups`, nest depth) stays on the **topic primitive**, independent of degree.
- Degree is **not** an upgrade purchased from leftover D on linear topics; it is a catalog/policy constant (or a poly-only setting).

### Anti-patterns

1. Sprinkling `x**2` into linear generators to “make hard.”  
2. Letting `factor_gcf` upgrades raise degree without a poly policy (already happening).  
3. One mega-`sample_expression(D)` with implicit degree from D.  
4. Copy-pasting linear equation builders into quadratic solvers.  
5. Soft documentation-only “please stay linear” without assert + audit.

---

## Separation rule (how a topic declares linear vs poly)

1. **Catalog / leaf metadata:** `expression_family: "linear" | "polynomial" | …` (or inferred from `LEAF_TO_PRIMITIVE` + a `LEAF_POLICY` map next to `LEAF_TO_PRIMITIVE`).
2. **Generator wiring:** `build_context(..., policy=LINEAR_POLICY)` for linear; poly leaves pass `PolynomialPolicy(max_degree=settings["max_degree"])`.
3. **Settings UI:** linear profiles = `primitive_layered_settings` (D + caps + number/variable lanes). Poly profiles add `min_degree`/`max_degree` from `settings/domains/polynomial.py` — **never** show degree sliders on linear equation leaves.
4. **CI / audit gate:** sample N items; fail if any term degree > policy.max_degree or if var×var product appears under linear policy.
5. **Shared leaf caution:** `polynomial_factoring_common_factor` must not share unconstrained generator with G6 “linear GCF” without policy split (two leaves → same engine, different policy).

---

## Open questions

1. **Scope cut:** Is “finish all linear” = Phases 1–8 (solve + abs/compound + proportions/literals + lines/systems + WP), or stop after Phase 4 (1-var solve family only) before graph/systems?
2. **Special solutions:** First-class multi-step upgrade now, or only when a curriculum leaf asks for it?
3. **`factor_gcf`:** Immediately clamp G6 / early leaves to `max_degree=1` and move degree-2 paths to poly-only policy, or leave until poly work starts?
4. **Word problems:** Re-base on primitive equation samplers in Phase 8, or leave WP frameworks until after systems feel solid?
5. **Absolute value graphing / variation:** In the linear finish line, or explicitly post-systems polish?
