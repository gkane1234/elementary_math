"""Regenerate all calc_* gallery sections."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_ROOT))

from question_engine.catalogs.calculus import CATALOG

ids = [e.id for e in CATALOG]
# batch --only in chunks to avoid huge argv
gen = _ROOT / "scripts/output/skeleton_phase01_gallery/gen_examples.py"
chunk = 20
for i in range(0, len(ids), chunk):
    batch = ids[i : i + chunk]
    only = ",".join(batch)
    print(f"=== batch {i // chunk + 1}: {len(batch)} types ===", flush=True)
    r = subprocess.run(
        [sys.executable, str(gen), "--only", only],
        cwd=str(_ROOT),
    )
    if r.returncode != 0:
        raise SystemExit(r.returncode)
print("done", len(ids), "calc types")
