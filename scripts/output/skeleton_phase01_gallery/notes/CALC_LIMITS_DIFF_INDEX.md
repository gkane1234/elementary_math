# Calculus limits + differentiation notes (steps 1–3)

Live-sampled D=0/8/16/22 (`seed=101`) on 2026-08-20. Diff defaults to `expr_skeleton`; limits use LimitSpec / `limits.json`.

**Limits / continuity / L'Hôpital shipped** (LimitSpec flesh + gallery) — flags cleared for those leaves.

**All calc_* notes now have `## Limitations`.** Gallery: 68/68 type pages under `skeleton_phase01_gallery/`.

**Implicit (2026-09-14):** catalog-routed §3.8 families (`implicit_basic` circle at D=0; ellipse/xy mid D; trig/exp/folium high D). `UNCLEAR` / `LOW_VARIETY` cleared; `LIMITATIONS` remains (closed-form families, not a general relation AST).

**Logarithmic differentiation (2026-09-14):** catalog-routed §3.9 families (`logdiff_power` at D=0; product/quotient/root mid D; \(x^x\) / \((x+1)^x\) / \((\sin x)^x\) high D). High D cannot emit `logdiff_power`. `LIMITATIONS` remains (closed-form pack, not a general \(u^v\) AST).

**Other-base log/exp (2026-09-14):** catalog-routed §3.9 families (`other_base_a_x` / `other_base_log_x` at D=0; \(a^{kx}\) / \(\log_a(ax+b)\) mid D; \(a^{x^2}\) / \(x a^x\) high D). High D cannot emit leftover \(a^x\). `LIMITATIONS` remains (no Example 3.79 quotient).

**Inverse functions (2026-09-14):** catalog-routed §3.7 IFT families (`invfn_power` at D=0; table/linear mid D; \(\sin x\) / \(\ln\) / \(x^3+x\) high D). D=22 cannot emit leftover \(e^x\). `LIMITATIONS` remains (scaffolded numeric IFT, not a general inverse AST).

## Files

- [`calc_limits_by_direct_evaluation.md`](calc_limits_by_direct_evaluation.md)
- [`calc_limits_at_jump_discontinuities_and_kinks.md`](calc_limits_at_jump_discontinuities_and_kinks.md)
- [`calc_limits_at_removable_discontinuities.md`](calc_limits_at_removable_discontinuities.md)
- [`calc_limits_at_essential_discontinuities.md`](calc_limits_at_essential_discontinuities.md)
- [`calc_limits_at_infinity.md`](calc_limits_at_infinity.md)
- [`calc_continuity_determining_and_classifying.md`](calc_continuity_determining_and_classifying.md)
- [`calc_app_diff_lhopitals_rule.md`](calc_app_diff_lhopitals_rule.md)
- [`calc_diff_power_rule.md`](calc_diff_power_rule.md)
- [`calc_diff_product_rule.md`](calc_diff_product_rule.md)
- [`calc_diff_quotient_rule.md`](calc_diff_quotient_rule.md)
- [`calc_diff_chain_rule.md`](calc_diff_chain_rule.md)
- [`calc_diff_trigonometric.md`](calc_diff_trigonometric.md)
- [`calc_diff_inverse_trigonometric.md`](calc_diff_inverse_trigonometric.md)
- [`calc_diff_natural_logarithms_and_exponentials.md`](calc_diff_natural_logarithms_and_exponentials.md)
- [`calc_diff_general.md`](calc_diff_general.md)
- [`calc_diff_higher_order_derivatives.md`](calc_diff_higher_order_derivatives.md)
- [`calc_diff_implicit.md`](calc_diff_implicit.md)
- [`calc_diff_logarithmic.md`](calc_diff_logarithmic.md)
- [`calc_diff_other_base_logarithms_and_exponentials.md`](calc_diff_other_base_logarithms_and_exponentials.md)
- [`calc_diff_inverse_functions.md`](calc_diff_inverse_functions.md)

## UNCLEAR

_(none on this index — `calc_diff_implicit` catalog-routed 2026-09-14)_

## LOW_VARIETY

_(none on this index)_

See also [`CALC_STATUS.md`](CALC_STATUS.md) for full shipped vs stub inventory.
