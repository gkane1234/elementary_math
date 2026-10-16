"""Structure-dependent edits for an expression tree.

The catalog form and the coefficients are chosen first. This module then reads
that tree, lists the actions the tree can support, and applies a random count
of them. Weights live on ``EDIT_CATALOG`` so a reader can see each action and
how often it is drawn. Ordinary actions are rated higher than wraps.

Rules
-----
* Algebraic factoring only. ``3x+3`` can become ``3(x+1)``. A bare ``6`` is not
  split into ``2·3``.
* A new factor stays outside a sum. ``e^{3x+3}`` can become ``e^{2(3x+3)}``.
  It does not become ``e^{6x+6}``.
* At most one wrap. ``e^{3x+3}`` can become ``1/e^{-3x-3}``.
* After the edits, adjacent constant factors of a sum are multiplied together.
  ``2·3(x+1)`` is presented as ``6(x+1)``. ``e^{2(3x+3)}`` is left alone.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from question_engine.frameworks.primitives.poly_expression import (
    Add,
    Const,
    ExprAST,
    Fn,
    Mul,
    Pow,
    Var,
)


@dataclass(frozen=True)
class EditAction:
    """One kind of change that can be applied to a matching part of a tree."""

    action_id: str
    part: str
    summary: str
    weight: float
    kind: str  # rewrite (same function), value (function changes), wrap
    coef_max: int = 4


# Readable weights. Higher means more common. Wraps stay low.
EDIT_CATALOG: tuple[EditAction, ...] = (
    EditAction(
        "factor_common_sum",
        "sum",
        "Factor a common integer out of a sum. 3x+3 becomes 3(x+1).",
        3.0,
        "rewrite",
    ),
    EditAction(
        "multiply_sum_unexpanded",
        "sum",
        "Multiply a sum by an integer and do not distribute. 3x+3 becomes 2(3x+3).",
        2.0,
        "value",
        coef_max=4,
    ),
    EditAction(
        "negate",
        "expression",
        "Multiply the whole expression by -1. e^{3x+3} becomes -e^{3x+3}.",
        2.0,
        "value",
    ),
    EditAction(
        "multiply_outside",
        "function_or_factored_sum",
        "Multiply a function, or an already factored sum, from the outside.",
        2.0,
        "value",
        coef_max=4,
    ),
    EditAction(
        "reciprocal_exp_wrap",
        "exp",
        "Write e^{u} as 1/e^{-u}. Same function. At most one wrap per question.",
        0.35,
        "wrap",
    ),
)


_Path = tuple[int, ...]


def _int_coef(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, Fraction) and value.denominator == 1:
        return int(value.numerator)
    return None


def _children(expr: ExprAST) -> tuple[ExprAST, ...]:
    if isinstance(expr, Add):
        return expr.terms
    if isinstance(expr, Mul):
        return expr.factors
    if isinstance(expr, Pow):
        return (expr.base,)
    if isinstance(expr, Fn):
        return (expr.arg,)
    return ()


def _with_children(expr: ExprAST, kids: tuple[ExprAST, ...]) -> ExprAST:
    if isinstance(expr, Add):
        return Add(kids)
    if isinstance(expr, Mul):
        return Mul(kids)
    if isinstance(expr, Pow):
        return Pow(kids[0], expr.exp)
    if isinstance(expr, Fn):
        return Fn(expr.name, kids[0])
    return expr


def _replace(expr: ExprAST, path: _Path, new: ExprAST) -> ExprAST:
    if not path:
        return new
    kids = list(_children(expr))
    kids[path[0]] = _replace(kids[path[0]], path[1:], new)
    return _with_children(expr, tuple(kids))


def _walk(expr: ExprAST, path: _Path = ()) -> list[tuple[_Path, ExprAST]]:
    found = [(path, expr)]
    for i, child in enumerate(_children(expr)):
        found.extend(_walk(child, path + (i,)))
    return found


def _monomial(term: ExprAST) -> tuple[int, int, str | None] | None:
    """Return ``(coef, degree, var)`` for an integer monomial, or None."""
    if isinstance(term, Const):
        coef = _int_coef(term.value)
        if coef is None:
            return None
        return coef, 0, None
    if isinstance(term, Var):
        return 1, 1, term.name
    if isinstance(term, Pow) and isinstance(term.base, Var) and isinstance(term.exp, int):
        if term.exp < 1:
            return None
        return 1, int(term.exp), term.base.name
    if isinstance(term, Mul) and len(term.factors) == 2 and isinstance(term.factors[0], Const):
        coef = _int_coef(term.factors[0].value)
        rest = term.factors[1]
        if coef is None:
            return None
        if isinstance(rest, Var):
            return coef, 1, rest.name
        if isinstance(rest, Pow) and isinstance(rest.base, Var) and isinstance(rest.exp, int):
            if rest.exp < 1:
                return None
            return coef, int(rest.exp), rest.base.name
    return None


def _gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def _sum_content(expr: Add) -> tuple[int, list[tuple[int, int, str | None]]] | None:
    """Common integer content of a sum of two or more monomials.

    A one-term coefficient is not factored. ``6x`` stays ``6x``.
    """
    if len(expr.terms) < 2:
        return None
    parsed: list[tuple[int, int, str | None]] = []
    var: str | None = None
    for term in expr.terms:
        mono = _monomial(term)
        if mono is None or mono[0] == 0:
            return None
        coef, degree, term_var = mono
        if term_var is not None:
            if var is None:
                var = term_var
            elif term_var != var:
                return None
        parsed.append((coef, degree, term_var))
    g = 0
    for coef, _degree, _var in parsed:
        g = _gcd(g, coef)
    if g < 2:
        return None
    if all(coef < 0 for coef, _d, _v in parsed):
        g = -g
    return g, parsed


def _rebuild_monomial(coef: int, degree: int, var: str | None) -> ExprAST:
    if degree == 0 or var is None:
        return Const(coef)
    body: ExprAST = Var(var) if degree == 1 else Pow(Var(var), degree)
    if coef == 1:
        return body
    return Mul((Const(coef), body))


def _factor_sum(expr: Add) -> ExprAST | None:
    content = _sum_content(expr)
    if content is None:
        return None
    g, parsed = content
    terms = []
    for coef, degree, var in parsed:
        new_coef = coef // g
        if new_coef == 0:
            continue
        terms.append(_rebuild_monomial(new_coef, degree, var))
    if len(terms) < 2:
        return None
    return Mul((Const(g), Add(tuple(terms))))


def _factor_choices(coef_abs_max: int, action: EditAction) -> list[int]:
    hi = min(int(action.coef_max), int(coef_abs_max))
    return [i for i in range(-hi, hi + 1) if abs(i) >= 2]


def _is_negated(expr: ExprAST) -> bool:
    return (
        isinstance(expr, Mul)
        and bool(expr.factors)
        and isinstance(expr.factors[0], Const)
        and _int_coef(expr.factors[0].value) == -1
    )


def _contains_add(expr: ExprAST) -> bool:
    if isinstance(expr, Add):
        return True
    return any(_contains_add(child) for child in _children(expr))


def _legal(
    expr: ExprAST,
    *,
    wrap_used: bool,
    coef_abs_max: int,
) -> list[tuple[EditAction, _Path]]:
    by_id = {action.action_id: action for action in EDIT_CATALOG}
    options: list[tuple[EditAction, _Path]] = []
    for path, node in _walk(expr):
        if isinstance(node, Add) and _factor_sum(node) is not None:
            options.append((by_id["factor_common_sum"], path))
        if isinstance(node, Add) and _factor_choices(coef_abs_max, by_id["multiply_sum_unexpanded"]):
            options.append((by_id["multiply_sum_unexpanded"], path))
        if isinstance(node, Fn) and _factor_choices(coef_abs_max, by_id["multiply_outside"]):
            options.append((by_id["multiply_outside"], path))
        if (
            isinstance(node, Mul)
            and _contains_add(node)
            and _factor_choices(coef_abs_max, by_id["multiply_outside"])
        ):
            options.append((by_id["multiply_outside"], path))
        if (
            not wrap_used
            and isinstance(node, Fn)
            and node.name == "exp"
        ):
            options.append((by_id["reciprocal_exp_wrap"], path))
    if not _is_negated(expr):
        options.append((by_id["negate"], ()))
    return [item for item in options if item[0].weight > 0]


def _pick(
    rng: random.Random, options: list[tuple[EditAction, _Path]]
) -> tuple[EditAction, _Path]:
    weights = [max(0.0, action.weight) for action, _path in options]
    return rng.choices(options, weights=weights, k=1)[0]


def _negate_affine(expr: ExprAST) -> ExprAST:
    if isinstance(expr, Add):
        parsed = []
        for term in expr.terms:
            mono = _monomial(term)
            if mono is None:
                return Mul((Const(-1), expr))
            parsed.append(mono)
        terms = [
            _rebuild_monomial(-coef, degree, var) for coef, degree, var in parsed
        ]
        return Add(tuple(terms))
    if isinstance(expr, Const):
        coef = _int_coef(expr.value)
        if coef is not None:
            return Const(-coef)
    if isinstance(expr, Mul) and expr.factors and isinstance(expr.factors[0], Const):
        coef = _int_coef(expr.factors[0].value)
        if coef is not None:
            return Mul((Const(-coef),) + expr.factors[1:])
    return Mul((Const(-1), expr))


def _apply_at(
    expr: ExprAST,
    action: EditAction,
    path: _Path,
    rng: random.Random,
    coef_abs_max: int,
) -> tuple[ExprAST, dict[str, Any]] | None:
    node = expr if not path else _node_at(expr, path)
    record: dict[str, Any] = {
        "action_id": action.action_id,
        "part": action.part,
        "kind": action.kind,
    }
    if action.action_id == "factor_common_sum":
        if not isinstance(node, Add):
            return None
        factored = _factor_sum(node)
        if factored is None:
            return None
        return _replace(expr, path, factored), record
    if action.action_id in {"multiply_sum_unexpanded", "multiply_outside"}:
        choices = _factor_choices(coef_abs_max, action)
        if not choices:
            return None
        factor = int(rng.choice(choices))
        record["factor"] = factor
        return _replace(expr, path, Mul((Const(factor), node))), record
    if action.action_id == "negate":
        return Mul((Const(-1), expr)), record
    if action.action_id == "reciprocal_exp_wrap":
        if not isinstance(node, Fn) or node.name != "exp":
            return None
        flipped = _negate_affine(node.arg)
        wrapped = Pow(Fn("exp", flipped), -1)
        return _replace(expr, path, wrapped), record
    return None


def _node_at(expr: ExprAST, path: _Path) -> ExprAST:
    node = expr
    for index in path:
        node = _children(node)[index]
    return node


def _flatten_mul(factors: tuple[ExprAST, ...]) -> list[ExprAST]:
    flat: list[ExprAST] = []
    for factor in factors:
        if isinstance(factor, Mul):
            flat.extend(_flatten_mul(factor.factors))
        else:
            flat.append(factor)
    return flat


def clean_adjacent_constants(expr: ExprAST) -> ExprAST:
    """Multiply adjacent constant factors of a sum. Do not distribute over a sum.

    ``2·3(x+1)`` becomes ``6(x+1)``. ``2(3x+3)`` stays ``2(3x+3)``.
    """
    kids = tuple(clean_adjacent_constants(child) for child in _children(expr))
    if kids:
        expr = _with_children(expr, kids)
    if not isinstance(expr, Mul):
        return expr
    flat = _flatten_mul(expr.factors)
    consts: list[int] = []
    rest: list[ExprAST] = []
    for factor in flat:
        if isinstance(factor, Const):
            coef = _int_coef(factor.value)
            if coef is not None and not rest:
                consts.append(coef)
                continue
        rest.append(factor)
    if len(consts) < 2 or not any(isinstance(part, Add) for part in rest):
        if flat == list(expr.factors):
            return expr
        return Mul(tuple(flat))
    product = 1
    for coef in consts:
        product *= coef
    if product == 1:
        combined: list[ExprAST] = rest
    else:
        combined = [Const(product), *rest]
    if len(combined) == 1:
        return combined[0]
    return Mul(tuple(combined))


def apply_expression_edits(
    expr: ExprAST,
    rng: random.Random,
    *,
    cap: int,
    coef_abs_max: int,
) -> tuple[ExprAST, dict[str, Any]]:
    """Apply up to ``cap`` catalog edits. The count is uniform on 0..cap."""
    pool = _legal(expr, wrap_used=False, coef_abs_max=coef_abs_max)
    applied: list[dict[str, Any]] = []
    cap = max(0, int(cap))
    if cap > 0 and pool:
        count = rng.randint(0, cap)
        wrap_used = False
        for _ in range(count):
            options = _legal(expr, wrap_used=wrap_used, coef_abs_max=coef_abs_max)
            if not options:
                break
            action, path = _pick(rng, options)
            result = _apply_at(expr, action, path, rng, coef_abs_max)
            if result is None:
                continue
            expr, record = result
            applied.append(record)
            if action.kind == "wrap":
                wrap_used = True
        if applied:
            expr = clean_adjacent_constants(expr)
    return expr, {
        "edit_cap": cap,
        "edit_pool_size": len(pool),
        "edits_applied": applied,
    }


def catalog_rows() -> list[dict[str, Any]]:
    """Plain rows for tests and for anyone reading the weights."""
    return [
        {
            "action_id": action.action_id,
            "part": action.part,
            "summary": action.summary,
            "weight": action.weight,
            "kind": action.kind,
            "coef_max": action.coef_max,
        }
        for action in EDIT_CATALOG
    ]
