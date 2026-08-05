# OpenStax / mined form inventory

Generated: `2026-08-03T16:46:48.360156+00:00`

Machine-readable twin: `scripts/output/ml/OPENSTAX_FORM_INVENTORY.json`

## Executive summary

- **Catalogs on disk:** 25 (`algebra1_factoring`, `algebra1_linear_equations`, `algebra1_polynomials`, `algebra1_quadratics`, `algebra1_radicals`, `algebra1_rationals`, `algebra2_exp_log`, `algebra2_function_ops`, `algebra2_polys`, `algebra2_radicals`, `algebra2_rationals`, `basic_power_integrals`, `derivatives`, `integration_by_parts`, `invtrig_integrals`, `limits`, `partial_fractions`, `precalculus_exp_log`, `precalculus_function_ops`, `precalculus_partial_fractions`, `precalculus_trig_equations`, `precalculus_trig_identities`, `trig_integrals`, `trig_substitution`, `u_substitution`)
- **Total forms:** 274
- **By generation_status:** implemented=224, stub=33, deferred=17, other=0
- **Forms with >=1 twin** (exact / alias / type_id sibling): 245 / 274 (exact form_id match: 120)
- **Cited mining ids with prompt LaTeX:** 109; cited missing/empty: 0
- **Forms with section-level inspiration only** (no `example_item_ids`): 205
- **Mining index size (item ids):** 17278

### Honesty

- Stage-1 mining (`scripts/output/example_mining/*/stage1/`) is an **inventory dump** (prompt LaTeX + headings). It does **not** tag `form_id`. Stage-2 family tagging is **not started**.
- Explicit form catalogs under `question_engine/frameworks/primitives/openstax_form_catalogs/` are the taxonomy layer. `generation_status=implemented` is author intent; **gallery `shape_id` / live generate** are the evidence a twin can be produced today.
- **Reference pipeline:** trig integrals (`OPENSTAX_FORM_CATALOG.md`) — catalog → `select_form_id` → Spec sampler → metadata `form_id` / `openstax_form`.
- Several catalogs have `stage1: null` (section not mined yet) — inspiration is **section-level** from the OpenStax TOC / prose, not per-exercise ids.
- Curriculum-gap docs map many OpenStax sections as missing/partial without per-form catalogs.
- **Twin matching honesty:** `exact form_id match` means gallery `shape_id`/`form` equals catalog `form_id` (or live metadata stamped the same). Many A1/A2/PC twins are **type_id siblings** or live `_generate_for_type` samples — similar skill, not guaranteed same textbook case. Algebraic galleries omit several leaves (linear equations, quadratics solve methods, A2 radicals, PC trig eq/identities); those were live-generated for this inventory.
- Some `example_item_ids` in catalogs resolve to mining items whose prompt is clearly the wrong exercise (e.g. identity fill-ins under trig-integral forms). Treat cited LaTeX as **what mining has for that id**, and prefer `openstax_case` labels for intent.

### Counts by course bucket

| Bucket | implemented | stub | deferred | total |
|--------|------------:|-----:|---------:|------:|
| Calc1 — Limits & continuity & L'Hôpital | 27 | 0 | 1 | 28 |
| Calc1 — Derivatives | 22 | 2 | 0 | 24 |
| Calc1 — Integrals (basic / table / power) | 12 | 0 | 0 | 12 |
| Calc1 — Integrals (u-substitution) | 13 | 1 | 0 | 14 |
| Calc1 — Integrals (trig integrals) | 24 | 0 | 1 | 25 |
| Calc1 — Integrals (trig substitution) | 13 | 1 | 1 | 15 |
| Calc1 — Integrals (integration by parts) | 10 | 1 | 1 | 12 |
| Calc1 — Integrals (partial fractions) | 9 | 2 | 0 | 11 |
| Precalculus | 26 | 8 | 6 | 40 |
| Algebra 2 | 32 | 12 | 4 | 48 |
| Algebra 1 | 36 | 6 | 3 | 45 |

## Calc1 — Limits & continuity & L'Hôpital

### Catalog `limits`

- **Title:** OpenStax limits — Calc Vol.1 Ch.2 / 4.6–4.8 form taxonomy
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/limits.json`
- **OpenStax:** calculus-volume-1 — 2.3 The Limit Laws
- **URL:** https://openstax.org/books/calculus-volume-1/pages/2-3-the-limit-laws
- **Stage-1 mining:** `scripts/output/example_mining/calculus-volume-1/stage1/2-3-the-limit-laws.json`
- **Forms:** 28 (implemented=27, stub=0, deferred=1)
- **Taxonomy notes:** Pack-scoped catalogs share this file; each form has generator_keys listing which leaves may emit it.

#### `poly_direct` — implemented

- **Description:** lim x→a of polynomial — plug in
- **Strategy:** `direct_eval`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §2.3 poly
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_direct_evaluation`, `calc_limits_by_direct_evaluation`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=539: `\lim_{x \to 5} \left(-3x^{2} - 2x + 6\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=605: `\lim_{x \to 1} \left(-4x^{2}\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=731: `\lim_{x \to -2} \left(5x^{2} + 5x - 5\right)`

#### `rational_direct` — implemented

- **Description:** lim rational with nonzero den at a
- **Strategy:** `direct_eval`
- **D gate:** d_min=2, d_max=None, d_weight=2.0
- **OpenStax case:** §2.3 rational
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_direct_evaluation`, `calc_limits_by_direct_evaluation`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=3.0 seed=590: `\lim_{x \to 5} \frac{-6x^{2} - 6}{2x + 1}`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=3.0 seed=656: `\lim_{x \to 3} \frac{5x^{2} + 4x}{4x + 1}`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=3.0 seed=782: `\lim_{x \to -5} \frac{4x^{2} - 5x}{-2x - 1}`

#### `direct_sin_shift` — implemented

- **Description:** lim sin / cos at special angles
- **Strategy:** `direct_eval`
- **D gate:** d_min=4, d_max=None, d_weight=1.8
- **OpenStax case:** §2.3 trig direct
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_direct_evaluation`, `calc_limits_by_direct_evaluation`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=539: `\lim_{x \to 5} \left(-3x^{2} - 2x + 6\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=605: `\lim_{x \to 1} \left(-4x^{2}\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=731: `\lim_{x \to -2} \left(5x^{2} + 5x - 5\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_

#### `direct_exp` — implemented

- **Description:** lim e^{kx} or e^{2x−x²}
- **Strategy:** `direct_eval`
- **D gate:** d_min=4, d_max=None, d_weight=1.6
- **OpenStax case:** §2.3 exp
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_direct_evaluation`, `calc_limits_by_direct_evaluation`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`limit_direct_evaluation` D=4.0 seed=233: `\lim_{x \to 3} \frac{x^{3} + 2x}{x - 2}`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=539: `\lim_{x \to 5} \left(-3x^{2} - 2x + 6\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=605: `\lim_{x \to 1} \left(-4x^{2}\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_

#### `direct_ln` — implemented

- **Description:** lim ln(x+1) style
- **Strategy:** `direct_eval`
- **D gate:** d_min=4, d_max=None, d_weight=1.5
- **OpenStax case:** §2.3 log
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_direct_evaluation`, `calc_limits_by_direct_evaluation`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=539: `\lim_{x \to 5} \left(-3x^{2} - 2x + 6\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=605: `\lim_{x \to 1} \left(-4x^{2}\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=731: `\lim_{x \to -2} \left(5x^{2} + 5x - 5\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_

#### `direct_sqrt` — implemented

- **Description:** lim of expression with square root
- **Strategy:** `direct_eval`
- **D gate:** d_min=6, d_max=None, d_weight=1.4
- **OpenStax case:** §2.3 roots
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_direct_evaluation`, `calc_limits_by_direct_evaluation`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=539: `\lim_{x \to 5} \left(-3x^{2} - 2x + 6\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=605: `\lim_{x \to 1} \left(-4x^{2}\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=731: `\lim_{x \to -2} \left(5x^{2} + 5x - 5\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_

#### `direct_arctan` — implemented

- **Description:** lim arctan(x)
- **Strategy:** `direct_eval`
- **D gate:** d_min=6, d_max=None, d_weight=1.3
- **OpenStax case:** §2.3 invtrig
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_direct_evaluation`, `calc_limits_by_direct_evaluation`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=539: `\lim_{x \to 5} \left(-3x^{2} - 2x + 6\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=605: `\lim_{x \to 1} \left(-4x^{2}\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=731: `\lim_{x \to -2} \left(5x^{2} + 5x - 5\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_

#### `removable_diff_sq` — implemented

- **Description:** (x²−a²)/(x−a) → x+a
- **Strategy:** `factor_cancel`
- **D gate:** d_min=0, d_max=None, d_weight=2.2
- **OpenStax case:** §2.3 / removable
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_removable`, `calc_limits_at_removable_discontinuities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`limit_removable` D=6.0 seed=107: `\lim_{x \to 4} \frac{x^{2}-16}{x-4}`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_removable_discontinuities` D=0.0 seed=946: `\lim_{x \to 1} \frac{x^{2}-1}{x-1}` _type_id sibling `calc_limits_at_removable_discontinuities` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_removable_discontinuities` D=3.0 seed=805: `\lim_{x \to 1} \frac{(x-1)(x+1)}{x-1}` _type_id sibling `calc_limits_at_removable_discontinuities` (not form_id-exact)_

#### `removable_linear_factor` — implemented

- **Description:** (x−a)(x−b)/(x−a)
- **Strategy:** `factor_cancel`
- **D gate:** d_min=2, d_max=None, d_weight=2.0
- **OpenStax case:** removable linear
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_removable`, `calc_limits_at_removable_discontinuities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`limit_removable` D=6.0 seed=41: `\lim_{x \to 2} \frac{(x-2)(x+2)}{x-2}`
  - [live_generate] type=`limit_removable` D=6.0 seed=233: `\lim_{x \to 5} \frac{(x-5)(x+5)}{x-5}`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_removable_discontinuities` D=0.0 seed=754: `\lim_{x \to 4} \frac{x^{2}-16}{x-4}` _type_id sibling `calc_limits_at_removable_discontinuities` (not form_id-exact)_

#### `removable_quad_shared` — implemented

- **Description:** Shared quadratic factor cancel
- **Strategy:** `factor_cancel`
- **D gate:** d_min=6, d_max=None, d_weight=1.6
- **OpenStax case:** removable quad
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_removable`, `calc_limits_at_removable_discontinuities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_removable_discontinuities` D=0.0 seed=754: `\lim_{x \to 4} \frac{x^{2}-16}{x-4}` _type_id sibling `calc_limits_at_removable_discontinuities` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_removable_discontinuities` D=0.0 seed=946: `\lim_{x \to 1} \frac{x^{2}-1}{x-1}` _type_id sibling `calc_limits_at_removable_discontinuities` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_removable_discontinuities` D=3.0 seed=805: `\lim_{x \to 1} \frac{(x-1)(x+1)}{x-1}` _type_id sibling `calc_limits_at_removable_discontinuities` (not form_id-exact)_

#### `removable_rationalize` — implemented

- **Description:** Rationalize numerator/denominator
- **Strategy:** `rationalize`
- **D gate:** d_min=8, d_max=None, d_weight=1.8
- **OpenStax case:** §2.3 rationalize
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_removable`, `calc_limits_at_removable_discontinuities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_removable_discontinuities` D=8.0 seed=890: `\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_removable_discontinuities` D=8.0 seed=1082: `\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_removable_discontinuities` D=12.0 seed=1024: `\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}`

#### `inf_rational` — implemented

- **Description:** lim x→±∞ rational — compare degrees
- **Strategy:** `compare_degrees`
- **D gate:** d_min=0, d_max=None, d_weight=2.2
- **OpenStax case:** §4.6 rational
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_at_infinity`, `calc_limits_at_infinity`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`limit_at_infinity` D=8.0 seed=107: `\lim_{x \to -\infty} \frac{4x^{2} - 2x}{x^{2}}`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_infinity` D=0.0 seed=817: `\lim_{x \to \infty} \frac{-4x + 3}{3}` _type_id sibling `calc_limits_at_infinity` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_infinity` D=0.0 seed=883: `\lim_{x \to -\infty} \frac{2x - 5}{2x}` _type_id sibling `calc_limits_at_infinity` (not form_id-exact)_

#### `inf_sin_over_x` — implemented

- **Description:** lim sin x / x → 0 at ∞
- **Strategy:** `end_behavior`
- **D gate:** d_min=6, d_max=None, d_weight=1.6
- **OpenStax case:** §4.6 bounded/x
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_at_infinity`, `calc_limits_at_infinity`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`limit_at_infinity` D=8.0 seed=41: `\lim_{x \to \infty} \frac{\cos(x)}{x^{3}}`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_infinity` D=0.0 seed=817: `\lim_{x \to \infty} \frac{-4x + 3}{3}` _type_id sibling `calc_limits_at_infinity` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_infinity` D=0.0 seed=883: `\lim_{x \to -\infty} \frac{2x - 5}{2x}` _type_id sibling `calc_limits_at_infinity` (not form_id-exact)_

#### `inf_arctan` — implemented

- **Description:** lim arctan → ±π/2
- **Strategy:** `end_behavior`
- **D gate:** d_min=6, d_max=None, d_weight=1.5
- **OpenStax case:** §4.6
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_at_infinity`, `calc_limits_at_infinity`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_infinity` D=0.0 seed=817: `\lim_{x \to \infty} \frac{-4x + 3}{3}` _type_id sibling `calc_limits_at_infinity` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_infinity` D=0.0 seed=883: `\lim_{x \to -\infty} \frac{2x - 5}{2x}` _type_id sibling `calc_limits_at_infinity` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_infinity` D=0.0 seed=1009: `\lim_{x \to -\infty} \frac{-4x^{2} - 6x}{4x}` _type_id sibling `calc_limits_at_infinity` (not form_id-exact)_

#### `inf_exp_ratio` — implemented

- **Description:** (a+be^x)/(c+de^x) at ±∞
- **Strategy:** `end_behavior`
- **D gate:** d_min=8, d_max=None, d_weight=1.6
- **OpenStax case:** §4.6 exp
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_at_infinity`, `calc_limits_at_infinity`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`limit_at_infinity` D=8.0 seed=233: `\lim_{x \to \infty} \frac{e^{x}}{x^{3}}`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_infinity` D=0.0 seed=817: `\lim_{x \to \infty} \frac{-4x + 3}{3}` _type_id sibling `calc_limits_at_infinity` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_infinity` D=0.0 seed=883: `\lim_{x \to -\infty} \frac{2x - 5}{2x}` _type_id sibling `calc_limits_at_infinity` (not form_id-exact)_

#### `inf_ln_over_poly` — implemented

- **Description:** lim ln x / x^k → 0
- **Strategy:** `end_behavior`
- **D gate:** d_min=8, d_max=None, d_weight=1.5
- **OpenStax case:** §4.6
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_at_infinity`, `calc_limits_at_infinity`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_infinity` D=0.0 seed=817: `\lim_{x \to \infty} \frac{-4x + 3}{3}` _type_id sibling `calc_limits_at_infinity` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_infinity` D=0.0 seed=883: `\lim_{x \to -\infty} \frac{2x - 5}{2x}` _type_id sibling `calc_limits_at_infinity` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_infinity` D=0.0 seed=1009: `\lim_{x \to -\infty} \frac{-4x^{2} - 6x}{4x}` _type_id sibling `calc_limits_at_infinity` (not form_id-exact)_

#### `squeeze_sin_over_x` — implemented

- **Description:** lim x→0 sin(kx)/x (classic squeeze / known limit)
- **Strategy:** `squeeze_trig`
- **D gate:** d_min=8, d_max=None, d_weight=1.4
- **OpenStax case:** §2.3 / squeeze; also L'H path
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_direct_evaluation`, `calc_limits_by_direct_evaluation`, `lhopitals_rule`, `calc_app_diff_lhopitals_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=539: `\lim_{x \to 5} \left(-3x^{2} - 2x + 6\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=605: `\lim_{x \to 1} \left(-4x^{2}\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_by_direct_evaluation` D=0.0 seed=731: `\lim_{x \to -2} \left(5x^{2} + 5x - 5\right)` _type_id sibling `calc_limits_by_direct_evaluation` (not form_id-exact)_

#### `piecewise_jump` — implemented

- **Description:** Piecewise jump — one- or two-sided
- **Strategy:** `one_sided`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §2.4 / jump
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_jump`, `calc_limits_at_jump_discontinuities_and_kinks`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_jump_discontinuities_and_kinks` D=0.0 seed=666: `\lim_{x \to 2^{-}} f(x)\text{ where }f(x)=\begin{cases}1&x<2\\-1&x\ge 2\end{cases}`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_jump_discontinuities_and_kinks` D=0.0 seed=732: `\lim_{x \to -5} f(x)\text{ where }f(x)=\begin{cases}4&x<-5\\-1&x\ge -5\end{cases}`
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_jump_discontinuities_and_kinks` D=0.0 seed=858: `\lim_{x \to 4} f(x)\text{ where }f(x)=\begin{cases}2&x<4\\4&x\ge 4\end{cases}`

#### `essential_1_over_x` — implemented

- **Description:** lim 1/x as x→0 — essential / infinite
- **Strategy:** `essential`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §2.4 essential
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_essential`, `calc_limits_at_essential_discontinuities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_essential_discontinuities` D=0.0 seed=829: `\lim_{x \to 0} \frac{1}{x}` _matched gallery shape_id~strategy `essential`_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_essential_discontinuities` D=6.0 seed=997: `\lim_{x \to 0} \sin\left(\frac{1}{x}\right)` _matched gallery shape_id~strategy `essential`_

#### `essential_sin_1_over_x` — implemented

- **Description:** lim sin(1/x) — oscillates
- **Strategy:** `essential`
- **D gate:** d_min=6, d_max=None, d_weight=1.5
- **OpenStax case:** §2.4
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_essential`, `calc_limits_at_essential_discontinuities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_essential_discontinuities` D=0.0 seed=829: `\lim_{x \to 0} \frac{1}{x}` _matched gallery shape_id~strategy `essential`_
  - [gallery:calc1_algebraic_gallery] type=`calc_limits_at_essential_discontinuities` D=6.0 seed=997: `\lim_{x \to 0} \sin\left(\frac{1}{x}\right)` _matched gallery shape_id~strategy `essential`_

#### `lhopital_0_0_poly` — implemented

- **Description:** 0/0 rational — one L'Hôpital pass
- **Strategy:** `lhopital`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §4.8 0/0
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `lhopitals_rule`, `calc_app_diff_lhopitals_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`lhopitals_rule` D=12.0 seed=107: `\lim_{x \to 0} \frac{\sin(3x)}{x}`
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=142: `\lim_{x \to 0} \frac{e^{5x}-1}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=334: `\lim_{x \to 0} \frac{e^{4x}-1}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_

#### `lhopital_0_0_trig` — implemented

- **Description:** sin(kx)/x → k via L'H or known
- **Strategy:** `lhopital`
- **D gate:** d_min=4, d_max=None, d_weight=1.8
- **OpenStax case:** §4.8
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `lhopitals_rule`, `calc_app_diff_lhopitals_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`lhopitals_rule` D=12.0 seed=41: `\lim_{x \to 0} \frac{\sin(5x)}{x}`
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=142: `\lim_{x \to 0} \frac{e^{5x}-1}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=208: `\lim_{x \to 0} \frac{\sin(3x)}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_

#### `lhopital_inf_inf_poly` — implemented

- **Description:** ∞/∞ rational at ∞
- **Strategy:** `lhopital`
- **D gate:** d_min=4, d_max=None, d_weight=1.8
- **OpenStax case:** §4.8 ∞/∞
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `lhopitals_rule`, `calc_app_diff_lhopitals_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=142: `\lim_{x \to 0} \frac{e^{5x}-1}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=208: `\lim_{x \to 0} \frac{\sin(3x)}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=334: `\lim_{x \to 0} \frac{e^{4x}-1}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_

#### `lhopital_multipass_exp` — implemented

- **Description:** (e^x−1−x)/x² — two passes
- **Strategy:** `lhopital_multi`
- **D gate:** d_min=12, d_max=None, d_weight=1.8
- **OpenStax case:** §4.8 multi-pass
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `lhopitals_rule`, `calc_app_diff_lhopitals_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`lhopitals_rule` D=12.0 seed=233: `\lim_{x \to 0} \frac{e^{x}-1-x}{x^{2}}`
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=142: `\lim_{x \to 0} \frac{e^{5x}-1}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=208: `\lim_{x \to 0} \frac{\sin(3x)}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_

#### `lhopital_multipass_trig` — implemented

- **Description:** (sin x − x)/x^n — 2–3 passes
- **Strategy:** `lhopital_multi`
- **D gate:** d_min=12, d_max=None, d_weight=1.6
- **OpenStax case:** §4.8
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `lhopitals_rule`, `calc_app_diff_lhopitals_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=142: `\lim_{x \to 0} \frac{e^{5x}-1}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=208: `\lim_{x \to 0} \frac{\sin(3x)}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=334: `\lim_{x \to 0} \frac{e^{4x}-1}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_

#### `lhopital_poly_over_exp` — implemented

- **Description:** x^k/e^x → 0 multi-pass
- **Strategy:** `lhopital_multi`
- **D gate:** d_min=14, d_max=None, d_weight=1.5
- **OpenStax case:** §4.8
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `lhopitals_rule`, `calc_app_diff_lhopitals_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=142: `\lim_{x \to 0} \frac{e^{5x}-1}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=208: `\lim_{x \to 0} \frac{\sin(3x)}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_lhopitals_rule` D=0.0 seed=334: `\lim_{x \to 0} \frac{e^{4x}-1}{x}` _type_id sibling `calc_app_diff_lhopitals_rule` (not form_id-exact)_

#### `continuity_classify` — implemented

- **Description:** Classify continuity at a point
- **Strategy:** `continuity`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §2.4
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **type_id / leaves:** `limit_continuity`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `epsilon_delta` — deferred

- **Description:** ε–δ precise definition exercises
- **Strategy:** `precise_def`
- **D gate:** d_min=20, d_max=None, d_weight=0.5
- **OpenStax case:** §2.5
- **Book / section:** calculus-volume-1 / 2.3 The Limit Laws
- **Gap reason:** Not in current algebraic gallery leaves
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

## Calc1 — Derivatives

### Catalog `derivatives`

- **Title:** OpenStax differentiation rules — Calc Vol.1 Ch.3 form taxonomy
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/derivatives.json`
- **OpenStax:** calculus-volume-1 — 3.3 Differentiation Rules
- **URL:** https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules
- **Stage-1 mining:** `scripts/output/example_mining/calculus-volume-1/stage1/3-3-differentiation-rules.json`
- **Forms:** 24 (implemented=22, stub=2, deferred=0)
- **Taxonomy notes:** Forms map to ExpressionSpec packs / force flags. generator_keys filter which leaf selects each form.

#### `power_poly` — implemented

- **Description:** Power rule on Σ c x^k
- **Strategy:** `power_rule`
- **D gate:** d_min=0, d_max=None, d_weight=2.2
- **OpenStax case:** §3.3 power
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_power_rule`, `calc_diff_power_rule`, `derivative_higher_order`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_power_rule` D=0.0 seed=164: `\text{Find }\frac{d}{dx}\left(-x^{3}\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_power_rule` D=0.0 seed=230: `\frac{d}{dx}\left[3x^{3}\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_power_rule` D=3.0 seed=215: `\frac{d}{dx}\left[2x^{2} - 2x - 3\right]`

#### `power_root` — implemented

- **Description:** Power rule with √x / fractional exponents
- **Strategy:** `power_rule`
- **D gate:** d_min=4, d_max=None, d_weight=1.8
- **OpenStax case:** §3.3 roots
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_power_rule`, `calc_diff_power_rule`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_power_rule` D=12.0 seed=434: `\frac{d}{dx}\left[x^{\sqrt{3}}\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_power_rule` D=16.0 seed=436: `\frac{d}{dx}\left[x^{\frac{2}{3}}\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_power_rule` D=20.0 seed=504: `\text{Find }\frac{d}{dx}\left(x^{\frac{3}{2}}\right)`

#### `power_negative` — implemented

- **Description:** Negative integer powers
- **Strategy:** `power_rule`
- **D gate:** d_min=6, d_max=None, d_weight=1.5
- **OpenStax case:** §3.3
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_power_rule`, `calc_diff_power_rule`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_power_rule` D=8.0 seed=300: `\text{Find }\frac{d}{dx}\left(x^{\frac{1}{2}}\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_power_rule` D=16.0 seed=502: `\frac{d^{2}}{dx^{2}}\left[3x^{3} - 3x^{2} + x - 5\right]`
  - [gallery:pc_algebraic_gallery] type=`pc_power_rule_for_differentiation` D=6.0 seed=556: `\text{Find }\frac{d}{dx}\left(x^{-\frac{3}{2}}\right)`

#### `product_two_poly` — implemented

- **Description:** Product of two polynomials
- **Strategy:** `product_rule`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §3.3 product
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_product_rule`, `calc_diff_product_rule`, `derivative_general`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_product_rule` D=0.0 seed=515: `\frac{d}{dx}\left[\left(-3x^{2}\right)x\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_product_rule` D=0.0 seed=581: `\text{Find }\frac{d}{dx}\left(3x^{4}\left(-x^{3}\right)\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_product_rule` D=0.0 seed=707: `\frac{d}{dx}\left[3x^{4}\left(2x\right)\right]`

#### `product_poly_trig` — implemented

- **Description:** Poly × trig product
- **Strategy:** `product_rule`
- **D gate:** d_min=8, d_max=None, d_weight=1.8
- **OpenStax case:** §3.3 / §3.5
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_product_rule`, `calc_diff_product_rule`, `derivative_trigonometric`, `derivative_general`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_product_rule` D=8.0 seed=843: `\frac{d}{dx}\left[\cos(3x)\left(-3x^{3}\right)\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_product_rule` D=12.0 seed=719: `\text{Find }\frac{d}{dx}\left(2x^{3}\tan(4x)\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_product_rule` D=12.0 seed=785: `\text{Find }\frac{d}{dx}\left(e^{5x + 2}\left(-x^{2}\right)\right)`

#### `product_poly_exp` — implemented

- **Description:** Poly × exp product
- **Strategy:** `product_rule`
- **D gate:** d_min=8, d_max=None, d_weight=1.8
- **OpenStax case:** §3.9
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_product_rule`, `calc_diff_product_rule`, `derivative_ln_exp`, `derivative_general`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_product_rule` D=20.0 seed=921: `\text{Find }\frac{d}{dx}\left(e^{5x + 5}\cos(5x)\cos^{3}(2x)\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_natural_logarithms_and_exponentials` D=12.0 seed=860: `\frac{d}{dx}\left[\ln^{2}(5x)\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_natural_logarithms_and_exponentials` D=20.0 seed=1062: `\frac{d^{2}}{dx^{2}}\left[e^{e^{x}}\right]`

#### `quotient_poly` — implemented

- **Description:** Quotient of polynomials
- **Strategy:** `quotient_rule`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §3.3 quotient
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_quotient_rule`, `calc_diff_general`, `calc_diff_product_rule`, `derivative_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_quotient_rule` D=0.0 seed=814: `\frac{d}{dx}\left[\frac{3x^{2}}{x - 1}\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_quotient_rule` D=0.0 seed=880: `\frac{d}{dx}\left[\frac{-x^{4}}{3x + 2}\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_quotient_rule` D=0.0 seed=1006: `\text{Find }\frac{d}{dx}\left(\frac{-3x^{3}}{x + 2}\right)`

#### `quotient_trig_poly` — implemented

- **Description:** Trig / poly quotient
- **Strategy:** `quotient_rule`
- **D gate:** d_min=8, d_max=None, d_weight=1.6
- **OpenStax case:** §3.5
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_quotient_rule`, `calc_diff_general`, `calc_diff_product_rule`, `derivative_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_quotient_rule` D=12.0 seed=1084: `\text{Find }\frac{d}{dx}\left(\frac{2x^{3} - 2x^{2} + 3x + 5}{2x - 4}\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_quotient_rule` D=16.0 seed=1086: `\text{Find }\frac{d}{dx}\left(\frac{3x^{3} + 3x^{2} - 3x}{5x - 2}\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_quotient_rule` D=16.0 seed=1152: `\text{Find }\frac{d}{dx}\left(\frac{2x^{3} - 5x^{2} + 4x + 2}{4x + 3}\right)`

#### `chain_power_linear` — implemented

- **Description:** (ax+b)^n chain
- **Strategy:** `chain_rule`
- **D gate:** d_min=2, d_max=None, d_weight=2.2
- **OpenStax case:** §3.6
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_chain_rule`, `calc_diff_chain_rule`, `derivative_power_rule`, `calc_diff_power_rule`, `derivative_general`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_power_rule` D=3.0 seed=407: `\text{Find }\frac{d}{dx}\left(\left(x^{2} - 1\right)^{3}\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_power_rule` D=6.0 seed=266: `\text{Find }\frac{d}{dx}\left(\left(3x^{2} - 4\right)^{5}\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_power_rule` D=8.0 seed=492: `\frac{d}{dx}\left[\left(2x^{2} - 1\right)^{\frac{1}{2}}\right]`

#### `chain_trig_poly` — implemented

- **Description:** sin/cos of polynomial
- **Strategy:** `chain_rule`
- **D gate:** d_min=4, d_max=None, d_weight=2.0
- **OpenStax case:** §3.6 / §3.5
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_chain_rule`, `calc_diff_chain_rule`, `derivative_trigonometric`, `derivative_general`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_chain_rule` D=0.0 seed=551: `\frac{d}{dx}\left[\left(3x - 2\right)^{2}\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_chain_rule` D=0.0 seed=677: `\text{Find }\frac{d}{dx}\left(\left(3x - 3\right)^{3}\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_chain_rule` D=6.0 seed=587: `\text{Find }\frac{d}{dx}\left(\tan\left(5x + 1\right)\right)`

#### `chain_nested` — implemented

- **Description:** Nested chain depth ≥2
- **Strategy:** `chain_rule`
- **D gate:** d_min=12, d_max=None, d_weight=1.8
- **OpenStax case:** §3.6 nested
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_chain_rule`, `calc_diff_chain_rule`, `derivative_general`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_chain_rule` D=12.0 seed=689: `\text{Find }\frac{d}{dx}\left(e^{5x - 5}\sqrt{x + 2}\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_chain_rule` D=12.0 seed=755: `\frac{d}{dx}\left[\ln^{3}\left(\sqrt{5x}\right)\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_chain_rule` D=12.0 seed=881: `\text{Find }\frac{d}{dx}\left(\ln^{2}(4x)\right)`

#### `trig_basic` — implemented

- **Description:** d/dx sin, cos, tan, sec table
- **Strategy:** `trig_table`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §3.5
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_trigonometric`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_trigonometric` D=0.0 seed=911: `\frac{d}{dx}\left[\tan(3x)\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_trigonometric` D=0.0 seed=977: `\text{Find }\frac{d}{dx}\left(\sin(3x)\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_trigonometric` D=0.0 seed=1103: `\frac{d}{dx}\left[\cos(3x)\right]`

#### `trig_product_chain` — implemented

- **Description:** Trig product or chained trig
- **Strategy:** `trig_advanced`
- **D gate:** d_min=8, d_max=None, d_weight=1.8
- **OpenStax case:** §3.5
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_trigonometric`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_general` D=0.0 seed=268: `\text{Find }\frac{d}{dx}\left(-3x^{3}\right)` _type_id sibling `calc_diff_general` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_general` D=0.0 seed=334: `\frac{d}{dx}\left[x^{4}\right]` _type_id sibling `calc_diff_general` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_general` D=0.0 seed=460: `\text{Find }\frac{d}{dx}\left(x\right)` _type_id sibling `calc_diff_general` (not form_id-exact)_

#### `ln_basic` — implemented

- **Description:** d/dx ln|x| / ln|g|
- **Strategy:** `log_rule`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §3.9
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_ln_exp`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_natural_logarithms_and_exponentials` D=3.0 seed=707: `\frac{d}{dx}\left[\ln\left(3x + 1\right)\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_natural_logarithms_and_exponentials` D=6.0 seed=758: `\text{Find }\frac{d}{dx}\left(\ln\left(x + 2\right)\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_natural_logarithms_and_exponentials` D=6.0 seed=950: `\frac{d}{dx}\left[\ln\left(4x - 1\right)\ln\left(3x + 3\right)\right]`

#### `exp_basic` — implemented

- **Description:** d/dx e^x / e^{g}
- **Strategy:** `exp_rule`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §3.9
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_ln_exp`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_natural_logarithms_and_exponentials` D=0.0 seed=656: `\frac{d}{dx}\left[e^{3x + 1}\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_natural_logarithms_and_exponentials` D=0.0 seed=722: `\text{Find }\frac{d}{dx}\left(e^{3x + 1}\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_natural_logarithms_and_exponentials` D=0.0 seed=848: `\frac{d}{dx}\left[e^{2x + 2}\right]`

#### `ln_exp_product` — implemented

- **Description:** Product/chain mixing ln and exp
- **Strategy:** `ln_exp_mix`
- **D gate:** d_min=10, d_max=None, d_weight=1.6
- **OpenStax case:** §3.9
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_ln_exp`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_natural_logarithms_and_exponentials` D=12.0 seed=1052: `\frac{d}{dx}\left[\ln\left(3x + 1\right)e^{4x - 1}\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_natural_logarithms_and_exponentials` D=16.0 seed=994: `\text{Find }\frac{d}{dx}\left(\ln\left(x - 1\right)\ln\left(x - 4\right)\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_natural_logarithms_and_exponentials` D=20.0 seed=996: `\frac{d}{dx}\left[\ln^{3}(3x)\right]`

#### `invtrig_arcsin` — implemented

- **Description:** d/dx arcsin
- **Strategy:** `invtrig`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §3.7
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_inverse_trig`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_inverse_trigonometric` D=0.0 seed=232: `\frac{d}{dx}\left[\arcsin(x)\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_inverse_trigonometric` D=0.0 seed=298: `\frac{d}{dx}\left[\arctan(x)\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_inverse_trigonometric` D=3.0 seed=349: `\text{Find }\frac{d}{dx}\left(\arccos(x)\right)`

#### `invtrig_arctan` — implemented

- **Description:** d/dx arctan
- **Strategy:** `invtrig`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §3.7
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_inverse_trig`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_inverse_trigonometric` D=0.0 seed=424: `\frac{d}{dx}\left[\arctan(x)\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_inverse_trigonometric` D=3.0 seed=283: `\text{Find }\frac{d}{dx}\left(\arcsin(x)\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_inverse_trigonometric` D=3.0 seed=475: `\frac{d}{dx}\left[\arcsin(x)\right]`

#### `invtrig_chained` — implemented

- **Description:** arcsinx/arctan of composite
- **Strategy:** `invtrig_chain`
- **D gate:** d_min=8, d_max=None, d_weight=1.6
- **OpenStax case:** §3.7
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_inverse_trig`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_inverse_trigonometric` D=8.0 seed=368: `\text{Find }\frac{d}{dx}\left(\arcsin^{2}(x)\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_inverse_trigonometric` D=8.0 seed=560: `\frac{d}{dx}\left[\arccos(x)\arctan(x)\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_inverse_trigonometric` D=12.0 seed=628: `\frac{d^{2}}{dx^{2}}\left[\arctan^{2}(x)\right]`

#### `higher_order_2` — implemented

- **Description:** Second derivative
- **Strategy:** `higher_order`
- **D gate:** d_min=4, d_max=None, d_weight=2.0
- **OpenStax case:** §3.3 higher-order
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_higher_order`, `calc_diff_power_rule`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_higher_order_derivatives` D=6.0 seed=802: `\frac{d^{2}}{dx^{2}}\left[\tan(4x)\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_higher_order_derivatives` D=6.0 seed=994: `\frac{d^{2}}{dx^{2}}\left[\tan(2x)\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_higher_order_derivatives` D=8.0 seed=902: `\frac{d^{2}}{dx^{2}}\left[e^{5x - 3}\right]`

#### `higher_order_3` — implemented

- **Description:** Third derivative
- **Strategy:** `higher_order`
- **D gate:** d_min=10, d_max=None, d_weight=1.5
- **OpenStax case:** §3.3
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_higher_order`, `calc_diff_power_rule`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_higher_order_derivatives` D=12.0 seed=904: `\frac{d^{3}}{dx^{3}}\left[e^{x}\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_higher_order_derivatives` D=12.0 seed=970: `\frac{d^{3}}{dx^{3}}\left[e^{3x - 5}\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_higher_order_derivatives` D=16.0 seed=972: `\frac{d^{3}}{dx^{3}}\left[e^{5x - 2}\right]`

#### `general_mixed` — implemented

- **Description:** General mix of product/chain/specials
- **Strategy:** `general`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §3.3–3.9 combined
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_general`, `calc_diff_general`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_general` D=0.0 seed=268: `\text{Find }\frac{d}{dx}\left(-3x^{3}\right)`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_general` D=0.0 seed=334: `\frac{d}{dx}\left[x^{4}\right]`
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_general` D=3.0 seed=385: `\frac{d}{dx}\left[3x^{3} - x^{2} - 3x\right]`

#### `implicit_basic` — stub

- **Description:** Implicit differentiation
- **Strategy:** `implicit`
- **D gate:** d_min=0, d_max=None, d_weight=1.0
- **OpenStax case:** §3.8
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_implicit`, `calc_diff_general`
- **Gap reason:** Implicit sampler not yet catalog-routed
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_general` D=0.0 seed=268: `\text{Find }\frac{d}{dx}\left(-3x^{3}\right)` _type_id sibling `calc_diff_general` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_general` D=0.0 seed=334: `\frac{d}{dx}\left[x^{4}\right]` _type_id sibling `calc_diff_general` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_general` D=0.0 seed=460: `\text{Find }\frac{d}{dx}\left(x\right)` _type_id sibling `calc_diff_general` (not form_id-exact)_

#### `logarithmic_diff` — stub

- **Description:** Logarithmic differentiation
- **Strategy:** `logarithmic`
- **D gate:** d_min=0, d_max=None, d_weight=1.0
- **OpenStax case:** §3.9 log diff
- **Book / section:** calculus-volume-1 / 3.3 Differentiation Rules
- **type_id / leaves:** `derivative_logarithmic`, `calc_diff_general`
- **Gap reason:** Logarithmic-diff leaf not yet catalog-routed
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_general` D=0.0 seed=268: `\text{Find }\frac{d}{dx}\left(-3x^{3}\right)` _type_id sibling `calc_diff_general` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_general` D=0.0 seed=334: `\frac{d}{dx}\left[x^{4}\right]` _type_id sibling `calc_diff_general` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_diff_general` D=0.0 seed=460: `\text{Find }\frac{d}{dx}\left(x\right)` _type_id sibling `calc_diff_general` (not form_id-exact)_

## Calc1 — Integrals (basic / table / power)

### Catalog `basic_power_integrals`

- **Title:** OpenStax basic power / rewrite antiderivatives
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/basic_power_integrals.json`
- **OpenStax:** calculus-volume-1 — 4.10 Antiderivatives
- **URL:** https://openstax.org/books/calculus-volume-1/pages/4-10-antiderivatives
- **Stage-1 mining:** `scripts/output/example_mining/calculus-volume-1/stage1/4-10-antiderivatives.json`
- **Forms:** 6 (implemented=6, stub=0, deferred=0)

#### `poly_sum` — implemented

- **Description:** ∫ Σ c_k x^k dx
- **Strategy:** `power_rule`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §4.10 power rule
- **Book / section:** calculus-volume-1 / 4.10 Antiderivatives
- **type_id / leaves:** `calc_indef_int_power_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=0.0 seed=1035: `\int 6 \, dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=0.0 seed=1101: `\int -x^{3} \, dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=0.0 seed=1227: `\int 3x^{3} \, dx`

#### `sqrt_x` — implemented

- **Description:** ∫ √x dx
- **Strategy:** `power_rule_root`
- **D gate:** d_min=0, d_max=None, d_weight=1.5
- **OpenStax case:** §4.10 / §5.4 roots
- **Book / section:** calculus-volume-1 / 4.10 Antiderivatives
- **type_id / leaves:** `calc_indef_int_power_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=3.0 seed=1152: `\int \sqrt{x}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=0.0 seed=1035: `\int 6 \, dx` _type_id sibling `calc_indef_int_power_rule` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=0.0 seed=1101: `\int -x^{3} \, dx` _type_id sibling `calc_indef_int_power_rule` (not form_id-exact)_

#### `one_over_sqrt_x` — implemented

- **Description:** ∫ 1/√x dx
- **Strategy:** `power_rule_root`
- **D gate:** d_min=2, d_max=None, d_weight=1.5
- **OpenStax case:** §4.10
- **Book / section:** calculus-volume-1 / 4.10 Antiderivatives
- **type_id / leaves:** `calc_indef_int_power_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=3.0 seed=1086: `\int \frac{1}{\sqrt{x}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=0.0 seed=1035: `\int 6 \, dx` _type_id sibling `calc_indef_int_power_rule` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=0.0 seed=1101: `\int -x^{3} \, dx` _type_id sibling `calc_indef_int_power_rule` (not form_id-exact)_

#### `x_sqrt_x` — implemented

- **Description:** ∫ x√x dx = ∫ x^{3/2}
- **Strategy:** `power_rule_root`
- **D gate:** d_min=4, d_max=None, d_weight=1.4
- **OpenStax case:** §4.10
- **Book / section:** calculus-volume-1 / 4.10 Antiderivatives
- **type_id / leaves:** `calc_indef_int_power_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=16.0 seed=1307: `\int x\sqrt{x}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=0.0 seed=1035: `\int 6 \, dx` _type_id sibling `calc_indef_int_power_rule` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=0.0 seed=1101: `\int -x^{3} \, dx` _type_id sibling `calc_indef_int_power_rule` (not form_id-exact)_

#### `neg_power` — implemented

- **Description:** ∫ k/x^n dx, n≥2
- **Strategy:** `power_rule_neg`
- **D gate:** d_min=4, d_max=None, d_weight=1.6
- **OpenStax case:** §4.10 negative powers ≠ −1
- **Book / section:** calculus-volume-1 / 4.10 Antiderivatives
- **type_id / leaves:** `calc_indef_int_power_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=6.0 seed=1137: `\int \frac{2}{x^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=6.0 seed=1329: `\int \frac{3}{x^{3}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=8.0 seed=1171: `\int \frac{4}{x^{4}}\,dx`

#### `rewrite_over_x` — implemented

- **Description:** ∫ (x² + c∛x)/x — rewrite then power
- **Strategy:** `rewrite_split`
- **D gate:** d_min=6, d_max=None, d_weight=1.8
- **OpenStax case:** §4.10 rewrite
- **Book / section:** calculus-volume-1 / 4.10 Antiderivatives
- **type_id / leaves:** `calc_indef_int_power_rule`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=6.0 seed=1203: `\int \frac{x^{2}+5\sqrt[3]{x}}{x}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=12.0 seed=1239: `\int \frac{x^{2}+4\sqrt[3]{x}}{x}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule` D=0.0 seed=1035: `\int 6 \, dx` _type_id sibling `calc_indef_int_power_rule` (not form_id-exact)_

### Catalog `invtrig_integrals`

- **Title:** OpenStax integrals → inverse trig — table forms
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/invtrig_integrals.json`
- **OpenStax:** calculus-volume-1 — 5.7 Integrals Resulting in Inverse Trigonometric Functions
- **URL:** https://openstax.org/books/calculus-volume-1/pages/5-7-integrals-resulting-in-inverse-trigonometric-functions
- **Stage-1 mining:** `scripts/output/example_mining/calculus-volume-1/stage1/5-7-integrals-resulting-in-inverse-trigonometric-functions.json`
- **Forms:** 6 (implemented=6, stub=0, deferred=0)

#### `arctan_basic` — implemented

- **Description:** ∫ 1/(1+x²) dx
- **Strategy:** `table_arctan`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §5.7 table
- **Book / section:** calculus-volume-1 / 5.7 Integrals Resulting in Inverse Trigonometric Functions
- **type_id / leaves:** `calc_indef_int_inverse_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=0.0 seed=41: `\int \frac{1}{1+x^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=3.0 seed=92: `\int \frac{1}{\sqrt{1-x^{2}}}\,dx` _type_id sibling `calc_indef_int_inverse_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=8.0 seed=177: `\int \frac{1}{\sqrt{16-x^{2}}}\,dx` _type_id sibling `calc_indef_int_inverse_trigonometric` (not form_id-exact)_

#### `arctan_a2` — implemented

- **Description:** ∫ 1/(a²+x²) dx
- **Strategy:** `table_arctan`
- **D gate:** d_min=2, d_max=None, d_weight=2.0
- **OpenStax case:** §5.7
- **Book / section:** calculus-volume-1 / 5.7 Integrals Resulting in Inverse Trigonometric Functions
- **type_id / leaves:** `calc_indef_int_inverse_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=8.0 seed=243: `\int \frac{1}{9+x^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=16.0 seed=505: `\int \frac{1}{4+x^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=0.0 seed=41: `\int \frac{1}{1+x^{2}}\,dx` _type_id sibling `calc_indef_int_inverse_trigonometric` (not form_id-exact)_

#### `arctan_scaled` — implemented

- **Description:** ∫ 1/(a²+b²x²) dx
- **Strategy:** `table_arctan_scaled`
- **D gate:** d_min=6, d_max=None, d_weight=1.8
- **OpenStax case:** §5.7 scaled
- **Book / section:** calculus-volume-1 / 5.7 Integrals Resulting in Inverse Trigonometric Functions
- **type_id / leaves:** `calc_indef_int_inverse_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=20.0 seed=381: `\int \frac{1}{25+9x^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=20.0 seed=447: `\int \frac{1}{25+16x^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=25.0 seed=658: `\int \frac{1}{16+4x^{2}}\,dx`

#### `arcsin_basic` — implemented

- **Description:** ∫ 1/√(1−x²) dx
- **Strategy:** `table_arcsin`
- **D gate:** d_min=2, d_max=None, d_weight=2.0
- **OpenStax case:** §5.7
- **Book / section:** calculus-volume-1 / 5.7 Integrals Resulting in Inverse Trigonometric Functions
- **type_id / leaves:** `calc_indef_int_inverse_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=3.0 seed=92: `\int \frac{1}{\sqrt{1-x^{2}}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=0.0 seed=41: `\int \frac{1}{1+x^{2}}\,dx` _type_id sibling `calc_indef_int_inverse_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=8.0 seed=177: `\int \frac{1}{\sqrt{16-x^{2}}}\,dx` _type_id sibling `calc_indef_int_inverse_trigonometric` (not form_id-exact)_

#### `arcsin_a2` — implemented

- **Description:** ∫ 1/√(a²−x²) dx
- **Strategy:** `table_arcsin`
- **D gate:** d_min=4, d_max=None, d_weight=1.8
- **OpenStax case:** §5.7
- **Book / section:** calculus-volume-1 / 5.7 Integrals Resulting in Inverse Trigonometric Functions
- **type_id / leaves:** `calc_indef_int_inverse_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=8.0 seed=177: `\int \frac{1}{\sqrt{16-x^{2}}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=12.0 seed=311: `\int \frac{1}{\sqrt{25-x^{2}}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=20.0 seed=573: `\int \frac{1}{\sqrt{9-x^{2}}}\,dx`

#### `arcsin_scaled` — implemented

- **Description:** ∫ 1/√(a²−b²x²) dx
- **Strategy:** `table_arcsin_scaled`
- **D gate:** d_min=8, d_max=None, d_weight=1.6
- **OpenStax case:** §5.7 scaled
- **Book / section:** calculus-volume-1 / 5.7 Integrals Resulting in Inverse Trigonometric Functions
- **type_id / leaves:** `calc_indef_int_inverse_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=16.0 seed=313: `\int \frac{1}{\sqrt{4-9x^{2}}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=0.0 seed=41: `\int \frac{1}{1+x^{2}}\,dx` _type_id sibling `calc_indef_int_inverse_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric` D=3.0 seed=92: `\int \frac{1}{\sqrt{1-x^{2}}}\,dx` _type_id sibling `calc_indef_int_inverse_trigonometric` (not form_id-exact)_

## Calc1 — Integrals (u-substitution)

### Catalog `u_substitution`

- **Title:** OpenStax u-substitution — explicit form taxonomy
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/u_substitution.json`
- **OpenStax:** calculus-volume-1 — 5.5 Substitution
- **URL:** https://openstax.org/books/calculus-volume-1/pages/5-5-substitution
- **Stage-1 mining:** `scripts/output/example_mining/calculus-volume-1/stage1/5-5-substitution.json`
- **Forms:** 14 (implemented=13, stub=1, deferred=0)
- **Taxonomy notes:** Forms enumerate textbook-visible u-sub patterns: power of linear/quadratic, du/u, exp-of-trig, trig-of-u, arctan chain, alteration.

#### `power_linear_du` — implemented

- **Description:** ∫ a(ax+b)^n dx — visible constant du factor
- **Strategy:** `u_equals_linear`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** Example 5.30 — ∫ 6x(3x²+4)^4 (related power-of-poly)
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises / examples:**
  - `fs-id1170573385785` Example 1.30: `\int 6 x \left(\right. 3 x^{2} + 4 \left.\right)^{4} d x . ; y = \frac{1}{5} \left(\right. 3 x^{2} + 4 \left.\right)^{5} + 1 . ; y = \frac{1}{5} \left(\right. 3 x^{2} + 4 \left.\right)^{5} + 1 , ; \\ y^{'} & = \left(\...`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=793: `\int 2\left(2x + 6\right)^{2}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=859: `\int 3\left(3x + 3\right)^{2}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=985: `\int 4\left(4x - 1\right)^{3}\,dx`

#### `power_quad_x_du` — implemented

- **Description:** ∫ (x²+c)^n · 2x dx (or without 2 absorbed)
- **Strategy:** `u_equals_quad`
- **D gate:** d_min=4, d_max=None, d_weight=2.2
- **OpenStax case:** Checkpoint 5.25 / Example 5.31 — quadratic inner
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises / examples:**
  - `fs-id1170573430304` Checkpoint 1.25: `\int 3 x^{2} \left(\right. x^{3} - 3 \left.\right)^{2} d x .`
  - `fs-id1170571334083` Example 1.31: `\int z \sqrt{z^{2} - 5} d z .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=6.0 seed=895: `\int 2x\left(x^{2}+3\right)^{2}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=8.0 seed=995: `\int 2x\left(x^{2}+3\right)^{4}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=8.0 seed=1121: `\int 2x\left(x^{2}+4\right)^{5}\,dx`

#### `root_quad_x_du` — implemented

- **Description:** ∫ x √(x²±c) dx — alteration / root of quadratic
- **Strategy:** `u_equals_quad_root`
- **D gate:** d_min=6, d_max=None, d_weight=1.8
- **OpenStax case:** Example 5.31 — ∫ z√(z²−5) dz
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises / examples:**
  - `fs-id1170571334083` Example 1.31: `\int z \sqrt{z^{2} - 5} d z .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=12.0 seed=997: `\int x\sqrt{x^{2}+6}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=12.0 seed=1189: `\int x\sqrt{x^{2}+1}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_def_int_substitution_with_change_of_variables` D=6.0 seed=220: `\int x\sqrt{x^{2}+2}\,dx`

#### `du_over_u_linear` — implemented

- **Description:** ∫ a/(ax+b) dx → ln|ax+b|
- **Strategy:** `du_over_u`
- **D gate:** d_min=2, d_max=None, d_weight=2.0
- **OpenStax case:** §5.5 / §5.6 ln|g| forms
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=3.0 seed=844: `\int \frac{3}{3x + 4}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=3.0 seed=1036: `\int \frac{3}{3x}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=6.0 seed=1087: `\int \frac{2}{2x - 3}\,dx`

#### `du_over_u_trig` — implemented

- **Description:** ∫ sin/cos^n or cos/sin^n — u = cos or sin
- **Strategy:** `trig_power_u_sub`
- **D gate:** d_min=6, d_max=None, d_weight=2.0
- **OpenStax case:** Example 5.32 / Checkpoint 5.27 — trig substitution warmup
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises / examples:**
  - `fs-id1170573573975` Example 1.32: `\int \frac{\sin t}{\cos^{3} t} d t .`
  - `fs-id1170573733746` Checkpoint 1.27: `\int \frac{\cos t}{\sin^{2} t} d t .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` D=0.0 seed=425: `\int \frac{\sin(x)}{\cos^{3}(x)}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` D=0.0 seed=491: `\int \frac{\cos(x)}{\sin^{2}(x)}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=793: `\int 2\left(2x + 6\right)^{2}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_

#### `exp_of_trig` — implemented

- **Description:** ∫ e^{sin x} cos x dx (or e^{cos} sin)
- **Strategy:** `exp_composite_trig`
- **D gate:** d_min=8, d_max=None, d_weight=2.2
- **OpenStax case:** §5.6 composite e^{g} g'
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` D=12.0 seed=629: `\int e^{\cos(x)}\sin(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` D=12.0 seed=821: `\int e^{\sin(x)}\cos(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=793: `\int 2\left(2x + 6\right)^{2}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_

#### `exp_of_poly` — implemented

- **Description:** ∫ e^{ax+b} · a dx
- **Strategy:** `exp_linear`
- **D gate:** d_min=4, d_max=None, d_weight=1.8
- **OpenStax case:** §5.6 exponential substitution
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` D=6.0 seed=527: `\int 3e^{3x}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` D=8.0 seed=561: `\int 4e^{4x + 3}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` D=25.0 seed=850: `\int 4e^{4x + 6}\,dx`

#### `trig_of_linear` — implemented

- **Description:** ∫ cos(ax+b)·a or sin(ax+b)·a
- **Strategy:** `trig_of_u`
- **D gate:** d_min=4, d_max=None, d_weight=1.8
- **OpenStax case:** §5.5 trig of linear inner
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=793: `\int 2\left(2x + 6\right)^{2}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=859: `\int 3\left(3x + 3\right)^{2}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=985: `\int 4\left(4x - 1\right)^{3}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_

#### `arctan_of_linear` — implemented

- **Description:** ∫ a/(1+(ax+b)²) dx → arctan(ax+b)
- **Strategy:** `arctan_chain`
- **D gate:** d_min=10, d_max=None, d_weight=1.6
- **OpenStax case:** §5.7 invtrig via substitution
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric_with_substitution` D=12.0 seed=1238: `\int \frac{2}{1+(2x - 6)^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric_with_substitution` D=16.0 seed=1180: `\int \frac{2}{1+(2x - 1)^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_inverse_trigonometric_with_substitution` D=16.0 seed=1306: `\int \frac{2}{1+(2x + 5)^{2}}\,dx`

#### `ln_squared_chain` — implemented

- **Description:** ∫ (ln|g|/g)·g' → (1/2)(ln|g|)²
- **Strategy:** `ln_squared`
- **D gate:** d_min=12, d_max=None, d_weight=1.4
- **OpenStax case:** §5.6 higher log-chain
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` D=12.0 seed=695: `\int \frac{2}{2x - 1}\ln|2x - 1|\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` D=16.0 seed=889: `\int \frac{2}{2x + 3}\ln|2x + 3|\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=793: `\int 2\left(2x + 6\right)^{2}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_

#### `alteration_linear_over_root` — implemented

- **Description:** ∫ x/√(x−a) style alteration (rewrite then u-sub)
- **Strategy:** `alteration`
- **D gate:** d_min=10, d_max=None, d_weight=1.5
- **OpenStax case:** Example 5.33 — ∫ x/√(x−1) dx
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises / examples:**
  - `fs-id1170573426799` Example 1.33: `\int \frac{x}{\sqrt{x - 1}} d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=12.0 seed=1063: `\int \frac{x}{\sqrt{x-1}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=20.0 seed=1325: `\int \frac{x}{\sqrt{x-2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=793: `\int 2\left(2x + 6\right)^{2}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_

#### `nested_trig_exp` — implemented

- **Description:** ∫ e^{sin(kx)} cos(kx) with k≠1
- **Strategy:** `exp_composite_trig_scaled`
- **D gate:** d_min=14, d_max=None, d_weight=1.2
- **OpenStax case:** Scaled composite e^{g} g'
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` D=16.0 seed=763: `\int e^{\sin(2x)}\cos(2x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=793: `\int 2\left(2x + 6\right)^{2}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=859: `\int 3\left(3x + 3\right)^{2}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_

#### `sec2_of_u` — implemented

- **Description:** ∫ sec²(g)·g' → tan(g)
- **Strategy:** `sec2_chain`
- **D gate:** d_min=8, d_max=None, d_weight=1.5
- **OpenStax case:** §5.5 sec² chain
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=793: `\int 2\left(2x + 6\right)^{2}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=859: `\int 3\left(3x + 3\right)^{2}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=985: `\int 4\left(4x - 1\right)^{3}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_

#### `composite_ln_of_trig` — stub

- **Description:** ∫ cot = cos/sin → ln|sin| (trig du/u)
- **Strategy:** `du_over_u_trig_basic`
- **D gate:** d_min=8, d_max=None, d_weight=1.3
- **OpenStax case:** Related §3.2 / §5.5 rewrite-then-u
- **Book / section:** calculus-volume-1 / 5.5 Substitution
- **type_id / leaves:** `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution`
- **Gap reason:** Covered partly by trig_integrals basic_tan; dedicated cot form not yet separate
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=793: `\int 2\left(2x + 6\right)^{2}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=859: `\int 3\left(3x + 3\right)^{2}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_power_rule_with_substitution` D=0.0 seed=985: `\int 4\left(4x - 1\right)^{3}\,dx` _type_id sibling `calc_indef_int_power_rule_with_substitution` (not form_id-exact)_

## Calc1 — Integrals (trig integrals)

### Catalog `trig_integrals`

- **Title:** OpenStax trigonometric integrals — explicit form taxonomy
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/trig_integrals.json`
- **OpenStax:** calculus-volume-2 — 3.2 Trigonometric Integrals
- **URL:** https://openstax.org/books/calculus-volume-2/pages/3-2-trigonometric-integrals
- **Stage-1 mining:** `scripts/output/example_mining/calculus-volume-2/stage1/3-2-trigonometric-integrals.json`
- **Forms:** 25 (implemented=24, stub=0, deferred=1)
- **Taxonomy notes:** Forms mirror the cases OpenStax enumerates in §3.2 (sin/cos odd/even strategies; tan/sec even/odd; reduction; product-to-sum).

#### `basic_sin_kx` — implemented

- **Description:** ∫ sin(kx) dx — table form
- **Strategy:** `basic_antiderivative`
- **D gate:** d_min=0, d_max=10, d_weight=1.0
- **OpenStax case:** basic table / Vol.1 antiderivatives
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=3.0 seed=982: `\int \sin(4x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `basic_cos_kx` — implemented

- **Description:** ∫ cos(kx) dx — table form
- **Strategy:** `basic_antiderivative`
- **D gate:** d_min=0, d_max=10, d_weight=1.0
- **OpenStax case:** basic table / Vol.1 antiderivatives
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=931: `\int \cos(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=3.0 seed=856: `\int \cos(4x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `basic_sec2` — implemented

- **Description:** ∫ sec²(kx) dx → (1/k) tan(kx)
- **Strategy:** `basic_antiderivative`
- **D gate:** d_min=0, d_max=10, d_weight=1.0
- **OpenStax case:** basic table
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=3.0 seed=790: `\int \sec^{2}(2x)\,dx`

#### `basic_sec_tan` — implemented

- **Description:** ∫ sec x tan x dx → sec x
- **Strategy:** `basic_antiderivative`
- **D gate:** d_min=0, d_max=12, d_weight=1.0
- **OpenStax case:** §3.2 exercise 87
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165042815096` section_exercise: `\sin^{2} x = _______`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=931: `\int \cos(x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `basic_tan` — implemented

- **Description:** ∫ tan x dx → −ln|cos x|
- **Strategy:** `rewrite_sin_over_cos_u_sub`
- **D gate:** d_min=2, d_max=14, d_weight=1.2
- **OpenStax case:** §3.2 exercise 88 (scaled)
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=8.0 seed=941: `\int \tan(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `cos_j_sin` — implemented

- **Description:** ∫ cos^j x · sin x dx (u = cos x)
- **Strategy:** `u_equals_cos`
- **D gate:** d_min=4, d_max=None, d_weight=2.0
- **OpenStax case:** Example 3.8 — ∫ cos^j x sin x dx
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165043250980` Example 3.8: `\int \cos^{j} x \sin x d x ; \int \cos^{3} x \sin x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=12.0 seed=1009: `\int \cos^{3}(x)\sin(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `sin_j_cos` — implemented

- **Description:** ∫ sin^j x · cos x dx (u = sin x)
- **Strategy:** `u_equals_sin`
- **D gate:** d_min=4, d_max=None, d_weight=2.0
- **OpenStax case:** Checkpoint 3.5 — ∫ sin^4 x cos x dx
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165042964834` Checkpoint 3.5: `\int \sin^{4} x \cos x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=6.0 seed=1033: `\int \sin^{2}(x)\cos(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=25.0 seed=1230: `\int \sin^{5}(x)\cos(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `sin_odd_cos_any` — implemented

- **Description:** ∫ cos^j x sin^k x dx with k odd ≥ 3 — save one sin, use 1−cos²
- **Strategy:** `odd_sin_power`
- **D gate:** d_min=8, d_max=None, d_weight=2.5
- **OpenStax case:** Example 3.9 / 3.11 — k odd
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165043281403` Example 3.9: `\int \cos^{j} x \sin^{k} x d x ; \int \cos^{2} x \sin^{3} x d x .`
  - `fs-id1165043272282` Example 3.11: `\int \cos^{j} x \sin^{k} x d x ; \int \cos^{8} x \sin^{5} x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=12.0 seed=943: `\int \sin^{3}(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `cos_odd_sin_any` — implemented

- **Description:** ∫ cos^j x sin^k x dx with j odd ≥ 3 — save one cos, use 1−sin²
- **Strategy:** `odd_cos_power`
- **D gate:** d_min=8, d_max=None, d_weight=2.5
- **OpenStax case:** Checkpoint 3.6 / 3.8 — j odd
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165043248784` Checkpoint 3.6: `\int \cos^{3} x \sin^{2} x d x .`
  - `fs-id1165043210017` Checkpoint 3.8: `\int \cos^{3} x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=8.0 seed=875: `\int \cos^{5}(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=16.0 seed=1077: `\int \cos^{3}(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `sin_even_power` — implemented

- **Description:** ∫ sin^{2n} x dx — power-reduction / half-angle
- **Strategy:** `power_reduction_sin`
- **D gate:** d_min=6, d_max=None, d_weight=2.2
- **OpenStax case:** Example 3.10 / 3.12 — even power of sin
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165042936506` Example 3.10: `\sin x ; \int \sin^{2} x d x .`
  - `fs-id1165042707196` Example 3.12: `\int \cos^{j} x \sin^{k} x d x ; \int \sin^{4} x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=8.0 seed=1067: `\int \sin^{2}(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `cos_even_power` — implemented

- **Description:** ∫ cos^{2n} x dx (optionally cos²(ax)) — power-reduction
- **Strategy:** `power_reduction_cos`
- **D gate:** d_min=6, d_max=None, d_weight=2.2
- **OpenStax case:** Checkpoint 3.7 / 3.9
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165043096050` Checkpoint 3.7: `\int \cos^{2} x d x .`
  - `fs-id1165039562343` Checkpoint 3.9: `\int \cos^{2} (3 x) d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=6.0 seed=841: `\int \cos^{2}(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `sin_cos_both_even` — implemented

- **Description:** ∫ sin^{2m} x cos^{2n} x dx — both even; reduce via identities
- **Strategy:** `both_even_power_reduction`
- **D gate:** d_min=12, d_max=None, d_weight=2.0
- **OpenStax case:** §3.2 exercise 100 — ∫ sin² cos²
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=20.0 seed=1145: `\int \sin^{2}(x)\cos^{2}(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `product_sin_a_cos_b` — implemented

- **Description:** ∫ sin(ax) cos(bx) dx — product-to-sum, a≠b
- **Strategy:** `product_to_sum`
- **D gate:** d_min=10, d_max=None, d_weight=1.8
- **OpenStax case:** Example 3.13 — different angles
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165043094091` Example 3.13: `\int \sin (a x) \cos (b x) d x ; \int \sin (5 x) \cos (3 x) d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=25.0 seed=1356: `\int \sin(2x)\cos(3x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `product_cos_a_cos_b` — implemented

- **Description:** ∫ cos(ax) cos(bx) dx — product-to-sum, a≠b
- **Strategy:** `product_to_sum`
- **D gate:** d_min=10, d_max=None, d_weight=1.6
- **OpenStax case:** Checkpoint 3.10
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165042707106` Checkpoint 3.10: `\int \cos (6 x) \cos (5 x) d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=931: `\int \cos(x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `sec_j_tan` — implemented

- **Description:** ∫ sec^j x · tan x dx (u = sec x)
- **Strategy:** `u_equals_sec`
- **D gate:** d_min=8, d_max=None, d_weight=2.0
- **OpenStax case:** Example 3.14 — ∫ sec^j tan
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165043183813` Example 3.14: `\int \sec^{j} x \tan x d x ; \int \sec^{5} x \tan x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=12.0 seed=1135: `\int \sec^{5}(x)\tan(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `tan_k_sec2` — implemented

- **Description:** ∫ tan^k x · sec² x dx (u = tan x)
- **Strategy:** `u_equals_tan`
- **D gate:** d_min=8, d_max=None, d_weight=2.0
- **OpenStax case:** Checkpoint 3.11 — ∫ tan^5 sec²
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165042708857` Checkpoint 3.11: `\int \tan^{5} x \sec^{2} x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=931: `\int \cos(x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `tan2` — implemented

- **Description:** ∫ tan² x dx = ∫(sec² x − 1) dx
- **Strategy:** `pythagorean_rewrite`
- **D gate:** d_min=6, d_max=None, d_weight=2.0
- **OpenStax case:** Pythagorean identity case (feeds reduction / tan^n)
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=931: `\int \cos(x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `tan_sec_sec_even` — implemented

- **Description:** ∫ tan^k x sec^j x dx with j even ≥ 4 — save sec², rewrite rest via tan²+1
- **Strategy:** `sec_even`
- **D gate:** d_min=14, d_max=None, d_weight=1.8
- **OpenStax case:** Example 3.15 — j even
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165042707642` Example 3.15: `\int \tan^{k} x \sec^{j} x d x ; j ; \int \tan^{6} x \sec^{4} x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=16.0 seed=1011: `\int \tan^{2}(x)\sec^{4}(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `tan_odd_sec_any` — implemented

- **Description:** ∫ tan^k x sec^j x dx with k odd ≥ 3 — save one tan·sec, rewrite via sec²−1
- **Strategy:** `tan_odd`
- **D gate:** d_min=14, d_max=None, d_weight=1.8
- **OpenStax case:** Example 3.16 / Checkpoint 3.12 — k odd
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165042527092` Example 3.16: `\int \tan^{k} x \sec^{j} x d x ; k ; \int \tan^{5} x \sec^{3} x d x .`
  - `fs-id1165042808795` Checkpoint 3.12: `\int \tan^{3} x \sec^{7} x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=20.0 seed=1271: `\int \tan^{3}(x)\sec(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `tan_odd_alone` — implemented

- **Description:** ∫ tan^{2n+1} x dx, n≥1 — rewrite tan^{2n}·tan = (sec²−1)^n tan
- **Strategy:** `tan_odd_alone`
- **D gate:** d_min=12, d_max=None, d_weight=1.8
- **OpenStax case:** Example 3.17 — ∫ tan³ x
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165043327268` Example 3.17: `\int \tan^{k} x d x ; k ; k \geq 3 ; \int \tan^{3} x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=931: `\int \cos(x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `sec3_reduction` — implemented

- **Description:** ∫ sec³ x dx — parts / reduction formula
- **Strategy:** `reduction_sec`
- **D gate:** d_min=16, d_max=None, d_weight=1.5
- **OpenStax case:** Example 3.18 / 3.19 — sec³
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165043311678` Example 3.18: `\int \sec^{3} x d x ; \int \sec^{3} x d x .`
  - `fs-id1165042445770` Example 3.19: `\int \sec^{3} x d x ; \int \sec^{3} x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=20.0 seed=1079: `\int \sec^{3}(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `tan_even_reduction` — implemented

- **Description:** ∫ tan^{2n} x dx via reduction / Pythagorean (n≥2)
- **Strategy:** `reduction_tan`
- **D gate:** d_min=16, d_max=None, d_weight=1.5
- **OpenStax case:** Example 3.20 — ∫ tan⁴ x
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165042599295` Example 3.20: `\int \tan^{4} x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=931: `\int \cos(x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `sec_odd_reduction_n5` — implemented

- **Description:** ∫ sec^5 x dx — reduction formula (higher odd)
- **Strategy:** `reduction_sec`
- **D gate:** d_min=18, d_max=None, d_weight=1.0
- **OpenStax case:** Checkpoint 3.13 — sec⁵
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises / examples:**
  - `fs-id1165043301703` Checkpoint 3.13: `\int \sec^{5} x d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=931: `\int \cos(x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `product_sin_a_sin_b` — implemented

- **Description:** ∫ sin(ax) sin(bx) dx — product-to-sum
- **Strategy:** `product_to_sum`
- **D gate:** d_min=12, d_max=None, d_weight=1.2
- **OpenStax case:** §3.2 product identities sibling of sin·cos / cos·cos
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=16.0 seed=1203: `\int \sin(6x)\sin(2x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

#### `weierstrass_t_sub` — deferred

- **Description:** Weierstrass t = tan(x/2) rationalization (other strategies §3.5)
- **Strategy:** `weierstrass`
- **D gate:** d_min=20, d_max=None, d_weight=0.5
- **OpenStax case:** Vol.2 §3.5 other strategies (not primary §3.2)
- **Book / section:** calculus-volume-2 / 3.2 Trigonometric Integrals
- **type_id / leaves:** `calc_indef_int_trigonometric`
- **Gap reason:** Belongs with other-strategies catalog; not §3.2 core cases
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=739: `\int \sec^{2}(5x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=805: `\int \sec^{2}(6x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric` D=0.0 seed=931: `\int \cos(x)\,dx` _type_id sibling `calc_indef_int_trigonometric` (not form_id-exact)_

## Calc1 — Integrals (trig substitution)

### Catalog `trig_substitution`

- **Title:** OpenStax trigonometric substitution — form taxonomy
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/trig_substitution.json`
- **OpenStax:** calculus-volume-2 — 3.3 Trigonometric Substitution
- **URL:** https://openstax.org/books/calculus-volume-2/pages/3-3-trigonometric-substitution
- **Stage-1 mining:** `scripts/output/example_mining/calculus-volume-2/stage1/3-3-trigonometric-substitution.json`
- **Forms:** 15 (implemented=13, stub=1, deferred=1)
- **Taxonomy notes:** a²−x² (x=a sinθ), a²+x² (x=a tanθ), x²−a² (x=a secθ); fractional powers ±3/2 ±5/2; optional linear wrap u=x+b.

#### `sqrt_a2_minus_x2` — implemented

- **Description:** ∫ √(a²−x²) dx — x = a sin θ
- **Strategy:** `sin_sub`
- **D gate:** d_min=0, d_max=None, d_weight=2.2
- **OpenStax case:** Example 3.21
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises / examples:**
  - `fs-id1165041837235` Example 3.21: `\sqrt{a^{2} - x^{2}} ; \int^{​} \sqrt{9 - x^{2}} d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=899: `\int \sqrt{9-x^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=1025: `\int \sqrt{16-x^{2}}\,dx`

#### `sqrt_a2_plus_x2` — implemented

- **Description:** ∫ √(a²+x²) dx — x = a tan θ
- **Strategy:** `tan_sub`
- **D gate:** d_min=2, d_max=None, d_weight=2.0
- **OpenStax case:** §3.3 a²+x² family
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=3.0 seed=950: `\int \sqrt{25+x^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=16.0 seed=1105: `\int \sqrt{4+x^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

#### `sqrt_x2_minus_a2` — implemented

- **Description:** ∫ √(x²−a²) dx — x = a sec θ
- **Strategy:** `sec_sub`
- **D gate:** d_min=4, d_max=None, d_weight=2.0
- **OpenStax case:** §3.3 x²−a² family
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=6.0 seed=1001: `\int \sqrt{x^{2}-16}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=8.0 seed=1161: `\int \sqrt{x^{2}-4}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

#### `one_over_sqrt_x2_plus_a2` — implemented

- **Description:** ∫ 1/√(x²+a²) dx
- **Strategy:** `tan_sub`
- **D gate:** d_min=4, d_max=None, d_weight=2.0
- **OpenStax case:** Example 3.24
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises / examples:**
  - `fs-id1165042089656` Example 3.24: `\sqrt{a^{2} + x^{2}} ; \int \frac{d x}{\sqrt{1 + x^{2}}}`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=6.0 seed=1127: `\int \frac{1}{\sqrt{x^{2}+25}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=12.0 seed=1103: `\int \frac{1}{\sqrt{x^{2}+4}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=20.0 seed=1365: `\int \frac{1}{\sqrt{\left(x - 2\right)^{2}+4}}\,dx`

#### `one_over_sqrt_x2_minus_a2` — implemented

- **Description:** ∫ 1/√(x²−a²) dx
- **Strategy:** `sec_sub`
- **D gate:** d_min=6, d_max=None, d_weight=1.8
- **OpenStax case:** §3.3
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=6.0 seed=935: `\int \frac{1}{\sqrt{x^{2}-25}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=899: `\int \sqrt{9-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

#### `x2_over_sqrt_a2_minus_x2` — implemented

- **Description:** ∫ x²/√(a²−x²) dx
- **Strategy:** `sin_sub`
- **D gate:** d_min=8, d_max=None, d_weight=1.8
- **OpenStax case:** Checkpoint 3.14 related
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises / examples:**
  - `fs-id1165042094001` Checkpoint 3.14: `\int \frac{x^{3}}{\sqrt{25 - x^{2}}} d x`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=8.0 seed=1035: `\int \frac{x^{2}}{\sqrt{25-x^{2}}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=16.0 seed=1297: `\int \frac{x^{2}}{\sqrt{9-x^{2}}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

#### `one_over_x2_sqrt_x2_plus_a2` — implemented

- **Description:** ∫ 1/(x² √(x²+a²)) dx
- **Strategy:** `tan_sub`
- **D gate:** d_min=10, d_max=None, d_weight=1.5
- **OpenStax case:** §3.3 denser rational×sqrt
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=899: `\int \sqrt{9-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=1025: `\int \sqrt{16-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

#### `pow_3_2_a2_minus` — implemented

- **Description:** ∫ (a²−x²)^{3/2} dx
- **Strategy:** `sin_sub`
- **D gate:** d_min=10, d_max=None, d_weight=1.6
- **OpenStax case:** §3.3 fractional power
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=12.0 seed=1229: `\int \left(4-x^{2}\right)^{\frac{3}{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=899: `\int \sqrt{9-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

#### `pow_3_2_a2_plus` — implemented

- **Description:** ∫ (a²+x²)^{3/2} dx
- **Strategy:** `tan_sub`
- **D gate:** d_min=10, d_max=None, d_weight=1.5
- **OpenStax case:** §3.3
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=899: `\int \sqrt{9-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=1025: `\int \sqrt{16-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

#### `pow_m3_2_a2_plus` — implemented

- **Description:** ∫ 1/(a²+x²)^{3/2} dx
- **Strategy:** `tan_sub`
- **D gate:** d_min=12, d_max=None, d_weight=1.5
- **OpenStax case:** §3.3
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=25.0 seed=1324: `\int \frac{1}{\left(4+x^{2}\right)^{\frac{3}{2}}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=25.0 seed=1450: `\int \frac{1}{\left(25+x^{2}\right)^{\frac{3}{2}}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

#### `pow_m3_2_a2_minus` — implemented

- **Description:** ∫ 1/(a²−x²)^{3/2} dx
- **Strategy:** `sin_sub`
- **D gate:** d_min=12, d_max=None, d_weight=1.5
- **OpenStax case:** §3.3
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=12.0 seed=1037: `\int \frac{1}{\left(9-x^{2}\right)^{\frac{3}{2}}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=20.0 seed=1173: `\int \frac{1}{\left(4-\left(x + 3\right)^{2}\right)^{\frac{3}{2}}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

#### `pow_m5_2_a2_plus` — implemented

- **Description:** ∫ 1/(a²+x²)^{5/2} dx
- **Strategy:** `tan_sub`
- **D gate:** d_min=16, d_max=None, d_weight=1.2
- **OpenStax case:** §3.3 high fractional
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=899: `\int \sqrt{9-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=1025: `\int \sqrt{16-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

#### `pow_5_2_a2_minus` — implemented

- **Description:** ∫ (a²−x²)^{5/2} dx
- **Strategy:** `sin_sub`
- **D gate:** d_min=16, d_max=None, d_weight=1.2
- **OpenStax case:** §3.3
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=16.0 seed=1171: `\int \left(25-x^{2}\right)^{\frac{5}{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=899: `\int \sqrt{9-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

#### `sqrt_over_x_a2_minus` — stub

- **Description:** ∫ √(a²−x²)/x dx
- **Strategy:** `sin_sub`
- **D gate:** d_min=10, d_max=None, d_weight=1.4
- **OpenStax case:** Example 3.22
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Gap reason:** Needs dedicated closed-form template (ln + sqrt mix)
- **Cited exercises / examples:**
  - `fs-id1165042229562` Example 3.22: `\sqrt{a^{2} - x^{2}} ; \int \frac{\sqrt{4 - x^{2}}}{x} d x .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=899: `\int \sqrt{9-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=1025: `\int \sqrt{16-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

#### `sinh_alternate_a2_plus` — deferred

- **Description:** ∫ 1/√(1+x²) via x=sinh θ (alternate)
- **Strategy:** `hyperbolic_sub`
- **D gate:** d_min=18, d_max=None, d_weight=0.5
- **OpenStax case:** Example 3.25 — hyperbolic alternate
- **Book / section:** calculus-volume-2 / 3.3 Trigonometric Substitution
- **type_id / leaves:** `calc_indef_int_trigonometric_with_substitution`
- **Gap reason:** Hyperbolic path not in primary Calc1 algebraic sampler
- **Cited exercises / examples:**
  - `fs-id1165042301696` Example 3.25: `\int \frac{d x}{\sqrt{1 + x^{2}}} ; x = \text{sinh} \theta ; \int \frac{d x}{\sqrt{1 + x^{2}}} . ; x = \tan \theta . ; y = \text{sinh}^{−1} x . ; \text{sinh} y = x . ; \frac{e^{y} - e^{− y}}{2} = x . ; 2 e^{y} ; e^{2 ...`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=833: `\int \sqrt{4-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=899: `\int \sqrt{9-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_trigonometric_with_substitution` D=0.0 seed=1025: `\int \sqrt{16-x^{2}}\,dx` _type_id sibling `calc_indef_int_trigonometric_with_substitution` (not form_id-exact)_

## Calc1 — Integrals (integration by parts)

### Catalog `integration_by_parts`

- **Title:** OpenStax integration by parts — LIATE form taxonomy
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/integration_by_parts.json`
- **OpenStax:** calculus-volume-2 — 3.1 Integration by Parts
- **URL:** https://openstax.org/books/calculus-volume-2/pages/3-1-integration-by-parts
- **Mining note:** Section not yet in stage-1 mining dump; taxonomy from OpenStax Vol.2 §3.1
- **Forms:** 12 (implemented=10, stub=1, deferred=1)
- **Taxonomy notes:** LIATE families: poly×ln, poly×exp, poly×trig, tabular/repeated parts, cyclic e^x sin/cos.

#### `ln_alone` — implemented

- **Description:** ∫ ln x dx — u=ln, dv=dx
- **Strategy:** `parts_ln`
- **D gate:** d_min=0, d_max=None, d_weight=1.5
- **OpenStax case:** §3.1 classic ∫ ln x
- **Book / section:** calculus-volume-2 / 3.1 Integration by Parts
- **type_id / leaves:** `calc_indef_int_integration_by_parts`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=0.0 seed=386: `\int \ln(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_differentials` D=12.0 seed=349: `\text{For }y=\ln|x|,\text{ find }dy.` _alias `ln`_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_logarithmic_rule_and_exponentials` D=0.0 seed=605: `\int \frac{1}{x}\,dx` _alias `ln`_

#### `poly1_ln` — implemented

- **Description:** ∫ x ln x dx
- **Strategy:** `parts_poly_ln`
- **D gate:** d_min=4, d_max=None, d_weight=2.0
- **OpenStax case:** §3.1 poly × ln
- **Book / section:** calculus-volume-2 / 3.1 Integration by Parts
- **type_id / leaves:** `calc_indef_int_integration_by_parts`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=6.0 seed=488: `\int x\ln(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=0.0 seed=386: `\int \ln(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=503: `\int xe^{x}\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_

#### `poly1_exp` — implemented

- **Description:** ∫ x e^x dx
- **Strategy:** `parts_poly_exp`
- **D gate:** d_min=2, d_max=None, d_weight=2.2
- **OpenStax case:** §3.1 poly × exp
- **Book / section:** calculus-volume-2 / 3.1 Integration by Parts
- **type_id / leaves:** `calc_indef_int_integration_by_parts`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=503: `\int xe^{x}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=0.0 seed=386: `\int \ln(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=629: `\int x\sin(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_

#### `poly1_sin` — implemented

- **Description:** ∫ x sin x dx
- **Strategy:** `parts_poly_trig`
- **D gate:** d_min=2, d_max=None, d_weight=2.0
- **OpenStax case:** §3.1 poly × sin
- **Book / section:** calculus-volume-2 / 3.1 Integration by Parts
- **type_id / leaves:** `calc_indef_int_integration_by_parts`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=629: `\int x\sin(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=0.0 seed=386: `\int \ln(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=503: `\int xe^{x}\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_

#### `poly1_cos` — implemented

- **Description:** ∫ x cos x dx
- **Strategy:** `parts_poly_trig`
- **D gate:** d_min=2, d_max=None, d_weight=2.0
- **OpenStax case:** §3.1 poly × cos
- **Book / section:** calculus-volume-2 / 3.1 Integration by Parts
- **type_id / leaves:** `calc_indef_int_integration_by_parts`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=6.0 seed=554: `\int x\cos(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=0.0 seed=386: `\int \ln(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=503: `\int xe^{x}\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_

#### `poly2_exp` — implemented

- **Description:** ∫ x² e^x dx — tabular / repeated parts
- **Strategy:** `tabular_parts`
- **D gate:** d_min=10, d_max=None, d_weight=2.0
- **OpenStax case:** §3.1 repeated / tabular
- **Book / section:** calculus-volume-2 / 3.1 Integration by Parts
- **type_id / leaves:** `calc_indef_int_integration_by_parts`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=0.0 seed=386: `\int \ln(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=503: `\int xe^{x}\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=629: `\int x\sin(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_

#### `poly2_sin` — implemented

- **Description:** ∫ x² sin x dx — repeated parts
- **Strategy:** `tabular_parts`
- **D gate:** d_min=14, d_max=None, d_weight=1.8
- **OpenStax case:** §3.1 repeated poly×trig
- **Book / section:** calculus-volume-2 / 3.1 Integration by Parts
- **type_id / leaves:** `calc_indef_int_integration_by_parts`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=16.0 seed=850: `\int x^{2}\sin(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=0.0 seed=386: `\int \ln(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=503: `\int xe^{x}\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_

#### `cyclic_exp_sin` — implemented

- **Description:** ∫ e^x sin x dx — cyclic parts
- **Strategy:** `cyclic_parts`
- **D gate:** d_min=12, d_max=None, d_weight=2.0
- **OpenStax case:** §3.1 cyclic e^x sin x
- **Book / section:** calculus-volume-2 / 3.1 Integration by Parts
- **type_id / leaves:** `calc_indef_int_integration_by_parts`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=12.0 seed=656: `\int e^{x}\sin(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=0.0 seed=386: `\int \ln(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=503: `\int xe^{x}\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_

#### `cyclic_exp_cos` — implemented

- **Description:** ∫ e^x cos x dx — cyclic parts
- **Strategy:** `cyclic_parts`
- **D gate:** d_min=12, d_max=None, d_weight=1.8
- **OpenStax case:** §3.1 cyclic e^x cos x
- **Book / section:** calculus-volume-2 / 3.1 Integration by Parts
- **type_id / leaves:** `calc_indef_int_integration_by_parts`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=20.0 seed=726: `\int e^{x}\cos(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=0.0 seed=386: `\int \ln(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=503: `\int xe^{x}\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_

#### `arctan_alone` — implemented

- **Description:** ∫ arctan x dx — parts with invtrig
- **Strategy:** `parts_invtrig`
- **D gate:** d_min=14, d_max=None, d_weight=1.2
- **OpenStax case:** §3.1 invtrig × 1
- **Book / section:** calculus-volume-2 / 3.1 Integration by Parts
- **type_id / leaves:** `calc_indef_int_integration_by_parts`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=20.0 seed=918: `\int \arctan(x)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=0.0 seed=386: `\int \ln(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=503: `\int xe^{x}\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_

#### `poly1_arcsin` — stub

- **Description:** ∫ x arcsin x dx
- **Strategy:** `parts_poly_invtrig`
- **D gate:** d_min=16, d_max=None, d_weight=1.0
- **OpenStax case:** §3.1 poly × arcsin
- **Book / section:** calculus-volume-2 / 3.1 Integration by Parts
- **type_id / leaves:** `calc_indef_int_integration_by_parts`
- **Gap reason:** Antiderivative messier; defer until answer-key template ready
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=0.0 seed=386: `\int \ln(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=503: `\int xe^{x}\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=629: `\int x\sin(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_

#### `sec3_via_parts` — deferred

- **Description:** ∫ sec³ x via parts (shared with trig integrals)
- **Strategy:** `parts_sec3`
- **D gate:** d_min=16, d_max=None, d_weight=0.8
- **OpenStax case:** Generated under trig_integrals.sec3_reduction
- **Book / section:** calculus-volume-2 / 3.1 Integration by Parts
- **type_id / leaves:** `calc_indef_int_integration_by_parts`
- **Gap reason:** Owned by trig_integrals catalog to avoid double-routing
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=0.0 seed=386: `\int \ln(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=503: `\int xe^{x}\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_integration_by_parts` D=3.0 seed=629: `\int x\sin(x)\,dx` _type_id sibling `calc_indef_int_integration_by_parts` (not form_id-exact)_

## Calc1 — Integrals (partial fractions)

### Catalog `partial_fractions`

- **Title:** OpenStax partial fractions integrals — form taxonomy
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/partial_fractions.json`
- **OpenStax:** calculus-volume-2 — 3.4 Partial Fractions
- **URL:** https://openstax.org/books/calculus-volume-2/pages/3-4-partial-fractions
- **Mining note:** Section not yet in stage-1 mining; taxonomy from OpenStax Vol.2 §3.4
- **Forms:** 11 (implemented=9, stub=2, deferred=0)
- **Taxonomy notes:** Distinct linear → ln; repeated linear → 1/(x−a)^k; irreducible quadratic → arctan/ln; mixed; multi-trick u_sub→PFD as separate form_ids.

#### `distinct_linear_2` — implemented

- **Description:** ∫ (Ax+B)/((x−r1)(x−r2)) — two distinct linear factors
- **Strategy:** `pfd_linear`
- **D gate:** d_min=0, d_max=None, d_weight=2.2
- **OpenStax case:** §3.4 distinct linear
- **Book / section:** calculus-volume-2 / 3.4 Partial Fractions
- **type_id / leaves:** `calc_indef_int_partial_fractions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=0.0 seed=984: `\int \frac{4x - 6}{x^{2} - 2x}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=0.0 seed=1050: `\int \frac{-5x + 11}{x^{2} - 4x + 3}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=0.0 seed=1176: `\int \frac{4x - 2}{x^{2} - x - 6}\,dx`

#### `distinct_linear_3` — implemented

- **Description:** ∫ rational with three distinct linear factors
- **Strategy:** `pfd_linear`
- **D gate:** d_min=8, d_max=None, d_weight=1.8
- **OpenStax case:** §3.4 three linears
- **Book / section:** calculus-volume-2 / 3.4 Partial Fractions
- **type_id / leaves:** `calc_indef_int_partial_fractions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=8.0 seed=1186: `\int \frac{-6x^{2} + 9x - 12}{3\left(x + 1\right)\left(x\right)\left(x - 2\right)}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=8.0 seed=1312: `\int \frac{-5x + 9}{\left(x - 3\right)\left(x - 2\right)\left(x - 1\right)}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=16.0 seed=1448: `\int \frac{2x^{2} + 4x - 28}{\left(x + 2\right)\left(x - 2\right)\left(x - 5\right)}\,dx`

#### `irreducible_quad_arctan` — implemented

- **Description:** ∫ C/(x²+a²) → (C/a) arctan(x/a)
- **Strategy:** `pfd_arctan`
- **D gate:** d_min=6, d_max=None, d_weight=2.0
- **OpenStax case:** §3.4 irreducible quadratic → arctan
- **Book / section:** calculus-volume-2 / 3.4 Partial Fractions
- **type_id / leaves:** `calc_indef_int_partial_fractions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=6.0 seed=1086: `\int \frac{-4}{x^{2} + 1}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=6.0 seed=1152: `\int \frac{8}{2x^{2} + 8}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=12.0 seed=1380: `\int \frac{\left(\left(2 + 2\right)\right)\left(4\right)}{\left(\left(2 + 2\right)\right)\left(2x^{2} + 2\right)}\,dx`

#### `irreducible_quad_ln` — implemented

- **Description:** ∫ Bx/(x²+a²) → (B/2) ln(x²+a²)
- **Strategy:** `pfd_quad_ln`
- **D gate:** d_min=8, d_max=None, d_weight=1.6
- **OpenStax case:** §3.4 Bx/(x²+a²)
- **Book / section:** calculus-volume-2 / 3.4 Partial Fractions
- **type_id / leaves:** `calc_indef_int_partial_fractions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=8.0 seed=1120: `\int \frac{-2x}{x^{2} + 4}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=12.0 seed=1188: `\int \frac{4x}{2x^{2} + 8}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=16.0 seed=1322: `\int \frac{-4x}{x^{2} + 1}\,dx`

#### `mixed_linear_quad` — implemented

- **Description:** Linear factor(s) + irreducible quadratic
- **Strategy:** `pfd_mixed`
- **D gate:** d_min=10, d_max=None, d_weight=2.0
- **OpenStax case:** §3.4 mixed
- **Book / section:** calculus-volume-2 / 3.4 Partial Fractions
- **type_id / leaves:** `calc_indef_int_partial_fractions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=12.0 seed=1254: `\int \frac{18x^{2} - 20x + 8}{2x^{3} - 4x^{2} + 2x - 4}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=20.0 seed=1516: `\int \frac{x^{2} + 6x + 10}{x^{3} - x^{2} + 16x - 16}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=25.0 seed=1475: `\int \frac{x^{2} + x + 8}{x^{3} - x^{2} + 9x - 9}\,dx`

#### `repeated_linear_square` — implemented

- **Description:** ∫ A/(x−a)² dx (and optional B/(x−a))
- **Strategy:** `pfd_repeated`
- **D gate:** d_min=10, d_max=None, d_weight=1.8
- **OpenStax case:** §3.4 repeated linear
- **Book / section:** calculus-volume-2 / 3.4 Partial Fractions
- **type_id / leaves:** `calc_indef_int_partial_fractions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=16.0 seed=1256: `\int \frac{-3x + 6}{\left(x - 3\right)^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=25.0 seed=1409: `\int \frac{-4x - 8}{\left(x + 1\right)^{2}}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=0.0 seed=984: `\int \frac{4x - 6}{x^{2} - 2x}\,dx` _type_id sibling `calc_indef_int_partial_fractions` (not form_id-exact)_

#### `u_sub_then_pfd_exp` — implemented

- **Description:** ∫ R(e^x) e^x dx — u=e^x then PFD
- **Strategy:** `pipeline_u_pfd`
- **D gate:** d_min=12, d_max=None, d_weight=1.6
- **OpenStax case:** Multi-trick leaf / §3.4 after sub
- **Book / section:** calculus-volume-2 / 3.4 Partial Fractions
- **type_id / leaves:** `calc_indef_int_partial_fractions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_multi_trick` D=0.0 seed=514: `\int 4\frac{0\left(4x - 1\right)+2}{\left(4x - 1-2\right)\left(4x - 1-1\right)}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_multi_trick` D=0.0 seed=706: `\int \frac{3\left(e^{2x}\right)-5}{\left(e^{2x}-3\right)\left(e^{2x}-1\right)}\cdot 2e^{2x}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_multi_trick` D=3.0 seed=565: `\int 4\frac{5\left(4x + 4\right)+9}{\left(4x + 4\right)\left(4x + 4+3\right)}\,dx`

#### `u_sub_then_pfd_trig` — implemented

- **Description:** ∫ R(sin x) cos x dx — u=sin then PFD
- **Strategy:** `pipeline_u_pfd`
- **D gate:** d_min=12, d_max=None, d_weight=1.6
- **OpenStax case:** Multi-trick leaf
- **Book / section:** calculus-volume-2 / 3.4 Partial Fractions
- **type_id / leaves:** `calc_indef_int_partial_fractions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_multi_trick` D=0.0 seed=580: `\int \frac{6\left(\cos(4x)\right)+6}{\left(\cos(4x)-1\right)\left(\cos(4x)+3\right)}\left(-4\sin(4x)\right)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_multi_trick` D=6.0 seed=808: `\int \frac{-2\left(\cos(x)\right)+6}{\left(\cos(x)-2\right)\left(\cos(x)-1\right)}\left(-\sin(x)\right)\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_multi_trick` D=8.0 seed=716: `\int \frac{3}{\left(\sin(x)\right)^{2}+9}\cdot \cos(x)\,dx`

#### `u_sub_then_pfd_log` — implemented

- **Description:** ∫ R(ln x)/x dx — u=ln then PFD
- **Strategy:** `pipeline_u_pfd`
- **D gate:** d_min=14, d_max=None, d_weight=1.3
- **OpenStax case:** Multi-trick leaf
- **Book / section:** calculus-volume-2 / 3.4 Partial Fractions
- **type_id / leaves:** `calc_indef_int_partial_fractions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_multi_trick` D=6.0 seed=616: `\int \frac{-3\left(\ln|3x - 6|\right)-18}{\left(\ln|3x - 6|+4\right)\left(\ln|3x - 6|-2\right)}\frac{3}{3x - 6}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_multi_trick` D=8.0 seed=650: `\int \frac{3\left(\ln|3x - 1|\right)}{\left(\ln|3x - 1|\right)^{2}+1}\frac{3}{3x - 1}\,dx`
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_multi_trick` D=8.0 seed=842: `\int \frac{-4\left(\ln|x - 5|\right)-4}{\left(\ln|x - 5|\right)^{2}+9}\frac{1}{x - 5}\,dx`

#### `repeated_linear_cube` — stub

- **Description:** ∫ A/(x−a)³ + B/(x−a)² + C/(x−a)
- **Strategy:** `pfd_repeated`
- **D gate:** d_min=16, d_max=None, d_weight=1.0
- **OpenStax case:** §3.4 multiplicity 3
- **Book / section:** calculus-volume-2 / 3.4 Partial Fractions
- **type_id / leaves:** `calc_indef_int_partial_fractions`
- **Gap reason:** Constructive PFD spine does not yet emit multiplicity≥3 dens
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=0.0 seed=984: `\int \frac{4x - 6}{x^{2} - 2x}\,dx` _type_id sibling `calc_indef_int_partial_fractions` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=0.0 seed=1050: `\int \frac{-5x + 11}{x^{2} - 4x + 3}\,dx` _type_id sibling `calc_indef_int_partial_fractions` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=0.0 seed=1176: `\int \frac{4x - 2}{x^{2} - x - 6}\,dx` _type_id sibling `calc_indef_int_partial_fractions` (not form_id-exact)_

#### `improper_long_division` — stub

- **Description:** Improper rational: divide then PFD
- **Strategy:** `long_division_then_pfd`
- **D gate:** d_min=14, d_max=None, d_weight=1.2
- **OpenStax case:** §3.4 improper rationals
- **Book / section:** calculus-volume-2 / 3.4 Partial Fractions
- **type_id / leaves:** `calc_indef_int_partial_fractions`
- **Gap reason:** Need long-division front-end before seed_partial_fraction_target
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=0.0 seed=984: `\int \frac{4x - 6}{x^{2} - 2x}\,dx` _type_id sibling `calc_indef_int_partial_fractions` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=0.0 seed=1050: `\int \frac{-5x + 11}{x^{2} - 4x + 3}\,dx` _type_id sibling `calc_indef_int_partial_fractions` (not form_id-exact)_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=0.0 seed=1176: `\int \frac{4x - 2}{x^{2} - x - 6}\,dx` _type_id sibling `calc_indef_int_partial_fractions` (not form_id-exact)_

## Precalculus

### Catalog `precalculus_function_ops`

- **Title:** OpenStax Precalculus 2e §1.4 Composition / function operations — form taxonomy
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/precalculus_function_ops.json`
- **OpenStax:** precalculus-2e — 1.4 Composition of Functions
- **URL:** https://openstax.org/books/precalculus-2e/pages/1-4-composition-of-functions
- **Stage-1 mining:** `scripts/output/example_mining/precalculus-2e/stage1/1-4-composition-of-functions.json`
- **Forms:** 8 (implemented=5, stub=1, deferred=2)
- **Taxonomy notes:** §1.4 learning objectives: algebraic ops on functions; create composition; evaluate composites; domain of composite; decompose composites.

#### `algebraic_sum` — implemented

- **Description:** Evaluate (f+g)(a)
- **Strategy:** `function_sum`
- **D gate:** d_min=0, d_max=None, d_weight=1.5
- **OpenStax case:** §1.4 Example 1 — algebraic operations (sum)
- **Book / section:** precalculus-2e / 1.4 Composition of Functions
- **type_id / leaves:** `pc_functions_operations`
- **Cited exercises / examples:**
  - `Example_01_04_01` Example 1: `(g - f) (x) ; \left(\right. \frac{g}{f} \left.\right) (x) , ; f (x) = x - 1 ; g (x) = x^{2} - 1.`
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=568: `\text{If } f(x) = 3x + 3 \text{ and } g(x) = 3x - 3, \text{ find } (f + g)(-4).`
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=634: `\text{If } f(x) = 3x - 4 \text{ and } g(x) = 3x + 4, \text{ find } (f + g)(-3).`
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=760: `\text{If } f(x) = 3x - 3 \text{ and } g(x) = -3x + 1, \text{ find } (f + g)(-3).`

#### `algebraic_difference` — implemented

- **Description:** Evaluate (f−g)(a) or (g−f)(a)
- **Strategy:** `function_difference`
- **D gate:** d_min=0, d_max=None, d_weight=1.5
- **OpenStax case:** §1.4 algebraic difference
- **Book / section:** precalculus-2e / 1.4 Composition of Functions
- **type_id / leaves:** `pc_functions_operations`
- **Cited exercises / examples:**
  - `Example_01_04_01` Example 1: `(g - f) (x) ; \left(\right. \frac{g}{f} \left.\right) (x) , ; f (x) = x - 1 ; g (x) = x^{2} - 1.`
  - `ti_01_04_09` Try It #1: `(f g) (x) ; (f - g) (x) . ; f (x) = x - 1 \text{and} g (x) = x^{2} - 1`
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=3.0 seed=685: `\text{If } f(x) = -3x + 0 \text{ and } g(x) = -3x - 2, \text{ find } (f - g)(-1).`
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=20.0 seed=1100: `\text{If } f(x) = 9x - 5 \text{ and } g(x) = 9x - 5, \text{ find } (f - g)(-9).`
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=568: `\text{If } f(x) = 3x + 3 \text{ and } g(x) = 3x - 3, \text{ find } (f + g)(-4).` _type_id sibling `pc_functions_operations` (not form_id-exact)_

#### `algebraic_product` — implemented

- **Description:** Evaluate (f·g)(a)
- **Strategy:** `function_product`
- **D gate:** d_min=6, d_max=None, d_weight=1.8
- **OpenStax case:** §1.4 product of functions
- **Book / section:** precalculus-2e / 1.4 Composition of Functions
- **type_id / leaves:** `pc_functions_operations`
- **Cited exercises / examples:**
  - `ti_01_04_09` Try It #1: `(f g) (x) ; (f - g) (x) . ; f (x) = x - 1 \text{and} g (x) = x^{2} - 1`
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=6.0 seed=862: `\text{If } f(x) = 6x - 4 \text{ and } g(x) = -6x + 2, \text{ find } (f \cdot g)(-2).`
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=12.0 seed=772: `\text{If } f(x) = 8x - 4 \text{ and } g(x) = -8x - 2, \text{ find } (f \cdot g)(-7).`
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=568: `\text{If } f(x) = 3x + 3 \text{ and } g(x) = 3x - 3, \text{ find } (f + g)(-4).` _type_id sibling `pc_functions_operations` (not form_id-exact)_

#### `algebraic_quotient` — implemented

- **Description:** Evaluate (f/g)(a)
- **Strategy:** `function_quotient`
- **D gate:** d_min=8, d_max=None, d_weight=1.6
- **OpenStax case:** §1.4 quotient of functions
- **Book / section:** precalculus-2e / 1.4 Composition of Functions
- **type_id / leaves:** `pc_functions_operations`
- **Cited exercises / examples:**
  - `Example_01_04_01` Example 1: `(g - f) (x) ; \left(\right. \frac{g}{f} \left.\right) (x) , ; f (x) = x - 1 ; g (x) = x^{2} - 1.`
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=8.0 seed=704: `\text{If } f(x) = 6x + 5 \text{ and } g(x) = -6x + 3, \text{ find } \left(\frac{f}{g}\right)(3).`
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=8.0 seed=770: `\text{If } f(x) = 6x + 6 \text{ and } g(x) = 6x + 2, \text{ find } \left(\frac{f}{g}\right)(4).`
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=16.0 seed=840: `\text{If } f(x) = 8x + 6 \text{ and } g(x) = -8x - 5, \text{ find } \left(\frac{f}{g}\right)(-2).`

#### `compose_evaluate` — implemented

- **Description:** Evaluate (f∘g)(a) = f(g(a))
- **Strategy:** `compose_eval`
- **D gate:** d_min=10, d_max=None, d_weight=2.2
- **OpenStax case:** §1.4 Example 2 — composition evaluate
- **Book / section:** precalculus-2e / 1.4 Composition of Functions
- **type_id / leaves:** `pc_functions_operations`
- **Cited exercises / examples:**
  - `Example_01_04_02` Example 2: `f \left(\right. g (x) \left.\right) ; g \left(\right. f (x) \left.\right) . ; f (x) = 2 x + 1 g (x) = 3 - x`
  - `Example_01_04_04` Example 4: `f (x) ; x ; g (y) ; y ; f \left(\right. g (y) \left.\right) ; g \left(\right. f (x) \left.\right) ?`
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=12.0 seed=964: `\text{If } f(x) = 8x - 8 \text{ and } g(x) = 8x - 4, \text{ find } (f \circ g)(6).`
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=16.0 seed=1032: `\text{If } f(x) = 8x + 2 \text{ and } g(x) = 8x - 2, \text{ find } (f \circ g)(4).`
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=20.0 seed=908: `\text{If } f(x) = -9x - 8 \text{ and } g(x) = 9x + 2, \text{ find } (f \circ g)(-8).`

#### `compose_expression` — stub

- **Description:** Find simplified rule for (f∘g)(x) as an expression
- **Strategy:** `compose_expand`
- **D gate:** d_min=12, d_max=None, d_weight=1.4
- **OpenStax case:** §1.4 find (f∘g)(x) simplified
- **Book / section:** precalculus-2e / 1.4 Composition of Functions
- **type_id / leaves:** `pc_functions_operations`
- **Cited exercises / examples:**
  - `Example_01_04_02` Example 2: `f \left(\right. g (x) \left.\right) ; g \left(\right. f (x) \left.\right) . ; f (x) = 2 x + 1 g (x) = 3 - x`
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=568: `\text{If } f(x) = 3x + 3 \text{ and } g(x) = 3x - 3, \text{ find } (f + g)(-4).` _type_id sibling `pc_functions_operations` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=634: `\text{If } f(x) = 3x - 4 \text{ and } g(x) = 3x + 4, \text{ find } (f + g)(-3).` _type_id sibling `pc_functions_operations` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=760: `\text{If } f(x) = 3x - 3 \text{ and } g(x) = -3x + 1, \text{ find } (f + g)(-3).` _type_id sibling `pc_functions_operations` (not form_id-exact)_

#### `domain_of_composite` — deferred

- **Description:** Domain of (f∘g)
- **Strategy:** `compose_domain`
- **D gate:** d_min=12, d_max=None, d_weight=1.0
- **OpenStax case:** §1.4 domain of a composite
- **Book / section:** precalculus-2e / 1.4 Composition of Functions
- **type_id / leaves:** `pc_functions_operations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=568: `\text{If } f(x) = 3x + 3 \text{ and } g(x) = 3x - 3, \text{ find } (f + g)(-4).` _type_id sibling `pc_functions_operations` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=634: `\text{If } f(x) = 3x - 4 \text{ and } g(x) = 3x + 4, \text{ find } (f + g)(-3).` _type_id sibling `pc_functions_operations` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=760: `\text{If } f(x) = 3x - 3 \text{ and } g(x) = -3x + 1, \text{ find } (f + g)(-3).` _type_id sibling `pc_functions_operations` (not form_id-exact)_

#### `decompose_composite` — deferred

- **Description:** Decompose h = f∘g into component functions
- **Strategy:** `decompose`
- **D gate:** d_min=14, d_max=None, d_weight=0.8
- **OpenStax case:** §1.4 decompose a composite
- **Book / section:** precalculus-2e / 1.4 Composition of Functions
- **type_id / leaves:** `pc_functions_operations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=568: `\text{If } f(x) = 3x + 3 \text{ and } g(x) = 3x - 3, \text{ find } (f + g)(-4).` _type_id sibling `pc_functions_operations` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=634: `\text{If } f(x) = 3x - 4 \text{ and } g(x) = 3x + 4, \text{ find } (f + g)(-3).` _type_id sibling `pc_functions_operations` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_functions_operations` D=0.0 seed=760: `\text{If } f(x) = 3x - 3 \text{ and } g(x) = -3x + 1, \text{ find } (f + g)(-3).` _type_id sibling `pc_functions_operations` (not form_id-exact)_

### Catalog `precalculus_exp_log`

- **Title:** OpenStax Precalculus 2e §4.5–4.6 Exp/Log properties & equations — form taxonomy
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/precalculus_exp_log.json`
- **OpenStax:** precalculus-2e — 4.6 Exponential and Logarithmic Equations
- **URL:** https://openstax.org/books/precalculus-2e/pages/4-6-exponential-and-logarithmic-equations
- **Stage-1 mining:** `scripts/output/example_mining/precalculus-2e/stage1/4-6-exponential-and-logarithmic-equations.json`
- **Forms:** 11 (implemented=8, stub=2, deferred=1)
- **Taxonomy notes:** §4.5: product, quotient, power rules; expand/condense; change of base.

#### `log_product_rule_expand` — implemented

- **Description:** Expand log(MN) → log M + log N
- **Strategy:** `log_product`
- **D gate:** d_min=0, d_max=None, d_weight=1.6
- **OpenStax case:** §4.5 Example 1 — product rule
- **Book / section:** precalculus-2e / 4.6 Exponential and Logarithmic Equations
- **type_id / leaves:** `pc_properties_of_logarithms`, `pc_writing_logs_in_terms_of_others`
- **Cited exercises / examples:**
  - `Example_04_05_01` Example 1: `log_{3} \left(\right. 30 x (3 x + 4) \left.\right) .`
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=0.0 seed=1030: `\text{Expand: } \log_{2}\left(32\right)`
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=0.0 seed=1096: `\text{Expand: } \log_{5}\left(24\right)`
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=3.0 seed=1081: `\text{Expand: } \log_{5}\left(18\right)`

#### `log_quotient_rule_expand` — implemented

- **Description:** Expand log(M/N) → log M − log N
- **Strategy:** `log_quotient`
- **D gate:** d_min=2, d_max=None, d_weight=1.6
- **OpenStax case:** §4.5 quotient rule
- **Book / section:** precalculus-2e / 4.6 Exponential and Logarithmic Equations
- **type_id / leaves:** `pc_properties_of_logarithms`, `pc_writing_logs_in_terms_of_others`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=3.0 seed=1273: `\text{Expand: } \log_{2}\left(\frac{30}{5}\right)`
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=6.0 seed=1132: `\text{Expand: } \log_{10}\left(\frac{24}{8}\right)`
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=12.0 seed=1234: `\text{Expand: } \log_{9}\left(\frac{4}{2}\right)`

#### `log_power_rule_expand` — implemented

- **Description:** Expand log(M^p) → p log M
- **Strategy:** `log_power`
- **D gate:** d_min=2, d_max=None, d_weight=1.6
- **OpenStax case:** §4.5 power rule
- **Book / section:** precalculus-2e / 4.6 Exponential and Logarithmic Equations
- **type_id / leaves:** `pc_properties_of_logarithms`, `pc_writing_logs_in_terms_of_others`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=3.0 seed=1147: `\text{Expand: } \log_{3}\left(9^{4}\right)`
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=8.0 seed=1358: `\text{Expand: } \log_{2}\left(3^{5}\right)`
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=20.0 seed=1562: `\text{Expand: } \log_{7}\left(6^{5}\right)`

#### `log_change_of_base` — implemented

- **Description:** Rewrite log_b(a) using change-of-base
- **Strategy:** `change_of_base`
- **D gate:** d_min=4, d_max=None, d_weight=2.0
- **OpenStax case:** §4.5 change-of-base formula
- **Book / section:** precalculus-2e / 4.6 Exponential and Logarithmic Equations
- **type_id / leaves:** `pc_properties_of_logarithms`, `pc_writing_logs_in_terms_of_others`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=0.0 seed=1222: `\text{Rewrite using change of base: } \log_{5}(3125)`
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=8.0 seed=1166: `\text{Rewrite using change of base: } \log_{2}(16)`
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=8.0 seed=1232: `\text{Rewrite using change of base: } \log_{4}(256)`

#### `exp_same_base` — implemented

- **Description:** Solve b^x = b^k by equating exponents
- **Strategy:** `same_base`
- **D gate:** d_min=0, d_max=None, d_weight=2.2
- **OpenStax case:** §4.6 Example 1 — common base
- **Book / section:** precalculus-2e / 4.6 Exponential and Logarithmic Equations
- **type_id / leaves:** `pc_exponential_equations_not_requiring_logarithms`
- **Cited exercises / examples:**
  - `Example_04_06_01` Example 1: `2^{x - 1} = 2^{2 x - 4} .`
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms` D=0.0 seed=700: `2^{x} = 2`
  - [gallery:a2_algebraic_gallery] type=`a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms` D=0.0 seed=766: `3^{x} = 3`
  - [gallery:a2_algebraic_gallery] type=`a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms` D=0.0 seed=892: `2^{x} = 4`

#### `exp_rewrite_common_base` — implemented

- **Description:** Rewrite both sides to a common base (e.g. 8=2³, 16=2⁴)
- **Strategy:** `rewrite_common_base`
- **D gate:** d_min=6, d_max=None, d_weight=2.0
- **OpenStax case:** §4.6 Example 2 — rewrite to common base
- **Book / section:** precalculus-2e / 4.6 Exponential and Logarithmic Equations
- **type_id / leaves:** `pc_exponential_equations_not_requiring_logarithms`
- **Cited exercises / examples:**
  - `Example_04_06_02` Example 2: `8^{x + 2} = 16^{x + 1} .`
  - `Example_04_06_03` Example 3: `2^{5 x} = \sqrt{2} .`
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_exponential_equations_not_requiring_logarithms` D=0.0 seed=575: `9^{x} = 27^{x - 1}`
  - [gallery:pc_algebraic_gallery] type=`pc_exponential_equations_not_requiring_logarithms` D=0.0 seed=641: `25^{x} = 5^{x + 2}`
  - [gallery:pc_algebraic_gallery] type=`pc_exponential_equations_not_requiring_logarithms` D=12.0 seed=779: `8^{x + 2} = 16^{x + 1}`

#### `exp_needs_logarithm` — implemented

- **Description:** Solve b^{cx} = k using logarithms
- **Strategy:** `take_log`
- **D gate:** d_min=6, d_max=None, d_weight=2.0
- **OpenStax case:** §4.6 use logarithms to solve exponential
- **Book / section:** precalculus-2e / 4.6 Exponential and Logarithmic Equations
- **type_id / leaves:** `pc_exponential_equations_requiring_logarithms`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_exponential_equations_requiring_logarithms` D=0.0 seed=788: `4^{3x} = 64`
  - [gallery:pc_algebraic_gallery] type=`pc_exponential_equations_requiring_logarithms` D=0.0 seed=854: `3^{-x} = 0.037037037037037035`
  - [gallery:pc_algebraic_gallery] type=`pc_exponential_equations_requiring_logarithms` D=0.0 seed=980: `3^{-x} = 0.3333333333333333`

#### `log_definition_equation` — implemented

- **Description:** Solve log_b(x) = k via definition x = b^k
- **Strategy:** `log_definition`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §4.6 definition of logarithm
- **Book / section:** precalculus-2e / 4.6 Exponential and Logarithmic Equations
- **type_id / leaves:** `pc_logarithmic_equations_simple`, `pc_logarithmic_equations_hard`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_logarithmic_equations_simple` D=0.0 seed=264: `\log_{4}(x) = 5` _type_id sibling `pc_logarithmic_equations_simple` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_logarithmic_equations_simple` D=0.0 seed=330: `\log_{2}(x) = 1` _type_id sibling `pc_logarithmic_equations_simple` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_logarithmic_equations_simple` D=0.0 seed=456: `\log_{5}(x) = 4` _type_id sibling `pc_logarithmic_equations_simple` (not form_id-exact)_

#### `log_one_to_one` — stub

- **Description:** Solve log_b(f(x)) = log_b(g(x)) by equating arguments
- **Strategy:** `log_1to1`
- **D gate:** d_min=10, d_max=None, d_weight=1.4
- **OpenStax case:** §4.6 one-to-one property of logs
- **Book / section:** precalculus-2e / 4.6 Exponential and Logarithmic Equations
- **type_id / leaves:** `pc_logarithmic_equations_hard`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `log_condense` — stub

- **Description:** Condense sum/difference of logs into a single log
- **Strategy:** `log_condense`
- **D gate:** d_min=8, d_max=None, d_weight=1.2
- **OpenStax case:** §4.5 condense logarithmic expressions
- **Book / section:** precalculus-2e / 4.6 Exponential and Logarithmic Equations
- **type_id / leaves:** `pc_properties_of_logarithms`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=0.0 seed=1030: `\text{Expand: } \log_{2}\left(32\right)` _type_id sibling `pc_properties_of_logarithms` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=0.0 seed=1096: `\text{Expand: } \log_{5}\left(24\right)` _type_id sibling `pc_properties_of_logarithms` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_properties_of_logarithms` D=0.0 seed=1222: `\text{Rewrite using change of base: } \log_{5}(3125)` _type_id sibling `pc_properties_of_logarithms` (not form_id-exact)_

#### `exp_log_models` — deferred

- **Description:** Applied growth/decay / logistic-style models
- **Strategy:** `exp_model`
- **D gate:** d_min=12, d_max=None, d_weight=0.6
- **OpenStax case:** §4.7 exponential and logarithmic models (gap)
- **Book / section:** precalculus-2e / 4.6 Exponential and Logarithmic Equations
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

### Catalog `precalculus_partial_fractions`

- **Title:** OpenStax Precalculus 2e §9.4 Partial Fractions — form taxonomy
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/precalculus_partial_fractions.json`
- **OpenStax:** precalculus-2e — 9.4 Partial Fractions
- **URL:** https://openstax.org/books/precalculus-2e/pages/9-4-partial-fractions
- **Mining note:** Section not in stage-1 mine (chs 1,4–7 only); taxonomy from OpenStax §9.4 headings
- **Forms:** 6 (implemented=4, stub=1, deferred=1)
- **Taxonomy notes:** OpenStax enumerates four Q(x) cases: nonrepeated linear; repeated linear; nonrepeated irreducible quadratic; repeated irreducible quadratic.

#### `nonrepeated_linear_2` — implemented

- **Description:** P/Q with exactly two distinct linear factors
- **Strategy:** `pfd_distinct_linear`
- **D gate:** d_min=0, d_max=14, d_weight=2.2
- **OpenStax case:** §9.4 Example 1 — nonrepeated linear factors
- **Book / section:** precalculus-2e / 9.4 Partial Fractions
- **type_id / leaves:** `pc_partial_fraction_decomposition`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=292: `\text{Decompose } \frac{2x - 1}{x^{2} - 3x + 2}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=358: `\text{Decompose } \frac{-2x + 8}{x^{2} - 4x + 3}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=484: `\text{Decompose } \frac{x - 4}{x^{2} - 5x + 6}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_

#### `nonrepeated_linear_3` — implemented

- **Description:** P/Q with three distinct linear factors
- **Strategy:** `pfd_distinct_linear`
- **D gate:** d_min=8, d_max=None, d_weight=1.8
- **OpenStax case:** §9.4 nonrepeated linear (3 factors)
- **Book / section:** precalculus-2e / 9.4 Partial Fractions
- **type_id / leaves:** `pc_partial_fraction_decomposition`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=292: `\text{Decompose } \frac{2x - 1}{x^{2} - 3x + 2}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=358: `\text{Decompose } \frac{-2x + 8}{x^{2} - 4x + 3}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=484: `\text{Decompose } \frac{x - 4}{x^{2} - 5x + 6}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_

#### `nonrepeated_irreducible_quadratic` — implemented

- **Description:** Q has a nonrepeated irreducible quadratic (plus optional linear)
- **Strategy:** `pfd_irreducible_quad`
- **D gate:** d_min=8, d_max=None, d_weight=2.0
- **OpenStax case:** §9.4 Example 3 — nonrepeated irreducible quadratic
- **Book / section:** precalculus-2e / 9.4 Partial Fractions
- **type_id / leaves:** `pc_partial_fraction_decomposition`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=292: `\text{Decompose } \frac{2x - 1}{x^{2} - 3x + 2}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=358: `\text{Decompose } \frac{-2x + 8}{x^{2} - 4x + 3}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=484: `\text{Decompose } \frac{x - 4}{x^{2} - 5x + 6}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_

#### `mixed_linear_quadratic` — implemented

- **Description:** Two+ linears with one irreducible quadratic
- **Strategy:** `pfd_mixed`
- **D gate:** d_min=12, d_max=None, d_weight=1.5
- **OpenStax case:** §9.4 mixed linear + irreducible quadratic
- **Book / section:** precalculus-2e / 9.4 Partial Fractions
- **type_id / leaves:** `pc_partial_fraction_decomposition`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=292: `\text{Decompose } \frac{2x - 1}{x^{2} - 3x + 2}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=358: `\text{Decompose } \frac{-2x + 8}{x^{2} - 4x + 3}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=484: `\text{Decompose } \frac{x - 4}{x^{2} - 5x + 6}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_

#### `repeated_linear` — stub

- **Description:** Q has a repeated linear factor (x−a)^k, k≥2
- **Strategy:** `pfd_repeated_linear`
- **D gate:** d_min=10, d_max=None, d_weight=1.2
- **OpenStax case:** §9.4 Example 2 — repeated linear factors
- **Book / section:** precalculus-2e / 9.4 Partial Fractions
- **type_id / leaves:** `pc_partial_fraction_decomposition`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=16.0 seed=1256: `\int \frac{-3x + 6}{\left(x - 3\right)^{2}}\,dx` _prefix match `repeated_linear_square`_
  - [gallery:calc1_algebraic_gallery] type=`calc_indef_int_partial_fractions` D=25.0 seed=1409: `\int \frac{-4x - 8}{\left(x + 1\right)^{2}}\,dx` _prefix match `repeated_linear_square`_
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=292: `\text{Decompose } \frac{2x - 1}{x^{2} - 3x + 2}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_

#### `repeated_irreducible_quadratic` — deferred

- **Description:** Q has a repeated irreducible quadratic factor
- **Strategy:** `pfd_repeated_quad`
- **D gate:** d_min=16, d_max=None, d_weight=0.8
- **OpenStax case:** §9.4 Example 4 — repeated irreducible quadratic
- **Book / section:** precalculus-2e / 9.4 Partial Fractions
- **type_id / leaves:** `pc_partial_fraction_decomposition`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=292: `\text{Decompose } \frac{2x - 1}{x^{2} - 3x + 2}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=358: `\text{Decompose } \frac{-2x + 8}{x^{2} - 4x + 3}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_
  - [gallery:pc_algebraic_gallery] type=`pc_partial_fraction_decomposition` D=0.0 seed=484: `\text{Decompose } \frac{x - 4}{x^{2} - 5x + 6}` _type_id sibling `pc_partial_fraction_decomposition` (not form_id-exact)_

### Catalog `precalculus_trig_identities`

- **Title:** OpenStax Precalculus 2e §7.1–7.4 Trig identities (algebraic) — form taxonomy
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/precalculus_trig_identities.json`
- **OpenStax:** precalculus-2e — 7.1 Simplifying and Verifying Trigonometric Identities
- **URL:** https://openstax.org/books/precalculus-2e/pages/7-1-simplifying-and-verifying-trigonometric-identities
- **Stage-1 mining:** `scripts/output/example_mining/precalculus-2e/stage1/7-1-simplifying-and-verifying-trigonometric-identities.json`
- **Forms:** 8 (implemented=5, stub=2, deferred=1)
- **Taxonomy notes:** §7.1 fundamental / reciprocal / Pythagorean simplify & verify.

#### `pythagorean_basic` — implemented

- **Description:** Simplify sin²+cos² / sec²−tan² / 1+cot² forms
- **Strategy:** `pythagorean`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §7.1 Pythagorean identities
- **Book / section:** precalculus-2e / 7.1 Simplifying and Verifying Trigonometric Identities
- **type_id / leaves:** `pc_fundamental_identities`
- **Cited exercises / examples:**
  - `Example_07_01_04` Example 4: `\frac{sec^{2} \theta - 1}{sec^{2} \theta} = sin^{2} \theta ; sec^{2} \theta = tan^{2} \theta + 1`
- **Generated twins (gallery / live):**
  - [live_generate] type=`pc_fundamental_identities` D=5.0 seed=41: `\text{Rewrite using a fundamental identity: } \csc \theta = \frac{1}{\sin \theta}` _live generate type_id `pc_fundamental_identities`_
  - [live_generate] type=`pc_fundamental_identities` D=10.0 seed=107: `\text{Rewrite using a fundamental identity: } \sin^2 \theta + \cos^2 \theta = 1` _live generate type_id `pc_fundamental_identities`_

#### `reciprocal_quotient` — implemented

- **Description:** Rewrite tan/cot/sec/csc via sin/cos
- **Strategy:** `reciprocal`
- **D gate:** d_min=0, d_max=None, d_weight=1.8
- **OpenStax case:** §7.1 reciprocal / quotient identities
- **Book / section:** precalculus-2e / 7.1 Simplifying and Verifying Trigonometric Identities
- **type_id / leaves:** `pc_fundamental_identities`
- **Cited exercises / examples:**
  - `Example_07_01_01` Example 1: `cot \theta = \frac{1}{tan \theta} . ; y = cot \theta ; y = \frac{1}{tan \theta} .`
  - `Example_07_01_02` Example 2: `tan \theta cos \theta = sin \theta . ; tan \theta ; sin \theta ; cos \theta .`
- **Generated twins (gallery / live):**
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_linear_approximations` D=12.0 seed=923: `\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=2.` _matched gallery shape_id~strategy `reciprocal`_
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_linear_approximations` D=16.0 seed=925: `\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=5.` _matched gallery shape_id~strategy `reciprocal`_
  - [gallery:calc1_algebraic_gallery] type=`calc_app_diff_linear_approximations` D=16.0 seed=1117: `\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=4.` _matched gallery shape_id~strategy `reciprocal`_

#### `verify_fundamental` — stub

- **Description:** Verify LHS = RHS using fundamental identities
- **Strategy:** `verify`
- **D gate:** d_min=8, d_max=None, d_weight=1.2
- **OpenStax case:** §7.1 verify identity (LHS=RHS)
- **Book / section:** precalculus-2e / 7.1 Simplifying and Verifying Trigonometric Identities
- **type_id / leaves:** `pc_fundamental_identities`
- **Cited exercises / examples:**
  - `Example_07_01_02` Example 2: `tan \theta cos \theta = sin \theta . ; tan \theta ; sin \theta ; cos \theta .`
  - `ti_07_01_01` Try It #1: `csc \theta cos \theta tan \theta = 1.`
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `sum_difference_expand` — implemented

- **Description:** Expand sin/cos/tan(α±β)
- **Strategy:** `sum_difference`
- **D gate:** d_min=4, d_max=None, d_weight=2.0
- **OpenStax case:** §7.2 sum and difference identities
- **Book / section:** precalculus-2e / 7.1 Simplifying and Verifying Trigonometric Identities
- **type_id / leaves:** `pc_sum_and_difference_identities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`pc_sum_and_difference_identities` D=5.0 seed=41: `\text{Expand }\cos(\alpha-\beta).` _live generate type_id `pc_sum_and_difference_identities`_
  - [live_generate] type=`pc_sum_and_difference_identities` D=10.0 seed=107: `\text{Expand }\sin(\alpha-\beta).` _live generate type_id `pc_sum_and_difference_identities`_

#### `double_angle` — implemented

- **Description:** Rewrite sin(2θ) / cos(2θ) / tan(2θ)
- **Strategy:** `double_angle`
- **D gate:** d_min=4, d_max=None, d_weight=2.0
- **OpenStax case:** §7.3 double-angle formulas
- **Book / section:** precalculus-2e / 7.1 Simplifying and Verifying Trigonometric Identities
- **type_id / leaves:** `pc_multiple_angle_identities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`pc_multiple_angle_identities` D=5.0 seed=41: `\text{Rewrite }\cos(2\theta)\text{ using a double-angle identity.}` _live generate type_id `pc_multiple_angle_identities`_

#### `product_to_sum` — implemented

- **Description:** Rewrite sin A cos B etc. as a sum
- **Strategy:** `product_to_sum`
- **D gate:** d_min=8, d_max=None, d_weight=1.8
- **OpenStax case:** §7.4 product-to-sum formulas
- **Book / section:** precalculus-2e / 7.1 Simplifying and Verifying Trigonometric Identities
- **type_id / leaves:** `pc_product_to_sum_identities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`pc_product_to_sum_identities` D=5.0 seed=41: `\text{Rewrite }\sin A\cos B\text{ as a sum.}` _live generate type_id `pc_product_to_sum_identities`_

#### `sum_to_product` — stub

- **Description:** Rewrite sin A ± sin B as a product
- **Strategy:** `sum_to_product`
- **D gate:** d_min=10, d_max=None, d_weight=1.2
- **OpenStax case:** §7.4 sum-to-product (curriculum gap)
- **Book / section:** precalculus-2e / 7.1 Simplifying and Verifying Trigonometric Identities
- **type_id / leaves:** `pc_product_to_sum_identities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `half_angle` — deferred

- **Description:** Half-angle / power-reduction formulas
- **Strategy:** `half_angle`
- **D gate:** d_min=12, d_max=None, d_weight=1.0
- **OpenStax case:** §7.3 half-angle and reduction
- **Book / section:** precalculus-2e / 7.1 Simplifying and Verifying Trigonometric Identities
- **type_id / leaves:** `pc_multiple_angle_identities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

### Catalog `precalculus_trig_equations`

- **Title:** OpenStax Precalculus 2e §7.5 Solving Trigonometric Equations — form taxonomy
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/precalculus_trig_equations.json`
- **OpenStax:** precalculus-2e — 7.5 Solving Trigonometric Equations
- **URL:** https://openstax.org/books/precalculus-2e/pages/7-5-solving-trigonometric-equations
- **Stage-1 mining:** `scripts/output/example_mining/precalculus-2e/stage1/7-5-solving-trigonometric-equations.json`
- **Forms:** 7 (implemented=4, stub=2, deferred=1)
- **Taxonomy notes:** §7.5 objectives: linear sin/cos; single trig function; quadratic-in-trig; fundamental-identity factoring; multiple angles.

#### `linear_sin_cos` — implemented

- **Description:** Solve sin θ = k or cos θ = k (unit-circle exact)
- **Strategy:** `linear_trig`
- **D gate:** d_min=0, d_max=None, d_weight=2.2
- **OpenStax case:** §7.5 Example 1–2 — linear sin/cos
- **Book / section:** precalculus-2e / 7.5 Solving Trigonometric Equations
- **type_id / leaves:** `pc_simple_trig_equations`, `pc_equations_and_multiple_angle_identities`
- **Cited exercises / examples:**
  - `Example_07_05_01` Example 1: `cos \theta = \frac{1}{2} .`
  - `Example_07_05_02` Example 2: `sin t = \frac{1}{2} .`
- **Generated twins (gallery / live):**
  - [live_generate] type=`pc_simple_trig_equations` D=5.0 seed=41: `\cos(x) = \frac{1}{2}` _live generate type_id `pc_simple_trig_equations`_
  - [live_generate] type=`pc_simple_trig_equations` D=10.0 seed=107: `\sin(x) = -\frac{\sqrt{2}}{2}` _live generate type_id `pc_simple_trig_equations`_
  - [live_generate] type=`pc_equations_and_multiple_angle_identities` D=5.0 seed=41: `\text{Solve }\cos(2\theta)=0\text{ for }0\le\theta<\pi.` _live generate type_id `pc_equations_and_multiple_angle_identities`_

#### `linear_scaled` — stub

- **Description:** Solve a cos θ + b = c (isolate then unit circle)
- **Strategy:** `linear_scaled`
- **D gate:** d_min=6, d_max=None, d_weight=1.6
- **OpenStax case:** §7.5 Example 3 — linear form with coefficients
- **Book / section:** precalculus-2e / 7.5 Solving Trigonometric Equations
- **type_id / leaves:** `pc_simple_trig_equations`, `pc_equations_and_multiple_angle_identities`
- **Cited exercises / examples:**
  - `Example_07_05_03` Example 3: `2 cos \theta - 3 = - 5 , 0 \leq \theta < 2 \pi .`
  - `ti_07_05_01` Try It #1: `\left[\right. 0 , 2 \pi \left.\right) : 2 sin x + 1 = 0.`
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `quadratic_in_trig` — implemented

- **Description:** Quadratic in sin/cos (e.g. 2sin²θ − 1 = 0)
- **Strategy:** `quadratic_trig`
- **D gate:** d_min=6, d_max=None, d_weight=2.0
- **OpenStax case:** §7.5 Example 4 — quadratic in trig
- **Book / section:** precalculus-2e / 7.5 Solving Trigonometric Equations
- **type_id / leaves:** `pc_equations_with_factoring_and_fundamental_identities`, `pc_equations_and_multiple_angle_identities`
- **Cited exercises / examples:**
  - `Example_07_05_04` Example 4: `2 sin^{2} \theta - 1 = 0 , 0 \leq \theta < 2 \pi .`
- **Generated twins (gallery / live):**
  - [live_generate] type=`pc_equations_with_factoring_and_fundamental_identities` D=5.0 seed=41: `\text{Solve }2\sin\theta\cos\theta=0\text{ for }0\le\theta<2\pi.` _live generate type_id `pc_equations_with_factoring_and_fundamental_identities`_
  - [live_generate] type=`pc_equations_and_multiple_angle_identities` D=5.0 seed=41: `\text{Solve }\cos(2\theta)=0\text{ for }0\le\theta<\pi.` _live generate type_id `pc_equations_and_multiple_angle_identities`_

#### `factor_fundamental` — implemented

- **Description:** Factor using fundamental identities (e.g. 2sinθ cosθ = 0)
- **Strategy:** `factor_identity`
- **D gate:** d_min=8, d_max=None, d_weight=2.0
- **OpenStax case:** §7.5 factoring with fundamental identities
- **Book / section:** precalculus-2e / 7.5 Solving Trigonometric Equations
- **type_id / leaves:** `pc_equations_with_factoring_and_fundamental_identities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`pc_equations_with_factoring_and_fundamental_identities` D=5.0 seed=41: `\text{Solve }2\sin\theta\cos\theta=0\text{ for }0\le\theta<2\pi.` _live generate type_id `pc_equations_with_factoring_and_fundamental_identities`_
  - [live_generate] type=`pc_equations_with_factoring_and_fundamental_identities` D=10.0 seed=107: `\text{Solve }\cos(2\theta)=0\text{ for }0\le\theta<\pi.` _live generate type_id `pc_equations_with_factoring_and_fundamental_identities`_

#### `double_angle_equation` — implemented

- **Description:** Solve cos(2θ)=0 / sin(2θ)=0 style
- **Strategy:** `multiple_angle`
- **D gate:** d_min=8, d_max=None, d_weight=1.8
- **OpenStax case:** §7.5 multiple-angle equations
- **Book / section:** precalculus-2e / 7.5 Solving Trigonometric Equations
- **type_id / leaves:** `pc_equations_and_multiple_angle_identities`, `pc_equations_with_factoring_and_fundamental_identities`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`pc_equations_and_multiple_angle_identities` D=5.0 seed=41: `\text{Solve }\cos(2\theta)=0\text{ for }0\le\theta<\pi.` _live generate type_id `pc_equations_and_multiple_angle_identities`_
  - [live_generate] type=`pc_equations_and_multiple_angle_identities` D=10.0 seed=107: `\text{Solve }2\sin\theta\cos\theta=0\text{ for }0\le\theta<2\pi.` _live generate type_id `pc_equations_and_multiple_angle_identities`_
  - [live_generate] type=`pc_equations_with_factoring_and_fundamental_identities` D=10.0 seed=107: `\text{Solve }2\sin^2\theta-\sin\theta=0\text{ for }0\le\theta<2\pi.` _live generate type_id `pc_equations_with_factoring_and_fundamental_identities`_

#### `single_trig_other` — stub

- **Description:** Solve csc θ = k / sec / tan on an interval
- **Strategy:** `reciprocal_trig_eq`
- **D gate:** d_min=10, d_max=None, d_weight=1.2
- **OpenStax case:** §7.5 Example 5 — cosecant equation
- **Book / section:** precalculus-2e / 7.5 Solving Trigonometric Equations
- **type_id / leaves:** `pc_equations_and_multiple_angle_identities`
- **Cited exercises / examples:**
  - `Example_07_05_05` Example 5: `csc \theta = - 2 , 0 \leq \theta < 4 \pi . ; sin \theta = - \frac{1}{2} ,`
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `calculator_approx` — deferred

- **Description:** Trig equations requiring calculator approximations
- **Strategy:** `calculator`
- **D gate:** d_min=12, d_max=None, d_weight=0.5
- **OpenStax case:** §7.5 calculator solutions
- **Book / section:** precalculus-2e / 7.5 Solving Trigonometric Equations
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

## Algebra 2

### Catalog `algebra2_polys`

- **Title:** OpenStax Intermediate Algebra 2e — polynomials (Ch 5–6)
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/algebra2_polys.json`
- **OpenStax:** intermediate-algebra-2e — Polynomials / Factoring Polynomials
- **URL:** https://openstax.org/books/intermediate-algebra-2e/pages/5-introduction
- **Stage-1 mining:** `scripts/output/example_mining/intermediate-algebra-2e/stage1/`
- **Forms:** 13 (implemented=10, stub=3, deferred=0)
- **Taxonomy notes:** Forms mirror OpenStax Intermediate Algebra §§5.1–5.4 and §§6.1–6.5 learning objectives.

#### `poly_add` — implemented

- **Description:** Add two polynomials (combine like terms)
- **Strategy:** `combine_like_terms`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §5.1 Add and subtract polynomials
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **type_id / leaves:** `a2_polynomial_functions_adding_and_subtracting`
- **Cited exercises / examples:**
  - `fs-id1167836415722` Example 5.1: `7 y^{2} - 5 y + 3 ; −2 a^{4} b^{2} ; 3 x^{5} - 4 x^{3} - 6 x^{2} + x - 8 ; 2 y - 8 x y^{3}`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`polynomial_add_subtract` D=0.0 seed=945: `\text{Simplify: } \left(3x^{2} - 1\right) + \left(3x^{2} - 1\right)` _alias `+`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_add_subtract` D=0.0 seed=1011: `\text{Simplify: } \left(x^{2} + 3\right) + \left(2x^{2} + 1\right)` _alias `+`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_add_subtract` D=0.0 seed=1137: `\text{Simplify: } \left(2x^{2} + 3\right) + \left(3x + 1\right)` _alias `+`_

#### `poly_subtract` — implemented

- **Description:** Subtract polynomials (distribute minus, combine)
- **Strategy:** `distribute_minus_combine`
- **D gate:** d_min=2, d_max=None, d_weight=2.0
- **OpenStax case:** §5.1 Subtract polynomials
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **type_id / leaves:** `a2_polynomial_functions_adding_and_subtracting`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`polynomial_add_subtract` D=3.0 seed=1062: `\text{Simplify: } \left(3x^{2} + 3\right) - \left(x^{2} + 1\right)` _alias `-`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_add_subtract` D=3.0 seed=1188: `\text{Simplify: } \left(-2x^{2} - 1\right) - \left(x^{2} + 3\right)` _alias `-`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_add_subtract` D=6.0 seed=1047: `\text{Simplify: } \left(3x^{2} + 3\right) - \left(x^{2} + 2\right)` _alias `-`_

#### `mono_times_poly` — implemented

- **Description:** Multiply a monomial by a polynomial
- **Strategy:** `distribute_monomial`
- **D gate:** d_min=0, d_max=None, d_weight=1.8
- **OpenStax case:** §5.3 Multiply a polynomial by a monomial
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **type_id / leaves:** `a2_polynomial_functions_multiplying`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=0.0 seed=760: `\text{Multiply: } \left(2x\right)\left(x + 3\right)` _alias `distribute`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=0.0 seed=826: `\text{Multiply: } \left(x\right)\left(2x - 1\right)` _alias `distribute`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=0.0 seed=952: `\text{Multiply: } \left(x\right)\left(x + 2\right)` _alias `distribute`_

#### `binomial_times_binomial` — implemented

- **Description:** Multiply two binomials (FOIL)
- **Strategy:** `foil`
- **D gate:** d_min=2, d_max=None, d_weight=2.2
- **OpenStax case:** §5.3 Multiply a binomial by a binomial
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **type_id / leaves:** `a2_polynomial_functions_multiplying`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=3.0 seed=877: `\text{Multiply: } \left(3x + 1\right)\left(x + 1\right)` _matched gallery shape_id~strategy `foil`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=6.0 seed=862: `\text{Multiply: } \left(3x^{2} + 4\right)\left(4x + 3\right)` _matched gallery shape_id~strategy `foil`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=6.0 seed=928: `\text{Multiply: } \left(2x^{2} + 1\right)\left(-x + 1\right)` _matched gallery shape_id~strategy `foil`_

#### `poly_times_poly` — implemented

- **Description:** Multiply a polynomial by a polynomial (deg≥2 × deg≥2)
- **Strategy:** `distribute_all`
- **D gate:** d_min=8, d_max=None, d_weight=1.6
- **OpenStax case:** §5.3 Multiply a polynomial by a polynomial
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **type_id / leaves:** `a2_polynomial_functions_multiplying`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=0.0 seed=760: `\text{Multiply: } \left(2x\right)\left(x + 3\right)` _alias `distribute`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=0.0 seed=826: `\text{Multiply: } \left(x\right)\left(2x - 1\right)` _alias `distribute`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=0.0 seed=952: `\text{Multiply: } \left(x\right)\left(x + 2\right)` _alias `distribute`_

#### `special_product_square` — implemented

- **Description:** (a±b)² special product
- **Strategy:** `perfect_square`
- **D gate:** d_min=4, d_max=None, d_weight=1.8
- **OpenStax case:** §5.3 Multiply special products — square
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **type_id / leaves:** `a2_polynomial_functions_multiplying_special_cases`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_polynomial_functions_multiplying_special_cases` D=5.0 seed=41: `\text{Multiply: } \left(x - 3\right)^{2}` _live generate type_id `a2_polynomial_functions_multiplying_special_cases`_
  - [live_generate] type=`a2_polynomial_functions_multiplying_special_cases` D=10.0 seed=107: `\text{Multiply: } \left(x + 2\right)\left(x - 1\right)` _live generate type_id `a2_polynomial_functions_multiplying_special_cases`_

#### `special_product_diff_squares` — implemented

- **Description:** (a−b)(a+b) difference of squares product
- **Strategy:** `diff_squares_product`
- **D gate:** d_min=4, d_max=None, d_weight=1.8
- **OpenStax case:** §5.3 Multiply special products — difference of squares
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **type_id / leaves:** `a2_polynomial_functions_multiplying_special_cases`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_polynomial_functions_multiplying_special_cases` D=5.0 seed=41: `\text{Multiply: } \left(x - 3\right)^{2}` _live generate type_id `a2_polynomial_functions_multiplying_special_cases`_
  - [live_generate] type=`a2_polynomial_functions_multiplying_special_cases` D=10.0 seed=107: `\text{Multiply: } \left(x + 2\right)\left(x - 1\right)` _live generate type_id `a2_polynomial_functions_multiplying_special_cases`_

#### `factor_by_grouping` — implemented

- **Description:** Factor four-term polynomial by grouping
- **Strategy:** `grouping`
- **D gate:** d_min=4, d_max=None, d_weight=2.0
- **OpenStax case:** §6.1 Factor by grouping
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **type_id / leaves:** `a2_polynomial_functions_factoring_by_grouping`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_by_grouping` D=6.0 seed=931: `3x^{3} + 12x^{2} - 2x - 8` _alias `grouping_cubic`_
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_by_grouping` D=6.0 seed=1123: `2x^{3} + 4x^{2} - 4x - 8` _alias `grouping_cubic`_
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_by_grouping` D=8.0 seed=965: `4x^{3} - 8x^{2} + 5x - 10` _alias `grouping_cubic`_

#### `sum_diff_cubes` — implemented

- **Description:** Factor sum or difference of cubes
- **Strategy:** `cubes`
- **D gate:** d_min=6, d_max=None, d_weight=1.6
- **OpenStax case:** §6.3 Factor sums and differences of cubes
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **type_id / leaves:** `a2_polynomial_functions_factoring_sum_difference_of_cubes`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_sum_difference_of_cubes` D=0.0 seed=218: `x^{3} - 8` _alias `difference_of_cubes`_
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_sum_difference_of_cubes` D=0.0 seed=284: `x^{3} - 1` _alias `difference_of_cubes`_
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_sum_difference_of_cubes` D=6.0 seed=320: `y^{3} - 125` _alias `difference_of_cubes`_

#### `poly_degree_classify` — implemented

- **Description:** Name monomial/binomial/trinomial and degree
- **Strategy:** `classify_degree`
- **D gate:** d_min=0, d_max=None, d_weight=1.0
- **OpenStax case:** §5.1 Degree of a polynomial
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **type_id / leaves:** `a2_polynomial_functions_naming`
- **Cited exercises / examples:**
  - `fs-id1167836415722` Example 5.1: `7 y^{2} - 5 y + 3 ; −2 a^{4} b^{2} ; 3 x^{5} - 4 x^{3} - 6 x^{2} + x - 8 ; 2 y - 8 x y^{3}`
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_polynomial_functions_naming` D=5.0 seed=41: `\text{Name the polynomial: } 2x^{2} + x` _live generate type_id `a2_polynomial_functions_naming`_
  - [live_generate] type=`a2_polynomial_functions_naming` D=10.0 seed=107: `\text{Name the polynomial: } 3x^{3} - 2x^{2} - 1` _live generate type_id `a2_polynomial_functions_naming`_

#### `long_division` — stub

- **Description:** Divide polynomials using long division
- **Strategy:** `long_division`
- **D gate:** d_min=6, d_max=None, d_weight=1.4
- **OpenStax case:** §5.4 Dividing polynomials using long division
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **type_id / leaves:** `a2_polynomial_functions_dividing`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `gcf_factor` — stub

- **Description:** Factor out greatest common factor
- **Strategy:** `gcf`
- **D gate:** d_min=0, d_max=None, d_weight=1.5
- **OpenStax case:** §6.1 Factor the GCF from a polynomial — A2 leaf unwired (A1 has dedicated type)
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `trinomial_a_gt_1` — stub

- **Description:** Factor ax²+bx+c with a≠1 (trial/ac)
- **Strategy:** `ac_method`
- **D gate:** d_min=6, d_max=None, d_weight=1.8
- **OpenStax case:** §6.2 Factor trinomials a≠1 — catalog form pending dedicated leaf wiring
- **Book / section:** intermediate-algebra-2e / Polynomials / Factoring Polynomials
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

### Catalog `algebra2_rationals`

- **Title:** OpenStax Intermediate Algebra 2e — rational expressions (Ch 7)
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/algebra2_rationals.json`
- **OpenStax:** intermediate-algebra-2e — Rational Expressions and Equations
- **URL:** https://openstax.org/books/intermediate-algebra-2e/pages/7-introduction
- **Stage-1 mining:** `scripts/output/example_mining/intermediate-algebra-2e/stage1/`
- **Forms:** 11 (implemented=6, stub=3, deferred=2)
- **Taxonomy notes:** Forms mirror §§7.1–7.4 learning objectives (simplify, ×÷, ±, complex fractions, equations).

#### `simplify_cancel` — implemented

- **Description:** Simplify a single rational by canceling common factors
- **Strategy:** `cancel_common_factors`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §7.1 Simplify rational expressions
- **Book / section:** intermediate-algebra-2e / Rational Expressions and Equations
- **type_id / leaves:** `a2_rational_expressions_simplifying`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_simplifying` D=0.0 seed=957: `\text{Simplify: } \frac{3x^{2} - 12x + 9}{x^{2} - 3x + 2}` _type_id sibling `a2_rational_expressions_simplifying` (not form_id-exact)_
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_simplifying` D=0.0 seed=1023: `\text{Simplify: } \frac{3x^{2} - 6x}{x^{2} - 3x}` _type_id sibling `a2_rational_expressions_simplifying` (not form_id-exact)_
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_simplifying` D=0.0 seed=1149: `\text{Simplify: } \frac{-x^{2} - 2x + 3}{x^{2} - 9}` _type_id sibling `a2_rational_expressions_simplifying` (not form_id-exact)_

#### `add_common_den` — implemented

- **Description:** Add/subtract rationals with a common denominator
- **Strategy:** `common_denominator`
- **D gate:** d_min=0, d_max=10, d_weight=2.0
- **OpenStax case:** §7.2 Add/subtract with a common denominator
- **Book / section:** intermediate-algebra-2e / Rational Expressions and Equations
- **type_id / leaves:** `a2_rational_expressions_adding_and_subtracting`
- **Cited exercises / examples:**
  - `fs-id1167836544834` Example 7.13: `\frac{11 x + 28}{x + 4} + \frac{x^{2}}{x + 4} .`
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_adding_and_subtracting` D=0.0 seed=305: `\text{Combine and simplify: } \frac{2}{x - 2} + \frac{1}{x - 2}` _type_id sibling `a2_rational_expressions_adding_and_subtracting` (not form_id-exact)_
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_adding_and_subtracting` D=0.0 seed=371: `\text{Combine and simplify: } \frac{2}{x - 1} - \frac{1}{x - 1}` _type_id sibling `a2_rational_expressions_adding_and_subtracting` (not form_id-exact)_
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_adding_and_subtracting` D=0.0 seed=497: `\text{Combine and simplify: } \frac{2}{x + 1} + \frac{3}{x + 1}` _type_id sibling `a2_rational_expressions_adding_and_subtracting` (not form_id-exact)_

#### `add_unlike_dens` — implemented

- **Description:** Add/subtract rationals with unlike denominators (LCD)
- **Strategy:** `lcd_combine`
- **D gate:** d_min=4, d_max=None, d_weight=2.4
- **OpenStax case:** §7.2 Add/subtract with unlike denominators
- **Book / section:** intermediate-algebra-2e / Rational Expressions and Equations
- **type_id / leaves:** `a2_rational_expressions_adding_and_subtracting`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_adding_and_subtracting` D=0.0 seed=305: `\text{Combine and simplify: } \frac{2}{x - 2} + \frac{1}{x - 2}` _type_id sibling `a2_rational_expressions_adding_and_subtracting` (not form_id-exact)_
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_adding_and_subtracting` D=0.0 seed=371: `\text{Combine and simplify: } \frac{2}{x - 1} - \frac{1}{x - 1}` _type_id sibling `a2_rational_expressions_adding_and_subtracting` (not form_id-exact)_
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_adding_and_subtracting` D=0.0 seed=497: `\text{Combine and simplify: } \frac{2}{x + 1} + \frac{3}{x + 1}` _type_id sibling `a2_rational_expressions_adding_and_subtracting` (not form_id-exact)_

#### `add_unlike_with_cancel` — implemented

- **Description:** Unlike dens plus planned cancel after combine
- **Strategy:** `lcd_combine_cancel`
- **D gate:** d_min=10, d_max=None, d_weight=1.8
- **OpenStax case:** §7.2 harder LCD + cancel
- **Book / section:** intermediate-algebra-2e / Rational Expressions and Equations
- **type_id / leaves:** `a2_rational_expressions_adding_and_subtracting`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_adding_and_subtracting` D=0.0 seed=305: `\text{Combine and simplify: } \frac{2}{x - 2} + \frac{1}{x - 2}` _type_id sibling `a2_rational_expressions_adding_and_subtracting` (not form_id-exact)_
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_adding_and_subtracting` D=0.0 seed=371: `\text{Combine and simplify: } \frac{2}{x - 1} - \frac{1}{x - 1}` _type_id sibling `a2_rational_expressions_adding_and_subtracting` (not form_id-exact)_
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_adding_and_subtracting` D=0.0 seed=497: `\text{Combine and simplify: } \frac{2}{x + 1} + \frac{3}{x + 1}` _type_id sibling `a2_rational_expressions_adding_and_subtracting` (not form_id-exact)_

#### `multiply_rationals` — implemented

- **Description:** Multiply rational expressions and simplify
- **Strategy:** `multiply_cancel`
- **D gate:** d_min=2, d_max=None, d_weight=1.8
- **OpenStax case:** §7.1 Multiply rational expressions
- **Book / section:** intermediate-algebra-2e / Rational Expressions and Equations
- **type_id / leaves:** `a2_rational_expressions_multiplying_and_dividing`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_rational_expressions_multiplying_and_dividing` D=5.0 seed=41: `\frac{\left(5x+4\right)\left(2x-3\right)}{\left(5x-8\right)\left(4x+1\right)} \cdot \frac{\left(2x-7\right)\left(4x+1\right)}{\left(x-7\right)\left(2x-3\right)}` _live generate type_id `a2_rational_expressions_multiplying_and_dividing`_
  - [live_generate] type=`a2_rational_expressions_multiplying_and_dividing` D=10.0 seed=107: `\frac{\left(3x+1\right)\left(4x+1\right)}{\left(5x-7\right)\left(2x+5\right)} \cdot \frac{\left(3x+2\right)\left(2x+5\right)}{\left(2x-3\right)\left(4x+1\right)}` _live generate type_id `a2_rational_expressions_multiplying_and_dividing`_

#### `divide_rationals` — implemented

- **Description:** Divide rational expressions (multiply by reciprocal)
- **Strategy:** `divide_reciprocal`
- **D gate:** d_min=4, d_max=None, d_weight=1.8
- **OpenStax case:** §7.1 Divide rational expressions
- **Book / section:** intermediate-algebra-2e / Rational Expressions and Equations
- **type_id / leaves:** `a2_rational_expressions_multiplying_and_dividing`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_rational_expressions_multiplying_and_dividing` D=5.0 seed=41: `\frac{\left(5x+4\right)\left(2x-3\right)}{\left(5x-8\right)\left(4x+1\right)} \cdot \frac{\left(2x-7\right)\left(4x+1\right)}{\left(x-7\right)\left(2x-3\right)}` _live generate type_id `a2_rational_expressions_multiplying_and_dividing`_
  - [live_generate] type=`a2_rational_expressions_multiplying_and_dividing` D=10.0 seed=107: `\frac{\left(3x+1\right)\left(4x+1\right)}{\left(5x-7\right)\left(2x+5\right)} \cdot \frac{\left(3x+2\right)\left(2x+5\right)}{\left(2x-3\right)\left(4x+1\right)}` _live generate type_id `a2_rational_expressions_multiplying_and_dividing`_

#### `complex_fraction_lcd` — stub

- **Description:** Simplify complex rational by LCD method
- **Strategy:** `complex_lcd`
- **D gate:** d_min=8, d_max=None, d_weight=1.4
- **OpenStax case:** §7.3 Simplify complex rational by LCD
- **Book / section:** intermediate-algebra-2e / Rational Expressions and Equations
- **type_id / leaves:** `a2_rational_expressions_complex_fractions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `rational_equation` — stub

- **Description:** Solve rational equation (clear dens; check extraneous)
- **Strategy:** `clear_denominators`
- **D gate:** d_min=6, d_max=None, d_weight=1.6
- **OpenStax case:** §7.4 Solve rational equations
- **Book / section:** intermediate-algebra-2e / Rational Expressions and Equations
- **type_id / leaves:** `a2_rational_expressions_equations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `add_opposite_dens` — stub

- **Description:** Add/subtract when denominators are opposites
- **Strategy:** `opposite_denominators`
- **D gate:** d_min=6, d_max=None, d_weight=1.2
- **OpenStax case:** §7.2 Denominators are opposites
- **Book / section:** intermediate-algebra-2e / Rational Expressions and Equations
- **type_id / leaves:** `a2_rational_expressions_adding_and_subtracting`
- **Cited exercises / examples:**
  - `fs-id1167836728843` Example 7.15: `\frac{m^{2} - 6 m}{m^{2} - 1} - \frac{3 m + 2}{1 - m^{2}} .`
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_adding_and_subtracting` D=0.0 seed=305: `\text{Combine and simplify: } \frac{2}{x - 2} + \frac{1}{x - 2}` _type_id sibling `a2_rational_expressions_adding_and_subtracting` (not form_id-exact)_
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_adding_and_subtracting` D=0.0 seed=371: `\text{Combine and simplify: } \frac{2}{x - 1} - \frac{1}{x - 1}` _type_id sibling `a2_rational_expressions_adding_and_subtracting` (not form_id-exact)_
  - [gallery:a2_algebraic_gallery] type=`a2_rational_expressions_adding_and_subtracting` D=0.0 seed=497: `\text{Combine and simplify: } \frac{2}{x + 1} + \frac{3}{x + 1}` _type_id sibling `a2_rational_expressions_adding_and_subtracting` (not form_id-exact)_

#### `pfd_linear_factors` — deferred

- **Description:** Partial fractions with distinct linear factors (not IntAlg core)
- **Strategy:** `construct_pfd`
- **D gate:** d_min=8, d_max=None, d_weight=1.0
- **OpenStax case:** Not in Intermediate Algebra — wrap construct_pfd / PC leaf pc_partial_fraction_decomposition
- **Book / section:** intermediate-algebra-2e / Rational Expressions and Equations
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `rational_apps` — deferred

- **Description:** Applications with rational equations (work/motion)
- **Strategy:** `rational_word_problem`
- **D gate:** d_min=10, d_max=None, d_weight=1.0
- **OpenStax case:** §7.5 — curriculum gap (missing on A2)
- **Book / section:** intermediate-algebra-2e / Rational Expressions and Equations
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

### Catalog `algebra2_radicals`

- **Title:** OpenStax Intermediate Algebra 2e — radicals & rational exponents (Ch 8)
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/algebra2_radicals.json`
- **OpenStax:** intermediate-algebra-2e — Roots and Rational Exponents
- **URL:** https://openstax.org/books/intermediate-algebra-2e/pages/8-introduction
- **Stage-1 mining:** `scripts/output/example_mining/intermediate-algebra-2e/stage1/`
- **Forms:** 10 (implemented=7, stub=3, deferred=0)
- **Taxonomy notes:** Forms mirror §§8.1–8.6 learning objectives.

#### `simplify_perfect_square_factor` — implemented

- **Description:** Simplify √n by extracting perfect-square factors
- **Strategy:** `product_property`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §8.2 Use the Product Property to simplify
- **Book / section:** intermediate-algebra-2e / Roots and Rational Exponents
- **type_id / leaves:** `a2_radical_functions_and_rational_exponents_simplifying_radicals`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_simplifying_radicals` D=5.0 seed=41: `\sqrt{192}` _live generate type_id `a2_radical_functions_and_rational_exponents_simplifying_radicals`_
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_simplifying_radicals` D=10.0 seed=107: `\sqrt{200}` _live generate type_id `a2_radical_functions_and_rational_exponents_simplifying_radicals`_

#### `add_like_radicals` — implemented

- **Description:** Add/subtract like radical expressions
- **Strategy:** `combine_like`
- **D gate:** d_min=0, d_max=10, d_weight=2.0
- **OpenStax case:** §8.4 Add and subtract radical expressions
- **Book / section:** intermediate-algebra-2e / Roots and Rational Exponents
- **type_id / leaves:** `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions` D=5.0 seed=41: `\sqrt{11} - 2\sqrt{11}` _live generate type_id `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions`_
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions` D=10.0 seed=107: `4\sqrt{6} + 3\sqrt{6} + 4\sqrt{6}` _live generate type_id `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions`_

#### `add_unsimplified_radicals` — implemented

- **Description:** Add radicals that must be simplified first
- **Strategy:** `simplify_then_combine`
- **D gate:** d_min=6, d_max=None, d_weight=2.0
- **OpenStax case:** §8.4 Add after simplifying
- **Book / section:** intermediate-algebra-2e / Roots and Rational Exponents
- **type_id / leaves:** `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions` D=5.0 seed=41: `\sqrt{11} - 2\sqrt{11}` _live generate type_id `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions`_
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions` D=10.0 seed=107: `4\sqrt{6} + 3\sqrt{6} + 4\sqrt{6}` _live generate type_id `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions`_

#### `multiply_radicals` — implemented

- **Description:** Multiply radical expressions
- **Strategy:** `product_property_multiply`
- **D gate:** d_min=2, d_max=None, d_weight=1.6
- **OpenStax case:** §8.4 Multiply radical expressions
- **Book / section:** intermediate-algebra-2e / Roots and Rational Exponents
- **type_id / leaves:** `a2_radical_functions_and_rational_exponents_multiplying_radical_expressions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_multiplying_radical_expressions` D=5.0 seed=41: `\sqrt{8} \cdot \sqrt{13}` _live generate type_id `a2_radical_functions_and_rational_exponents_multiplying_radical_expressions`_
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_multiplying_radical_expressions` D=10.0 seed=107: `3\sqrt{20} \cdot 2\sqrt{32}` _live generate type_id `a2_radical_functions_and_rational_exponents_multiplying_radical_expressions`_

#### `radical_eq_isolate` — implemented

- **Description:** Solve √(linear) = constant / light prep before square
- **Strategy:** `isolate_square`
- **D gate:** d_min=0, d_max=12, d_weight=2.0
- **OpenStax case:** §8.6 Solve radical equations
- **Book / section:** intermediate-algebra-2e / Roots and Rational Exponents
- **type_id / leaves:** `a2_radical_functions_and_rational_exponents_radical_equations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_radical_equations` D=5.0 seed=41: `5 + \sqrt{4x - 16} = 7` _live generate type_id `a2_radical_functions_and_rational_exponents_radical_equations`_
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_radical_equations` D=10.0 seed=107: `\sqrt{x + 4} = x - 2` _live generate type_id `a2_radical_functions_and_rational_exponents_radical_equations`_

#### `radical_eq_equals_linear` — implemented

- **Description:** √(expr) = linear — check extraneous
- **Strategy:** `square_check_extraneous`
- **D gate:** d_min=6, d_max=None, d_weight=2.2
- **OpenStax case:** §8.6 Isolate and square; extraneous roots
- **Book / section:** intermediate-algebra-2e / Roots and Rational Exponents
- **type_id / leaves:** `a2_radical_functions_and_rational_exponents_radical_equations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_radical_equations` D=5.0 seed=41: `5 + \sqrt{4x - 16} = 7` _live generate type_id `a2_radical_functions_and_rational_exponents_radical_equations`_
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_radical_equations` D=10.0 seed=107: `\sqrt{x + 4} = x - 2` _live generate type_id `a2_radical_functions_and_rational_exponents_radical_equations`_

#### `radical_eq_two_radicals` — implemented

- **Description:** Equation with two radicals (square twice)
- **Strategy:** `two_radicals`
- **D gate:** d_min=12, d_max=None, d_weight=1.8
- **OpenStax case:** §8.6 Solve radical equations with two radicals
- **Book / section:** intermediate-algebra-2e / Roots and Rational Exponents
- **type_id / leaves:** `a2_radical_functions_and_rational_exponents_radical_equations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_radical_equations` D=5.0 seed=41: `5 + \sqrt{4x - 16} = 7` _live generate type_id `a2_radical_functions_and_rational_exponents_radical_equations`_
  - [live_generate] type=`a2_radical_functions_and_rational_exponents_radical_equations` D=10.0 seed=107: `\sqrt{x + 4} = x - 2` _live generate type_id `a2_radical_functions_and_rational_exponents_radical_equations`_

#### `rationalize_one_term` — stub

- **Description:** Rationalize a one-term denominator
- **Strategy:** `rationalize_monomial`
- **D gate:** d_min=4, d_max=None, d_weight=1.4
- **OpenStax case:** §8.5 Rationalize a one-term denominator
- **Book / section:** intermediate-algebra-2e / Roots and Rational Exponents
- **type_id / leaves:** `a2_radical_functions_and_rational_exponents_dividing_radical_expressions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `rationalize_two_term` — stub

- **Description:** Rationalize a two-term denominator (conjugate)
- **Strategy:** `rationalize_conjugate`
- **D gate:** d_min=8, d_max=None, d_weight=1.2
- **OpenStax case:** §8.5 Rationalize a two-term denominator
- **Book / section:** intermediate-algebra-2e / Roots and Rational Exponents
- **type_id / leaves:** `a2_radical_functions_and_rational_exponents_dividing_radical_expressions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `rational_exponents_simplify` — stub

- **Description:** Simplify a^{m/n} / convert radical ↔ rational exponent
- **Strategy:** `rational_exponent_props`
- **D gate:** d_min=4, d_max=None, d_weight=1.4
- **OpenStax case:** §8.3 Simplify rational exponents
- **Book / section:** intermediate-algebra-2e / Roots and Rational Exponents
- **type_id / leaves:** `a2_radical_functions_and_rational_exponents_connecting_radical_expressions_and_rational_exponents`, `a2_radical_functions_and_rational_exponents_evaluating_rational_exponent_expressions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

### Catalog `algebra2_exp_log`

- **Title:** OpenStax Intermediate Algebra 2e — exponential & logarithmic equations (Ch 10)
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/algebra2_exp_log.json`
- **OpenStax:** intermediate-algebra-2e — Exponential and Logarithmic Functions
- **URL:** https://openstax.org/books/intermediate-algebra-2e/pages/10-introduction
- **Stage-1 mining:** `scripts/output/example_mining/intermediate-algebra-2e/stage1/`
- **Forms:** 7 (implemented=4, stub=2, deferred=1)
- **Taxonomy notes:** Forms mirror §§10.2–10.5 (evaluate/graph warmups deferred; equation + property forms prioritized).

#### `exp_same_base` — implemented

- **Description:** b^x = b^k → x = k (same base, no log)
- **Strategy:** `same_base`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §10.2 / §10.5 Solve exponential equations (same base)
- **Book / section:** intermediate-algebra-2e / Exponential and Logarithmic Functions
- **type_id / leaves:** `a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms` D=0.0 seed=700: `2^{x} = 2`
  - [gallery:a2_algebraic_gallery] type=`a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms` D=0.0 seed=766: `3^{x} = 3`
  - [gallery:a2_algebraic_gallery] type=`a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms` D=0.0 seed=892: `2^{x} = 4`

#### `exp_requiring_log` — implemented

- **Description:** b^{cx} = k — take log / rewrite
- **Strategy:** `take_logarithm`
- **D gate:** d_min=4, d_max=None, d_weight=2.0
- **OpenStax case:** §10.5 Solve exponential equations using logarithms
- **Book / section:** intermediate-algebra-2e / Exponential and Logarithmic Functions
- **type_id / leaves:** `a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms` D=5.0 seed=41: `5^{-2x} = 0.0016` _live generate type_id `a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms`_
  - [live_generate] type=`a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms` D=10.0 seed=107: `5^{5x} = 95367431640625` _live generate type_id `a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms`_

#### `log_equation_basic` — implemented

- **Description:** log_b(x) = k → x = b^k
- **Strategy:** `log_definition`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** §10.3 Solve logarithmic equations
- **Book / section:** intermediate-algebra-2e / Exponential and Logarithmic Functions
- **type_id / leaves:** `a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple`, `a2_exponential_and_logarithmic_expressions_logarithmic_equations_hard`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple` D=5.0 seed=41: `\log_{8}(x) = 3` _live generate type_id `a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple`_
  - [live_generate] type=`a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple` D=10.0 seed=107: `\log_{5}(x) = 5` _live generate type_id `a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple`_

#### `log_properties_condense` — implemented

- **Description:** Use product/quotient/power properties (condense or expand)
- **Strategy:** `log_properties`
- **D gate:** d_min=4, d_max=None, d_weight=1.8
- **OpenStax case:** §10.4 Use the properties of logarithms
- **Book / section:** intermediate-algebra-2e / Exponential and Logarithmic Functions
- **type_id / leaves:** `a2_exponential_and_logarithmic_expressions_properties_of_logarithms`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_exponential_and_logarithmic_expressions_properties_of_logarithms` D=0.0 seed=412: `\text{Expand: } \log_{2}\left(\frac{6}{2}\right)`
  - [gallery:a2_algebraic_gallery] type=`a2_exponential_and_logarithmic_expressions_properties_of_logarithms` D=0.0 seed=478: `\text{Expand: } \log_{3}\left(\frac{12}{2}\right)`
  - [gallery:a2_algebraic_gallery] type=`a2_exponential_and_logarithmic_expressions_properties_of_logarithms` D=0.0 seed=604: `\text{Expand: } \log_{3}\left(56\right)`

#### `change_of_base` — stub

- **Description:** Change-of-base formula evaluation
- **Strategy:** `change_of_base`
- **D gate:** d_min=6, d_max=None, d_weight=1.4
- **OpenStax case:** §10.4 Use the Change of Base Formula
- **Book / section:** intermediate-algebra-2e / Exponential and Logarithmic Functions
- **type_id / leaves:** `a2_exponential_and_logarithmic_expressions_properties_of_logarithms`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_exponential_and_logarithmic_expressions_properties_of_logarithms` D=0.0 seed=412: `\text{Expand: } \log_{2}\left(\frac{6}{2}\right)` _type_id sibling `a2_exponential_and_logarithmic_expressions_properties_of_logarithms` (not form_id-exact)_
  - [gallery:a2_algebraic_gallery] type=`a2_exponential_and_logarithmic_expressions_properties_of_logarithms` D=0.0 seed=478: `\text{Expand: } \log_{3}\left(\frac{12}{2}\right)` _type_id sibling `a2_exponential_and_logarithmic_expressions_properties_of_logarithms` (not form_id-exact)_
  - [gallery:a2_algebraic_gallery] type=`a2_exponential_and_logarithmic_expressions_properties_of_logarithms` D=0.0 seed=604: `\text{Expand: } \log_{3}\left(56\right)` _type_id sibling `a2_exponential_and_logarithmic_expressions_properties_of_logarithms` (not form_id-exact)_

#### `log_equation_properties` — stub

- **Description:** log equations needing product/quotient properties first
- **Strategy:** `properties_then_solve`
- **D gate:** d_min=8, d_max=None, d_weight=1.6
- **OpenStax case:** §10.5 Solve logarithmic equations using properties
- **Book / section:** intermediate-algebra-2e / Exponential and Logarithmic Functions
- **type_id / leaves:** `a2_exponential_and_logarithmic_expressions_logarithmic_equations_hard`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `exp_growth_decay` — deferred

- **Description:** Exponential growth/decay application models
- **Strategy:** `growth_decay_model`
- **D gate:** d_min=8, d_max=None, d_weight=1.0
- **OpenStax case:** §10.5 Use exponential models — leaf exists; catalog stamp not yet wired
- **Book / section:** intermediate-algebra-2e / Exponential and Logarithmic Functions
- **type_id / leaves:** `a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems`, `a2_exponential_and_logarithmic_expressions_continuous_exponential_growth_and_decay_word_problems`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

### Catalog `algebra2_function_ops`

- **Title:** OpenStax Intermediate Algebra 2e — composite & inverse functions (Ch 10.1)
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/algebra2_function_ops.json`
- **OpenStax:** intermediate-algebra-2e — 10.1 Finding Composite and Inverse Functions
- **URL:** https://openstax.org/books/intermediate-algebra-2e/pages/10-1-finding-composite-and-inverse-functions
- **Stage-1 mining:** `scripts/output/example_mining/intermediate-algebra-2e/stage1/10-1-finding-composite-and-inverse-functions.json`
- **Forms:** 7 (implemented=5, stub=1, deferred=1)
- **Taxonomy notes:** Forms enumerate (f±g), (f·g), (f∘g), evaluate, and inverse as Intermediate Algebra §10.1 + A2 general-functions ops.

#### `fn_add` — implemented

- **Description:** (f+g)(x) evaluation
- **Strategy:** `add_functions`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** Function operations — sum (A2 General Functions / §10.1 prep)
- **Book / section:** intermediate-algebra-2e / 10.1 Finding Composite and Inverse Functions
- **type_id / leaves:** `a2_general_functions_operations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_general_functions_operations` D=0.0 seed=302: `\text{If } f(x) = 3x - 1 \text{ and } g(x) = -3x - 1, \text{ find } (f + g)(3).`
  - [gallery:a2_algebraic_gallery] type=`a2_general_functions_operations` D=3.0 seed=227: `\text{If } f(x) = -3x - 1 \text{ and } g(x) = 3x - 3, \text{ find } (f + g)(1).`
  - [gallery:a2_algebraic_gallery] type=`a2_general_functions_operations` D=6.0 seed=404: `\text{If } f(x) = 6x + 8 \text{ and } g(x) = 6x - 5, \text{ find } (f + g)(-6).`

#### `fn_subtract` — implemented

- **Description:** (f−g)(x) evaluation
- **Strategy:** `subtract_functions`
- **D gate:** d_min=0, d_max=None, d_weight=2.0
- **OpenStax case:** Function operations — difference
- **Book / section:** intermediate-algebra-2e / 10.1 Finding Composite and Inverse Functions
- **type_id / leaves:** `a2_general_functions_operations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_general_functions_operations` D=0.0 seed=176: `\text{If } f(x) = 3x - 1 \text{ and } g(x) = 3x + 2, \text{ find } (f - g)(-5).`
  - [gallery:a2_algebraic_gallery] type=`a2_general_functions_operations` D=3.0 seed=161: `\text{If } f(x) = 3x - 1 \text{ and } g(x) = -3x + 3, \text{ find } (f - g)(3).`
  - [gallery:a2_algebraic_gallery] type=`a2_general_functions_operations` D=3.0 seed=353: `\text{If } f(x) = -3x - 3 \text{ and } g(x) = 3x - 3, \text{ find } (f - g)(-4).`

#### `fn_product` — implemented

- **Description:** (f·g)(x) evaluation
- **Strategy:** `multiply_functions`
- **D gate:** d_min=6, d_max=None, d_weight=2.0
- **OpenStax case:** Function operations — product
- **Book / section:** intermediate-algebra-2e / 10.1 Finding Composite and Inverse Functions
- **type_id / leaves:** `a2_general_functions_operations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_general_functions_operations` D=0.0 seed=110: `\text{If } f(x) = 3x + 0 \text{ and } g(x) = 3x + 4, \text{ find } (f \cdot g)(1).`
  - [gallery:a2_algebraic_gallery] type=`a2_general_functions_operations` D=6.0 seed=212: `\text{If } f(x) = 6x - 7 \text{ and } g(x) = 6x - 4, \text{ find } (f \cdot g)(4).`
  - [gallery:a2_algebraic_gallery] type=`a2_general_functions_operations` D=6.0 seed=278: `\text{If } f(x) = -6x + 7 \text{ and } g(x) = -6x + 6, \text{ find } (f \cdot g)(1).`

#### `fn_compose` — implemented

- **Description:** (f∘g)(x) evaluation
- **Strategy:** `compose`
- **D gate:** d_min=10, d_max=None, d_weight=2.2
- **OpenStax case:** §10.1 Find and evaluate composite functions
- **Book / section:** intermediate-algebra-2e / 10.1 Finding Composite and Inverse Functions
- **type_id / leaves:** `a2_general_functions_operations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_general_functions_operations` D=16.0 seed=448: `\text{If } f(x) = -8x + 1 \text{ and } g(x) = -8x + 3, \text{ find } (f \circ g)(0).`
  - [gallery:a2_algebraic_gallery] type=`a2_general_functions_operations` D=20.0 seed=642: `\text{If } f(x) = 9x + 9 \text{ and } g(x) = 9x - 7, \text{ find } (f \circ g)(-1).`
  - [gallery:a2_algebraic_gallery] type=`a2_general_functions_operations` D=25.0 seed=535: `\text{If } f(x) = -11x + 7 \text{ and } g(x) = -11x - 4, \text{ find } (f \circ g)(-7).`

#### `fn_evaluate` — implemented

- **Description:** Evaluate f(a) for linear/quadratic f
- **Strategy:** `evaluate`
- **D gate:** d_min=0, d_max=None, d_weight=1.5
- **OpenStax case:** Evaluate a function (A2 General Functions)
- **Book / section:** intermediate-algebra-2e / 10.1 Finding Composite and Inverse Functions
- **type_id / leaves:** `a2_general_functions_evaluating`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`a2_general_functions_evaluating` D=5.0 seed=41: `\text{If } f(x) = (x + 2)^2, \text{ find } f(3).` _live generate type_id `a2_general_functions_evaluating`_
  - [live_generate] type=`a2_general_functions_evaluating` D=10.0 seed=107: `\text{If } f(x) = -x + 3, \text{ find } f(0).` _live generate type_id `a2_general_functions_evaluating`_

#### `fn_inverse` — stub

- **Description:** Find inverse of a linear function
- **Strategy:** `inverse`
- **D gate:** d_min=4, d_max=None, d_weight=1.6
- **OpenStax case:** §10.1 Find the inverse of a function
- **Book / section:** intermediate-algebra-2e / 10.1 Finding Composite and Inverse Functions
- **type_id / leaves:** `a2_general_functions_inverses`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `fn_one_to_one` — deferred

- **Description:** Determine whether a function is one-to-one
- **Strategy:** `horizontal_line_test`
- **D gate:** d_min=2, d_max=None, d_weight=1.0
- **OpenStax case:** §10.1 Determine whether a function is one-to-one — no A2 leaf
- **Book / section:** intermediate-algebra-2e / 10.1 Finding Composite and Inverse Functions
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

## Algebra 1

### Catalog `algebra1_linear_equations`

- **Title:** OpenStax Elementary Algebra 2e — linear equations form taxonomy (Ch. 2)
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/algebra1_linear_equations.json`
- **OpenStax:** elementary-algebra-2e — 2.4 Use a General Strategy to Solve Linear Equations
- **URL:** https://openstax.org/books/elementary-algebra-2e/pages/2-4-use-a-general-strategy-to-solve-linear-equations
- **Stage-1 mining:** `scripts/output/example_mining/elementary-algebra-2e/stage1/2-4-use-a-general-strategy-to-solve-linear-equations.json`
- **Forms:** 7 (implemented=6, stub=1, deferred=0)
- **Taxonomy notes:** Algebraic equation forms only — no graphing.

#### `one_step_add_sub` — implemented

- **Description:** x ± a = b — addition/subtraction property
- **Strategy:** `one_step`
- **D gate:** d_min=0, d_max=8, d_weight=1.0
- **OpenStax case:** §2.1
- **Book / section:** elementary-algebra-2e / 2.4 Use a General Strategy to Solve Linear Equations
- **type_id / leaves:** `one_step_equations`
- **Cited exercises / examples:**
  - `fs-id1168345419326` Example 2.1: `x = \frac{3}{2} ; 4 x - 2 = 2 x + 1`
  - `fs-id1168345195281` Example 2.2: `y + 37 = −13 .`
- **Generated twins (gallery / live):**
  - [live_generate] type=`one_step_equations` D=5.0 seed=41: `-3x = -12` _live generate type_id `one_step_equations`_
  - [live_generate] type=`one_step_equations` D=10.0 seed=107: `-2x = -1` _live generate type_id `one_step_equations`_

#### `one_step_mul_div` — implemented

- **Description:** ax = b or x/a = b — multiplication/division property
- **Strategy:** `one_step`
- **D gate:** d_min=0, d_max=8, d_weight=1.0
- **OpenStax case:** §2.2
- **Book / section:** elementary-algebra-2e / 2.4 Use a General Strategy to Solve Linear Equations
- **type_id / leaves:** `one_step_equations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`one_step_equations` D=5.0 seed=41: `-3x = -12` _live generate type_id `one_step_equations`_
  - [live_generate] type=`one_step_equations` D=10.0 seed=107: `-2x = -1` _live generate type_id `one_step_equations`_

#### `two_step` — implemented

- **Description:** ax ± b = c — two-step linear
- **Strategy:** `two_step`
- **D gate:** d_min=2, d_max=None, d_weight=1.4
- **OpenStax case:** §2.2–2.3
- **Book / section:** elementary-algebra-2e / 2.4 Use a General Strategy to Solve Linear Equations
- **type_id / leaves:** `two_step_equations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`two_step_equations` D=5.0 seed=41: `-x + 3 = -1` _live generate type_id `two_step_equations`_
  - [live_generate] type=`two_step_equations` D=10.0 seed=107: `-x - 2 = -\frac{5}{2}` _live generate type_id `two_step_equations`_

#### `vars_both_sides` — implemented

- **Description:** Variables and constants on both sides
- **Strategy:** `collect_both_sides`
- **D gate:** d_min=4, d_max=None, d_weight=1.5
- **OpenStax case:** §2.3
- **Book / section:** elementary-algebra-2e / 2.4 Use a General Strategy to Solve Linear Equations
- **type_id / leaves:** `two_step_equations`, `multi_step_equations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`two_step_equations` D=5.0 seed=41: `-x + 3 = -1` _live generate type_id `two_step_equations`_
  - [live_generate] type=`two_step_equations` D=10.0 seed=107: `-x - 2 = -\frac{5}{2}` _live generate type_id `two_step_equations`_
  - [live_generate] type=`multi_step_equations` D=5.0 seed=41: `\left(x + 2\right)3 - 5 = \left(x + 1\right)\left(-3\right) + 11x + 44` _live generate type_id `multi_step_equations`_

#### `multi_step_distribute` — implemented

- **Description:** Distribute, combine like terms, both sides (general strategy)
- **Strategy:** `general_strategy`
- **D gate:** d_min=6, d_max=None, d_weight=1.8
- **OpenStax case:** §2.4
- **Book / section:** elementary-algebra-2e / 2.4 Use a General Strategy to Solve Linear Equations
- **type_id / leaves:** `multi_step_equations`
- **Cited exercises / examples:**
  - `fs-id1166503246595` Example 2.37: `−6 (x + 3) = 24 .`
  - `fs-id1166503471619` Example 2.38: `− (y + 9) = 8 .`
  - `fs-id1166503131348` Example 2.39: `5 (a - 3) + 5 = −10`
- **Generated twins (gallery / live):**
  - [live_generate] type=`multi_step_equations` D=5.0 seed=41: `\left(x + 2\right)3 - 5 = \left(x + 1\right)\left(-3\right) + 11x + 44` _live generate type_id `multi_step_equations`_
  - [live_generate] type=`multi_step_equations` D=10.0 seed=107: `\left(-x - 1\right) * 2 + 4x + 3 = \left(x + 1\right) * 2 - 4x + \frac{1}{3}` _live generate type_id `multi_step_equations`_

#### `fraction_or_decimal_coeffs` — stub

- **Description:** Clear denominators / ×10ⁿ for fraction or decimal coefficients
- **Strategy:** `clear_denominators`
- **D gate:** d_min=8, d_max=None, d_weight=1.2
- **OpenStax case:** §2.5 — partial: folded into multi-step, no dedicated mode
- **Book / section:** elementary-algebra-2e / 2.4 Use a General Strategy to Solve Linear Equations
- **type_id / leaves:** `multi_step_equations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `literal_equation` — implemented

- **Description:** Solve a formula for a specified variable
- **Strategy:** `literal`
- **D gate:** d_min=4, d_max=None, d_weight=1.0
- **OpenStax case:** §2.6
- **Book / section:** elementary-algebra-2e / 2.4 Use a General Strategy to Solve Linear Equations
- **type_id / leaves:** `literal_equations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`literal_equations` D=5.0 seed=41: `2x + 1y = 2 \quad \text{Solve for } y.` _live generate type_id `literal_equations`_
  - [live_generate] type=`literal_equations` D=10.0 seed=107: `A = \frac{1}{2} b h \quad \text{Solve for } h.` _live generate type_id `literal_equations`_

### Catalog `algebra1_polynomials`

- **Title:** OpenStax Elementary Algebra 2e — polynomial operations form taxonomy (Ch. 6)
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/algebra1_polynomials.json`
- **OpenStax:** elementary-algebra-2e — 6.3 Multiply Polynomials
- **URL:** https://openstax.org/books/elementary-algebra-2e/pages/6-3-multiply-polynomials
- **Stage-1 mining:** `scripts/output/example_mining/elementary-algebra-2e/stage1/6-3-multiply-polynomials.json`
- **Forms:** 9 (implemented=8, stub=1, deferred=0)
- **Taxonomy notes:** Algebraic poly ops only — no graphing.

#### `poly_add_subtract` — implemented

- **Description:** Add or subtract polynomials (combine like terms)
- **Strategy:** `like_terms`
- **D gate:** d_min=0, d_max=None, d_weight=1.0
- **OpenStax case:** §6.1
- **Book / section:** elementary-algebra-2e / 6.3 Multiply Polynomials
- **type_id / leaves:** `polynomial_add_subtract`, `simplify_polynomials`
- **Cited exercises / examples:**
  - `fs-id1169596297065` Example 6.1: `4 y^{2} - 8 y - 6 ; −5 a^{4} b^{2} ; 2 x^{5} - 5 x^{3} - 9 x^{2} + 3 x + 4 ; 13 - 5 m^{3} ; q`
  - `fs-id1169596396655` Example 6.2: `10 y ; 4 x^{3} - 7 x + 5 ; −15 ; −8 b^{2} + 9 b - 2 ; 8 x y^{2} + 2 y`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`polynomial_add_subtract` D=0.0 seed=945: `\text{Simplify: } \left(3x^{2} - 1\right) + \left(3x^{2} - 1\right)` _type_id sibling `polynomial_add_subtract` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`polynomial_add_subtract` D=0.0 seed=1011: `\text{Simplify: } \left(x^{2} + 3\right) + \left(2x^{2} + 1\right)` _type_id sibling `polynomial_add_subtract` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`polynomial_add_subtract` D=0.0 seed=1137: `\text{Simplify: } \left(2x^{2} + 3\right) + \left(3x + 1\right)` _type_id sibling `polynomial_add_subtract` (not form_id-exact)_

#### `exponent_product_rules` — implemented

- **Description:** Multiply monomials via exponent product / power rules
- **Strategy:** `exponent_laws`
- **D gate:** d_min=0, d_max=None, d_weight=1.0
- **OpenStax case:** §6.2
- **Book / section:** elementary-algebra-2e / 6.3 Multiply Polynomials
- **type_id / leaves:** `properties_of_exponents`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`properties_of_exponents` D=5.0 seed=41: `\frac{y^{3}}{y^{2}}` _live generate type_id `properties_of_exponents`_
  - [live_generate] type=`properties_of_exponents` D=10.0 seed=107: `a^{5} \cdot a^{7}` _live generate type_id `properties_of_exponents`_

#### `mono_times_poly` — implemented

- **Description:** Monomial × polynomial distribute
- **Strategy:** `distribute`
- **D gate:** d_min=0, d_max=10, d_weight=1.2
- **OpenStax case:** §6.3
- **Book / section:** elementary-algebra-2e / 6.3 Multiply Polynomials
- **type_id / leaves:** `polynomial_multiply`
- **Cited exercises / examples:**
  - `fs-id1169596273441` Example 6.28: `4 (x + 3) .`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=0.0 seed=760: `\text{Multiply: } \left(2x\right)\left(x + 3\right)` _matched gallery shape_id~strategy `distribute`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=0.0 seed=826: `\text{Multiply: } \left(x\right)\left(2x - 1\right)` _matched gallery shape_id~strategy `distribute`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=0.0 seed=952: `\text{Multiply: } \left(x\right)\left(x + 2\right)` _matched gallery shape_id~strategy `distribute`_

#### `binomial_times_binomial` — implemented

- **Description:** FOIL / (ax+b)(cx+d)
- **Strategy:** `foil`
- **D gate:** d_min=3, d_max=None, d_weight=1.5
- **OpenStax case:** §6.3
- **Book / section:** elementary-algebra-2e / 6.3 Multiply Polynomials
- **type_id / leaves:** `polynomial_multiply`
- **Cited exercises / examples:**
  - `fs-id1169596397391` Example 6.29: `y (y - 2) .`
  - `fs-id1169596319379` Example 6.30: `7 x (2 x + y) .`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=3.0 seed=877: `\text{Multiply: } \left(3x + 1\right)\left(x + 1\right)` _matched gallery shape_id~strategy `foil`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=6.0 seed=862: `\text{Multiply: } \left(3x^{2} + 4\right)\left(4x + 3\right)` _matched gallery shape_id~strategy `foil`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_multiply` D=6.0 seed=928: `\text{Multiply: } \left(2x^{2} + 1\right)\left(-x + 1\right)` _matched gallery shape_id~strategy `foil`_

#### `special_product_square` — implemented

- **Description:** (a±b)² expand
- **Strategy:** `special_square`
- **D gate:** d_min=2, d_max=None, d_weight=1.3
- **OpenStax case:** §6.4
- **Book / section:** elementary-algebra-2e / 6.3 Multiply Polynomials
- **type_id / leaves:** `polynomial_multiply_special`
- **Cited exercises / examples:**
  - `fs-id1169596316193` Example 6.47: `(x + 5)^{2} .`
  - `fs-id1169596365341` Example 6.48: `(y - 3)^{2} .`
- **Generated twins (gallery / live):**
  - [live_generate] type=`polynomial_multiply_special` D=5.0 seed=41: `\text{Multiply: } \left(x - 3\right)^{2}` _live generate type_id `polynomial_multiply_special`_
  - [live_generate] type=`polynomial_multiply_special` D=10.0 seed=107: `\text{Multiply: } \left(x + 2\right)\left(x - 1\right)` _live generate type_id `polynomial_multiply_special`_

#### `special_product_diff_squares` — implemented

- **Description:** (a−b)(a+b) → a²−b²
- **Strategy:** `diff_squares_expand`
- **D gate:** d_min=2, d_max=None, d_weight=1.2
- **OpenStax case:** §6.4
- **Book / section:** elementary-algebra-2e / 6.3 Multiply Polynomials
- **type_id / leaves:** `polynomial_multiply_special`
- **Cited exercises / examples:**
  - `fs-id1169596402057` Example 6.49: `(4 x + 6)^{2} .`
- **Generated twins (gallery / live):**
  - [live_generate] type=`polynomial_multiply_special` D=5.0 seed=41: `\text{Multiply: } \left(x - 3\right)^{2}` _live generate type_id `polynomial_multiply_special`_
  - [live_generate] type=`polynomial_multiply_special` D=10.0 seed=107: `\text{Multiply: } \left(x + 2\right)\left(x - 1\right)` _live generate type_id `polynomial_multiply_special`_

#### `divide_monomials` — stub

- **Description:** Quotient of monomials (OpenStax separates from long division)
- **Strategy:** `monomial_quotient`
- **D gate:** d_min=2, d_max=None, d_weight=1.0
- **OpenStax case:** §6.5 — partial via properties_of_exponents
- **Book / section:** elementary-algebra-2e / 6.3 Multiply Polynomials
- **type_id / leaves:** `properties_of_exponents`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `polynomial_long_division` — implemented

- **Description:** Divide polynomials (long division)
- **Strategy:** `long_division`
- **D gate:** d_min=8, d_max=None, d_weight=1.0
- **OpenStax case:** §6.6
- **Book / section:** elementary-algebra-2e / 6.3 Multiply Polynomials
- **type_id / leaves:** `polynomial_long_division`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`polynomial_long_division` D=5.0 seed=41: `\frac{40x^{4}+7x^{3}-51x^{2}+6x+9}{8x+3}` _live generate type_id `polynomial_long_division`_
  - [live_generate] type=`polynomial_long_division` D=10.0 seed=107: `\frac{9x^{3}+79x^{2}-22x-36}{x+9}` _live generate type_id `polynomial_long_division`_

#### `integer_exponents_sci_notation` — implemented

- **Description:** Negative exponents / scientific notation
- **Strategy:** `sci_notation`
- **D gate:** d_min=4, d_max=None, d_weight=0.9
- **OpenStax case:** §6.7
- **Book / section:** elementary-algebra-2e / 6.3 Multiply Polynomials
- **type_id / leaves:** `properties_of_exponents`, `scientific_notation_write`, `scientific_notation_operations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`properties_of_exponents` D=5.0 seed=41: `\frac{y^{3}}{y^{2}}` _live generate type_id `properties_of_exponents`_
  - [live_generate] type=`properties_of_exponents` D=10.0 seed=107: `a^{5} \cdot a^{7}` _live generate type_id `properties_of_exponents`_
  - [live_generate] type=`scientific_notation_write` D=5.0 seed=41: `\text{Write in standard form: } 3.9 \times 10^{2}` _live generate type_id `scientific_notation_write`_

### Catalog `algebra1_factoring`

- **Title:** OpenStax Elementary Algebra 2e — factoring form taxonomy (Ch. 7)
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/algebra1_factoring.json`
- **OpenStax:** elementary-algebra-2e — 7.5 General Strategy for Factoring Polynomials
- **URL:** https://openstax.org/books/elementary-algebra-2e/pages/7-5-general-strategy-for-factoring-polynomials
- **Stage-1 mining:** `scripts/output/example_mining/elementary-algebra-2e/stage1/7-5-general-strategy-for-factoring-polynomials.json`
- **Forms:** 10 (implemented=8, stub=1, deferred=1)
- **Wired type_ids (catalog):** `polynomial_factoring_general_strategy`, `quadratic_factoring`, `polynomial_factoring_special_cases`
- **Taxonomy notes:** Forms mirror OpenStax Elementary Algebra 2e Ch. 7 decision tree: GCF first, then by term count (binomial special / trinomial monic or ax²+bx+c / grouping).

#### `gcf_monomial` — implemented

- **Description:** Factor out a monomial GCF; residual may remain unfactored (OpenStax §7.1)
- **Strategy:** `factor_gcf`
- **D gate:** d_min=0, d_max=14, d_weight=1.2
- **OpenStax case:** §7.1 Example 7.1–7.3 — find / factor GCF
- **Book / section:** elementary-algebra-2e / 7.5 General Strategy for Factoring Polynomials
- **type_id / leaves:** `polynomial_factoring_common_factor`, `polynomial_factoring_general_strategy`
- **Cited exercises / examples:**
  - `fs-id1168345255661` Example 7.1: `How to Find the Greatest Common Factor of Two or More Expressions Find the GCF of 54 and 36.`
  - `fs-id1168345342784` Example 7.2: `27 x^{3} \text{and} 18 x^{4}`
  - `fs-id1168341863655` Example 7.3: `4 x^{2} y , 6 x y^{3}`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`polynomial_factoring_common_factor` D=0.0 seed=649: `\text{Factor: } 6x + 3` _matched gallery shape_id~strategy `factor_gcf`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_factoring_common_factor` D=0.0 seed=715: `\text{Factor: } 3x + 6` _matched gallery shape_id~strategy `factor_gcf`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_factoring_common_factor` D=3.0 seed=700: `\text{Factor: } 4 + 4x + 2x^{2}` _matched gallery shape_id~strategy `factor_gcf`_

#### `factor_by_grouping` — implemented

- **Description:** Four-term polynomial factors by grouping (OpenStax §7.1)
- **Strategy:** `grouping`
- **D gate:** d_min=3, d_max=None, d_weight=1.0
- **OpenStax case:** §7.1 factor by grouping
- **Book / section:** elementary-algebra-2e / 7.5 General Strategy for Factoring Polynomials
- **type_id / leaves:** `polynomial_factoring_grouping`, `polynomial_factoring_general_strategy`
- **Cited exercises / examples:**
  - `fs-id1168345688810` Example 7.4: `21 x^{3} , 9 x^{2} , 15 x`
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_by_grouping` D=6.0 seed=931: `3x^{3} + 12x^{2} - 2x - 8` _alias `grouping_cubic`_
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_by_grouping` D=6.0 seed=1123: `2x^{3} + 4x^{2} - 4x - 8` _alias `grouping_cubic`_
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_by_grouping` D=8.0 seed=965: `4x^{3} - 8x^{2} + 5x - 10` _alias `grouping_cubic`_

#### `trinomial_x2_bx_c` — implemented

- **Description:** Factor monic trinomial x² + bx + c (OpenStax §7.2)
- **Strategy:** `trial_factors`
- **D gate:** d_min=0, d_max=12, d_weight=1.6
- **OpenStax case:** §7.2 Example 7.17–7.19
- **Book / section:** elementary-algebra-2e / 7.5 General Strategy for Factoring Polynomials
- **type_id / leaves:** `quadratic_factoring`, `polynomial_factoring_general_strategy`
- **Cited exercises / examples:**
  - `fs-id1168344333319` Example 7.17: `x^{2} + b x + c ; x^{2} + 7 x + 12`
  - `fs-id1168344523984` Example 7.18: `u^{2} + 11 u + 24`
  - `fs-id1168344083254` Example 7.19: `y^{2} + 17 y + 60`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`polynomial_factoring_common_factor` D=0.0 seed=649: `\text{Factor: } 6x + 3` _alias `factor_gcf`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_factoring_common_factor` D=0.0 seed=715: `\text{Factor: } 3x + 6` _alias `factor_gcf`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_factoring_common_factor` D=3.0 seed=700: `\text{Factor: } 4 + 4x + 2x^{2}` _alias `factor_gcf`_

#### `trinomial_ax2_bx_c` — implemented

- **Description:** Factor non-monic ax² + bx + c via trial / ac method (OpenStax §7.3)
- **Strategy:** `ac_method`
- **D gate:** d_min=6, d_max=None, d_weight=1.8
- **OpenStax case:** §7.3 Example 7.29+
- **Book / section:** elementary-algebra-2e / 7.5 General Strategy for Factoring Polynomials
- **type_id / leaves:** `quadratic_factoring`, `polynomial_factoring_general_strategy`
- **Cited exercises / examples:**
  - `fs-id1168345435723` Example 7.29: `6 y^{2} - 72 ; r^{2} - 10 r - 24 ; p^{2} + 5 p + p q + 5 q`
  - `fs-id1168345330140` Example 7.30: `2 n^{2} - 8 n - 42`
  - `fs-id1168345274691` Example 7.31: `4 y^{2} - 36 y + 56`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`polynomial_factoring_common_factor` D=0.0 seed=649: `\text{Factor: } 6x + 3` _alias `factor_gcf`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_factoring_common_factor` D=0.0 seed=715: `\text{Factor: } 3x + 6` _alias `factor_gcf`_
  - [gallery:a1_algebraic_gallery] type=`polynomial_factoring_common_factor` D=3.0 seed=700: `\text{Factor: } 4 + 4x + 2x^{2}` _alias `factor_gcf`_

#### `trinomial_x2_bxy_cy2` — stub

- **Description:** Factor x² + bxy + cy² (two-variable monic trinomial, OpenStax §7.2)
- **Strategy:** `trial_factors_two_var`
- **D gate:** d_min=8, d_max=None, d_weight=1.0
- **OpenStax case:** §7.2 Factor Trinomials of the Form x² + bxy + cy²
- **Book / section:** elementary-algebra-2e / 7.5 General Strategy for Factoring Polynomials
- **type_id / leaves:** `quadratic_factoring`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`quadratic_factoring` D=0.0 seed=109: `x^{2}+7x+12` _type_id sibling `quadratic_factoring` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`quadratic_factoring` D=0.0 seed=175: `x^{2}+5x+4` _type_id sibling `quadratic_factoring` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`quadratic_factoring` D=0.0 seed=301: `x^{2}-5x+6` _type_id sibling `quadratic_factoring` (not form_id-exact)_

#### `difference_of_squares` — implemented

- **Description:** Factor a² − b² (OpenStax §7.4)
- **Strategy:** `difference_of_squares`
- **D gate:** d_min=0, d_max=None, d_weight=1.4
- **OpenStax case:** §7.4 difference of squares
- **Book / section:** elementary-algebra-2e / 7.5 General Strategy for Factoring Polynomials
- **type_id / leaves:** `polynomial_factoring_special_cases`, `polynomial_factoring_general_strategy`
- **Cited exercises / examples:**
  - `fs-id1168345414926` Example 7.42: `9 x^{2} + 12 x + 4`
  - `fs-id1168345273788` Example 7.43: `81 y^{2} - 72 y + 16`
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_sum_difference_of_cubes` D=0.0 seed=218: `x^{3} - 8` _alias `difference_of_cubes`_
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_sum_difference_of_cubes` D=0.0 seed=284: `x^{3} - 1` _alias `difference_of_cubes`_
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_sum_difference_of_cubes` D=6.0 seed=320: `y^{3} - 125` _alias `difference_of_cubes`_

#### `perfect_square_trinomial` — implemented

- **Description:** Factor a² ± 2ab + b² (OpenStax §7.4)
- **Strategy:** `perfect_square`
- **D gate:** d_min=2, d_max=None, d_weight=1.3
- **OpenStax case:** §7.4 perfect-square trinomials
- **Book / section:** elementary-algebra-2e / 7.5 General Strategy for Factoring Polynomials
- **type_id / leaves:** `polynomial_factoring_special_cases`, `polynomial_factoring_general_strategy`
- **Cited exercises / examples:**
  - `fs-id1168345390064` Example 7.44: `36 x^{2} + 84 x y + 49 y^{2}`
  - `fs-id1168345251566` Example 7.45: `9 x^{2} + 50 x + 25`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`quadratic_factoring` D=0.0 seed=109: `x^{2}+7x+12` _type_id sibling `quadratic_factoring` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`quadratic_factoring` D=0.0 seed=175: `x^{2}+5x+4` _type_id sibling `quadratic_factoring` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`quadratic_factoring` D=0.0 seed=301: `x^{2}-5x+6` _type_id sibling `quadratic_factoring` (not form_id-exact)_

#### `sum_diff_cubes` — deferred

- **Description:** Factor a³ ± b³ (OpenStax Intermediate / A2; light in Elem Alg §7.4)
- **Strategy:** `sum_diff_cubes`
- **D gate:** d_min=10, d_max=None, d_weight=0.8
- **OpenStax case:** Cubes primarily A2 leaf polynomial_factoring_sum_diff_cubes
- **Book / section:** elementary-algebra-2e / 7.5 General Strategy for Factoring Polynomials
- **type_id / leaves:** `polynomial_factoring_sum_diff_cubes`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_sum_difference_of_cubes` D=0.0 seed=218: `x^{3} - 8` _alias `difference_of_cubes`_
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_sum_difference_of_cubes` D=0.0 seed=284: `x^{3} - 1` _alias `difference_of_cubes`_
  - [gallery:a2_algebraic_gallery] type=`a2_polynomial_functions_factoring_sum_difference_of_cubes` D=6.0 seed=320: `y^{3} - 125` _alias `difference_of_cubes`_

#### `gcf_then_pattern` — implemented

- **Description:** GCF first, then residual special/trinomial pattern (general strategy Hard)
- **Strategy:** `gcf_then_pattern`
- **D gate:** d_min=10, d_max=None, d_weight=1.5
- **OpenStax case:** §7.5 general strategy — GCF then second pattern
- **Book / section:** elementary-algebra-2e / 7.5 General Strategy for Factoring Polynomials
- **type_id / leaves:** `polynomial_factoring_general_strategy`
- **Cited exercises / examples:**
  - `fs-id1168343047249` Example 7.59: `4 x^{5} + 12 x^{4}`
  - `fs-id1168343113466` Example 7.60: `12 x^{2} - 11 x + 2`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`quadratic_factoring` D=0.0 seed=109: `x^{2}+7x+12` _type_id sibling `quadratic_factoring` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`quadratic_factoring` D=0.0 seed=175: `x^{2}+5x+4` _type_id sibling `quadratic_factoring` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`quadratic_factoring` D=0.0 seed=301: `x^{2}-5x+6` _type_id sibling `quadratic_factoring` (not form_id-exact)_

#### `quadratic_equation_factor` — implemented

- **Description:** Solve ax²+bx+c=0 by factoring / zero-product (OpenStax §7.6)
- **Strategy:** `zero_product`
- **D gate:** d_min=4, d_max=None, d_weight=1.2
- **OpenStax case:** §7.6 quadratic equations by factoring
- **Book / section:** elementary-algebra-2e / 7.5 General Strategy for Factoring Polynomials
- **type_id / leaves:** `quadratic_factoring_equations`
- **Cited exercises / examples:**
  - `fs-id1168341961578` Example 7.69: `(x + 1) (x - 4) = 0`
  - `fs-id1168345549988` Example 7.70: `(5 n - 2) (6 n - 1) = 0`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`quadratic_factoring` D=0.0 seed=109: `x^{2}+7x+12` _type_id sibling `quadratic_factoring` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`quadratic_factoring` D=0.0 seed=175: `x^{2}+5x+4` _type_id sibling `quadratic_factoring` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`quadratic_factoring` D=0.0 seed=301: `x^{2}-5x+6` _type_id sibling `quadratic_factoring` (not form_id-exact)_

### Catalog `algebra1_rationals`

- **Title:** OpenStax Elementary Algebra 2e — rational expressions form taxonomy (Ch. 8)
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/algebra1_rationals.json`
- **OpenStax:** elementary-algebra-2e — 8.1 Simplify Rational Expressions
- **URL:** https://openstax.org/books/elementary-algebra-2e/pages/8-1-simplify-rational-expressions
- **Stage-1 mining:** `scripts/output/example_mining/elementary-algebra-2e/stage1/8-1-simplify-rational-expressions.json`
- **Forms:** 7 (implemented=5, stub=1, deferred=1)
- **Wired type_ids (catalog):** `rational_simplification`
- **Taxonomy notes:** Algebraic rational forms only — no graphing applications beyond equation solving.

#### `simplify_cancel` — implemented

- **Description:** Factor numerator/denominator and cancel common factors
- **Strategy:** `factor_cancel`
- **D gate:** d_min=0, d_max=None, d_weight=1.5
- **OpenStax case:** §8.1
- **Book / section:** elementary-algebra-2e / 8.1 Simplify Rational Expressions
- **type_id / leaves:** `rational_simplification`, `rational_expression_simplification`
- **Cited exercises / examples:**
  - `fs-id1169596588865` Example 8.1: `\frac{9 y}{x} ; \frac{4 b - 3}{2 b + 5} ; \frac{x + 4}{x^{2} + 5 x + 6}`
  - `fs-id1169596584785` Example 8.2: `\frac{2 x + 3}{3 x - 5} ; x = 0 ; x = 2 ; x = −3`
  - `fs-id1169596363395` Example 8.3: `\frac{x^{2} + 8 x + 7}{x^{2} - 4} ; x = 0 ; x = 2 ; x = −1`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=485: `\frac{x+3}{x^{2}+4x+3}` _type_id sibling `rational_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=551: `\frac{2x-10}{2x^{2}-18x+40}` _type_id sibling `rational_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=677: `\frac{5x+20}{5x+20}` _type_id sibling `rational_simplification` (not form_id-exact)_

#### `multiply_divide` — implemented

- **Description:** Multiply or divide rationals (factor then cancel across)
- **Strategy:** `mul_div`
- **D gate:** d_min=4, d_max=None, d_weight=1.2
- **OpenStax case:** §8.2
- **Book / section:** elementary-algebra-2e / 8.1 Simplify Rational Expressions
- **type_id / leaves:** `rational_expression_multiply_divide`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=485: `\frac{x+3}{x^{2}+4x+3}` _type_id sibling `rational_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=551: `\frac{2x-10}{2x^{2}-18x+40}` _type_id sibling `rational_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=677: `\frac{5x+20}{5x+20}` _type_id sibling `rational_simplification` (not form_id-exact)_

#### `add_sub_common_denom` — implemented

- **Description:** ± rationals with a common denominator
- **Strategy:** `combine_like_denoms`
- **D gate:** d_min=3, d_max=None, d_weight=1.3
- **OpenStax case:** §8.3
- **Book / section:** elementary-algebra-2e / 8.1 Simplify Rational Expressions
- **type_id / leaves:** `rational_expression_simplification`
- **Cited exercises / examples:**
  - `fs-id1169595185567` Example 8.30: `\frac{5}{18} + \frac{7}{18} .`
  - `fs-id1169597570539` Example 8.31: `\frac{3 y}{4 y - 3} + \frac{7}{4 y - 3} .`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`rational_expression_simplification` D=0.0 seed=388: `\frac{-1}{x+1} + \frac{-1}{x+1}` _type_id sibling `rational_expression_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_expression_simplification` D=0.0 seed=454: `\frac{2}{x-3} + \frac{1}{3x-9}` _type_id sibling `rational_expression_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_expression_simplification` D=0.0 seed=580: `\frac{-4}{3x-12} + \frac{-3}{x-4}` _type_id sibling `rational_expression_simplification` (not form_id-exact)_

#### `add_sub_unlike_denoms` — implemented

- **Description:** ± rationals with unlike denominators (LCD)
- **Strategy:** `lcd_combine`
- **D gate:** d_min=6, d_max=None, d_weight=1.5
- **OpenStax case:** §8.4
- **Book / section:** elementary-algebra-2e / 8.1 Simplify Rational Expressions
- **type_id / leaves:** `rational_expression_simplification`
- **Cited exercises / examples:**
  - `fs-id1169597368792` Example 8.38: `\frac{8}{x^{2} - 2 x - 3} , \frac{3 x}{x^{2} + 4 x + 3}`
  - `fs-id1169597688690` Example 8.39: `(x + 1) (x - 3) (x + 3) ; \frac{8}{x^{2} - 2 x - 3} , \frac{3 x}{x^{2} + 4 x + 3} .`
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`rational_expression_simplification` D=0.0 seed=388: `\frac{-1}{x+1} + \frac{-1}{x+1}` _type_id sibling `rational_expression_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_expression_simplification` D=0.0 seed=454: `\frac{2}{x-3} + \frac{1}{3x-9}` _type_id sibling `rational_expression_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_expression_simplification` D=0.0 seed=580: `\frac{-4}{3x-12} + \frac{-3}{x-4}` _type_id sibling `rational_expression_simplification` (not form_id-exact)_

#### `complex_rational` — deferred

- **Description:** Simplify a complex rational expression
- **Strategy:** `complex_fraction`
- **D gate:** d_min=10, d_max=None, d_weight=1.0
- **OpenStax case:** §8.5 — A2 home (complex_fractions)
- **Book / section:** elementary-algebra-2e / 8.1 Simplify Rational Expressions
- **type_id / leaves:** `complex_fractions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=485: `\frac{x+3}{x^{2}+4x+3}` _type_id sibling `rational_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=551: `\frac{2x-10}{2x^{2}-18x+40}` _type_id sibling `rational_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=677: `\frac{5x+20}{5x+20}` _type_id sibling `rational_simplification` (not form_id-exact)_

#### `rational_equation` — implemented

- **Description:** Solve rational equations; check extraneous
- **Strategy:** `clear_denoms_solve`
- **D gate:** d_min=6, d_max=None, d_weight=1.2
- **OpenStax case:** §8.6
- **Book / section:** elementary-algebra-2e / 8.1 Simplify Rational Expressions
- **type_id / leaves:** `rational_expressions_equations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=485: `\frac{x+3}{x^{2}+4x+3}` _type_id sibling `rational_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=551: `\frac{2x-10}{2x^{2}-18x+40}` _type_id sibling `rational_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=677: `\frac{5x+20}{5x+20}` _type_id sibling `rational_simplification` (not form_id-exact)_

#### `proportion_application` — stub

- **Description:** Proportion / similar-figure applications
- **Strategy:** `proportion`
- **D gate:** d_min=4, d_max=None, d_weight=0.8
- **OpenStax case:** §8.7 — partial via solving_proportions
- **Book / section:** elementary-algebra-2e / 8.1 Simplify Rational Expressions
- **type_id / leaves:** `solving_proportions`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=485: `\frac{x+3}{x^{2}+4x+3}` _type_id sibling `rational_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=551: `\frac{2x-10}{2x^{2}-18x+40}` _type_id sibling `rational_simplification` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`rational_simplification` D=0.0 seed=677: `\frac{5x+20}{5x+20}` _type_id sibling `rational_simplification` (not form_id-exact)_

### Catalog `algebra1_radicals`

- **Title:** OpenStax Elementary Algebra 2e — radicals & square roots form taxonomy (Ch. 9 algebraic)
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/algebra1_radicals.json`
- **OpenStax:** elementary-algebra-2e — 9.2 Simplify Square Roots
- **URL:** https://openstax.org/books/elementary-algebra-2e/pages/9-2-simplify-square-roots
- **Stage-1 mining:** `scripts/output/example_mining/elementary-algebra-2e/stage1/9-2-simplify-square-roots.json`
- **Forms:** 7 (implemented=5, stub=1, deferred=1)
- **Taxonomy notes:** Square-root algebraic ops; higher roots / rational exponents deferred to A2 unless product wants Elem Alg parity.

#### `simplify_square_root` — implemented

- **Description:** Factor perfect-square factors out of √
- **Strategy:** `perfect_square_factor`
- **D gate:** d_min=0, d_max=None, d_weight=1.5
- **OpenStax case:** §9.1–9.2
- **Book / section:** elementary-algebra-2e / 9.2 Simplify Square Roots
- **type_id / leaves:** `radical_simplification`
- **Cited exercises / examples:**
  - `fs-id1169594051758` Example 9.12: `\sqrt{50}`
  - `fs-id1169594272843` Example 9.13: `\sqrt{500}`
  - `fs-id1169596287619` Example 9.14: `\sqrt{x^{3}}`
- **Generated twins (gallery / live):**
  - [live_generate] type=`radical_simplification` D=5.0 seed=41: `\sqrt{192}` _live generate type_id `radical_simplification`_
  - [live_generate] type=`radical_simplification` D=10.0 seed=107: `\sqrt{200}` _live generate type_id `radical_simplification`_

#### `add_sub_like_radicals` — implemented

- **Description:** ± like square roots (after optional simplify)
- **Strategy:** `like_radicals`
- **D gate:** d_min=2, d_max=None, d_weight=1.2
- **OpenStax case:** §9.3
- **Book / section:** elementary-algebra-2e / 9.2 Simplify Square Roots
- **type_id / leaves:** `radical_add_subtract`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [gallery:a1_algebraic_gallery] type=`radical_add_subtract` D=0.0 seed=745: `2\sqrt{14} - \sqrt{14}` _type_id sibling `radical_add_subtract` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`radical_add_subtract` D=0.0 seed=811: `\sqrt{5} + 2\sqrt{5}` _type_id sibling `radical_add_subtract` (not form_id-exact)_
  - [gallery:a1_algebraic_gallery] type=`radical_add_subtract` D=0.0 seed=937: `2\sqrt{3} + 4\sqrt{3}` _type_id sibling `radical_add_subtract` (not form_id-exact)_

#### `multiply_square_roots` — implemented

- **Description:** Product rule / FOIL with radicals
- **Strategy:** `product_rule`
- **D gate:** d_min=3, d_max=None, d_weight=1.2
- **OpenStax case:** §9.4
- **Book / section:** elementary-algebra-2e / 9.2 Simplify Square Roots
- **type_id / leaves:** `radical_multiply`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`radical_multiply` D=5.0 seed=41: `\sqrt{8} \cdot \sqrt{13}` _live generate type_id `radical_multiply`_
  - [live_generate] type=`radical_multiply` D=10.0 seed=107: `3\sqrt{20} \cdot 2\sqrt{32}` _live generate type_id `radical_multiply`_

#### `divide_rationalize` — implemented

- **Description:** Divide / rationalize denominator (incl. conjugate)
- **Strategy:** `rationalize`
- **D gate:** d_min=4, d_max=None, d_weight=1.3
- **OpenStax case:** §9.5
- **Book / section:** elementary-algebra-2e / 9.2 Simplify Square Roots
- **type_id / leaves:** `radical_divide`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`radical_divide` D=5.0 seed=41: `\frac{\sqrt{240}}{\sqrt{6}}` _live generate type_id `radical_divide`_
  - [live_generate] type=`radical_divide` D=10.0 seed=107: `\frac{\sqrt{1485}}{\sqrt{11}}` _live generate type_id `radical_divide`_

#### `radical_equation` — implemented

- **Description:** Solve equations with square roots; check extraneous
- **Strategy:** `isolate_square`
- **D gate:** d_min=6, d_max=None, d_weight=1.2
- **OpenStax case:** §9.6
- **Book / section:** elementary-algebra-2e / 9.2 Simplify Square Roots
- **type_id / leaves:** `radical_equations`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`radical_equations` D=5.0 seed=41: `\sqrt{3x + 7} = x - 1` _live generate type_id `radical_equations`_
  - [live_generate] type=`radical_equations` D=10.0 seed=107: `\sqrt{5x - 5} + 3 = x + 2` _live generate type_id `radical_equations`_

#### `higher_roots` — stub

- **Description:** Simplify cube / nth roots
- **Strategy:** `nth_root`
- **D gate:** d_min=8, d_max=None, d_weight=1.0
- **OpenStax case:** §9.7 — missing on A1
- **Book / section:** elementary-algebra-2e / 9.2 Simplify Square Roots
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

#### `rational_exponents` — deferred

- **Description:** a^{m/n} ↔ radical; exponent laws
- **Strategy:** `rational_exp`
- **D gate:** d_min=8, d_max=None, d_weight=0.8
- **OpenStax case:** §9.8 — A2 home
- **Book / section:** elementary-algebra-2e / 9.2 Simplify Square Roots
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

### Catalog `algebra1_quadratics`

- **Title:** OpenStax Elementary Algebra 2e — quadratic solve methods (Ch. 10 algebraic; no graphing)
- **Path:** `question_engine/frameworks/primitives/openstax_form_catalogs/algebra1_quadratics.json`
- **OpenStax:** elementary-algebra-2e — 10.3 Solve Quadratic Equations Using the Quadratic Formula
- **URL:** https://openstax.org/books/elementary-algebra-2e/pages/10-3-solve-quadratic-equations-using-the-quadratic-formula
- **Stage-1 mining:** `scripts/output/example_mining/elementary-algebra-2e/stage1/10-3-solve-quadratic-equations-using-the-quadratic-formula.json`
- **Forms:** 5 (implemented=4, stub=1, deferred=0)
- **Taxonomy notes:** Solve methods only — exclude §10.5 graphing (out of algebraic scope for this catalog).

#### `square_root_property` — implemented

- **Description:** Solve x² = k or (x−h)² = k via ±√
- **Strategy:** `square_root_property`
- **D gate:** d_min=0, d_max=None, d_weight=1.3
- **OpenStax case:** §10.1
- **Book / section:** elementary-algebra-2e / 10.3 Solve Quadratic Equations Using the Quadratic Formula
- **type_id / leaves:** `quadratic_square_roots`
- **Cited exercises / examples:**
  - `fs-id1168345255637` Example 10.1: `x^{2} = 169`
  - `fs-id1168345509987` Example 10.2: `\left(a x\right)^{2} = k ; x^{2} - 48 = 0`
- **Generated twins (gallery / live):**
  - [live_generate] type=`quadratic_square_roots` D=5.0 seed=41: `3(x - 3)^{2} - 48 = 0` _live generate type_id `quadratic_square_roots`_
  - [live_generate] type=`quadratic_square_roots` D=10.0 seed=107: `6(x - 4)^{2} - 150 = 0` _live generate type_id `quadratic_square_roots`_

#### `completing_the_square` — implemented

- **Description:** Complete the square then square-root property
- **Strategy:** `complete_square`
- **D gate:** d_min=6, d_max=None, d_weight=1.4
- **OpenStax case:** §10.2
- **Book / section:** elementary-algebra-2e / 10.3 Solve Quadratic Equations Using the Quadratic Formula
- **type_id / leaves:** `quadratic_completing_square_solve`, `quadratic_completing_square_constant`
- **Cited exercises / examples:**
  - `fs-id1168344331852` Example 10.14: `x^{2} + 14 x`
  - `fs-id1168344150117` Example 10.15: `m^{2} - 26 m`
- **Generated twins (gallery / live):**
  - [live_generate] type=`quadratic_completing_square_solve` D=5.0 seed=41: `3x^{2} + 12x + 39 = 0` _live generate type_id `quadratic_completing_square_solve`_
  - [live_generate] type=`quadratic_completing_square_solve` D=10.0 seed=107: `2x^{2} + 20x + 148 = 0` _live generate type_id `quadratic_completing_square_solve`_
  - [live_generate] type=`quadratic_completing_square_constant` D=5.0 seed=41: `x^{2} + 4x + c \text{ is a perfect square trinomial. Find } c.` _live generate type_id `quadratic_completing_square_constant`_

#### `quadratic_formula` — implemented

- **Description:** Solve via quadratic formula
- **Strategy:** `quadratic_formula`
- **D gate:** d_min=4, d_max=None, d_weight=1.5
- **OpenStax case:** §10.3
- **Book / section:** elementary-algebra-2e / 10.3 Solve Quadratic Equations Using the Quadratic Formula
- **type_id / leaves:** `quadratic_formula`
- **Cited exercises / examples:**
  - `fs-id1166502221779` Example 10.28: `2 x^{2} + 9 x - 5 = 0`
  - `fs-id1166502221189` Example 10.29: `x^{2} - 6 x + 5 = 0`
- **Generated twins (gallery / live):**
  - [live_generate] type=`quadratic_formula` D=5.0 seed=41: `3x^{2} + 9x = 0` _live generate type_id `quadratic_formula`_
  - [live_generate] type=`quadratic_formula` D=10.0 seed=107: `2x^{2} - 22x + 60 = 0` _live generate type_id `quadratic_formula`_

#### `discriminant_classify` — implemented

- **Description:** Use discriminant to classify number/type of roots
- **Strategy:** `discriminant`
- **D gate:** d_min=4, d_max=None, d_weight=1.0
- **OpenStax case:** §10.3 related
- **Book / section:** elementary-algebra-2e / 10.3 Solve Quadratic Equations Using the Quadratic Formula
- **type_id / leaves:** `quadratic_discriminant`
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins (gallery / live):**
  - [live_generate] type=`quadratic_discriminant` D=5.0 seed=41: `\text{Find the discriminant of } 3x^{2} - 3.` _live generate type_id `quadratic_discriminant`_
  - [live_generate] type=`quadratic_discriminant` D=10.0 seed=107: `\text{Find the discriminant of } 2x^{2} + 6x + 5.` _live generate type_id `quadratic_discriminant`_

#### `quadratic_application` — stub

- **Description:** Model → quadratic equation → solve in context
- **Strategy:** `modeling`
- **D gate:** d_min=10, d_max=None, d_weight=1.0
- **OpenStax case:** §10.4 — missing on A1
- **Book / section:** elementary-algebra-2e / 10.3 Solve Quadratic Equations Using the Quadratic Formula
- **Cited exercises:** _(none — section-level inspiration only)_
- **Generated twins:** _(none matched in galleries; status may still be implemented via a different shape_id)_

## Code / section-level inspiration (no per-exercise catalog id)

- **Calc1 limits** (`question_engine/frameworks/primitives/limits.py`): OpenStax Vol.1 §2.3 direct, §4.6 ∞, §4.8 L'Hôpital mirrored in sampler families; now also catalogued in limits.json. openstax_form stamps like direct_{fam}, inf_{fam}, lhopital_*.
- **Calc1 derivatives** (`question_engine/frameworks/primitives/derivatives.py`): Grounded in OpenStax Calc Vol.1 Ch.3 patterns; derivatives.json form catalog added. poly_expression packs also cite OpenStax 3.6 chain+power.
- **Curriculum gaps (section-level only)** (`scripts/output/curriculum_gaps/*.md`): Many OpenStax sections mapped as missing/partial/unwired at curriculum grain — not per-exercise form catalogs. See calculus.md, algebra_1.md, algebra_2.md, precalculus.md.

## Catalog files not yet mirrored under example_mining/form_catalogs

Canonical catalogs live in `openstax_form_catalogs/`. Only `calculus-volume-2/form_catalogs/trig_integrals.json` was mirrored next to stage-1 at inventory time — treat the primitives path as source of truth.

## How to refresh

```powershell
$env:PYTHONPATH='.'
python scripts/output/ml/_build_openstax_form_inventory.py
```
