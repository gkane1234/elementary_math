# Calculus shipped vs stub

- Catalog leaves: **68**
- Integrals slice (u-sub presets + reverse-chain): shipped 2026-09-03
- Apps-of-diff / DE-intro stubs: **0 remaining** on `calculus_foundations`
- Phase-01 catalog: all integral / app-int leaves + **named u-sub preset
  showcase** sections (`u_sub_preset_*`, `u_sub_reverse_chain*`)

## Integrals slice

- Named **u-sub form presets** from `u_substitution.json` (OpenStax Vol 1 §5.5–5.7 + BC bank): `power_linear`, `power_quadratic`, `power_cubic`, `du_over_u`, `exp_chain`, `trig_chain`, `arctan_chain`, `ln_power_chain`, `alteration`, `challenging`, `bc_bank`.
- **Reverse chain:** `sample_reverse_chain_integral` — F∘g from Diff `expr_skeleton`, prompt F′, answer F+C.

### Phase-01 showcase sections (forced knobs)

| slug | host type_id | knobs |
|---|---|---|
| `u_sub_preset_power_linear` | `calc_indef_int_power_rule_with_substitution` | `power_linear` / catalog |
| `u_sub_preset_power_quadratic` | same | `power_quadratic` / catalog |
| `u_sub_preset_power_cubic` | same | `power_cubic` / catalog |
| `u_sub_preset_du_over_u` | `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` | `du_over_u` / catalog |
| `u_sub_preset_exp_chain` | same | `exp_chain` / catalog |
| `u_sub_preset_trig_chain` | power u-sub leaf | `trig_chain` / catalog |
| `u_sub_preset_arctan_chain` | `calc_indef_int_inverse_trigonometric_with_substitution` | `arctan_chain` / catalog |
| `u_sub_preset_ln_power_chain` | ln/exp u-sub leaf | `ln_power_chain` / catalog |
| `u_sub_preset_alteration` | power u-sub leaf | `alteration` / catalog |
| `u_sub_preset_challenging` | power u-sub leaf | `challenging` / catalog |
| `u_sub_preset_challenging_ln_exp` | ln/exp u-sub leaf | `challenging` / catalog |
| `u_sub_preset_bc_bank` | power u-sub leaf | `bc_bank` / catalog (Calc BC §1) |
| `u_sub_preset_bc_bank_ln_exp` | ln/exp u-sub leaf | `bc_bank` / catalog |
| `parts_preset_bc_bank` | parts leaf | `parts_form_preset=bc_bank` (Calc BC §2) |
| `pfd_preset_bc_bank` | PFD leaf | `pfd_form_preset=bc_bank` (Calc BC §4) |
| `trig_sub_preset_bc_bank` | trig-sub leaf | `trig_sub_form_preset=bc_bank` (Calc BC §5) |
| `u_sub_reverse_chain` | power u-sub leaf | reverse_chain |
| `u_sub_reverse_chain_ln_exp` | ln/exp u-sub leaf | reverse_chain |
| `u_sub_reverse_chain_invtrig` | invtrig u-sub leaf | reverse_chain + arctan_chain |

## Apps / DE intro (this pass)

Dedicated `calc_app_diff` generators (not `calculus_foundations`):

- `calc_app_diff_relative_extrema`
- `calc_app_diff_absolute_extrema`
- `calc_app_diff_intervals_of_concavity`
- `calc_app_diff_optimization`
- `calc_app_diff_curve_sketching` (checklist; LIMITATIONS no drawing)
- `calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime` (sign of f′; LIMITATIONS no figures)
- `calc_app_diff_motion_along_a_line`
- `calc_app_diff_newtons_method`
- `calc_app_int_motion_along_a_line_revisited`
- `calc_diff_eq_introduction`

## Still thin / LIMITATIONS (not stubs)

- Graphical comparison: no figure bank
- Curve sketching: text checklist only
- Optimization / Newton / DE intro: OpenStax-shaped but not full exercise breadth
- Challenging on the power host stays algebraic (cubic / root-quad / alteration); trig/exp challenging is on the ln/exp host
- Reverse-chain: `x^{1}` elided here; unsimplified juxtaposition (`2x(-4)`) and high-D nested F∘g remain
- Implicit: catalog families only (not a general \(F(x,y)\) AST)
- Logarithmic differentiation: catalog families only (not a general \(u^v\) AST)
- Parts: definite IBP not on the indefinite leaf; \(\int x e^{ax}\sin(bx)\) deferred
- PFD: cube multiplicity and improper (long division) still stubs; \((x^2+1)^2\) / \(1/(x^4+1)\) deferred; high D can still emit single-term quad arctan/ln
- Trig-sub: \(\sqrt{a^2-x^2}/x\) still no closed template; \(x/\sqrt{\,\cdot\,}\) and \(x^3/\sqrt{\,\cdot\,}\) are u-sub (wrong leaf)

## This pass (2026-09-14)

- **`calc_indef_int_integration_by_parts`:** D=0 rotates ln / \(xe^x\) / \(x\sin x\) / \(x\cos x\); mid D scales \(k\); high D tabular n≤3 + \((\ln)^{2,3}\) + cyclic + invtrig. Easy `ln_alone` has `d_max=8`. Named preset `parts_form_preset=bc_bank`.
- **U-sub BC bank §1:** named preset `bc_bank` (negative powers of poly, ln^n/x, e^x/(a+e^x)^n, trig'/(a+trig)^n). D=0 auto stays OpenStax easy. Bank file: `scripts/output/example_mining/challenging_indefinite_integrals_bc.tex`.
- **IBP BC bank §2 lookalikes:** `poly3_exp`, `poly3_sin/cos`, `poly2_cos`, `poly2_ln`, `ln_power_2/3`, `poly1_arctan`, `poly1_arcsin`, `arcsin_alone`, `power_frac_ln`, `ln_quad`. Deferred: `poly_exp_trig`, `poly1_arccos`, `poly2_ln_quad`.
- **PFD BC bank §4:** named preset `pfd_form_preset=bc_bank` on existing distinct-linear / mixed / repeated-square / irred-quad cores. Deferred: `x4_plus_1`, `repeated_quad_square`.
- **Trig-sub BC bank §5:** named preset `trig_sub_form_preset=bc_bank` on existing √ / 1/√ / \(x^2/\sqrt\) / \((\,)^{±3/2}\) cores plus honest siblings \(x^2/\sqrt{x^2\pm a^2}\) and \((x^2-a^2)^{-3/2}\). D=0 auto stays \(\sqrt{a^2-x^2}\). Deferred: \(\sqrt{a^2-x^2}/x\), \(x/\sqrt\), \(x^3/\sqrt\), table arcsin \(1/\sqrt{a^2-x^2}\).
- **`calc_diff_implicit`:** `derivatives.json` form_ids with `d_min`/`d_max`; D=0 circle; mid xy/ellipse; high trig/exp/folium. Cleared UNCLEAR / LOW_VARIETY.
- **`calc_diff_logarithmic`:** catalog-routed `logdiff_*`; D=0 power; mid product/quotient/root; high \(x^x\) / \((x+1)^x\) / \((\sin x)^x\). High D cannot emit `logdiff_power`.
- **`calc_diff_other_base_logarithms_and_exponentials`:** catalog-routed `other_base_*`; D=0 \(a^x\) / \(\log_a x\); mid \(a^{kx}\) / \(\log_a(ax+b)\); high \(a^{x^2}\) / \(x a^x\) / log-power. High D cannot emit leftover \(a^x\).
- **`calc_diff_inverse_functions`:** catalog-routed `invfn_*`; D=0 \(x^n\); mid table/linear; high \(\sin x\) / \(\ln\) / \(x^3+x\). D=22 cannot emit leftover \(e^x\) (`invfn_exp` `d_max=18`).
- **`calc_indef_int_partial_fractions`:** `distinct_linear_2` has `d_max=10`; D=0 two linears; high D 3-linear / mixed / repeated / quad. High D cannot emit two-linear leftovers.
- **U-sub challenging + reverse-chain:** `power_cubic_x2_du` (Checkpoint 5.25/5.26); §5.6 `exp_of_cubic` / `exp_of_quartic` (Checkpoint 5.33) / `exp_root_chain` / `exp_power_of_exp`; `composite_ln_of_trig` (cot/tan); reverse-chain elides `x^{1}`. Showcases `u_sub_preset_power_cubic`, `u_sub_preset_challenging_ln_exp`.
