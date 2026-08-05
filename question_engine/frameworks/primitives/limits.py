"""Limit expression sampler — continuous-D + form/method allow-lists.

Algebraic Calc 1 limits (plug-in, factor, rationalize, infinity, piecewise jump,
L'Hôpital 0/0 and ∞/∞). Packs are closed-form families with known answers —
not a general limit solver. Mirrors ``derivatives.sample_derivative_expression``
for ML join keys (θ, seed, spec_snapshot, effort_features).

OpenStax structures mirrored (Vol. 1 stage-1 mining)
----------------------------------------------------
- **2.3 Limit Laws / direct:** poly & rational plug-in; ``sin(x−π/4)``,
  ``e^{2x−x²}``, ``ln(x+1)``, ``(2x−1)√(x+4)``, ``arctan`` (via ExpressionSpec
  / ``expr_direct``). Removable factor/conjugate stays algebraic-primary.
- **4.6 Limits at ∞:** rational degree compare; ``sin x / x``; ``arctan``;
  ``(a+be^x)/(c+de^x)``; ``ln x / x^k``; ``e^x / x^k``.
- **4.8 L'Hôpital:** 1-pass ``sin(kx)/x``, ``(e^{kx}−1)/x``; multi-pass
  ``(e^x−1−x)/x²``, ``(sin x−x)/x³``, ``x^k/e^x``, equal-degree poly ∞/∞.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.difficulty_budget import (
    DifficultyFactor,
    select_upgrades,
    settings_difficulty,
)
from question_engine.generators.utils import (
    format_linear_latex,
    format_monomial_latex,
    format_polynomial_latex,
    frac_latex,
    random_int_range,
)

LimitForm = Literal[
    "poly_direct",
    "rational_direct",
    "expr_direct",
    "removable_factor",
    "removable_rationalize",
    "rational_inf",
    "trig_inf",
    "exp_inf",
    "log_inf",
    "invtrig_inf",
    "trig_standard",
    "piecewise_jump",
    "essential",
    "indet_0_0",
    "indet_inf_inf",
]

FORM_ALLOW_KEYS: tuple[str, ...] = (
    "allow_rational",
    "allow_removable",
    "allow_rationalize",
    "allow_trig",
    "allow_exp",
    "allow_log",
    "allow_roots",
    "allow_invtrig",
    "allow_piecewise",
    "allow_essential",
    "allow_indet",
    "allow_one_sided",
    "apply_lhopital",
)

_TOPIC_DEFAULTS: dict[str, dict[str, bool]] = {
    "limit_direct_evaluation": {
        "allow_rational": True,
        "allow_removable": False,
        "allow_rationalize": False,
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": True,
        "allow_roots": True,
        "allow_invtrig": True,
        "allow_piecewise": False,
        "allow_essential": False,
        "allow_indet": False,
        "allow_one_sided": False,
        "apply_lhopital": False,
        "require_removable": False,
        "require_indet": False,
    },
    "limit_at_infinity": {
        "allow_rational": True,
        "allow_removable": False,
        "allow_rationalize": False,
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": True,
        "allow_roots": True,
        "allow_invtrig": True,
        "allow_piecewise": False,
        "allow_essential": False,
        "allow_indet": False,
        "allow_one_sided": False,
        "apply_lhopital": False,
        "require_removable": False,
        "require_indet": False,
    },
    "limit_removable": {
        "allow_rational": True,
        "allow_removable": True,
        "allow_rationalize": True,
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_roots": True,
        "allow_invtrig": False,
        "allow_piecewise": False,
        "allow_essential": False,
        "allow_indet": False,
        "allow_one_sided": False,
        "apply_lhopital": False,
        "require_removable": True,
        "require_indet": False,
    },
    "limit_jump": {
        "allow_rational": False,
        "allow_removable": False,
        "allow_rationalize": False,
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_piecewise": True,
        "allow_essential": False,
        "allow_indet": False,
        "allow_one_sided": True,
        "apply_lhopital": False,
        "require_removable": False,
        "require_indet": False,
    },
    "limit_essential": {
        "allow_rational": True,
        "allow_removable": False,
        "allow_rationalize": False,
        "allow_trig": True,
        "allow_exp": False,
        "allow_log": False,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_piecewise": False,
        "allow_essential": True,
        "allow_indet": False,
        "allow_one_sided": False,
        "apply_lhopital": False,
        "require_removable": False,
        "require_indet": False,
    },
    "limit_continuity": {
        "allow_rational": True,
        "allow_removable": True,
        "allow_rationalize": False,
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_piecewise": True,
        "allow_essential": False,
        "allow_indet": False,
        "allow_one_sided": True,
        "apply_lhopital": False,
        "require_removable": False,
        "require_indet": False,
    },
    "lhopitals_rule": {
        "allow_rational": True,
        "allow_removable": False,
        "allow_rationalize": False,
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": True,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_piecewise": False,
        "allow_essential": False,
        "allow_indet": True,
        "allow_one_sided": False,
        "apply_lhopital": True,
        "require_removable": False,
        "require_indet": True,
    },
}

_TYPE_ID_TO_GENERATOR: dict[str, str] = {
    "calc_limits_by_direct_evaluation": "limit_direct_evaluation",
    "calc_limits_at_jump_discontinuities_and_kinks": "limit_jump",
    "calc_limits_at_removable_discontinuities": "limit_removable",
    "calc_limits_at_essential_discontinuities": "limit_essential",
    "calc_limits_at_infinity": "limit_at_infinity",
    "calc_continuity_determining_and_classifying": "limit_continuity",
    "calc_app_diff_lhopitals_rule": "lhopitals_rule",
    "pc_limits_by_direct_evaluation": "limit_direct_evaluation",
    "pc_limits_at_removable_discontinuities": "limit_removable",
    "pc_limits_at_infinity": "limit_at_infinity",
    "pc_limits_at_essential_discontinuities": "limit_essential",
    "pc_limits_at_kinks_and_jumps": "limit_jump",
    "pc_continuity": "limit_continuity",
}


@dataclass
class LimitSpec:
    """Constraint pack for algebraic limit generation."""

    variable: str = "x"
    approach_mode: str = "finite"  # finite | +inf | -inf | left | right
    approach_abs_max: int = 5
    forms: frozenset[str] = frozenset({"poly_direct"})
    allow_rational: bool = True
    allow_removable: bool = False
    allow_rationalize: bool = False
    allow_trig: bool = False
    allow_exp: bool = False
    allow_log: bool = False
    allow_roots: bool = False
    allow_invtrig: bool = False
    allow_piecewise: bool = False
    allow_essential: bool = False
    allow_indet: bool = False
    allow_one_sided: bool = False
    apply_lhopital: bool = False
    require_removable: bool = False
    require_indet: bool = False
    max_lhopital_steps: int = 1
    coef_abs_max: int = 5
    degree_max: int = 4
    term_count_max: int = 3
    d_spend: float = 6.0
    pack: str = "limit_direct"

    def snapshot(self) -> dict[str, Any]:
        return {
            "pack": self.pack,
            "variable": self.variable,
            "approach_mode": self.approach_mode,
            "approach_abs_max": self.approach_abs_max,
            "forms": sorted(self.forms),
            "allow_rational": self.allow_rational,
            "allow_removable": self.allow_removable,
            "allow_rationalize": self.allow_rationalize,
            "allow_trig": self.allow_trig,
            "allow_exp": self.allow_exp,
            "allow_log": self.allow_log,
            "allow_roots": self.allow_roots,
            "allow_invtrig": self.allow_invtrig,
            "allow_piecewise": self.allow_piecewise,
            "allow_essential": self.allow_essential,
            "allow_indet": self.allow_indet,
            "allow_one_sided": self.allow_one_sided,
            "apply_lhopital": self.apply_lhopital,
            "require_removable": self.require_removable,
            "require_indet": self.require_indet,
            "max_lhopital_steps": self.max_lhopital_steps,
            "coef_abs_max": self.coef_abs_max,
            "degree_max": self.degree_max,
            "term_count_max": self.term_count_max,
            "d_spend": self.d_spend,
        }


@dataclass(frozen=True)
class LimitSample:
    prompt_latex: str
    answer_latex: str
    form: str
    technique: str
    upgrades: tuple[str, ...]
    effective_d: float
    band: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_metadata(self) -> dict[str, Any]:
        gen_key = str(self.metadata.get("generator") or "")
        family = self.form
        structure_id = f"{gen_key}:{family}" if gen_key else family
        return {
            "family": family,
            "structure_id": structure_id,
            "form": self.form,
            "technique": self.technique,
            "methods_used": [self.technique],
            "function_classes": list(self.metadata.get("function_classes") or ["algebraic"]),
            "upgrades": list(self.upgrades),
            "effective_d": self.effective_d,
            "band": self.band,
            **self.metadata,
        }


def resolve_generator_key(topic_or_generator: str | None) -> str | None:
    if not topic_or_generator:
        return None
    key = str(topic_or_generator).strip()
    if key in _TOPIC_DEFAULTS:
        return key
    if key in _TYPE_ID_TO_GENERATOR:
        return _TYPE_ID_TO_GENERATOR[key]
    if key.startswith("c1_") and key[3:] in _TYPE_ID_TO_GENERATOR:
        return _TYPE_ID_TO_GENERATOR[key[3:]]
    return None


def topic_allow_defaults(generator_key: str | None) -> dict[str, bool]:
    base = {k: False for k in FORM_ALLOW_KEYS}
    base["allow_rational"] = True
    base["require_removable"] = False
    base["require_indet"] = False
    if generator_key and generator_key in _TOPIC_DEFAULTS:
        base.update(_TOPIC_DEFAULTS[generator_key])
    return base


def resolve_limit_allows(
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
    topic: str | None = None,
) -> dict[str, bool]:
    key = generator_key or resolve_generator_key(topic)
    defaults = topic_allow_defaults(key)
    out = dict(defaults)
    for k in list(defaults.keys()):
        if k in settings and settings[k] is not None:
            out[k] = bool(settings[k])
    # Legacy allow_infinity → infinity leaf behavior
    if key == "limit_at_infinity" or bool(settings.get("allow_infinity")):
        out["allow_rational"] = True
    return out


def _rng(settings: dict[str, Any]) -> random.Random:
    seed = settings.get("seed")
    if seed is None:
        return random.Random()
    return random.Random(int(seed) ^ 0x4C494D17)


def _band(d: float) -> str:
    if d < 5:
        return "easy"
    if d < 12:
        return "medium"
    return "hard"


def _limit_upgrades() -> list[DifficultyFactor]:
    return [
        DifficultyFactor("rational_body", 2.0, ("form",)),
        DifficultyFactor("higher_degree", 2.5, ("ops",)),
        DifficultyFactor("removable_factor", 3.0, ("method",)),
        DifficultyFactor("rationalize", 3.5, ("method",)),
        DifficultyFactor("trig_form", 3.0, ("class",)),
        DifficultyFactor("exp_log", 3.5, ("class",)),
        DifficultyFactor("piecewise", 4.0, ("form",)),
        DifficultyFactor("essential", 4.5, ("form",)),
        DifficultyFactor("indet_0_0", 5.0, ("method",)),
        DifficultyFactor("indet_inf_inf", 5.5, ("method",)),
        DifficultyFactor("lhopital_twice", 4.0, ("method",)),
        DifficultyFactor("one_sided", 2.0, ("form",)),
    ]


def _coef(rng: random.Random, hi: int, *, exclude_zero: bool = True) -> int:
    excl = {0} if exclude_zero else set()
    return random_int_range(-hi, hi, exclude=excl) if hi > 0 else (1 if exclude_zero else 0)


def _poly_terms(rng: random.Random, *, n_terms: int, degree_max: int, coef_hi: int) -> list[tuple[int, int]]:
    terms: list[tuple[int, int]] = []
    used: set[int] = set()
    for _ in range(max(1, n_terms)):
        power = rng.randint(0, max(0, degree_max))
        tries = 0
        while power in used and tries < 8:
            power = rng.randint(0, max(0, degree_max))
            tries += 1
        used.add(power)
        terms.append((_coef(rng, coef_hi), power))
    return terms


def _eval_poly(terms: list[tuple[int, int]], x: int) -> int:
    return sum(c * (x**p) for c, p in terms)


def _format_poly(terms: list[tuple[int, int]], var: str) -> str:
    if not terms:
        return "0"
    max_p = max(p for _, p in terms)
    coeffs = [0] * (max_p + 1)
    for c, p in terms:
        coeffs[max_p - p] += c
    return format_polynomial_latex(coeffs, variable=var)


def _effort(
    *,
    form: str,
    technique: str,
    degree: int,
    coef_hi: int,
    n_terms: int,
    answer: str,
    pack: str,
    lhopital_steps: int = 0,
) -> dict[str, Any]:
    return {
        "form": form,
        "technique": technique,
        "degree_max": degree,
        "coef_abs_max": coef_hi,
        "n_terms": n_terms,
        "answer_len": len(answer or ""),
        "lhopital_steps": lhopital_steps,
        "nest_depth": 1 if "rational" in form or "indet" in form else 0,
        "pack": pack,
        "methods": [technique],
    }


# ---------------------------------------------------------------------------
# Family builders
# ---------------------------------------------------------------------------


def _sample_poly_direct(
    rng: random.Random,
    spec: LimitSpec,
    *,
    force_form_id: str | None = None,
) -> tuple[str, str, str, str, dict[str, Any]]:
    """OpenStax 2.3 direct eval — polys plus ExpressionSpec specials when allowed."""
    if force_form_id == "squeeze_sin_over_x":
        var = spec.variable
        k = rng.randint(1, max(1, min(4, spec.coef_abs_max)))
        prompt = (
            rf"\lim_{{{var} \to 0}} \frac{{\sin({k}{var})}}{{{var}}}"
            if k != 1
            else rf"\lim_{{{var} \to 0}} \frac{{\sin({var})}}{{{var}}}"
        )
        answer = str(k)
        form, tech = "trig_squeeze", "squeeze_trig"
        effort = _effort(
            form=form, technique=tech, degree=1, coef_hi=spec.coef_abs_max,
            n_terms=1, answer=answer, pack=spec.pack,
        )
        return prompt, answer, form, tech, {
            "function_classes": ["trig"],
            "effort_features": effort,
            "variant": "sin_kx_over_x",
            "form_id": force_form_id,
            "openstax_form": force_form_id,
        }
    if force_form_id and force_form_id.startswith("direct_"):
        hit = _sample_expr_direct(rng, spec, force_form_id=force_form_id)
        if hit is not None:
            return hit
    # Prefer shared expression generator when specials unlocked (mid+ D).
    specials_on = any(
        [
            spec.allow_trig,
            spec.allow_exp,
            spec.allow_log,
            spec.allow_roots,
            spec.allow_invtrig,
        ]
    )
    if specials_on and spec.d_spend >= 4 and rng.random() < (0.75 if spec.d_spend >= 6 else 0.45):
        hit = _sample_expr_direct(rng, spec)
        if hit is not None:
            return hit
    var = spec.variable
    n = rng.randint(1, max(1, spec.term_count_max))
    terms = _poly_terms(rng, n_terms=n, degree_max=spec.degree_max, coef_hi=spec.coef_abs_max)
    a = rng.randint(-spec.approach_abs_max, spec.approach_abs_max)
    value = _eval_poly(terms, a)
    poly = _format_poly(terms, var)
    prompt = rf"\lim_{{{var} \to {a}}} \left({poly}\right)"
    answer = str(value)
    form, tech = "poly_direct", "direct_eval"
    effort = _effort(
        form=form, technique=tech, degree=spec.degree_max, coef_hi=spec.coef_abs_max,
        n_terms=n, answer=answer, pack=spec.pack,
    )
    return prompt, answer, form, tech, {
        "function_classes": ["algebraic"],
        "effort_features": effort,
        "approach_value": a,
        "form_id": "poly_direct",
        "openstax_form": "poly_direct",
    }


def _sample_expr_direct(
    rng: random.Random,
    spec: LimitSpec,
    *,
    force_form_id: str | None = None,
) -> tuple[str, str, str, str, dict[str, Any]] | None:
    """Direct eval via ``pack_limit_direct`` / ``sample_expression`` (OpenStax 2.3).

    Solvable-by-construction: pick approach so domain is OK and answer is clean.
    """
    from question_engine.frameworks.primitives import poly_expression as pe

    fns: set[str] = set()
    if spec.allow_trig:
        fns.add("trig")
    if spec.allow_exp:
        fns.add("exp")
    if spec.allow_log:
        fns.add("log")
    if spec.allow_roots:
        fns.add("roots")
    if spec.allow_invtrig:
        fns.add("invtrig")
    if not fns:
        return None

    # OpenStax-like closed families first (clean exact answers)
    var = spec.variable
    families: list[str] = []
    if spec.allow_trig:
        families.extend(["sin_shift", "cos_kx", "sin_pi_over"])
    if spec.allow_exp:
        families.extend(["exp_linear", "exp_quad"])
    if spec.allow_log:
        families.extend(["ln_linear", "ln_exp"])
    if spec.allow_roots:
        families.append("sqrt_poly")
    if spec.allow_invtrig:
        families.append("arctan_linear")
    if not families:
        return None
    force_map = {
        "direct_sin_shift": ["sin_shift", "cos_kx", "sin_pi_over"],
        "direct_exp": ["exp_linear", "exp_quad"],
        "direct_ln": ["ln_linear", "ln_exp"],
        "direct_sqrt": ["sqrt_poly"],
        "direct_arctan": ["arctan_linear"],
    }
    if force_form_id and force_form_id in force_map:
        cand = [f for f in force_map[force_form_id] if f in families]
        fam = rng.choice(cand) if cand else rng.choice(families)
    else:
        fam = rng.choice(families)

    if fam == "sin_shift":
        # lim x→π/4 sin(x) or lim x→a sin(x − π/4) with a=π/4 → 0
        mode = rng.choice(["plain", "shift"])
        if mode == "plain":
            a_tex, ans = r"\frac{\pi}{6}", r"\frac{1}{2}"
            if rng.random() < 0.5:
                a_tex, ans = r"\frac{\pi}{3}", r"\frac{\sqrt{3}}{2}"
            prompt = rf"\lim_{{{var} \to {a_tex}}} \sin({var})"
        else:
            prompt = rf"\lim_{{{var} \to \frac{{\pi}}{{4}}}} \sin\left({var}-\frac{{\pi}}{{4}}\right)"
            ans = "0"
        classes = ["trig"]
    elif fam == "cos_kx":
        k = rng.randint(1, 3)
        prompt = rf"\lim_{{{var} \to 0}} \cos({k}{var})" if k != 1 else rf"\lim_{{{var} \to 0}} \cos({var})"
        ans = "1"
        classes = ["trig"]
    elif fam == "sin_pi_over":
        prompt = rf"\lim_{{{var} \to \pi}} \frac{{\sin({var})}}{{\tan({var})}}"
        ans = "-1"
        classes = ["trig"]
    elif fam == "exp_linear":
        k = rng.randint(1, 3)
        a = rng.randint(0, 2)
        prompt = rf"\lim_{{{var} \to {a}}} e^{{{k}{var}}}" if k != 1 else rf"\lim_{{{var} \to {a}}} e^{{{var}}}"
        # e^{k a}
        if a == 0:
            ans = "1"
        elif k == 1 and a == 1:
            ans = "e"
        else:
            ans = rf"e^{{{k * a}}}" if k * a != 1 else "e"
        classes = ["exp"]
    elif fam == "exp_quad":
        # OpenStax: lim x→2 e^{2x−x²}
        prompt = rf"\lim_{{{var} \to 2}} e^{{2{var}-{var}^{{2}}}}"
        ans = "1"
        classes = ["exp"]
    elif fam == "ln_linear":
        # lim x→0 ln(x+1) = 0; lim x→e−1 ln(x+1)=1
        if rng.random() < 0.5:
            prompt = rf"\lim_{{{var} \to 0}} \ln({var}+1)"
            ans = "0"
        else:
            prompt = rf"\lim_{{{var} \to e-1}} \ln({var}+1)"
            ans = "1"
        classes = ["log"]
    elif fam == "ln_exp":
        prompt = rf"\lim_{{{var} \to 3}} \ln e^{{3{var}}}"
        ans = "9"
        classes = ["log", "exp"]
    elif fam == "sqrt_poly":
        prompt = rf"\lim_{{{var} \to 6}} (2{var}-1)\sqrt{{{var}+4}}"
        # (12-1)√10 = 11√10
        ans = r"11\sqrt{10}"
        classes = ["algebraic", "roots"]
    else:
        prompt = rf"\lim_{{{var} \to 0}} \arctan({var})"
        ans = "0"
        classes = ["invtrig"]

    # Also stamp ExpressionSpec snapshot for ML
    expr_spec = pe.pack_limit_direct(
        float(spec.d_spend),
        coef_hi=spec.coef_abs_max,
        variable=var,
        allowed_functions=frozenset(fns),
    )
    form, tech = "expr_direct", "direct_eval"
    effort = _effort(
        form=form, technique=tech, degree=spec.degree_max, coef_hi=spec.coef_abs_max,
        n_terms=1, answer=ans, pack=spec.pack,
    )
    return prompt, ans, form, tech, {
        "function_classes": classes,
        "effort_features": effort,
        "variant": fam,
        "expr_spec_snapshot": pe.spec_snapshot(expr_spec),
        "openstax_form": force_form_id or f"direct_{fam}",
        "form_id": force_form_id or f"direct_{fam}",
    }


def _sample_rational_direct(
    rng: random.Random, spec: LimitSpec
) -> tuple[str, str, str, str, dict[str, Any]]:
    var = spec.variable
    a = rng.randint(-spec.approach_abs_max, spec.approach_abs_max)
    # Ensure denominator ≠ 0 at a
    for _ in range(20):
        num = _poly_terms(rng, n_terms=2, degree_max=min(3, spec.degree_max), coef_hi=spec.coef_abs_max)
        den_c = _coef(rng, max(1, spec.coef_abs_max))
        den_b = _coef(rng, max(1, spec.coef_abs_max), exclude_zero=False)
        if den_c * a + den_b == 0:
            continue
        num_v = _eval_poly(num, a)
        den_v = den_c * a + den_b
        num_l = _format_poly(num, var)
        den_l = format_linear_latex(den_c, den_b, variable=var)
        prompt = rf"\lim_{{{var} \to {a}}} \frac{{{num_l}}}{{{den_l}}}"
        answer = frac_latex(Fraction(num_v, den_v))
        form, tech = "rational_direct", "direct_eval"
        effort = _effort(
            form=form, technique=tech, degree=spec.degree_max, coef_hi=spec.coef_abs_max,
            n_terms=2, answer=answer, pack=spec.pack,
        )
        return prompt, answer, form, tech, {
            "function_classes": ["algebraic"],
            "effort_features": effort,
            "approach_value": a,
        }
    return _sample_poly_direct(rng, spec)


def _sample_removable_factor(
    rng: random.Random,
    spec: LimitSpec,
    *,
    force_form_id: str | None = None,
) -> tuple[str, str, str, str, dict[str, Any]]:
    var = spec.variable
    a = rng.randint(1, max(1, spec.approach_abs_max))
    b = _coef(rng, max(2, spec.coef_abs_max))
    # (x-a)(x-b)/(x-a) → x-b at x=a, value a-b; or (x^2-a^2)/(x-a)=x+a
    kind_map = {
        "removable_diff_sq": "diff_sq",
        "removable_linear_factor": "linear_factor",
        "removable_quad_shared": "quad_shared",
    }
    if force_form_id and force_form_id in kind_map:
        kind = kind_map[force_form_id]
    else:
        kind = rng.choice(["diff_sq", "linear_factor", "quad_shared"])
    if kind == "diff_sq":
        prompt = rf"\lim_{{{var} \to {a}}} \frac{{{var}^{{2}}-{a * a}}}{{{var}-{a}}}"
        answer = str(2 * a)
        variant = "diff_sq"
    elif kind == "linear_factor":
        # (x-a)(x+b)/(x-a) = x+b
        prompt = (
            rf"\lim_{{{var} \to {a}}} "
            rf"\frac{{({var}-{a})({var}+{b})}}{{{var}-{a}}}"
        )
        answer = str(a + b)
        variant = "linear_factor"
    else:
        # (x^2+(c-a)x - a c)/(x-a) = x+c with c≠0
        c = _coef(rng, max(2, spec.coef_abs_max))
        # expand (x-a)(x+c) = x^2+(c-a)x - a c
        mid = c - a
        const = -a * c
        # Avoid printing a bare 0x term when mid==0
        if mid == 0:
            body = f"{var}^{{2}}" + (f"+{const}" if const > 0 else str(const))
        else:
            mid_s = f"+{mid}" if mid > 0 else str(mid)
            const_s = f"+{const}" if const > 0 else str(const)
            body = f"{var}^{{2}}{mid_s}{var}{const_s}"
        prompt = (
            rf"\lim_{{{var} \to {a}}} "
            rf"\frac{{{body}}}{{{var}-{a}}}"
        )
        answer = str(a + c)
        variant = "quad_shared"
    form, tech = "removable_factor", "factor_cancel"
    effort = _effort(
        form=form, technique=tech, degree=2, coef_hi=spec.coef_abs_max,
        n_terms=2, answer=answer, pack=spec.pack,
    )
    return prompt, answer, form, tech, {
        "function_classes": ["algebraic"],
        "effort_features": effort,
        "approach_value": a,
        "variant": variant,
        "form_id": force_form_id or f"removable_{variant}",
        "openstax_form": force_form_id or f"removable_{variant}",
    }


def _sample_removable_rationalize(
    rng: random.Random, spec: LimitSpec
) -> tuple[str, str, str, str, dict[str, Any]]:
    var = spec.variable
    a = rng.randint(1, max(1, min(4, spec.approach_abs_max)))
    # lim x→a (√x - √a)/(x-a) = 1/(2√a)
    prompt = (
        rf"\lim_{{{var} \to {a}}} "
        rf"\frac{{\sqrt{{{var}}}-\sqrt{{{a}}}}}{{{var}-{a}}}"
    )
    answer = frac_latex(Fraction(1, 2 * a)) if a > 0 else rf"\frac{{1}}{{2\sqrt{{{a}}}}}"
    # Prefer exact 1/(2√a)
    answer = rf"\frac{{1}}{{2\sqrt{{{a}}}}}"
    form, tech = "removable_rationalize", "rationalize"
    effort = _effort(
        form=form, technique=tech, degree=1, coef_hi=spec.coef_abs_max,
        n_terms=2, answer=answer, pack=spec.pack,
    )
    return prompt, answer, form, tech, {
        "function_classes": ["algebraic", "roots"],
        "effort_features": effort,
        "approach_value": a,
    }


def _sample_infinity(
    rng: random.Random,
    spec: LimitSpec,
    *,
    force_form_id: str | None = None,
) -> tuple[str, str, str, str, dict[str, Any]]:
    """OpenStax 4.6 — rationals plus sin/x, arctan, exp ratios, ln/x^k."""
    var = spec.variable
    to_pos = rng.choice([True, False])
    infinity = r"\infty" if to_pos else r"-\infty"
    families: list[str] = ["rational"]
    if spec.allow_trig:
        families.extend(["sin_over_x", "bounded_over_poly"])
    if spec.allow_invtrig:
        families.append("arctan_inf")
    if spec.allow_exp:
        families.extend(["exp_ratio", "exp_over_poly"])
    if spec.allow_log:
        families.append("ln_over_poly")
    if spec.d_spend < 5:
        families = ["rational"]
    force_map = {
        "inf_rational": ["rational"],
        "inf_sin_over_x": ["sin_over_x", "bounded_over_poly"],
        "inf_arctan": ["arctan_inf"],
        "inf_exp_ratio": ["exp_ratio", "exp_over_poly"],
        "inf_ln_over_poly": ["ln_over_poly"],
    }
    if force_form_id and force_form_id in force_map:
        cand = [f for f in force_map[force_form_id] if f in families] or force_map[force_form_id]
        fam = rng.choice(cand)
    else:
        fam = rng.choice(families)

    if fam == "sin_over_x":
        prompt = rf"\lim_{{{var} \to {infinity}}} \frac{{\sin({var})}}{{{var}}}"
        answer = "0"
        classes = ["trig"]
        form = "trig_inf"
    elif fam == "bounded_over_poly":
        n = rng.randint(1, 3)
        prompt = rf"\lim_{{{var} \to {infinity}}} \frac{{\cos({var})}}{{{var}^{{{n}}}}}"
        answer = "0"
        classes = ["trig"]
        form = "trig_inf"
    elif fam == "arctan_inf":
        prompt = rf"\lim_{{{var} \to {infinity}}} \arctan({var})"
        answer = r"\frac{\pi}{2}" if to_pos else r"-\frac{\pi}{2}"
        classes = ["invtrig"]
        form = "invtrig_inf"
    elif fam == "exp_ratio":
        # (a + b e^x)/(c + d e^x) → b/d as +∞; a/c as −∞
        a, b = rng.randint(1, 4), rng.randint(1, 4)
        c, d = rng.randint(1, 4), rng.randint(1, 4)
        prompt = (
            rf"\lim_{{{var} \to {infinity}}} "
            rf"\frac{{{a}+{b}e^{{{var}}}}}{{{c}+{d}e^{{{var}}}}}"
        )
        answer = frac_latex(Fraction(b, d)) if to_pos else frac_latex(Fraction(a, c))
        classes = ["exp"]
        form = "exp_inf"
    elif fam == "exp_over_poly":
        k = rng.randint(1, 3)
        prompt = rf"\lim_{{{var} \to {infinity}}} \frac{{e^{{{var}}}}}{{{var}^{{{k}}}}}"
        answer = r"\infty" if to_pos else "0"  # e^x/x^k →0 as x→−∞
        classes = ["exp"]
        form = "exp_inf"
    elif fam == "ln_over_poly":
        k = rng.randint(1, 3)
        prompt = rf"\lim_{{{var} \to \infty}} \frac{{\ln({var})}}{{{var}^{{{k}}}}}"
        answer = "0"
        classes = ["log"]
        form = "log_inf"
        infinity = r"\infty"
        to_pos = True
    else:
        lead_coef = _coef(rng, spec.coef_abs_max)
        lead_power = rng.randint(1, max(1, spec.degree_max))
        lower_power = rng.randint(0, max(0, lead_power - 1))
        lower_coef = _coef(rng, spec.coef_abs_max)
        num = _format_poly([(lead_coef, lead_power), (lower_coef, lower_power)], var)
        den_power = rng.randint(0, lead_power)
        den_coef = rng.randint(1, max(1, spec.coef_abs_max))
        den = format_monomial_latex(den_coef, variable=var, degree=den_power) or str(den_coef)
        prompt = rf"\lim_{{{var} \to {infinity}}} \frac{{{num}}}{{{den}}}"
        if lead_power > den_power:
            if lead_power % 2 == 0:
                pos_inf = lead_coef > 0
            else:
                pos_inf = (lead_coef > 0) == to_pos
            answer = r"\infty" if pos_inf else r"-\infty"
        elif lead_power < den_power:
            answer = "0"
        else:
            answer = frac_latex(Fraction(lead_coef, den_coef))
        classes = ["algebraic"]
        form = "rational_inf"

    tech = "compare_degrees" if form == "rational_inf" else "end_behavior"
    effort = _effort(
        form=form, technique=tech, degree=spec.degree_max, coef_hi=spec.coef_abs_max,
        n_terms=2, answer=answer, pack=spec.pack,
    )
    return prompt, answer, form, tech, {
        "function_classes": classes,
        "effort_features": effort,
        "approach_mode": "+inf" if to_pos else "-inf",
        "variant": fam,
        "openstax_form": force_form_id or f"inf_{fam}",
        "form_id": force_form_id or f"inf_{fam}",
    }


def _sample_jump(
    rng: random.Random, spec: LimitSpec
) -> tuple[str, str, str, str, dict[str, Any]]:
    var = spec.variable
    a = rng.randint(-spec.approach_abs_max, spec.approach_abs_max)
    left_val = _coef(rng, spec.coef_abs_max, exclude_zero=False)
    right_val = left_val + _coef(rng, max(2, spec.coef_abs_max))
    # Piecewise constant sides: lim x→a- = L, lim x→a+ = R; two-sided DNE if L≠R
    one_sided = spec.allow_one_sided and rng.random() < 0.55
    if one_sided:
        side = rng.choice(["left", "right"])
        if side == "left":
            prompt = (
                rf"\lim_{{{var} \to {a}^{{-}}}} f({var})\text{{ where }}"
                rf"f({var})=\begin{{cases}}{left_val}&{var}<{a}\\"
                rf"{right_val}&{var}\ge {a}\end{{cases}}"
            )
            answer = str(left_val)
            approach_mode = "left"
        else:
            prompt = (
                rf"\lim_{{{var} \to {a}^{{+}}}} f({var})\text{{ where }}"
                rf"f({var})=\begin{{cases}}{left_val}&{var}<{a}\\"
                rf"{right_val}&{var}\ge {a}\end{{cases}}"
            )
            answer = str(right_val)
            approach_mode = "right"
    else:
        prompt = (
            rf"\lim_{{{var} \to {a}}} f({var})\text{{ where }}"
            rf"f({var})=\begin{{cases}}{left_val}&{var}<{a}\\"
            rf"{right_val}&{var}\ge {a}\end{{cases}}"
        )
        answer = r"\text{DNE}" if left_val != right_val else str(left_val)
        approach_mode = "two_sided"
    form, tech = "piecewise_jump", "one_sided" if one_sided else "two_sided_compare"
    effort = _effort(
        form=form, technique=tech, degree=0, coef_hi=spec.coef_abs_max,
        n_terms=2, answer=answer, pack=spec.pack,
    )
    return prompt, answer, form, tech, {
        "function_classes": ["algebraic", "piecewise"],
        "effort_features": effort,
        "approach_value": a,
        "approach_mode": approach_mode,
        "left_value": left_val,
        "right_value": right_val,
    }


def _sample_essential(
    rng: random.Random,
    spec: LimitSpec,
    *,
    force_form_id: str | None = None,
) -> tuple[str, str, str, str, dict[str, Any]]:
    var = spec.variable
    a = 0
    if force_form_id == "essential_sin_1_over_x":
        kind = "oscillate"
    elif force_form_id == "essential_1_over_x":
        kind = "reciprocal"
    else:
        kind = rng.choice(["reciprocal", "oscillate"]) if spec.allow_trig else "reciprocal"
    if kind == "reciprocal":
        prompt = rf"\lim_{{{var} \to {a}}} \frac{{1}}{{{var}}}"
        answer = r"\text{DNE}"
        classes = ["algebraic"]
        variant = "1/x"
        fid = "essential_1_over_x"
    else:
        prompt = rf"\lim_{{{var} \to {a}}} \sin\left(\frac{{1}}{{{var}}}\right)"
        answer = r"\text{DNE}"
        classes = ["trig"]
        variant = "sin_1_over_x"
        fid = "essential_sin_1_over_x"
    form, tech = "essential", "essential_dne"
    effort = _effort(
        form=form, technique=tech, degree=1, coef_hi=1,
        n_terms=1, answer=answer, pack=spec.pack,
    )
    return prompt, answer, form, tech, {
        "function_classes": classes,
        "effort_features": effort,
        "approach_value": a,
        "variant": variant,
        "form_id": force_form_id or fid,
        "openstax_form": force_form_id or fid,
    }


def _sample_continuity(
    rng: random.Random, spec: LimitSpec
) -> tuple[str, str, str, str, dict[str, Any]]:
    """Classify continuity at a point: continuous / removable / jump."""
    var = spec.variable
    a = rng.randint(-spec.approach_abs_max, spec.approach_abs_max)
    kind = rng.choice(["continuous", "removable", "jump"])
    if kind == "continuous":
        b = _coef(rng, spec.coef_abs_max)
        c = _coef(rng, spec.coef_abs_max, exclude_zero=False)
        body = format_linear_latex(b, c, variable=var)
        prompt = (
            rf"\text{{Classify the continuity of }}f({var})={body}"
            rf"\text{{ at }}{var}={a}."
        )
        answer = r"\text{continuous}"
        form, tech = "poly_direct", "classify_continuous"
    elif kind == "removable":
        prompt = (
            rf"\text{{Classify the continuity of }}"
            rf"f({var})=\frac{{{var}^{{2}}-{a * a}}}{{{var}-{a}}}"
            rf"\text{{ at }}{var}={a}."
        )
        answer = r"\text{removable discontinuity}"
        form, tech = "removable_factor", "classify_removable"
    else:
        left_val = _coef(rng, spec.coef_abs_max, exclude_zero=False)
        right_val = left_val + _coef(rng, max(2, spec.coef_abs_max))
        prompt = (
            rf"\text{{Classify the continuity of }}"
            rf"f({var})=\begin{{cases}}{left_val}&{var}<{a}\\"
            rf"{right_val}&{var}\ge {a}\end{{cases}}"
            rf"\text{{ at }}{var}={a}."
        )
        answer = r"\text{jump discontinuity}"
        form, tech = "piecewise_jump", "classify_jump"
    effort = _effort(
        form=form, technique=tech, degree=2, coef_hi=spec.coef_abs_max,
        n_terms=2, answer=answer, pack=spec.pack,
    )
    return prompt, answer, form, tech, {
        "function_classes": ["algebraic", "piecewise"] if kind == "jump" else ["algebraic"],
        "effort_features": effort,
        "approach_value": a,
        "variant": kind,
    }


def _sample_lhopital(
    rng: random.Random,
    spec: LimitSpec,
    *,
    purchased: set[str],
    force_form_id: str | None = None,
) -> tuple[str, str, str, str, dict[str, Any]]:
    """OpenStax 4.8 — 1-pass at low D; 2+ passes (poly/exp/trig) at mid/high D."""
    var = spec.variable
    steps = 2 if "lhopital_twice" in purchased and spec.max_lhopital_steps >= 2 else 1
    if spec.d_spend >= 12 and spec.max_lhopital_steps >= 2 and rng.random() < 0.55:
        steps = max(steps, 2)
    if spec.d_spend >= 18 and rng.random() < 0.35:
        steps = max(steps, 3)
    # Catalog forces
    if force_form_id == "lhopital_multipass_exp":
        steps = max(steps, 2)
        use_inf = False
        purchased = set(purchased) | {"lhopital_twice"}
    elif force_form_id == "lhopital_multipass_trig":
        steps = max(steps, 2)
        use_inf = False
    elif force_form_id == "lhopital_poly_over_exp":
        steps = max(steps, 2)
        use_inf = True
        purchased = set(purchased) | {"indet_inf_inf", "lhopital_twice"}
    elif force_form_id == "lhopital_inf_inf_poly":
        use_inf = True
        purchased = set(purchased) | {"indet_inf_inf"}
    elif force_form_id == "lhopital_0_0_trig":
        use_inf = False
        steps = 1
    elif force_form_id == "lhopital_0_0_poly":
        use_inf = False
        steps = 1
    else:
        use_inf = "indet_inf_inf" in purchased or (
            spec.allow_indet and rng.random() < 0.35 and "indet_0_0" not in purchased
        )
    classes = ["algebraic"]
    variant = "poly"

    # Multi-pass OpenStax forms first when steps≥2
    if steps >= 2 and not use_inf:
        multi = []
        if spec.allow_trig:
            multi.append("sin_minus_x")  # (sin x − x)/x² → 0 (2 passes); /x³ needs 3
        if spec.allow_exp:
            multi.append("exp_taylor")  # (e^x−1−x)/x² → 1/2
        multi.append("poly_high")  # (x^n−a^n) style still 1; use x² e^{-x} growth
        if spec.allow_exp:
            multi.append("poly_over_exp")  # x^k / e^x → 0 (k passes)
        if spec.allow_log and steps >= 2:
            multi.append("ln_over_power")
        if force_form_id == "lhopital_multipass_trig":
            fam = "sin_minus_x"
        elif force_form_id == "lhopital_multipass_exp":
            fam = "exp_taylor"
        elif force_form_id == "lhopital_poly_over_exp":
            fam = "poly_over_exp"
        else:
            fam = rng.choice(multi or ["exp_taylor"])
        if fam == "sin_minus_x":
            # OpenStax: lim (sin x − x)/x² = 0 (actually needs careful; (sinx-x)/x^3 = -1/6)
            if steps >= 3:
                prompt = rf"\lim_{{{var} \to 0}} \frac{{\sin({var})-{var}}}{{{var}^{{3}}}}"
                answer = frac_latex(Fraction(-1, 6))
                steps = 3
            else:
                prompt = rf"\lim_{{{var} \to 0}} \frac{{\sin({var})-{var}}}{{{var}^{{2}}}}"
                answer = "0"
                steps = 2
            classes = ["trig"]
            variant = fam
            form, tech = "indet_0_0", "lhopital"
        elif fam == "exp_taylor":
            prompt = rf"\lim_{{{var} \to 0}} \frac{{e^{{{var}}}-1-{var}}}{{{var}^{{2}}}}"
            answer = frac_latex(Fraction(1, 2))
            classes = ["exp"]
            variant = fam
            form, tech = "indet_0_0", "lhopital"
            steps = 2
        elif fam == "poly_over_exp":
            k = min(steps, rng.randint(2, 3))
            prompt = rf"\lim_{{{var} \to \infty}} \frac{{{var}^{{{k}}}}}{{e^{{{var}}}}}"
            answer = "0"
            classes = ["exp"]
            variant = fam
            form, tech = "indet_inf_inf", "lhopital"
            steps = k
        elif fam == "ln_over_power":
            k = rng.randint(1, 2)
            prompt = rf"\lim_{{{var} \to \infty}} \frac{{\ln({var})}}{{{var}^{{{k}}}}}"
            answer = "0"
            classes = ["log"]
            variant = fam
            form, tech = "indet_inf_inf", "lhopital"
            steps = 1 if k == 1 else 2
        else:
            # High-degree equal polys needing 2 L'H: (ax³+…)/(bx³+…)
            a = rng.randint(1, max(1, spec.coef_abs_max))
            c = rng.randint(1, max(1, spec.coef_abs_max))
            prompt = (
                rf"\lim_{{{var} \to \infty}} "
                rf"\frac{{{a}{var}^{{3}}+{var}}}{{{c}{var}^{{3}}+1}}"
            )
            answer = frac_latex(Fraction(a, c))
            form, tech = "indet_inf_inf", "lhopital"
            steps = 3
            variant = "poly_deg3"
    elif use_inf:
        a = rng.randint(1, max(1, spec.coef_abs_max))
        c = rng.randint(1, max(1, spec.coef_abs_max))
        b = _coef(rng, spec.coef_abs_max, exclude_zero=False)
        d = _coef(rng, spec.coef_abs_max, exclude_zero=False)
        if steps >= 2 and spec.allow_exp and rng.random() < 0.4:
            prompt = rf"\lim_{{{var} \to \infty}} \frac{{{var}^{{2}}}}{{e^{{{var}}}}}"
            answer = "0"
            classes = ["exp"]
            form, tech = "indet_inf_inf", "lhopital"
            steps = 2
            variant = "x2_over_exp"
        else:
            prompt = (
                rf"\lim_{{{var} \to \infty}} "
                rf"\frac{{{a}{var}^{{2}}+{b}}}{{{c}{var}^{{2}}+{d}}}"
            )
            answer = frac_latex(Fraction(a, c))
            form, tech = "indet_inf_inf", "lhopital"
            steps = min(2, max(1, steps))
            variant = "poly_inf"
    elif force_form_id == "lhopital_0_0_trig" or (spec.allow_trig and rng.random() < 0.45):
        k = rng.randint(2, max(2, min(6, spec.coef_abs_max)))
        arg = format_monomial_latex(k, variable=var) or f"{k}{var}"
        prompt = rf"\lim_{{{var} \to 0}} \frac{{\sin({arg})}}{{{var}}}"
        answer = str(k)
        form, tech = "indet_0_0", "lhopital"
        classes = ["trig"]
        steps = 1
        variant = "sin_kx_over_x"
    elif spec.allow_exp and rng.random() < 0.4:
        k = rng.randint(1, max(1, min(5, spec.coef_abs_max)))
        prompt = rf"\lim_{{{var} \to 0}} \frac{{e^{{{k}{var}}}-1}}{{{var}}}"
        answer = str(k)
        form, tech = "indet_0_0", "lhopital"
        classes = ["exp"]
        steps = 1
        variant = "exp_kx"
    else:
        a = rng.randint(1, max(1, min(4, spec.approach_abs_max)))
        n = 2 if steps == 1 else rng.randint(2, 3)
        prompt = (
            rf"\lim_{{{var} \to {a}}} "
            rf"\frac{{{var}^{{{n}}}-{a ** n}}}{{{var}-{a}}}"
        )
        answer = str(n * (a ** (n - 1)))
        form, tech = "indet_0_0", "lhopital"
        steps = 1
        variant = "power_diff"

    effort = _effort(
        form=form, technique=tech, degree=2, coef_hi=spec.coef_abs_max,
        n_terms=2, answer=answer, pack=spec.pack, lhopital_steps=steps,
    )
    effort["lhopital_passes"] = steps
    return prompt, answer, form, tech, {
        "function_classes": classes,
        "effort_features": effort,
        "lhopital_steps": steps,
        "lhopital_passes": steps,
        "tricks_required": ["lhopital"] * steps,
        "indet_form": "inf_inf" if form == "indet_inf_inf" else "0_0",
        "variant": variant,
        "openstax_form": force_form_id or f"lhopital_{variant}_{steps}pass",
        "form_id": force_form_id or f"lhopital_{variant}_{steps}pass",
    }


def build_limit_spec(
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
    allows: dict[str, bool] | None = None,
    purchased: set[str] | None = None,
    d: float | None = None,
) -> LimitSpec:
    key = generator_key or "limit_direct_evaluation"
    allows = allows or resolve_limit_allows(settings, generator_key=key)
    purchased = purchased or set()
    d = float(d if d is not None else settings_difficulty(settings, default=6.0))
    var = str(settings.get("variable", "x"))
    coef_hi = int(settings.get("coef_max", 6) or 6)
    if "coef_min" in settings and settings["coef_min"] is not None:
        coef_hi = max(coef_hi, abs(int(settings["coef_min"])))
    # D widens coef/degree
    coef_hi = max(coef_hi, 3 + int(d // 4))
    degree_max = int(settings.get("power_max", 3) or 3)
    if "higher_degree" in purchased:
        degree_max = max(degree_max, min(6, degree_max + 1))
    approach_abs = int(settings.get("limit_approach_max", 5) or 5)
    approach_abs = max(approach_abs, abs(int(settings.get("limit_approach_min", -5) or -5)))

    forms: set[str] = set()
    pack = "limit_direct"
    approach_mode = "finite"

    if key == "limit_at_infinity":
        forms.add("rational_inf")
        pack = "limit_infinity"
        approach_mode = "+inf"
    elif key == "limit_removable":
        forms.add("removable_factor")
        if allows.get("allow_rationalize") and (
            "rationalize" in purchased or d >= 8
        ):
            forms.add("removable_rationalize")
        pack = "limit_removable"
    elif key == "limit_jump":
        forms.add("piecewise_jump")
        pack = "limit_jump"
    elif key == "limit_essential":
        forms.add("essential")
        pack = "limit_essential"
    elif key == "limit_continuity":
        forms.update({"poly_direct", "removable_factor", "piecewise_jump"})
        pack = "limit_continuity"
    elif key == "lhopitals_rule":
        forms.add("indet_0_0")
        if "indet_inf_inf" in purchased or d >= 10:
            forms.add("indet_inf_inf")
        pack = "limit_lhopital"
    else:
        forms.add("poly_direct")
        if allows.get("allow_rational") and (
            "rational_body" in purchased or d >= 5
        ):
            forms.add("rational_direct")
        if allows.get("allow_trig") and "trig_form" in purchased:
            forms.add("trig_standard")
        pack = "limit_direct"

    max_lh = int(settings.get("max_lhopital_steps", 1) or 1)
    if "lhopital_twice" in purchased:
        max_lh = max(max_lh, 2)
    if d >= 12:
        max_lh = max(max_lh, 2)
    if d >= 18:
        max_lh = max(max_lh, 3)

    return LimitSpec(
        variable=var,
        approach_mode=approach_mode,
        approach_abs_max=approach_abs,
        forms=frozenset(forms),
        allow_rational=bool(allows.get("allow_rational")),
        allow_removable=bool(allows.get("allow_removable")),
        allow_rationalize=bool(allows.get("allow_rationalize")),
        allow_trig=bool(allows.get("allow_trig")),
        allow_exp=bool(allows.get("allow_exp")),
        allow_log=bool(allows.get("allow_log")),
        allow_roots=bool(allows.get("allow_roots")),
        allow_invtrig=bool(allows.get("allow_invtrig")),
        allow_piecewise=bool(allows.get("allow_piecewise")),
        allow_essential=bool(allows.get("allow_essential")),
        allow_indet=bool(allows.get("allow_indet")),
        allow_one_sided=bool(allows.get("allow_one_sided")),
        apply_lhopital=bool(allows.get("apply_lhopital")),
        require_removable=bool(allows.get("require_removable")),
        require_indet=bool(allows.get("require_indet")),
        max_lhopital_steps=max_lh,
        coef_abs_max=coef_hi,
        degree_max=degree_max,
        term_count_max=max(1, int(settings.get("term_count", 3) or 3)),
        d_spend=d,
        pack=pack,
    )


def _pick_form(rng: random.Random, forms: frozenset[str]) -> str:
    pool = list(forms) or ["poly_direct"]
    return rng.choice(pool)


def sample_limit_expression(
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
    topic: str | None = None,
    rng: random.Random | None = None,
) -> LimitSample:
    rng = rng or _rng(settings)
    key = generator_key or resolve_generator_key(topic) or "limit_direct_evaluation"
    allows = resolve_limit_allows(settings, generator_key=key, topic=topic)
    d = settings_difficulty(settings, default=6.0)
    band = _band(d)

    allowed_ids: set[str] | None = None
    upgrades = _limit_upgrades()
    # Gate upgrades by allow flags
    id_gate = {
        "rational_body": allows.get("allow_rational"),
        "removable_factor": allows.get("allow_removable") or allows.get("require_removable"),
        "rationalize": allows.get("allow_rationalize"),
        "trig_form": allows.get("allow_trig"),
        "exp_log": allows.get("allow_exp") or allows.get("allow_log"),
        "piecewise": allows.get("allow_piecewise"),
        "essential": allows.get("allow_essential"),
        "indet_0_0": allows.get("allow_indet") or allows.get("apply_lhopital"),
        "indet_inf_inf": allows.get("allow_indet") or allows.get("apply_lhopital"),
        "lhopital_twice": allows.get("apply_lhopital"),
        "one_sided": allows.get("allow_one_sided"),
        "higher_degree": True,
    }
    allowed_ids = {uid for uid, ok in id_gate.items() if ok}
    purchased_list, _, _ = select_upgrades(
        upgrades, d, allowed_ids=allowed_ids, rng=rng
    )
    purchased = {f.id for f in purchased_list}
    if allows.get("require_removable"):
        purchased.add("removable_factor")
    if allows.get("require_indet") or allows.get("apply_lhopital"):
        purchased.add("indet_0_0")

    spec = build_limit_spec(
        settings, generator_key=key, allows=allows, purchased=purchased, d=d
    )

    # Catalog-driven form_id (textbook case), then dispatch.
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        forms_for_leaf,
        load_form_catalog,
        select_form_id,
    )

    lim_catalog = load_form_catalog("limits")
    lim_forms = forms_for_leaf(lim_catalog, key)
    catalog_form = select_form_id(lim_forms, d=d, rng=rng) if lim_forms else None
    catalog_fid = str(catalog_form["form_id"]) if catalog_form else ""
    form = _pick_form(rng, spec.forms)

    if catalog_fid.startswith("lhopital") or key == "lhopitals_rule" or form in {
        "indet_0_0",
        "indet_inf_inf",
    }:
        prompt, answer, form, tech, extra = _sample_lhopital(
            rng, spec, purchased=purchased, force_form_id=catalog_fid or None
        )
    elif catalog_fid == "continuity_classify" or key == "limit_continuity":
        prompt, answer, form, tech, extra = _sample_continuity(rng, spec)
    elif catalog_fid.startswith("inf_") or form == "rational_inf" or key == "limit_at_infinity":
        prompt, answer, form, tech, extra = _sample_infinity(
            rng, spec, force_form_id=catalog_fid or None
        )
    elif catalog_fid == "removable_rationalize" or form == "removable_rationalize":
        prompt, answer, form, tech, extra = _sample_removable_rationalize(rng, spec)
    elif catalog_fid.startswith("removable_") or form == "removable_factor" or key == "limit_removable":
        if catalog_fid == "removable_rationalize" or (
            not catalog_fid
            and "rationalize" in purchased
            and allows.get("allow_rationalize")
            and rng.random() < 0.35
        ):
            prompt, answer, form, tech, extra = _sample_removable_rationalize(rng, spec)
            catalog_fid = catalog_fid or "removable_rationalize"
        else:
            prompt, answer, form, tech, extra = _sample_removable_factor(
                rng, spec, force_form_id=catalog_fid or None
            )
    elif catalog_fid == "piecewise_jump" or form == "piecewise_jump" or key == "limit_jump":
        prompt, answer, form, tech, extra = _sample_jump(rng, spec)
    elif catalog_fid.startswith("essential_") or form == "essential" or key == "limit_essential":
        prompt, answer, form, tech, extra = _sample_essential(
            rng, spec, force_form_id=catalog_fid or None
        )
    elif catalog_fid == "rational_direct" or form == "rational_direct":
        prompt, answer, form, tech, extra = _sample_rational_direct(rng, spec)
    elif catalog_fid.startswith("direct_") or catalog_fid == "squeeze_sin_over_x":
        prompt, answer, form, tech, extra = _sample_poly_direct(
            rng, spec, force_form_id=catalog_fid or None
        )
    else:
        prompt, answer, form, tech, extra = _sample_poly_direct(rng, spec)

    snap = spec.snapshot()
    snap["form"] = form
    snap["technique"] = tech
    if "variant" in extra:
        snap["variant"] = extra["variant"]
    if "lhopital_steps" in extra:
        snap["lhopital_steps"] = extra["lhopital_steps"]
    if "indet_form" in extra:
        snap["indet_form"] = extra["indet_form"]

    # Prefer catalog form_id; fall back to openstax_form / variant / coarse form
    fid = (
        catalog_fid
        or str(extra.get("form_id") or "")
        or str(extra.get("openstax_form") or "")
        or form
    )
    meta: dict[str, Any] = {
        "generator": key,
        "variable": spec.variable,
        "d_spend": d,
        "spec_snapshot": snap,
        "effort_features": extra.get("effort_features") or {},
        "function_classes": extra.get("function_classes") or ["algebraic"],
        "shape_id": form,
        "form_id": fid,
        "openstax_form": fid,
        "catalog_id": "limits",
    }
    if catalog_form:
        meta.update({k: v for k, v in catalog_form_meta(catalog_form, lim_catalog).items() if k not in meta or k in {"openstax_case", "strategy"}})
        meta["form_id"] = fid
        meta["openstax_form"] = fid
    for k in ("approach_value", "approach_mode", "left_value", "right_value", "variant", "lhopital_steps", "lhopital_passes", "indet_form", "expr_spec_snapshot"):
        if k in extra:
            meta[k] = extra[k]

    return LimitSample(
        prompt_latex=prompt,
        answer_latex=answer,
        form=form,
        technique=tech,
        upgrades=tuple(sorted(purchased)),
        effective_d=d,
        band=band,
        metadata=meta,
    )


def sample_limit_problem(
    topic: str,
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
) -> tuple[str, str, str | None, dict[str, Any]]:
    include_answer_key = bool(settings.get("include_answer_key", False))
    key = generator_key or resolve_generator_key(topic)
    sample = sample_limit_expression(settings, generator_key=key, topic=topic)
    label = {
        "limit_direct_evaluation": "limit (direct)",
        "limit_at_infinity": "limit at infinity",
        "limit_removable": "removable discontinuity limit",
        "limit_jump": "jump discontinuity limit",
        "limit_essential": "essential discontinuity limit",
        "limit_continuity": "continuity classification",
        "lhopitals_rule": "L'Hôpital limit",
    }.get(key or "", "limit")
    answer = sample.answer_latex if include_answer_key else None
    return sample.prompt_latex, label, answer, sample.as_metadata()
