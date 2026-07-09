"""Reorganize question_engine/ into logical subpackages."""

from __future__ import annotations

import re
import shutil
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QE = ROOT / "question_engine"

# (source relative to QE, destination relative to QE)
MOVES: list[tuple[str, str]] = [
    ("base.py", "core/base.py"),
    ("models.py", "core/models.py"),
    ("registry.py", "core/registry.py"),
    ("scaffold.py", "core/scaffold.py"),
    ("api_handler.py", "api/handler.py"),
    ("dev_server.py", "api/dev_server.py"),
    ("common_settings.py", "settings/common_settings.py"),
    ("factoring_settings.py", "settings/factoring_settings.py"),
    ("latex_helpers.py", "utils/latex_helpers.py"),
    ("layout.py", "utils/layout.py"),
]

HAND_WRITTEN_TYPE_MOVES: list[tuple[str, str]] = [
    ("types/quadratic_factoring.py", "types/algebra_1/polynomials/quadratic_factoring.py"),
    ("types/polynomial_long_division.py", "types/algebra_1/polynomials/polynomial_long_division.py"),
    ("types/radical_simplification.py", "types/algebra_1/radical_expressions/radical_simplification.py"),
    ("types/rational_simplification.py", "types/algebra_1/rational_expressions/rational_simplification.py"),
    (
        "types/rational_expression_simplification.py",
        "types/algebra_1/rational_expressions/rational_expression_simplification.py",
    ),
]

LEGACY_CATALOG_FILES = [
    "grade6_catalog.py",
    "prealgebra_catalog.py",
    "algebra2_catalog.py",
    "geometry_catalog.py",
    "precalc_catalog.py",
    "calculus_catalog.py",
    "_legacy_algebra1_catalog.py",
]

SHIMS: dict[str, str] = {
    "base.py": "from .core.base import *  # noqa: F403\n",
    "models.py": "from .core.models import *  # noqa: F403\n",
    "registry.py": "from .core.registry import *  # noqa: F403\n",
    "scaffold.py": "from .core.scaffold import *  # noqa: F403\n",
    "api_handler.py": "from .api.handler import *  # noqa: F403\n",
    "dev_server.py": "from .api.dev_server import *  # noqa: F403\n",
    "common_settings.py": "from .settings.common_settings import *  # noqa: F403\n",
    "factoring_settings.py": "from .settings.factoring_settings import *  # noqa: F403\n",
    "latex_helpers.py": "from .utils.latex_helpers import *  # noqa: F403\n",
    "layout.py": "from .utils.layout import *  # noqa: F403\n",
}

def apply_import_updates(text: str, *, depth: int) -> str:
    """Update relative imports based on package depth from question_engine root."""
    if depth == 1:
        replacements = [
            (r"from \.catalogs\.", "from ..catalogs."),
            (r"from \.generators", "from ..generators"),
            (r"from \.base import", "from ..core.base import"),
            (r"from \.models import", "from ..core.models import"),
            (r"from \.registry import", "from ..core.registry import"),
            (r"from \.scaffold import", "from ..core.scaffold import"),
            (r"from \.common_settings import", "from ..settings.common_settings import"),
            (r"from \.factoring_settings import", "from ..settings.factoring_settings import"),
            (r"from \.latex_helpers import", "from ..utils.latex_helpers import"),
            (r"from \.layout import", "from ..utils.layout import"),
            (r"from \.\.common_settings import", "from ..settings.common_settings import"),
            (r"from \.\.factoring_settings import", "from ..settings.factoring_settings import"),
            (r"from \.\.models import", "from ..core.models import"),
            (r"from \.\.base import", "from ..core.base import"),
            (r"from \.\.latex_helpers import", "from ..utils.latex_helpers import"),
        ]
    elif depth == 2:
        replacements = [
            (r"from \.\.catalog import", "from ...catalog import"),
            (r"from \.\.base import", "from ...core.base import"),
            (r"from \.\.models import", "from ...core.models import"),
            (r"from \.\.registry import", "from ...core.registry import"),
            (r"from \.\.scaffold import", "from ...core.scaffold import"),
            (r"from \.\.common_settings import", "from ...settings.common_settings import"),
            (r"from \.\.factoring_settings import", "from ...settings.factoring_settings import"),
            (r"from \.\.latex_helpers import", "from ...utils.latex_helpers import"),
            (r"from \.\.layout import", "from ...utils.layout import"),
            (r"from \.\.generators", "from ...generators"),
        ]
    elif depth >= 3:
        replacements = [
            (r"from \.\.\.catalog import", "from ....catalog import"),
            (r"from \.\.\.base import", "from ....core.base import"),
            (r"from \.\.\.models import", "from ....core.models import"),
            (r"from \.\.\.registry import", "from ....core.registry import"),
            (r"from \.\.\.scaffold import", "from ....core.scaffold import"),
            (r"from \.\.\.common_settings import", "from ....settings.common_settings import"),
            (r"from \.\.\.factoring_settings import", "from ....settings.factoring_settings import"),
            (r"from \.\.\.latex_helpers import", "from ....utils.latex_helpers import"),
            (r"from \.\.\.layout import", "from ....utils.layout import"),
            (r"from \.\.\.generators", "from ....generators"),
            (r"from \.\.base import", "from ....core.base import"),
            (r"from \.\.models import", "from ....core.models import"),
            (r"from \.\.factoring_settings import", "from ....settings.factoring_settings import"),
            (r"from \.\.latex_helpers import", "from ....utils.latex_helpers import"),
        ]
    else:
        replacements = []

    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text


def fix_core_scaffold() -> None:
    path = QE / "core/scaffold.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace("from .common_settings import", "from ..settings.common_settings import")
    text = text.replace("from .generators import", "from ..generators import")
    path.write_text(text, encoding="utf-8")

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
    slug = chapter.lower().replace(" and ", "_and_")
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    return re.sub(r"_+", "_", slug).strip("_")


def category_to_paths(category: str) -> tuple[str, str]:
    course_label, chapter = category.split(" — ", 1)
    course_id, _ = COURSE_PREFIXES[course_label]
    return course_id, chapter_to_snake(chapter)


def ensure_package(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    init = path / "__init__.py"
    if not init.exists():
        init.write_text('"""Package."""\n', encoding="utf-8")



def move_file(src: Path, dst: Path) -> None:
    ensure_package(dst.parent)
    if src.exists():
        shutil.move(str(src), str(dst))


def write_shims() -> None:
    for name, body in SHIMS.items():
        (QE / name).write_text(body, encoding="utf-8")


def fix_core_registry() -> None:
    text = (QE / "core/registry.py").read_text(encoding="utf-8")
    text = text.replace("from .catalogs.", "from ..catalogs.")
    (QE / "core/registry.py").write_text(text, encoding="utf-8")


def fix_catalog_py() -> None:
    (QE / "catalog.py").write_text(
        textwrap.dedent(
            '''\
            """Backward-compatible re-exports from the registry layer."""

            from .catalogs.base import TypeCatalogEntry
            from .core.registry import CATEGORY_ORDER, TYPE_CATALOG, get_catalog_entry

            __all__ = ["TypeCatalogEntry", "CATEGORY_ORDER", "TYPE_CATALOG", "get_catalog_entry"]
            '''
        ),
        encoding="utf-8",
    )


def fix_package_init() -> None:
    (QE / "__init__.py").write_text(
        textwrap.dedent(
            '''\
            from . import types
            from .core.base import QUESTION_TYPES, list_question_types, register
            from .core.models import Question, QuestionSet, SettingField

            __all__ = [
                "QUESTION_TYPES",
                "Question",
                "QuestionSet",
                "SettingField",
                "list_question_types",
                "register",
                "types",
            ]
            '''
        ),
        encoding="utf-8",
    )


def fix_cli() -> None:
    text = (QE / "cli.py").read_text(encoding="utf-8")
    text = text.replace("from question_engine.api_handler import", "from question_engine.api.handler import")
    (QE / "cli.py").write_text(text, encoding="utf-8")


def fix_api_dev_server() -> None:
    text = (QE / "api/dev_server.py").read_text(encoding="utf-8")
    text = text.replace(
        "from question_engine.api_handler import",
        "from question_engine.api.handler import",
    )
    (QE / "api/dev_server.py").write_text(text, encoding="utf-8")


def fix_api_handler() -> None:
    text = (QE / "api/handler.py").read_text(encoding="utf-8")
    text = apply_import_updates(text, depth=1)
    (QE / "api/handler.py").write_text(text, encoding="utf-8")


def fix_from_generator() -> None:
    (QE / "types/_from_generator.py").write_text(
        textwrap.dedent(
            '''\
            """Register a catalog entry that uses a real generator from generators/basic.py."""

            from __future__ import annotations

            from ..core.base import register
            from ..core.registry import get_catalog_entry
            from ..core.scaffold import make_catalog_type


            def register_from_catalog(type_id: str) -> None:
                entry = get_catalog_entry(type_id)
                if entry.generator == "scaffold":
                    raise ValueError(
                        f"{type_id} uses scaffold generator; register via register_catalog_types()"
                    )
                register(make_catalog_type(entry))
            '''
        ),
        encoding="utf-8",
    )


def write_types_init() -> None:
    (QE / "types/__init__.py").write_text(
        textwrap.dedent(
            '''\
            """Discover and register all question type modules."""

            from __future__ import annotations

            import importlib
            import pkgutil
            from pathlib import Path

            from ..core.scaffold import register_catalog_types


            def _import_descendants() -> None:
                package_dir = Path(__file__).parent
                prefix = f"{__name__}."
                skip = {f"{__name__}._from_generator"}
                for module_info in pkgutil.walk_packages([str(package_dir)], prefix=prefix):
                    if module_info.name in skip:
                        continue
                    importlib.import_module(module_info.name)


            register_catalog_types()
            _import_descendants()

            __all__: list[str] = []
            '''
        ),
        encoding="utf-8",
    )


def build_generator_stubs() -> int:
    import sys

    sys.path.insert(0, str(ROOT))
    from question_engine.core.registry import TYPE_CATALOG

    created = 0
    stub_template = '''"""Catalog generator type: {type_id}."""

from question_engine.types._from_generator import register_from_catalog

register_from_catalog("{type_id}")
'''
    types_dir = QE / "types"
    for entry in TYPE_CATALOG:
        if entry.generator == "scaffold":
            continue
        course, chapter = category_to_paths(entry.category)
        dest_dir = types_dir / course / chapter
        ensure_package(dest_dir)
        dest = dest_dir / f"{entry.id}.py"
        if not dest.exists():
            dest.write_text(stub_template.format(type_id=entry.id), encoding="utf-8")
            created += 1
    return created


def update_imports_in_tree() -> None:
    skip_names = set(SHIMS) | {"catalog.py", "__init__.py", "cli.py"}
    for path in QE.rglob("*.py"):
        if path.name in skip_names and path.parent == QE:
            continue
        rel = path.relative_to(QE)
        depth = len(rel.parts) - 1
        if rel.parts[0] == "core":
            if rel.name == "scaffold.py":
                fix_core_scaffold()
            continue
        text = path.read_text(encoding="utf-8")
        updated = apply_import_updates(text, depth=depth)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def add_package_inits() -> None:
    for sub in ("core", "api", "settings", "utils", "catalogs", "generators", "frameworks", "types"):
        ensure_package(QE / sub)


def remove_legacy_files() -> None:
    for name in LEGACY_CATALOG_FILES:
        path = QE / name
        if path.exists():
            path.unlink()


def write_architecture_doc() -> None:
    (QE / "ARCHITECTURE.md").write_text(
        textwrap.dedent(
            """\
            # Question Engine Layout

            ```
            question_engine/
              __init__.py          # Public package API
              catalog.py             # Backward-compat re-exports (TYPE_CATALOG, etc.)
              cli.py                 # `python -m question_engine.cli` entry point
              api/
                handler.py           # HTTP-style generate / question-types handlers
                dev_server.py        # Local dev API server
              core/
                base.py              # QuestionType ABC, register(), QUESTION_TYPES
                models.py            # Question, QuestionSet, SettingField
                registry.py          # Aggregates per-course catalogs
                scaffold.py          # Factory for scaffold catalog types
              catalogs/
                base.py              # TypeCatalogEntry dataclass
                {course}.py          # Per-course CATALOG + CATEGORY_ORDER (data only)
              generators/
                basic.py             # Shared generator functions keyed by generator name
              settings/
                common_settings.py   # Standard worksheet settings schema
                factoring_settings.py
              utils/
                latex_helpers.py
                layout.py            # Column layout helpers
              frameworks/            # Reusable generation frameworks
              types/
                _from_generator.py   # Helper for catalog-backed generator stubs
                {course}/{chapter}/{type_id}.py
            ```

            ## Registration flow

            1. `import question_engine.types` runs `types/__init__.py`.
            2. `register_catalog_types()` registers all scaffold catalog entries.
            3. Auto-discovery imports every module under `types/{course}/{chapter}/`.
            4. Hand-written types and generator stubs call `register()` on import.

            ## Backward compatibility

            Root-level modules such as `question_engine.base`, `question_engine.models`,
            and `question_engine.api_handler` are thin re-export shims.
            """
        ),
        encoding="utf-8",
    )


def main() -> None:
    add_package_inits()

    for src, dst in MOVES:
        move_file(QE / src, QE / dst)

    for src, dst in HAND_WRITTEN_TYPE_MOVES:
        move_file(QE / src, QE / dst)
        parent = (QE / dst).parent
        while parent != QE / "types":
            ensure_package(parent)
            parent = parent.parent

    update_imports_in_tree()
    fix_core_registry()
    fix_catalog_py()
    fix_package_init()
    fix_cli()
    fix_api_dev_server()
    fix_api_handler()
    fix_from_generator()
    write_types_init()
    write_shims()
    created = build_generator_stubs()
    remove_legacy_files()
    write_architecture_doc()
    print(f"Reorganization complete. Created {created} generator stub modules.")


if __name__ == "__main__":
    main()
