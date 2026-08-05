# Catalog → Spec → generate (Calc 1 algebraic)

## Honesty about mining today

Stage-1 OpenStax mining (`scripts/output/example_mining/*/stage1/`) is an **inventory dump**: section slug, item kind (example / checkpoint / exercise), prompt LaTeX bits, nearest heading. It is **not** per-nuance classification.

Stage-2 (“tag question families + within-family EMH”) is **not started** (`scripts/output/example_mining/README.md`). Generators are driven by curated **form catalogs** (this layer), not by auto-tagged mining alone.

## Scope

| Now (this pass) | Follow-on |
|-----------------|-----------|
| **Calc 1 algebraic** — limits, derivatives, integrals (Vol.1 + Vol.2 technique sections) | Form catalogs for **all textbooks** in the mining set (prealgebra → precalc → Calc 2/3) |
| Machine-readable `form_id` → D-weighted sampler → metadata | Stage-2 per-item tags aligned to the same `form_id`s |

Algebra1 / Algebra2 / Precalculus catalogs may already exist under `openstax_form_catalogs/` for parallel work; this doc tracks **Calc 1** coverage first, with course sections appended below.

## Pipeline

```
OpenStax HTML
    → stage1 inventory (prompts only; no form_id tags)
    → curated form_catalog JSON  (textbook taxonomy + example_item_ids when known)
    → Spec / leaf sampler selects form_id (D-weighted among generation_status=implemented)
    → build prompt for that form_id
    → metadata: form_id, openstax_form, strategy, catalog_id, tricks_required, …
```

Continuous **D** gates eligibility (`d_min` / optional `d_max`) and reweights toward higher-`d_min` forms as D rises.

## Coverage table (Calc 1)

| Catalog | Path | Implemented | Gaps (stub/deferred) |
|---------|------|-------------|----------------------|
| `trig_integrals` | `…/trig_integrals.json` | 24 | `weierstrass_t_sub` (deferred §3.5) |
| `u_substitution` | `…/u_substitution.json` | 13 | `composite_ln_of_trig` |
| `integration_by_parts` | `…/integration_by_parts.json` | 10 | `poly1_arcsin`; `sec3_via_parts` deferred (owned by trig) |
| `trig_substitution` | `…/trig_substitution.json` | 13 | `sqrt_over_x_a2_minus`; `sinh_alternate_a2_plus` deferred |
| `partial_fractions` | `…/partial_fractions.json` | 9 | `repeated_linear_cube`; `improper_long_division` |
| `basic_power_integrals` | `…/basic_power_integrals.json` | 6 | — |
| `invtrig_integrals` | `…/invtrig_integrals.json` | 6 | — |
| `limits` | `…/limits.json` | 27 | `epsilon_delta` (§2.5 deferred) |
| `derivatives` | `…/derivatives.json` | 22 | `implicit_basic`; `logarithmic_diff` |

Canonical files: `question_engine/frameworks/primitives/openstax_form_catalogs/`.  
Helpers: `load_form_catalog` / `implemented_forms` / `forms_for_leaf` / `select_form_id` / `catalog_form_meta`.

### Trig integrals (§3.2) — recently closed

| form_id | Status |
|---------|--------|
| `sec_odd_reduction_n5` | **implemented** (Checkpoint 3.13) |
| `product_sin_a_sin_b` | **implemented** |
| `weierstrass_t_sub` | deferred (other strategies §3.5) |

### Still-open gaps (prioritized)

1. **PFD** — multiplicity ≥3 dens; improper rational long-division front-end  
2. **Trig-sub** — `√(a²−x²)/x` closed form (Example 3.22)  
3. **Derivatives** — implicit + logarithmic differentiation catalog routing  
4. **Limits** — ε–δ precise definition leaf  
5. **Parts** — poly×arcsin antiderivative template  
6. **Mining** — stage-1 for Vol.2 §3.1 parts / §3.4 PFD (taxonomy is hand-aligned for now)  
7. **All textbooks** — wire remaining A1/A2/PC catalogs the same way; mine + catalog Calc 2/3 leftovers  

## Verify

```powershell
$env:PYTHONPATH='.'
python -m pytest question_engine/tests/test_openstax_form_catalogs.py question_engine/tests/test_calc_limits_integrals_spec.py -q
python scripts/build_algebraic_topic_galleries.py --only calc1
```

Gallery: `scripts/output/topic_fit/calc1_algebraic_gallery/` — inspect `form_id=` in meta lines; expect diversity per section (trig, parts, u-sub, trig-sub, PFD, limits, derivatives).

---

# Algebra 2 — Intermediate Algebra 2e (algebraic topics)

## Catalogs

| Catalog | OpenStax chapters | Path |
|---------|-------------------|------|
| `algebra2_polys` | Ch. 5–6 poly ops / factoring | `openstax_form_catalogs/algebra2_polys.json` |
| `algebra2_rationals` | Ch. 7 rationals (add/simplify/×÷) | `…/algebra2_rationals.json` |
| `algebra2_radicals` | Ch. 8 roots / radical equations | `…/algebra2_radicals.json` |
| `algebra2_exp_log` | Ch. 10 exp/log equations & props | `…/algebra2_exp_log.json` |
| `algebra2_function_ops` | §10.1 + General Functions ops | `…/algebra2_function_ops.json` |

Helper: `question_engine/frameworks/primitives/openstax_a2.py` (`select_a2_form`).  
Mirrored under `scripts/output/example_mining/intermediate-algebra-2e/form_catalogs/`.  
Stage-1: `…/intermediate-algebra-2e/stage1/`. Gaps: `scripts/output/curriculum_gaps/algebra_2.md`.

## Pipeline

```
OpenStax Intermediate Algebra 2e
    → stage1 inventory
    → algebra2_*.json (form_id taxonomy + leaves[] tags)
    → select_a2_form(catalog, D, leaf_id)
    → A2 / shared generator builds prompt for that form_id
    → metadata: form_id, openstax_form, catalog_id, construction=forward_form_catalog
```

## Wired leaves

| type_id | Catalog | Notes |
|---------|---------|-------|
| `a2_polynomial_functions_adding_and_subtracting` | `algebra2_polys` | poly_add / poly_subtract |
| `a2_polynomial_functions_naming` | `algebra2_polys` | poly_degree_classify |
| `a2_polynomial_functions_factoring_by_grouping` | `algebra2_polys` | factor_by_grouping |
| `a2_rational_expressions_simplifying` | `algebra2_rationals` | simplify_cancel |
| `a2_rational_expressions_adding_and_subtracting` | `algebra2_rationals` | common-den / unlike / cancel |
| `a2_rational_expressions_multiplying_and_dividing` | `algebra2_rationals` | multiply vs divide |
| `a2_radical_…_adding_and_subtracting_radical_expressions` | `algebra2_radicals` | like / unsimplified |
| `a2_radical_…_radical_equations` | `algebra2_radicals` | isolate / equals-linear / two radicals |
| `a2_general_functions_operations` | `algebra2_function_ops` | ± / · / ∘ |
| `a2_exponential_…_exponential_equations_*` | `algebra2_exp_log` | same-base / needing log |
| `a2_exponential_…_logarithmic_equations_*` | `algebra2_exp_log` | basic log eq |
| `a2_exponential_…_properties_of_logarithms` | `algebra2_exp_log` | product/quotient/power |

## Gaps (selected)

| form_id | Catalog | Status | Notes |
|---------|---------|--------|-------|
| `pfd_linear_factors` | rationals | deferred | Not IntAlg — wrap `construct_pfd` / PC leaf |
| `rational_apps` | rationals | deferred | §7.5 curriculum gap |
| `add_opposite_dens` | rationals | stub | §7.2 opposite dens |
| `complex_fraction_lcd` / `rational_equation` | rationals | stub | leaves exist; stamp not driving yet |
| `gcf_factor` / `long_division` / `trinomial_a_gt_1` | polys | stub | GCF unwired on A2; division / a≠1 pending |
| `rationalize_*` / `rational_exponents_simplify` | radicals | stub | §8.3–8.5 |
| `change_of_base` / `log_equation_properties` | exp_log | stub | props-first log eq |
| `exp_growth_decay` | exp_log | deferred | WP leaf exists; no form stamp |
| `fn_inverse` / `fn_one_to_one` | function_ops | stub/deferred | §10.1 |

## Verify

```powershell
$env:PYTHONPATH='.'
python -m pytest question_engine/tests/test_a2_openstax_form_catalogs.py -q
python scripts/build_algebraic_topic_galleries.py --only a2
```

Expect distinct `form_id` values on rational add / function ops / radical eq rows in `scripts/output/topic_fit/a2_algebraic_gallery/`.
