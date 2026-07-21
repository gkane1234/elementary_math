"""Compositional polynomial inflate — subset disguise with hierarchical budget.

Working expression is a piece-tree. Each difficulty unit:
  1. Sample a sum-node level (weight ∝ level_bias^depth, favoring root)
  2. Pick a subset of that node's children
  3. Apply a local value-preserving unsimplify
  4. Splice the result back

Invariant: root.coeffs ≡ PolynomialTarget throughout.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.primitives._algebra_render import (
    num_latex,
    sample_integerish,
)
from question_engine.frameworks.primitives.presentation import (
    DisplayPiece,
    presentation_for_ctx,
    render_addition,
    render_product,
)
from question_engine.frameworks.primitives.registry import PrimitiveContext
from question_engine.frameworks.primitives.variables import SampledVariable

NodeKind = Literal["leaf", "sum", "product", "scale"]


def _clean(coeffs: dict[int, Fraction]) -> dict[int, Fraction]:
    return {int(d): Fraction(c) for d, c in coeffs.items() if c != 0}


def _poly_add(a: dict[int, Fraction], b: dict[int, Fraction]) -> dict[int, Fraction]:
    out = dict(a)
    for d, c in b.items():
        out[d] = out.get(d, Fraction(0)) + c
        if out[d] == 0:
            del out[d]
    return out


def _poly_scale(p: dict[int, Fraction], k: Fraction) -> dict[int, Fraction]:
    if k == 0:
        return {}
    return {d: c * k for d, c in p.items() if c * k != 0}


def _poly_mul(a: dict[int, Fraction], b: dict[int, Fraction]) -> dict[int, Fraction]:
    out: dict[int, Fraction] = {}
    for d1, c1 in a.items():
        for d2, c2 in b.items():
            d = d1 + d2
            out[d] = out.get(d, Fraction(0)) + c1 * c2
    return _clean(out)


def _poly_all_divisible(coeffs: dict[int, Fraction], k: Fraction) -> bool:
    if k == 0:
        return False
    return all(c % k == 0 for c in coeffs.values())


@dataclass
class PolyNode:
    """Mutable piece-tree node with cached polynomial value."""

    kind: NodeKind
    coeffs: dict[int, Fraction]
    children: list[PolyNode] = field(default_factory=list)
    scale_factor: Fraction | None = None  # for kind == "scale"
    # Depth is recomputed when collecting eligible nodes from root.
    depth: int = 0

    def recompute(self) -> dict[int, Fraction]:
        if self.kind == "leaf":
            self.coeffs = _clean(self.coeffs)
            return self.coeffs
        if self.kind == "sum":
            acc: dict[int, Fraction] = {}
            for ch in self.children:
                acc = _poly_add(acc, ch.recompute())
            self.coeffs = acc
            return acc
        if self.kind == "product":
            acc = {0: Fraction(1)}
            for ch in self.children:
                acc = _poly_mul(acc, ch.recompute())
            self.coeffs = acc
            return acc
        if self.kind == "scale":
            k = self.scale_factor if self.scale_factor is not None else Fraction(1)
            inner = self.children[0].recompute() if self.children else {}
            self.coeffs = _poly_scale(inner, k)
            return self.coeffs
        return self.coeffs


def leaf_from_coeffs(coeffs: dict[int, Fraction]) -> PolyNode:
    return PolyNode(kind="leaf", coeffs=_clean(coeffs))


def leaf_monomial(degree: int, coeff: Fraction) -> PolyNode:
    return leaf_from_coeffs({int(degree): Fraction(coeff)})


def tree_from_target(coeffs: dict[int, Fraction]) -> PolyNode:
    """Root sum of monomial leaves (single leaf if one term)."""
    clean = _clean(coeffs)
    if not clean:
        return leaf_from_coeffs({0: Fraction(0)})
    monos = [leaf_monomial(d, c) for d, c in sorted(clean.items(), reverse=True)]
    if len(monos) == 1:
        return monos[0]
    root = PolyNode(kind="sum", coeffs=dict(clean), children=monos)
    return root


def _knobs() -> dict[str, Any]:
    from question_engine.frameworks.primitives.difficulty_knobs import section

    return section("constructive") or {}


def collect_sum_nodes(root: PolyNode, *, max_depth: int) -> list[PolyNode]:
    """All sum nodes (and multi-child roots treated as sums) up to max_depth."""
    out: list[PolyNode] = []

    def walk(n: PolyNode, depth: int) -> None:
        n.depth = depth
        if depth > max_depth:
            return
        if n.kind == "sum" and len(n.children) >= 1:
            out.append(n)
        elif n.kind == "leaf" and depth == 0:
            # Root leaf: wrap opportunity handled by promoting to sum on first inflate.
            pass
        for ch in n.children:
            walk(ch, depth + 1)

    walk(root, 0)
    return out


def ensure_sum_root(root: PolyNode) -> PolyNode:
    """If root is a lone leaf, wrap as sum of one child so subset ops work."""
    if root.kind == "sum":
        return root
    wrapped = PolyNode(
        kind="sum",
        coeffs=dict(root.coeffs),
        children=[root],
    )
    return wrapped


def pick_level(
    ctx: PrimitiveContext,
    nodes: list[PolyNode],
    *,
    level_bias: float,
) -> PolyNode | None:
    if not nodes:
        return None
    weights: list[float] = []
    for n in nodes:
        w = float(level_bias) ** int(n.depth)
        weights.append(max(1e-9, w))
    total = sum(weights)
    r = ctx.rng.random() * total
    acc = 0.0
    for n, w in zip(nodes, weights):
        acc += w
        if r <= acc:
            return n
    return nodes[-1]


def pick_subset_indices(
    ctx: PrimitiveContext,
    n_children: int,
    *,
    singleton_chance: float,
    full_set_chance: float,
    max_subset_size: int,
) -> list[int]:
    """Return sorted indices of a nonempty subset of children."""
    n = max(1, n_children)
    indices = list(range(n))
    if n == 1:
        return [0]
    r = ctx.rng.random()
    if r < singleton_chance:
        return [ctx.rng.choice(indices)]
    if r < singleton_chance + full_set_chance:
        return indices
    # Small multi-subset: size 2..min(max_subset_size, n)
    lo = 2
    hi = min(max_subset_size, n)
    if hi < lo:
        return [ctx.rng.choice(indices)]
    k = ctx.rng.randint(lo, hi)
    return sorted(ctx.rng.sample(indices, k))


def _try_factor_quadratic(
    coeffs: dict[int, Fraction],
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]] | None:
    """If ``ax^2+bx+c`` factors over small integers, return ``((p,q),(r,s))``."""
    a = coeffs.get(2, Fraction(0))
    b = coeffs.get(1, Fraction(0))
    c = coeffs.get(0, Fraction(0))
    if a == 0 or any(d > 2 for d in coeffs):
        return None
    if a.denominator != 1 or b.denominator != 1 or c.denominator != 1:
        return None
    ai, bi, ci = int(a), int(b), int(c)

    def _divisors(n: int) -> list[int]:
        n = abs(n) if n != 0 else 0
        if n == 0:
            return [0]
        out: list[int] = []
        for i in range(1, min(n, 12) + 1):
            if n % i == 0:
                out.extend([i, -i, n // i, -(n // i)])
        seen: set[int] = set()
        uniq: list[int] = []
        for x in out:
            if x not in seen:
                seen.add(x)
                uniq.append(x)
        return uniq

    for p in _divisors(ai) or [1, -1]:
        if p == 0 or ai % p != 0:
            continue
        r = ai // p
        for q in _divisors(ci) if ci != 0 else [0]:
            if ci != 0 and q == 0:
                continue
            if ci == 0:
                s = 0
            elif q == 0 or ci % q != 0:
                continue
            else:
                s = ci // q
            if p * s + q * r == bi:
                return (Fraction(p), Fraction(q)), (Fraction(r), Fraction(s))
    return None


def _local_split_const(
    ctx: PrimitiveContext, coeffs: dict[int, Fraction]
) -> PolyNode | None:
    b0 = coeffs.get(0, Fraction(0))
    if b0 == 0:
        return None
    k = sample_integerish(ctx, exclude_zero=True).value
    if k == b0 or k == 0:
        return None
    left = dict(coeffs)
    left[0] = b0 - k
    if left[0] == 0:
        del left[0]
    if not left:
        return None
    return PolyNode(
        kind="sum",
        coeffs=_clean(coeffs),
        children=[leaf_from_coeffs(left), leaf_monomial(0, k)],
    )


def _local_split_term(
    ctx: PrimitiveContext, coeffs: dict[int, Fraction]
) -> PolyNode | None:
    degs = [d for d, c in coeffs.items() if c != 0]
    if len(degs) < 2:
        return None
    peel_deg = ctx.rng.choice(degs)
    peel_c = coeffs[peel_deg]
    left = {d: c for d, c in coeffs.items() if d != peel_deg}
    return PolyNode(
        kind="sum",
        coeffs=_clean(coeffs),
        children=[leaf_from_coeffs(left), leaf_monomial(peel_deg, peel_c)],
    )


def _local_distribute(
    ctx: PrimitiveContext, coeffs: dict[int, Fraction]
) -> PolyNode | None:
    from question_engine.frameworks.primitives.poly_helpers import poly_degree, scale_coeffs

    if not coeffs:
        return None
    k = sample_integerish(ctx, exclude_zero=True).value
    if abs(k) == 1:
        k = Fraction(ctx.rng.choice([2, 3, -2, -3]))
    deg = poly_degree(coeffs)
    if _poly_all_divisible(coeffs, k):
        inner = scale_coeffs(coeffs, Fraction(1) / k)
        return PolyNode(
            kind="scale",
            coeffs=_clean(coeffs),
            scale_factor=k,
            children=[leaf_from_coeffs(inner)],
        )
    # Peel scaled simple inner (leading ± maybe const).
    lead = coeffs.get(deg, Fraction(1))
    inner_lead = Fraction(1) if lead % k != 0 else lead / k
    if abs(inner_lead) > 6:
        return None
    inner: dict[int, Fraction] = {deg: inner_lead}
    if 0 in coeffs and ctx.rng.random() < 0.5:
        peel = Fraction(ctx.rng.choice([-2, -1, 1, 2]))
        inner[0] = peel
    scaled = scale_coeffs(inner, k)
    rem = dict(coeffs)
    for d, c in scaled.items():
        rem[d] = rem.get(d, Fraction(0)) - c
        if rem[d] == 0:
            del rem[d]
    scale_node = PolyNode(
        kind="scale",
        coeffs=_clean(scaled),
        scale_factor=k,
        children=[leaf_from_coeffs(inner)],
    )
    if not rem:
        scale_node.coeffs = _clean(coeffs)
        return scale_node
    return PolyNode(
        kind="sum",
        coeffs=_clean(coeffs),
        children=[scale_node, leaf_from_coeffs(rem)],
    )


def _local_binom_product(coeffs: dict[int, Fraction]) -> PolyNode | None:
    fac = _try_factor_quadratic(coeffs)
    if fac is None:
        return None
    (p, q), (r, s) = fac
    return PolyNode(
        kind="product",
        coeffs=_clean(coeffs),
        children=[
            leaf_from_coeffs(_clean({1: p, 0: q})),
            leaf_from_coeffs(_clean({1: r, 0: s})),
        ],
    )


def _local_numeric_split(
    ctx: PrimitiveContext, coeffs: dict[int, Fraction]
) -> PolyNode | None:
    """Pure constant → sum of two constants."""
    if set(coeffs.keys()) - {0}:
        return None
    v = coeffs.get(0, Fraction(0))
    if v == 0:
        return None
    # Prefer small integer splits.
    choices = [a for a in range(-6, 7) if a != 0 and a != v and abs(v - a) <= 12]
    if not choices:
        return None
    a = Fraction(ctx.rng.choice(choices))
    b = v - a
    if b == 0:
        return None
    return PolyNode(
        kind="sum",
        coeffs=_clean(coeffs),
        children=[leaf_monomial(0, a), leaf_monomial(0, b)],
    )


def apply_local_inflate(
    ctx: PrimitiveContext,
    coeffs: dict[int, Fraction],
    *,
    prefer_distribute: bool = True,
) -> tuple[PolyNode, str] | None:
    """Pick and apply one local inflator; return (new_subtree, tag) or None."""
    coeffs = _clean(coeffs)
    if not coeffs:
        return None
    pure_const = set(coeffs.keys()) <= {0}
    choices: list[str] = ["split_term", "split_const", "numeric_split"]
    if not pure_const:
        choices.append("distribute")
        if prefer_distribute:
            choices = [
                "distribute",
                "distribute",
                "split_term",
                "split_const",
                "numeric_split",
            ]
    else:
        # Constants: prefer split, never ``3(1)``-style distribute.
        choices = ["numeric_split", "numeric_split", "split_const"]
    if not pure_const and _try_factor_quadratic(coeffs) is not None:
        choices.extend(["binom_product", "binom_product"])

    ctx.rng.shuffle(choices)
    ordered: list[str] = []
    if prefer_distribute and "distribute" in choices and not pure_const:
        ordered.append("distribute")
    for c in choices:
        if c not in ordered:
            ordered.append(c)

    for choice in ordered:
        node: PolyNode | None = None
        if choice == "distribute":
            node = _local_distribute(ctx, coeffs)
        elif choice == "split_const":
            node = _local_split_const(ctx, coeffs)
        elif choice == "split_term":
            node = _local_split_term(ctx, coeffs)
        elif choice == "numeric_split":
            node = _local_numeric_split(ctx, coeffs)
        elif choice == "binom_product":
            node = _local_binom_product(coeffs)
        if node is not None:
            node.recompute()
            if _clean(node.coeffs) == coeffs:
                return node, choice
    return None


def _is_single_monomial(node: PolyNode) -> bool:
    return node.kind == "leaf" and len(node.coeffs) == 1


def _is_multi_term_poly(node: PolyNode) -> bool:
    """True if rendering this node needs grouping inside a product/scale."""
    if node.kind == "sum":
        return len(node.children) > 1 or (
            len(node.children) == 1 and _is_multi_term_poly(node.children[0])
        )
    if node.kind == "leaf":
        return len(node.coeffs) > 1
    if node.kind in ("product", "scale"):
        return False  # already a tight unit
    return True


def render_node(
    node: PolyNode,
    var: SampledVariable,
    style: Any,
    rng: Any,
    *,
    parent_kind: NodeKind | None = None,
) -> tuple[str, str]:
    from question_engine.frameworks.primitives.poly_helpers import render_poly

    if node.kind == "leaf":
        return render_poly(node.coeffs, var)

    if node.kind == "sum":
        if not node.children:
            return render_poly(node.coeffs, var)
        # Flatten trivial single-child sums for display
        if len(node.children) == 1:
            return render_node(
                node.children[0], var, style, rng, parent_kind=parent_kind
            )
        l0, t0 = render_node(node.children[0], var, style, rng, parent_kind="sum")
        latex, text = l0, t0
        for ch in node.children[1:]:
            cl, ct = render_node(ch, var, style, rng, parent_kind="sum")
            # Only wrap nested *sums* so addition doesn't eat their ± structure.
            # Scale/product children already read as single terms (e.g. 2(x+1)).
            if ch.kind == "sum" and len(ch.children) > 1:
                cl = f"\\left({cl}\\right)"
                ct = f"({ct})"
            latex, text = render_addition(
                DisplayPiece(latex, text),
                DisplayPiece(cl, ct),
                style,
                rng,
            )
        if parent_kind in ("product", "scale"):
            latex = f"\\left({latex}\\right)"
            text = f"({text})"
        return latex, text

    if node.kind == "scale":
        k = node.scale_factor if node.scale_factor is not None else Fraction(1)
        inner = node.children[0] if node.children else leaf_from_coeffs({})
        # Unwrap trivial sum wrappers
        while inner.kind == "sum" and len(inner.children) == 1:
            inner = inner.children[0]
        il, it = render_node(inner, var, style, rng, parent_kind="scale")
        k_l, k_t = num_latex(k), num_latex(k)
        # Single monomial: schoolbook juxtaposition ``2x^{2}`` (no parens).
        if _is_single_monomial(inner):
            # Avoid ``2-x`` ambiguity: if monomial latex starts with '-', keep parens.
            if il.startswith("-"):
                return f"{k_l}\\left({il}\\right)", f"{k_t}*({it})"
            return f"{k_l}{il}", f"{k_t}*{it}"
        # Pure constant leaf: ``3\\cdot 1`` rather than ``3(1)``.
        if inner.kind == "leaf" and set(inner.coeffs.keys()) <= {0}:
            c_l, c_t = il, it
            return f"{k_l}\\cdot {c_l}", f"{k_t}*{c_t}"
        # Multi-term or nested structure: need grouping.
        if not (il.startswith("\\left(") or il.startswith("(")):
            il = f"\\left({il}\\right)"
            it = f"({it})"
        return f"{k_l}{il}", f"{k_t}*{it}"

    if node.kind == "product":
        pieces: list[DisplayPiece] = []
        for ch in node.children:
            cl, ct = render_node(ch, var, style, rng, parent_kind="product")
            # Parens only when the factor is a sum / multi-term poly.
            if ch.kind == "sum" or (ch.kind == "leaf" and len(ch.coeffs) > 1):
                if not (cl.startswith("\\left(") or cl.startswith("(")):
                    cl = f"\\left({cl}\\right)"
                    ct = f"({ct})"
            pieces.append(DisplayPiece(cl, ct))
        return render_product(pieces, style, rng)

    return render_poly(node.coeffs, var)


def compose_inflate(
    ctx: PrimitiveContext,
    root: PolyNode,
    *,
    budget: int,
    var: SampledVariable,
    prefer_distribute: bool = True,
) -> tuple[PolyNode, list[str], dict[str, int]]:
    """Spend ``budget`` compose units on ``root``. Returns (root, tags, depth_counts)."""
    kn = _knobs()
    level_bias = float(kn.get("poly_level_bias", 0.5))
    max_depth = int(kn.get("poly_max_compose_depth", 6))
    singleton_chance = float(kn.get("poly_singleton_chance", 0.45))
    full_set_chance = float(kn.get("poly_full_set_chance", 0.12))
    max_subset = int(kn.get("poly_max_subset_size", 4))

    tags: list[str] = ["seed"]
    depth_counts: dict[str, int] = {}
    root = ensure_sum_root(root)
    root.recompute()

    for _ in range(max(0, budget)):
        nodes = collect_sum_nodes(root, max_depth=max_depth)
        # Also allow promoting: if somehow no sum nodes, bail
        if not nodes:
            break
        node = pick_level(ctx, nodes, level_bias=level_bias)
        if node is None or not node.children:
            break
        idxs = pick_subset_indices(
            ctx,
            len(node.children),
            singleton_chance=singleton_chance,
            full_set_chance=full_set_chance,
            max_subset_size=max_subset,
        )
        subset = [node.children[i] for i in idxs]
        subset_coeffs: dict[int, Fraction] = {}
        for ch in subset:
            subset_coeffs = _poly_add(subset_coeffs, ch.recompute())

        result = apply_local_inflate(
            ctx, subset_coeffs, prefer_distribute=prefer_distribute
        )
        if result is None:
            continue
        new_sub, tag = result

        # Splice: replace selected children with new_sub.
        # Flatten sum→sum so we don't force ``(...)+(...)`` paren nests.
        remaining = [ch for i, ch in enumerate(node.children) if i not in set(idxs)]
        if new_sub.kind == "sum" and new_sub.children:
            node.children = remaining + list(new_sub.children)
        else:
            node.children = remaining + [new_sub]
        if len(node.children) == 0:
            node.children = [new_sub]
        node.recompute()
        root.recompute()

        depth_key = str(node.depth)
        depth_counts[depth_key] = depth_counts.get(depth_key, 0) + 1
        tags.append(f"compose:d{node.depth}:{tag}")

    root.recompute()
    return root, tags, depth_counts


def construct_poly_composed(
    ctx: PrimitiveContext,
    *,
    d: float,
    var: SampledVariable,
    target_coeffs: dict[int, Fraction],
    prefer_distribute: bool = True,
    min_inflators: int | None = None,
    allow_cancel_clutter: bool = False,
    scope_meta: dict[str, Any] | None = None,
    _depth: int = 0,
    inflator_budget_fn: Any = None,
) -> tuple[str, str, list[str], dict[str, Any]]:
    """Build latex/text via compositional inflate. Returns latex, text, tags, meta extras."""
    from question_engine.frameworks.primitives.presentation import maybe_inject_cancel_clutter

    eff = float(d)
    style = presentation_for_ctx(ctx, d=eff)
    root = tree_from_target(target_coeffs)
    if inflator_budget_fn is None:
        # Late bind to avoid circular import at module load.
        from question_engine.frameworks.primitives.constructive import inflator_budget as _ib

        inflator_budget_fn = _ib
    budget = int(inflator_budget_fn(eff))
    if min_inflators is not None:
        budget = max(budget, int(min_inflators))
    if _depth > 0:
        budget = max(0, budget // 2)

    root, tags, depth_counts = compose_inflate(
        ctx,
        root,
        budget=budget,
        var=var,
        prefer_distribute=prefer_distribute,
    )
    latex, text = render_node(root, var, style, ctx.rng)

    if allow_cancel_clutter:
        latex, text, cancel_tags = maybe_inject_cancel_clutter(
            ctx,
            style,
            var_latex=var.latex,
            var_text=var.name,
            core_latex=latex,
            core_text=text,
            d=eff,
        )
        tags.extend(cancel_tags)

    extras = {
        "compose_depth_counts": depth_counts,
        "compose_budget": budget,
        "tree_kind": root.kind,
        "n_root_children": len(root.children) if root.kind == "sum" else 0,
    }
    if scope_meta:
        extras["scope"] = scope_meta
    return latex, text, tags, extras
