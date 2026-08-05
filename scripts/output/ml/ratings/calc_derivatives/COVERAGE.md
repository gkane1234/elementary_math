# OpenStax Calc Vol 1 — derivatives coverage checklist

Grounded in stage-1 mining under
`scripts/output/example_mining/calculus-volume-1/stage1/` and generator packs
in `question_engine/frameworks/primitives/derivatives.py` /
`poly_expression.py`.

| Form / skill (OpenStax-informed) | Pack / type_id | Status |
|----------------------------------|----------------|--------|
| Constant / constant-multiple / power | `power` / `calc_diff_power_rule` | Covered |
| Sum / difference of powers | `power` | Covered |
| Negative integer exponents | `power` (D unlock + `allow_negative_exponents` Spec) | Covered (D-gated) |
| Fractional / root exponents | `power` (`allow_roots` / fractional Spec) | Covered (D-gated) |
| Irrational exponents (π, e, √2) | Spec `allow_irrational_exponents` | Partial — unlocks at high D; sparse in rating sweep |
| Product rule (poly × poly) | `product` | Covered |
| Product with specials | `product` / `trig` / `ln_exp` / `general` | Covered when allow_* on |
| Quotient rule | `quotient` | Covered (legacy atom path; `spec_snapshot.pack=legacy_quotient`) |
| Chain rule algebraic `(ax+b)^n` | `chain` | Covered |
| Chain with trig / ln / exp | `chain`, `trig`, `ln_exp` | Covered |
| Nested chain depth ≥2 | `chain` / `general` (D≥~14) | Covered (D-gated) |
| Trig derivatives (sin/cos/tan…) | `trig` | Covered |
| Trig × product / quotient | `trig` | Covered when methods allowed |
| Inverse trig | `invtrig` | Covered |
| Natural ln / exp | `ln_exp` | Covered |
| Other-base log / exp (aˣ, log_a) | `calc_diff_other_base_…` | Structured pack — use `calc_diff_gaps` campaign |
| Logarithmic differentiation | `calc_diff_logarithmic` | Structured pack — use `calc_diff_gaps` campaign |
| Implicit differentiation | `calc_diff_implicit` | Structured pack — use `calc_diff_gaps` campaign |
| Higher-order derivatives | `higher_order` | Covered via Spec (order≥2; soft trig/exp) |
| Definition of derivative | `calc_diff_definition_…` | Gap — out of scope for this pack |
| Rates of change / tables | rates / tables leaves | Gap — out of scope |
| Function powers e.g. tan²(x) | Spec `allow_fn_power` via chain/general/trig | Covered (D≥6) |
| Exotic / mixed general | `general` | Covered |
| Hyperbolic | allow_hyperbolic | Gap — rarely unlocked; not stratified here |

## Gaps intentionally left open

1. **definition / rates / tables** — separate campaigns later (thin Mad-Libs still).
2. **other_base / logarithmic / implicit** — generator ML plumbing ready; build via
   `python scripts/build_hand_rating_set.py --campaign calc_diff_gaps` (does **not**
   overwrite rated `calc_derivatives` items).
3. **Irrational / hyperbolic / deep exotic** — present in knobs but low density at
   default allow-lists; optional follow-up sweep with forced knobs.
4. Full pre-algebra Spec unification is **not** required for this rating push.
5. **higher_order** Spec migration: existing rated Mad-Libs rows keep join keys
   (`rating_id` / type / seed / D) as historical labels; live regen may differ.

## Seed join note

Spec sampling sorts frozenset/class token iteration so `PYTHONHASHSEED` cannot
reshuffle prompts for the same `(type_id, seed, difficulty)`. Rebuild the JSONL
after generator changes before rating if prompts must match live regen.
