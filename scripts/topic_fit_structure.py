"""Extract / display generation structure metadata for topic-fit galleries.

Prefers live question ``metadata`` fields already emitted by generators
(family, shape_id, upgrades, function_classes, …) — does not invent a
parallel Mad-Libs inventory.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

# Keys that identify the structural template / family for a sample.
_PRIMARY_KEYS = (
    "form_id",
    "openstax_form",
    "structure_id",
    "family",
    "template_id",
    "shape_id",
    "shape",
    "form",
)

# Extra knobs / fingerprint fields shown when present (readable, not a dump).
# ``band`` is kept for internal sorting / EMH generators but never displayed —
# prefer continuous ``difficulty`` (shown as ``D=``) in gallery UX.
_DETAIL_KEYS = (
    "variant",
    "function_classes",
    "methods_used",
    "chain_depth",
    "upgrades",
    "upgrades_applied",
    "structure_upgrades",
    "n_ops",
    "nest_depth",
    "difficulty",
    "band",
    "primitive_engine",
    "wp_kind",
    "n_constraints",
    "frame",
    "solution_kind",
    "core_form_id",
    "wrappers_applied",
    "difficulty_sources",
    "approx_max_d",
    "difficulty_clamped",
    "difficulty_shortfall",
)


def extract_structure_meta(meta: dict[str, Any] | None) -> dict[str, Any]:
    """Pull structure-relevant fields from live question metadata."""
    m = meta if isinstance(meta, dict) else {}
    out: dict[str, Any] = {}

    for key in _PRIMARY_KEYS + _DETAIL_KEYS:
        if key not in m:
            continue
        val = m[key]
        if val is None or val == "" or val == [] or val == ():
            continue
        if isinstance(val, (list, tuple, set, frozenset)):
            items = [str(x) for x in val if x is not None and str(x) != ""]
            if not items:
                continue
            out[key] = items
        elif isinstance(val, (int, float)) and not isinstance(val, bool):
            out[key] = val
        else:
            out[key] = str(val)

    # Alias: some generators only set upgrades under structure_upgrades.
    if "upgrades" not in out and "structure_upgrades" in out:
        out["upgrades"] = out["structure_upgrades"]

    primary = structure_primary(out)
    if primary:
        out["structure_primary"] = primary
    return out


def structure_primary(struct: dict[str, Any] | None) -> str:
    """Single scannable label for inventory grouping."""
    s = struct if isinstance(struct, dict) else {}
    for key in _PRIMARY_KEYS:
        val = s.get(key)
        if isinstance(val, list):
            val = val[0] if val else None
        if val:
            return str(val)

    # Framework derivatives: methods + classes is the real structure signal.
    methods = s.get("methods_used") or []
    classes = s.get("function_classes") or []
    if methods or classes:
        m = "+".join(methods) if isinstance(methods, list) else str(methods)
        c = "+".join(classes) if isinstance(classes, list) else str(classes)
        bits = [b for b in (m, c) if b]
        if bits:
            depth = s.get("chain_depth")
            label = " · ".join(bits)
            if depth not in (None, "", 0, "0"):
                label = f"{label} · chain={depth}"
            return label

    ups = s.get("upgrades") or s.get("upgrades_applied") or []
    if ups:
        return "ups:" + ",".join(str(u) for u in ups[:4])

    return ""


def _format_d(val: Any) -> str | None:
    """Format continuous difficulty for display (``D=0``, ``D=5.5``)."""
    if val is None or val == "":
        return None
    try:
        d = float(val)
    except (TypeError, ValueError):
        return None
    if d != d:  # NaN
        return None
    text = f"{d:g}"
    return f"D={text}"


def format_structure_cell(
    struct: dict[str, Any] | None,
    *,
    difficulty: float | int | None = None,
) -> str:
    """Compact table cell: primary + a few details.

    Prefer numeric continuous ``D=`` over EMH ``band=easy|medium|hard``.
    ``band`` may still exist on the struct for internal use but is never shown.
    """
    s = struct if isinstance(struct, dict) else {}
    primary = s.get("structure_primary") or structure_primary(s)
    if not primary:
        return "—"

    extras: list[str] = []
    variant = s.get("variant")
    if variant:
        extras.append(f"var={variant}")

    d_label = _format_d(difficulty if difficulty is not None else s.get("difficulty"))
    if d_label:
        extras.append(d_label)

    # Avoid repeating primary when it already is family/structure_id.
    # Never surface ``band`` (easy/medium/hard) — continuous D is the product UX.
    for key, label in (
        ("methods_used", "methods"),
        ("function_classes", "classes"),
        ("upgrades", "ups"),
        ("upgrades_applied", "ups"),
        ("n_ops", "n_ops"),
        ("chain_depth", "chain"),
    ):
        if key not in s:
            continue
        val = s[key]
        if key in ("methods_used", "function_classes") and primary and (
            (isinstance(val, list) and "+".join(val) in primary) or str(val) in primary
        ):
            continue
        if key == "upgrades" and primary.startswith("ups:"):
            continue
        if key == "chain_depth" and (
            val in (0, "0", None) or f"chain={val}" in primary
        ):
            continue
        if isinstance(val, list):
            if not val:
                continue
            extras.append(f"{label}={','.join(str(x) for x in val[:5])}")
        else:
            extras.append(f"{label}={val}")

    sources = s.get("difficulty_sources")
    if isinstance(sources, list) and sources:
        bits: list[str] = []
        for item in sources[:6]:
            if isinstance(item, dict):
                kind = item.get("kind") or "?"
                tag = item.get("tag") or "?"
                bits.append(f"{kind}:{tag}")
            else:
                bits.append(str(item))
        if bits:
            extras.append("from=" + ",".join(bits))
    amax = s.get("approx_max_d")
    if amax is not None and amax != "":
        extras.append(f"amax={amax}")
    if s.get("difficulty_clamped") in (True, "True", "true", 1):
        extras.append("clamped")

    if not extras:
        return primary
    # Keep cell scannable.
    shown = extras[:4]
    return f"{primary} · " + "; ".join(shown)


def inventory_counts(rows: list[dict[str, Any]]) -> list[tuple[str, int]]:
    """Unique structure_primary labels with counts (desc)."""
    counter: Counter[str] = Counter()
    for row in rows:
        if row.get("error"):
            continue
        struct = row.get("structure") or {}
        if not isinstance(struct, dict):
            struct = extract_structure_meta(struct) if struct else {}
        primary = (
            struct.get("structure_primary")
            or structure_primary(struct)
            or "(unlabeled)"
        )
        counter[str(primary)] += 1
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))


def inventory_markdown(rows: list[dict[str, Any]], *, heading: str = "### Structure inventory") -> list[str]:
    """Markdown lines: summary table of structures found in the sample set."""
    counts = inventory_counts(rows)
    lines = [
        heading,
        "",
        "Structures / families / templates actually used in this sample set "
        "(from live question metadata — not a static template list).",
        "",
    ]
    if not counts:
        lines.append("_No structure metadata on these samples._")
        lines.append("")
        return lines

    labeled = sum(1 for k, _ in counts if k != "(unlabeled)")
    total = sum(n for _, n in counts)
    lines.append(f"- distinct structures: **{labeled}** · samples: **{total}**")
    lines.append("")
    lines.append("| Structure / family | Count |")
    lines.append("|--------|------:|")
    for label, n in counts:
        safe = str(label).replace("|", "\\|")
        lines.append(f"| `{safe}` | {n} |")
    lines.append("")
    return lines


def structure_from_question_meta(meta: dict[str, Any] | None) -> dict[str, Any]:
    """Convenience for gallery samplers: extract + ensure primary label."""
    return extract_structure_meta(meta)
