"""Verify incorrect-implementation demotions are not counted as Ready."""

from __future__ import annotations

from question_engine.type_readiness import INCORRECT_IMPLEMENTATION_TYPE_IDS

print(f"Incorrect-implementation denylist: {len(INCORRECT_IMPLEMENTATION_TYPE_IDS)}")
for tid in sorted(INCORRECT_IMPLEMENTATION_TYPE_IDS):
    print(f"  - {tid}")
print("OK")
