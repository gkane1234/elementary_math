"""Precalculus / Calculus effort scorers (parseable prompts).

Kept separate from ``effort.py`` to reduce merge contention with PA/A1 agents.
Imported and registered from ``effort.py`` via ``register_precalc_calc_scorers``.
"""

from __future__ import annotations

import math
import re
from typing import Any

EffortScorer = callable  # noqa: A001 — local alias; real type used at register site


def _clip(e: float) -> float:
    return round(min(max(e, 0.0), 25.0), 1)


def _term_count(expr: str) -> int:
    # Split on + / - outside braces roughly.
    body = expr.strip()
    if not body:
        return 0
    parts = re.split(r"(?<!\{)\s*[+\-]\s*(?![^}]*\})", body)
    return max(1, len([p for p in parts if p.strip()]))


def _max_power(expr: str) -> int:
    powers = [int(m) for m in re.findall(r"\^\{(-?\d+)\}", expr)]
    powers += [int(m) for m in re.findall(r"\^(-?\d+)", expr)]
    return max(powers) if powers else (1 if re.search(r"[a-zA-Z]", expr) else 0)


def effort_limit(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Direct / infinity polynomial limits."""
    feats: dict[str, Any] = {}
    p = prompt.replace(" ", "")
    if r"\infty" in prompt or r"-\infty" in prompt:
        feats["kind"] = "at_infinity"
        e = 8.0
        if r"\frac" in prompt:
            e += 3.0
            feats["rational"] = True
        e += 1.5 * min(4, _max_power(prompt))
        return _clip(e), feats
    m = re.search(r"\\lim_\{[^}]*\\to\s*(-?\d+)", prompt)
    approach = int(m.group(1)) if m else 0
    feats["approach"] = approach
    feats["kind"] = "direct"
    terms = _term_count(re.sub(r".*\\left\(|.*\\lim_[^]]*\]", "", prompt))
    # Fallback: count + signs in poly body
    body_m = re.search(r"\\left\((.*)\\right\)", prompt)
    body = body_m.group(1) if body_m else prompt
    terms = max(terms, _term_count(body))
    pwr = _max_power(body)
    feats["terms"] = terms
    feats["power"] = pwr
    e = 2.0 + 2.0 * max(0, terms - 1) + 1.5 * max(0, pwr - 1)
    if abs(approach) >= 8:
        e += 1.5
    if r"\frac" in prompt:
        e += 4.0
        feats["rational"] = True
    return _clip(e), feats


def effort_derivative_power(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {"form": "power"}
    body_m = re.search(
        r"(?:\\left\[|\\left\()(.*)(?:\\right\]|\\right\))",
        prompt,
        re.DOTALL,
    )
    body = body_m.group(1) if body_m else prompt
    if r"\frac{1}{" in body or "^{-" in body:
        feats["neg_power"] = True
        e = 10.0
    elif "/" in body and "frac" in body:
        feats["fractional_power"] = True
        e = 12.0
    else:
        terms = _term_count(body)
        pwr = _max_power(body)
        feats["terms"] = terms
        feats["power"] = pwr
        e = 2.5 + 2.0 * max(0, terms - 1) + 1.8 * max(0, pwr - 1)
    return _clip(e), feats


def effort_derivative_rules(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Product / quotient / chain / trig / ln-exp structure heuristics."""
    feats: dict[str, Any] = {}
    p = prompt
    e = 6.0
    if r"\frac{" in p and r"}{" in p and "d}{d" not in p.replace(r"\frac{d}{d", ""):
        # Quotient-looking (inner frac besides d/dx)
        inner = p.count(r"\frac{")
        if inner >= 2 or (r"\frac{" in p and r"\frac{d}{d" in p and p.count(r"\frac{") >= 2):
            feats["form"] = "quotient"
            e = 10.0
        elif r"^{-1}" in p:
            feats["form"] = "quotient_inv"
            e = 11.0
    if r"\left(" in p and r"\right)\left(" in p.replace(" ", ""):
        feats["form"] = feats.get("form") or "product"
        e = max(e, 8.0)
    if r"\cdot" in p or r")(" in p.replace(" ", ""):
        feats["form"] = feats.get("form") or "product"
        e = max(e, 8.0)
    # Chain: composition (sin/cos/ln/exp of non-x) or outer power
    if re.search(r"\\(?:sin|cos|tan|ln|log|e\^)\\left\(", p) or re.search(
        r"\\(?:sin|cos|tan|ln)\([^x)]", p
    ):
        feats["form"] = feats.get("form") or "chain_transcendental"
        e = max(e, 12.0)
    if re.search(r"\\left\([^)]+\\right\)\^\{\d+\}", p) or re.search(
        r"\([^)]+\)\^\{\d+\}", p
    ):
        feats["form"] = feats.get("form") or "chain_power"
        e = max(e, 9.0)
    # Power of special: \sin^{2}, \tan^{3}, \ln^{2}
    if re.search(r"\\(?:sin|cos|tan|ln|arcsin|arccos|arctan)\^\{", p):
        feats["fn_power"] = True
        e = max(e, 11.0)
        e += 1.5
    if r"\sin" in p or r"\cos" in p or r"\tan" in p:
        e += 2.0
        feats["trig"] = True
    if r"\ln" in p or r"e^{" in p or r"\log" in p:
        e += 2.0
        feats["exp_log"] = True
    if r"\arcsin" in p or r"\arccos" in p or r"\arctan" in p:
        e += 2.5
        feats["invtrig"] = True
    # Nesting depth proxy: count nested specials / left-delims in body
    nest_proxy = min(5, p.count(r"\left(") + p.count(r"\sin") + p.count(r"\cos")
                     + p.count(r"\tan") + p.count(r"\ln") + p.count(r"e^{") - 1)
    if nest_proxy >= 2:
        feats["nest_proxy"] = nest_proxy
        e += 1.2 * (nest_proxy - 1)
    # Higher-order prompts
    if r"d^{2}" in p or r"d^2" in p or r"d^{{2}}" in p:
        feats["derivative_order"] = 2
        e += 4.0
    elif r"d^{3}" in p or r"d^3" in p or r"d^{{3}}" in p:
        feats["derivative_order"] = 3
        e += 6.0
    pwr = _max_power(p)
    if pwr >= 3:
        e += 1.5
        feats["power"] = pwr
    # Answer length / method applications (when answer key present)
    if answer:
        ans_len = len(answer)
        feats["answer_len"] = ans_len
        e += min(6.0, ans_len / 40.0)
        if r"\left(" in answer and answer.count(r"\left(") >= 2:
            feats["product_like_answer"] = True
            e += 1.5
    if not feats.get("form"):
        feats["form"] = "derivative"
        e = max(e, effort_derivative_power(prompt, answer)[0])
    return _clip(e), feats


def effort_integral_power(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {"form": "power_integral"}
    body = prompt
    m = re.search(r"\\int\s*(.*?)\\,", prompt)
    if m:
        body = m.group(1)
    terms = _term_count(body)
    pwr = _max_power(body)
    feats["terms"] = terms
    feats["power"] = pwr
    e = 3.0 + 2.2 * max(0, terms - 1) + 1.5 * max(0, pwr - 1)
    if r"\sin" in prompt or r"\cos" in prompt:
        e += 3.0
        feats["trig"] = True
    if r"\frac" in body:
        e += 2.5
    if "e^{" in prompt or r"\ln" in prompt:
        e += 3.0
        feats["exp_log"] = True
    return _clip(e), feats


def effort_integral_rules(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    e, feats = effort_integral_power(prompt, answer)
    if "u=" in prompt.lower() or "substitution" in prompt.lower():
        e += 4.0
        feats["form"] = "substitution"
    if r"\int" in prompt and r"\left(" in prompt and r"\right)" in prompt:
        # Composition hint
        if re.search(r"\\(?:sin|cos|e\^|ln)", prompt):
            e = max(e, 12.0)
            feats["form"] = feats.get("form") or "composed"
    return _clip(e), feats


def effort_log_evaluate(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {}
    e = 3.0
    if r"\ln" in prompt:
        feats["base"] = "e"
        e += 2.0
    elif r"\log\left" in prompt or r"\log(" in prompt:
        feats["base"] = "10"
        e += 1.0
    else:
        m = re.search(r"\\log_\{(\d+)\}", prompt)
        if m:
            feats["base"] = int(m.group(1))
            if int(m.group(1)) not in (2, 10):
                e += 2.0
    arg_m = re.search(r"\\left\(([^)]+)\\right\)|\(([^)]+)\)", prompt)
    arg = (arg_m.group(1) or arg_m.group(2)) if arg_m else ""
    feats["argument"] = arg
    try:
        aval = float(arg)
        if aval >= 100:
            e += 2.0
        if aval >= 1000:
            e += 2.0
        if not float(aval).is_integer():
            e += 3.0
            feats["non_int_arg"] = True
    except (TypeError, ValueError):
        e += 1.0
    if "change of base" in prompt.lower() or r"\frac{\log" in prompt:
        e += 4.0
        feats["form"] = "change_of_base"
    return _clip(e), feats


def effort_trig_evaluate(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {}
    e = 3.0
    for fn in ("cot", "tan", "sec", "csc", "sin", "cos"):
        if rf"\{fn}" in prompt or f"\\{fn}" in prompt:
            feats["fn"] = fn
            if fn in ("cot", "sec", "csc"):
                e += 3.0
            elif fn == "tan":
                e += 1.5
            break
    deg_m = re.search(r"(-?\d+)\^\\circ", prompt) or re.search(r"(-?\d+)\^\{?\\circ\}?", prompt)
    if not deg_m:
        deg_m = re.search(r"(-?\d+)\^\\circ", prompt.replace(" ", ""))
    # Common patterns: 30^\circ or 30^{\circ}
    deg_m = re.search(r"(-?\d+)\s*\^\s*\\circ", prompt) or re.search(
        r"(-?\d+)\^\{\\circ\}", prompt
    )
    if deg_m:
        deg = abs(int(deg_m.group(1))) % 360
        feats["deg"] = deg
        if deg % 90 == 0:
            e += 0.5
        elif deg % 45 == 0:
            e += 2.0
        elif deg % 30 == 0 or deg % 60 == 0:
            e += 3.5
        else:
            e += 5.0
    if r"\pi" in prompt:
        e += 2.0
        feats["radians"] = True
    return _clip(e), feats


def effort_exp_equation(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {}
    e = 5.0
    if r"\log" in prompt or r"\ln" in prompt:
        feats["needs_log"] = True
        e += 5.0
    bases = re.findall(r"(\d+)\^\{", prompt)
    if bases:
        feats["base"] = int(bases[0])
    if r"\frac" in prompt:
        e += 2.0
    if prompt.count("^") >= 2 or prompt.count("^{") >= 2:
        e += 3.0
        feats["multi_exp"] = True
    return _clip(e), feats


def effort_average_rate(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    nums = [int(x) for x in re.findall(r"-?\d+", prompt)]
    feats: dict[str, Any] = {"n_nums": len(nums)}
    e = 4.0
    if len(nums) >= 2:
        span = abs(nums[0] - nums[1]) if len(nums) >= 2 else 1
        e += min(6.0, 0.4 * span)
    if r"\frac" in prompt:
        e += 2.0
    return _clip(e), feats


def effort_trig_identity(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Fundamental / sum-difference / double-half angle identities."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 6.0
    if "double" in p or "half" in p or "2\\theta" in prompt or "2theta" in p:
        feats["family"] = "double_half"
        e = 9.0
    elif "sum" in p or "difference" in p or "+\\theta" in prompt or "-\\theta" in prompt:
        feats["family"] = "sum_diff"
        e = 8.5
    elif "simplify" in p:
        feats["family"] = "fundamental_simplify"
        e = 5.5
    elif "solve" in p or "equation" in p:
        feats["family"] = "identity_equation"
        e = 8.0
    else:
        feats["family"] = "fundamental"
        e = 6.0
    if "factor" in p:
        e += 1.5
        feats["factoring"] = True
    if prompt.count(r"\sin") + prompt.count(r"\cos") + prompt.count(r"\tan") >= 3:
        e += 1.0
        feats["multi_fn"] = True
    return _clip(e), feats


def effort_inverse_trig(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Evaluate inverse trig / compose with trig."""
    feats: dict[str, Any] = {"task": "inverse_trig"}
    e = 5.0
    if r"\arcsin" in prompt or "arcsin" in prompt.lower() or r"\sin^{-1}" in prompt:
        feats["fn"] = "arcsin"
        e = 5.0
    elif r"\arccos" in prompt or "arccos" in prompt.lower():
        feats["fn"] = "arccos"
        e = 5.5
    elif r"\arctan" in prompt or "arctan" in prompt.lower():
        feats["fn"] = "arctan"
        e = 6.0
    if r"\frac" in prompt:
        e += 1.5
    if r"\pi" in (answer or ""):
        e += 0.5
        feats["exact"] = True
    return _clip(e), feats


def effort_law_of_sines_cosines_pc(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Law of sines / cosines / area (precalc + A2 shared stems)."""
    p = prompt.lower()
    feats: dict[str, Any] = {}
    e = 7.0
    if "cosine" in p or "cosines" in p:
        feats["law"] = "cosines"
        e = 8.5
    elif "area" in p:
        feats["law"] = "area"
        e = 7.5
    else:
        feats["law"] = "sines"
        e = 7.0
    nums = re.findall(r"\d+(?:\.\d+)?", prompt)
    feats["n_given"] = len(nums)
    e += 0.4 * max(0, len(nums) - 3)
    if "ambiguous" in p or "two triangles" in p:
        e += 2.5
        feats["ambiguous"] = True
    return _clip(e), feats


def effort_graph_trig_pc(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Graph y = a sin(bx+c)+d style transforms."""
    feats: dict[str, Any] = {"task": "graph_trig"}
    e = 6.0
    if r"\sin" in prompt:
        feats["fn"] = "sin"
    elif r"\cos" in prompt:
        feats["fn"] = "cos"
    elif r"\tan" in prompt:
        feats["fn"] = "tan"
        e += 1.5
    if re.search(r"\d+\s*\\?(?:sin|cos|tan)", prompt) or re.search(
        r"[a-z]\s*\\?(?:sin|cos|tan)", prompt
    ):
        e += 1.0
        feats["amplitude"] = True
    if "(" in prompt and ("+" in prompt or "-" in prompt):
        e += 1.5
        feats["phase_or_shift"] = True
    return _clip(e), feats


def effort_right_triangle_trig(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """SOHCAHTOA ratios and missing sides/angles."""
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    if "find" in pl and any(fn in prompt for fn in (r"\sin", r"\cos", r"\tan")):
        feats["mode"] = "ratio"
        e = 4.5
        if r"\tan" in prompt:
            e += 1.0
    elif "angle" in pl or r"^\circ" in prompt or r"^{\circ}" in prompt:
        feats["mode"] = "angle_or_side"
        e = 7.0
    else:
        feats["mode"] = "side"
        e = 6.5
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    if nums:
        feats["max_side"] = max(nums)
        e += 0.12 * max(0, max(nums) - 10)
    if "30" in prompt or "60" in prompt or "45" in prompt:
        e += 0.5
        feats["special"] = True
    return _clip(e), feats


def effort_vector(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """2D/3D vector arithmetic, magnitude, dot, cross."""
    feats: dict[str, Any] = {}
    e = 5.0
    if r"\times" in prompt or "\\times" in prompt or "cross" in prompt.lower():
        feats["op"] = "cross"
        e = 10.0
    elif r"\cdot" in prompt or "dot" in prompt.lower():
        feats["op"] = "dot"
        e = 6.5
    elif r"\lVert" in prompt or "magnitude" in prompt.lower() or "norm" in prompt.lower():
        feats["op"] = "magnitude"
        e = 5.5
    elif "+" in prompt or "-" in prompt:
        feats["op"] = "add_sub"
        e = 4.5
    else:
        feats["op"] = "vector"
    # Component count: angle brackets or (a,b,c)
    comps = re.findall(r"\\langle\s*([^\\]+)\\rangle|\((-?\d+),\s*(-?\d+)(?:,\s*(-?\d+))?\)", prompt)
    dim = 2
    if comps:
        # Heuristic: three numbers → 3D
        flat = re.findall(r"-?\d+", comps[0][0] if comps[0][0] else ",".join(comps[0][1:]))
        if len(flat) >= 3 or any(g and g[2] for g in comps if isinstance(g, tuple)):
            dim = 3
    if re.search(r"-?\d+,\s*-?\d+,\s*-?\d+", prompt):
        dim = 3
    feats["dim"] = dim
    if dim >= 3:
        e += 2.0
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums and max(nums) >= 10:
        e += 1.0
        feats["large"] = True
    return _clip(e), feats


def effort_vector_diagram(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Tip-to-tail / opposite / resultant from a described vector diagram."""
    e, feats = effort_vector(prompt, answer)
    e += 1.5
    feats["diagram"] = True
    pl = prompt.lower()
    if "tip-to-tail" in pl or "tip to tail" in pl:
        feats["tip_to_tail"] = True
        e += 0.5
    if "resultant" in pl:
        feats["resultant"] = True
    if "opposite" in pl or "-\\mathbf" in prompt or "-\\mathbf{u}" in prompt:
        feats["opposite"] = True
        e = max(e, 5.0)
    if "magnitude" in pl:
        e += 1.0
    return _clip(e), feats


def effort_counting_pc(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {"mode": "counting"}
    e = 3.5
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    feats["n_factors"] = max(2, len(nums))
    e += 1.2 * max(0, feats["n_factors"] - 2)
    if nums:
        e += 0.15 * max(0, max(nums) - 5)
    return _clip(e), feats


def effort_perm_comb_pc(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    if "ordered" in pl or "permutation" in pl or "arrange" in pl:
        feats["mode"] = "perm"
        e = 6.0
    elif "combination" in pl or "unordered" in pl or "committee" in pl:
        feats["mode"] = "comb"
        e = 5.5
    else:
        feats["mode"] = "mixed"
        e = 6.0
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    if len(nums) >= 2:
        candidates = sorted(nums, reverse=True)
        n, r = candidates[0], candidates[1]
        feats["n"], feats["r"] = n, r
        e += 0.35 * max(0, n - 6) + 0.5 * max(0, r - 2)
    return _clip(e), feats


def effort_probability_pc(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 4.0
    if " or " in pl:
        e = 5.5
        feats["mode"] = "mutually_exclusive"
    elif "both" in pl or " and " in pl or "replace" in pl or "again" in pl:
        e = 6.5
        feats["mode"] = "independent"
        if "replace" in pl or "without" in pl:
            e += 1.0
    else:
        feats["mode"] = "single"
    if "permutation" in pl or "combination" in pl:
        e += 2.0
        feats["uses_counting"] = True
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    if nums:
        e += 0.12 * max(0, max(nums) - 6)
    return _clip(e), feats


def effort_binomial(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {"task": "binomial"}
    e = 6.0
    m_pow = re.search(r"\(([^\)]+)\)\^\{?(\d+)\}?", prompt)
    if m_pow:
        n = int(m_pow.group(2))
        feats["n"] = n
        e += 0.8 * max(0, n - 3)
    m_term = re.search(r"x\^\{?(\d+)\}?", prompt)
    if m_term:
        feats["k"] = int(m_term.group(1))
        e += 0.4 * int(m_term.group(1))
    if re.search(r"\d+\s*\+", prompt) or re.search(r"\(\d+", prompt):
        e += 1.5
        feats["coef"] = True
    return _clip(e), feats


def effort_partial_fractions(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {"task": "partial_fractions"}
    e = 10.0
    dens = prompt.count(r")(") + prompt.count(r"\right)\left(")
    feats["factors"] = dens
    e += 2.0 * dens
    if "^{2}" in prompt or "^2" in prompt:
        e += 2.5
        feats["repeated"] = True
    if r"\frac" in prompt:
        e += 1.0
    return _clip(e), feats


def effort_poly_zeros_writing(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Remainder theorem, writing from roots, FTA, Descartes, rational-zero lists."""
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 6.0
    if "remainder" in pl:
        feats["mode"] = "remainder"
        e = 5.5
    elif "descartes" in pl:
        feats["mode"] = "descartes"
        e = 8.0
    elif "rational zero" in pl or "possible rational" in pl:
        feats["mode"] = "rational_zero"
        e = 7.5
    elif "fundamental theorem" in pl or "how many complex zeros" in pl:
        feats["mode"] = "fta"
        e = 4.0
        m = re.search(r"degree-?\s*\}?\s*(\d+)|degree\s*(\d+)", prompt, re.I)
        if m:
            deg = int(m.group(1) or m.group(2))
            feats["degree"] = deg
            e += 0.5 * deg
    elif "write" in pl and ("root" in pl or "zero" in pl):
        feats["mode"] = "write_from_roots"
        e = 7.0
        if "i" in prompt and ("+" in prompt or "-" in prompt):
            e += 2.5
            feats["complex"] = True
    elif "zero" in pl or "root" in pl:
        feats["mode"] = "find_zeros"
        e = 7.5
    else:
        feats["mode"] = "poly"
    pwr = _max_power(prompt)
    feats["power"] = pwr
    e += 1.2 * max(0, pwr - 2)
    return _clip(e), feats


def effort_conic_pc(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {}
    e = 5.0
    pl = prompt.lower()
    if "write" in pl:
        e += 3.0
        feats["mode"] = "write"
    elif "classify" in pl or "rotation" in pl:
        e += 2.5
        feats["mode"] = "classify"
    else:
        feats["mode"] = "properties"
    if "ellipse" in pl:
        feats["kind"] = "ellipse"
        e += 1.5
    elif "hyperbola" in pl:
        feats["kind"] = "hyperbola"
        e += 2.0
    elif "circle" in pl or "radius" in pl:
        feats["kind"] = "circle"
    elif "parabola" in pl:
        feats["kind"] = "parabola"
        e += 1.0
    if re.search(r"center.*\(-?[1-9]|vertex.*\(-?[1-9]", prompt) or re.search(
        r"\(-?[1-9]\d*,\s*-?\d+\)", prompt
    ):
        e += 2.0
        feats["translated"] = True
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums and max(nums) >= 16:
        e += 1.0
    return _clip(e), feats


def effort_polar(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 6.0
    if "convert" in pl or "rectangular" in pl:
        feats["mode"] = "convert"
        e = 6.5
    elif "complex" in pl or "cis" in pl or r"\cos" in prompt and r"\sin" in prompt:
        feats["mode"] = "complex_polar"
        e = 7.0
    elif "conic" in pl or r"\frac" in prompt:
        feats["mode"] = "polar_conic"
        e = 9.0
    else:
        feats["mode"] = "polar_graph"
        e = 7.5
    if r"\theta" in prompt:
        e += 0.5
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    if nums and max(nums) >= 8:
        e += 1.0
    return _clip(e), feats


def effort_compound_interest_pc(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    pl = prompt.lower()
    compound = "compound" in pl
    e = 6.0 if not compound else 11.0
    feats: dict[str, Any] = {"compound": compound}
    if "semiannual" in pl:
        e += 1.5
    elif "month" in pl:
        e += 2.0
    elif "quarter" in pl:
        e += 1.5
    years = re.search(r"for\s*(\d+)\s*year", pl)
    if years:
        t = int(years.group(1))
        feats["years"] = t
        e += 0.4 * max(0, t - 3)
    if re.search(r"\d+\\?%", prompt):
        e += 0.5
    return _clip(e), feats


def effort_fn_analysis_pc(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Power / inverse / piecewise / extrema / end behavior / transforms."""
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 5.0
    if "piecewise" in pl or r"\begin{cases}" in prompt:
        feats["mode"] = "piecewise"
        e = 8.0
        e += 1.5 * prompt.count(r"\\")
    elif "inverse" in pl:
        feats["mode"] = "inverse"
        e = 6.5
        if r"\frac" in prompt or "^" in prompt:
            e += 2.0
    elif "end behavior" in pl or "extrema" in pl or "increasing" in pl or "decreasing" in pl:
        feats["mode"] = "analysis"
        e = 7.0
        e += 1.5 * max(0, _max_power(prompt) - 1)
    elif "transform" in pl or "graph" in pl:
        feats["mode"] = "transform"
        e = 6.0
        if "-" in prompt or "+" in prompt:
            e += 1.5
    elif "evaluate" in pl or "at" in pl:
        feats["mode"] = "evaluate_power"
        e = 3.5 + 1.2 * max(0, _max_power(prompt) - 1)
    else:
        feats["mode"] = "function"
        e = 5.0 + 1.0 * _max_power(prompt)
    return _clip(e), feats


def effort_rational_poly_eq(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {}
    e = 6.0
    if r"\frac" in prompt:
        feats["kind"] = "rational"
        e = 8.0
    else:
        feats["kind"] = "polynomial"
        e = 6.5
    if ">" in prompt or "<" in prompt or r"\ge" in prompt or r"\le" in prompt:
        e += 2.5
        feats["inequality"] = True
    e += 1.2 * max(0, _term_count(prompt) - 2)
    e += 1.0 * max(0, _max_power(prompt) - 1)
    return _clip(e), feats


def effort_parametric_projectile(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 6.0
    if "maximum height" in pl or "projectile" in pl or "h(t)" in prompt:
        feats["mode"] = "projectile"
        e = 8.0
    elif "parametric" in pl or ("x=" in prompt.replace(" ", "") and "y=" in prompt.replace(" ", "")):
        feats["mode"] = "parametric"
        e = 6.5
    else:
        feats["mode"] = "motion_param"
    pwr = _max_power(prompt)
    e += 1.0 * max(0, pwr - 1)
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    if nums and max(nums) >= 50:
        e += 1.5
    return _clip(e), feats


def effort_power_series_induction(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    if "induction" in pl or "base case" in pl:
        feats["mode"] = "induction"
        e = 9.0
    elif "radius" in pl or "series" in pl or r"\sum" in prompt:
        feats["mode"] = "power_series"
        e = 10.0
        if r"\infty" in prompt:
            e += 1.0
    else:
        feats["mode"] = "series"
        e = 8.0
    return _clip(e), feats


def effort_systems_row(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {"mode": "linear_system"}
    e = 7.0
    eqs = prompt.count("=")
    feats["n_eq"] = eqs
    e += 2.0 * max(0, eqs - 2)
    if "z" in prompt:
        e += 2.0
        feats["three_var"] = True
    return _clip(e), feats


def effort_distance_midpoint(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {}
    pl = prompt.lower()
    e = 4.0
    if "midpoint" in pl:
        feats["mode"] = "midpoint"
        e = 4.0
    else:
        feats["mode"] = "distance"
        e = 5.5
    pts = re.findall(r"\((-?\d+),\s*(-?\d+)(?:,\s*(-?\d+))?\)", prompt)
    if pts and any(p[2] for p in pts):
        e += 2.0
        feats["dim"] = 3
    else:
        feats["dim"] = 2
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums and max(nums) >= 10:
        e += 1.0
    return _clip(e), feats


def effort_def_of_derivative(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Difference-quotient / definition limits."""
    feats: dict[str, Any] = {"form": "definition"}
    e = 8.0
    if r"\frac" in prompt and "h" in prompt:
        e += 2.0
        feats["diff_quot"] = True
    if r"\sin" in prompt or r"\cos" in prompt or r"\sqrt" in prompt:
        e += 2.5
        feats["transcendental"] = True
    if r"\frac{1}{" in prompt or "1/" in prompt.replace(" ", ""):
        e += 2.0
        feats["reciprocal"] = True
    e += 1.0 * max(0, _max_power(prompt) - 1)
    return _clip(e), feats


def effort_implicit_log_diff(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 10.0
    if "logarithmic" in pl:
        feats["mode"] = "log_diff"
        e = 12.0
        if r"^" in prompt or "^{" in prompt:
            e += 2.0
    elif "implicit" in pl:
        feats["mode"] = "implicit"
        e = 11.0
        e += 1.5 * max(0, _max_power(prompt) - 2)
    elif "inverse" in pl or r"f^{-1}" in prompt or "(f^{-1})" in prompt:
        feats["mode"] = "inverse_deriv"
        e = 9.0
    else:
        feats["mode"] = "advanced_diff"
    if r"\sin" in prompt or r"\cos" in prompt or r"e^" in prompt:
        e += 1.5
    return _clip(e), feats


def effort_curve_analysis_calc(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Rolle/MVT, intervals, extrema, concavity, optimization, Newton, differentials."""
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 8.0
    if "rolle" in pl:
        feats["mode"] = "rolle"
        e = 9.0
    elif "mean value" in pl:
        feats["mode"] = "mvt"
        e = 9.5
    elif "optim" in pl or "maximize" in pl or "minimize" in pl or "perimeter" in pl:
        feats["mode"] = "optimization"
        e = 12.0
    elif "newton" in pl:
        feats["mode"] = "newton"
        e = 10.0
    elif "differential" in pl or "find }dy" in pl or "find dy" in pl:
        feats["mode"] = "differential"
        e = 6.0
    elif "concav" in pl:
        feats["mode"] = "concavity"
        e = 8.5
    elif "increasing" in pl or "decreasing" in pl:
        feats["mode"] = "mono"
        e = 8.0
    elif "extrema" in pl or "minimum" in pl or "maximum" in pl:
        feats["mode"] = "extrema"
        e = 8.5
    elif "sketch" in pl:
        feats["mode"] = "sketch"
        e = 11.0
    else:
        feats["mode"] = "analysis"
    e += 1.2 * max(0, _max_power(prompt) - 1)
    e += 0.8 * max(0, _term_count(prompt) - 2)
    return _clip(e), feats


def effort_lhopital(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    e, feats = effort_limit(prompt, answer)
    feats = dict(feats)
    feats["lhopital"] = True
    e = max(e, 9.0) + 3.0
    if r"\sin" in prompt or r"\ln" in prompt or r"e^" in prompt:
        e += 1.5
    return _clip(e), feats


def effort_ibp_sub_integral(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    e, feats = effort_integral_rules(prompt, answer)
    feats = dict(feats)
    pl = prompt.lower()
    if "parts" in pl or (r"\int" in prompt and "e^" in prompt and "x" in prompt):
        feats["form"] = "ibp"
        e = max(e, 12.0) + 2.0
    else:
        feats["form"] = feats.get("form") or "sub"
        e = max(e, 10.0) + 1.5
    return _clip(e), feats


def effort_definite_ftc(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {}
    e = 7.0
    if r"\frac{d}{dx}" in prompt and r"\int" in prompt:
        feats["mode"] = "ftc2"
        e = 10.0
    elif r"\int_" in prompt or r"\int_{" in prompt:
        feats["mode"] = "definite"
        e = 8.0
        bounds = re.findall(r"\\int_\{?(-?\d+)", prompt)
        if len(bounds) >= 1:
            e += 0.5
    elif "average value" in prompt.lower():
        feats["mode"] = "avg_value"
        e = 9.0
    elif "riemann" in prompt.lower() or "midpoint" in prompt.lower():
        feats["mode"] = "riemann"
        e = 7.5
    else:
        feats["mode"] = "area_limit"
        e = 8.5
    e += 1.5 * max(0, _max_power(prompt) - 1)
    e += 1.0 * max(0, _term_count(prompt) - 2)
    return _clip(e), feats


def effort_area_volume(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 9.0
    if "washer" in pl or "disk" in pl:
        feats["mode"] = "disk_washer"
        e = 12.0
    elif "shell" in pl or "cylinder" in pl:
        feats["mode"] = "shell"
        e = 12.5
    elif "cross section" in pl or "semicircle" in pl:
        feats["mode"] = "cross_section"
        e = 13.0
    elif "between" in pl:
        feats["mode"] = "area_between"
        e = 10.0
    else:
        feats["mode"] = "area"
        e = 8.5
    e += 1.0 * max(0, _max_power(prompt) - 1)
    nums = [int(x) for x in re.findall(r"\d+", prompt)]
    if nums and max(nums) >= 5:
        e += 0.8
    return _clip(e), feats


def effort_diff_eq(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    pl = prompt.lower()
    feats: dict[str, Any] = {}
    e = 8.0
    if "slope" in pl and "field" not in pl and "at" in pl:
        feats["mode"] = "slope_field_pt"
        e = 5.0
    elif "slope field" in pl:
        feats["mode"] = "slope_field"
        e = 7.0
    elif "separable" in pl or r"\frac{dy}{dx}" in prompt:
        feats["mode"] = "separable"
        e = 11.0
    elif "growth" in pl or "decay" in pl or "%" in prompt:
        feats["mode"] = "growth_decay"
        e = 10.0
    elif "verify" in pl or "solves" in pl:
        feats["mode"] = "verify"
        e = 7.0
    else:
        feats["mode"] = "de"
    return _clip(e), feats


def effort_table_derivative(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """Table / chain values for (f∘g)' etc."""
    feats: dict[str, Any] = {"mode": "table_diff"}
    e = 7.0
    if r"\circ" in prompt or "circ" in prompt.lower():
        e += 2.0
        feats["composition"] = True
    if "f'" in prompt and "g'" in prompt:
        e += 1.5
    nums = [int(x) for x in re.findall(r"-?\d+", prompt)]
    feats["n_vals"] = len(nums)
    e += 0.3 * max(0, len(nums) - 4)
    return _clip(e), feats


def effort_motion_line(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {"mode": "motion"}
    e = 6.0
    pl = prompt.lower()
    if "acceleration" in pl or "a(" in prompt:
        e += 2.0
        feats["ask"] = "accel"
    elif "velocity" in pl or "v(" in prompt or "find }v" in pl:
        e += 1.0
        feats["ask"] = "vel"
    elif "position" in pl or "s(" in prompt:
        feats["ask"] = "pos"
    e += 1.2 * max(0, _max_power(prompt) - 1)
    return _clip(e), feats


def effort_linear_relation(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    """A1 discrete/continuous relation table / evaluate."""
    feats: dict[str, Any] = {}
    e = 3.5
    if "array" in prompt or "table" in prompt.lower() or "?" in prompt:
        feats["mode"] = "table"
        e = 4.5
    elif ">" in prompt or "<" in prompt:
        feats["mode"] = "inequality_graph"
        e = 3.0
    else:
        feats["mode"] = "evaluate"
        e = 3.5
    nums = [abs(int(x)) for x in re.findall(r"-?\d+", prompt)]
    if nums and max(nums) >= 10:
        e += 1.0
    return _clip(e), feats


def effort_g6_fraction_props(prompt: str, answer: str = "") -> tuple[float, dict[str, Any]]:
    feats: dict[str, Any] = {}
    e = 3.0
    if r"\frac" in prompt:
        feats["mode"] = "fraction_of"
        e = 5.0
        fracs = len(re.findall(r"\\frac\{", prompt))
        e += 1.5 * max(0, fracs - 1)
    else:
        feats["mode"] = "properties"
        e = 2.5
        if r"\cdot" in prompt or "*" in prompt:
            e += 1.0
    return _clip(e), feats


# type_id → scorer
PRECALC_CALC_SCORERS: dict[str, Any] = {
    # Limits (calc + precalc intro)
    "calc_limits_by_direct_evaluation": effort_limit,
    "calc_limits_at_jump_discontinuities_and_kinks": effort_limit,
    "calc_limits_at_removable_discontinuities": effort_limit,
    "calc_limits_at_essential_discontinuities": effort_limit,
    "calc_limits_at_infinity": effort_limit,
    "calc_continuity_determining_and_classifying": effort_limit,
    "pc_limits_by_direct_evaluation": effort_limit,
    "pc_limits_at_removable_discontinuities": effort_limit,
    "pc_limits_at_infinity": effort_limit,
    # Derivatives
    "calc_diff_power_rule": effort_derivative_power,
    "calc_diff_product_rule": effort_derivative_rules,
    "calc_diff_quotient_rule": effort_derivative_rules,
    "calc_diff_chain_rule": effort_derivative_rules,
    "calc_diff_trigonometric": effort_derivative_rules,
    "calc_diff_natural_logarithms_and_exponentials": effort_derivative_rules,
    "calc_diff_other_base_logarithms_and_exponentials": effort_derivative_rules,
    "calc_diff_inverse_trigonometric": effort_derivative_rules,
    "calc_diff_general": effort_derivative_rules,
    "calc_diff_higher_order_derivatives": effort_derivative_rules,
    "calc_diff_average_rates_of_change": effort_average_rate,
    "pc_definition_of_the_derivative": effort_derivative_power,
    "pc_power_rule_for_differentiation": effort_derivative_power,
    # Integrals
    "calc_indef_int_power_rule": effort_integral_power,
    "calc_indef_int_trigonometric": effort_integral_rules,
    "calc_indef_int_logarithmic_rule_and_exponentials": effort_integral_rules,
    "calc_indef_int_power_rule_with_substitution": effort_integral_rules,
    "calc_indef_int_inverse_trigonometric": effort_integral_rules,
    "pc_indefinite_integrals": effort_integral_power,
    # Precalc log / trig / exp
    "pc_evaluating_logarithms": effort_log_evaluate,
    "pc_exponents_and_logarithms": effort_log_evaluate,
    "pc_logarithms_and_exponents_as_inverses": effort_log_evaluate,
    "pc_properties_of_logarithms": effort_log_evaluate,
    "pc_writing_logs_in_terms_of_others": effort_log_evaluate,
    "pc_logarithmic_equations_simple": effort_log_evaluate,
    "pc_logarithmic_equations_hard": effort_log_evaluate,
    "pc_trig_functions_of_any_angle": effort_trig_evaluate,
    "pc_angles_and_angle_measure": effort_trig_evaluate,
    "pc_radians_and_degrees": effort_trig_evaluate,
    "pc_simple_trig_equations": effort_trig_evaluate,
    "pc_exponential_equations_not_requiring_logarithms": effort_exp_equation,
    "pc_exponential_equations_requiring_logarithms": effort_exp_equation,
    # Trig identities / inverse / laws / graphing
    "pc_fundamental_identities": effort_trig_identity,
    "pc_equations_with_factoring_and_fundamental_identities": effort_trig_identity,
    "pc_equations_and_multiple_angle_identities": effort_trig_identity,
    "pc_inverse_trig_functions": effort_inverse_trig,
    "pc_law_of_sines": effort_law_of_sines_cosines_pc,
    "pc_law_of_cosines": effort_law_of_sines_cosines_pc,
    "pc_area_and_laws_of_sines_and_cosines": effort_law_of_sines_cosines_pc,
    "pc_graphing_trig_functions": effort_graph_trig_pc,
    "pc_average_rates_of_change": effort_average_rate,
    "pc_approximating_area_under_a_curve": effort_integral_power,
    "pc_continuity": effort_limit,
    "pc_limits_at_essential_discontinuities": effort_limit,
    "pc_limits_at_kinks_and_jumps": effort_limit,
    # A2 identity leaves (shared stems)
    "a2_trigonometry_angle_sum_difference_identities": effort_trig_identity,
    "a2_trigonometry_double_angle_half_angle_identities": effort_trig_identity,
    "a2_trigonometry_angles_and_angle_measure": effort_trig_evaluate,
    "a2_trigonometry_degrees_and_degrees_minutes_seconds": effort_trig_evaluate,
    # --- Wave: remaining parseable PC / Calc (+ A1/A2/G6 easy wins) ---
    # PC right-triangle trig + identities leftovers
    "pc_right_triangle_trig_finding_ratios": effort_right_triangle_trig,
    "pc_right_triangle_trig_finding_angles_and_sides": effort_right_triangle_trig,
    "pc_sum_and_difference_identities": effort_trig_identity,
    "pc_multiple_angle_identities": effort_trig_identity,
    "pc_product_to_sum_identities": effort_trig_identity,
    # PC functions / analysis
    "pc_power_functions": effort_fn_analysis_pc,
    "pc_transformations_of_graphs": effort_fn_analysis_pc,
    "pc_piecewise_functions": effort_fn_analysis_pc,
    "pc_inverses": effort_fn_analysis_pc,
    "pc_extrema_intervals_of_increase_and_decrease": effort_fn_analysis_pc,
    "pc_polynomial_graphs_real_zeros_and_end_behavior": effort_fn_analysis_pc,
    "pc_graphs_of_rational_functions": effort_fn_analysis_pc,
    "pc_graphing_exponential_functions": effort_fn_analysis_pc,
    "pc_graphing_logarithmic_functions": effort_fn_analysis_pc,
    # PC poly / rational
    "pc_dividing_polynomial_functions": effort_poly_zeros_writing,
    "pc_remainder_theorem_and_bounds_of_real_zeros": effort_poly_zeros_writing,
    "pc_writing_polynomial_functions_and_conjugate_roots": effort_poly_zeros_writing,
    "pc_complex_zeros_and_fundamental_theorem_of_algebra": effort_poly_zeros_writing,
    "pc_rational_equations": effort_rational_poly_eq,
    "pc_polynomial_inequalities": effort_rational_poly_eq,
    "pc_rational_inequalities": effort_rational_poly_eq,
    "pc_partial_fraction_decomposition": effort_partial_fractions,
    # PC exp finance / discrete / vectors / polar / conics
    "pc_compound_interest": effort_compound_interest_pc,
    "pc_sample_spaces_and_fundamental_counting_principle": effort_counting_pc,
    "pc_permutations_vs_combinations": effort_perm_comb_pc,
    "pc_binomial_theorem": effort_binomial,
    "pc_probability_independent_dependent_events": effort_probability_pc,
    "pc_probability_independent_dependent_events_word_problems": effort_probability_pc,
    "pc_probability_mutually_exclusive": effort_probability_pc,
    "pc_probability_mutually_exclusive_word_problems": effort_probability_pc,
    "pc_probability_with_permutations_and_combinations": effort_probability_pc,
    "pc_vectors_basics": effort_vector,
    "pc_vectors_operations": effort_vector,
    "pc_vectors_diagrams": effort_vector_diagram,
    "pc_dot_products": effort_vector,
    "pc_cross_products": effort_vector,
    "pc_3d_points_in_three_dimensions": effort_distance_midpoint,
    "pc_3d_vectors_basics": effort_vector,
    "pc_3d_vectors_operations": effort_vector,
    "pc_multivariable_linear_systems_and_row_operations": effort_systems_row,
    "pc_polar_coordinates": effort_polar,
    "pc_graphs_of_polar_equations": effort_polar,
    "pc_polar_and_rectangular_forms_of_equations": effort_polar,
    "pc_polar_forms_of_conic_sections": effort_polar,
    "pc_complex_numbers_in_polar_form": effort_polar,
    "pc_parabolas_graphing_and_properties": effort_conic_pc,
    "pc_parabolas_writing_equations": effort_conic_pc,
    "pc_circles_graphing_and_properties": effort_conic_pc,
    "pc_circles_writing_equations": effort_conic_pc,
    "pc_ellipses_graphing_and_properties": effort_conic_pc,
    "pc_ellipses_writing_equations": effort_conic_pc,
    "pc_hyperbolas_graphing_and_properties": effort_conic_pc,
    "pc_hyperbolas_writing_equations": effort_conic_pc,
    "pc_rotations_of_conic_sections": effort_conic_pc,
    "pc_parametric_equations": effort_parametric_projectile,
    "pc_projectile_motion": effort_parametric_projectile,
    "pc_mathematical_induction": effort_power_series_induction,
    "pc_power_series": effort_power_series_induction,
    "pc_instantaneous_rates_of_change": effort_derivative_power,
    "pc_motion_along_a_line": effort_motion_line,
    "pc_area_under_a_curve_by_limit_of_sums": effort_definite_ftc,
    # Calc advanced derivatives / apps
    "calc_diff_definition_of_the_derivative": effort_def_of_derivative,
    "calc_diff_instantaneous_rates_of_change": effort_derivative_rules,
    "calc_diff_rules_using_tables": effort_table_derivative,
    "calc_diff_logarithmic": effort_implicit_log_diff,
    "calc_diff_implicit": effort_implicit_log_diff,
    "calc_diff_inverse_functions": effort_implicit_log_diff,
    "calc_app_diff_rolles_theorem": effort_curve_analysis_calc,
    "calc_app_diff_mean_value_theorem": effort_curve_analysis_calc,
    "calc_app_diff_intervals_of_increase_and_decrease": effort_curve_analysis_calc,
    "calc_app_diff_intervals_of_concavity": effort_curve_analysis_calc,
    "calc_app_diff_relative_extrema": effort_curve_analysis_calc,
    "calc_app_diff_absolute_extrema": effort_curve_analysis_calc,
    "calc_app_diff_optimization": effort_curve_analysis_calc,
    "calc_app_diff_curve_sketching": effort_derivative_power,
    "calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime": effort_derivative_power,
    "calc_app_diff_motion_along_a_line": effort_motion_line,
    "calc_app_diff_differentials": effort_curve_analysis_calc,
    "calc_app_diff_linear_approximations": effort_curve_analysis_calc,
    "calc_app_diff_newtons_method": effort_curve_analysis_calc,
    "calc_app_diff_limits_in_form_of_definition_of_derivative": effort_def_of_derivative,
    "calc_app_diff_lhopitals_rule": effort_lhopital,
    # Calc integrals / area / volume / DE
    "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution": effort_ibp_sub_integral,
    "calc_indef_int_trigonometric_with_substitution": effort_ibp_sub_integral,
    "calc_indef_int_inverse_trigonometric_with_substitution": effort_ibp_sub_integral,
    "calc_indef_int_integration_by_parts": effort_ibp_sub_integral,
    "calc_indef_int_partial_fractions": effort_ibp_sub_integral,
    "calc_indef_int_multi_trick": effort_ibp_sub_integral,
    "calc_indef_int_general": effort_ibp_sub_integral,
    "calc_def_int_area_under_a_curve_by_limit_of_sums": effort_definite_ftc,
    "calc_def_int_riemann_sum_tables": effort_definite_ftc,
    "calc_def_int_first_fundamental_theorem_of_calculus": effort_definite_ftc,
    "calc_def_int_substitution_with_change_of_variables": effort_ibp_sub_integral,
    "calc_def_int_mean_value_theorem": effort_definite_ftc,
    "calc_def_int_second_fundamental_theorem_of_calculus": effort_definite_ftc,
    "calc_app_int_area_under_a_curve": effort_area_volume,
    "calc_app_int_area_between_curves": effort_area_volume,
    "calc_app_int_volume_by_slicing_disks_and_washers": effort_area_volume,
    "calc_app_int_volume_by_cylinders": effort_area_volume,
    "calc_app_int_volume_of_solids_with_known_cross_sections": effort_area_volume,
    "calc_app_int_motion_along_a_line_revisited": effort_motion_line,
    "calc_diff_eq_slope_fields": effort_diff_eq,
    "calc_diff_eq_introduction": effort_diff_eq,
    "calc_diff_eq_separable": effort_diff_eq,
    "calc_diff_eq_exponential_growth_and_decay": effort_diff_eq,
    # A1 / A2 / G6 easy wins (merge-friendly satellite registrations)
    "finding_sine_cosine_tangent": effort_right_triangle_trig,
    "find_missing_sides_of_triangles": effort_right_triangle_trig,
    "radical_distance_formula": effort_distance_midpoint,
    "radical_midpoint_formula": effort_distance_midpoint,
    "graphing_single_variable_inequalities": effort_linear_relation,
    "discrete_relations": effort_linear_relation,
    "continuous_relations": effort_linear_relation,
    "a2_polynomial_functions_the_binomial_theorem": effort_binomial,
    "a2_polynomial_functions_the_remainder_theorem": effort_poly_zeros_writing,
    "a2_polynomial_functions_writing_functions": effort_poly_zeros_writing,
    "a2_polynomial_functions_conjugate_roots_and_writing_functions": effort_poly_zeros_writing,
    "a2_polynomial_functions_descartes_rule_of_signs": effort_poly_zeros_writing,
    "a2_polynomial_functions_rational_zero_root_theorem": effort_poly_zeros_writing,
    "a2_polynomial_functions_fundamental_theorem_of_algebra": effort_poly_zeros_writing,
    "a2_conic_sections_parabolas_writing_equations": effort_conic_pc,
    "a2_general_functions_inverses": effort_fn_analysis_pc,
    "g6_what_fraction_of_a_whole": effort_g6_fraction_props,
    "g6_properties_of_addition_and_multiplication": effort_g6_fraction_props,
}


def register_precalc_calc_scorers(register) -> None:
    """Register all precalc/calc scorers onto the shared EFFORT_SCORERS map."""
    for type_id, scorer in PRECALC_CALC_SCORERS.items():
        register(type_id, scorer)
