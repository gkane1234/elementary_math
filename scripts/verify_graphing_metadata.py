"""Verify graphing types emit prompt vs answer graph metadata."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.api.handler import handle_generate

BLANK_SAMPLES = [
    "graphing_linear_equations",
    "graphing_linear_inequalities",
    "systems_graphing",
    "graphing_quadratic_functions",
    "graphing_absolute_value_equations",
    "graphing_exponential_functions",
    "a2_linear_relations_and_functions_graphing_absolute_value_equations",
    "a2_linear_relations_and_functions_graphing_linear_equations",
    "geo_parallel_graphing_linear_equations",
]

STIMULUS_SAMPLES = [
    "more_on_slope",
    "writing_linear_equations",
    "continuous_relations",
]

settings = {"count": 1, "include_graph_metadata": True, "include_answer_key": True}
ok = 0
total = 0

for tid in BLANK_SAMPLES:
    total += 1
    status, _, body = handle_generate({"type_id": tid, "settings": settings})
    data = json.loads(body)
    if status != 200:
        print(f"{tid}: FAIL {data.get('error')}")
        continue
    meta = data["questions"][0].get("metadata", {})
    gs = meta.get("graph_spec") or {}
    nls = meta.get("number_line_spec") or {}
    role = meta.get("graph_role")
    prompt_empty = (
        (gs and len(gs.get("functions", [])) == 0 and len(gs.get("points", [])) == 0)
        or nls.get("blank") is True
    )
    has_answer = bool(meta.get("answer_graph_spec") or meta.get("answer_number_line_spec"))
    if role == "blank" and prompt_empty and has_answer:
        print(f"{tid}: OK blank prompt + answer graph")
        ok += 1
    else:
        print(
            f"{tid}: BAD role={role} prompt_empty={prompt_empty} "
            f"answer={has_answer} fn={len(gs.get('functions', []))} pts={len(gs.get('points', []))}"
        )

for tid in STIMULUS_SAMPLES:
    total += 1
    status, _, body = handle_generate({"type_id": tid, "settings": settings})
    data = json.loads(body)
    if status != 200:
        print(f"{tid}: FAIL {data.get('error')}")
        continue
    meta = data["questions"][0].get("metadata", {})
    gs = meta.get("graph_spec") or {}
    role = meta.get("graph_role")
    has_line = len(gs.get("functions", [])) > 0 or len(gs.get("points", [])) > 0
    if role == "stimulus" and has_line:
        print(f"{tid}: OK stimulus line on prompt answer={data['questions'][0].get('answer_latex')}")
        ok += 1
    else:
        print(f"{tid}: BAD role={role} has_line={has_line} gs={gs}")

print(f"\n{ok}/{total} checks passed")
sys.exit(0 if ok == total else 1)
