# Challenging Indefinite Integrals (Calc BC bank)

User-supplied drill bank (not OpenStax). Gold as **extra form families / high-D presets** on existing technique leaves. OpenStax shapes stay D=0 / mid-D.

- **LaTeX:** [`challenging_indefinite_integrals_bc.tex`](challenging_indefinite_integrals_bc.tex)
- **Catalogs:** `question_engine/frameworks/primitives/openstax_form_catalogs/`
- **Do not** invent closed forms. Deferred items keep `generation_status: deferred` + `gap_reason`.

## Section → type_id

| § | Bank section | Host `type_id` | Catalog |
|---|--------------|----------------|---------|
| 1 | Substitution and structural tricks | `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`, `calc_indef_int_trigonometric_with_substitution` | `u_substitution.json` preset `bc_bank` |
| 2 | Integration by parts | `calc_indef_int_integration_by_parts` | `integration_by_parts.json` |
| 3 | Trigonometric integrals | `calc_indef_int_trigonometric` | `trig_integrals.json` |
| 4 | Rational functions / PFD | `calc_indef_int_partial_fractions` | `partial_fractions.json` |
| 5 | Algebraic radicals / trig sub | (trig-sub leaf; see `trig_substitution.json`) | `trig_substitution.json` |
| 6 | Mixed / clever | split: PFD / u-sub / long-division | `partial_fractions` + `u_substitution` |
| 7 | Log, invtrig, nested | ln/exp u-sub + parts | `u_substitution` + `integration_by_parts` |
| 8 | Multiple techniques | `calc_indef_int_multi_trick` | pipeline forms |
| 9 | Parameterized families | same hosts as the technique; n as D-scaled exponent | existing form_ids |
| 10 | Final challenge | mix of PFD / Weierstrass / trig | mostly deferred |
| 11 | Hyperbolic | optional; `∫ dx/(1+cosh x)` only | deferred |

Named u-sub preset: `u_sub_form_preset=bc_bank` (gallery slugs `u_sub_preset_bc_bank`, `_ln_exp`, `_trig`).

## §1 inventory (u-sub)

| Bank item | Shape | Status | form_id |
|-----------|-------|--------|---------|
| 1.1 | ∫ x/(x²+1)⁴ | implemented | `power_quad_neg` |
| 1.2 | ∫ 3x²/(x³−5)² | implemented | `power_cubic_neg` |
| 1.3 | ∫ x√(x²+9) | already | `root_quad_x_du` |
| 1.4 | ∫ x/√(4−x²) | implemented | `root_quad_minus` |
| 1.5 | ∫ x/((1+x²)√(1+x²)) | implemented | `power_quad_m3_2` |
| 1.6 | ∫ (ln x)³/x | implemented | `ln_power_over_x` |
| 1.7 | ∫ 1/(x(1+ln x)³) | implemented | `power_of_one_plus_ln` |
| 1.8 | ∫ eˣ/(1+eˣ)² | implemented | `exp_over_power_of_exp` |
| 1.9 | ∫ e^{2x}/(1+eˣ)³ | implemented | `exp_e2x_over_power` |
| 1.10–1.13 | sin/(a+cos)ⁿ, cos/(a+sin)ⁿ, sec²/(a+tan)ⁿ, sec tan/(a+sec)ⁿ | implemented | `trig_over_linear_trig_power` |
| 1.14 | ∫ dx/(x ln x (ln ln x)²) | implemented | `ln_ln_nested` |
| 1.15 | ∫ dx/(x √ln x) | implemented | `ln_over_x_sqrt` |
| 1.16 | ∫ dx/(x(1+ln² x)) | implemented | `arctan_of_ln` |
| 1.17 | ∫ (2x+1)/(x²+x+7) | implemented | `du_over_u_quadratic` |
| 1.18 | ∫ x²/((x³+1) ln(x³+1)) | implemented | `du_over_ln_of_poly` |
| 1.19 | ∫ cos(ln x)/x | implemented | `cos_of_ln_over_x` |
| 1.20 | ∫ sin(√x)/√x | implemented | `sin_of_sqrt` |
| 1.21 | ∫ e^{√x}/√x | implemented | `exp_of_sqrt` |
| 1.22 | ∫ dx/((x+1)√ln(x+1)) | implemented | `root_ln_of_linear` |
| 1.23 | ∫ (ln x)²/(x √(1+(ln x)³)) | implemented | `ln_sq_over_root_ln_cube` |
| 1.24 | ∫ x⁵/(x⁶+1)³ | implemented | `power_hex_neg` |
| 1.25 | ∫ x³/√(1+x⁴) | implemented | `root_of_x4` |

## §2 inventory (parts) — next slice

| Bank | Status | form_id |
|------|--------|---------|
| xeˣ, x²eˣ, x sin/cos, x ln, eˣ sin/cos, arctan | already | `poly1_exp`, `poly2_exp`, `poly1_sin/cos`, `poly1_ln`, `cyclic_*`, `arctan_alone` |
| x³ e^{2x}, x³ cos, x² ln, (ln x)^{2,3} | missing | need `poly3_exp`, `poly3_cos`, `poly2_ln`, `ln_power_parts` |
| x arctan, x arcsin/arccos | stub/missing | `poly1_arcsin` stub; `poly1_arctan` not in catalog |
| x eˣ sin/cos, √x ln, ln(x²+1) | missing | needs extra parts templates |

## §3 inventory (trig) — next slice after u-sub

Already: odd/even sin/cos, tan/sec save-one, sec³, sec⁵, tan⁴, product-to-sum.

**Implemented this pass:** `sin_cos_both_odd` (sin³cos³), `csc_j_cot`, `sin_over_one_plus_cos2` (and cos/(1+sin²)), `one_over_one_plus_cos`, `one_over_one_plus_sin`.

**Deferred:** `csc5_reduction`, `tan4_sec3`, `one_over_a_plus_sin` / Weierstrass (`1/(2+sin)`, `1/(1+sin+cos)`).

## §4–5 / 10 — later

PFD three-linear / mixed / repeated already exist. Missing: `(x²+1)²`, `x⁴+1` factorization, improper long division (`improper_long_division` stub), repeated cube.

Trig-sub √(a²±x²) families already exist. Missing: x³/√(x²±a²) (u-sub actually), `(x²−a²)^{-3/2}`.

§10 `x⁴+1`, `x⁶+1`, 1/(1+tan x): **deferred** (need PFD of x⁴+1 / Weierstrass).
