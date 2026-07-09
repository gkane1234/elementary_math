"""List remaining scaffold catalog entries."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.catalogs.algebra_1 import CATALOG as A1
from question_engine.catalogs.algebra_2 import CATALOG as A2
from question_engine.catalogs.calculus import CATALOG as CALC
from question_engine.catalogs.geometry import CATALOG as GEO
from question_engine.catalogs.grade_6 import CATALOG as G6
from question_engine.catalogs.pre_algebra import CATALOG as PA
from question_engine.catalogs.precalculus import CATALOG as PC

CATALOG = A1 + G6 + PA + A2 + GEO + PC + CALC
scaffold = [e for e in CATALOG if e.generator == "scaffold"]
wired = [e for e in CATALOG if e.generator != "scaffold"]
print(f"wired={len(wired)} scaffold={len(scaffold)} total={len(CATALOG)}")
for e in sorted(scaffold, key=lambda x: (x.category, x.id)):
    print(f"{e.id}|{e.name}|{e.category}")
