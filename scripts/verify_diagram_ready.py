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
# Only compare the REQUIRES_DIAGRAM set (not INCORRECT_IMPLEMENTATION or other quoted ids).
ts_block = re.search(
    r"REQUIRES_DIAGRAM_TYPE_IDS[^=]*=\s*new Set\(\[([\s\S]*?)\]\)",
    TS_MIRROR,
)
TS_IDS = set(re.findall(r'"([^"]+)"', ts_block.group(1) if ts_block else ""))

ts_only = TS_IDS - REQUIRES_DIAGRAM_TYPE_IDS
py_only = REQUIRES_DIAGRAM_TYPE_IDS - TS_IDS

demoted_linked = [tid for tid in TYPE_IDS if type_requires_diagram(tid)]

print(f"Curriculum type_ids: {len(TYPE_IDS)}")
print(f"Demoted (requires_diagram) and curriculum-linked: {len(demoted_linked)}")
for tid in demoted_linked:
    print(f"  - {tid}")

print(f"\nFlag set size: {len(REQUIRES_DIAGRAM_TYPE_IDS)}")
print(f"TS mirror size: {len(TS_IDS)}")

if py_only:
    print(f"\nERROR: in Python denylist but missing from TS mirror ({len(py_only)}):")
    for tid in sorted(py_only):
        print(f"  - {tid}")
if ts_only:
    print(f"\nERROR: in TS mirror but missing from Python denylist ({len(ts_only)}):")
    for tid in sorted(ts_only):
        print(f"  - {tid}")

import question_engine.types  # noqa: F401
from question_engine.core.base import list_question_types

api_types = list_question_types()
available = {
    t["id"]
    for t in api_types
    if not type_requires_diagram(t["id"]) and not t.get("requires_diagram")
}
diagram_blocked = {
    t["id"] for t in api_types if type_requires_diagram(t["id"]) or t.get("requires_diagram")
}
diagram_blocked |= set(REQUIRES_DIAGRAM_TYPE_IDS)

leaked_ready = [tid for tid in demoted_linked if tid in available and tid not in diagram_blocked]
assert not leaked_ready, f"Demoted types still in available set: {leaked_ready}"

for tid in demoted_linked:
    assert tid in diagram_blocked or tid not in available
    status = "coming_soon" if tid in diagram_blocked else ("ready" if tid in available else "preview")
    assert status == "coming_soon", f"{tid} would be {status}, expected coming_soon"

# Keepers that must remain Ready (diagram-capable or graph-based).
for tid in (
    "geo_basics_angles_and_their_measures",
    "geo_right_pythagorean_theorem",
    "g6_interpreting_dot_plots",
    "g6_equations_tape_diagrams",
    "g6_drawing_dot_plots",
    "g6_isometric_sketching",
    "finding_sine_cosine_tangent",
    "graphing_linear_equations",
):
    if tid in TYPE_IDS:
        assert not type_requires_diagram(tid), f"{tid} should not be demoted"

assert "g6_equations_tape_diagrams" not in REQUIRES_DIAGRAM_TYPE_IDS
assert "graphing_linear_equations" not in REQUIRES_DIAGRAM_TYPE_IDS
assert not py_only and not ts_only, "Python/TS denylist drift"
print("\nOK")
