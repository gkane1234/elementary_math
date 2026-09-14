"""Per-topic Diff skeleton galleries with conceptual difficulty ladders.
Generates:
  index.html                 — links to each algebraic deriv topic
  <topic>/gallery.html       — KaTeX-rendered ladder samples + debug panels
  <topic>/samples.json       — full row payloads including knobs / cost_spend
  DIFFICULTY_SCALE.md        — conceptual band → hole-fill doc (sibling)
Topics = algebraic derivative generator keys that have OpenStax forms mapped
in ``expr_skeleton`` (power, product, quotient, chain, trig, ln/exp, …).
"""
from __future__ import annotations
import json
import re
import random
from html import escape
from pathlib import Path
from typing import Any
from question_engine.frameworks.primitives.expr_skeleton import (
    FORM_PATTERNS,
    richness_from_conceptual,
    sample_from_form,
)
from question_engine.frameworks.primitives.openstax_form_catalogs import (
    filter_forms_by_allows,
    forms_for_leaf,
    load_form_catalog,
)
from question_engine.frameworks.primitives.poly_expression import Fn, Mul, render_latex
OUT_DIR = Path(__file__).resolve().parent
KATEX = "../../topic_fit/_assets/katex"  # from <topic>/gallery.html
KATEX_INDEX = "../topic_fit/_assets/katex"
# Topic notes (steps 1–3): prefer local notes/, else phase-01 calc_*.md
NOTES_DIRS = [
    OUT_DIR / "notes",
    OUT_DIR.parent / "skeleton_phase01_gallery" / "notes",
]
# Map Diff gallery topic_key → notes/<slug>.md (calc_diff_*)
TOPIC_NOTE_SLUGS: dict[str, str] = {
    "derivative_power_rule": "calc_diff_power_rule",
    "derivative_product_rule": "calc_diff_product_rule",
    "derivative_quotient_rule": "calc_diff_quotient_rule",
    "derivative_chain_rule": "calc_diff_chain_rule",
    "derivative_trigonometric": "calc_diff_trigonometric",
    "derivative_ln_exp": "calc_diff_natural_logarithms_and_exponentials",
    "derivative_inverse_trig": "calc_diff_inverse_trigonometric",
    "derivative_higher_order": "calc_diff_higher_order_derivatives",
    "derivative_general": "calc_diff_general",
}
_NOTES_FLAG_RE = re.compile(r"\b(UNCLEAR|LOW_VARIETY)\b")
# Algebraic derivative topics with catalog form routing (stubs omitted).
TOPICS: list[tuple[str, str]] = [
    ("derivative_power_rule", "Power rule"),
    ("derivative_product_rule", "Product rule"),
    ("derivative_quotient_rule", "Quotient rule"),
    ("derivative_chain_rule", "Chain rule"),
    ("derivative_trigonometric", "Trigonometric"),
    ("derivative_ln_exp", "Exp / ln"),
    ("derivative_inverse_trig", "Inverse trig"),
    ("derivative_higher_order", "Higher order"),
    ("derivative_general", "General / mixed"),
]
# Difficulty ladder samples per form (low → mid → high → elite).
LADDER_DS = (2.0, 8.0, 14.0, 20.0)
ALLOWS_BY_TOPIC: dict[str, dict[str, bool]] = {
    "derivative_power_rule": {
        "allow_roots": True,
        "allow_chain": False,
        "require_chain": False,
    },
    "derivative_product_rule": {
        # Algebraic product by default; chain-on-a-factor unlocks mid/high.
        "allow_trig": False,
        "allow_exp": False,
        "allow_chain": True,
    },
    "derivative_quotient_rule": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_invtrig": False,
    },
    "derivative_chain_rule": {
        # Match leaf defaults: trig/exp/ln ON; D-unlocks keep low-C algebraic.
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": True,
        "allow_roots": True,
        "allow_chain": True,
        "require_chain": True,
    },
    "derivative_trigonometric": {
        "allow_trig": True,
        "allow_product": True,
        "allow_chain": True,
    },
    "derivative_ln_exp": {"allow_exp": True, "allow_log": True, "allow_chain": True},
    "derivative_inverse_trig": {"allow_invtrig": True, "allow_chain": True},
    "derivative_higher_order": {"allow_chain": False},
    "derivative_general": {
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": True,
        "allow_roots": True,
        "allow_chain": True,
        "allow_product": True,
        "allow_quotient": True,
    },
}

def _prompt(body: str, order: int) -> str:
    if order >= 3:
        return rf"\frac{{d^{{3}}}}{{dx^{{3}}}}\left[{body}\right]"
    if order == 2:
        return rf"\frac{{d^{{2}}}}{{dx^{{2}}}}\left[{body}\right]"
    return rf"\frac{{d}}{{dx}}\left[{body}\right]"

def _order_for(fid: str) -> int:
    if fid == "higher_order_2":
        return 2
    if fid == "higher_order_3":
        return 3
    return 1

def _shared_u_ok(expr, inv: dict) -> bool | None:
    """Return True/False when checkable; None if N/A."""
    if not inv.get("shared_inner"):
        return None
    if inv.get("skeleton_kind") != "diff_prod_fg_u":
        return None
    if not isinstance(expr, Mul) or len(expr.factors) != 2:
        return False
    f, g = expr.factors
    args = []
    for piece in (f, g):
        if isinstance(piece, Fn):
            args.append(piece.arg)
        elif isinstance(piece, Mul):
            for fac in piece.factors:
                if isinstance(fac, Fn):
                    args.append(fac.arg)
    if len(args) == 2:
        return render_latex(args[0]) == render_latex(args[1])
    return True

def _notes_candidate_paths(topic_key: str, slug: str) -> list[Path]:
    names = [TOPIC_NOTE_SLUGS.get(topic_key, ""), slug, f"calc_diff_{slug}", topic_key]
    paths: list[Path] = []
    seen: set[Path] = set()
    for name in names:
        if not name or name.startswith("_"):
            continue
        for base in NOTES_DIRS:
            p = base / f"{name}.md"
            if p not in seen:
                seen.add(p)
                paths.append(p)
    colocated = OUT_DIR / slug / "NOTES.md"
    if colocated not in seen:
        paths.append(colocated)
    return paths

def _load_notes_markdown(topic_key: str, slug: str) -> str | None:
    for path in _notes_candidate_paths(topic_key, slug):
        if path.is_file():
            return path.read_text(encoding="utf-8")
    return None

def _notes_flags(md: str) -> list[str]:
    found: list[str] = []
    for m in _NOTES_FLAG_RE.finditer(md):
        flag = m.group(1)
        if flag not in found:
            found.append(flag)
    return found

def _md_inline(text: str) -> str:
    s = escape(text)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s

def _is_md_table_sep(line: str) -> bool:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells)

def _md_table_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]

def _notes_body_html(md: str) -> str:
    """Tiny markdown subset: headings, lists, paragraphs, pipe tables."""
    parts: list[str] = []
    buf: list[str] = []
    in_list = False
    lines = md.splitlines()
    i = 0
    def flush_p() -> None:
        if buf:
            parts.append("<p>" + " ".join(_md_inline(x) for x in buf) + "</p>")
            buf.clear()
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip() or line.strip() == "---":
            if in_list:
                parts.append("</ul>")
                in_list = False
            flush_p()
            i += 1
            continue
        # Pipe table: header + separator
        if (
            "|" in line
            and i + 1 < len(lines)
            and _is_md_table_sep(lines[i + 1])
        ):
            if in_list:
                parts.append("</ul>")
                in_list = False
            flush_p()
            headers = _md_table_row(line)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                if _is_md_table_sep(lines[i]):
                    i += 1
                    continue
                rows.append(_md_table_row(lines[i]))
                i += 1
            thead = "".join(f"<th>{_md_inline(h)}</th>" for h in headers)
            body_rows = []
            for row in rows:
                cells = (row + [""] * len(headers))[: len(headers)]
                body_rows.append(
                    "<tr>" + "".join(f"<td>{_md_inline(c)}</td>" for c in cells) + "</tr>"
                )
            parts.append(
                "<table class='notes-table'><thead><tr>"
                + thead
                + "</tr></thead><tbody>"
                + "".join(body_rows)
                + "</tbody></table>"
            )
            continue
        heading = re.match(r"^(#{1,3})\s+(.*)$", line)
        if heading:
            if in_list:
                parts.append("</ul>")
                in_list = False
            flush_p()
            level = len(heading.group(1))
            parts.append(f"<h{level}>{_md_inline(heading.group(2))}</h{level}>")
            i += 1
            continue
        bullet = re.match(r"^[-*]\s+(.*)$", line)
        if bullet:
            flush_p()
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{_md_inline(bullet.group(1))}</li>")
            i += 1
            continue
        if in_list:
            parts.append("</ul>")
            in_list = False
        buf.append(line.strip())
        i += 1
    if in_list:
        parts.append("</ul>")
    flush_p()
    return "\n".join(parts)

def _notes_section_html(topic_key: str, slug: str) -> str:
    md = _load_notes_markdown(topic_key, slug)
    if not md:
        return ""
    flags = _notes_flags(md)
    banner = ""
    if flags:
        label = " · ".join(flags)
        banner = (
            f"<div class='notes-alert'>{escape(label)} — gold look not locked; "
            "see notes below.</div>"
        )
    return (
        banner
        + "<div class='notes-block'>"
        + _notes_body_html(md)
        + "</div>\n"
    )

def _katex_head(title: str, katex_rel: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{escape(title)}</title>
<style>
body {{ font-family: Georgia, "Iowan Old Style", serif; margin: 1.25rem 1.75rem;
  background: #f7f5f0; color: #1a1a1a; }}
h1 {{ font-size: 1.35rem; margin-bottom: 0.35rem; }}
h2 {{ font-size: 1.1rem; margin-top: 1.4rem; border-bottom: 1px solid #d8d2c4;
  padding-bottom: 0.25rem; }}
.sub {{ color: #555; font-size: 0.9rem; margin-bottom: 1rem; }}
.nav a {{ margin-right: 0.85rem; }}
.card {{ background: #fff; border: 1px solid #d8d2c4; padding: 0.75rem 1rem;
  margin-bottom: 0.75rem; max-width: 52rem; }}
.card.fail {{ border-color: #c44; }}
.card.warn {{ border-color: #c80; }}
header {{ display: flex; flex-wrap: wrap; gap: 0.45rem; align-items: baseline;
  font-size: 0.88rem; margin-bottom: 0.35rem; }}
.n {{ color: #666; }}
.pat {{ color: #3a5a40; font-family: ui-monospace, Consolas, monospace; font-size: 0.82rem; }}
.band {{ background: #e8efe6; padding: 0.05rem 0.35rem; border-radius: 3px;
  font-size: 0.75rem; }}
.band.low {{ background: #e8efe6; }}
.band.mid {{ background: #e6ebe8; }}
.band.high {{ background: #dde8f0; }}
.band.elite {{ background: #e8dde8; }}
.meta {{ font-size: 0.78rem; color: #555; margin: 0.3rem 0; }}
.debug {{ margin-top: 0.55rem; font-size: 0.72rem; background: #f3efe7;
  border: 1px solid #e0d8cc; padding: 0.55rem 0.65rem; }}
.debug h3 {{ margin: 0 0 0.35rem; font-size: 0.78rem; font-weight: 600;
  color: #444; letter-spacing: 0.02em; text-transform: uppercase; }}
.debug dl {{ display: grid; grid-template-columns: 11rem 1fr; gap: 0.15rem 0.6rem;
  margin: 0; }}
.debug dt {{ color: #666; font-family: ui-monospace, Consolas, monospace; }}
.debug dd {{ margin: 0; font-family: ui-monospace, Consolas, monospace;
  word-break: break-word; }}
.debug .section {{ margin-top: 0.45rem; padding-top: 0.35rem;
  border-top: 1px dashed #d8d2c4; }}
.debug .section:first-of-type {{ margin-top: 0; padding-top: 0; border-top: 0; }}
.raw {{ font-size: 0.72rem; white-space: pre-wrap; background: #f0ebe3; padding: 0.45rem; }}
.math {{ margin: 0.4rem 0; }}
.lab {{ font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.04em; }}
.err {{ color: #a20; }}
.notes-alert {{ background: #c62828; color: #fff; padding: 0.7rem 0.95rem;
  font-weight: 700; margin: 0.85rem 0 1rem; max-width: 54rem; }}
.notes-block {{ background: #fff; border: 1px solid #d8d2c4; padding: 0.75rem 1rem;
  margin-bottom: 1rem; max-width: 54rem; font-size: 0.92rem; }}
.notes-block h1 {{ font-size: 1.1rem; margin: 0 0 0.35rem; }}
.notes-block h2 {{ font-size: 1rem; margin: 0.85rem 0 0.35rem; border: 0; padding: 0; }}
.notes-block h2:first-child {{ margin-top: 0; }}
.notes-block ul {{ margin: 0.35rem 0 0.5rem 1.2rem; }}
.notes-block p {{ margin: 0.35rem 0; }}
.notes-table {{ border-collapse: collapse; width: 100%; margin: 0.5rem 0 0.75rem;
  font-size: 0.82rem; }}
.notes-table th, .notes-table td {{ border: 1px solid #d8d2c4; padding: 0.3rem 0.45rem;
  text-align: left; vertical-align: top; }}
.notes-table th {{ background: #f3efe7; }}
code {{ font-family: ui-monospace, Consolas, monospace; font-size: 0.85em; }}
ul.topics {{ line-height: 1.7; }}
.katex .katex-mathml {{
  position: absolute !important;
  clip: rect(1px, 1px, 1px, 1px) !important;
  -webkit-clip-path: inset(50%) !important;
  clip-path: inset(50%) !important;
  padding: 0 !important; border: 0 !important;
  height: 1px !important; width: 1px !important;
  overflow: hidden !important; white-space: nowrap !important;
}}
</style>
<link rel="stylesheet" href="{katex_rel}/katex.min.css"/>
<script defer src="{katex_rel}/katex.min.js"></script>
<script defer src="{katex_rel}/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}],throwOnError:false}});document.documentElement.setAttribute('data-math-ready','1');"></script>
</head>
<body>
"""

def _fmt_val(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return f"{v:g}"
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(str(x) for x in v) + "]"
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False, separators=(",", ":"))
    return str(v)

def _dl_rows(items: list[tuple[str, Any]]) -> str:
    parts: list[str] = []
    for k, v in items:
        if v is None:
            continue
        parts.append(f"<dt>{escape(k)}</dt><dd>{escape(_fmt_val(v))}</dd>")
    return "".join(parts)

def _debug_panel(r: dict) -> str:
    knobs = r.get("richness_knobs") or {}
    spend = r.get("cost_spend") or {}
    indep = r.get("independent_inners") or {}
    identity = [
        ("form_id", r.get("form_id")),
        ("skeleton_pattern", r.get("skeleton_pattern")),
        ("skeleton_kind", r.get("skeleton_kind")),
        ("productions", r.get("productions")),
        ("shared_inner", r.get("shared_inner")),
        ("chosen_outer", r.get("chosen_outer")),
        ("rng_seed", r.get("seed")),
        ("allow_chain", (r.get("allows") or {}).get("allow_chain")),
        ("require_chain", (r.get("allows") or {}).get("require_chain")),
        ("chain_used", "chain" in (r.get("methods") or [])),
        ("allows", r.get("allows")),
    ]
    knob_rows = [
        ("conceptual_d / C", knobs.get("conceptual_d", r.get("conceptual_d"))),
        ("band", knobs.get("band", r.get("band"))),
        ("nest_budget", knobs.get("nest_budget")),
        ("force_min_nest", knobs.get("force_min_nest")),
        ("allow_poly_u", knobs.get("allow_poly_u")),
        ("prefer_poly_u", knobs.get("prefer_poly_u")),
        ("power_min / power_max", f"{knobs.get('power_min')} / {knobs.get('power_max')}"),
        ("poly_degree_min", knobs.get("poly_degree_min")),
        ("coef_abs_max", knobs.get("coef_abs_max")),
        ("atom_fn_candidates", r.get("atom_fn_candidates")),
        ("atom_fn_candidates_g", r.get("atom_fn_candidates_g")),
    ]
    spend_rows = [
        ("inner_kind", spend.get("inner_kind") or r.get("inner_kind")),
        ("inner_latex", r.get("inner_latex")),
        ("inner_degree", spend.get("inner_degree")),
        ("nest_depth_expr", spend.get("nest_depth_expr")),
        ("chain_depth", spend.get("chain_depth") or r.get("chain_depth")),
        ("degree_max", spend.get("degree_max")),
        ("n_applies", spend.get("n_applies")),
        ("n_terms", spend.get("n_terms")),
        ("n_factors", spend.get("n_factors")),
        ("shared_vs_independent", spend.get("shared_vs_independent")),
        ("pattern_locks_top_structure", spend.get("pattern_locks_top_structure")),
        ("note", spend.get("note")),
    ]
    if indep:
        spend_rows.extend(
            [
                ("u_f_kind", indep.get("u_f_kind")),
                ("u_g_kind", indep.get("u_g_kind")),
                ("u_f_latex", indep.get("u_f_latex")),
                ("u_g_latex", indep.get("u_g_latex")),
            ]
        )
    return f"""
<div class="debug">
  <h3>Generation debug</h3>
  <div class="section"><dl>{_dl_rows(identity)}</dl></div>
  <div class="section"><h3>Richness knobs</h3><dl>{_dl_rows(knob_rows)}</dl></div>
  <div class="section"><h3>Cost / spend (honest)</h3><dl>{_dl_rows(spend_rows)}</dl></div>
</div>"""

def _sample_row(
    fid: str,
    d: float,
    allows: dict[str, bool],
    seed: int,
) -> dict:
    order = _order_for(fid)
    try:
        expr, _d_expr, body, deriv, inv = sample_from_form(
            fid,
            conceptual_d=d,
            allows=allows,
            rng=random.Random(seed),
            var="x",
            derivative_order=order,
            seed=seed,
        )
        rich = richness_from_conceptual(
            d,
            allow_roots=bool(allows.get("allow_roots"))
            or bool(FORM_PATTERNS.get(fid) and FORM_PATTERNS[fid].prefer_roots),
        )
        share_check = _shared_u_ok(expr, inv)
        knobs = inv.get("richness_knobs") or rich.as_knobs()
        spend = inv.get("cost_spend") or {}
        note_bits = [
            str(inv.get("skeleton_kind") or ""),
            f"C={d:g}",
            f"band={knobs.get('band', rich.band)}",
            f"inner={spend.get('inner_kind') or inv.get('inner_kind') or '?'}",
            f"nest={spend.get('nest_depth_expr', 0)}",
            f"deg={spend.get('degree_max', 0)}",
        ]
        if inv.get("shared_inner"):
            note_bits.append("shared u")
        else:
            note_bits.append("independent inners")
        if share_check is False:
            note_bits.append("SHARED-U FAIL")
        chain_used = "chain" in (inv.get("methods_used") or [])
        note_bits.append(
            f"chain={'used' if chain_used else 'no'}"
            f"/allow={bool(allows.get('allow_chain'))}"
            f"/req={bool(allows.get('require_chain'))}"
        )
        return {
            "form_id": fid,
            "skeleton_pattern": inv.get("skeleton_pattern")
            or FORM_PATTERNS[fid].label(),
            "skeleton_kind": inv.get("skeleton_kind"),
            "conceptual_d": d,
            "band": knobs.get("band", rich.band),
            "prompt_latex": _prompt(body, order),
            "body_latex": body,
            "answer_latex": deriv,
            "note": "; ".join(note_bits),
            "methods": inv.get("methods_used") or [],
            "classes": inv.get("function_classes") or [],
            "shared_inner": bool(inv.get("shared_inner")),
            "allows": dict(allows),
            "chain_used": chain_used,
            "shared_u_ok": share_check,
            "seed": seed,
            "productions": inv.get("productions"),
            "chosen_outer": inv.get("chosen_outer"),
            "richness_knobs": knobs,
            "cost_spend": spend,
            "atom_fn_candidates": inv.get("atom_fn_candidates"),
            "atom_fn_candidates_g": inv.get("atom_fn_candidates_g"),
            "inner_kind": inv.get("inner_kind") or spend.get("inner_kind"),
            "inner_latex": inv.get("inner_latex"),
            "independent_inners": inv.get("independent_inners"),
            "chain_depth": inv.get("chain_depth"),
            "ok": True,
        }
    except Exception as e:  # noqa: BLE001
        return {
            "form_id": fid,
            "skeleton_pattern": FORM_PATTERNS.get(fid, FORM_PATTERNS["power_poly"]).label()
            if fid in FORM_PATTERNS
            else fid,
            "conceptual_d": d,
            "prompt_latex": "",
            "note": f"FAILED: {type(e).__name__}: {e}",
            "ok": False,
        }

def _cards_html(rows: list[dict]) -> str:
    parts: list[str] = []
    for i, r in enumerate(rows, 1):
        if not r.get("ok"):
            parts.append(
                f"""
<article class="card fail">
  <header><span class="n">#{i}</span> <code>{escape(r['form_id'])}</code></header>
  <p class="err">{escape(r.get('note', ''))}</p>
</article>"""
            )
            continue
        warn = r.get("shared_u_ok") is False
        cls = "card warn" if warn else "card"
        band = str(r.get("band") or "")
        parts.append(
            f"""
<article class="{cls}">
  <header><span class="n">#{i}</span> <code>{escape(r['form_id'])}</code>
    <span class="pat">{escape(str(r.get('skeleton_pattern', '')))}</span>
    <span class="band {escape(band)}">C={escape(str(r.get('conceptual_d', '')))} · {escape(band)}</span></header>
  <div class="math"><div class="lab">Prompt</div>$${r['prompt_latex']}$$</div>
  <div class="math"><div class="lab">Answer</div>$${r.get('answer_latex', '')}$$</div>
  <p class="meta">{escape(r.get('note', ''))} · methods: """
            f"""{escape(', '.join(r.get('methods') or []))} · classes: """
            f"""{escape(', '.join(r.get('classes') or []))}</p>
  {_debug_panel(r)}
  <details><summary>raw latex / answer</summary>
    <pre class="raw">{escape(r['prompt_latex'])}</pre>
    <p>answer: <code>{escape(r.get('answer_latex', ''))}</code></p>
  </details>
</article>"""
        )
    return "".join(parts)

def gen_topic(
    catalog: dict,
    topic_key: str,
    title: str,
) -> dict:
    forms = [
        f
        for f in forms_for_leaf(catalog, topic_key)
        if str(f.get("form_id") or "") in FORM_PATTERNS
    ]
    allows = dict(ALLOWS_BY_TOPIC.get(topic_key, {}))
    # Hard-gate by representative allow kit (checkboxes).
    forms = filter_forms_by_allows(
        forms, allows, conceptual_d=99.0, soft_c_schedule=False
    )
    rows: list[dict] = []
    failures: list[dict] = []
    for fi, form in enumerate(forms):
        fid = str(form["form_id"])
        d_min = float(form.get("d_min") or 0)
        for di, d in enumerate(LADDER_DS):
            if d + 1e-9 < d_min and d < 8:
                continue
            # Soft C schedule: skip fancy forms on the low rungs.
            if not filter_forms_by_allows(
                [form], allows, conceptual_d=d, soft_c_schedule=True
            ):
                continue
            use_d = max(d, d_min)
            seed = 2000 + fi * 100 + di * 7 + sum(ord(c) for c in topic_key) % 97
            row = _sample_row(fid, use_d, allows, seed)
            rows.append(row)
            if not row.get("ok"):
                failures.append(
                    {"form_id": fid, "d": use_d, "error": row.get("note")}
                )
    if topic_key == "derivative_product_rule":
        extra_allows = {
            "allow_trig": True,
            "allow_exp": True,
            "allow_log": True,
            "allow_chain": True,
        }
        for di, d in enumerate((8.0, 14.0, 20.0)):
            seed = 9000 + di * 11
            row = _sample_row("product_trig_exp_chain", d, extra_allows, seed)
            rows.append(row)
            if not row.get("ok"):
                failures.append(
                    {
                        "form_id": "product_trig_exp_chain",
                        "d": d,
                        "error": row.get("note"),
                    }
                )
    slug = topic_key.replace("derivative_", "")
    topic_dir = OUT_DIR / slug
    topic_dir.mkdir(parents=True, exist_ok=True)
    ok_n = sum(1 for r in rows if r.get("ok"))
    warn_n = sum(1 for r in rows if r.get("shared_u_ok") is False)
    (topic_dir / "samples.json").write_text(
        json.dumps({"topic": topic_key, "rows": rows, "failures": failures}, indent=2),
        encoding="utf-8",
    )
    notes_html = _notes_section_html(topic_key, slug)
    html = (
        _katex_head(f"{title} — Diff skeleton", KATEX)
        + f"""
<p class="nav"><a href="../index.html">← all topics</a>
  <a href="../DIFFICULTY_SCALE.md">difficulty scale</a></p>
<h1>{escape(title)}</h1>
<p class="sub"><code>{escape(topic_key)}</code> · live <code>sample_from_form</code>
 · {ok_n}/{len(rows)} ok"""
        + (f" · {warn_n} shared-u warnings" if warn_n else "")
        + f""" · C ladder {', '.join(str(int(d)) if d==int(d) else str(d) for d in LADDER_DS)}
 · each card shows richness knobs + honest cost/spend</p>
{notes_html}
{_cards_html(rows)}
</body></html>
"""
    )
    (topic_dir / "gallery.html").write_text(html, encoding="utf-8")
    return {
        "key": topic_key,
        "slug": slug,
        "title": title,
        "ok": ok_n,
        "total": len(rows),
        "warn": warn_n,
        "forms": [str(f["form_id"]) for f in forms],
    }

def main() -> None:
    catalog = load_form_catalog("derivatives")
    summaries = [gen_topic(catalog, k, t) for k, t in TOPICS]
    mixed_rows: list[dict] = []
    for i, (fid, d, allows) in enumerate(
        [
            ("power_poly", 2.0, {}),
            ("product_poly_trig", 8.0, {"allow_trig": True}),
            ("product_chain_powers", 10.0, {"allow_chain": True}),
            ("product_trig_exp_chain", 10.0, {
                "allow_trig": True, "allow_exp": True, "allow_chain": True,
            }),
            ("trig_product_chain", 10.0, {"allow_trig": True}),
            ("quotient_poly", 4.0, {}),
            ("chain_trig_poly", 8.0, {"allow_trig": True}),
            ("ln_basic", 6.0, {"allow_log": True}),
            ("exp_basic", 6.0, {"allow_exp": True}),
            ("ln_exp_product", 12.0, {"allow_log": True, "allow_exp": True}),
        ]
    ):
        mixed_rows.append(_sample_row(fid, d, allows, 5000 + i * 13))
    overview = (
        _katex_head("Diff skeleton — mixed overview", KATEX_INDEX)
        + """
<p class="nav"><a href="index.html">← all topics</a></p>
<h1>Mixed overview (spot-check)</h1>
<p class="sub">Prefer per-topic pages from the index. This page is a short cross-check with debug panels.</p>
"""
        + _cards_html(mixed_rows)
        + "</body></html>"
    )
    (OUT_DIR / "gallery.html").write_text(overview, encoding="utf-8")
    index_items = []
    for s in summaries:
        index_items.append(
            f'<li><a href="{escape(s["slug"])}/gallery.html"><strong>{escape(s["title"])}</strong></a>'
            f' · <code>{escape(s["key"])}</code> · {s["ok"]}/{s["total"]} ok'
            f' · forms: {escape(", ".join(s["forms"]))}</li>'
        )
    index_html = (
        _katex_head("Diff skeleton galleries — by topic", KATEX_INDEX)
        + f"""
<h1>Diff skeleton galleries by topic</h1>
<p class="sub">OpenStax form → pattern → hole-fill · conceptual C ladder per form ·
  KaTeX · debug knobs + cost/spend on every card ·
  see <a href="DIFFICULTY_SCALE.md">DIFFICULTY_SCALE.md</a></p>
<ul class="topics">
{''.join(index_items)}
</ul>
<p><a href="gallery.html">Mixed overview (spot-check)</a></p>
</body></html>
"""
    )
    (OUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
    scale = """# Differentiation skeleton — conceptual difficulty scale
Conceptual difficulty (`conceptual_difficulty` / C) elaborates **holes** inside
an OpenStax form’s skeleton pattern. It does **not** change the pattern itself
(e.g. C never swaps `Diff(Prod(F,G)(u))` for `Diff(Prod(F,G))`).
Pattern choice comes from the form map in `expr_skeleton.FORM_PATTERNS`.
## Bands
| Band | C (approx) | Inner `u` | Hole F / G / powers | Nest |
|------|------------|-----------|---------------------|------|
| **Low** | 0–4 | Var / Affine | Apply / simple poly of x | 0 |
| **Mid** | 4–12 | Affine → **Poly** unlock | poly-of-u; `power_min` rises | 0 (poly is the unlock) |
| **High** | 12–20 | Poly; **forced nest ≥1** | higher exponents | 1 (Apply or algebraic compose) |
| **Elite** | 20+ | Deeper nest | richest exponents / coefs | 2 |
When the pattern’s atom pool is **poly-only**, nest spends as algebraic compose
(poly / power of a sub-inner) rather than Apply — so C still densifies latex.
## Debug fields (gallery)
Each sample records:
- **Identity:** `form_id`, `skeleton_pattern`, `skeleton_kind`, `productions`, seed
- **Richness knobs:** band, nest_budget, force_min_nest, allow/prefer_poly_u,
  power_min/max, poly_degree_min, coef_abs_max, atomFN candidates
- **Cost / spend (honest):** inner_kind, nest_depth_expr, chain_depth, degree_max,
  n_applies, n_terms — measured from the generated AST, not padded
## Pattern kinds (form-owned)
| Pattern | Meaning | Typical forms |
|---------|---------|---------------|
| `Diff(Pow(H,n))` | Power / chain-power | `power_*`, `chain_power_linear`, higher-order |
| `Diff(Apply(fn,u))` | Named outer | `trig_basic`, `ln_basic`, `exp_basic`, chain/invtrig |
| `Diff(Prod(F,G))` | Product, **independent** inners | `product_two_poly`, `product_poly_trig`, `product_poly_exp` |
| `Diff(Prod(F,G)(u))` | Product, **shared** u | `trig_product_chain`, `ln_exp_product` |
| `Diff(Quot(F,G))` | Quotient, independent inners | `quotient_*` textbook cases |
| `Diff(F(u))` | Loose | `general_mixed` |
## Spec axis
Spec difficulty only spends identity extras (`expression_flesh`), not skeleton
richness. See module docs on `expr_skeleton` / `expression_flesh`.
"""
    (OUT_DIR / "DIFFICULTY_SCALE.md").write_text(scale, encoding="utf-8")
    summary = {"topics": summaries}
    (OUT_DIR / "samples.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("topics:")
    for s in summaries:
        print(f"  {s['slug']}: {s['ok']}/{s['total']} ok warn={s['warn']}")
    print(f"index -> {OUT_DIR / 'index.html'}")
if __name__ == "__main__":
    main()
