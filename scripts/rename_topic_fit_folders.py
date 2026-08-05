"""Rename topic_fit by_topic + calc one-topic folders to course-prefixed names.

Dry-run by default; pass --apply to rename. Then rebuild INDEX via
build_verified_topic_galleries.py --index-only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "topic_fit_naming", ROOT / "scripts" / "topic_fit_naming.py"
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)
gallery_folder_name = _mod.gallery_folder_name
has_course_prefix = _mod.has_course_prefix

TOPIC_FIT = ROOT / "scripts" / "output" / "topic_fit"
BY_TOPIC = TOPIC_FIT / "by_topic"

# Old calc one-topic / aggregate roots → new prefixed names.
CALC_ROOT_RENAMES: dict[str, str] = {
    "calc_deriv_calc_diff_average_rates_of_change": "c1_calc_diff_average_rates_of_change",
    "calc_deriv_calc_diff_chain_rule": "c1_calc_diff_chain_rule",
    "calc_deriv_calc_diff_definition_of_the_derivative": "c1_calc_diff_definition_of_the_derivative",
    "calc_deriv_calc_diff_higher_order_derivatives": "c1_calc_diff_higher_order_derivatives",
    "calc_deriv_calc_diff_implicit": "c1_calc_diff_implicit",
    "calc_deriv_calc_diff_instantaneous_rates_of_change": "c1_calc_diff_instantaneous_rates_of_change",
    "calc_deriv_calc_diff_inverse_functions": "c1_calc_diff_inverse_functions",
    "calc_deriv_calc_diff_inverse_trigonometric": "c1_calc_diff_inverse_trigonometric",
    "calc_deriv_calc_diff_logarithmic": "c1_calc_diff_logarithmic",
    "calc_deriv_calc_diff_natural_logarithms_and_exponentials": (
        "c1_calc_diff_natural_logarithms_and_exponentials"
    ),
    "calc_deriv_calc_diff_other_base_logarithms_and_exponentials": (
        "c1_calc_diff_other_base_logarithms_and_exponentials"
    ),
    "calc_deriv_calc_diff_power_rule": "c1_calc_diff_power_rule",
    "calc_deriv_calc_diff_product_rule": "c1_calc_diff_product_rule",
    "calc_deriv_calc_diff_quotient_rule": "c1_calc_diff_quotient_rule",
    "calc_deriv_calc_diff_trigonometric": "c1_calc_diff_trigonometric",
    "calculus_pilot_tf": "c1_calc_app_diff_differentials",
    "calculus_pilot_tf_tangent": "c1_calc_app_diff_slope_tangent_and_normal_lines",
    "calculus_pilot_tf_int": (
        "c1_calc_indef_int_logarithmic_rule_and_exponentials_with_substitution"
    ),
    "calculus_derivative_rules": "c1_calculus_derivative_rules",
    "calculus_pilot": "c1_calculus_pilot",
}


def _rename(src: Path, dest: Path, *, apply: bool) -> str:
    if not src.exists():
        return f"MISSING {src.relative_to(ROOT)}"
    if dest.exists():
        return f"SKIP exists {dest.relative_to(ROOT)}"
    if apply:
        src.rename(dest)
        return f"OK {src.name} -> {dest.name}"
    return f"DRY {src.name} -> {dest.name}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="Perform renames")
    args = ap.parse_args()

    mapping: list[tuple[str, str]] = []
    results: list[str] = []

    if BY_TOPIC.is_dir():
        for p in sorted(BY_TOPIC.iterdir()):
            if not p.is_dir():
                continue
            tid = p.name
            new = gallery_folder_name(tid)
            if new == tid:
                continue
            dest = BY_TOPIC / new
            mapping.append((f"by_topic/{tid}", f"by_topic/{new}"))
            results.append(_rename(p, dest, apply=args.apply))

    for old, new in CALC_ROOT_RENAMES.items():
        src = TOPIC_FIT / old
        if not src.exists():
            continue
        dest = TOPIC_FIT / new
        mapping.append((old, new))
        results.append(_rename(src, dest, apply=args.apply))

    out_map = TOPIC_FIT / "_folder_rename_map.json"
    payload = {
        "applied": args.apply,
        "mapping": [{"from": a, "to": b} for a, b in mapping],
        "results": results,
    }
    out_map.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    for line in results:
        print(line)
    print(f"map={out_map.relative_to(ROOT)} count={len(mapping)} apply={args.apply}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
