"""Verify incorrect-implementation demotions are not counted as Ready."""

from __future__ import annotations

import re
from pathlib import Path

from question_engine.type_readiness import (
    INCORRECT_IMPLEMENTATION_TYPE_IDS,
    type_incorrect_implementation,
    type_not_ready,
)

CURR = Path("lib/curriculum.ts").read_text(encoding="utf-8")
TYPE_IDS = sorted(set(re.findall(r'type_id:\s*"([^"]+)"', CURR)))

assert "g6_writing_numeric_expressions" in INCORRECT_IMPLEMENTATION_TYPE_IDS
assert type_incorrect_implementation("g6_writing_numeric_expressions")
assert type_not_ready("g6_writing_numeric_expressions")
assert "g6_writing_numeric_expressions" in TYPE_IDS

# Neighbor Ready types in the same chapter must not be swept in.
for keep in (
    "g6_numeric_expressions_with_exponents",
    "g6_numeric_expressions_and_order_of_operations",
):
    assert keep in TYPE_IDS
    assert not type_incorrect_implementation(keep)
    # order-of-ops may still be Ready; exponents likewise (unless diagram-flagged).
    assert not type_not_ready(keep) or keep in INCORRECT_IMPLEMENTATION_TYPE_IDS

print(f"Incorrect-implementation denylist: {len(INCORRECT_IMPLEMENTATION_TYPE_IDS)}")
for tid in sorted(INCORRECT_IMPLEMENTATION_TYPE_IDS):
    linked = tid in TYPE_IDS
    print(f"  - {tid} (curriculum-linked={linked})")
print("OK")
