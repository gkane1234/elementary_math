# ML / hand-rating training readiness

Status of generation → export → rating plumbing for difficulty learning.
Human campaigns live under `scripts/output/ml/ratings/`.

## Required machine fields (every export / rating row)

| Field | Role |
|-------|------|
| `type_id` | Catalog leaf |
| `generator` | Generator key (when known) |
| `seed` | RNG join |
| `difficulty` | Continuous D |
| `theta_full` | Resolved settings + Spec/structured knobs |
| structural metadata | `function_classes` / `methods_used` / `structure_id` / `effort_features` / `spec_snapshot` when available |

Featurization (`question_engine/ml/features.py`) auto-promotes bool/numeric θ keys and
flattens nested `effort_features` / `spec_snapshot` (`ast_ef_*` / `spec_*`). Prefer
emitting knobs on θ / snapshot over growing allow-lists.

## Course readiness

| Course | Generator θ + structure | Spec / structured packs | Hand-rating campaign | Notes |
|--------|-------------------------|-------------------------|----------------------|-------|
| **Calc derivatives (core)** | Ready | Spec packs + legacy quotient snapshot | `ratings/calc_derivatives/` (partially rated) | Join keys preserved; do not overwrite items blindly |
| **Calc other_base / log-diff / implicit** | Ready | Structured packs (`spec_snapshot.pack=structured_*`) | Build via `--campaign calc_diff_gaps` | Not yet human-rated |
| **Calc higher_order** | Ready | Spec path (`derivative_order` ≥ 2) | Included in `calc_derivatives` | Live regen may differ from older Mad-Libs rows |
| **Calc limits (algebraic)** | Ready | `LimitSpec` packs (direct / ∞ / removable / jump / essential / L'H) | Stub `calc_limits/` | No graph interpretation |
| **Calc integrals (algebraic)** | Ready | `IntegralSpec` + trick pipeline; PFD via `partial_fractions` facade | Stub `calc_integrals/` | u-sub derivative-backed; multi `u_sub→pfd` |
| **Calc linear approx / differentials** | Ready | Structured snapshots on pilot families | Optional with integrals | OpenStax 4.2 |
| **Calc definition / rates / tables** | Thin | Mad-Libs family/structure only | Open | Out of scope for current rating push |
| **Precalc algebraic / intro-calc** | Ready for first rating | Power-rule Spec shared with calc; log/exp/function_ops/PFD emit structured snapshots | `precalc_algebraic/CAMPAIGN.json` (~8 packs) | PFD wraps `construct_pfd` |
| **Algebra 2** | Ready for first rating | Rational / poly / factor / log / function_ops structured packs; inherits A1 primitives | `algebra_2/` (~8 packs) | No A2 PFD leaf; future wrap `construct_pfd` |
| **Algebra 1** | Ready for first rating | Poly / factor / rational / radical structured packs + effort scorers | `algebra_1/` (~8 packs) | Expression subset first |
| **G6 / PA** | Continuous-D + effort scorers | Not Spec-unified | Not required for this push | Keep export JSONL path |

## PFD / rational inheritance

| Leaf / path | Core | Status |
|-------------|------|--------|
| A1/A2 rational simplify + add | `construct_rational_sum` (L2/L3) | Shared; continuous cancel/term knobs |
| PC `pc_partial_fraction_decomposition` | `construct_pfd` via `frameworks.primitives.partial_fractions` | Live; knobs `pfd_term_count`, coef/root spans |
| A2 PFD | — | **No leaf**; future leaf must wrap `construct_pfd` (not a new core) |
| Calc `integral_partial_fractions` | `partial_fractions.combine_pf_to_rational` + ∫/ln adapter | **Wired**; no forked PF seed |
| Calc `integral_multi_trick` (`u_sub→pfd`) | `pf.seed_partial_fraction_target` then linear wrap | **Wired**; `tricks_required: ["u_sub","pfd"]` |

Pedagogy: PFD seeds Σ Aᵢ/(x−rᵢ) then combines (reverse of rational-add). True
bidirectional / reverse-of-add unify can come later; quadratic & repeated
factors still deferred. Do not invent a third PFD sampler.

## Integral trick pipeline (Calc 1)

- **API:** `IntegralSpec` + `TrickPipeline` / `plan_trick_pipeline` in
  `frameworks/primitives/integrals.py`.
- **Modes:** forward form packs; derivative-backed `u_sub`; multi-trick ordered
  list (`tricks_required` on metadata + `spec_snapshot`).
- **Shipped combo:** `["u_sub", "pfd"]` (PFD core from facade, then compose
  linear inner so u-sub is first).
- **Knobs:** `allow_*` / `require_*` techniques; D buys `pipeline_len_2`.

## Algebraic Spec packs (`poly_expression`)

Additive packs (calc packs untouched): `pack_poly_expand`, `pack_poly_product`,
`pack_poly_factor`, `pack_compose_algebraic`. Spec fields: `course_tag`,
`factor_count_min/max`, `composition_depth`. Generators stamp
`spec_snapshot` / `structure_id` via `algebraic_ml.enrich_algebraic_meta`
(constructive engines) or Spec snapshots (function ops / calc).

## What was backfilled (this tranche)

1. **Structured pack metadata** for A1/A2/PC algebraic leaves (poly, factor,
   rational, radical, log/exp, function ops, PFD).
2. **`partial_fractions.py`** facade over existing `construct_pfd` (knobs +
   stable import) — **not** a new PFD core.
3. **Calc limits / integrals Spec** + catalog leaves (`limit_jump`,
   `integral_partial_fractions`, `integral_multi_trick`,
   `linear_approximation`).
4. **Hand-rating packs** expanded to ~8 leaves per `algebra_1` / `algebra_2` /
   `precalc_algebraic` campaign; calc_limits / calc_integrals stubs.
5. **Export path** unchanged: `scripts/export_generation_dataset.py` +
   `build_generation_record` continue to record θ + structural hints.

## What’s still open

1. **Smoke → full build** — run `--smoke` per campaign, then full generate.
2. **Human labels** — none yet outside calc derivatives.
3. **Reverse rational-add ↔ PFD unify** — shared LCD today; true bidirectional
   adapter later.
4. **A2 PFD leaf** — catalog + wrap only when curriculum wants it.
5. **Quadratic / repeated PF factors**; improper integrals; multi-step L'H
   edge forms (∞−∞, 1^∞).
6. **Definition / rates** — still Mad-Libs if those leaves enter a campaign.

## Commands

```powershell
$env:PYTHONPATH='.'

# Gap packs only (safe; separate folder)
python scripts/build_hand_rating_set.py --campaign calc_diff_gaps --smoke

# Calc limits / integrals stubs
python scripts/build_hand_rating_set.py --campaign calc_limits --smoke
python scripts/build_hand_rating_set.py --campaign calc_integrals --smoke

# Non-calc scaffolds (uses CAMPAIGN.json packs)
python scripts/build_hand_rating_set.py --campaign algebra_1 --smoke
python scripts/build_hand_rating_set.py --campaign algebra_2 --smoke
python scripts/build_hand_rating_set.py --campaign precalc_algebraic --smoke

# Export sweep (training JSONL, not hand rater)
python scripts/export_generation_dataset.py --types calc_indef_int_partial_fractions --n-per 2 --out scripts/output/ml/_spot_calc_pfd.jsonl
```

## Join / regen notes

- Primary join keys: `type_id` + `seed` + `difficulty` (+ `rating_id` inside campaigns).
- Existing `calc_derivatives` ratings stay valid as historical labels even when
  generators evolve; rebuild campaign JSONL only when starting a fresh rating pass.
- Structured packs use `spec_snapshot.pack` values like `structured_rational_add`,
  `structured_pfd`, `structured_function_ops`, Spec pack names, or calc
  `structured_*` / `legacy_quotient`.
