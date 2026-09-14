"""Polynomial / elementary expression sampler (Spec-driven).

Extracted from ``derivatives.py`` so derivative topics become constraint packs
on a reusable AST. Sampling owns structure; ``differentiate`` / ``render_latex``
are separate consumers.

Phase coverage:
  0 — poly atom + algebraic product / ``(inner)^n`` latex helpers
  1 — ``ExpressionSpec`` + ``ExprAST`` + packs for power / product / alg-chain
  2 — ``structure_inventory`` + ``paren_style``
  3 — elementary ``Fn`` nodes (trig / exp / log / invtrig / roots / hyperbolic)
"""

from __future__ import annotations

import random
from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Any, Literal, Sequence, Union

from packages.polynomial_core import (
    format_linear_latex,
    format_monomial_latex,
    format_polynomial_latex,
)
from question_engine.generators.utils import frac_latex

# ---------------------------------------------------------------------------
# AST
# ---------------------------------------------------------------------------

ParenStyle = Literal["minimal", "always_factors", "always_powers"]
AssocBias = Literal["left", "right", "balanced", "flat"]
ExponentKind = Literal["integer", "fractional", "irrational", "negative"]

# Named constants used as power exponents / coefficients (π, e, √2, …).
IRRATIONAL_EXPONENT_NAMES: frozenset[str] = frozenset({"pi", "e", "sqrt2", "sqrt3"})

# Default elementary classes for bare ExpressionSpec: all except hyperbolic.
# Topic/pack constructors override (power → algebraic; specialty → primary class).
DEFAULT_ALLOWED_FUNCTIONS: frozenset[str] = frozenset(
    {"trig", "exp", "log", "roots", "invtrig"}
)
ALGEBRAIC_ONLY_FUNCTIONS: frozenset[str] = frozenset()
_SYM_CONST_LATEX: dict[str, str] = {
    "pi": r"\pi",
    "e": "e",
    "sqrt2": r"\sqrt{2}",
    "sqrt3": r"\sqrt{3}",
}
_FRACTIONAL_EXPONENT_POOL: tuple[Fraction, ...] = (
    Fraction(1, 2),
    Fraction(-1, 2),
    Fraction(3, 2),
    Fraction(5, 2),
    Fraction(2, 3),
    Fraction(4, 3),
    Fraction(5, 3),
    Fraction(7, 2),
    Fraction(-3, 2),
    Fraction(1, 3),
    Fraction(4, 5),
)


@dataclass(frozen=True)
class SymConst:
    """Symbolic constant (π, e, √2, √3) used as coef or power exponent."""

    name: str  # member of IRRATIONAL_EXPONENT_NAMES


@dataclass(frozen=True)
class SymOffset:
    """Symbolic constant plus integer offset, e.g. π−1 after d/dx[u^π]."""

    sym: SymConst
    offset: int = 0


# Power exponents: integers, rationals, symbolic constants, or const±k after diff.
PowerExp = Union[int, Fraction, SymConst, SymOffset]


@dataclass(frozen=True)
class Const:
    value: int | Fraction | SymConst


@dataclass(frozen=True)
class Var:
    name: str = "x"


@dataclass(frozen=True)
class Add:
    terms: tuple["ExprAST", ...]


@dataclass(frozen=True)
class Mul:
    factors: tuple["ExprAST", ...]


@dataclass(frozen=True)
class Pow:
    base: "ExprAST"
    exp: PowerExp


@dataclass(frozen=True)
class Fn:
    """Elementary function node: sin, cos, tan, exp, ln, arcsin, …"""

    name: str
    arg: "ExprAST"


ExprAST = Union[Const, Var, Add, Mul, Pow, Fn]

FN_DERIVATIVES: dict[str, str] = {
    "sin": "cos",
    "cos": "neg_sin",  # special: -sin
    "tan": "sec2",
    "exp": "exp",
    "ln": "inv",
    "arcsin": "darcsin",
    "arccos": "darccos",
    "arctan": "darctan",
    "sinh": "cosh",
    "cosh": "sinh",
    "sqrt": "dsqrt",
}

FN_LATEX: dict[str, str] = {
    "sin": "\\sin",
    "cos": "\\cos",
    "tan": "\\tan",
    "exp": "e",
    "ln": "\\ln",
    "arcsin": "\\arcsin",
    "arccos": "\\arccos",
    "arctan": "\\arctan",
    "sinh": "\\sinh",
    "cosh": "\\cosh",
    "sqrt": "\\sqrt",
}


# ---------------------------------------------------------------------------
# Spec
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExpressionSpec:
    """Constraints for sampling one univariate expression tree."""

    variable: str = "x"

    allowed_ops: frozenset[str] = frozenset({"+", "*", "^"})
    degree_min: int = 1
    degree_max: int = 4
    term_count_min: int = 1
    term_count_max: int = 3
    coef_abs_max: int = 5
    allow_negative_coefs: bool = True
    allow_constant_term: bool = True
    require_leading: bool = True

    require_product: bool = False
    require_sum: bool = False
    require_power_of_poly: bool = False
    forbid_product: bool = False
    forbid_quotient: bool = True
    max_nesting: int = 1
    max_factors: int = 2

    # ``always_factors`` keeps the legacy name but uses the same *minimal*
    # product policy (paren a factor only when needed for precedence).
    paren_style: ParenStyle = "minimal"
    assoc_bias: AssocBias | None = None

    d_spend: float = 6.0
    seed: int | None = None

    # Phase 3+ — default: trig/exp/log/roots/invtrig ON; hyperbolic OFF.
    # Packs that must stay algebraic (power, A1 poly, removable limits) pass
    # ``ALGEBRAIC_ONLY_FUNCTIONS`` / ``frozenset()`` explicitly.
    allowed_functions: frozenset[str] = DEFAULT_ALLOWED_FUNCTIONS
    require_function: str | None = None  # force a primary class atom
    prefer_chained_fn: bool = False
    prefer_special_structure: bool = False  # bias products/chains toward Fn nodes
    min_special_nodes: int = 0  # specialty leaves: require ≥N Fn nodes when >0
    allow_rational_powers: bool = False
    allow_quotient: bool = False
    deep_chain: bool = False
    extra_term: bool = False  # denser poly / quadratic chain inner
    # Power-exponent styles for Pow(inner, c) — packs set presets; callers override
    allow_integer_exponents: bool = True
    allow_fractional_exponents: bool = False  # 3/2, 5/2, -1/2, …
    allow_irrational_exponents: bool = False  # π, e, √2, √3, …
    # Orthogonal: when True, integer/fractional pools may include negatives
    allow_negative_exponents: bool = False
    irrational_exponent_set: frozenset[str] = frozenset(
        {"pi", "e", "sqrt2", "sqrt3"}
    )
    # Richer Spec sampling (Fn powers / mixed nests / higher-order)
    mix_fn_classes: bool = False  # heterogeneous Fn∘Fn across classes
    allow_fn_power: bool = False  # Pow(Fn(...), n) e.g. tan^2(x)
    prefer_fn_power: bool = False
    derivative_order: int = 1  # 1=first; 2/3 gated by D upstream

    # Algebraic (A1/A2/PC) packs — defaults keep calc packs unchanged.
    course_tag: str = ""  # "a1" / "a2" / "pc" / "calc" (informational for ML)
    factor_count_min: int = 1  # factoring leaves / product factor budgets
    factor_count_max: int = 2
    composition_depth: int = 0  # 0=plain; ≥1 for compose/evaluate algebraic


def spec_snapshot(spec: ExpressionSpec) -> dict[str, Any]:
    """JSON-safe snapshot of ExpressionSpec fields for ML / rating join keys.

    Converts frozensets to sorted lists. Callers attach this to question
    metadata so resolved pack θ (including exponent knobs) can be regenerated
    or featurized without relying on hand-maintained bool key lists.
    """
    out: dict[str, Any] = {}
    for name, val in spec.__dict__.items():
        if isinstance(val, frozenset):
            out[name] = sorted(str(x) for x in val)
        elif isinstance(val, set):
            out[name] = sorted(str(x) for x in val)
        elif isinstance(val, (bool, int, float, str)) or val is None:
            out[name] = val
        else:
            out[name] = str(val)
    return out


def exponent_kinds(spec: ExpressionSpec) -> frozenset[str]:
    """Active exponent styles from Spec allow flags (always ≥ one kind).

    ``negative`` is orthogonal to integer/fractional/irrational — it gates
    whether those pools may include negative values.
    """
    kinds: set[str] = set()
    if spec.allow_integer_exponents:
        kinds.add("integer")
    if spec.allow_fractional_exponents:
        kinds.add("fractional")
    if spec.allow_irrational_exponents:
        kinds.add("irrational")
    if spec.allow_negative_exponents:
        kinds.add("negative")
    base = kinds - {"negative"}
    if not base:
        kinds.add("integer")
    return frozenset(kinds)


def with_exponent_kinds(
    spec: ExpressionSpec, kinds: frozenset[str] | set[str] | Sequence[str]
) -> ExpressionSpec:
    """Return Spec with allow_* exponent flags matching ``kinds``.

    Pass ``\"negative\"`` to allow negatives inside integer/fractional sampling.
    """
    k = frozenset(kinds)
    base = k & {"integer", "fractional", "irrational"}
    if not base:
        base = frozenset({"integer"})
    return replace(
        spec,
        allow_integer_exponents="integer" in base,
        allow_fractional_exponents="fractional" in base,
        allow_irrational_exponents="irrational" in base,
        allow_negative_exponents="negative" in k,
    )


def _sym_const_latex(sym: SymConst) -> str:
    return _SYM_CONST_LATEX.get(sym.name, sym.name)


def _juxtapose_coef_body(coef_s: str, body: str) -> str:
    """Join a symbolic/fraction coef onto a body without eating ``\\pi x``.

    Sums / leading-minus bodies are parenthesized so ``5`` + ``5x^{2}+…`` does
    not digit-glue into the false monomial ``55x^{2}+…``.
    """
    if not coef_s:
        return body
    if body.startswith("-") or _latex_factor_needs_paren(body):
        return rf"{coef_s}\left({body}\right)"
    # Bare control-word coefs (\pi) need a space before a letter
    if coef_s.startswith("\\") and not coef_s.endswith("}") and body[:1].isalpha():
        return f"{coef_s} {body}"
    return f"{coef_s}{body}"


def _power_exp_latex(exp: PowerExp) -> str:
    """Render a power exponent (integer / Fraction / SymConst / SymOffset)."""
    if isinstance(exp, int):
        return str(exp)
    if isinstance(exp, Fraction):
        return frac_latex(exp)
    if isinstance(exp, SymConst):
        return _sym_const_latex(exp)
    if isinstance(exp, SymOffset):
        base = _sym_const_latex(exp.sym)
        if exp.offset == 0:
            return base
        if exp.offset > 0:
            return rf"{base}+{exp.offset}"
        return rf"{base}{exp.offset}"  # e.g. \pi-1
    return str(exp)


def _exp_minus_one(exp: PowerExp) -> PowerExp:
    if isinstance(exp, int):
        return exp - 1
    if isinstance(exp, Fraction):
        return exp - Fraction(1)
    if isinstance(exp, SymConst):
        return SymOffset(exp, -1)
    if isinstance(exp, SymOffset):
        return SymOffset(exp.sym, exp.offset - 1)
    return exp


def _const_from_exp(exp: PowerExp) -> Const:
    """Coefficient factor for power rule: c in c·u^{c−1}·u'."""
    if isinstance(exp, SymOffset):
        # Rare: treat as symbolic + offset sum — prefer not as single Const
        if exp.offset == 0:
            return Const(exp.sym)
        # Fall through via Mul in caller; here only pure symbols / numbers
        return Const(exp.sym)
    if isinstance(exp, SymConst):
        return Const(exp)
    if isinstance(exp, Fraction):
        return Const(exp)
    return Const(int(exp))


def _chain_exponent_bias(d: float, kinds: frozenset[str]) -> list[str]:
    """Weighted kind list: mid/high D prefer fractional/irrational (non-expandable)."""
    pool: list[str] = []
    has_int = "integer" in kinds
    has_frac = "fractional" in kinds
    has_irr = "irrational" in kinds
    if d < 6:
        if has_int:
            pool.extend(["integer"] * 5)
        if has_frac:
            pool.append("fractional")
        if has_irr:
            pool.append("irrational")
    elif d < 10:
        if has_frac:
            pool.extend(["fractional"] * 3)
        if has_irr:
            pool.extend(["irrational"] * 2)
        if has_int:
            pool.append("integer")
    elif d < 16:
        if has_frac:
            pool.extend(["fractional"] * 3)
        if has_irr:
            pool.extend(["irrational"] * 3)
        if has_int:
            pool.append("integer")
    else:
        if has_frac:
            pool.extend(["fractional"] * 2)
        if has_irr:
            pool.extend(["irrational"] * 4)
        if has_int:
            pool.append("integer")
    return pool or (["integer"] if has_int else [k for k in kinds if k != "negative"] or ["integer"])


def _sample_power_exponent(
    spec: ExpressionSpec,
    rng: random.Random,
    *,
    for_fn_power: bool = False,
) -> PowerExp:
    """Sample Pow exponent honoring Spec exponent allow flags.

    Fn-powers (tan²) stay integer (or rare half) — irrationals reserved for
    algebraic ``(inner)^c`` chain forms that cannot be multiplied out.
    """
    kinds = exponent_kinds(spec)
    if for_fn_power:
        # Fn superscripts: integer by default; fractional only when unlocked
        if (
            spec.allow_fractional_exponents
            and spec.d_spend >= 16
            and rng.random() < 0.2
        ):
            return Fraction(1, 2)
        hi = 3 if spec.derivative_order == 1 else 2
        if spec.d_spend >= 18:
            hi = min(4, max(2, spec.degree_max)) if spec.derivative_order == 1 else 2
        return rng.randint(2, min(hi, max(2, spec.degree_max)))

    pool = _chain_exponent_bias(float(spec.d_spend), kinds)
    kind = rng.choice(pool)
    if kind == "fractional" and "fractional" in kinds:
        frac_pool = _FRACTIONAL_EXPONENT_POOL
        if not spec.allow_negative_exponents:
            frac_pool = tuple(f for f in frac_pool if f > 0)
        return rng.choice(frac_pool or _FRACTIONAL_EXPONENT_POOL)
    if kind == "irrational" and "irrational" in kinds:
        names = [
            n
            for n in sorted(spec.irrational_exponent_set & IRRATIONAL_EXPONENT_NAMES)
        ] or sorted(IRRATIONAL_EXPONENT_NAMES)
        return SymConst(rng.choice(names))
    # integer — optionally include teaching-friendly negatives
    hi = min(5, max(2, spec.degree_max))
    if spec.allow_negative_exponents:
        neg_p = 0.5 if spec.d_spend >= 6 else 0.35
        if rng.random() < neg_p:
            return -rng.randint(1, min(5, max(1, spec.degree_max)))
    return rng.randint(2, hi)


def _exponent_preset_for_chain(d: float, *, order: int = 1) -> dict[str, Any]:
    """Default exponent allow flags for algebraic / general chain packs."""
    if order >= 2:
        return {
            "allow_integer_exponents": True,
            "allow_fractional_exponents": False,
            "allow_irrational_exponents": False,
            "allow_negative_exponents": False,
        }
    return {
        "allow_integer_exponents": True,
        "allow_fractional_exponents": d >= 6.0,
        "allow_irrational_exponents": d >= 8.0,
        # Keep fractional negatives available when fractions unlock
        "allow_negative_exponents": d >= 6.0,
    }


def _exponent_preset_for_power(d: float, *, order: int = 1) -> dict[str, Any]:
    """Power-rule pack: weird exponents teach structure at modest+ / low-mid D."""
    if order >= 2:
        return {
            "allow_integer_exponents": True,
            "allow_fractional_exponents": False,
            "allow_irrational_exponents": False,
            "allow_negative_exponents": False,
        }
    return {
        "allow_integer_exponents": True,
        "allow_negative_exponents": d >= 4.0,  # low-mid: x^{-3}, 4x^{-2}
        "allow_fractional_exponents": d >= 5.0,  # modest+: x^{3/2}, x^{-1/2}
        "allow_irrational_exponents": d >= 10.0,  # optional: x^π, x^{√2}
    }


# ---------------------------------------------------------------------------
# Phase 0 latex-parity helpers (shared with derivatives façade)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PolyLatexPair:
    """Body + derivative latex with topic-fit tags (Phase 0 extract surface)."""

    body_latex: str
    deriv_latex: str
    function_classes: frozenset[str]
    methods_used: frozenset[str]
    chain_depth: int = 0


def _mono(coef: int, var: str, power: int = 1) -> str:
    return format_monomial_latex(coef, variable=var, degree=power) or (
        "0" if coef == 0 else str(coef)
    )


def _latex_factor_needs_paren(s: str) -> bool:
    """True if ``s`` needs outer parens as a juxtaposed / product factor."""
    s = s.strip()
    if not s:
        return False
    if s.startswith("-"):
        return True
    # Top-level sum: binary + / - outside braces, brackets, and \left...\right
    depth = 0
    i = 0
    while i < len(s):
        ch = s[i]
        if s.startswith(r"\left", i):
            depth += 1
            i += 5
            continue
        if s.startswith(r"\right", i):
            depth = max(0, depth - 1)
            i += 6
            continue
        if ch in "{[(":
            depth += 1
        elif ch in "}])":
            depth = max(0, depth - 1)
        elif depth == 0 and ch in "+-" and i > 0:
            return True
        i += 1
    return False


def _wrap_as_product_factor(s: str) -> str:
    """Wrap a latex factor only when it is a sum or leading-minus term."""
    if _latex_factor_needs_paren(s):
        return rf"\left({s}\right)"
    return s


def _already_wrapped_factor(s: str) -> bool:
    s = s.strip()
    return s.startswith(r"\left(") and s.endswith(r"\right)")


def _juxtapose_product_factors(parts: Sequence[str]) -> str:
    """Join product factors; paren a later factor if it starts with a digit.

    Avoids digit glue like ``3`` + ``4x^{3}`` → ``34x^{3}``, while keeping
    ``3x\\sin(x)`` and ``\\sin(3x)\\cos(2x)`` bare.
    """
    cleaned = [p for p in (p.strip() for p in parts) if p]
    if not cleaned:
        return "1"
    out = cleaned[0]
    for p in cleaned[1:]:
        if (
            not _already_wrapped_factor(p)
            and not _latex_factor_needs_paren(p)
            and p[0].isdigit()
        ):
            p = rf"\left({p}\right)"
        out += p
    return out


def _factor_ast_needs_paren(factor: ExprAST, rendered: str) -> bool:
    """AST + rendered string policy for Mul factor parentheses."""
    if isinstance(factor, Add):
        return True
    return _latex_factor_needs_paren(rendered)


def _linear_pair(rng: random.Random, coef_hi: int) -> tuple[int, int]:
    a = rng.randint(1, max(1, coef_hi))
    b = rng.choice([i for i in range(-coef_hi, coef_hi + 1) if i != 0] or [1])
    return a, b


def sample_poly_atom(
    rng: random.Random,
    var: str,
    coef_hi: int,
    power_max: int,
    *,
    extra_term: bool,
) -> PolyLatexPair:
    """Algebraic power-rule atom — latex-stable extract of former ``_atom_poly``."""
    if extra_term:
        n = rng.randint(2, min(4, power_max))
        a = rng.randint(1, max(1, min(3, coef_hi)))
        b = rng.choice([i for i in range(-coef_hi, coef_hi + 1) if i != 0] or [1])
        c = rng.randint(-coef_hi, coef_hi)
        coeffs = [a, b, c] if n == 2 else [a, b, c, rng.randint(-coef_hi, coef_hi)]
        body = format_polynomial_latex(coeffs, variable=var)
        d_coeffs = []
        deg = len(coeffs) - 1
        for i, coef in enumerate(coeffs[:-1]):
            d_coeffs.append(coef * (deg - i))
        answer = format_polynomial_latex(d_coeffs, variable=var) if any(d_coeffs) else "0"
        return PolyLatexPair(
            body, answer, frozenset({"algebraic"}), frozenset({"power", "sum"}), 0
        )
    n = rng.randint(2, min(6, power_max))
    c = rng.choice([i for i in range(-coef_hi, coef_hi + 1) if i != 0] or [1])
    if c == 1:
        body = f"{var}^{{{n}}}"
    elif c == -1:
        body = f"-{var}^{{{n}}}"
    else:
        body = f"{c}{var}^{{{n}}}"
    answer = _mono(c * n, var, n - 1) if n > 1 else str(c * n)
    return PolyLatexPair(body, answer, frozenset({"algebraic"}), frozenset({"power"}), 0)


def sample_linear_atom(rng: random.Random, var: str, coef_hi: int) -> PolyLatexPair:
    a, b = _linear_pair(rng, coef_hi)
    body = format_linear_latex(a, b, variable=var)
    return PolyLatexPair(body, str(a), frozenset({"algebraic"}), frozenset({"power"}), 0)


def compose_power(
    rng: random.Random,
    inner: PolyLatexPair,
    var: str,
    power_max: int,
) -> PolyLatexPair:
    """``(inner)^n`` — classic chain + power (OpenStax 3.6)."""
    del var  # reserved for future rational-power variants
    n = rng.randint(2, min(5, power_max))
    body = rf"\left({inner.body_latex}\right)^{{{n}}}"
    power_part = (
        rf"\left({inner.body_latex}\right)"
        if n - 1 == 1
        else rf"\left({inner.body_latex}\right)^{{{n - 1}}}"
    )
    if inner.deriv_latex == "1":
        answer = f"{n}{power_part}"
    else:
        answer = rf"{n}{power_part}\left({inner.deriv_latex}\right)"
    return PolyLatexPair(
        body,
        answer,
        inner.function_classes | frozenset({"algebraic"}),
        inner.methods_used | frozenset({"chain", "power"}),
        max(1, inner.chain_depth + 1),
    )


def product_pair(
    left: PolyLatexPair, right: PolyLatexPair, rng: random.Random
) -> PolyLatexPair:
    if rng.choice([True, False]):
        left, right = right, left
    u_b = _wrap_as_product_factor(left.body_latex)
    v_b = _wrap_as_product_factor(right.body_latex)
    u_d = _wrap_as_product_factor(left.deriv_latex)
    v_d = _wrap_as_product_factor(right.deriv_latex)
    body = _juxtapose_product_factors([u_b, v_b])
    answer = (
        f"{_juxtapose_product_factors([u_d, v_b])}"
        f"+{_juxtapose_product_factors([u_b, v_d])}"
    )
    return PolyLatexPair(
        body,
        answer,
        left.function_classes | right.function_classes,
        left.methods_used | right.methods_used | frozenset({"product"}),
        max(left.chain_depth, right.chain_depth),
    )


def quotient_pair(num: PolyLatexPair, den: PolyLatexPair) -> PolyLatexPair:
    body = rf"\frac{{{num.body_latex}}}{{{den.body_latex}}}"
    answer = (
        rf"\frac{{\left({num.deriv_latex}\right)\left({den.body_latex}\right)"
        rf"-\left({num.body_latex}\right)\left({den.deriv_latex}\right)}}"
        rf"{{\left({den.body_latex}\right)^{{2}}}}"
    )
    return PolyLatexPair(
        body,
        answer,
        num.function_classes | den.function_classes,
        num.methods_used | den.methods_used | frozenset({"quotient"}),
        max(num.chain_depth, den.chain_depth),
    )


# ---------------------------------------------------------------------------
# Packs (topic → Spec)
# ---------------------------------------------------------------------------


def pack_power_rule(
    d: float,
    *,
    coef_hi: int = 5,
    power_max: int = 4,
    extra_term: bool = False,
    allow_roots: bool = False,
    variable: str = "x",
    **overrides: Any,
) -> ExpressionSpec:
    """Power-rule pack: sums/monomials; no product/quotient; optional roots.

    At modest+ D unlocks negative / fractional / irrational exponents on
    ``k x^p`` monomials so students practice the structure ``c p x^{p-1}``.
    """
    order = max(1, int(overrides.get("derivative_order", 1) or 1))
    exp_preset = _exponent_preset_for_power(d, order=order)
    weird = (
        exp_preset["allow_negative_exponents"]
        or exp_preset["allow_fractional_exponents"]
        or exp_preset["allow_irrational_exponents"]
    )
    # Dense poly sums stay classic positive-integer; weird exponents prefer monomials
    require_sum = extra_term or (d >= 8 and not weird)
    term_max = 4 if extra_term else (3 if d >= 6 and not weird else 1)
    if weird and d >= 8 and not extra_term:
        # Occasional multi-term still allowed via term_count_max sampling bias
        term_max = 3
    # Higher-order: keep classic algebraic polys (no root / fractional leaf)
    roots_on = bool(allow_roots) and order == 1
    spec = ExpressionSpec(
        variable=variable,
        allowed_ops=frozenset({"+", "^"}),
        degree_min=2,
        degree_max=max(2, min(6, power_max)),
        term_count_min=2 if require_sum else 1,
        term_count_max=term_max,
        coef_abs_max=max(1, coef_hi),
        require_sum=require_sum,
        require_product=False,
        require_power_of_poly=False,
        forbid_product=True,
        forbid_quotient=True,
        max_nesting=0,
        paren_style="minimal",
        d_spend=d,
        allow_rational_powers=roots_on,
        extra_term=extra_term,
        # Power-rule is algebraic-primary (optional sqrt / rational powers only).
        allowed_functions=frozenset({"sqrt"}) if roots_on else ALGEBRAIC_ONLY_FUNCTIONS,
        prefer_chained_fn=False,
        prefer_special_structure=False,
        min_special_nodes=0,
        mix_fn_classes=False,
        derivative_order=order,
        **exp_preset,
    )
    return replace(spec, **{k: v for k, v in overrides.items() if hasattr(spec, k)})


def _factor_budget(d: float, *, order: int = 1) -> int:
    """Continuous-D budget for product factor count.

    Mid-D (~8–14) stays at 2 factors so product-rule answers stay tractable.
    3-factor products unlock ~D≥16; 4-factor only in the hard band (D≥20).
    Higher-order derivatives cap at 2 factors (answers explode otherwise).
    """
    if order >= 2:
        return 2
    if d < 16:
        return 2
    if d < 20:
        return 3
    if d < 40:
        return 4
    return min(6, 4 + int((d - 40) // 30))


def _nest_budget(d: float, *, deep: bool = False, order: int = 1) -> int:
    """Continuous-D budget for Fn / power nesting depth.

    Mid-D nests stay shallow; deep mixed packs reach 4 only at high D.
    Order≥2 keeps nests ≤2 so expanded answers stay within length gates.
    """
    if order >= 3:
        return 1
    if order >= 2:
        if deep and d >= 18:
            return 2
        return 1 if d < 12 else 2
    if deep:
        if d >= 40:
            return min(5, 4 + int((d - 40) // 40))
        if d >= 18:
            return 4
        if d >= 12:
            return 3
        if d >= 8:
            return 2
        return 1
    if d >= 18:
        return 3
    if d >= 12:
        return 2
    if d >= 4:
        return 1
    return 0


def _answer_len_budget(d: float, *, order: int = 1) -> int:
    """Soft cap on rendered derivative latex length for resample gating."""
    base = 80 + int(max(0.0, d) * 10)
    if order >= 3:
        base = int(base * 1.45)
    elif order >= 2:
        # Slightly tighter than before — order=2 must use simpler bases
        base = int(base * 1.2)
    return max(120, min(900, base))


def _count_fn_powers(expr: ExprAST) -> int:
    if isinstance(expr, Pow) and isinstance(expr.base, Fn):
        return 1 + _count_fn_powers(expr.base.arg)
    if isinstance(expr, Fn):
        return _count_fn_powers(expr.arg)
    if isinstance(expr, Add):
        return sum(_count_fn_powers(t) for t in expr.terms)
    if isinstance(expr, Mul):
        return sum(_count_fn_powers(f) for f in expr.factors)
    if isinstance(expr, Pow):
        return _count_fn_powers(expr.base)
    return 0


def _has_canceling_exp_ln(expr: ExprAST) -> bool:
    """True when expr contains exp∘ln or ln∘exp (algebraically canceling)."""
    if isinstance(expr, Fn):
        if isinstance(expr.arg, Fn):
            pair = (expr.name, expr.arg.name)
            if pair in {("exp", "ln"), ("ln", "exp")}:
                return True
        return _has_canceling_exp_ln(expr.arg)
    if isinstance(expr, Add):
        return any(_has_canceling_exp_ln(t) for t in expr.terms)
    if isinstance(expr, Mul):
        return any(_has_canceling_exp_ln(f) for f in expr.factors)
    if isinstance(expr, Pow):
        return _has_canceling_exp_ln(expr.base)
    return False


def _complexity_ok_for_d(expr: ExprAST, spec: ExpressionSpec) -> bool:
    """Reject samples that are trivial cancels or too heavy for ``d_spend``."""
    d = float(spec.d_spend)
    order = max(1, int(spec.derivative_order or 1))
    if _has_canceling_exp_ln(expr):
        return False
    n_factors = len(expr.factors) if isinstance(expr, Mul) else 1
    n_fn_pow = _count_fn_powers(expr)
    nest = _nest_depth(expr)
    # Higher-order: only "2nd-deriv safe" shapes (simple base, short product, shallow nest)
    if order >= 2:
        if n_factors > 2:
            return False
        if nest > (2 if order == 2 else 1):
            return False
        if n_fn_pow >= 2:
            return False
        if n_factors >= 2 and (n_fn_pow >= 1 or nest >= 2):
            return False
        if nest >= 2 and n_fn_pow >= 1:
            return False
        return True
    # Mid-D: no 3–4 factor products; limit Fn-powers stacked into products
    if d < 16 and n_factors > 2:
        return False
    # D=12: reject 4× heavy powers / 3-factor of powered Fns
    if d < 18 and n_factors >= 3 and n_fn_pow >= 2:
        return False
    if d < 14 and n_fn_pow >= 2 and n_factors >= 2:
        return False
    if d < 12 and nest > 2:
        return False
    if d < 16 and nest > 3:
        return False
    # D=18–25: richer products+powers ok, but not every factor heavily powered
    if d < 22 and n_factors >= 4 and n_fn_pow >= 3:
        return False
    return True


def pack_product_rule(
    d: float,
    *,
    coef_hi: int = 5,
    power_max: int = 4,
    extra_term: bool = False,
    variable: str = "x",
    allowed_functions: frozenset[str] | None = None,
    prefer_chained_fn: bool = False,
    require_function: str | None = None,
    prefer_special_structure: bool = False,
    **overrides: Any,
) -> ExpressionSpec:
    fns = allowed_functions or frozenset()
    special_bias = prefer_special_structure or bool(require_function)
    order = max(1, int(overrides.get("derivative_order", 1) or 1))
    max_f = (
        _factor_budget(d, order=order)
        if (fns or special_bias)
        else (2 if order >= 2 else (3 if d >= 12 else 2))
    )
    fn_power = bool(fns) and d >= 6 and order <= 2
    spec = ExpressionSpec(
        variable=variable,
        allowed_ops=frozenset({"+", "*", "^"}),
        degree_min=1,
        degree_max=max(1, min(4, power_max)),
        term_count_min=1,
        term_count_max=3 if extra_term and order == 1 else 2,
        coef_abs_max=max(1, coef_hi),
        require_product=True,
        forbid_product=False,
        forbid_quotient=True,
        max_factors=max_f,
        max_nesting=(
            _nest_budget(d, order=order)
            if prefer_chained_fn
            else (1 if fns and order == 1 else 0)
        ),
        paren_style="minimal",
        d_spend=d,
        extra_term=extra_term and order == 1,
        allowed_functions=fns,
        require_function=require_function,
        prefer_chained_fn=prefer_chained_fn,
        prefer_special_structure=special_bias,
        min_special_nodes=(
            1
            if order >= 2
            else (max(2, max_f - 1) if special_bias and d >= 10 else (1 if special_bias else 0))
        ),
        allow_fn_power=fn_power,
        prefer_fn_power=fn_power and d >= 12 and order == 1,
        derivative_order=order,
    )
    return replace(spec, **{k: v for k, v in overrides.items() if hasattr(spec, k)})


def pack_algebraic_chain(
    d: float,
    *,
    coef_hi: int = 5,
    power_max: int = 4,
    extra_term: bool = False,
    deep_chain: bool = False,
    variable: str = "x",
    allowed_functions: frozenset[str] | None = None,
    prefer_chained_fn: bool = False,
    require_function: str | None = None,
    prefer_special_structure: bool = False,
    **overrides: Any,
) -> ExpressionSpec:
    fns = allowed_functions or frozenset()
    special_bias = prefer_special_structure or bool(require_function) or bool(fns)
    order = max(1, int(overrides.get("derivative_order", 1) or 1))
    nest = _nest_budget(d, deep=deep_chain and order == 1, order=order)
    if special_bias and nest < 1:
        nest = 1
    # Specials unlock product factors inside chain-rule leaves (sin·cos·…)
    allow_prod = special_bias and d >= 8 and order <= 2
    fn_power = bool(fns) and d >= 6 and order <= 2
    mix = bool(fns) and len(fns) >= 2 and d >= 10 and order == 1
    exp_preset = _exponent_preset_for_chain(d, order=order)
    spec = ExpressionSpec(
        variable=variable,
        allowed_ops=frozenset({"+", "*", "^"}) if allow_prod else frozenset({"+", "^"}),
        degree_min=1,
        degree_max=max(1, min(5, power_max)),
        term_count_min=1,
        term_count_max=3 if extra_term and order == 1 else 2,
        coef_abs_max=max(1, coef_hi),
        require_power_of_poly=not (special_bias and d >= 10),
        forbid_product=not allow_prod,
        forbid_quotient=True,
        max_factors=_factor_budget(d, order=order) if allow_prod else 2,
        max_nesting=max(nest, 2 if deep_chain and order == 1 else nest),
        paren_style="always_powers" if not special_bias else "minimal",
        d_spend=d,
        extra_term=extra_term and order == 1,
        deep_chain=deep_chain and order == 1,
        allowed_functions=fns,
        prefer_chained_fn=prefer_chained_fn or special_bias,
        prefer_special_structure=special_bias,
        require_function=require_function,
        min_special_nodes=(
            1
            if order >= 2
            else (min(nest + 1, 5) if special_bias and d >= 12 else (1 if special_bias else 0))
        ),
        mix_fn_classes=mix or (deep_chain and len(fns) >= 2 and order == 1),
        allow_fn_power=fn_power,
        prefer_fn_power=fn_power and (d >= 10 or order >= 2),
        derivative_order=order,
        **exp_preset,
    )
    return replace(spec, **{k: v for k, v in overrides.items() if hasattr(spec, k)})


def pack_special_atom(
    d: float,
    *,
    primary: str,
    coef_hi: int = 5,
    power_max: int = 4,
    prefer_chained_fn: bool = False,
    variable: str = "x",
    allowed_functions: frozenset[str] | None = None,
    **overrides: Any,
) -> ExpressionSpec:
    """Trig / ln-exp / invtrig: special-heavy products, Fn-powers & nested chains.

    Topic-primary: ``allowed_functions`` should already be restricted to the
    specialty class(es); mix is only within that set (e.g. log+exp).
    Hardness mixes products + Pow(Fn,n) + modest nests — not nest-depth alone.
    """
    fns = allowed_functions or frozenset({primary})
    order = max(1, int(overrides.get("derivative_order", 1) or 1))
    primary_cls = _fn_token_class(primary)
    max_f = _factor_budget(d, order=order)
    nest = _nest_budget(d, deep=d >= 18 and order == 1, order=order)
    if prefer_chained_fn and nest < 1:
        nest = 1
    # Low D: single special atom; mid+: products / nested compositions of specials
    multi = d >= 6.0 and order <= 2
    high = d >= 16.0
    # Unlock Fn-powers early (esp. invtrig arcsin² / arctan³)
    fn_power = d >= 6.0 and order <= 2
    prefer_power = fn_power and (
        primary_cls == "invtrig"
        or order >= 2
        or d >= 10
    )
    # min_special_nodes: don't force 3–4 Fn nodes (that starved products via length gate)
    if order >= 2:
        min_special = 1
    elif high:
        # 2 specials is enough for product interest; 3-factor unlocks via max_factors
        min_special = 2
    elif d >= 10:
        min_special = 2
    elif multi:
        min_special = 1
    else:
        min_special = 1
    spec = ExpressionSpec(
        variable=variable,
        allowed_ops=frozenset({"+", "*", "^"}) if multi else frozenset({"+", "^"}),
        degree_min=1,
        degree_max=max(1, min(4, power_max)),
        coef_abs_max=max(1, coef_hi),
        require_product=False,
        require_power_of_poly=False,
        forbid_product=not multi,
        forbid_quotient=True,
        max_factors=max_f if multi else 2,
        max_nesting=max(nest, 1 if prefer_chained_fn or multi else 0),
        paren_style="minimal",
        d_spend=d,
        allowed_functions=fns,
        require_function=primary,
        prefer_chained_fn=prefer_chained_fn or multi,
        prefer_special_structure=True,
        min_special_nodes=min_special,
        deep_chain=d >= 18 and order == 1,
        mix_fn_classes=len(fns) >= 2 and d >= 10 and order == 1,
        allow_fn_power=fn_power,
        prefer_fn_power=prefer_power,
        derivative_order=order,
    )
    return replace(spec, **{k: v for k, v in overrides.items() if hasattr(spec, k)})


def pack_general_derivatives(
    d: float,
    *,
    coef_hi: int = 5,
    power_max: int = 4,
    extra_term: bool = False,
    deep_chain: bool = False,
    variable: str = "x",
    allowed_functions: frozenset[str] | None = None,
    allow_product: bool = True,
    allow_fn_power: bool = False,
    mix_fn_classes: bool = True,
    derivative_order: int = 1,
    **overrides: Any,
) -> ExpressionSpec:
    """General derivatives pack: all unlocked classes/methods under allow + D.

    Unlike specialty leaves, this does not force a primary function class.
    Settings / upstream routing turn classes and methods on or off.
    """
    fns = allowed_functions or frozenset()
    order = max(1, int(derivative_order))
    nest = _nest_budget(
        d,
        deep=deep_chain or (mix_fn_classes and d >= 12 and order == 1),
        order=order,
    )
    if fns and nest < 1:
        nest = 1
    allow_prod = allow_product and d >= 6 and order <= 2
    # Higher-order: simpler inners; still allow a single Fn-power (arctan²)
    if order >= 2:
        max_f = 2
        fn_power = bool(allow_fn_power and d >= 6)
    else:
        max_f = _factor_budget(d, order=order) if allow_prod else 2
        fn_power = bool(allow_fn_power and d >= 6)
    # Exponent styles default integer-only; opt in via overrides / settings.
    spec = ExpressionSpec(
        variable=variable,
        allowed_ops=frozenset({"+", "*", "^"}) if allow_prod else frozenset({"+", "^"}),
        degree_min=1,
        degree_max=max(1, min(5, power_max)),
        term_count_min=1,
        term_count_max=3 if extra_term and order == 1 else 2,
        coef_abs_max=max(1, coef_hi),
        require_product=False,
        require_power_of_poly=False,
        forbid_product=not allow_prod,
        forbid_quotient=True,
        max_factors=max_f,
        max_nesting=max(nest, 1 if fns else 0),
        paren_style="minimal",
        d_spend=d,
        extra_term=extra_term and order == 1,
        deep_chain=deep_chain and order == 1,
        allowed_functions=fns,
        prefer_chained_fn=bool(fns),
        prefer_special_structure=bool(fns),
        require_function=None,
        min_special_nodes=(2 if fns and d >= 10 and order == 1 else (1 if fns else 0)),
        mix_fn_classes=mix_fn_classes and len(fns) >= 2 and order == 1,
        allow_fn_power=fn_power,
        prefer_fn_power=fn_power and (d >= 10 or order >= 2),
        derivative_order=order,
        allow_integer_exponents=True,
        allow_fractional_exponents=False,
        allow_irrational_exponents=False,
    )
    return replace(spec, **{k: v for k, v in overrides.items() if hasattr(spec, k)})


# ---------------------------------------------------------------------------
# Algebraic packs (A1 / A2 / PC — expand / product / compose; no differentiation)
# ---------------------------------------------------------------------------


def pack_poly_expand(
    d: float,
    *,
    coef_hi: int = 5,
    power_max: int = 4,
    variable: str = "x",
    course_tag: str = "a1",
    **overrides: Any,
) -> ExpressionSpec:
    """Expand/simplify pack: poly sums with optional distribute-style products.

    Sampling-only (no differentiate). Continuous D grows degree / term count /
    nesting the same way power-rule packs do for calc.
    """
    d = max(0.0, float(d))
    deg_max = max(1, min(6, power_max if d < 8 else max(power_max, 3 + int(d // 6))))
    term_max = 2 if d < 4 else (3 if d < 10 else min(5, 3 + int((d - 10) // 5)))
    nest = 0 if d < 6 else (1 if d < 14 else 2)
    require_prod = d >= 5.0
    spec = ExpressionSpec(
        variable=variable,
        allowed_ops=frozenset({"+", "*", "^"}),
        degree_min=1 if d < 4 else 2,
        degree_max=deg_max,
        term_count_min=2 if d >= 2 else 1,
        term_count_max=term_max,
        coef_abs_max=max(1, coef_hi if d < 10 else min(12, coef_hi + int(d // 4))),
        allow_negative_coefs=d >= 3.0,
        require_sum=d >= 2.0,
        require_product=require_prod,
        forbid_product=not require_prod,
        forbid_quotient=True,
        max_nesting=nest,
        max_factors=2 if d < 12 else 3,
        paren_style="minimal",
        d_spend=d,
        derivative_order=1,
        course_tag=course_tag,
        composition_depth=0,
        allowed_functions=ALGEBRAIC_ONLY_FUNCTIONS,
        allow_integer_exponents=True,
        allow_fractional_exponents=False,
        allow_irrational_exponents=False,
        allow_negative_exponents=False,
    )
    return replace(spec, **{k: v for k, v in overrides.items() if hasattr(spec, k)})


def pack_poly_product(
    d: float,
    *,
    coef_hi: int = 5,
    power_max: int = 3,
    variable: str = "x",
    course_tag: str = "a1",
    special: bool = False,
    **overrides: Any,
) -> ExpressionSpec:
    """Polynomial multiply / FOIL pack (forced product of poly factors)."""
    d = max(0.0, float(d))
    n_factors = 2 if d < 14 else (3 if d < 22 else 4)
    deg = 1 if d < 4 else (2 if d < 12 else min(3, power_max))
    if special:
        # Difference of squares / perfect-square trinomial style: 2 linear factors.
        n_factors = 2
        deg = 1
    spec = ExpressionSpec(
        variable=variable,
        allowed_ops=frozenset({"+", "*", "^"}),
        degree_min=1,
        degree_max=max(1, deg),
        term_count_min=1,
        term_count_max=2 if d < 8 else 3,
        coef_abs_max=max(1, coef_hi if d < 10 else min(10, coef_hi + int(d // 5))),
        allow_negative_coefs=d >= 2.0 or special,
        require_product=True,
        require_sum=False,
        forbid_product=False,
        forbid_quotient=True,
        max_factors=n_factors,
        max_nesting=0 if d < 10 else 1,
        paren_style="minimal",
        d_spend=d,
        derivative_order=1,
        course_tag=course_tag,
        factor_count_min=2,
        factor_count_max=n_factors,
        allowed_functions=ALGEBRAIC_ONLY_FUNCTIONS,
        allow_integer_exponents=True,
    )
    return replace(spec, **{k: v for k, v in overrides.items() if hasattr(spec, k)})


def pack_poly_factor(
    d: float,
    *,
    coef_hi: int = 5,
    variable: str = "x",
    course_tag: str = "a1",
    **overrides: Any,
) -> ExpressionSpec:
    """Factoring-oriented Spec snapshot (quadratic / GCF / grouping knobs).

    Does not replace ``factor_poly`` sampling — provides joinable Spec θ for ML
    when generators stamp ``spec_snapshot(pack_poly_factor(...))``.
    """
    d = max(0.0, float(d))
    nonmonic = d >= 8.0
    n_fac = 2 if d < 12 else 3
    spec = ExpressionSpec(
        variable=variable,
        allowed_ops=frozenset({"+", "*", "^"}),
        degree_min=2,
        degree_max=2 if d < 14 else min(4, 2 + int((d - 14) // 6)),
        term_count_min=2,
        term_count_max=3 if d < 10 else 4,
        coef_abs_max=max(1, min(9, coef_hi if not nonmonic else coef_hi + 2)),
        allow_negative_coefs=d >= 3.0,
        require_product=True,
        forbid_quotient=True,
        max_factors=n_fac,
        max_nesting=0,
        paren_style="minimal",
        d_spend=d,
        derivative_order=1,
        course_tag=course_tag,
        factor_count_min=2,
        factor_count_max=n_fac,
        allowed_functions=ALGEBRAIC_ONLY_FUNCTIONS,
    )
    return replace(spec, **{k: v for k, v in overrides.items() if hasattr(spec, k)})


def pack_compose_algebraic(
    d: float,
    *,
    coef_hi: int = 4,
    power_max: int = 2,
    variable: str = "x",
    course_tag: str = "pc",
    **overrides: Any,
) -> ExpressionSpec:
    """Function compose / evaluate algebraic — nested poly/power inners."""
    d = max(0.0, float(d))
    depth = 1 if d < 8 else (2 if d < 16 else 3)
    spec = ExpressionSpec(
        variable=variable,
        allowed_ops=frozenset({"+", "*", "^"}),
        degree_min=1,
        degree_max=max(1, min(4, power_max if d < 10 else power_max + 1)),
        term_count_min=1,
        term_count_max=2 if d < 10 else 3,
        coef_abs_max=max(1, coef_hi),
        allow_negative_coefs=True,
        require_sum=d >= 4.0,
        require_product=d >= 8.0,
        forbid_quotient=True,
        max_nesting=depth,
        max_factors=2,
        paren_style="minimal",
        d_spend=d,
        derivative_order=1,
        course_tag=course_tag,
        composition_depth=depth,
        allowed_functions=ALGEBRAIC_ONLY_FUNCTIONS,
        allow_integer_exponents=True,
    )
    return replace(spec, **{k: v for k, v in overrides.items() if hasattr(spec, k)})


def pack_limit_direct(
    d: float,
    *,
    coef_hi: int = 5,
    variable: str = "x",
    allowed_functions: frozenset[str] | None = None,
    **overrides: Any,
) -> ExpressionSpec:
    """Limit direct-eval pack — OpenStax 2.3 continuous plug-in shapes.

    Defaults to ``DEFAULT_ALLOWED_FUNCTIONS`` (no hyperbolic). Removable /
    power packs must not use this; they pass algebraic-only elsewhere.
    """
    fns = (
        DEFAULT_ALLOWED_FUNCTIONS
        if allowed_functions is None
        else frozenset(allowed_functions) - {"hyperbolic"}
    )
    nest = 1 if d < 10 else (2 if d < 16 else 3)
    allow_prod = d >= 8 and bool(fns)
    spec = ExpressionSpec(
        variable=variable,
        allowed_ops=frozenset({"+", "*", "^"}) if allow_prod else frozenset({"+", "^"}),
        degree_min=1,
        degree_max=max(1, min(4, 2 + int(d // 6))),
        term_count_min=1,
        term_count_max=2 if d < 10 else 3,
        coef_abs_max=max(1, coef_hi),
        require_sum=d >= 6,
        forbid_product=not allow_prod,
        forbid_quotient=True,
        max_nesting=nest if fns else 0,
        max_factors=2,
        paren_style="minimal",
        d_spend=d,
        allowed_functions=fns,
        prefer_chained_fn=bool(fns),
        prefer_special_structure=bool(fns) and d >= 5,
        mix_fn_classes=len(fns) >= 2 and d >= 8,
        min_special_nodes=1 if fns and d >= 5 else 0,
        derivative_order=1,
        course_tag="calc",
    )
    return replace(spec, **{k: v for k, v in overrides.items() if hasattr(spec, k)})


# ---------------------------------------------------------------------------
# Sampling helpers (AST)
# ---------------------------------------------------------------------------


def _nz_coef(rng: random.Random, hi: int, *, allow_neg: bool = True) -> int:
    hi = max(1, hi)
    if allow_neg:
        choices = [i for i in range(-hi, hi + 1) if i != 0]
    else:
        choices = list(range(1, hi + 1))
    return rng.choice(choices or [1])


def _sample_monomial(spec: ExpressionSpec, rng: random.Random) -> ExprAST:
    var = Var(spec.variable)
    kinds = exponent_kinds(spec)
    rich = bool(kinds & {"fractional", "irrational"}) or spec.allow_negative_exponents
    if rich and (
        bool(kinds & {"fractional", "irrational"})
        or rng.random() < (0.6 if spec.d_spend >= 6 else 0.55)
    ):
        deg: PowerExp = _sample_power_exponent(spec, rng, for_fn_power=False)
    else:
        deg = rng.randint(max(1, spec.degree_min), max(spec.degree_min, spec.degree_max))
    coef = _nz_coef(rng, spec.coef_abs_max, allow_neg=spec.allow_negative_coefs)
    if isinstance(deg, int) and deg == 1:
        powered: ExprAST = var
    elif isinstance(deg, int) and deg == 0:
        return Const(coef)
    else:
        powered = Pow(var, deg)
    if coef == 1:
        return powered
    if coef == -1:
        return Mul((Const(-1), powered))
    return Mul((Const(coef), powered))


def _prefer_weird_power_monomial(spec: ExpressionSpec, rng: random.Random) -> bool:
    """Bias power-rule packs toward ``k x^p`` with weird p when unlocked."""
    if spec.require_power_of_poly or spec.require_product:
        return False
    kinds = exponent_kinds(spec)
    exotic = bool(kinds & {"fractional", "irrational"}) or spec.allow_negative_exponents
    if not exotic:
        return False
    if spec.extra_term and rng.random() < 0.35:
        return False
    p = 0.75 if spec.d_spend >= 8 else (0.55 if spec.d_spend >= 5 else 0.4)
    return rng.random() < p


def _sample_poly_sum(spec: ExpressionSpec, rng: random.Random) -> ExprAST:
    n_terms = rng.randint(
        max(1, spec.term_count_min),
        max(spec.term_count_min, spec.term_count_max),
    )
    if n_terms == 1 and not spec.require_sum:
        return _sample_monomial(spec, rng)
    # Dense leading-first poly (matches former extra_term atom)
    deg = rng.randint(2, min(4, spec.degree_max))
    a = rng.randint(1, max(1, min(3, spec.coef_abs_max)))
    b = _nz_coef(rng, spec.coef_abs_max)
    c = rng.randint(-spec.coef_abs_max, spec.coef_abs_max) if spec.allow_constant_term else 0
    coeffs = [a, b, c] if deg == 2 else [a, b, c, rng.randint(-spec.coef_abs_max, spec.coef_abs_max)]
    return _coeffs_to_ast(coeffs, spec.variable)


def _coeffs_to_ast(coeffs: Sequence[int], var: str) -> ExprAST:
    """Highest-degree-first coefficient list → Add of monomials."""
    terms: list[ExprAST] = []
    degree = len(coeffs) - 1
    for i, coef in enumerate(coeffs):
        if coef == 0:
            continue
        power = degree - i
        if power == 0:
            terms.append(Const(coef))
        elif power == 1:
            if coef == 1:
                terms.append(Var(var))
            elif coef == -1:
                terms.append(Mul((Const(-1), Var(var))))
            else:
                terms.append(Mul((Const(coef), Var(var))))
        else:
            powered = Pow(Var(var), power)
            if coef == 1:
                terms.append(powered)
            elif coef == -1:
                terms.append(Mul((Const(-1), powered)))
            else:
                terms.append(Mul((Const(coef), powered)))
    if not terms:
        return Const(0)
    if len(terms) == 1:
        return terms[0]
    return Add(tuple(terms))


def _sample_linear(spec: ExpressionSpec, rng: random.Random) -> ExprAST:
    a, b = _linear_pair(rng, spec.coef_abs_max)
    return _coeffs_to_ast([a, b], spec.variable)


def sample_linear_expr(spec: ExpressionSpec, rng: random.Random) -> ExprAST:
    """Public Spec linear ``ax+b`` sampler (complexity_wrap / dress helpers)."""
    return _sample_linear(spec, rng)


def sample_scale_coef(spec: ExpressionSpec, rng: random.Random) -> int:
    """Nonzero integer coef from Spec (optionally signed)."""
    return _nz_coef(
        rng,
        max(1, int(spec.coef_abs_max)),
        allow_neg=bool(spec.allow_negative_coefs),
    )


def _sample_quadratic_inner(spec: ExpressionSpec, rng: random.Random) -> ExprAST:
    a = rng.randint(1, max(1, min(3, spec.coef_abs_max)))
    c = _nz_coef(rng, spec.coef_abs_max)
    return _coeffs_to_ast([a, 0, c], spec.variable)


def _sample_fn_atom(spec: ExpressionSpec, rng: random.Random, name: str) -> ExprAST:
    """Single elementary Fn with affine/linear or bare-var argument (poly as arg OK)."""
    chained = spec.prefer_chained_fn or spec.max_nesting >= 1
    var = Var(spec.variable)
    if name == "exp":
        if chained:
            return Fn("exp", _sample_linear(spec, rng))
        return Fn("exp", var)
    if name == "ln":
        if chained:
            return Fn("ln", _sample_linear(spec, rng))
        return Fn("ln", var)
    if name == "sqrt":
        if chained:
            a = rng.choice([1, 4, 9])
            b = rng.randint(0, max(1, spec.coef_abs_max))
            inner = _coeffs_to_ast([a, b], spec.variable) if b else Mul((Const(a), var)) if a != 1 else var
            return Fn("sqrt", inner)
        # rational power x^{p/q} — only when fractional exponents are unlocked
        if spec.allow_fractional_exponents:
            pool = [(1, 2), (3, 2), (2, 3)]
            if spec.allow_negative_exponents:
                pool = pool + [(-1, 2), (-3, 2)]
            p, q = rng.choice(pool)
            return Pow(var, Fraction(p, q))
        return Fn("sqrt", var)
        if chained:
            k = rng.randint(2, max(2, min(5, spec.coef_abs_max)))
            return Fn(name, Mul((Const(k), var)))
        return Fn(name, var)
    if name in {"sin", "cos", "tan", "sinh", "cosh"}:
        if chained:
            k = rng.randint(2, max(2, spec.coef_abs_max))
            return Fn(name, Mul((Const(k), var)))
        return Fn(name, var)
    return Fn(name, var)


def _resolve_fn_alias(raw: str, rng: random.Random) -> str:
    """Map class tokens (trig / log / invtrig / …) to concrete Fn names."""
    alias = {
        "trig": lambda: rng.choice(["sin", "cos", "tan"]),
        "exp": lambda: "exp",
        "log": lambda: "ln",
        "invtrig": lambda: rng.choice(["arcsin", "arccos", "arctan"]),
        "hyperbolic": lambda: rng.choice(["sinh", "cosh"]),
        "roots": lambda: "sqrt",
    }
    fn = alias.get(raw)
    return fn() if fn is not None else raw


def _fn_token_class(raw: str) -> str:
    """Map concrete Fn name or class token → coarse class label."""
    if raw in {"sin", "cos", "tan", "trig"}:
        return "trig"
    if raw in {"exp"}:
        return "exp"
    if raw in {"ln", "log"}:
        return "log"
    if raw in {"arcsin", "arccos", "arctan", "invtrig"}:
        return "invtrig"
    if raw in {"sinh", "cosh", "hyperbolic"}:
        return "hyperbolic"
    if raw in {"sqrt", "roots"}:
        return "roots"
    return raw


def _expand_fn_tokens(fns: frozenset[str] | set[str]) -> list[str]:
    """Expand class tokens into concrete sampler choices (class tokens preferred).

    Iterate a sorted view so PYTHONHASHSEED cannot reshuffle frozenset order
    across processes (breaks seed-stable regeneration for ratings / ML join).
    """
    out: list[str] = []
    for f in sorted(fns):
        if f in {"trig", "exp", "log", "invtrig", "hyperbolic", "roots", "sqrt"}:
            out.append("roots" if f == "sqrt" else f)
        elif f in {"sin", "cos", "tan"}:
            out.append("trig")
        elif f == "ln":
            out.append("log")
        elif f in {"arcsin", "arccos", "arctan"}:
            out.append("invtrig")
        elif f in {"sinh", "cosh"}:
            out.append("hyperbolic")
        else:
            out.append(f)
    # unique preserve order
    seen: set[str] = set()
    uniq: list[str] = []
    for t in out:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq


def _pick_fn_name(
    spec: ExpressionSpec,
    rng: random.Random,
    *,
    avoid_class: str | None = None,
) -> str | None:
    """Pick a concrete Fn name; with mix_fn_classes, draw across allowed classes."""
    tokens = _expand_fn_tokens(spec.allowed_functions or frozenset())
    if spec.mix_fn_classes and tokens:
        pool = [t for t in tokens if _fn_token_class(t) != avoid_class] or tokens
        # Specialty bias: still prefer primary class most of the time
        if spec.require_function and rng.random() < 0.55:
            primary = _fn_token_class(spec.require_function)
            if primary in pool or any(_fn_token_class(t) == primary for t in pool):
                return _resolve_fn_alias(spec.require_function, rng)
        raw = rng.choice(pool)
        return _resolve_fn_alias(raw, rng)
    if spec.require_function:
        # Still vary concrete names within the required class
        return _resolve_fn_alias(spec.require_function, rng)
    if not tokens:
        return None
    raw = rng.choice(tokens)
    return _resolve_fn_alias(raw, rng)


def _count_fn_nodes(expr: ExprAST) -> int:
    if isinstance(expr, Fn):
        return 1 + _count_fn_nodes(expr.arg)
    if isinstance(expr, Add):
        return sum(_count_fn_nodes(t) for t in expr.terms)
    if isinstance(expr, Mul):
        return sum(_count_fn_nodes(f) for f in expr.factors)
    if isinstance(expr, Pow):
        return _count_fn_nodes(expr.base)
    return 0


def _affine_inner(spec: ExpressionSpec, rng: random.Random) -> ExprAST:
    """Linear/affine poly used as Fn argument — not a free poly body."""
    if rng.random() < 0.55:
        k = rng.randint(2, max(2, spec.coef_abs_max))
        return Mul((Const(k), Var(spec.variable)))
    return _sample_linear(spec, rng)


_FN_POWER_OK = frozenset(
    {
        "sin",
        "cos",
        "tan",
        "ln",
        "arcsin",
        "arccos",
        "arctan",
        "sinh",
        "cosh",
    }
)


def _maybe_fn_power(spec: ExpressionSpec, rng: random.Random, fn_expr: ExprAST) -> ExprAST:
    """Optionally wrap Fn(...) as Pow(Fn(...), n) when allow_fn_power is on."""
    if not spec.allow_fn_power or not isinstance(fn_expr, Fn):
        return fn_expr
    if fn_expr.name not in _FN_POWER_OK:
        return fn_expr
    # Higher-order: only wrap when prefer_fn_power (safer 2nd-deriv bases)
    if spec.derivative_order >= 2 and not spec.prefer_fn_power:
        return fn_expr
    prefer = spec.prefer_fn_power or spec.d_spend >= 10
    # Invtrig / preferred: lean hard into powers
    if fn_expr.name in {"arcsin", "arccos", "arctan"}:
        p = 0.7 if prefer else 0.4
    else:
        p = 0.55 if prefer else 0.28
    if rng.random() >= p:
        return fn_expr
    # Integer / rare half via Spec exponent flags
    return Pow(fn_expr, _sample_power_exponent(spec, rng, for_fn_power=True))


def _sample_fn_power(spec: ExpressionSpec, rng: random.Random) -> ExprAST:
    """First-class Pow(Fn(arg), n) — tan^2(x), arcsin^3(3x), (ln x)^2."""
    name = _pick_fn_name(spec, rng) or _resolve_fn_alias(
        spec.require_function or "sin", rng
    )
    if name not in _FN_POWER_OK:
        # Stay topic-primary — never fall back to trig from an ln/exp leaf
        primary_tok = spec.require_function
        primary_cls = _fn_token_class(primary_tok) if primary_tok else None
        allowed = _expand_fn_tokens(spec.allowed_functions or frozenset())
        if primary_cls == "invtrig" or any(
            _fn_token_class(t) == "invtrig" for t in allowed
        ):
            name = rng.choice(["arcsin", "arccos", "arctan"])
        elif primary_cls in {"log", "exp"} or any(
            _fn_token_class(t) in {"log", "exp"} for t in allowed
        ):
            name = "ln"
        elif primary_cls == "trig" or any(_fn_token_class(t) == "trig" for t in allowed):
            name = rng.choice(["sin", "cos", "tan"])
        elif primary_tok:
            resolved = _resolve_fn_alias(primary_tok, rng)
            name = resolved if resolved in _FN_POWER_OK else "ln"
        else:
            name = "ln"
    # Prefer simpler affine / bare-var args so power-of-fn stays readable
    # Invtrig + higher-order: always modest args (kx / x)
    simple_arg = (
        spec.derivative_order > 1
        or name in {"arcsin", "arccos", "arctan"}
        or rng.random() < 0.55
    )
    if simple_arg:
        arg: ExprAST = Var(spec.variable)
        if rng.random() < 0.65:
            k = rng.randint(2, max(2, min(5, spec.coef_abs_max)))
            arg = Mul((Const(k), Var(spec.variable)))
    else:
        arg = _affine_inner(spec, rng)
    fn_expr = Fn(name, arg)
    return Pow(fn_expr, _sample_power_exponent(spec, rng, for_fn_power=True))


def _sample_fn_nest(
    spec: ExpressionSpec, rng: random.Random, *, depth: int | None = None
) -> ExprAST:
    """Nested compositions Fn∘Fn∘…∘(affine); mixed classes when mix_fn_classes."""
    depth = depth if depth is not None else max(1, spec.max_nesting)
    # Cap at 4 Fn layers — keeps D≈20–25 readable; deep mixed chains still fit
    depth = max(1, min(depth, 4))
    # Higher-order: keep inners simple
    if spec.derivative_order >= 2:
        depth = min(depth, 2 if spec.derivative_order == 2 else 1)
        inner: ExprAST = Var(spec.variable)
        if rng.random() < 0.5:
            inner = _affine_inner(spec, rng)
    else:
        # Occasional power-of-var innermost for spice: arctan(x^2)
        # Use rarer + shallower when depth is already high so nest_depth stays ≤5
        if rng.random() < (0.15 if depth >= 3 else 0.25) and spec.d_spend >= 8:
            n = rng.randint(2, min(3, max(2, spec.degree_max)))
            inner = Pow(Var(spec.variable), n)
        else:
            inner = _affine_inner(spec, rng)
    used_classes: list[str] = []
    for i in range(depth):
        avoid = used_classes[-1] if (spec.mix_fn_classes and used_classes) else None
        name = _pick_fn_name(spec, rng, avoid_class=avoid) or _resolve_fn_alias(
            spec.require_function or "sin", rng
        )
        # Reject canceling exp∘ln / ln∘exp pairs
        if isinstance(inner, Fn):
            if name == "exp" and inner.name == "ln":
                alt = _pick_fn_name(spec, rng, avoid_class="exp") or "ln"
                name = "ln" if alt == "exp" else alt
            elif name == "ln" and inner.name == "exp":
                alt = _pick_fn_name(spec, rng, avoid_class="log") or "exp"
                name = "exp" if alt == "ln" else alt
        if name == "sqrt" and isinstance(inner, Fn):
            # Avoid ugly sqrt(sin(…)) domains; fall back to trig/exp class mates
            name = _resolve_fn_alias(
                spec.require_function
                or ("trig" if "trig" in (spec.allowed_functions or frozenset()) else "exp"),
                rng,
            )
        layer: ExprAST = Fn(name, inner)
        # Outer-most layer may become a power-of-fn (tan^2(…))
        if i == depth - 1 and spec.allow_fn_power:
            layer = _maybe_fn_power(spec, rng, layer)
        inner = layer
        used_classes.append(_fn_token_class(name))
    return inner


def _specialty_has_primary(expr: ExprAST, spec: ExpressionSpec) -> bool:
    """Specialty leaves must include the topic's function class(es)."""
    if not spec.require_function:
        return True
    classes = function_classes_of(expr)
    primary = _fn_token_class(spec.require_function)
    if primary in {"log", "exp"}:
        return bool(classes & {"log", "exp"})
    return primary in classes


def _specialty_shape(spec: ExpressionSpec, rng: random.Random) -> str:
    """Choose atom / product / nest / fn_power for specialty packs from D budget.

    Hardness is a mix of products, Fn-powers, and nests — not nest-depth alone.
    Invtrig biases toward Pow(arcsin/arctan/arccos, n) and modest products.
    Order≥2 prefers 2nd-deriv-safe shapes (atom / fn_power / shallow nest / 2-factor).
    """
    d = spec.d_spend
    order = max(1, int(spec.derivative_order or 1))
    min_n = max(0, spec.min_special_nodes)
    primary_cls = (
        _fn_token_class(spec.require_function) if spec.require_function else None
    )
    allow_power = bool(spec.allow_fn_power)
    if primary_cls == "exp":
        # exp itself isn't Pow-of-Fn; allow ln^n only when log is unlocked
        allow_power = bool(
            spec.allow_fn_power
            and (
                "log" in (spec.allowed_functions or frozenset())
                or "ln" in (spec.allowed_functions or frozenset())
            )
        )

    # Higher-order: stick to safe bases
    if order >= 2:
        choices = ["atom", "atom"]
        if allow_power:
            choices.extend(["fn_power", "fn_power", "fn_power"])
        if not spec.forbid_product and order == 2:
            choices.append("product")
        if spec.max_nesting >= 1:
            choices.append("nest")
        return rng.choice(choices)

    # Invtrig: strong bias to powers + products over deep nests
    if primary_cls == "invtrig":
        if not spec.forbid_product and d >= 6:
            # Explicit mix — don't let early fn_power starve products
            pool = ["product", "product", "fn_power", "fn_power", "atom"]
            if allow_power:
                pool.extend(["fn_power", "product"])
            else:
                pool.extend(["product", "atom"])
            if d >= 10:
                pool.append("nest")
            if d >= 16:
                pool.extend(["product", "fn_power" if allow_power else "product", "nest"])
            return rng.choice(pool)
        if allow_power and d >= 6:
            return "fn_power" if rng.random() < 0.65 else "atom"
        return "atom" if d < 8 else rng.choice(["atom", "nest"])

    # Trig / ln-exp / general specialty
    p_power = 0.22 if d < 12 else (0.3 if d < 18 else 0.28)
    if allow_power and (spec.prefer_fn_power or d >= 8) and rng.random() < p_power:
        return "fn_power"
    if d >= 20:
        pool = ["product", "product", "nest", "fn_power" if allow_power else "nest"]
        return rng.choice(pool)
    if min_n >= 3 or d >= 16:
        choices = ["product", "nest", "product"]
        if allow_power:
            choices.extend(["fn_power", "fn_power"])
        return rng.choice(choices)
    if min_n >= 2 or d >= 8:
        choices = ["product", "nest", "atom", "product"]
        if allow_power:
            choices.append("fn_power")
        return rng.choice(choices)
    if d >= 6 and not spec.forbid_product:
        return rng.choice(["atom", "product", "atom", "fn_power" if allow_power else "atom"])
    if spec.prefer_chained_fn or spec.max_nesting >= 1:
        return rng.choice(["atom", "nest"])
    return "atom"


def _sample_expression_once(spec: ExpressionSpec, rng: random.Random) -> ExprAST:
    """Single unconstrained draw (caller applies reject/resample gates)."""
    # Specialty leaf: prefer multi-Fn products / nested compositions over poly glue
    if spec.require_function and spec.prefer_special_structure:
        shape = _specialty_shape(spec, rng)
        if shape == "fn_power" and spec.allow_fn_power:
            return _sample_fn_power(spec, rng)
        if shape == "product" and not spec.forbid_product:
            return _sample_product(spec, rng)
        if shape == "nest":
            # Share the stage with products/powers — don't always max out nest
            order = max(1, int(spec.derivative_order or 1))
            if order >= 2:
                depth = min(2, max(1, spec.max_nesting))
            elif spec.d_spend < 12:
                depth = 1
            elif spec.d_spend < 18:
                depth = rng.randint(1, min(2, max(1, spec.max_nesting)))
            else:
                depth = rng.randint(2, min(3, max(2, spec.max_nesting)))
                if spec.deep_chain and rng.random() < 0.35:
                    depth = min(4, max(depth, spec.max_nesting))
            return _sample_fn_nest(spec, rng, depth=depth)
        atom = _sample_fn_atom(
            replace(spec, prefer_chained_fn=True),
            rng,
            _pick_fn_name(spec, rng) or _resolve_fn_alias(spec.require_function, rng),
        )
        return _maybe_fn_power(spec, rng, atom) if spec.allow_fn_power else atom

    # General / multi-class specials without a forced primary class
    if (
        spec.prefer_special_structure
        and spec.allowed_functions
        and not spec.require_function
        and not spec.require_product
        and not spec.require_power_of_poly
    ):
        shape = _specialty_shape(spec, rng)
        if shape == "fn_power" and spec.allow_fn_power:
            return _sample_fn_power(spec, rng)
        if shape == "product" and not spec.forbid_product:
            return _sample_product(spec, rng)
        if shape == "nest" or (spec.mix_fn_classes and shape != "atom"):
            order = max(1, int(spec.derivative_order or 1))
            if order >= 2:
                depth = min(2, max(1, spec.max_nesting))
            elif spec.d_spend < 16:
                depth = min(2, max(1, spec.max_nesting))
            else:
                depth = min(4, max(1, spec.max_nesting, 2 if spec.deep_chain else 1))
            return _sample_fn_nest(spec, rng, depth=depth)
        name = _pick_fn_name(spec, rng)
        if name:
            atom = _sample_fn_atom(replace(spec, prefer_chained_fn=True), rng, name)
            return _maybe_fn_power(spec, rng, atom) if spec.allow_fn_power else atom

    # Forced specials atom (legacy single-Fn path)
    if spec.require_function and not spec.require_product and not spec.require_power_of_poly:
        name = _pick_fn_name(spec, rng) or spec.require_function
        atom = _sample_fn_atom(spec, rng, name)
        return _maybe_fn_power(spec, rng, atom) if spec.allow_fn_power else atom

    if spec.require_product and not spec.forbid_product:
        return _sample_product(spec, rng)

    if spec.require_power_of_poly:
        return _sample_power_chain(spec, rng)

    # Specials unlocked on a chain pack without require_power_of_poly —
    # still inject algebraic (inner)^c when exotic exponents are unlocked.
    # Skip bare power-rule leaves (max_nesting=0, no chain bias).
    kinds = exponent_kinds(spec)
    if (
        bool(kinds & {"fractional", "irrational"})
        and spec.d_spend >= 6
        and (
            spec.require_power_of_poly
            or spec.prefer_chained_fn
            or spec.prefer_special_structure
            or (bool(spec.allowed_functions) and spec.max_nesting >= 1)
        )
        and rng.random() < (0.4 if spec.d_spend >= 12 else 0.3)
    ):
        return _sample_power_chain(
            replace(
                spec,
                prefer_chained_fn=False,
                prefer_special_structure=False,
                require_function=None,
                allowed_functions=frozenset(),
                require_power_of_poly=True,
            ),
            rng,
        )

    # Specials unlocked on a chain pack without require_power_of_poly
    if (
        spec.prefer_special_structure
        and spec.allowed_functions
        and not spec.forbid_product
        and rng.random() < 0.45
    ):
        return _sample_product(spec, rng)
    if spec.prefer_special_structure and spec.allowed_functions:
        if spec.allow_fn_power and rng.random() < 0.3:
            return _sample_fn_power(spec, rng)
        depth = max(1, spec.max_nesting)
        return _sample_fn_nest(spec, rng, depth=depth)

    # Optional special preference (roots on power-rule)
    if (
        spec.allow_rational_powers
        and "sqrt" in (spec.allowed_functions or frozenset())
        and rng.random() < 0.35
    ):
        return _sample_fn_atom(replace(spec, prefer_chained_fn=False), rng, "sqrt")

    # Weird exponents on classic power-rule monomials (teach c·p·x^{p−1})
    if _prefer_weird_power_monomial(spec, rng):
        return _sample_monomial(spec, rng)

    if spec.extra_term or spec.require_sum:
        return _sample_poly_sum(spec, rng)
    if spec.term_count_max > 1 and rng.random() < 0.35:
        return _sample_poly_sum(spec, rng)
    return _sample_monomial(spec, rng)


def sample_expression(
    spec: ExpressionSpec, *, rng: random.Random | None = None
) -> ExprAST:
    """Sample one expression tree under ``spec`` constraints."""
    if rng is None:
        rng = random.Random(spec.seed) if spec.seed is not None else random.Random()

    best: ExprAST | None = None
    for _ in range(24):
        cand = _sample_expression_once(spec, rng)
        if spec.require_function and spec.prefer_special_structure:
            if not _specialty_has_primary(cand, spec):
                continue
        if not _complexity_ok_for_d(cand, spec):
            if best is None:
                best = cand
            continue
        return cand
    if best is not None:
        if _has_canceling_exp_ln(best) and spec.require_function:
            return _sample_fn_atom(
                spec, rng, _resolve_fn_alias(spec.require_function, rng)
            )
        if spec.require_function and spec.prefer_special_structure:
            if _specialty_has_primary(best, spec):
                return best
            return _sample_fn_atom(
                spec, rng, _resolve_fn_alias(spec.require_function, rng)
            )
        return best
    if spec.require_function:
        return _sample_fn_atom(
            spec, rng, _resolve_fn_alias(spec.require_function, rng)
        )
    return _sample_expression_once(spec, rng)


def _sample_product_factor(spec: ExpressionSpec, rng: random.Random, *, as_special: bool) -> ExprAST:
    if as_special and (spec.allowed_functions or spec.require_function):
        name = _pick_fn_name(spec, rng)
        if name is None:
            name = _resolve_fn_alias(spec.require_function or "sin", rng)
        order = max(1, int(spec.derivative_order or 1))
        # Fewer Fn-powers inside products at mid D; almost none at order≥2
        if order >= 2:
            power_p = 0.0
            nest_p = 0.0
        else:
            power_p = 0.12 if spec.d_spend < 16 else (0.22 if spec.d_spend < 20 else 0.32)
            nest_p = 0.12 if spec.d_spend < 16 else 0.28
        if spec.allow_fn_power and rng.random() < power_p:
            return _sample_fn_power(
                replace(spec, require_function=spec.require_function or name), rng
            )
        # Occasional nested Fn factor when nesting budget allows
        if spec.max_nesting >= 2 and rng.random() < nest_p:
            depth_hi = 2 if spec.d_spend < 18 else min(3, spec.max_nesting)
            return _sample_fn_nest(
                replace(spec, require_function=spec.require_function or name),
                rng,
                depth=rng.randint(2, max(2, depth_hi)),
            )
        atom = _sample_fn_atom(
            replace(spec, prefer_chained_fn=spec.prefer_chained_fn or True),
            rng,
            name,
        )
        # Do not auto-wrap every product factor as Fn^n — dedicated power_p above
        # already injects powers; wrapping all factors yields arcsin²·arctan⁴ monsters.
        return atom
    left_spec = replace(
        spec,
        require_product=False,
        require_power_of_poly=False,
        require_function=None,
        prefer_chained_fn=False,
        prefer_special_structure=False,
        allowed_functions=frozenset(),
        min_special_nodes=0,
        allow_fn_power=False,
        prefer_fn_power=False,
        mix_fn_classes=False,
        term_count_max=min(3, spec.term_count_max),
    )
    if spec.extra_term and rng.random() < 0.5:
        return _sample_poly_sum(left_spec, rng)
    return _sample_monomial(left_spec, rng)


def _sample_product(spec: ExpressionSpec, rng: random.Random) -> ExprAST:
    max_f = max(2, spec.max_factors)
    order = max(1, int(spec.derivative_order or 1))
    # Prefer fewer factors when Fn-powers are likely (mid-D) or order≥2
    if order >= 2 or (spec.allow_fn_power and spec.d_spend < 16):
        max_f = 2
    elif spec.d_spend < 20 and spec.allow_fn_power:
        # At D=16–19 allow 3 factors only when not stacking heavy powers
        max_f = min(max_f, 3)
    n = rng.randint(2, max_f)
    specials_available = bool(spec.allowed_functions or spec.require_function)
    prefer_special = spec.prefer_special_structure or bool(spec.require_function)
    min_special = max(0, spec.min_special_nodes)
    if order >= 2:
        min_special = min(min_special, 2)
    if prefer_special and specials_available:
        # Specialty: prefer 2 special factors; only fill all slots at high D when n==2
        if order >= 2 or n == 2:
            target_special = min(n, max(min_special, n))
        elif spec.d_spend >= 20 and n >= 3:
            # 3-factor: leave one modest (poly or plain Fn), not all heavily powered
            target_special = min(n, max(min_special, n - 1))
        else:
            target_special = max(min_special, max(1, n - 1))
        target_special = min(n, target_special)
    elif specials_available:
        # Product/chain with allow_*: mix specials into factors (not poly-only)
        bias = 0.55 if spec.d_spend >= 10 else 0.35
        target_special = sum(1 for _ in range(n) if rng.random() < bias)
        target_special = max(1, target_special)  # at least one special when unlocked
    else:
        target_special = 0

    special_slots = set(rng.sample(range(n), k=target_special)) if target_special else set()
    factors: list[ExprAST] = [
        _sample_product_factor(spec, rng, as_special=(i in special_slots))
        for i in range(n)
    ]
    # Guarantee min_special_nodes after possible nest packing
    if min_special > 0 and _count_fn_nodes(Mul(tuple(factors))) < min_special:
        # Rebuild as all-special product, optionally with nested factors
        factors = [
            _sample_product_factor(spec, rng, as_special=True) for _ in range(n)
        ]
        while (
            _count_fn_nodes(Mul(tuple(factors))) < min_special
            and n < max(2, spec.max_factors)
        ):
            n += 1
            factors.append(_sample_product_factor(spec, rng, as_special=True))
    rng.shuffle(factors)
    return Mul(tuple(factors))


def _sample_power_chain(spec: ExpressionSpec, rng: random.Random) -> ExprAST:
    # Prefer specials when unlocked — nested Fn∘Fn when nesting budget allows
    fns = [f for f in sorted(spec.allowed_functions or frozenset()) if f]
    kinds = exponent_kinds(spec)
    # When fractional/irrational exponents are unlocked, keep a solid share of
    # algebraic (inner)^c samples — those cannot be multiplied out.
    exotic_on = bool(kinds & {"fractional", "irrational"})
    use_special = bool(fns) and (
        (
            spec.prefer_chained_fn
            or spec.prefer_special_structure
            or spec.require_function
            or rng.random()
            < (
                0.75
                if any(
                    f in fns
                    for f in (
                        "sin",
                        "cos",
                        "tan",
                        "trig",
                        "exp",
                        "ln",
                        "log",
                        "arcsin",
                        "invtrig",
                    )
                )
                else 0.45
            )
        )
        and (not exotic_on or rng.random() < (0.45 if spec.d_spend >= 12 else 0.35))
    )
    if use_special:
        nest = max(1, spec.max_nesting)
        if spec.deep_chain or nest >= 2 or (spec.min_special_nodes >= 2):
            depth = max(nest, spec.min_special_nodes or 1, 2 if spec.deep_chain else 1)
            depth = min(4, depth)
            # Mix: sometimes nest, sometimes product of specials under chain pack
            if (
                not spec.forbid_product
                and spec.max_factors >= 3
                and rng.random() < 0.4
            ):
                return _sample_product(
                    replace(
                        spec,
                        require_product=True,
                        prefer_special_structure=True,
                        min_special_nodes=max(spec.min_special_nodes, 3),
                    ),
                    rng,
                )
            return _sample_fn_nest(spec, rng, depth=depth)
        name = _pick_fn_name(spec, rng) or "sin"
        expr = _sample_fn_atom(
            replace(spec, prefer_chained_fn=True, require_function=name), rng, name
        )
        if spec.deep_chain and name in {"sin", "cos", "exp", "tan", "ln"}:
            inner = _sample_linear(spec, rng)
            n = rng.randint(2, min(3, spec.degree_max))
            return Fn(name, Pow(inner, n))
        return expr

    inner = _sample_quadratic_inner(spec, rng) if spec.extra_term else _sample_linear(spec, rng)
    n = _sample_power_exponent(spec, rng, for_fn_power=False)
    expr: ExprAST = Pow(inner, n)
    # Nested integer outer only when the leaf power is already integer (avoid π^e)
    if spec.deep_chain and isinstance(n, int):
        n2 = rng.randint(2, min(3, max(2, spec.degree_max)))
        expr = Pow(expr, n2)
    return expr


# ---------------------------------------------------------------------------
# Differentiate (AST → AST)
# ---------------------------------------------------------------------------


def differentiate(expr: ExprAST, var: str = "x") -> ExprAST:
    """Symbolic derivative; poly + elementary Fn subset."""
    if isinstance(expr, Const):
        return Const(0)
    if isinstance(expr, Var):
        return Const(1) if expr.name == var else Const(0)
    if isinstance(expr, Add):
        parts = tuple(differentiate(t, var) for t in expr.terms)
        return _simplify_add(parts)
    if isinstance(expr, Mul):
        return _diff_mul(expr.factors, var)
    if isinstance(expr, Pow):
        return _diff_pow(expr, var)
    if isinstance(expr, Fn):
        return _diff_fn(expr, var)
    return Const(0)


def _diff_mul(factors: tuple[ExprAST, ...], var: str) -> ExprAST:
    if len(factors) == 0:
        return Const(0)
    if len(factors) == 1:
        return differentiate(factors[0], var)
    terms: list[ExprAST] = []
    for i, fi in enumerate(factors):
        dfi = differentiate(fi, var)
        rest = factors[:i] + factors[i + 1 :]
        if isinstance(dfi, Const) and dfi.value == 0:
            continue
        if not rest:
            terms.append(_simplify_expr(dfi))
        elif isinstance(dfi, Const) and dfi.value == 1:
            terms.append(_simplify_expr(Mul(rest) if len(rest) > 1 else rest[0]))
        else:
            terms.append(_simplify_expr(Mul((dfi,) + rest)))
    if not terms:
        return Const(0)
    if len(terms) == 1:
        return terms[0]
    return Add(tuple(terms))


def _simplify_expr(expr: ExprAST) -> ExprAST:
    """Collapse nested coef muls like 3*(3*x^2) → 9*x^2.

    Only folds integer Const factors — leave Fraction / SymConst visible so
    chain answers keep the power-rule coefficient ``c`` in ``c·u^{c−1}·u'``.
    """
    if isinstance(expr, Mul):
        coef = 1
        others: list[ExprAST] = []

        def absorb(f: ExprAST) -> None:
            nonlocal coef
            f = _simplify_expr(f)
            if isinstance(f, Const) and isinstance(f.value, int):
                coef *= int(f.value)
            elif isinstance(f, Mul):
                for g in f.factors:
                    absorb(g)
            else:
                others.append(f)

        for f in expr.factors:
            absorb(f)
        if coef == 0:
            return Const(0)
        if not others:
            return Const(coef)
        if coef == 1:
            return others[0] if len(others) == 1 else Mul(tuple(others))
        if coef == -1 and len(others) == 1:
            return Mul((Const(-1), others[0]))
        return Mul((Const(coef),) + tuple(others)) if len(others) >= 1 else Const(coef)
    if isinstance(expr, Add):
        return Add(tuple(_simplify_expr(t) for t in expr.terms))
    if isinstance(expr, Pow):
        return Pow(_simplify_expr(expr.base), expr.exp)
    if isinstance(expr, Fn):
        return Fn(expr.name, _simplify_expr(expr.arg))
    return expr


def _diff_pow(expr: Pow, var: str) -> ExprAST:
    """d/dx[u^c] = c·u^{c−1}·u' for constant c (int / Fraction / SymConst)."""
    base, exp = expr.base, expr.exp
    db = differentiate(base, var)
    if isinstance(db, Const) and db.value == 0:
        return Const(0)

    # Integer specials
    if isinstance(exp, int):
        n = int(exp)
        if n == 0:
            return Const(0)
        if n == 1:
            return db
        power_part: ExprAST = base if n - 1 == 1 else Pow(base, n - 1)
        if isinstance(db, Const) and db.value == 1:
            return _simplify_expr(Mul((Const(n), power_part)))
        return _simplify_expr(Mul((Const(n), power_part, db)))

    # Fraction / SymConst / SymOffset: c · u^{c-1} · u'
    coef: ExprAST = _const_from_exp(exp)
    if isinstance(exp, SymOffset) and exp.offset != 0:
        # (π+k) as Add for coefficient when somehow present
        coef = Add((Const(exp.sym), Const(exp.offset)))
    new_exp = _exp_minus_one(exp)
    powered = Pow(base, new_exp)
    if isinstance(db, Const) and db.value == 1:
        return _simplify_expr(Mul((coef, powered)))
    return _simplify_expr(Mul((coef, powered, db)))


def _diff_fn(expr: Fn, var: str) -> ExprAST:
    name, arg = expr.name, expr.arg
    darg = differentiate(arg, var)

    def chain(outer: ExprAST) -> ExprAST:
        if isinstance(darg, Const) and darg.value == 0:
            return Const(0)
        if isinstance(darg, Const) and darg.value == 1:
            return outer
        return Mul((outer, darg))

    if name == "sin":
        return chain(Fn("cos", arg))
    if name == "cos":
        return chain(Mul((Const(-1), Fn("sin", arg))))
    if name == "tan":
        # sec^2(arg) — encode as tag for first-deriv render; still re-diffable
        return chain(Fn("sec2", arg))
    if name == "exp":
        return chain(Fn("exp", arg))
    if name == "ln":
        return chain(_inv(arg))
    if name == "arcsin":
        return chain(Fn("darcsin", arg))
    if name == "arccos":
        return chain(Fn("darccos", arg))
    if name == "arctan":
        return chain(Fn("darctan", arg))
    if name == "sinh":
        return chain(Fn("cosh", arg))
    if name == "cosh":
        return chain(Fn("sinh", arg))
    if name == "sqrt":
        return chain(Fn("dsqrt", arg))

    # Re-differentiate derivative tags (needed for 2nd/3rd order)
    if name == "sec2":
        # d/dx[sec^2(u)] = 2 sec^2(u) tan(u) u'
        return chain(Mul((Const(2), Fn("sec2", arg), Fn("tan", arg))))
    if name == "darcsin":
        # d/dx[1/sqrt(1-u^2)] = u (1-u^2)^{-3/2} u'
        one_minus = Add((Const(1), Mul((Const(-1), Pow(arg, 2)))))
        return chain(Mul((arg, Pow(one_minus, Fraction(-3, 2)))))
    if name == "darccos":
        one_minus = Add((Const(1), Mul((Const(-1), Pow(arg, 2)))))
        return chain(Mul((Const(-1), arg, Pow(one_minus, Fraction(-3, 2)))))
    if name == "darctan":
        # d/dx[1/(1+u^2)] = -2u/(1+u^2)^2 u'
        return chain(
            Mul((Const(-2), arg, Pow(Add((Const(1), Pow(arg, 2))), -2)))
        )
    if name == "dsqrt":
        # d/dx[1/(2 sqrt(u))] = -1/(4 u^{3/2}) u'
        return chain(Mul((Const(Fraction(-1, 4)), Pow(arg, Fraction(-3, 2)))))
    if name == "inv":
        # d/dx[1/u] = -1/u^2 u'
        return chain(Mul((Const(-1), Pow(arg, -2))))
    return Const(0)


def _inv(arg: ExprAST) -> ExprAST:
    """Represent 1/arg as Pow(arg, -1) for rendering."""
    return Pow(arg, -1)


def _simplify_add(parts: tuple[ExprAST, ...]) -> ExprAST:
    nonzero = [p for p in parts if not (isinstance(p, Const) and p.value == 0)]
    if not nonzero:
        return Const(0)
    if len(nonzero) == 1:
        return nonzero[0]
    return Add(tuple(nonzero))


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------


def render_latex(
    expr: ExprAST,
    *,
    paren_style: ParenStyle | None = None,
    _parent: str | None = None,
) -> str:
    """Render AST to latex. ``paren_style`` defaults to minimal for leaves."""
    style: ParenStyle = paren_style or "minimal"
    return _render(expr, style=style, parent=_parent)


def _const_numeric(v: int | Fraction | SymConst) -> float | None:
    if isinstance(v, SymConst):
        import math

        if v.name == "pi":
            return math.pi
        if v.name == "e":
            return math.e
        if v.name == "sqrt2":
            return math.sqrt(2)
        if v.name == "sqrt3":
            return math.sqrt(3)
        return None
    if isinstance(v, Fraction):
        return float(v)
    return float(v)


def eval_expr_at(expr: ExprAST, x: float) -> float | None:
    """Numeric evaluation of ``expr`` at ``x``. Returns None on domain/overflow."""
    import math

    try:
        if isinstance(expr, Const):
            return _const_numeric(expr.value)
        if isinstance(expr, Var):
            return float(x)
        if isinstance(expr, Add):
            parts = [eval_expr_at(t, x) for t in expr.terms]
            if any(p is None for p in parts):
                return None
            return float(sum(parts))  # type: ignore[arg-type]
        if isinstance(expr, Mul):
            acc = 1.0
            for f in expr.factors:
                v = eval_expr_at(f, x)
                if v is None:
                    return None
                acc *= v
            return acc
        if isinstance(expr, Pow):
            base = eval_expr_at(expr.base, x)
            if base is None:
                return None
            exp = expr.exp
            if isinstance(exp, SymOffset):
                e_num = _const_numeric(exp.sym)
                if e_num is None:
                    return None
                e_num = e_num + exp.offset
            elif isinstance(exp, (int, float, Fraction, SymConst)):
                e_num = _const_numeric(exp) if isinstance(exp, SymConst) else float(exp)
            else:
                return None
            if base < 0 and abs(e_num - round(e_num)) > 1e-12:
                return None
            return float(base**e_num)
        if isinstance(expr, Fn):
            arg = eval_expr_at(expr.arg, x)
            if arg is None:
                return None
            name = expr.name
            if name == "sin":
                return math.sin(arg)
            if name == "cos":
                return math.cos(arg)
            if name == "tan":
                # Reject near odd multiples of π/2
                if abs(math.cos(arg)) < 1e-10:
                    return None
                return math.tan(arg)
            if name == "exp":
                if arg > 700:
                    return None
                return math.exp(arg)
            if name == "ln":
                if arg <= 0:
                    return None
                return math.log(arg)
            if name == "sqrt":
                if arg < 0:
                    return None
                return math.sqrt(arg)
            if name == "arcsin":
                if arg < -1 or arg > 1:
                    return None
                return math.asin(arg)
            if name == "arccos":
                if arg < -1 or arg > 1:
                    return None
                return math.acos(arg)
            if name == "arctan":
                return math.atan(arg)
            if name == "sinh":
                return math.sinh(arg)
            if name == "cosh":
                return math.cosh(arg)
            return None
    except (OverflowError, ValueError, ZeroDivisionError):
        return None
    return None


def format_numeric_limit_answer(value: float, *, tol: float = 1e-9) -> str | None:
    """Pretty latex for a finite limit value; None if not a clean Calc-1 answer."""
    import math

    if not math.isfinite(value):
        return None
    if abs(value) < tol:
        return "0"
    # Integers
    nearest = round(value)
    if abs(value - nearest) < tol:
        return str(int(nearest))
    # Simple rationals with den ≤ 12
    for den in range(2, 13):
        num = round(value * den)
        if abs(value * den - num) < tol * den:
            return frac_latex(Fraction(int(num), den))
    # Common π multiples
    if abs(value - math.pi) < 1e-6:
        return r"\pi"
    if abs(value + math.pi) < 1e-6:
        return r"-\pi"
    if abs(value - math.pi / 2) < 1e-6:
        return r"\frac{\pi}{2}"
    if abs(value + math.pi / 2) < 1e-6:
        return r"-\frac{\pi}{2}"
    if abs(value - math.pi / 3) < 1e-6:
        return r"\frac{\pi}{3}"
    if abs(value - math.pi / 4) < 1e-6:
        return r"\frac{\pi}{4}"
    if abs(value - math.pi / 6) < 1e-6:
        return r"\frac{\pi}{6}"
    if abs(value - math.e) < 1e-6:
        return "e"
    # Known trig values at special angles already covered via numeric
    return None


def _needs_paren_add(parent: str | None) -> bool:
    return parent in {"mul", "pow", "fn"}


def _wrap(s: str, *, force: bool) -> str:
    if not force:
        return s
    return rf"\left({s}\right)"


def _render(expr: ExprAST, *, style: ParenStyle, parent: str | None) -> str:
    if isinstance(expr, Const):
        v = expr.value
        if isinstance(v, SymConst):
            return _sym_const_latex(v)
        if isinstance(v, Fraction):
            return frac_latex(v)
        return str(v)
    if isinstance(expr, Var):
        return expr.name
    if isinstance(expr, Add):
        parts = [_render(t, style=style, parent="add") for t in expr.terms]
        out = parts[0] if parts else "0"
        for p in parts[1:]:
            if p.startswith("-"):
                out += f" - {p[1:]}"
            else:
                out += f" + {p}"
        poly = _try_poly_coeffs(expr)
        if poly is not None:
            out = format_polynomial_latex(poly[0], variable=poly[1])
        # Parent Pow/Mul/Fn applies outer wrappers — avoid double \left
        force = parent in {"mul", "fn"} and style != "minimal"
        return _wrap(out, force=force)

    if isinstance(expr, Mul):
        return _render_mul(expr.factors, style=style, parent=parent)

    if isinstance(expr, Pow):
        return _render_pow(expr, style=style, parent=parent)

    if isinstance(expr, Fn):
        return _render_fn(expr, style=style, parent=parent)

    return "0"


def _try_poly_coeffs(expr: Add) -> tuple[list[int], str] | None:
    """If Add is a dense poly in one var, return (hi-first coeffs, var)."""
    var: str | None = None
    deg_coef: dict[int, int] = {}

    def absorb(term: ExprAST, sign: int = 1) -> bool:
        nonlocal var
        if isinstance(term, Const) and isinstance(term.value, int):
            deg_coef[0] = deg_coef.get(0, 0) + sign * term.value
            return True
        if isinstance(term, Var):
            var = var or term.name
            if term.name != var:
                return False
            deg_coef[1] = deg_coef.get(1, 0) + sign
            return True
        if isinstance(term, Pow) and isinstance(term.base, Var) and isinstance(term.exp, int):
            var = var or term.base.name
            if term.base.name != var:
                return False
            deg_coef[int(term.exp)] = deg_coef.get(int(term.exp), 0) + sign
            return True
        if isinstance(term, Mul) and len(term.factors) == 2:
            a, b = term.factors
            if isinstance(a, Const) and isinstance(a.value, int):
                if isinstance(b, Var):
                    var = var or b.name
                    if b.name != var:
                        return False
                    deg_coef[1] = deg_coef.get(1, 0) + sign * a.value
                    return True
                if isinstance(b, Pow) and isinstance(b.base, Var) and isinstance(b.exp, int):
                    var = var or b.base.name
                    if b.base.name != var:
                        return False
                    deg_coef[int(b.exp)] = deg_coef.get(int(b.exp), 0) + sign * a.value
                    return True
            if isinstance(a, Const) and a.value == -1:
                return absorb(b, -sign)
        return False

    for t in expr.terms:
        if not absorb(t):
            return None
    if var is None:
        return None
    max_deg = max(deg_coef) if deg_coef else 0
    coeffs = [deg_coef.get(d, 0) for d in range(max_deg, -1, -1)]
    return coeffs, var


def _render_mul(
    factors: tuple[ExprAST, ...], *, style: ParenStyle, parent: str | None
) -> str:
    if not factors:
        return "1"

    # Quotient sugar: F · G^{-1} · … → \frac{F·…}{G·…}
    nums: list[ExprAST] = []
    dens: list[ExprAST] = []
    for f in factors:
        if (
            isinstance(f, Pow)
            and (
                f.exp == -1
                or (isinstance(f.exp, Fraction) and f.exp == Fraction(-1))
            )
        ):
            dens.append(f.base)
        else:
            nums.append(f)
    if dens:
        if not nums:
            den_s = (
                _render(dens[0], style=style, parent="fn")
                if len(dens) == 1
                else _render_mul(tuple(dens), style=style, parent="fn")
            )
            return rf"\frac{{1}}{{{den_s}}}"
        # Pull a leading -1 coef out as a sign on the fraction.
        sign = ""
        if (
            len(nums) >= 1
            and isinstance(nums[0], Const)
            and nums[0].value == -1
        ):
            sign = "-"
            nums = nums[1:]
            if not nums:
                den_s = (
                    _render(dens[0], style=style, parent="fn")
                    if len(dens) == 1
                    else _render_mul(tuple(dens), style=style, parent="fn")
                )
                return rf"{sign}\frac{{1}}{{{den_s}}}"
        num_s = (
            _render(nums[0], style=style, parent=None)
            if len(nums) == 1
            else _render_mul(tuple(nums), style=style, parent="mul")
        )
        den_s = (
            _render(dens[0], style=style, parent="fn")
            if len(dens) == 1
            else _render_mul(tuple(dens), style=style, parent="fn")
        )
        return rf"{sign}\frac{{{num_s}}}{{{den_s}}}"

    # coef * rest sugar (int / Fraction / SymConst leading coefficients)
    if len(factors) >= 2 and isinstance(factors[0], Const):
        # On monomials k·x^p, fold a run of rational Consts into one coefficient.
        # Leave int×Fraction visible on chain answers so ``c`` stays in view.
        rational = Fraction(1)
        rest_idx = 0
        saw_rational = False
        while rest_idx < len(factors) and isinstance(factors[rest_idx], Const):
            v = factors[rest_idx].value
            if isinstance(v, int):
                rational *= int(v)
                saw_rational = True
                rest_idx += 1
            elif isinstance(v, Fraction):
                rational *= v
                saw_rational = True
                rest_idx += 1
            else:
                break
        rest = factors[rest_idx:]
        monomial_fold = (
            saw_rational
            and rest_idx >= 1
            and len(rest) == 1
            and isinstance(rest[0], Pow)
            and isinstance(rest[0].base, Var)
        )
        if monomial_fold:
            if rational == 0:
                return "0"
            rest_s = _render(rest[0], style=style, parent="mul")
            if rational.denominator == 1:
                coef = int(rational)
                if coef == -1:
                    return f"-{rest_s}"
                if coef == 1:
                    return rest_s
                if rest_s.startswith("-"):
                    return rf"{coef}\cdot\left({rest_s}\right)"
                return f"{coef}{rest_s}"
            return _juxtapose_coef_body(frac_latex(rational), rest_s)

        coef_v = factors[0].value
        rest = factors[1:]
        rest_ast = rest[0] if len(rest) == 1 else None
        rest_s = (
            _render_mul(rest, style=style, parent="mul")
            if len(rest) > 1
            else _render(rest[0], style=style, parent="mul")
        )
        # Parenthesize sums (and similar) before coef juxtaposition. Without
        # this, ``5·(5x^{2}+2x-4)`` digit-glues to the false ``55x^{2}+2x-4``.
        rest_needs_paren = rest_s.startswith("-") or (
            _factor_ast_needs_paren(rest_ast, rest_s)
            if rest_ast is not None
            else _latex_factor_needs_paren(rest_s)
        )
        if isinstance(coef_v, int):
            coef = int(coef_v)
            if coef == -1:
                if rest_needs_paren and not _already_wrapped_factor(rest_s):
                    return rf"-\left({rest_s}\right)"
                return f"-{rest_s}"
            if coef == 1:
                return rest_s
            if rest_needs_paren:
                if rest_s.startswith("-"):
                    return rf"{coef}\cdot\left({rest_s}\right)"
                return rf"{coef}\left({rest_s}\right)"
            return f"{coef}{rest_s}"
        if isinstance(coef_v, (Fraction, SymConst)):
            if isinstance(coef_v, Fraction) and coef_v == -1:
                if rest_needs_paren and not _already_wrapped_factor(rest_s):
                    return rf"-\left({rest_s}\right)"
                return f"-{rest_s}"
            if isinstance(coef_v, Fraction) and coef_v == 1:
                return rest_s
            coef_s = (
                frac_latex(coef_v)
                if isinstance(coef_v, Fraction)
                else _sym_const_latex(coef_v)
            )
            return _juxtapose_coef_body(coef_s, rest_s)

    # Product-rule style: wrap a factor only when needed for precedence /
    # ambiguity (sums, leading minus). Digit-starting later factors get
    # parens at join time so ``3·4x^{3}`` does not glue to ``34x^{3}``.
    # ``always_factors`` shares this minimal policy.
    parts = []
    for f in factors:
        s = _render(f, style="minimal", parent=None)
        if _factor_ast_needs_paren(f, s):
            s = _wrap(s, force=True)
        parts.append(s)
    return _juxtapose_product_factors(parts)


def _render_pow(expr: Pow, *, style: ParenStyle, parent: str | None) -> str:
    del parent
    base, exp = expr.base, expr.exp
    if isinstance(exp, int) and exp == -1:
        # Keep x^{-1} for power-rule pedagogy; 1/(inner) for compound bases
        if isinstance(base, Var):
            return rf"{base.name}^{{-1}}"
        inner = _render(base, style=style, parent="fn")
        return rf"\frac{{1}}{{{inner}}}"

    exp_s = _power_exp_latex(exp)

    # Power of elementary Fn: \tan^{2}(x), \sin^{3}(3x), \ln^{2}(x)
    if isinstance(base, Fn) and base.name in _FN_POWER_OK:
        latex = FN_LATEX[base.name]
        arg_s = _render(base.arg, style=style, parent="fn")
        # Bare var / kx: sin^n(x) style; richer args use \left(
        simple_arg = isinstance(base.arg, Var) or (
            isinstance(base.arg, Mul)
            and len(base.arg.factors) == 2
            and isinstance(base.arg.factors[0], Const)
            and isinstance(base.arg.factors[1], Var)
        )
        if simple_arg:
            return rf"{latex}^{{{exp_s}}}({arg_s})"
        return rf"{latex}^{{{exp_s}}}\left({arg_s}\right)"

    # Fractional / symbolic / non-int: always use ^{…} form (never expand)
    if not isinstance(exp, int):
        base_s = _render(base, style=style, parent="pow")
        if isinstance(base, Var):
            return rf"{base_s}^{{{exp_s}}}"
        return rf"\left({base_s}\right)^{{{exp_s}}}"

    n = int(exp)
    if isinstance(base, Var):
        if n == 1:
            return base.name
        return f"{base.name}^{{{n}}}"

    base_s = _render(base, style="minimal", parent=None)
    wrap = style in {"always_powers", "always_factors"} or isinstance(
        base, (Add, Mul, Pow, Fn)
    )
    if wrap:
        base_s = _wrap(base_s, force=True)
    if n == 1:
        return base_s
    return rf"{base_s}^{{{n}}}"


def _render_fn(expr: Fn, *, style: ParenStyle, parent: str | None) -> str:
    del parent
    name, arg = expr.name, expr.arg
    arg_s = _render(arg, style=style, parent="fn")

    if name == "exp":
        return rf"e^{{{arg_s}}}"
    if name == "ln":
        # Parentheses only — never `|` bars (break markdown gallery tables /
        # get truncated to `\ln\left\`). Domain bars → use \lvert/\rvert if needed.
        if isinstance(arg, Var):
            return rf"\ln({arg_s})"
        return rf"\ln\left({arg_s}\right)"
    if name == "sqrt":
        return rf"\sqrt{{{arg_s}}}"
    if name == "sec2":
        return rf"\sec^{{2}}({arg_s})"
    if name == "darcsin":
        return rf"\frac{{1}}{{\sqrt{{1-({arg_s})^{{2}}}}}}"
    if name == "darccos":
        return rf"-\frac{{1}}{{\sqrt{{1-({arg_s})^{{2}}}}}}"
    if name == "darctan":
        return rf"\frac{{1}}{{1+({arg_s})^{{2}}}}"
    if name == "dsqrt":
        # handled specially in differentiate rendering path usually
        return rf"\frac{{1}}{{2\sqrt{{{arg_s}}}}}"
    if name == "inv":
        return rf"\frac{{1}}{{{arg_s}}}"

    latex = FN_LATEX.get(name, name)
    if isinstance(arg, Var) or (
        isinstance(arg, Mul)
        and len(arg.factors) == 2
        and isinstance(arg.factors[0], Const)
        and isinstance(arg.factors[1], Var)
    ):
        return rf"{latex}({arg_s})"
    return rf"{latex}\left({arg_s}\right)"


# ---------------------------------------------------------------------------
# Structure inventory (Phase 2)
# ---------------------------------------------------------------------------


def structure_inventory(expr: ExprAST) -> dict[str, Any]:
    """Topic-fit / gallery fields: ops, degrees, nest, shape_id."""
    ops: list[str] = []
    fns: list[str] = []
    degrees: list[int] = []
    nest = _nest_depth(expr)
    n_factors = 0
    n_terms = 0
    has_product = False
    has_sum = False
    has_power = False
    has_fn = False
    has_quotient = False

    def is_coef_mul(e: Mul) -> bool:
        """True when Mul is only a numeric coefficient times one atom."""
        if len(e.factors) != 2:
            return False
        a, b = e.factors
        return isinstance(a, Const) and not isinstance(b, Const)

    def is_quot_mul(e: Mul) -> bool:
        """F · G^{-1} (possibly with extra num factors) — quotient shape."""
        dens = 0
        nums = 0
        for f in e.factors:
            if isinstance(f, Pow) and (
                f.exp == -1
                or (isinstance(f.exp, Fraction) and f.exp == Fraction(-1))
            ):
                dens += 1
            elif not (isinstance(f, Const)):
                nums += 1
            elif isinstance(f, Const):
                nums += 1  # coef counts toward numerator side
        return dens >= 1 and nums >= 1

    def walk(e: ExprAST) -> None:
        nonlocal n_factors, n_terms, has_product, has_sum, has_power, has_fn, has_quotient
        if isinstance(e, Const):
            return
        if isinstance(e, Var):
            degrees.append(1)
            return
        if isinstance(e, Add):
            ops.append("+")
            has_sum = True
            n_terms = max(n_terms, len(e.terms))
            for t in e.terms:
                walk(t)
            return
        if isinstance(e, Mul):
            if is_coef_mul(e):
                # coefficient sugar — not a product-rule structure
                if isinstance(e.factors[1], Pow) and isinstance(e.factors[1].exp, int):
                    ops.append("^")
                    has_power = True
                    degrees.append(int(e.factors[1].exp))
                    walk(e.factors[1].base)
                else:
                    walk(e.factors[1])
                return
            if is_quot_mul(e):
                ops.append("/")
                has_quotient = True
                for f in e.factors:
                    if isinstance(f, Pow) and (
                        f.exp == -1
                        or (isinstance(f.exp, Fraction) and f.exp == Fraction(-1))
                    ):
                        walk(f.base)
                    else:
                        walk(f)
                return
            ops.append("*")
            has_product = True
            n_factors = max(n_factors, len(e.factors))
            for f in e.factors:
                walk(f)
            return
        if isinstance(e, Pow):
            ops.append("^")
            has_power = True
            if isinstance(e.exp, int):
                degrees.append(int(e.exp))
            elif isinstance(e.exp, Fraction):
                degrees.append(max(1, abs(int(e.exp.numerator))))
            walk(e.base)
            return
        if isinstance(e, Fn):
            has_fn = True
            fns.append(e.name)
            walk(e.arg)

    walk(expr)
    has_fn_power = False

    def check_fn_power(e: ExprAST) -> None:
        nonlocal has_fn_power
        if isinstance(e, Pow) and isinstance(e.base, Fn):
            has_fn_power = True
        if isinstance(e, Add):
            for t in e.terms:
                check_fn_power(t)
        elif isinstance(e, Mul):
            for f in e.factors:
                check_fn_power(f)
        elif isinstance(e, Pow):
            check_fn_power(e.base)
        elif isinstance(e, Fn):
            check_fn_power(e.arg)

    check_fn_power(expr)
    shape_parts = []
    if has_fn:
        shape_parts.append("fn:" + "+".join(sorted(set(fns)) or ["?"]))
    if has_fn_power:
        shape_parts.append("fn_power")
    if has_quotient:
        shape_parts.append("quotient")
    if has_product:
        shape_parts.append("product")
    if has_sum:
        shape_parts.append("sum")
    if has_power:
        shape_parts.append("power")
    if not shape_parts:
        shape_parts.append("atom")
    shape_id = "+".join(shape_parts)
    return {
        "shape_id": shape_id,
        "ops": ops,
        "functions": sorted(set(fns)),
        "nest_depth": nest,
        "degrees": degrees,
        "degree_max": max(degrees) if degrees else 0,
        "n_terms": n_terms or (1 if not has_sum else n_terms),
        "n_factors": n_factors,
        "has_product": has_product,
        "has_quotient": has_quotient,
        "has_sum": has_sum,
        "has_power": has_power,
        "has_fn": has_fn,
        "has_fn_power": has_fn_power,
    }


def _nest_depth(expr: ExprAST) -> int:
    """Composition nesting: powers of a bare variable do not count as nest."""
    if isinstance(expr, (Const, Var)):
        return 0
    if isinstance(expr, Add):
        return max((_nest_depth(t) for t in expr.terms), default=0)
    if isinstance(expr, Mul):
        # coef * atom: ignore coef
        if (
            len(expr.factors) == 2
            and isinstance(expr.factors[0], Const)
            and not isinstance(expr.factors[1], Const)
        ):
            return _nest_depth(expr.factors[1])
        return max((_nest_depth(f) for f in expr.factors), default=0)
    if isinstance(expr, Pow):
        if isinstance(expr.base, Var):
            return 0
        return 1 + _nest_depth(expr.base)
    if isinstance(expr, Fn):
        if isinstance(expr.arg, Var):
            return 0
        return 1 + _nest_depth(expr.arg)
    return 0


def function_classes_of(expr: ExprAST) -> frozenset[str]:
    inv = structure_inventory(expr)
    classes: set[str] = set()
    for fn in inv["functions"]:
        if fn in {"sin", "cos", "tan", "sec2"}:
            classes.add("trig")
        elif fn == "exp":
            classes.add("exp")
        elif fn == "ln":
            classes.add("log")
        elif fn in {"arcsin", "arccos", "arctan", "darcsin", "darccos", "darctan"}:
            classes.add("invtrig")
        elif fn in {"sinh", "cosh"}:
            classes.add("hyperbolic")
        elif fn in {"sqrt", "dsqrt"}:
            classes.add("roots")

    def walk(e: ExprAST) -> None:
        if isinstance(e, Pow) and isinstance(e.exp, Fraction):
            classes.add("roots")
            classes.add("algebraic")
        if isinstance(e, Add):
            for t in e.terms:
                walk(t)
        elif isinstance(e, Mul):
            for f in e.factors:
                walk(f)
        elif isinstance(e, Pow):
            walk(e.base)
        elif isinstance(e, Fn):
            walk(e.arg)

    walk(expr)
    if not classes or classes <= {"roots"}:
        classes.add("algebraic")
    # Chained specials of non-trivial args also tag algebraic
    if classes & {"trig", "exp", "log", "invtrig", "hyperbolic"} and inv["nest_depth"] >= 1:
        classes.add("algebraic")
    # Products mixing algebraic factors with specials
    if inv["has_product"] and classes & {"trig", "exp", "log", "invtrig", "hyperbolic"}:
        classes.add("algebraic")
    return frozenset(classes)


def methods_used_of(expr: ExprAST) -> frozenset[str]:
    inv = structure_inventory(expr)
    methods: set[str] = set()
    methods.add("power")
    if inv.get("has_quotient"):
        methods.add("quotient")
    if inv["has_product"]:
        methods.add("product")

    def is_top_sum(e: ExprAST) -> bool:
        if isinstance(e, Add):
            return True
        if (
            isinstance(e, Mul)
            and len(e.factors) == 2
            and isinstance(e.factors[0], Const)
            and not isinstance(e.factors[1], Const)
        ):
            return is_top_sum(e.factors[1])
        return False

    if is_top_sum(expr):
        methods.add("sum")

    def needs_chain(e: ExprAST) -> bool:
        if isinstance(e, Fn):
            return not isinstance(e.arg, Var)
        if isinstance(e, Pow):
            return not isinstance(e.base, Var)
        if isinstance(e, Add):
            return any(needs_chain(t) for t in e.terms)
        if isinstance(e, Mul):
            if (
                len(e.factors) == 2
                and isinstance(e.factors[0], Const)
                and not isinstance(e.factors[1], Const)
            ):
                return needs_chain(e.factors[1])
            return any(needs_chain(f) for f in e.factors)
        return False

    if needs_chain(expr):
        methods.add("chain")
    return frozenset(methods) or frozenset({"power"})


def chain_depth_of(expr: ExprAST) -> int:
    if "chain" not in methods_used_of(expr):
        return 0
    return max(1, _nest_depth(expr))


# ---------------------------------------------------------------------------
# High-level: sample + differentiate → latex pair (for derivatives façade)
# ---------------------------------------------------------------------------


def sample_and_differentiate(
    spec: ExpressionSpec, *, rng: random.Random | None = None
) -> tuple[ExprAST, ExprAST, str, str, dict[str, Any]]:
    """Return (expr, d_expr, body_latex, deriv_latex, inventory)."""
    if rng is None:
        rng = random.Random(spec.seed) if spec.seed is not None else random.Random()
    order = max(1, int(spec.derivative_order or 1))
    len_cap = _answer_len_budget(spec.d_spend, order=order)

    expr: ExprAST | None = None
    d_expr: ExprAST | None = None
    body = ""
    deriv = ""
    for _ in range(16):
        cand = sample_expression(spec, rng=rng)
        d_cand = cand
        for _ in range(order):
            d_cand = differentiate(d_cand, spec.variable)
        body_c = render_latex(cand, paren_style=spec.paren_style)
        # Prefer minimal product parens for readability; keep always_powers
        # for algebraic chain answers that need base wrapping.
        deriv_style: ParenStyle = (
            "always_powers"
            if spec.require_power_of_poly or spec.paren_style == "always_powers"
            else "minimal"
        )
        deriv_c: str | None = None
        if order == 1:
            deriv_c = _render_deriv_legacy(cand, d_cand, spec)
        if deriv_c is None:
            deriv_c = render_latex(d_cand, paren_style=deriv_style)
        # Reject trivial canceling / zero higher-order / enormous answers
        if _has_canceling_exp_ln(cand):
            continue
        if order >= 2 and isinstance(d_cand, Const) and d_cand.value == 0:
            # Ultra-simple bodies that collapse under re-diff — resample
            if _count_fn_nodes(cand) <= 2 and not isinstance(cand, Mul):
                continue
        if len(deriv_c) > len_cap and (
            (isinstance(cand, Mul) and len(cand.factors) > 2)
            or _count_fn_powers(cand) >= 2
            or (order >= 2 and (_nest_depth(cand) >= 2 or isinstance(cand, Mul)))
            or (order >= 2 and _count_fn_powers(cand) >= 1 and _nest_depth(cand) >= 1)
        ):
            # Keep as fallback but prefer shorter
            if expr is None or len(deriv_c) < len(deriv):
                expr, d_expr, body, deriv = cand, d_cand, body_c, deriv_c
            continue
        # Order≥2: also reject when answer is huge even on "simple" bases
        if order >= 2 and len(deriv_c) > len_cap:
            if expr is None or len(deriv_c) < len(deriv):
                expr, d_expr, body, deriv = cand, d_cand, body_c, deriv_c
            continue
        expr, d_expr, body, deriv = cand, d_cand, body_c, deriv_c
        break
    if expr is None or d_expr is None:
        expr = sample_expression(spec, rng=rng)
        d_expr = expr
        for _ in range(order):
            d_expr = differentiate(d_expr, spec.variable)
        body = render_latex(expr, paren_style=spec.paren_style)
        deriv_style: ParenStyle = (
            "always_powers"
            if spec.require_power_of_poly or spec.paren_style == "always_powers"
            else "minimal"
        )
        deriv = None
        if order == 1:
            deriv = _render_deriv_legacy(expr, d_expr, spec)
        if deriv is None:
            deriv = render_latex(d_expr, paren_style=deriv_style)

    inv = structure_inventory(expr)
    inv["function_classes"] = sorted(function_classes_of(expr))
    inv["methods_used"] = sorted(methods_used_of(expr))
    inv["chain_depth"] = chain_depth_of(expr)
    inv["derivative_order"] = order
    inv["effort_features"] = effort_features_of(expr, answer_latex=deriv, order=order)
    return expr, d_expr, body, deriv, inv


def effort_features_of(
    expr: ExprAST, *, answer_latex: str = "", order: int = 1
) -> dict[str, Any]:
    """Structural effort signals for ML / continuous-D scoring."""
    inv = structure_inventory(expr)
    methods = methods_used_of(expr)
    chain_apps = max(0, chain_depth_of(expr))
    product_apps = max(0, int(inv.get("n_factors") or 0) - 1) if inv.get("has_product") else 0
    # Quotient not yet Spec-native; leave 0
    coef_span = 0

    def walk_coefs(e: ExprAST) -> None:
        nonlocal coef_span
        if isinstance(e, Const) and isinstance(e.value, int):
            coef_span = max(coef_span, abs(int(e.value)))
        elif isinstance(e, Add):
            for t in e.terms:
                walk_coefs(t)
        elif isinstance(e, Mul):
            for f in e.factors:
                walk_coefs(f)
        elif isinstance(e, Pow):
            if isinstance(e.exp, int):
                coef_span = max(coef_span, abs(int(e.exp)))
            walk_coefs(e.base)
        elif isinstance(e, Fn):
            walk_coefs(e.arg)

    walk_coefs(expr)
    ans_len = len(answer_latex or "")
    return {
        "answer_len": ans_len,
        "nest_depth": int(inv.get("nest_depth") or 0),
        "chain_applications": chain_apps,
        "product_applications": product_apps,
        "quotient_applications": 0,
        "n_factors": int(inv.get("n_factors") or 0),
        "n_terms": int(inv.get("n_terms") or 0),
        "degree_max": int(inv.get("degree_max") or 0),
        "coef_abs_max": coef_span,
        "has_fn_power": bool(inv.get("has_fn_power")),
        "derivative_order": order,
        "methods": sorted(methods),
        "n_fn_nodes": _count_fn_nodes(expr),
    }


def _render_deriv_legacy(
    expr: ExprAST, d_expr: ExprAST, spec: ExpressionSpec
) -> str | None:
    """Match legacy string derivative forms for common patterns."""
    var = spec.variable

    def _mono_power(coef: int | Fraction, exp: PowerExp) -> str:
        """Render ``coef · x^{exp}`` for power-rule answers."""
        if isinstance(exp, int):
            if exp == 0:
                if isinstance(coef, Fraction) and coef.denominator != 1:
                    return frac_latex(coef)
                return str(int(coef))
            if exp == 1:
                if isinstance(coef, Fraction) and coef.denominator != 1:
                    return f"{frac_latex(coef)}{var}"
                return _mono(int(coef), var, 1)
            if isinstance(coef, Fraction) and coef.denominator != 1:
                return rf"{frac_latex(coef)}{var}^{{{exp}}}"
            return _mono(int(coef), var, exp)
        exp_s = _power_exp_latex(exp)
        if isinstance(coef, Fraction) and coef.denominator != 1:
            return rf"{frac_latex(coef)}{var}^{{{exp_s}}}"
        if isinstance(coef, Fraction):
            coef = int(coef)
        if coef == 1:
            return rf"{var}^{{{exp_s}}}"
        if coef == -1:
            return rf"-{var}^{{{exp_s}}}"
        return rf"{coef}{var}^{{{exp_s}}}"

    # Bare monomial x^n / x^p
    if isinstance(expr, Pow) and isinstance(expr.base, Var):
        if isinstance(expr.exp, int):
            n = int(expr.exp)
            if n == 0:
                return "0"
            if n == 1:
                return "1"
            return _mono_power(n, n - 1)
        if isinstance(expr.exp, Fraction):
            p, q = expr.exp.numerator, expr.exp.denominator
            return _mono_power(Fraction(p, q), Fraction(p - q, q))
        if isinstance(expr.exp, SymConst):
            c_s = _power_exp_latex(expr.exp)
            new_s = _power_exp_latex(SymOffset(expr.exp, -1))
            return _juxtapose_coef_body(c_s, rf"{var}^{{{new_s}}}")

    if (
        isinstance(expr, Mul)
        and len(expr.factors) == 2
        and isinstance(expr.factors[0], Const)
        and isinstance(expr.factors[0].value, int)
        and isinstance(expr.factors[1], Pow)
        and isinstance(expr.factors[1].base, Var)
    ):
        c = int(expr.factors[0].value)
        exp = expr.factors[1].exp
        if isinstance(exp, int):
            n = int(exp)
            if n == 0:
                return "0"
            if n == 1:
                return str(c)
            return _mono_power(c * n, n - 1)
        if isinstance(exp, Fraction):
            return _mono_power(Fraction(c) * exp, exp - Fraction(1))
        if isinstance(exp, SymConst):
            # c·π·x^{π-1} — keep symbolic coefficient visible
            c_s = _power_exp_latex(exp)
            new_s = _power_exp_latex(SymOffset(exp, -1))
            body = _juxtapose_coef_body(c_s, rf"{var}^{{{new_s}}}")
            if c == 1:
                return body
            if c == -1:
                return f"-{body}" if not body.startswith("-") else rf"-\left({body}\right)"
            return f"{c}{body}"

    # Neg monomial -x^n
    if (
        isinstance(expr, Mul)
        and len(expr.factors) == 2
        and isinstance(expr.factors[0], Const)
        and expr.factors[0].value == -1
        and isinstance(expr.factors[1], Pow)
        and isinstance(expr.factors[1].base, Var)
        and isinstance(expr.factors[1].exp, int)
    ):
        n = int(expr.factors[1].exp)
        if n == 0:
            return "0"
        if n == 1:
            return "-1"
        return _mono_power(-n, n - 1)

    # Dense poly sum
    if isinstance(expr, Add):
        poly = _try_poly_coeffs(expr)
        if poly is not None:
            coeffs, v = poly
            d_coeffs = []
            deg = len(coeffs) - 1
            for i, coef in enumerate(coeffs[:-1]):
                d_coeffs.append(coef * (deg - i))
            return format_polynomial_latex(d_coeffs, variable=v) if any(d_coeffs) else "0"

    # Linear ax+b → a
    if isinstance(expr, Add) or True:
        poly = _try_poly_coeffs(expr) if isinstance(expr, Add) else None
        if poly and len(poly[0]) == 2:
            return str(poly[0][0])

    # Product u·v → u'v + uv' with minimal factor parens
    if isinstance(expr, Mul) and len(expr.factors) == 2 and spec.require_product:
        u, v = expr.factors
        u_b = render_latex(u, paren_style="minimal")
        v_b = render_latex(v, paren_style="minimal")
        u_d_ast = _simplify_expr(differentiate(u, spec.variable))
        v_d_ast = _simplify_expr(differentiate(v, spec.variable))
        u_d = _fn_deriv_latex(u, spec) or _legacy_atom_deriv(u_d_ast, spec) or render_latex(
            u_d_ast, paren_style="minimal"
        )
        v_d = _fn_deriv_latex(v, spec) or _legacy_atom_deriv(v_d_ast, spec) or render_latex(
            v_d_ast, paren_style="minimal"
        )
        return (
            f"{_juxtapose_product_factors([_wrap_as_product_factor(u_d), _wrap_as_product_factor(v_b)])}"
            f"+{_juxtapose_product_factors([_wrap_as_product_factor(u_b), _wrap_as_product_factor(v_d)])}"
        )

    # (inner)^c — integer / Fraction / SymConst (do not expand binomials)
    if (
        isinstance(expr, Pow)
        and not isinstance(expr.base, Var)
        and isinstance(expr.exp, (int, Fraction, SymConst))
    ):
        exp = expr.exp
        if isinstance(exp, int):
            n = int(exp)
            inner_b = render_latex(expr.base, paren_style="minimal")
            inner_d = (
                _fn_deriv_latex(expr.base, spec)
                or render_latex(
                    differentiate(expr.base, spec.variable), paren_style="minimal"
                )
            )
            power_part = (
                rf"\left({inner_b}\right)"
                if n - 1 == 1
                else rf"\left({inner_b}\right)^{{{n - 1}}}"
            )
            if inner_d == "1":
                return f"{n}{power_part}"
            return rf"{n}{power_part}\left({inner_d}\right)"

        # Fraction / SymConst: c·(inner)^{c-1}·(inner)'
        c_s = _power_exp_latex(exp)
        new_exp_s = _power_exp_latex(_exp_minus_one(exp))
        inner_b = render_latex(expr.base, paren_style="minimal")
        inner_d = (
            _fn_deriv_latex(expr.base, spec)
            or render_latex(
                differentiate(expr.base, spec.variable), paren_style="minimal"
            )
        )
        power_part = rf"\left({inner_b}\right)^{{{new_exp_s}}}"
        if inner_d == "1":
            return f"{c_s}{power_part}"
        return rf"{c_s}{power_part}\left({inner_d}\right)"

    # Elementary functions
    fn_d = _fn_deriv_latex(expr, spec)
    if fn_d is not None:
        return fn_d

    return None


def _legacy_atom_deriv(d_expr: ExprAST, spec: ExpressionSpec) -> str | None:
    """Compact latex for simple algebraic derivatives (monomials / linears / polys)."""
    if isinstance(d_expr, Const) and isinstance(d_expr.value, int):
        return str(d_expr.value)
    if isinstance(d_expr, Var):
        return d_expr.name
    if isinstance(d_expr, Pow) and isinstance(d_expr.base, Var) and isinstance(d_expr.exp, int):
        return _mono(1, spec.variable, int(d_expr.exp))
    if (
        isinstance(d_expr, Mul)
        and len(d_expr.factors) == 2
        and isinstance(d_expr.factors[0], Const)
        and isinstance(d_expr.factors[0].value, int)
    ):
        c = int(d_expr.factors[0].value)
        rest = d_expr.factors[1]
        if isinstance(rest, Var):
            return _mono(c, spec.variable, 1)
        if isinstance(rest, Pow) and isinstance(rest.base, Var) and isinstance(rest.exp, int):
            return _mono(c, spec.variable, int(rest.exp))
    if isinstance(d_expr, Add):
        poly = _try_poly_coeffs(d_expr)
        if poly is not None:
            return format_polynomial_latex(poly[0], variable=poly[1])
    return None


def _is_simple_fn_arg(arg: ExprAST) -> bool:
    """Var or k·var — safe for legacy single-factor Fn derivative latex."""
    if isinstance(arg, Var):
        return True
    return (
        isinstance(arg, Mul)
        and len(arg.factors) == 2
        and isinstance(arg.factors[0], Const)
        and isinstance(arg.factors[1], Var)
    )


def _fn_deriv_latex(expr: ExprAST, spec: ExpressionSpec) -> str | None:
    if not isinstance(expr, Fn):
        return None
    name, arg = expr.name, expr.arg
    # Nested / rich args: use full AST derivative render (preserves chain factors)
    if not _is_simple_fn_arg(arg):
        return None
    arg_s = render_latex(arg, paren_style="minimal")
    darg = differentiate(arg, spec.variable)
    darg_s = render_latex(darg, paren_style="minimal")

    if name == "sin":
        if darg_s == "1":
            return rf"\cos({arg_s})"
        if isinstance(arg, Mul) and isinstance(arg.factors[0], Const):
            k = arg.factors[0].value
            return rf"{k}\cos({arg_s})"
        return rf"\cos\left({arg_s}\right)\left({darg_s}\right)"
    if name == "cos":
        if darg_s == "1":
            return rf"-\sin({arg_s})"
        if isinstance(arg, Mul) and isinstance(arg.factors[0], Const):
            k = arg.factors[0].value
            return rf"-{k}\sin({arg_s})"
        return rf"-\sin\left({arg_s}\right)\left({darg_s}\right)"
    if name == "tan":
        if darg_s == "1":
            return rf"\sec^{{2}}({arg_s})"
        if isinstance(arg, Mul) and isinstance(arg.factors[0], Const):
            k = arg.factors[0].value
            return rf"{k}\sec^{{2}}({arg_s})"
        return rf"\sec^{{2}}\left({arg_s}\right)\left({darg_s}\right)"
    if name == "exp":
        body = rf"e^{{{arg_s}}}"
        if darg_s == "1":
            return body
        if isinstance(darg, Const) and isinstance(darg.value, int):
            return rf"{darg.value}{body}"
        return rf"{body}\left({darg_s}\right)"
    if name == "ln":
        if darg_s == "1":
            return rf"\frac{{1}}{{{arg_s}}}"
        if isinstance(darg, Const) and isinstance(darg.value, int):
            return rf"\frac{{{darg.value}}}{{{arg_s}}}"
        return rf"\frac{{1}}{{{arg_s}}}\left({darg_s}\right)"
    if name == "arcsin":
        if isinstance(arg, Mul) and isinstance(arg.factors[0], Const):
            k = arg.factors[0].value
            return rf"\frac{{{k}}}{{\sqrt{{1-({arg_s})^{{2}}}}}}"
        return rf"\frac{{1}}{{\sqrt{{1-{arg_s}^{{2}}}}}}"
    if name == "arccos":
        if isinstance(arg, Mul) and isinstance(arg.factors[0], Const):
            k = arg.factors[0].value
            return rf"-\frac{{{k}}}{{\sqrt{{1-({arg_s})^{{2}}}}}}"
        return rf"-\frac{{1}}{{\sqrt{{1-{arg_s}^{{2}}}}}}"
    if name == "arctan":
        if isinstance(arg, Mul) and isinstance(arg.factors[0], Const):
            k = arg.factors[0].value
            return rf"\frac{{{k}}}{{1+({arg_s})^{{2}}}}"
        return rf"\frac{{1}}{{1+{arg_s}^{{2}}}}"
    if name == "sinh":
        if isinstance(arg, Mul) and isinstance(arg.factors[0], Const):
            k = arg.factors[0].value
            return rf"{k}\cosh({arg_s})"
        return rf"\cosh({arg_s})"
    if name == "cosh":
        if isinstance(arg, Mul) and isinstance(arg.factors[0], Const):
            k = arg.factors[0].value
            return rf"{k}\sinh({arg_s})"
        return rf"\sinh({arg_s})"
    if name == "sqrt":
        # d/dx sqrt(ax+b) = a/(2 sqrt(ax+b))
        if isinstance(darg, Const) and isinstance(darg.value, int):
            a = darg.value
            std = arg_s
            return rf"\frac{{{a}}}{{2\sqrt{{{std}}}}}"
        return rf"\frac{{1}}{{2\sqrt{{{arg_s}}}}}"
    return None


def latex_pair_from_spec(
    spec: ExpressionSpec, *, rng: random.Random | None = None
) -> PolyLatexPair:
    """Convenience: Spec → PolyLatexPair with class/method tags."""
    expr, _d, body, deriv, inv = sample_and_differentiate(spec, rng=rng)
    return PolyLatexPair(
        body_latex=body,
        deriv_latex=deriv,
        function_classes=function_classes_of(expr),
        methods_used=methods_used_of(expr),
        chain_depth=chain_depth_of(expr),
    )
