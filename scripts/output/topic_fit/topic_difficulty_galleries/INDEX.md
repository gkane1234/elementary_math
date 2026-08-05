# Topic difficulty galleries (Calc 1) — conceptual × Spec

Each gallery is a **2D grid**: rows = conceptual difficulty (0 → approx
conceptual max for the full `allow_*` kit), columns = Spec difficulty
(independent; demo ladder, unbounded in intent).

Generated: 2026-08-05 19:09 UTC

| Topic | type_id | Conceptual max | Gallery |
|-------|---------|----------------|---------|
| Limits — direct evaluation | `calc_limits_by_direct_evaluation` | 25 | [gallery.html](direct/gallery.html) |
| Limits — removable discontinuities | `calc_limits_at_removable_discontinuities` | 25 | [gallery.html](removable/gallery.html) |
| Limits — jump discontinuities / kinks | `calc_limits_at_jump_discontinuities_and_kinks` | 25 | [gallery.html](jump/gallery.html) |
| Limits — essential discontinuities | `calc_limits_at_essential_discontinuities` | 25 | [gallery.html](essential/gallery.html) |
| Limits — at infinity | `calc_limits_at_infinity` | 25 | [gallery.html](infinity/gallery.html) |
| Continuity — classify | `calc_continuity_determining_and_classifying` | 25 | [gallery.html](continuity/gallery.html) |
| L'Hôpital's rule | `calc_app_diff_lhopitals_rule` | 25 | [gallery.html](lhopital/gallery.html) |
| Derivatives — power rule | `calc_diff_power_rule` | 25 | [gallery.html](deriv_power/gallery.html) |
| Derivatives — product rule | `calc_diff_product_rule` | 25 | [gallery.html](deriv_product/gallery.html) |
| Derivatives — quotient rule | `calc_diff_quotient_rule` | 25 | [gallery.html](deriv_quotient/gallery.html) |
| Derivatives — chain rule | `calc_diff_chain_rule` | 25 | [gallery.html](deriv_chain/gallery.html) |
| Derivatives — trigonometric | `calc_diff_trigonometric` | 25 | [gallery.html](deriv_trig/gallery.html) |
| Derivatives — ln / exp | `calc_diff_natural_logarithms_and_exponentials` | 25 | [gallery.html](deriv_ln_exp/gallery.html) |
| Derivatives — inverse trig | `calc_diff_inverse_trigonometric` | 25 | [gallery.html](deriv_invtrig/gallery.html) |
| Derivatives — higher order | `calc_diff_higher_order_derivatives` | 25 | [gallery.html](deriv_higher/gallery.html) |
| Derivatives — general | `calc_diff_general` | 25 | [gallery.html](deriv_general/gallery.html) |
| Linear approximations | `calc_app_diff_linear_approximations` | 25 | [gallery.html](linear_approx/gallery.html) |
| Differentials | `calc_app_diff_differentials` | 25 | [gallery.html](differentials/gallery.html) |
| Integrals — power rule | `calc_indef_int_power_rule` | 25 | [gallery.html](int_power/gallery.html) |
| Integrals — trigonometric | `calc_indef_int_trigonometric` | 25 | [gallery.html](int_trig/gallery.html) |
| Integrals — log / exp | `calc_indef_int_logarithmic_rule_and_exponentials` | 25 | [gallery.html](int_log_exp/gallery.html) |
| Integrals — inverse trig | `calc_indef_int_inverse_trigonometric` | 25 | [gallery.html](int_invtrig/gallery.html) |
| Integrals — substitution (power) | `calc_indef_int_power_rule_with_substitution` | 25 | [gallery.html](int_sub/gallery.html) |
| Integrals — log/exp with substitution | `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` | 25 | [gallery.html](int_log_exp_sub/gallery.html) |
| Integrals — trigonometric substitution | `calc_indef_int_trigonometric_with_substitution` | 25 | [gallery.html](int_trig_sub/gallery.html) |
| Integrals — invtrig with substitution | `calc_indef_int_inverse_trigonometric_with_substitution` | 25 | [gallery.html](int_invtrig_sub/gallery.html) |
| Integrals — integration by parts | `calc_indef_int_integration_by_parts` | 25 | [gallery.html](int_parts/gallery.html) |
| Integrals — partial fractions | `calc_indef_int_partial_fractions` | 25 | [gallery.html](int_pfd/gallery.html) |
| Integrals — multi-trick | `calc_indef_int_multi_trick` | 25 | [gallery.html](int_multi/gallery.html) |
| FTC — first | `calc_def_int_first_fundamental_theorem_of_calculus` | 25 | [gallery.html](ftc1/gallery.html) |
| FTC — second | `calc_def_int_second_fundamental_theorem_of_calculus` | 25 | [gallery.html](ftc2/gallery.html) |
| Definite — substitution / change of variables | `calc_def_int_substitution_with_change_of_variables` | 25 | [gallery.html](def_sub/gallery.html) |

## What Spec does **right now**

Independent ``spec_difficulty`` runs the **expression flesher** on a **fixed
conceptual skeleton** (topic form + answer from undressed core):

- ``cancel_quot_bait`` — write body as a canceling quotient
- ``add_cancel_const`` / ``add_cancel_linear`` — add then subtract the same piece
- ``double_neg`` — ``-(-(body))``
- ``exp_ln_id`` / ``ln_exp_id`` — ``e^{\ln(·)}`` / ``\ln(e^{·})`` when allow_exp+allow_log
- ``poly_inflate`` — compose_inflate on parseable pure-poly islands only
- **Answer is taken from the undressed skeleton** (``spec_answer_preserved``)
- Spec does **not** raise poly degree / invent a different harder problem

Shared API: ``expression_flesh.flesh_from_skeleton`` / ``n_dress_layers``.

Conceptual still owns forms, singularity type, allow_*-gated classes, jump
piece counts, L'Hôpital step unlocks, exotic exponents, higher-order derivatives —
and is **clamped** to approx conceptual max for the current checkboxes.

## Honest limitations

- Equivalence is by construction (cancel pairs / identity wraps / poly inflate), not a CAS proof.
- Some leaves restrict cancel-quot and exp/ln wraps (jump, continuity, L'Hôpital, FTC).
- Poly inflate skips non-poly latex (honest shortfall).
- Trig identity wraps are stubbed (``trig_pythag_id``) — not implemented yet.
- High conceptual exotic-power density still depends on pack sampling bias.

## Ideas for later

1. AST-level equivalent rewrites (expand/factor) with a simplify check.
2. Soft “reasonable” Spec band on worksheets (0–16) vs sandbox 32+.
3. Stronger conceptual bias toward ``x^\pi`` / higher-order at high C.
4. Trig Pythagorean / angle-addition identity wraps in the flesher catalog.

Open each `gallery.html` in a browser (local KaTeX under `../_assets/katex`).
