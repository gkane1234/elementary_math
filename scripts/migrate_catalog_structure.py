"""One-time migration helper: build catalogs/ package and generator type stubs."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
QE = ROOT / "question_engine"

COURSE_PREFIXES = {
    "Grade 6": ("grade_6", "grade_6"),
    "Pre-Algebra": ("pre_algebra", "pre_algebra"),
    "Algebra 1": ("algebra_1", "algebra_1"),
    "Geometry": ("geometry", "geometry"),
    "Algebra 2": ("algebra_2", "algebra_2"),
    "Precalculus": ("precalculus", "precalculus"),
    "Calculus": ("calculus", "calculus"),
}


def chapter_to_snake(chapter: str) -> str:
    slug = chapter.lower()
    slug = slug.replace(" and ", "_and_")
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug


def category_to_paths(category: str) -> tuple[str, str]:
    course_label, chapter = category.split(" — ", 1)
    course_id, _ = COURSE_PREFIXES[course_label]
    return course_id, chapter_to_snake(chapter)


def category_order_from_legacy_file(path: Path, helper_prefix: str, course_label: str) -> tuple[str, ...]:
    text = path.read_text(encoding="utf-8")
    chapters: list[str] = []
    for match in re.finditer(rf'{helper_prefix}\(\s*"([^"]+)"', text):
        chapter = match.group(1)
        category = f"{course_label} — {chapter}"
        if category not in chapters:
            chapters.append(category)
    return tuple(chapters)


def algebra1_category_order() -> tuple[str, ...]:
    path = QE / "catalogs" / "algebra_1.py"
    if not path.exists():
        return tuple()
    text = path.read_text(encoding="utf-8")
    block = text.split("CATEGORY_ORDER", 1)[1].split("CATALOG", 1)[0]
    return tuple(re.findall(r'"([^"]+ — [^"]+)"', block))


def split_category_order() -> dict[str, tuple[str, ...]]:
    return {
        "Grade 6": category_order_from_legacy_file(QE / "grade6_catalog.py", "_g6", "Grade 6"),
        "Pre-Algebra": category_order_from_legacy_file(QE / "prealgebra_catalog.py", "_pa", "Pre-Algebra"),
        "Algebra 1": algebra1_category_order(),
        "Geometry": category_order_from_legacy_file(QE / "geometry_catalog.py", "_geo", "Geometry"),
        "Algebra 2": category_order_from_legacy_file(QE / "algebra2_catalog.py", "_a2", "Algebra 2"),
        "Precalculus": category_order_from_legacy_file(QE / "precalc_catalog.py", "_pc", "Precalculus"),
        "Calculus": category_order_from_legacy_file(QE / "calculus_catalog.py", "_calc", "Calculus"),
    }


def build_catalogs_package() -> None:
    catalogs_dir = QE / "catalogs"
    catalogs_dir.mkdir(exist_ok=True)

    # Ensure algebra_1 exists before category order extraction.
    import subprocess

    subprocess.run([sys.executable, str(ROOT / "scripts" / "rebuild_algebra1_catalog.py")], check=True)

    (catalogs_dir / "__init__.py").write_text(
        '"""Per-course question type catalogs (data only)."""\n',
        encoding="utf-8",
    )

    base_py = '''from dataclasses import dataclass


@dataclass(frozen=True)
class TypeCatalogEntry:
    id: str
    name: str
    category: str
    subcategory: str | None = None
    description: str = ""
    instruction_latex: str = ""
    instruction_text: str = ""
    generator: str = "scaffold"
    count_default: int = 10


def entry(
    id: str,
    name: str,
    category: str,
    *,
    subcategory: str | None = None,
    generator: str = "scaffold",
    description: str = "",
    instruction_latex: str = "",
    instruction_text: str = "",
    count_default: int = 10,
) -> TypeCatalogEntry:
    return TypeCatalogEntry(
        id=id,
        name=name,
        category=category,
        subcategory=subcategory,
        generator=generator,
        description=description or f"Practice {name.lower()}.",
        instruction_latex=instruction_latex or "\\\\text{Solve.}",
        instruction_text=instruction_text or "Solve.",
        count_default=count_default,
    )
'''
    (catalogs_dir / "base.py").write_text(base_py, encoding="utf-8")

    category_orders = split_category_order()

    moves = [
        ("grade6_catalog.py", "grade_6.py", "Grade 6", "GRADE6_CATALOG", "_g6"),
        ("prealgebra_catalog.py", "pre_algebra.py", "Pre-Algebra", "PREALGEBRA_CATALOG", "_pa"),
        ("geometry_catalog.py", "geometry.py", "Geometry", "GEOMETRY_CATALOG", "_geo"),
        ("algebra2_catalog.py", "algebra_2.py", "Algebra 2", "ALGEBRA2_CATALOG", "_a2"),
        ("precalc_catalog.py", "precalculus.py", "Precalculus", "PRECALC_CATALOG", "_pc"),
        ("calculus_catalog.py", "calculus.py", "Calculus", "CALCULUS_CATALOG", "_calc"),
    ]

    for src_name, dst_name, course_label, catalog_var, _ in moves:
        src = QE / src_name
        text = src.read_text(encoding="utf-8")
        text = text.replace("from .catalog import TypeCatalogEntry", "from .base import TypeCatalogEntry")
        text = text.replace(f"{catalog_var}: tuple", "CATALOG: tuple")
        course_id, _ = COURSE_PREFIXES[course_label]
        order = category_orders.get(course_label, ())
        order_lines = ",\n    ".join(repr(c) for c in order)
        header = (
            f'from .base import TypeCatalogEntry\n\n'
            f'COURSE_ID = "{course_id}"\n\n'
            f"CATEGORY_ORDER: tuple[str, ...] = (\n    {order_lines},\n)\n\n"
        )
        # Drop legacy import line if present
        text = re.sub(r"^from \.catalog import TypeCatalogEntry\s*\n", "", text, count=1)
        if "from .base import TypeCatalogEntry" not in text.split("CATALOG", 1)[0]:
            text = header + text.split("\n", 1)[1] if text.startswith("from ") or text.startswith("def ") else header + text
        else:
            # Replace existing header through helper def
            text = re.sub(r"^.*?^def ", header + "def ", text, count=1, flags=re.MULTILINE | re.DOTALL)
        (catalogs_dir / dst_name).write_text(text, encoding="utf-8")


def build_generator_stubs() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "question_engine.registry",
        QE / "registry.py",
        submodule_search_locations=[str(QE)],
    )
    assert spec and spec.loader
    registry = importlib.util.module_from_spec(spec)
    # Minimal package stubs to avoid loading question_engine/__init__.py
    import sys
    import types as types_mod

    pkg = types_mod.ModuleType("question_engine")
    pkg.__path__ = [str(QE)]  # type: ignore[attr-defined]
    sys.modules["question_engine"] = pkg
    sys.modules["question_engine.registry"] = registry
    spec.loader.exec_module(registry)
    TYPE_CATALOG = registry.TYPE_CATALOG

    types_dir = QE / "types"
    stub_template = '''"""Catalog generator type: {type_id}."""

from question_engine.types._from_generator import register_from_catalog

register_from_catalog("{type_id}")
'''
    created = 0
    for entry in TYPE_CATALOG:
        if entry.generator == "scaffold":
            continue
        course, chapter = category_to_paths(entry.category)
        dest_dir = types_dir / course / chapter
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{entry.id}.py"
        dest.write_text(stub_template.format(type_id=entry.id), encoding="utf-8")
        created += 1
    print(f"Created {created} generator stub modules")


if __name__ == "__main__":
    build_catalogs_package()
    build_generator_stubs()
    print("Migration files generated.")
