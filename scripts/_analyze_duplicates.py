"""Analyze duplicate question type names across catalogs."""
from __future__ import annotations

import ast
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@dataclass(frozen=True)
class Entry:
    source: str
    id: str
    name: str
    category: str
    generator: str


def _parse_catalog(path: Path, tuple_name: str) -> list[Entry]:
    src = path.read_text(encoding="utf-8")
    # Extract name= and id= from _entry/_pa/_geo etc calls inside the tuple
    entries: list[Entry] = []
    # Match helper calls: _pa("Chapter", "id", "Name", ...)
    pattern = re.compile(
        r'_\w+\(\s*"[^"]*"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"',
    )
    pattern2 = re.compile(
        r'_entry\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"',
    )
    cat_pattern = re.compile(r'category=f?"([^"]+)"|"([^"]+)"\s*,\s*#.*category')
    gen_pattern = re.compile(r'generator="([^"]+)"')

    for block in src.split("\n"):
        m = pattern.search(block) or pattern2.search(block)
        if not m:
            continue
        if pattern2.search(block):
            eid, name, category = m.group(1), m.group(2), m.group(3)
        else:
            eid, name = m.group(1), m.group(2)
            cat_m = re.search(r'_\w+\(\s*"([^"]+)"', block)
            category = cat_m.group(1) if cat_m else "?"
        gen_m = gen_pattern.search(block)
        generator = gen_m.group(1) if gen_m else "scaffold"
        entries.append(Entry(path.name, eid, name, category, generator))
    return entries


def _parse_algebra_catalog() -> list[Entry]:
    src = (ROOT / "question_engine/catalog.py").read_text(encoding="utf-8")
    section = src.split("_ALGEBRA_CATALOG")[1].split("from .algebra2")[0]
    entries: list[Entry] = []
    gen_pattern = re.compile(r'generator="([^"]+)"')
    for block in section.split("_entry(")[1:]:
        id_m = re.search(r'"([^"]+)"', block)
        name_m = re.search(r',\s*"([^"]+)"', block[id_m.end() :] if id_m else block)
        cat_m = re.search(r',\s*"([^"]+)"', block[(id_m.end() + name_m.end()) if id_m and name_m else 0 :])
        if not (id_m and name_m and cat_m):
            continue
        eid = id_m.group(1)
        name = name_m.group(1)
        category = cat_m.group(1)
        gen_m = gen_pattern.search(block)
        generator = gen_m.group(1) if gen_m else "scaffold"
        entries.append(Entry("catalog.py (_ALGEBRA)", eid, name, category, generator))
    return entries


def main() -> None:
    catalogs = [
        ("grade6_catalog.py", "GRADE6_CATALOG"),
        ("prealgebra_catalog.py", "PREALGEBRA_CATALOG"),
        ("algebra2_catalog.py", "A2_CATALOG"),
        ("geometry_catalog.py", "GEOMETRY_CATALOG"),
        ("precalc_catalog.py", "PRECALC_CATALOG"),
        ("calculus_catalog.py", "CALC_CATALOG"),
    ]
    all_entries = _parse_algebra_catalog()
    for fname, _ in catalogs:
        all_entries.extend(_parse_catalog(ROOT / "question_engine" / fname, _))

    by_name: dict[str, list[Entry]] = defaultdict(list)
    for e in all_entries:
        by_name[e.name.lower().strip()].append(e)

    dupes = {k: v for k, v in by_name.items() if len(v) > 1}
    print(f"Total entries: {len(all_entries)}")
    print(f"Duplicate names: {len(dupes)}")
    for name, entries in sorted(dupes.items(), key=lambda x: (-len(x[1]), x[0])):
        print(f"\n=== {name!r} ({len(entries)}) ===")
        for e in entries:
            print(f"  [{e.source}] {e.id} | {e.category} | gen={e.generator}")


if __name__ == "__main__":
    main()
