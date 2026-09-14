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

- Area under a curve: leftover lockout of \(y=x\) shipped; still three frozen monomials on \([0,b]\) (no \(\sin x\) / \(e^x\) / \(a\neq 0\))
- Limit of sums: skipped — live is the FTC area stem (shared `area_under_curve`); no existing \(\lim\sum\) core (finite Riemann is the approximating sibling; tables is the tables sibling)
- Riemann sum tables: leftover lockout of 3-point left shipped; still three frozen old builders (no story tables / \(L_n\) vs \(R_n\) / unequal \(\Delta x\)); D=16 can still emit 4-point leftover
- Area between curves: leftover lockout of exclusive cliffs and of \(y=k-x\) vs \(y=0\) at expert; still five frozen old builders (no Ex. 6.1 two-line / Ex. 6.2 parabola-vs-line / \(dy\)); D=22 is frozen \(y=x\) vs \(y=x^{2}\)
- Volume disks/washers: leftover lockout of disk \(y=x\) shipped (already in `volume_methods`); still three frozen old builders (no Ex. 6.8 \(\sqrt{x}\) / Ex. 6.10 washer \(1/x\) / \(y\)-axis); D=16/22 washer \(y=n\) vs \(y=x\) only
- Volume by cylinders: leftover lockout of exclusive \(y=x\) shipped; still three frozen old builders (no Ex. 6.12 \(1/x\) / Ex. 6.13 \(2x-x^{2}\) / \(x\)-axis shells); D=16 can still emit \(y=x^{2}\) leftover
- Volume known cross sections: leftover lockout of exclusive squares shipped; still three frozen old builders (no Ex. 6.6 pyramid / Ex. 68 circular-base squares / Ex. 69 triangular-base semicircles / Ex. 72 isosceles); D=16 can still emit equilateral leftover

- Motion along a line (diff): leftover lockout + Ex. 3.36/3.35 cubics shipped; still no free-fall \(-16t^{2}\) / piecewise / trig / \(s(t)\) graph
- Motion along a line revisited (integral): leftover lockout of \(v=2t\) shipped; still no \(\int|v|\) distance / Ex. 5.24 nonzero net / quadratic \(v(t)\)
- Graphical comparison: no figure bank
- Instantaneous rates of change: leftover lockout of \(x^{n}\) shipped; still seven frozen old builders (no Ex. 3.34 free-fall / table / graph); D=16 can still emit \(px^{2}+q\) / \(\sqrt{x}\) / \(1/x\) leftover
- Rules using tables: leftover lockout of D=0 \((fg)'\) shipped; still three frozen old builders (text values, no figure-bank table / three-function product); D=16 can still emit quotient leftover
- Average rates of change: leftover lockout of \(x^{2}\) shipped; still seven frozen old builders (no \(\sqrt{x}\) / trig / exp / story \(s(t)\)); D=16 can still emit cubic / \(px^{2}+q\) / linear leftover
- Limits in form of definition of derivative: leftover lockout of D=0 \(x^{2}\) \(x\to a\) / \(h\to 0\) shipped; still eight frozen old builders (no general \(f\) / trig / exp); D=16 can still emit cube / \(k(a+h)^{2}\) / named leftover
- First FTC (evaluate \(\int_a^b\)): leftover lockout of D=0 \(\int x\) / \(\int kx^{2}\) shipped; still five frozen old builders (no Ex. 5.20 \(t^{2}-4\) / Ex. 5.21 \(\frac{x-1}{\sqrt{x}}\) / \(a\neq 0\)); D=16 can still emit quad-const leftover
- Substitution with change of variables: leftover lockout of D=0 linear \(u\) shipped; still three frozen old builders (no Ex. 5.31 \(\sin^2\theta\cos\theta\) / Ex. 5.32 \(e^{\sqrt{x}}/\sqrt{x}\) / reverse limits); D=16 can still emit quad leftover; named EMH presets unused by the definite sampler
- Second FTC (\(\frac{d}{dx}\int_a^{g(x)}\)): leftover lockout of D=0 \(t^{2}\) shipped; still three frozen old builders (no Ex. 5.17 \(1/(t^{3}+1)\) / Ex. 5.18 \(\sqrt{x}\) upper / Ex. 5.19 two limits); D=16 can still emit \(\sin t\) leftover
- Integral MVT (average value): leftover lockout of \(f(x)=x\) shipped; still three frozen monomials on \([0,b]\) (no \(\sin x\) / \(e^x\) / \(a\neq 0\) / find-\(c\)); D=16 can still emit \(x^{2}\) leftover
- Slope, tangent, and normal lines: leftover lockout of D=0 poly/trig/exp/ln shipped; still no implicit/folium / \(x\cdot 5^{x}\) normals; D=16 can still emit reciprocal/radical leftover; generic `function_sketch` only
- Linear approximations: leftover lockout of \(x^{2}\) shipped; still no Ex. 4.5 estimate-\(\sqrt{x}\) / Ex. 4.6 \(\sin x\) / cube-root / \((1+x)^{n}\); D=16 can still emit \(\sqrt{x}\) leftover
- Differentials: leftover lockout of D=0 log/power/trig/exp shipped; still no \(\Delta y\) vs \(dy\) / cube-error / percent-error (Ex. 4.9–4.11); D=16 can still emit radical/reciprocal leftover
- Absolute extrema: leftover lockout + Ex. 4.17 shifted closed-interval shipped; still no fractional-power EVT (Ex. 4.13 \(x^{2}-3x^{2/3}\))
- Relative extrema: leftover lockout + Ex. 4.17 shifted extrema shipped; still no fractional-power first-derivative test
- Curve sketching: leftover lockout + shifted inflections shipped; still text checklist only (no SVG / asymptotes)
- Newton: leftover lockout + two cubic steps shipped; still no Ex. 4.46 \(x^{3}-3x+1\) / failure / two-step quadratic
- DE intro: leftover lockout of \(y=Ce^{kx}\) shipped; still no classify-order / IVP find-\(C\) / trig verify (D=16 and D=22 both Euler-only)
- Slope fields: leftover lockout of \(y'=x\) shipped; still eval-at-a-point only (no direction-field figures / match-the-sketch); three frozen RHSs
- Separable: leftover lockout of \(dy/dx=ax\) shipped; still no OpenStax mixes (\(x/y\), logistic); D=22 is the single frozen \(y/x\), \(y(1)=4\) IVP
- Exponential growth/decay: leftover lockout of story \(y'=ky\) shipped; still no Newton's cooling / logistic / find-\(k\) from data; D=22 is doubling / half-life \(nT\) only
- Optimization: leftover lockout + §4.7 frames shipped; still no travel-time / Norman window / solids-in-solids
- Increase/decrease: leftover lockout + Ex. 4.17 cubics shipped; still no fractional-power first-derivative test
- Concavity: leftover lockout + Ex. 4.19 shifted inflections shipped; still no quintic second-derivative test
- MVT: leftover lockout + Ex. 4.15 \(\sqrt{x}\) shipped; still no velocity story / interior-only \(\sqrt{x}\)
- Rolle's: leftover lockout shipped (high D no even-quad \(c=0\)); still no scaled Checkpoint 4.14 / hypothesis-verify stem
- Power rule (indef): leftover lockout of `poly_sum` / \(\sqrt{x}\) shipped; still six frozen old builders (no Ex. 4.50 \(1/x\) / \(\cos x\) / \(e^{x}\); no Ex. 5.23 \(\sqrt{t}(1+t)\)); D=16 can still emit \(1/\sqrt{x}\) / \(x\sqrt{x}\) leftover
- Challenging on the power host stays algebraic (cubic / root-quad / alteration); trig/exp challenging is on the ln/exp host
- Reverse-chain: `x^{1}` elided here; unsimplified juxtaposition (`2x(-4)`) and high-D nested F∘g remain
- Implicit: catalog families only (not a general \(F(x,y)\) AST)
- Logarithmic differentiation: catalog families only (not a general \(u^v\) AST)
- Parts: definite IBP not on the indefinite leaf; \(\int x e^{ax}\sin(bx)\) deferred
- PFD: cube multiplicity and improper (long division) still stubs; \((x^2+1)^2\) / \(1/(x^4+1)\) deferred; high D can still emit single-term quad arctan/ln
- Trig-sub: \(\sqrt{a^2-x^2}/x\) still no closed template; \(x/\sqrt{\,\cdot\,}\) and \(x^3/\sqrt{\,\cdot\,}\) are u-sub (wrong leaf)

## This pass (2026-09-14)

- **`calc_indef_int_power_rule`:** Leftover lockout of D=0 `poly_sum` / \(\sqrt{x}\). D=0 poly or \(\int\sqrt{x}\) (old easy); D=8 leftover easy + \(1/\sqrt{x}\) / \(x\sqrt{x}\) / \(k/x^n\) / rewrite; D=16 mid leftover + rewrite/neg-power (no `poly_sum` / \(\sqrt{x}\)); D=22 rewrite / neg-power only. Stamps `form_id` + `generator=integral_power_rule`; `select_form_id` / `live_quality_form_weights`. Shared generator also leftover-locks `pc_indefinite_integrals`. Did not invent Ex. 4.50 trig/exp / Ex. 5.23 \(\sqrt{t}(1+t)\) cores.
- **`calc_def_int_substitution_with_change_of_variables`:** Leftover lockout of D=0 linear \(u\). D=0 \(\int_0^b p(px+q)^n\) (old easy); D=8 leftover linear + quad \(2x(x^{2}+1)^n\); D=16 quad leftover + \(du/u\) (no linear); D=22 \(du/u\) only. Stamps `form_id` + `generator=integral_definite_substitution`; `select_form_id` / `live_quality_form_weights`. Did not invent Ex. 5.31 trig / Ex. 5.32 exp / reverse-limit cores.
- **`calc_diff_rules_using_tables`:** Leftover lockout of D=0 \((fg)'\). D=0 product from four tabulated values (old easy); D=8 leftover product + quotient; D=16 quotient leftover + compose (no product); D=22 compose only. Stamps `form_id` + `generator=derivative_from_tables`; `select_form_id` / `live_quality_form_weights`. Text tables only. Did not invent a figure-bank table / three-function core.
- **`calc_diff_instantaneous_rates_of_change`:** Leftover lockout of D=0 \(x^{n}\). D=0 monomial \(x^{n}\) at a point (old easy); D=8 leftover power + \(px^{2}+q\) / \(\sqrt{x}\) / \(1/x\); D=16 medium leftover + cubic / trig / exp (no \(x^{n}\) leftover); D=22 cubic / trig / exp only. Stamps `form_id` + `generator=instantaneous_rate_of_change`; `select_form_id` / `live_quality_form_weights`. Shared generator also leftover-locks `pc_instantaneous_rates_of_change`. Did not invent free-fall / table / graph cores.
- **`calc_diff_average_rates_of_change`:** Leftover lockout of D=0 \(x^{2}\). D=0 \(f(x)=x^{2}\) on \([a,b]\) (old easy); D=8 leftover quad + cubic / \(px^{2}+q\) / linear; D=16 medium leftover + poly / \(x^{3}+x\) / \(1/x\) (no \(x^{2}\) leftover); D=22 poly / shifted / reciprocal only. Stamps `form_id` + `generator=average_rate_of_change`; `select_form_id` / `live_quality_form_weights`. Shared generator also leftover-locks `pc_average_rates_of_change`. Did not invent \(\sqrt{x}\) / trig / story cores.
- **`calc_app_diff_limits_in_form_of_definition_of_derivative`:** Leftover lockout of D=0 \(x^{2}\) limits. D=0 \(\lim_{x\to a}\) / \(\lim_{h\to 0}\) of \(x^{2}\) (old easy); D=8 leftover easy + cube / \(k(a+h)^{2}\) / named; D=16 medium leftover + reciprocal / \(\sqrt{\,\cdot\,}\) / named-poly (no \(x^{2}\) leftover); D=22 reciprocal / sqrt / named-poly only. Stamps `form_id` + `generator=definition_of_derivative`; `select_form_id` / `live_quality_form_weights`. Shared generator also leftover-locks `calc_diff_definition_of_the_derivative` / `pc_definition_of_the_derivative`. Did not invent a general \(f\) core.
- **`calc_app_int_volume_of_solids_with_known_cross_sections`:** Leftover lockout of exclusive cliffs / D=0 square. D=0 square of side \(x\) on \([0,n]\) (old easy); D=8 leftover square + equilateral; D=16 equilateral leftover + semicircle (no square); D=22 semicircle only. Stamps `form_id` + `generator=volume_cross_sections`; `select_form_id` / `live_quality_form_weights`. Did not invent pyramid / circular-base / triangular-base / isosceles cores.
- **`calc_app_int_volume_by_cylinders`:** Leftover lockout of exclusive cliffs / D=0 \(y=x\). D=0 shell \(y=x\) on \([0,n]\) (old easy); D=8 leftover linear + shell \(y=x^{2}\); D=16 \(x^{2}\) leftover + \(y=n-x\) (no \(y=x\)); D=22 \(y=n-x\) only. Stamps `form_id` + `generator=volume_shell`; `select_form_id` / `live_quality_form_weights`. Did not invent \(1/x\) / \(2x-x^{2}\) / \(x\)-axis cores.
- **`calc_app_int_volume_by_slicing_disks_and_washers`:** Leftover lockout of disk \(y=x\) (already dropped at high D in `volume_methods`; now stamps `form_id` + `generator=volume_disk_washer`). D=0 disk \(y=x\) on \([0,n]\) (old easy); D=8 leftover disk linear + disk \(y=x^{2}\); D=16/22 washer \(y=n\) vs \(y=x\) only (no disk leftover). `select_form_id` / `live_quality_form_weights`. Did not invent \(\sqrt{x}\) / \(1/x\) / \(y\)-axis cores.
- **`calc_def_int_riemann_sum_tables`:** Leftover lockout of D=0 3-point left. D=0 \(f(0),f(1),f(2)\) left on \([0,2]\) (old easy); D=8 leftover 3-point + 4-point L/R; D=16 4-point leftover + midpoint (no 3-point left); D=22 midpoint only. Stamps `form_id` + `generator=riemann_sum_tables`; `select_form_id` / `live_quality_form_weights`.
- **`calc_def_int_area_under_a_curve_by_limit_of_sums`:** Skip. Live `_generate_for_type` is the FTC sibling stem (`Find the area under \(y=\ldots\)`). Existing Riemann cores are finite-\(n\) (`riemann_approximate_area`) or tables (`riemann_sum_tables`), not OpenStax Ex. 5.7 definition. Did not invent a \(\lim\sum\) core. Shared leftover lockout of \(y=x\) already on `area_under_curve`. Flags `UNCLEAR` / `LIMITATIONS` / `NOT_IMPLEMENTED`.
- **`calc_def_int_second_fundamental_theorem_of_calculus`:** Leftover lockout of D=0 \(t^{2}\). D=0 \(\frac{d}{dx}\int_a^{x} t^{2}\) (old easy); D=8 leftover poly + \(\sin t\); D=16 \(\sin t\) leftover + chain \(g(x)=kx\) (no \(t^{2}\)); D=22 chain only. Stamps `form_id` + `generator=second_fundamental_theorem`; `select_form_id` / `live_quality_form_weights`.
- **`calc_def_int_first_fundamental_theorem_of_calculus`:** Leftover lockout of D=0 \(\int x\) / \(\int kx^{2}\). D=0 linear+quad (old easy); D=8 leftover linear/quad + \(px^{2}+q\); D=16 quad-const leftover + \(\sqrt{x}\) / \(\sin x\) (no \(\int x\)); D=22 \(\sqrt{x}\) / \(\sin x\) only. Stamps `form_id` + `generator=first_fundamental_theorem`; `select_form_id` / `live_quality_form_weights`.
- **`calc_def_int_mean_value_theorem`:** Leftover lockout of D=0 \(f(x)=x\). D=0 linear on \([0,b]\) (old easy); D=8 leftover linear + \(f(x)=x^{2}\); D=16 \(x^{2}\) leftover + \(kx^{2}\) (no \(f(x)=x\)); D=22 \(kx^{2}\) only. Stamps `form_id` + `generator=def_int_mean_value`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_int_area_between_curves`:** Leftover lockout of exclusive cliffs and of D=0 triangle \(y=k-x\) vs \(y=0\) at expert. D=0 \(y=x\) vs \(y=0\) (old easy); D=8 leftover axis-triangles + \(x^{2}\) vs \(0\) + three-line region (no two-curve yet); D=16 \(x^{2}\) leftover + three-line leftover + \(y=x\) vs \(y=x^{2}\) (no axis-triangles); D=22 two-curve only. Stamps `form_id` + `generator=area_between_curves`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_int_area_under_a_curve`:** Leftover lockout of D=0 \(y=x\). D=0 linear on \([0,b]\) (old easy); D=8 leftover linear + \(y=x^{2}\); D=16 \(x^{2}\) leftover + \(kx^{2}\) (no \(y=x\)); D=22 \(kx^{2}\) only. Stamps `form_id` + `generator=area_under_curve`; `select_form_id` / `live_quality_form_weights`. Shared generator also served the skipped limit-of-sums sibling (still FTC wording).
- **`calc_app_diff_slope_tangent_and_normal_lines`:** Leftover lockout of D=0 poly/trig/exp/ln. D=0 easy mix (old easy, always tangent); D=8 leftover easy + \(1/x\) + radical (normals begin); D=16 reciprocal/radical leftover + cubic / nested (no poly/trig/exp/ln); D=22 cubic / \((x+p)/(x+q)\) / \(\sin(kx)\) only. Stamps `form_id` + `generator=tangent_normal_line`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_diff_linear_approximations`:** Leftover lockout of D=0 \(x^{2}\) (formula + estimate). D=0 \(\sqrt{x}\) / \(x^{2}\) (old easy); D=8 leftover easy + estimate-\(x^{2}\) + \(1/x\) + \(e^{x}\); D=16 \(\sqrt{x}\) leftover + \(1/x\) + \(e^{x}\) (no \(x^{2}\)); D=22 \(1/x\) and \(e^{x}\) only. Stamps `form_id` + `generator=linear_approximation`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_diff_differentials`:** Leftover lockout of D=0 log/power/trig/exp. D=0 easy mix (old easy); D=8 leftover easy + radical/reciprocal; D=16 radical/reciprocal leftover + nested (no log/power); D=22 nested only (product / quotient / \(e^{x^{2}}\) / eval \(dx\)). Stamps `form_id` + `generator=differentials`; `select_form_id` / `live_quality_form_weights`.
- **`calc_diff_eq_exponential_growth_and_decay`:** Leftover lockout of story \(y'=ky\). D=0 growth story find \(y(t)\) (old easy); D=8 growth leftover + decay story + IVP; D=16 decay/IVP leftover + doubling/half-life (no growth); D=22 doubling/half-life only. Stamps `form_id` + `generator=calc_continuous_growth_decay`; `select_form_id` / `live_quality_form_weights`.
- **`calc_diff_eq_slope_fields`:** Leftover lockout of \(y'=x\). D=0 eval \(y'=x\) at a lattice point (old easy); D=8 \(y'=x\) leftover + \(y'=x+y\); D=16 \(y'=x+y\) leftover + \(y'=xy\) (no \(y'=x\)); D=22 \(y'=xy\) only. Stamps `form_id` + `generator=slope_field_interpret`; `select_form_id` / `live_quality_form_weights`. No slope-field figures.
- **`calc_diff_eq_separable`:** Leftover lockout of poly \(dy/dx=ax\). D=0 poly IVP (old easy); D=8 poly leftover + exp \(dy/dx=ky\); D=16 exp leftover + homogeneous \(y/x\) (no poly); D=22 homogeneous only. Stamps `form_id` + `generator=separable_diff_eq`; `select_form_id` / `live_quality_form_weights`.
- **`calc_diff_eq_introduction`:** Leftover lockout of exponential verify \(y=Ce^{kx}\). D=0 exp verify (old easy); D=8 exp leftover + Euler \(y=Cx^{n}\); D=16/22 Euler only (no third old form). Stamps `form_id` + `generator=de_introduction`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_int_motion_along_a_line_revisited`:** Leftover lockout of linear \(v=2t\). D=0 linear displacement (old easy); D=8 linear leftover + const \(v=b\); D=16 const leftover + sign-change (no linear); D=22 sign-change only (net 0). Stamps `form_id` + `generator=motion_along_a_line_integral`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_diff_newtons_method`:** Leftover lockout of one-quad \(x^{2}-a\). D=0 one Newton step on \(x^{2}-a\) (old easy); D=8 one-quad leftover + one cubic step; D=16 one-cubic leftover + two cubic steps (no quad); D=22 two cubic steps only. Stamps `form_id` + `generator=newtons_method`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_diff_motion_along_a_line`:** Leftover lockout + Ex. 3.36/3.35 cubics. D=0 \(s=t^{2}-nt\) eval \(v(n)\) (old easy); D=8 eval leftover + quadratic rest; D=16 rest leftover + cubic rest (no eval-velocity); D=22 cubics only (no \(t^{2}-nt\)). Drops inverted old `Find a(t)` (always 2). Stamps `form_id` + `generator=motion_along_a_line`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_diff_relative_extrema`:** Leftover lockout + Ex. 4.17 shifted extrema. D=0 parabola vertex (old easy); D=8 parabola leftover + odd cubic (crits ±a); D=16 odd-cubic leftover + shifted (no parabola); D=22 shifted only. Stamps `form_id` + `generator=relative_extrema`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_diff_absolute_extrema`:** Leftover lockout + Ex. 4.17 shifted cubics on a closed interval. D=0 parabola on \([0,b]\) (old easy); D=8 parabola leftover + odd cubic (crits ±a); D=16 odd-cubic leftover + shifted (no parabola); D=22 shifted only (endpoint pad so EVT is not interior-only). Stamps `form_id` + `generator=absolute_extrema`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_diff_optimization`:** OpenStax §4.7 frames + leftover lockout. D=0 rectangle/pen; D=8 garden/river leftover; D=16 box/revenue (no four-sided leftover); D=22 inscribed ellipse/circle, closed cylinder, 24×36 box (no garden leftover). Stamps `form_id` + `generator=optimization_applied`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_diff_intervals_of_increase_and_decrease`:** Reuses extrema cubics. D=0 parabola (old easy); D=8 parabola leftover + odd cubic; D=16 shifted Ex. 4.17 cubics (no parabola); D=22 shifted only. Stamps `form_id` + `generator=intervals_increase_decrease`.
- **`calc_app_diff_intervals_of_concavity`:** Leftover lockout + Ex. 4.19 shifted inflections. D=0 odd-power ray; D=8 ray leftover + odd cubic (inflect at 0); D=16 shifted \(h\neq 0\) (no ray); D=22 shifted only. Stamps `form_id` + `generator=intervals_concavity`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_diff_mean_value_theorem`:** Leftover lockout + Ex. 4.15 \(\sqrt{x}\). D=0 \(x^{2}\); D=8 quad leftover + \(kx^{3}\); D=16 \(\sqrt{x}\) (no quad); D=22 \(\sqrt{x}\) only. Stamps `form_id` + `generator=mean_value_theorem`.
- **`calc_app_diff_rolles_theorem`:** Leftover lockout of even-quad \(c=0\). D=0 \(x^{2}-n^{2}\) on \([-n,n]\); D=8 even-quad leftover + two-root (Ex. 4.14 first); D=16 odd cubic \(x^{3}-n^{2}x\) (no even-quad); D=22 cubic only. Stamps `form_id` + `generator=rolles_theorem`; `select_form_id` / `live_quality_form_weights`.
- **`calc_app_diff_curve_sketching`:** Leftover lockout + shifted inflections on the `_cubic_odd` checklist. D=0 parabola; D=8 parabola leftover + odd cubic (inflect at 0); D=16 shifted \(h\neq 0\) (no parabola); D=22 shifted only. Stamps `form_id` + `generator=curve_sketching`.
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
