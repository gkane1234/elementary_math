"""Inventory A2 SECTIONS coverage and notes Limitations gaps."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from question_engine.catalogs.algebra_2 import CATALOG as A2_CATALOG  # noqa: E402

OUT = Path(__file__).resolve().parent
GALLERY = OUT.parent


def _load_sections() -> list[dict]:
    ge_path = GALLERY / "gen_examples.py"
    spec = importlib.util.spec_from_file_location("phase01_gen_examples", ge_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {ge_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return list(mod.SECTIONS)


sections = _load_sections()
ids: set[str] = set()
for sec in sections:
    tid = str(sec.get("type_id") or "")
    if tid:
        ids.add(tid)
    for a in sec.get("aliases") or []:
        ids.add(str(a))

a2 = [t.id for t in A2_CATALOG]
missing = [t for t in a2 if t not in ids]
covered = [t for t in a2 if t in ids]
print(f"A2 catalog: {len(a2)}")
print(f"In SECTIONS (type_id or alias): {len(covered)}")
print(f"Missing from SECTIONS: {len(missing)}")
for t in missing:
    print(f"  {t}")

notes_dir = OUT
no_notes: list[str] = []
no_lim: list[tuple[str, str]] = []
has_unclear: list[str] = []
has_lim: list[str] = []

# Map type_id -> notes file via stem match or backtick mention in first 40 lines
note_files = list(notes_dir.glob("*.md"))


def find_notes(tid: str) -> Path | None:
    direct = notes_dir / f"{tid}.md"
    if direct.exists():
        return direct
    for p in note_files:
        if p.stem.startswith("_") or p.stem.endswith("_INDEX"):
            continue
        head = "\n".join(p.read_text(encoding="utf-8", errors="ignore").splitlines()[:40])
        if f"`{tid}`" in head or tid in head[:200]:
            return p
    return None


for t in a2:
    found = find_notes(t)
    if not found:
        no_notes.append(t)
        continue
    txt = found.read_text(encoding="utf-8", errors="ignore")
    if re.search(r"^#+\s*Limitations\b", txt, re.M):
        has_lim.append(t)
    else:
        no_lim.append((t, found.name))
    if re.search(r"\bUNCLEAR\b", txt):
        has_unclear.append(t)

print(f"\nNo notes found: {len(no_notes)}")
for t in no_notes:
    print(f"  {t}")
print(f"\nNotes WITH ## Limitations: {len(has_lim)}")
print(f"Notes WITHOUT ## Limitations: {len(no_lim)}")
print(f"Notes with UNCLEAR: {len(has_unclear)}")

# Graphing-ish leaves
graphish = [t for t in a2 if "graph" in t]
print(f"\nGraphing-ish ({len(graphish)}):")
for t in graphish:
    status = []
    if t in missing:
        status.append("NO_SECTION")
    if t in no_notes:
        status.append("NO_NOTES")
    elif t in [x[0] for x in no_lim]:
        status.append("NO_LIM")
    if t in has_unclear:
        status.append("UNCLEAR")
    print(f"  {t}: {', '.join(status) or 'ok'}")
