"""Verify curriculum type_id links against the question type registry."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.base import QUESTION_TYPES
from question_engine.catalog import TYPE_CATALOG
import question_engine.types  # noqa: F401

HAND_WRITTEN = {
    "quadratic_factoring",
    "polynomial_long_division",
    "radical_simplification",
    "rational_simplification",
    "rational_expression_simplification",
}


def has_real_generator(type_id: str) -> bool:
    if type_id in HAND_WRITTEN:
        return True
    entry = next((e for e in TYPE_CATALOG if e.id == type_id), None)
    return entry is not None and entry.generator != "scaffold"


def parse_curriculum_type_ids(src: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    topic_re = re.compile(
        r'id:\s*"([^"]+)"[^}]*?type_id:\s*"([^"]+)"',
        re.DOTALL,
    )
    for match in topic_re.finditer(src):
        pairs.append((match.group(1), match.group(2)))
    return pairs


def main() -> None:
    src = (ROOT / "lib" / "curriculum.ts").read_text(encoding="utf-8")
    linked = parse_curriculum_type_ids(src)
    real_types = {tid for tid in QUESTION_TYPES if has_real_generator(tid)}

    invalid = [(topic_id, type_id) for topic_id, type_id in linked if type_id not in QUESTION_TYPES]
    scaffold_linked = [
        (topic_id, type_id) for topic_id, type_id in linked if not has_real_generator(type_id)
    ]
    covered = {type_id for _, type_id in linked}
    missing = sorted(real_types - covered)

    print(f"Curriculum topics with type_id: {len(linked)}")
    print(f"Unique type_ids linked: {len(covered)}")
    print(f"Real generator types: {len(real_types)}")
    print(f"Scaffold-only types in registry: {len(QUESTION_TYPES) - len(real_types)}")

    ok = True
    if invalid:
        ok = False
        print("\nINVALID type_id (not in QUESTION_TYPES):")
        for row in invalid:
            print(f"  {row}")

    if scaffold_linked:
        ok = False
        print("\nLinked to scaffold-only types:")
        for row in scaffold_linked:
            print(f"  {row}")

    if missing:
        ok = False
        print("\nReal generator types missing from curriculum:")
        for type_id in missing:
            print(f"  {type_id}")

    if ok:
        print("\nAll checks passed.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
