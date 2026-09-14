"""Write Calculus limits/diff notes (steps 1–3) from live samples JSON."""
from __future__ import annotations

import json
from pathlib import Path

NOTES = Path(__file__).resolve().parent
SAMPLES = json.loads((NOTES / "_calc_limits_diff_samples.json").read_text(encoding="utf-8"))

# (type_id, title, generator, course_cat, skill, d0, high_d, must_not, openstax_rows, variety, engine, flags)
# openstax_rows: list of (cite, url, shape)
# flags: list of flag strings to put near top if any

META: dict[str, dict] = {
    "calc_limits_by_direct_evaluation": {
        "title": "By direct evaluation",
        "generator": "limit_direct_evaluation",
        "category": "Calculus — Limits",
        "skill": "Evaluate a two-sided limit at a finite point by plugging in (poly / rational / specials).",
        "d0": "Polynomial plug-in, e.g. lim_{x→a}(ax²+bx+c).",
        "high_d": "Richer direct plug-ins (rational with nonzero den, roots/trig/exp/log when unlocked) — still direct, not removable/indet.",
        "must_not": "0/0 cancel, jump piecewise, ∞, L'Hôpital — those are other leaves.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §2.3 The Limit Laws",
                "https://openstax.org/books/calculus-volume-1/pages/2-3-the-limit-laws",
                "direct plug-in poly / rational / trig / exp",
            ),
            (
                "OpenStax Calculus Volume 1 §2.2 The Limit of a Function",
                "https://openstax.org/books/calculus-volume-1/pages/2-2-the-limit-of-a-function",
                "limit-at-a-point language",
            ),
        ],
        "local": "scripts/output/example_mining/calculus-volume-1/stage1/2-3-the-limit-laws.md; form catalog limits.json",
        "variety": "Live LimitSpec packs (`limit_direct`). form_id at D≥8 often stamped `direct_sqrt` while latex is still rational plug-in — metadata mismatch; shapes themselves escalate coefs ok. No Diff skeleton.",
        "engine": "**Reuse:** `question_engine/frameworks/primitives/limits.py` LimitSpec + form catalog `limits.json` (`poly_direct`, `rational_direct`, …). **Not** `expr_skeleton` Diff. Optional future: dedicated limit-skeleton patterns if pack variety stalls.",
        "flags": [],
        "opt_out": "none found (LimitSpec / form catalog is the live default; no `use_sample_*` opt-out)",
    },
    "calc_limits_at_jump_discontinuities_and_kinks": {
        "title": "At jump discontinuities and kinks",
        "generator": "limit_jump",
        "category": "Calculus — Limits",
        "skill": "Decide whether a two-sided limit exists for a piecewise jump (one-sided values disagree) — OpenStax one-sided / jump story.",
        "d0": "Constant-vs-constant piecewise at the kink; answer DNE.",
        "high_d": "Linear/poly pieces meeting with unequal one-sided limits; optionally ask one-sided lim x→a± explicitly.",
        "must_not": "Removable holes, essential 1/x oscillation, infinity limits.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §2.2 The Limit of a Function",
                "https://openstax.org/books/calculus-volume-1/pages/2-2-the-limit-of-a-function",
                "one-sided limits; jump where lim− ≠ lim+",
            ),
            (
                "OpenStax Calculus Volume 1 §2.4 Continuity",
                "https://openstax.org/books/calculus-volume-1/pages/2-4-continuity",
                "piecewise jump / kink continuity",
            ),
        ],
        "local": "scripts/output/example_mining/calculus-volume-1/stage1/2-2-the-limit-of-a-function.md; 2-4-continuity.md",
        "variety": (
            "LOW_VARIETY — all sampled D show constant piecewise cases even when form_id claims "
            "`piecewise_jump_linear` / `piecewise_jump_poly`. Rarely asks explicit one-sided lim. "
            "Gold: OpenStax piecewise linear/poly with lim− ≠ lim+ and occasional one-sided prompts."
        ),
        "engine": "**Reuse:** LimitSpec `limit_jump` pack. Flesh linear/poly pieces to match form_ids; optionally emit one-sided prompts. No Diff skeleton.",
        "flags": ["LOW_VARIETY", "UNCLEAR"],
        "opt_out": "none found (LimitSpec default)",
    },
    "calc_limits_at_removable_discontinuities": {
        "title": "At removable discontinuities",
        "generator": "limit_removable",
        "category": "Calculus — Limits",
        "skill": "Evaluate 0/0 limits by canceling a common factor (or rationalizing) at a hole.",
        "d0": "Difference of squares cancel: (x²−a²)/(x−a).",
        "high_d": "Shared quadratic factor; rationalize √x−√a over x−a.",
        "must_not": "Direct plug-in with nonzero den; L'Hôpital as first method on this leaf.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §2.3 The Limit Laws",
                "https://openstax.org/books/calculus-volume-1/pages/2-3-the-limit-laws",
                "algebraic cancel / factor for 0/0",
            ),
            (
                "OpenStax Calculus Volume 1 §2.4 Continuity",
                "https://openstax.org/books/calculus-volume-1/pages/2-4-continuity",
                "removable discontinuity / redefine at hole",
            ),
        ],
        "local": "scripts/output/example_mining/calculus-volume-1/stage1/2-3-the-limit-laws.md; limits.json removable_*",
        "variety": "Good D ladder (diff sq → quad shared → rationalize). D=16 and 22 same seed shape — acceptable. LimitSpec, not Diff.",
        "engine": "**Reuse:** LimitSpec `limit_removable`. Keep factor_cancel / rationalize strategies.",
        "flags": [],
        "opt_out": "none found (LimitSpec default)",
    },
    "calc_limits_at_essential_discontinuities": {
        "title": "At essential discontinuities",
        "generator": "limit_essential",
        "category": "Calculus — Limits",
        "skill": "Recognize limits that DNE at vertical asymptotes / wild oscillation (essential).",
        "d0": "lim_{x→0} 1/x → DNE.",
        "high_d": "1/x², sin(1/x), cos(1/x), tan asymptotes — still DNE or ±∞ per OpenStax.",
        "must_not": "Removable cancel that exists; ordinary rational plug-in.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §2.2 The Limit of a Function",
                "https://openstax.org/books/calculus-volume-1/pages/2-2-the-limit-of-a-function",
                "infinite / oscillating behavior near asymptotes",
            ),
            (
                "OpenStax Calculus Volume 1 §2.4 Continuity",
                "https://openstax.org/books/calculus-volume-1/pages/2-4-continuity",
                "essential discontinuity classification",
            ),
        ],
        "local": "scripts/output/example_mining/calculus-volume-1/stage1/2-4-continuity.md; limits.json essential_*",
        "variety": (
            "LOW_VARIETY / UNCLEAR — form_id advances to `essential_cos_1_over_x` but live latex stays "
            "`1/x` at every D. Catalog lists sin/cos(1/x), 1/x², tan asymptote — flesh those."
        ),
        "engine": "**Reuse:** LimitSpec `limit_essential` — implement missing fleshers for catalog forms. No Diff skeleton.",
        "flags": ["LOW_VARIETY", "UNCLEAR"],
        "opt_out": "none found (LimitSpec default)",
    },
    "calc_limits_at_infinity": {
        "title": "At infinity",
        "generator": "limit_at_infinity",
        "category": "Calculus — Limits",
        "skill": "Evaluate lim_{x→±∞} (end behavior / compare degrees / growth rates).",
        "d0": "Rational same-degree → horizontal asymptote ratio of leading coefs.",
        "high_d": "exp vs poly, ln/poly, arctan, trig/x — OpenStax §4.6 ladder.",
        "must_not": "Finite-a removable / jump; L'Hôpital leaf owns indeterminate ∞/∞ when teaching the rule.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §4.6 Limits at Infinity and Asymptotes",
                "https://openstax.org/books/calculus-volume-1/pages/4-6-limits-at-infinity-and-asymptotes",
                "rational end behavior; exp/ln growth",
            ),
        ],
        "local": "scripts/output/example_mining/calculus-volume-1/stage1/4-6-limits-at-infinity-and-asymptotes.md",
        "variety": (
            "LOW_VARIETY — D=0 rational good; D≥8 always `e^x/x²→∞` for seed 101. Rotate "
            "`inf_ln_over_poly`, `inf_arctan`, equal/unequal degree rationals."
        ),
        "engine": "**Reuse:** LimitSpec `limit_at_infinity`. Broaden form rotation at mid/high D.",
        "flags": ["LOW_VARIETY"],
        "opt_out": "none found (LimitSpec default)",
    },
    "calc_continuity_determining_and_classifying": {
        "title": "Determining and classifying",
        "generator": "limit_continuity",
        "category": "Calculus — Continuity",
        "skill": "Classify continuity at a point (continuous / removable / jump / essential).",
        "d0": "Removable hole from canceled factor: classify removable discontinuity.",
        "high_d": "Mix jump piecewise, essential VA, continuous polys, removable — several OpenStax cases.",
        "must_not": "Only evaluate a numeric limit without classifying.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §2.4 Continuity",
                "https://openstax.org/books/calculus-volume-1/pages/2-4-continuity",
                "types of discontinuity; continuity checklist",
            ),
        ],
        "local": "scripts/output/example_mining/calculus-volume-1/stage1/2-4-continuity.md; limits.json continuity_classify",
        "variety": (
            "LOW_VARIETY / UNCLEAR — identical removable classify prompt at D=0/8/16/22. Need jump / "
            "essential / continuous-at-point varieties."
        ),
        "engine": "**Reuse:** LimitSpec `limit_continuity`. Expand case sampler. Related to limit leaves, not Diff.",
        "flags": ["LOW_VARIETY", "UNCLEAR"],
        "opt_out": "none found (LimitSpec default)",
    },
    "calc_app_diff_lhopitals_rule": {
        "title": "L'Hôpital's Rule",
        "generator": "lhopitals_rule",
        "category": "Calculus — Applications of Differentiation",
        "skill": "Evaluate indeterminate limits (0/0, ∞/∞, …) via L'Hôpital when appropriate.",
        "d0": "Simple 0/0 like (e^{kx}−1)/x or sin(kx)/x.",
        "high_d": "∞/∞ rationals, multipass, exp/poly, 0·∞ / 1^∞ after rewrite — OpenStax §4.8.",
        "must_not": "Direct plug-in that is already determinate; dump non-indet cancel as if L'Hôpital were required.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §4.8 L'Hôpital's Rule",
                "https://openstax.org/books/calculus-volume-1/pages/4-8-lhopitals-rule",
                "0/0 and ∞/∞; other forms after algebra",
            ),
        ],
        "local": "scripts/output/example_mining/calculus-volume-1/stage1/4-8-lhopitals-rule.md; limits.json lhopital_*",
        "variety": (
            "UNCLEAR — form_id labels often disagree with latex (`lhopital_0_inf_product` on sin(5x)/x; "
            "`lhopital_0_inf_power` on (x²−16)/(x−4)). Shapes are mostly 0/0 or ∞/∞ rational; variety thin vs §4.8."
        ),
        "engine": "**Reuse:** LimitSpec `limit_lhopital` / generator `lhopitals_rule`. Fix form→flesh map; keep as limit pack (not Diff skeleton).",
        "flags": ["UNCLEAR", "LOW_VARIETY"],
        "opt_out": "none found (LimitSpec default)",
    },
    "calc_diff_power_rule": {
        "title": "Power Rule",
        "generator": "derivative_power_rule",
        "category": "Calculus — Differentiation",
        "skill": "Differentiate polynomial / power / root expressions with the power rule (and sum).",
        "d0": "Single monomial c x^n, e.g. d/dx(2x²).",
        "high_d": "Fractional/negative powers, multi-term polys; stay first derivative on this leaf.",
        "must_not": "Product/quotient/trig as primary skill; second derivative belongs on higher-order leaf.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §3.3 Differentiation Rules",
                "https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules",
                "power / sum / constant multiple",
            ),
        ],
        "local": "scripts/output/example_mining/calculus-volume-1/stage1/3-3-differentiation-rules.md; diff_skeleton_gallery/power_rule/",
        "variety": (
            "UNCLEAR at high D — D=22 emitted d²/dx² of a poly while form_id stayed `power_root`. "
            "Gold: first-derivative power/roots only; higher order → `calc_diff_higher_order_derivatives`."
        ),
        "engine": "**Reuse:** `expr_skeleton` Diff patterns `Diff(Pow(H,n))` / roots / neg via OpenStax forms `power_*`. Covered in `scripts/output/diff_skeleton_gallery/`. No separate opt-out flag — skeleton is default when form maps.",
        "flags": ["UNCLEAR"],
        "opt_out": "none — Diff/`expr_skeleton` is default when catalog form has FORM_PATTERNS entry",
    },
    "calc_diff_product_rule": {
        "title": "Product Rule",
        "generator": "derivative_product_rule",
        "category": "Calculus — Differentiation",
        "skill": "Differentiate a product uv with the product rule (algebraic factors by default).",
        "d0": "Simple product of monomials/linears, e.g. x·(2x).",
        "high_d": "Higher-degree factors; optional chain on a powered factor (still product-primary).",
        "must_not": "Pure chain without a product; quotient leaf shapes.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §3.3 Differentiation Rules",
                "https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules",
                "product rule (f g)'",
            ),
        ],
        "local": "diff_skeleton_gallery/product_rule/; derivatives.json product_*",
        "variety": "Good ladder: monomial product → poly×linear → poly×(poly)^n. Default algebraic (trig off).",
        "engine": "**Reuse:** `expr_skeleton` `Diff(Prod(F,G))` (independent inners). Gallery: `diff_skeleton_gallery/product_rule/`.",
        "flags": [],
        "opt_out": "none — expr_skeleton default",
    },
    "calc_diff_quotient_rule": {
        "title": "Quotient Rule",
        "generator": "derivative_quotient_rule",
        "category": "Calculus — Differentiation",
        "skill": "Differentiate a quotient f/g with the quotient rule.",
        "d0": "Simple poly/poly, e.g. x/(2x).",
        "high_d": "Higher-degree num/den; chain on powered pieces; keep algebraic unless checkboxes allow specials.",
        "must_not": "Product-only; trig/log quotients unless allow_* enabled.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §3.3 Differentiation Rules",
                "https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules",
                "quotient rule (f/g)'",
            ),
        ],
        "local": "diff_skeleton_gallery/quotient_rule/; derivatives.json quotient_*",
        "variety": (
            "UNCLEAR metadata — D≥8 form_id/`skeleton_pattern` say exp/log quotient while latex stays algebraic "
            "poly quotients. Student-facing shapes escalate ok; stamp form_id to match flesh."
        ),
        "engine": "**Reuse:** `expr_skeleton` `Diff(Quot(F,G))`. Gallery: `diff_skeleton_gallery/quotient_rule/`.",
        "flags": ["UNCLEAR"],
        "opt_out": "none — expr_skeleton default",
    },
    "calc_diff_chain_rule": {
        "title": "Chain Rule",
        "generator": "derivative_chain_rule",
        "category": "Calculus — Differentiation",
        "skill": "Differentiate compositions with the chain rule (powered inners / nested).",
        "d0": "(affine)^n, e.g. (2x)².",
        "high_d": "Poly inner raised to power; nested compositions; stay first derivative unless higher-order leaf.",
        "must_not": "Bare product without composition; second derivative bleed at D=22.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §3.6 The Chain Rule",
                "https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule",
                "outer·inner'; nested chain",
            ),
        ],
        "local": "diff_skeleton_gallery/chain_rule/; 3-6-the-chain-rule.md",
        "variety": (
            "UNCLEAR — D=22 emitted d²/dx² while form was `chain_nested`. Prefer deeper nest / richer poly "
            "inners as first derivatives for this leaf."
        ),
        "engine": "**Reuse:** `expr_skeleton` `Diff(Pow(H,n))` chain-linear + `Diff(Apply(fn,u))` nested. Gallery: `diff_skeleton_gallery/chain_rule/`.",
        "flags": ["UNCLEAR"],
        "opt_out": "none — expr_skeleton default",
    },
    "calc_diff_trigonometric": {
        "title": "Trigonometric",
        "generator": "derivative_trigonometric",
        "category": "Calculus — Differentiation",
        "skill": "Differentiate trig functions (with chain / product-of-trig as D rises).",
        "d0": "Basic trig of affine, e.g. tan(3x+3).",
        "high_d": "Powered trig of poly; product of trig compositions; first derivative preferred.",
        "must_not": "Invtrig-only; second derivative as the main D=22 unlock.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §3.5 Derivatives of Trigonometric Functions",
                "https://openstax.org/books/calculus-volume-1/pages/3-5-derivatives-of-trigonometric-functions",
                "sin/cos/tan/… + chain",
            ),
            (
                "OpenStax Calculus Volume 1 §3.6 The Chain Rule",
                "https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule",
                "trig compositions",
            ),
        ],
        "local": "diff_skeleton_gallery/trigonometric/; 3-5-….md",
        "variety": "Good mid/high trig variety. UNCLEAR: D=22 second derivative of cos·cos — prefer nest richness on first deriv.",
        "engine": "**Reuse:** `expr_skeleton` `Diff(Apply(fn,u))` + `Diff(Prod(F,G)(u))` trig×trig. Gallery: `diff_skeleton_gallery/trigonometric/`.",
        "flags": ["UNCLEAR"],
        "opt_out": "none — expr_skeleton default",
    },
    "calc_diff_inverse_trigonometric": {
        "title": "Inverse trigonometric",
        "generator": "derivative_inverse_trig",
        "category": "Calculus — Differentiation",
        "skill": "Differentiate arcsin/arctan/… of an inner.",
        "d0": "arctan(affine).",
        "high_d": "arctan(poly); nested invtrig; first derivative preferred.",
        "must_not": "Plain trig without inv; second-deriv-only unlock.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §3.7 Derivatives of Inverse Functions",
                "https://openstax.org/books/calculus-volume-1/pages/3-7-derivatives-of-inverse-functions",
                "arcsin/arctan formulas + chain",
            ),
        ],
        "local": "diff_skeleton_gallery/inverse_trig/; 3-7-….md",
        "variety": "Good D=0→16. UNCLEAR: D=22 second derivative — keep on higher-order or deepen nest.",
        "engine": "**Reuse:** `expr_skeleton` `Diff(Apply(arctan,u))` / invtrig chained. Gallery: `diff_skeleton_gallery/inverse_trig/`.",
        "flags": ["UNCLEAR"],
        "opt_out": "none — expr_skeleton default",
    },
    "calc_diff_natural_logarithms_and_exponentials": {
        "title": "Natural logarithms and exponentials",
        "generator": "derivative_ln_exp",
        "category": "Calculus — Differentiation",
        "skill": "Differentiate e^{u} and ln(u) (and products/quotients of them when allowed).",
        "d0": "e^{affine}.",
        "high_d": "ln of poly / nested ln; ln·exp product; optional quotient of ln/poly.",
        "must_not": "Other-base logs (separate leaf); pure algebraic power without exp/ln.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §3.9 Derivatives of Exponential and Logarithmic Functions",
                "https://openstax.org/books/calculus-volume-1/pages/3-9-derivatives-of-exponential-and-logarithmic-functions",
                "e^u, ln u, products",
            ),
        ],
        "local": "diff_skeleton_gallery/ln_exp/; 3-9-….md",
        "variety": "D=0 exp_basic good; mid mixes quotient_log_poly. UNCLEAR: D=22 second deriv of ln(affine).",
        "engine": "**Reuse:** `expr_skeleton` `Diff(Apply(exp,u))` / `Diff(Apply(ln,u))` / `Diff(Prod(F,G)(u))` ln×exp. Gallery: `diff_skeleton_gallery/ln_exp/`.",
        "flags": ["UNCLEAR"],
        "opt_out": "none — expr_skeleton default",
    },
    "calc_diff_general": {
        "title": "General derivatives",
        "generator": "derivative_general",
        "category": "Calculus — Differentiation",
        "skill": "Differentiate mixed expressions drawing on several rules (trig/exp/log/product/quotient/chain).",
        "d0": "Still simple single-class (e.g. sin(affine)) — mixed unlocks with D.",
        "high_d": "Mixed quotient/product/chain across function classes; first derivative preferred.",
        "must_not": "Force one rule leaf’s exclusivity; second-deriv bleed.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §3.3–3.9 (mixed practice)",
                "https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules",
                "combine power/product/quotient/chain/trig/exp/ln",
            ),
        ],
        "local": "diff_skeleton_gallery/general/; form general_mixed + shared forms",
        "variety": "Rotates forms (trig → quotient log/trig → chain power). UNCLEAR: D=22 second derivative.",
        "engine": "**Reuse:** `expr_skeleton` with broad allows + `general_mixed` / shared Diff patterns. Gallery: `diff_skeleton_gallery/general/`.",
        "flags": ["UNCLEAR"],
        "opt_out": "none — expr_skeleton default",
    },
    "calc_diff_higher_order_derivatives": {
        "title": "Higher order derivatives",
        "generator": "derivative_higher_order",
        "category": "Calculus — Differentiation",
        "skill": "Compute second (or higher) derivatives of power/chain-style expressions.",
        "d0": "d²/dx² of a simple monomial/power, e.g. x².",
        "high_d": "d² of (poly)^n or richer inners; optional order 3 forms.",
        "must_not": "First-derivative-only prompts on this leaf; steal all high-D from other leaves via order=2.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §3.2 The Derivative as a Function",
                "https://openstax.org/books/calculus-volume-1/pages/3-2-the-derivative-as-a-function",
                "higher-order derivatives notation",
            ),
            (
                "OpenStax Calculus Volume 1 §3.3 Differentiation Rules",
                "https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules",
                "repeated differentiation of powers",
            ),
        ],
        "local": "diff_skeleton_gallery/higher_order/; forms higher_order_2 / higher_order_3",
        "variety": "Correctly order≥2 from D=0. Good power/chain ladder.",
        "engine": "**Reuse:** `expr_skeleton` with `derivative_order≥2` + `Diff(Pow(H,n))` order2 patterns. Gallery: `diff_skeleton_gallery/higher_order/`.",
        "flags": [],
        "opt_out": "none — expr_skeleton default",
    },
    "calc_diff_implicit": {
        "title": "Implicit",
        "generator": "derivative_implicit",
        "category": "Calculus — Differentiation",
        "skill": "Differentiate an F(x,y)=c relation implicitly and solve for dy/dx.",
        "d0": "Circle-like y²+x²=c → dy/dx = −x/y.",
        "high_d": "Higher powers, products xy, trig of y — OpenStax §3.8.",
        "must_not": "Explicit y=f(x) only; dump without solving for y'.",
        "openstax": [
            (
                "OpenStax Calculus Volume 1 §3.8 Implicit Differentiation",
                "https://openstax.org/books/calculus-volume-1/pages/3-8-implicit-differentiation",
                "F(x,y)=c; solve for dy/dx",
            ),
        ],
        "local": "scripts/output/example_mining/calculus-volume-1/stage1/3-8-implicit-differentiation.md; derivatives.json implicit_basic",
        "variety": (
            "LOW_VARIETY / UNCLEAR — live path is Mad-Lib circle/cubic (y²+x², y³+x³); no `form_id` / "
            "expr_skeleton inventory. Catalog has `implicit_basic` but samples show skeleton_source None."
        ),
        "engine": (
            "**Proposal:** wire `implicit_basic` (and richer §3.8 forms) through a dedicated implicit "
            "skeleton or Diff-adjacent relation sampler — not plain `Diff(F(u))`. Until then leave on "
            "current constructive/Mad-Lib path but expand OpenStax shapes."
        ),
        "flags": ["LOW_VARIETY", "UNCLEAR"],
        "opt_out": "no Diff skeleton yet — live Mad-Lib / constructive implicit",
    },
}


def esc_cell(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ")


def write_note(tid: str, meta: dict) -> Path:
    rows = SAMPLES[tid]
    flags = meta.get("flags") or []
    flag_block = ""
    if flags:
        flag_block = "\n".join(f"- `{f}`" for f in flags) + "\n\n"

    table_lines = []
    for d in ("0", "8", "16", "22"):
        r = rows[d]
        form = r.get("form_id") or "—"
        skel = r.get("skeleton_pattern") or "—"
        pack = r.get("pack") or "—"
        shape = f"form=`{form}`; skel=`{skel}`; pack=`{pack}`"
        table_lines.append(
            f"| {d} | 101 | `${esc_cell(r.get('prompt') or '')}$` | `${esc_cell(r.get('answer') or '')}$` | {esc_cell(shape)} |"
        )

    os_lines = [
        "| Cite | URL | What to copy (shape / frame, not wording) |",
        "|------|-----|-------------------------------------------|",
    ]
    for cite, url, shape in meta["openstax"]:
        os_lines.append(f"| {cite} | {url} | {shape} |")

    body = f"""# Notes — `{tid}` (`{meta['title']}`)

{flag_block}- **Course:** Calculus
- **Category:** {meta['category']}
- **Generator:** `{meta['generator']}`
- **Suggested family:** other (calc limits / Diff)

---

## What the question should look like (D=0 vs high D)

- **Skill:** {meta['skill']}
- **D=0:** {meta['d0']}
- **High D (≈16–22):** {meta['high_d']}
- **Must not:** {meta['must_not']}

## What old / live path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path (Diff leaves → `expr_skeleton` when form maps; limits → LimitSpec packs). No `use_sample_*` / Mad-Lib opt-out found for these generators.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
{chr(10).join(table_lines)}

Opt-out flag used: _{meta['opt_out']}_

## OpenStax examples + chapter/section cites

{chr(10).join(os_lines)}

Local HTML / mining: `{meta['local']}`

## Variety notes / flags

{meta['variety']}

## Proposed engine (reuse vs new) — proposal only

{meta['engine']}

- **Not this pass:** notes only — no generator changes.

Coverage: Diff algebraic families also cataloged in `scripts/output/diff_skeleton_gallery/` (power, product, quotient, chain, trig, invtrig, ln/exp, general, higher_order).
"""
    path = NOTES / f"{tid}.md"
    path.write_text(body, encoding="utf-8")
    return path


def main() -> None:
    written = []
    unclear = []
    low = []
    for tid, meta in META.items():
        assert tid in SAMPLES, tid
        p = write_note(tid, meta)
        written.append(p.name)
        if "UNCLEAR" in (meta.get("flags") or []):
            unclear.append(tid)
        if "LOW_VARIETY" in (meta.get("flags") or []):
            low.append(tid)

    index = NOTES / "CALC_LIMITS_DIFF_INDEX.md"
    index.write_text(
        "# Calculus limits + differentiation notes (steps 1–3)\n\n"
        "Live-sampled D=0/8/16/22 (`seed=101`) on 2026-08-20. Diff defaults to "
        "`expr_skeleton`; limits use LimitSpec / `limits.json`. No generator changes.\n\n"
        "## Files\n\n"
        + "\n".join(f"- [`{n}`]({n})" for n in written)
        + "\n\n## UNCLEAR\n\n"
        + ("\n".join(f"- `{t}`" for t in unclear) or "_none_")
        + "\n\n## LOW_VARIETY\n\n"
        + ("\n".join(f"- `{t}`" for t in low) or "_none_")
        + "\n",
        encoding="utf-8",
    )
    print("wrote", len(written), "notes +", index.name)
    print("UNCLEAR:", ", ".join(unclear))
    print("LOW_VARIETY:", ", ".join(low))


if __name__ == "__main__":
    main()
