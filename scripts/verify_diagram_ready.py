"""Verify diagram-dependent curriculum leaves are not counted as Ready.

Also keeps the Python denylist and `lib/diagram-readiness.ts` in sync, and
simulates curriculum-picker Ready status.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.diagram_readiness import REQUIRES_DIAGRAM_TYPE_IDS, type_requires_diagram

CURR = (ROOT / "lib" / "curriculum.ts").read_text(encoding="utf-8")
TS_MIRROR = (ROOT / "lib" / "diagram-readiness.ts").read_text(encoding="utf-8")
TYPE_IDS = sorted(set(re.findall(r'type_id:\s*"([^"]+)"', CURR)))
TS_IDS = set(re.findall(r'^\s*"([^"]+)",?\s*$', TS_MIRROR, flags=re.M))

# Drop non-id string literals from the TS file (comments / docs don't match this).
# The Set constructor only has type-id string entries on their own lines.
ts_only = TS_IDS - REQUIRES_DIAGRAM_TYPE_IDS
py_only = REQUIRES_DIAGRAM_TYPE_IDS - TS_IDS

demoted_linked = [tid for tid in TYPE_IDS if type_requires_diagram(tid)]
still_ready_suspects = [
    tid
    for tid in TYPE_IDS
    if any(
        tok in tid
        for tok in (
            "diagram",
            "dot_plot",
            "histogram",
            "box_plot",
            "scatter",
            "visualizing",
            "right_triangle_trig",
            "area_of_triangles",
            "similar_triangles",
            "similar_figures",
            "special_right",
            "circumference",
            "classifying_angles",
            "finding_trig",
            "finding_angles",
            "finding_sine",
            "solving_right_triangles",
        )
    )
    and not type_requires_diagram(tid)
]

print(f"Curriculum type_ids: {len(TYPE_IDS)}")
print(f"Demoted (requires_diagram) and curriculum-linked: {len(demoted_linked)}")
for tid in demoted_linked:
    print(f"  - {tid}")

print(f"\nFlag set size: {len(REQUIRES_DIAGRAM_TYPE_IDS)}")
print(f"TS mirror size: {len(TS_IDS)}")
print(f"Suspect names still Ready (review): {len(still_ready_suspects)}")
for tid in still_ready_suspects:
    print(f"  ? {tid}")

if py_only:
    print(f"\nERROR: in Python denylist but missing from TS mirror ({len(py_only)}):")
    for tid in sorted(py_only):
        print(f"  - {tid}")
if ts_only:
    print(f"\nERROR: in TS mirror but missing from Python denylist ({len(ts_only)}):")
    for tid in sorted(ts_only):
        print(f"  - {tid}")

# Simulate picker: demoted linked types must not be Ready.
import question_engine.types  # noqa: F401
from question_engine.core.base import list_question_types

api_types = list_question_types()
available = {
    t["id"]
    for t in api_types
    if not type_requires_diagram(t["id"]) and not t.get("requires_diagram")
}
# Frontend also blocks denylist ids even without API flag.
diagram_blocked = {t["id"] for t in api_types if type_requires_diagram(t["id"]) or t.get("requires_diagram")}
diagram_blocked |= set(REQUIRES_DIAGRAM_TYPE_IDS)

leaked_ready = [tid for tid in demoted_linked if tid in available and tid not in diagram_blocked]
assert not leaked_ready, f"Demoted types still in available set: {leaked_ready}"

# Coming-soon simulation for demoted linked ids
for tid in demoted_linked:
    assert tid in diagram_blocked or tid not in available
    status = "coming_soon" if tid in diagram_blocked else ("ready" if tid in available else "preview")
    assert status == "coming_soon", f"{tid} would be {status}, expected coming_soon"

# Graphing should NOT be flagged
graph_keep = [
    tid
    for tid in TYPE_IDS
    if "graphing_linear" in tid or tid in ("writing_linear_equations", "more_on_slope", "pa_plotting_points")
]
bad_graph = [tid for tid in graph_keep if type_requires_diagram(tid)]
print(f"\nGraphing/plot keepers flagged by mistake: {bad_graph or 'none'}")
assert not bad_graph
assert "g6_interpreting_dot_plots" in demoted_linked
assert "finding_angles" in demoted_linked
assert "pa_similar_figures" in demoted_linked
assert "graphing_linear_equations" not in REQUIRES_DIAGRAM_TYPE_IDS
assert not py_only and not ts_only, "Python/TS denylist drift"
assert not still_ready_suspects, f"Suspect Ready leftovers: {still_ready_suspects}"
print("\nOK")
