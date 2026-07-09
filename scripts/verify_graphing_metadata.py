"""Verify graphing types emit graph_spec or number_line_spec."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.api.handler import handle_generate

SAMPLES = [
    "graphing_linear_equations",
    "graphing_single_variable_inequalities",
    "slope",
    "pa_plotting_points",
    "g6_numbers_on_a_number_line",
    "systems_graphing",
    "graphing_quadratic_functions",
    "a2_linear_relations_and_functions_graphing_linear_equations",
    "geo_parallel_graphing_linear_equations",
    "g6_writing_and_graphing_inequalities",
]

settings = {"count": 1, "include_graph_metadata": True}
ok = 0
for tid in SAMPLES:
    status, _, body = handle_generate({"type_id": tid, "settings": settings})
    data = json.loads(body)
    if status != 200:
        print(f"{tid}: FAIL {data.get('error')}")
        continue
    meta = data["questions"][0].get("metadata", {})
    if meta.get("number_line_spec"):
        print(f"{tid}: number_line_spec boundary={meta['number_line_spec'].get('boundary')}")
        ok += 1
    elif meta.get("graph_spec"):
        gs = meta["graph_spec"]
        print(f"{tid}: graph_spec functions={len(gs.get('functions', []))} points={len(gs.get('points', []))}")
        ok += 1
    else:
        print(f"{tid}: NO_META scaffold={meta.get('scaffolded')}")

print(f"\n{ok}/{len(SAMPLES)} with graph metadata")
