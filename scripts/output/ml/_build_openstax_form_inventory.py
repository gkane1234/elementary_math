#!/usr/bin/env python3
"""Build OPENSTAX_FORM_INVENTORY.md/.json from form catalogs + mining + galleries."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CATALOG_DIR = ROOT / "question_engine" / "frameworks" / "primitives" / "openstax_form_catalogs"
MINING_ROOT = ROOT / "scripts" / "output" / "example_mining"
GALLERY_ROOT = ROOT / "scripts" / "output" / "topic_fit"
OUT_MD = ROOT / "scripts" / "output" / "ml" / "OPENSTAX_FORM_INVENTORY.md"
OUT_JSON = ROOT / "scripts" / "output" / "ml" / "OPENSTAX_FORM_INVENTORY.json"

# Course / technique section ordering for the document
SECTION_ORDER: list[tuple[str, str, list[str]]] = [
    (
        "Calc1 — Limits & continuity & L'Hôpital",
        "calc1_limits",
        ["limits"],
    ),
    (
        "Calc1 — Derivatives",
        "calc1_derivatives",
        ["derivatives"],
    ),
    (
        "Calc1 — Integrals (basic / table / power)",
        "calc1_integrals_basic",
        ["basic_power_integrals", "invtrig_integrals"],
    ),
    (
        "Calc1 — Integrals (u-substitution)",
        "calc1_integrals_usub",
        ["u_substitution"],
    ),
    (
        "Calc1 — Integrals (trig integrals)",
        "calc1_integrals_trig",
        ["trig_integrals"],
    ),
    (
        "Calc1 — Integrals (trig substitution)",
        "calc1_integrals_trigsub",
        ["trig_substitution"],
    ),
    (
        "Calc1 — Integrals (integration by parts)",
        "calc1_integrals_parts",
        ["integration_by_parts"],
    ),
    (
        "Calc1 — Integrals (partial fractions)",
        "calc1_integrals_pfd",
        ["partial_fractions"],
    ),
    (
        "Precalculus",
        "precalc",
        [
            "precalculus_function_ops",
            "precalculus_exp_log",
            "precalculus_partial_fractions",
            "precalculus_trig_identities",
            "precalculus_trig_equations",
        ],
    ),
    (
        "Algebra 2",
        "algebra2",
        [
            "algebra2_polys",
            "algebra2_rationals",
            "algebra2_radicals",
            "algebra2_exp_log",
            "algebra2_function_ops",
        ],
    ),
    (
        "Algebra 1",
        "algebra1",
        [
            "algebra1_linear_equations",
            "algebra1_polynomials",
            "algebra1_factoring",
            "algebra1_rationals",
            "algebra1_radicals",
            "algebra1_quadratics",
        ],
    ),
]

GALLERY_FILES = [
    "calc1_algebraic_gallery",
    "a1_algebraic_gallery",
    "a2_algebraic_gallery",
    "pc_algebraic_gallery",
    "poly_expression_spec_gallery",
]


def load_catalogs() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for path in sorted(CATALOG_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        cid = str(data.get("catalog_id") or path.stem)
        data["_path"] = str(path.relative_to(ROOT)).replace("\\", "/")
        out[cid] = data
    return out


def index_mining() -> dict[str, dict[str, Any]]:
    """Map fs-id / item id → {book, section, kind, prompt_latex, label, ...}."""
    by_id: dict[str, dict[str, Any]] = {}
    for stage1 in MINING_ROOT.glob("*/stage1/*.json"):
        if stage1.name.upper().startswith("INDEX"):
            continue
        try:
            data = json.loads(stage1.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        book = data.get("book") or stage1.parent.parent.name
        section = data.get("slug") or data.get("section") or stage1.stem
        title = data.get("title") or section
        items = data.get("items") or []
        if not isinstance(items, list):
            continue
        for it in items:
            if not isinstance(it, dict):
                continue
            iid = it.get("item_id") or it.get("id") or it.get("fs_id")
            if not iid:
                continue
            iid = str(iid)
            bits = it.get("prompt_latex_bits") or []
            if isinstance(bits, list) and bits:
                prompt = " ; ".join(str(x) for x in bits if x)
            else:
                prompt = it.get("prompt_text") or it.get("prompt_latex") or ""
            by_id[iid] = {
                "id": iid,
                "book": book,
                "section": section,
                "section_title": title,
                "kind": it.get("kind") or it.get("type"),
                "label": it.get("title") or it.get("label") or it.get("number"),
                "prompt_latex": str(prompt)[:500] if prompt else None,
                "prompt_text": (it.get("prompt_text") or "")[:400] or None,
                "stage1_path": str(stage1.relative_to(ROOT)).replace("\\", "/"),
                "heading": it.get("nearest_heading") or it.get("heading"),
            }
    return by_id


def _gallery_form_key(o: dict[str, Any]) -> str | None:
    f = o.get("form")
    if isinstance(f, dict):
        return str(f.get("form_id") or f.get("id") or "") or None
    if isinstance(f, str) and f.strip():
        return f.strip()
    for k in ("shape_id", "form_id", "openstax_form", "family"):
        v = o.get(k)
        if v:
            return str(v)
    meta = o.get("metadata") or {}
    if isinstance(meta, dict):
        for k in ("form_id", "openstax_form", "shape_id"):
            if meta.get(k):
                return str(meta[k])
    return None


def index_galleries() -> tuple[
    dict[str, list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
]:
    """Return (by_form_or_shape, by_type_id)."""
    by_form: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for name in GALLERY_FILES:
        path = GALLERY_ROOT / name / "samples.jsonl"
        if not path.exists():
            continue
        for line in path.open(encoding="utf-8"):
            if not line.strip():
                continue
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            fid = _gallery_form_key(o)
            twin = {
                "source": f"gallery:{name}",
                "type_id": o.get("type_id"),
                "difficulty": o.get("difficulty"),
                "seed": o.get("seed"),
                "prompt_latex": o.get("prompt_latex"),
                "shape_id": o.get("shape_id") or fid,
                "pack": o.get("pack"),
                "gallery_form_key": fid,
            }
            tid = o.get("type_id")
            if tid and len(by_type[str(tid)]) < 12:
                by_type[str(tid)].append(twin)
            if not fid:
                continue
            keys = {fid}
            if "__" in fid:
                keys.add(fid.split("__", 1)[0])
            m = re.match(r"^(trig_sub_\w+)_p", fid)
            if m:
                keys.add(m.group(1))
            for k in keys:
                if len(by_form[k]) < 8:
                    by_form[k].append(twin)
    return by_form, by_type


def try_live_generate(
    catalogs: dict[str, dict[str, Any]],
    gallery_by_form: dict[str, list[dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    """Generate a few live twins for catalog forms lacking gallery samples."""
    live: dict[str, list[dict[str, Any]]] = defaultdict(list)
    import random

    def _record(fid: str, *, topic: str, d: float, seed: int, prompt: str, type_id: str) -> None:
        if not fid or not prompt:
            return
        if len(live[fid]) >= 3:
            return
        if gallery_by_form.get(fid) and len(gallery_by_form[fid]) >= 2:
            return
        live[fid].append(
            {
                "source": "live_generate",
                "topic": topic,
                "difficulty": d,
                "seed": seed,
                "prompt_latex": str(prompt)[:400],
                "type_id": type_id,
                "shape_id": fid,
            }
        )

    def _meta_fid(meta: dict[str, Any]) -> str | None:
        for k in ("form_id", "openstax_form", "shape_id", "family"):
            if meta.get(k):
                return str(meta[k])
        return None

    # Integrals via settings dict
    try:
        from question_engine.frameworks.primitives.integrals import (
            sample_integral_expression,
        )

        integral_jobs = [
            ("calc_indef_int_trigonometric", 8.0),
            ("calc_indef_int_trigonometric", 16.0),
            ("calc_indef_int_trigonometric", 20.0),
            ("calc_indef_int_power_rule_with_substitution", 10.0),
            ("calc_indef_int_integration_by_parts", 12.0),
            ("calc_indef_int_partial_fractions", 10.0),
            ("calc_indef_int_trigonometric_with_substitution", 10.0),
            ("calc_indef_int_power_rule", 6.0),
            ("calc_indef_int_inverse_trigonometric", 8.0),
            ("calc_indef_int_logarithmic_rule_and_exponentials_with_substitution", 10.0),
        ]
        for gkey, d in integral_jobs:
            for seed in (41, 107, 233, 419):
                rng = random.Random(seed + int(d * 10))
                try:
                    sample = sample_integral_expression(
                        {"difficulty": d, "seed": seed},
                        generator_key=gkey,
                        rng=rng,
                    )
                except Exception:
                    continue
                meta = dict(getattr(sample, "metadata", None) or {})
                fid = _meta_fid(meta) or getattr(sample, "shape_id", None)
                prompt = getattr(sample, "prompt_latex", None) or getattr(
                    sample, "integrand_latex", None
                )
                if not prompt and hasattr(sample, "latex"):
                    prompt = sample.latex
                _record(
                    str(fid) if fid else "",
                    topic=gkey,
                    d=d,
                    seed=seed,
                    prompt=str(prompt or ""),
                    type_id=gkey,
                )
    except Exception as e:
        live["_integral_error"] = [{"error": str(e)}]  # type: ignore

    # Limits
    try:
        from question_engine.frameworks.primitives.limits import (
            sample_limit_expression,
        )
        import inspect

        sig = inspect.signature(sample_limit_expression)
        for topic, d in [
            ("limit_direct_evaluation", 4.0),
            ("limit_at_infinity", 8.0),
            ("limit_removable", 6.0),
            ("lhopitals_rule", 12.0),
        ]:
            for seed in (41, 107, 233):
                rng = random.Random(seed)
                kwargs: dict[str, Any] = {}
                params = sig.parameters
                if "rng" in params:
                    kwargs["rng"] = rng
                if "topic" in params:
                    kwargs["topic"] = topic
                if "settings" in params:
                    kwargs["settings"] = {"difficulty": d, "seed": seed}
                elif "difficulty" in params:
                    kwargs["difficulty"] = d
                elif "d" in params:
                    kwargs["d"] = d
                try:
                    sample = sample_limit_expression(**kwargs)
                except TypeError:
                    try:
                        sample = sample_limit_expression(
                            {"difficulty": d, "seed": seed}, topic=topic, rng=rng
                        )
                    except Exception:
                        continue
                except Exception:
                    continue
                meta = {}
                prompt = None
                if hasattr(sample, "metadata"):
                    meta = dict(sample.metadata or {})
                if hasattr(sample, "prompt_latex"):
                    prompt = sample.prompt_latex
                elif isinstance(sample, dict):
                    meta = sample.get("metadata") or sample
                    prompt = sample.get("prompt_latex")
                fid = _meta_fid(meta)
                _record(
                    fid or "",
                    topic=topic,
                    d=d,
                    seed=seed,
                    prompt=str(prompt or ""),
                    type_id=topic,
                )
    except Exception:
        pass

    return live


def _append_twins(
    out: list[dict[str, Any]],
    seen: set[str],
    samples: list[dict[str, Any]],
    *,
    match_note: str | None = None,
    limit: int = 3,
) -> None:
    for src in samples:
        key = str(src.get("prompt_latex") or "")
        if not key or key in seen:
            continue
        seen.add(key)
        item = dict(src)
        if match_note:
            item["match_note"] = match_note
        out.append(item)
        if len(out) >= limit:
            return


# Coarse strategy / form_id → gallery shape_id aliases (A1/A2/PC + calc)
_SHAPE_ALIASES: dict[str, list[str]] = {
    "gcf_monomial": ["factor_gcf"],
    "factor_gcf": ["factor_gcf"],
    "factor_by_grouping": ["grouping_cubic", "grouping"],
    "trinomial_x2_bx_c": ["factor_gcf", "construct_poly"],
    "trinomial_ax2_bx_c": ["factor_gcf", "construct_poly"],
    "difference_of_squares": ["difference_of_cubes", "factor_gcf"],
    "sum_difference_cubes": ["difference_of_cubes"],
    "sum_diff_cubes": ["difference_of_cubes"],
    "poly_add": ["+", "construct_poly"],
    "poly_subtract": ["-", "construct_poly"],
    "mono_times_poly": ["distribute"],
    "binomial_times_binomial": ["foil", "distribute"],
    "poly_times_poly": ["distribute", "foil"],
    "simplify_rational": ["simplify_rational"],
    "add_subtract_rationals": ["add_subtract_rationals"],
    "log_props": ["structured_log_props"],
    "exp_equation": ["structured_exp_equation"],
    "function_ops": ["structured_function_ops"],
    "pfd": ["pfd", "pfd_constructive", "pfd_quad_arctan"],
    "distinct_linear_2": ["pfd_constructive", "pfd"],
    "irreducible_quad_arctan": ["pfd_quad_arctan"],
    "poly_direct": ["poly_direct"],
    "rational_direct": ["rational_direct"],
    "removable_factor": ["removable_factor"],
    "removable_rationalize": ["removable_rationalize"],
    "rational_inf": ["rational_inf"],
    "piecewise_jump": ["piecewise_jump"],
    "essential": ["essential"],
    "indet_0_0": ["indet_0_0"],
    "indet_inf_inf": ["indet_inf_inf"],
    # parts catalog form_id → gallery shape_id
    "ln_alone": ["ln"],
    "poly1_ln": ["x_ln"],
    "poly1_exp": ["x_exp"],
    "poly1_sin": ["x_sin"],
    "poly1_cos": ["x_cos"],
    "poly2_exp": ["x2_exp"],
    "poly2_sin": ["x_sin"],
    "cyclic_exp_sin": ["exp_sin"],
    "cyclic_exp_cos": ["exp_sin"],
    # trig-sub catalog → gallery openstax_form style
    "sqrt_a2_minus_x2": ["trig_sub_sin_p1/2"],
    "sqrt_a2_plus_x2": ["trig_sub_tan_p1/2"],
    "sqrt_x2_minus_a2": ["trig_sub_sec_p1/2"],
    "one_over_sqrt_x2_plus_a2": ["trig_sub_tan_p-1/2"],
    "one_over_sqrt_x2_minus_a2": ["trig_sub_sec_p-1/2"],
    "power_poly": ["power", "sum+power"],
    "power_root": ["power", "sum+power"],
    "product_two_poly": ["product+power", "product+sum+power"],
    "chain_power": ["sum+power"],
}


def resolve_twins(
    form: dict[str, Any],
    gallery_by_form: dict[str, list[dict[str, Any]]],
    gallery_by_type: dict[str, list[dict[str, Any]]],
    live: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    form_id = str(form.get("form_id") or "")
    strategy = str(form.get("strategy") or "")
    seen: set[str] = set()
    out: list[dict[str, Any]] = []

    _append_twins(out, seen, gallery_by_form.get(form_id) or [])
    _append_twins(out, seen, live.get(form_id) or [])

    if len(out) < 3 and strategy:
        _append_twins(
            out,
            seen,
            gallery_by_form.get(strategy) or [],
            match_note=f"matched gallery shape_id~strategy `{strategy}`",
        )

    if len(out) < 3:
        for alias in _SHAPE_ALIASES.get(form_id, []) + _SHAPE_ALIASES.get(strategy, []):
            _append_twins(
                out,
                seen,
                gallery_by_form.get(alias) or [],
                match_note=f"alias `{alias}`",
            )
            if len(out) >= 3:
                break

    if len(out) < 3:
        for k, samples in gallery_by_form.items():
            if k == form_id:
                continue
            if k.startswith(form_id + "__") or k.startswith(form_id + "_"):
                _append_twins(
                    out,
                    seen,
                    samples,
                    match_note=f"prefix match `{k}`",
                )
            if len(out) >= 3:
                break

    if len(out) < 3:
        for tid in list(form.get("leaves") or []) + list(form.get("_type_ids") or []):
            samples = gallery_by_type.get(str(tid)) or []
            _append_twins(
                out,
                seen,
                samples,
                match_note=f"type_id sibling `{tid}` (not form_id-exact)",
            )
            if len(out) >= 3:
                break

    return out[:3]


# Map catalog generator_keys / leaf packs → gallery type_ids
_GENERATOR_TO_TYPE: dict[str, list[str]] = {
    "limit_direct_evaluation": ["calc_limits_by_direct_evaluation"],
    "limit_at_infinity": ["calc_limits_at_infinity"],
    "limit_removable": ["calc_limits_at_removable_discontinuities"],
    "limit_jump": ["calc_limits_at_jump_discontinuities_and_kinks"],
    "limit_essential": ["calc_limits_at_essential_discontinuities"],
    "lhopitals_rule": ["calc_app_diff_lhopitals_rule"],
    "continuity": ["calc_continuity_determining_and_classifying"],
    "derivative_power_rule": ["calc_diff_power_rule"],
    "derivative_product_rule": ["calc_diff_product_rule"],
    "derivative_quotient_rule": ["calc_diff_general", "calc_diff_product_rule"],
    "derivative_chain_rule": ["calc_diff_chain_rule"],
    "derivative_trig": ["calc_diff_trigonometric"],
    "derivative_exp_log": ["calc_diff_natural_logarithms_and_exponentials"],
    "derivative_invtrig": ["calc_diff_inverse_trigonometric"],
    "derivative_higher_order": ["calc_diff_power_rule", "calc_diff_general"],
    "derivative_general": ["calc_diff_general"],
    "diff_power_rule": ["calc_diff_power_rule"],
    "diff_product_rule": ["calc_diff_product_rule"],
    "diff_chain_rule": ["calc_diff_chain_rule"],
    "diff_trig": ["calc_diff_trigonometric"],
    "diff_log_exp": ["calc_diff_natural_logarithms_and_exponentials"],
    "diff_invtrig": ["calc_diff_inverse_trigonometric"],
    "diff_general": ["calc_diff_general"],
    "integral_power": ["calc_indef_int_power_rule"],
    "integral_trig": ["calc_indef_int_trigonometric"],
    "integral_log_exp": ["calc_indef_int_logarithmic_rule_and_exponentials"],
    "integral_invtrig": ["calc_indef_int_inverse_trigonometric"],
    "integral_substitution": [
        "calc_indef_int_power_rule_with_substitution",
        "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
        "calc_indef_int_trigonometric_with_substitution",
    ],
    "integral_parts": ["calc_indef_int_integration_by_parts"],
    "integral_partial_fractions": ["calc_indef_int_partial_fractions"],
    "integral_trig_sub": ["calc_indef_int_trigonometric_with_substitution"],
}


def form_type_ids(catalog: dict[str, Any], form: dict[str, Any]) -> list[str]:
    leaves = form.get("leaves") or []
    wired = catalog.get("wired_type_ids") or []
    gkeys = form.get("generator_keys") or []
    out: list[str] = []
    for x in list(leaves) + list(wired) + list(gkeys):
        s = str(x)
        if s and s not in out:
            out.append(s)
        for mapped in _GENERATOR_TO_TYPE.get(s, []):
            if mapped not in out:
                out.append(mapped)
    cid = str(catalog.get("catalog_id") or "")
    catalog_defaults = {
        "integration_by_parts": ["calc_indef_int_integration_by_parts"],
        "trig_substitution": ["calc_indef_int_trigonometric_with_substitution"],
        "partial_fractions": ["calc_indef_int_partial_fractions"],
        "u_substitution": [
            "calc_indef_int_power_rule_with_substitution",
            "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
            "calc_indef_int_trigonometric_with_substitution",
        ],
        "basic_power_integrals": ["calc_indef_int_power_rule"],
        "invtrig_integrals": ["calc_indef_int_inverse_trigonometric"],
        "trig_integrals": ["calc_indef_int_trigonometric"],
        "derivatives": ["calc_diff_general"],
    }
    for t in catalog_defaults.get(cid, []):
        if t not in out:
            out.append(t)
    return out


def course_bucket(catalog_id: str) -> str:
    if catalog_id.startswith("algebra1"):
        return "algebra1"
    if catalog_id.startswith("algebra2"):
        return "algebra2"
    if catalog_id.startswith("precalculus"):
        return "precalc"
    if catalog_id in {"limits"}:
        return "calc1_limits"
    if catalog_id in {"derivatives"}:
        return "calc1_derivatives"
    if catalog_id in {"basic_power_integrals", "invtrig_integrals"}:
        return "calc1_integrals_basic"
    if catalog_id == "u_substitution":
        return "calc1_integrals_usub"
    if catalog_id == "trig_integrals":
        return "calc1_integrals_trig"
    if catalog_id == "trig_substitution":
        return "calc1_integrals_trigsub"
    if catalog_id == "integration_by_parts":
        return "calc1_integrals_parts"
    if catalog_id == "partial_fractions":
        return "calc1_integrals_pfd"
    return "other"


def build() -> tuple[dict[str, Any], str]:
    catalogs = load_catalogs()
    mining = index_mining()
    gallery_by_form, gallery_by_type = index_galleries()
    live = try_live_generate(catalogs, gallery_by_form)

    forms_out: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    by_course_status: dict[str, Counter[str]] = defaultdict(Counter)
    cited_with_prompt = 0
    cited_missing_prompt = 0
    forms_with_twins = 0
    forms_with_exact_twins = 0
    section_only_notes: list[str] = []

    for cid, cat in catalogs.items():
        src = cat.get("source") or {}
        primary = src.get("primary") or {}
        for form in cat.get("forms") or []:
            if not isinstance(form, dict):
                continue
            fid = str(form.get("form_id") or "")
            status = str(form.get("generation_status") or "unknown")
            status_counts[status] += 1
            bucket = course_bucket(cid)
            by_course_status[bucket][status] += 1

            cited: list[dict[str, Any]] = []
            for eid in form.get("example_item_ids") or []:
                eid = str(eid)
                hit = mining.get(eid)
                if hit and hit.get("prompt_latex"):
                    cited_with_prompt += 1
                    cited.append(hit)
                elif hit:
                    cited_missing_prompt += 1
                    cited.append(hit)
                else:
                    cited_missing_prompt += 1
                    cited.append(
                        {
                            "id": eid,
                            "prompt_latex": None,
                            "note": "id not found in stage-1 mining index",
                        }
                    )

            case = form.get("openstax_case") or ""
            if not (form.get("example_item_ids") or []) and case:
                section_only_notes.append(f"{cid}/{fid}: {case}")

            type_ids = form_type_ids(cat, form)
            form_for_twins = dict(form)
            form_for_twins["_type_ids"] = type_ids
            twins = resolve_twins(form_for_twins, gallery_by_form, gallery_by_type, live)

            # Live-generate via worksheet API when galleries lack this leaf
            if len(twins) < 2 and status == "implemented":
                import io
                import contextlib

                candidates = [
                    t
                    for t in (list(form.get("leaves") or []) + type_ids)
                    if t
                    and not str(t).startswith(("limit_", "derivative_", "integral_"))
                    and str(t) not in gallery_by_type
                ]
                seen_t: set[str] = set()
                for tid in candidates:
                    if tid in seen_t:
                        continue
                    seen_t.add(tid)
                    for seed, d in ((41, 5.0), (107, 10.0)):
                        if len(twins) >= 3:
                            break
                        try:
                            from question_engine.api.handler import _generate_for_type

                            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
                                io.StringIO()
                            ):
                                qs = _generate_for_type(
                                    tid,
                                    {"difficulty": d, "seed": seed, "count": 1},
                                )
                        except Exception:
                            break  # unknown type_id
                        for q in qs or []:
                            prompt = getattr(q, "prompt_latex", None)
                            if not prompt and hasattr(q, "to_dict"):
                                prompt = (q.to_dict() or {}).get("prompt_latex")
                            if not prompt:
                                continue
                            key = str(prompt)
                            if any(str(t.get("prompt_latex")) == key for t in twins):
                                continue
                            twins.append(
                                {
                                    "source": "live_generate",
                                    "type_id": tid,
                                    "difficulty": d,
                                    "seed": seed,
                                    "prompt_latex": str(prompt)[:400],
                                    "shape_id": fid,
                                    "match_note": f"live generate type_id `{tid}`",
                                }
                            )
                            if len(twins) >= 3:
                                break
                    if len(twins) >= 3:
                        break

            if twins:
                forms_with_twins += 1
                if any(not t.get("match_note") for t in twins):
                    forms_with_exact_twins += 1

            entry = {
                "form_id": fid,
                "catalog_id": cid,
                "course_bucket": bucket,
                "description": form.get("description"),
                "strategy": form.get("strategy"),
                "generation_status": status,
                "d_min": form.get("d_min"),
                "d_max": form.get("d_max"),
                "d_weight": form.get("d_weight"),
                "tricks": form.get("tricks") or [],
                "constraints": form.get("constraints"),
                "openstax_case": case,
                "gap_reason": form.get("gap_reason"),
                "book": primary.get("book"),
                "section_slug": primary.get("slug") or primary.get("title"),
                "section_title": primary.get("title"),
                "section_url": primary.get("url"),
                "stage1": primary.get("stage1"),
                "stage1_note": primary.get("note"),
                "related_sources": src.get("related") or [],
                "cited_exercises": cited,
                "type_ids": type_ids,
                "leaves": form.get("leaves") or [],
                "live_twins": twins[:3],
                "catalog_path": cat.get("_path"),
                "wired_note": None,
            }
            # Honesty: catalog exists but may not be wired into sampler
            if status == "implemented":
                exact = any(not t.get("match_note") for t in twins)
                if not twins:
                    entry["wired_note"] = (
                        "Catalog marks implemented; no gallery/live twin matched "
                        "(exact form_id, strategy, alias, or leaf type_id). "
                        "May still be wired under a different shape_id naming scheme."
                    )
                elif not exact and not form.get("leaves"):
                    entry["wired_note"] = (
                        "Twins are alias/type_id siblings only — form_id may not be "
                        "stamped on generated metadata yet."
                    )
            forms_out.append(entry)

    # Section-level inspiration without form catalogs (from code docs)
    code_inspiration = [
        {
            "area": "Calc1 limits",
            "file": "question_engine/frameworks/primitives/limits.py",
            "note": (
                "OpenStax Vol.1 §2.3 direct, §4.6 ∞, §4.8 L'Hôpital mirrored in "
                "sampler families; now also catalogued in limits.json. "
                "openstax_form stamps like direct_{fam}, inf_{fam}, lhopital_*."
            ),
        },
        {
            "area": "Calc1 derivatives",
            "file": "question_engine/frameworks/primitives/derivatives.py",
            "note": (
                "Grounded in OpenStax Calc Vol.1 Ch.3 patterns; "
                "derivatives.json form catalog added. poly_expression packs "
                "also cite OpenStax 3.6 chain+power."
            ),
        },
        {
            "area": "Curriculum gaps (section-level only)",
            "file": "scripts/output/curriculum_gaps/*.md",
            "note": (
                "Many OpenStax sections mapped as missing/partial/unwired at "
                "curriculum grain — not per-exercise form catalogs. See "
                "calculus.md, algebra_1.md, algebra_2.md, precalculus.md."
            ),
        },
    ]

    inventory = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "catalog_count": len(catalogs),
        "catalog_ids": sorted(catalogs.keys()),
        "form_count": len(forms_out),
        "status_counts": dict(status_counts),
        "by_course_status": {k: dict(v) for k, v in by_course_status.items()},
        "mining_index_size": len(mining),
        "cited_with_prompt": cited_with_prompt,
        "cited_missing_or_empty_prompt": cited_missing_prompt,
        "forms_with_twins": forms_with_twins,
        "forms_with_exact_form_id_twins": forms_with_exact_twins,
        "section_level_only_form_count": len(section_only_notes),
        "code_inspiration_without_per_exercise_ids": code_inspiration,
        "forms": forms_out,
        "honesty": {
            "stage1_is_inventory_only": True,
            "stage2_family_tagging": "not started",
            "catalogs_vs_wiring": (
                "generation_status=implemented means the catalog author believes "
                "a sampler can emit the form; gallery shape_id / live generate "
                "are the best evidence of live wiring. Some catalogs list leaves "
                "type_ids; others are taxonomy-only until Spec samplers call "
                "select_form_id."
            ),
            "trig_integrals_is_reference_pipeline": (
                "See scripts/output/ml/OPENSTAX_FORM_CATALOG.md — trig integrals "
                "is the first fully catalog→select_form_id→metadata pipeline."
            ),
            "mining_missing_sections": sorted(
                cid
                for cid, cat in catalogs.items()
                if not ((cat.get("source") or {}).get("primary") or {}).get("stage1")
            ),
        },
    }

    md = render_md(inventory, catalogs)
    return inventory, md


def _esc(s: Any) -> str:
    return str(s).replace("|", "\\|") if s is not None else ""


def render_md(inv: dict[str, Any], catalogs: dict[str, dict[str, Any]]) -> str:
    lines: list[str] = []
    sc = inv["status_counts"]
    lines.append("# OpenStax / mined form inventory")
    lines.append("")
    lines.append(f"Generated: `{inv['generated_at']}`")
    lines.append("")
    lines.append("Machine-readable twin: `scripts/output/ml/OPENSTAX_FORM_INVENTORY.json`")
    lines.append("")
    lines.append("## Executive summary")
    lines.append("")
    lines.append(
        f"- **Catalogs on disk:** {inv['catalog_count']} "
        f"(`{'`, `'.join(inv['catalog_ids'])}`)"
    )
    lines.append(f"- **Total forms:** {inv['form_count']}")
    lines.append(
        f"- **By generation_status:** implemented={sc.get('implemented', 0)}, "
        f"stub={sc.get('stub', 0)}, deferred={sc.get('deferred', 0)}, "
        f"other={sum(v for k, v in sc.items() if k not in {'implemented', 'stub', 'deferred'})}"
    )
    lines.append(
        f"- **Forms with >=1 twin** (exact / alias / type_id sibling): "
        f"{inv['forms_with_twins']} / {inv['form_count']} "
        f"(exact form_id match: {inv.get('forms_with_exact_form_id_twins', '?')})"
    )
    lines.append(
        f"- **Cited mining ids with prompt LaTeX:** {inv['cited_with_prompt']}; "
        f"cited missing/empty: {inv['cited_missing_or_empty_prompt']}"
    )
    lines.append(
        f"- **Forms with section-level inspiration only** "
        f"(no `example_item_ids`): {inv['section_level_only_form_count']}"
    )
    lines.append(f"- **Mining index size (item ids):** {inv['mining_index_size']}")
    lines.append("")
    lines.append("### Honesty")
    lines.append("")
    lines.append(
        "- Stage-1 mining (`scripts/output/example_mining/*/stage1/`) is an "
        "**inventory dump** (prompt LaTeX + headings). It does **not** tag "
        "`form_id`. Stage-2 family tagging is **not started**."
    )
    lines.append(
        "- Explicit form catalogs under "
        "`question_engine/frameworks/primitives/openstax_form_catalogs/` are the "
        "taxonomy layer. `generation_status=implemented` is author intent; "
        "**gallery `shape_id` / live generate** are the evidence a twin can be "
        "produced today."
    )
    lines.append(
        "- **Reference pipeline:** trig integrals "
        "(`OPENSTAX_FORM_CATALOG.md`) — catalog → `select_form_id` → Spec sampler "
        "→ metadata `form_id` / `openstax_form`."
    )
    lines.append(
        "- Several catalogs have `stage1: null` (section not mined yet) — "
        "inspiration is **section-level** from the OpenStax TOC / prose, not "
        "per-exercise ids."
    )
    lines.append(
        "- Curriculum-gap docs map many OpenStax sections as missing/partial "
        "without per-form catalogs."
    )
    lines.append(
        "- **Twin matching honesty:** `exact form_id match` means gallery "
        "`shape_id`/`form` equals catalog `form_id` (or live metadata stamped "
        "the same). Many A1/A2/PC twins are **type_id siblings** or live "
        "`_generate_for_type` samples — similar skill, not guaranteed same "
        "textbook case. Algebraic galleries omit several leaves (linear "
        "equations, quadratics solve methods, A2 radicals, PC trig eq/"
        "identities); those were live-generated for this inventory."
    )
    lines.append(
        "- Some `example_item_ids` in catalogs resolve to mining items whose "
        "prompt is clearly the wrong exercise (e.g. identity fill-ins under "
        "trig-integral forms). Treat cited LaTeX as **what mining has for "
        "that id**, and prefer `openstax_case` labels for intent."
    )
    lines.append("")
    lines.append("### Counts by course bucket")
    lines.append("")
    lines.append("| Bucket | implemented | stub | deferred | total |")
    lines.append("|--------|------------:|-----:|---------:|------:|")
    for title, bucket, _ in SECTION_ORDER:
        c = inv["by_course_status"].get(bucket) or {}
        tot = sum(c.values())
        if not tot:
            continue
        lines.append(
            f"| {title} | {c.get('implemented', 0)} | {c.get('stub', 0)} | "
            f"{c.get('deferred', 0)} | {tot} |"
        )
    lines.append("")

    # Index forms by catalog
    by_cat: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for f in inv["forms"]:
        by_cat[f["catalog_id"]].append(f)

    for title, _bucket, cat_ids in SECTION_ORDER:
        present = [c for c in cat_ids if c in catalogs]
        if not present:
            lines.append(f"## {title}")
            lines.append("")
            lines.append("_No form catalogs present on disk for this section yet._")
            lines.append("")
            continue
        lines.append(f"## {title}")
        lines.append("")
        for cid in present:
            cat = catalogs[cid]
            forms = by_cat.get(cid) or []
            src = (cat.get("source") or {}).get("primary") or {}
            lines.append(f"### Catalog `{cid}`")
            lines.append("")
            lines.append(f"- **Title:** {cat.get('title')}")
            lines.append(f"- **Path:** `{cat.get('_path')}`")
            if src.get("book"):
                lines.append(
                    f"- **OpenStax:** {src.get('book')} — {src.get('title') or src.get('slug')}"
                )
            if src.get("url"):
                lines.append(f"- **URL:** {src['url']}")
            if src.get("stage1"):
                lines.append(f"- **Stage-1 mining:** `{src['stage1']}`")
            elif src.get("note"):
                lines.append(f"- **Mining note:** {src['note']}")
            st = Counter(f["generation_status"] for f in forms)
            lines.append(
                f"- **Forms:** {len(forms)} "
                f"(implemented={st.get('implemented', 0)}, stub={st.get('stub', 0)}, "
                f"deferred={st.get('deferred', 0)})"
            )
            if cat.get("wired_type_ids"):
                lines.append(
                    f"- **Wired type_ids (catalog):** "
                    + ", ".join(f"`{t}`" for t in cat["wired_type_ids"])
                )
            notes = cat.get("taxonomy_notes") or []
            if notes:
                lines.append(f"- **Taxonomy notes:** {notes[0]}")
            lines.append("")

            for form in forms:
                fid = form["form_id"]
                lines.append(f"#### `{fid}` — {form.get('generation_status')}")
                lines.append("")
                if form.get("description"):
                    lines.append(f"- **Description:** {form['description']}")
                if form.get("strategy"):
                    lines.append(f"- **Strategy:** `{form['strategy']}`")
                lines.append(
                    f"- **D gate:** d_min={form.get('d_min')}, "
                    f"d_max={form.get('d_max')}, d_weight={form.get('d_weight')}"
                )
                if form.get("openstax_case"):
                    lines.append(f"- **OpenStax case:** {form['openstax_case']}")
                if form.get("book") or form.get("section_title"):
                    lines.append(
                        f"- **Book / section:** {form.get('book')} / "
                        f"{form.get('section_title') or form.get('section_slug')}"
                    )
                tids = form.get("type_ids") or []
                leaves = form.get("leaves") or []
                if tids or leaves:
                    lines.append(
                        "- **type_id / leaves:** "
                        + ", ".join(f"`{t}`" for t in (leaves or tids))
                    )
                elif form.get("wired_note"):
                    lines.append(f"- **Wiring:** {form['wired_note']}")
                if form.get("gap_reason"):
                    lines.append(f"- **Gap reason:** {form['gap_reason']}")

                cited = form.get("cited_exercises") or []
                if cited:
                    lines.append("- **Cited exercises / examples:**")
                    for c in cited:
                        lab = c.get("label") or c.get("kind") or ""
                        prompt = c.get("prompt_latex")
                        if prompt:
                            pl = prompt.replace("\n", " ")
                            if len(pl) > 220:
                                pl = pl[:217] + "..."
                            lines.append(
                                f"  - `{c.get('id')}` {lab}: `{pl}`"
                            )
                        else:
                            note = c.get("note") or "no prompt in mining"
                            lines.append(f"  - `{c.get('id')}` {lab}: _{note}_")
                else:
                    lines.append(
                        "- **Cited exercises:** _(none — section-level inspiration only)_"
                    )

                twins = form.get("live_twins") or []
                if twins:
                    lines.append("- **Generated twins (gallery / live):**")
                    for t in twins:
                        d = t.get("difficulty")
                        seed = t.get("seed")
                        tid = t.get("type_id") or ""
                        src = t.get("source") or ""
                        note = t.get("match_note")
                        pl = (t.get("prompt_latex") or "").replace("\n", " ")
                        if len(pl) > 220:
                            pl = pl[:217] + "..."
                        suffix = f" _{note}_" if note else ""
                        lines.append(
                            f"  - [{src}] type=`{tid}` D={d} seed={seed}: `{pl}`{suffix}"
                        )
                else:
                    lines.append(
                        "- **Generated twins:** _(none matched in galleries; "
                        "status may still be implemented via a different shape_id)_"
                    )
                lines.append("")

    lines.append("## Code / section-level inspiration (no per-exercise catalog id)")
    lines.append("")
    for row in inv.get("code_inspiration_without_per_exercise_ids") or []:
        lines.append(f"- **{row['area']}** (`{row['file']}`): {row['note']}")
    lines.append("")
    lines.append("## Catalog files not yet mirrored under example_mining/form_catalogs")
    lines.append("")
    lines.append(
        "Canonical catalogs live in `openstax_form_catalogs/`. Only "
        "`calculus-volume-2/form_catalogs/trig_integrals.json` was mirrored next "
        "to stage-1 at inventory time — treat the primitives path as source of truth."
    )
    lines.append("")
    lines.append("## How to refresh")
    lines.append("")
    lines.append("```powershell")
    lines.append("$env:PYTHONPATH='.'")
    lines.append("python scripts/output/ml/_build_openstax_form_inventory.py")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    inv, md = build()
    OUT_JSON.write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(md, encoding="utf-8")
    sc = inv["status_counts"]
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")
    print(
        f"catalogs={inv['catalog_count']} forms={inv['form_count']} "
        f"implemented={sc.get('implemented', 0)} stub={sc.get('stub', 0)} "
        f"deferred={sc.get('deferred', 0)} twins={inv['forms_with_twins']}"
    )


if __name__ == "__main__":
    main()
