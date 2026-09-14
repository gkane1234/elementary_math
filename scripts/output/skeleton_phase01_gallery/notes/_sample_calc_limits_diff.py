"""One-shot sampler for Calculus limits/diff notes (steps 1–3)."""
from __future__ import annotations

import json
from pathlib import Path

from question_engine.api.handler import _generate_for_type

TYPES = [
    # limits / continuity / indeterminate
    "calc_limits_by_direct_evaluation",
    "calc_limits_at_jump_discontinuities_and_kinks",
    "calc_limits_at_removable_discontinuities",
    "calc_limits_at_essential_discontinuities",
    "calc_limits_at_infinity",
    "calc_continuity_determining_and_classifying",
    "calc_app_diff_lhopitals_rule",
    # diffs
    "calc_diff_power_rule",
    "calc_diff_product_rule",
    "calc_diff_quotient_rule",
    "calc_diff_chain_rule",
    "calc_diff_trigonometric",
    "calc_diff_inverse_trigonometric",
    "calc_diff_natural_logarithms_and_exponentials",
    "calc_diff_general",
    "calc_diff_higher_order_derivatives",
    "calc_diff_implicit",
    "calc_diff_other_base_logarithms_and_exponentials",
    "calc_diff_logarithmic",
    "calc_diff_definition_of_the_derivative",
]

SEED = 101
out: dict = {}
for tid in TYPES:
    out[tid] = {}
    for d in (0, 8, 16, 22):
        try:
            qs = _generate_for_type(
                tid,
                {
                    "difficulty": d,
                    "seed": SEED,
                    "count": 1,
                    "include_answer_key": True,
                },
            )
            q = qs[0]
            meta = getattr(q, "metadata", None) or {}
            if hasattr(meta, "items"):
                meta = dict(meta)
            snap = meta.get("spec_snapshot")
            pack = snap.get("pack") if isinstance(snap, dict) else None
            out[tid][str(d)] = {
                "prompt": getattr(q, "prompt_latex", None) or getattr(q, "prompt", ""),
                "answer": getattr(q, "answer_latex", None) or getattr(q, "answer", ""),
                "form_id": meta.get("form_id") or meta.get("openstax_form"),
                "skeleton_pattern": meta.get("skeleton_pattern"),
                "skeleton_source": meta.get("skeleton_source"),
                "pack": pack,
                "methods": list(meta.get("methods_used") or [])[:8]
                if meta.get("methods_used")
                else None,
                "error": None,
            }
        except Exception as e:  # noqa: BLE001
            out[tid][str(d)] = {"error": f"{type(e).__name__}: {e}"}

dest = Path(__file__).with_name("_calc_limits_diff_samples.json")
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"wrote {dest}")
for tid, rows in out.items():
    errs = [d for d, r in rows.items() if r.get("error")]
    ok = [d for d, r in rows.items() if not r.get("error")]
    print(f"{tid}: ok={ok} errs={errs}")
    for d in ("0", "8", "16", "22"):
        r = rows[d]
        if r.get("error"):
            print(f"  D={d} ERROR {r['error'][:120]}")
        else:
            p = (r.get("prompt") or "")[:100]
            print(f"  D={d} form={r.get('form_id')} skel={r.get('skeleton_pattern')} :: {p}")
