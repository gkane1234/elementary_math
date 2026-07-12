"""Audit scaffold / demoted catalog entries for implementation planning."""
from __future__ import annotations

from collections import defaultdict

from question_engine.catalog import CATALOG
from question_engine.diagram_readiness import REQUIRES_DIAGRAM_TYPE_IDS
from question_engine.type_readiness import (
    INCORRECT_IMPLEMENTATION_TYPE_IDS,
    type_not_ready,
)

wired = [e for e in CATALOG if e.generator != "scaffold"]
scaffold = [e for e in CATALOG if e.generator == "scaffold"]
ready = [e for e in wired if not type_not_ready(e.id)]
demoted_wired = [e for e in wired if type_not_ready(e.id)]

print(f"Total: {len(CATALOG)}")
print(f"Wired: {len(wired)}")
print(f"Scaffold: {len(scaffold)}")
print(f"INCORRECT: {len(INCORRECT_IMPLEMENTATION_TYPE_IDS)}")
print(f"REQUIRES_DIAGRAM: {len(REQUIRES_DIAGRAM_TYPE_IDS)}")
print(f"Ready (wired, not demoted): {len(ready)}")
print(f"Demoted wired: {len(demoted_wired)}")

by_cat: dict[str, list] = defaultdict(list)
for e in scaffold:
    by_cat[e.category].append(e)

print("\n=== SCAFFOLD BY CATEGORY ===")
for cat, items in sorted(by_cat.items(), key=lambda x: -len(x[1])):
    print(f"\n## {cat}: {len(items)}")
    for e in items:
        sub = e.subcategory or ""
        print(f"  {e.id} | {e.name} | {sub}")

print("\n=== DEMOTED WIRED ===")
for e in demoted_wired:
    reasons = []
    if e.id in REQUIRES_DIAGRAM_TYPE_IDS:
        reasons.append("diagram")
    if e.id in INCORRECT_IMPLEMENTATION_TYPE_IDS:
        reasons.append("incorrect")
    print(f"  {e.id}: gen={e.generator} [{','.join(reasons)}]")

print("\n=== REQUIRES_DIAGRAM FULL ===")
for tid in sorted(REQUIRES_DIAGRAM_TYPE_IDS):
    e = next((x for e in CATALOG if x.id == tid for x in [e]), None)
    # simpler:
    e = next((x for x in CATALOG if x.id == tid), None)
    gen = e.generator if e else "?"
    scaf = "SCAFFOLD" if gen == "scaffold" else "wired"
    print(f"  {tid}: {gen} ({scaf})")
