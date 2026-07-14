"""Register catalog types, then import specialization modules.

Catalog registration covers every skill. Modules under this package exist only
for framework wiring, hand-written producers, or real setting overrides.
"""

from __future__ import annotations

import importlib
from pathlib import Path

from ..core.scaffold import register_catalog_types

_HELPER_MODULES = {
    "__init__.py",
    "_from_generator.py",
    "_framework_type.py",
    "_linear_type.py",
    "_geometry_type.py",
    "_graphing_type.py",
}


def _import_descendants() -> None:
    package_dir = Path(__file__).parent
    for path in sorted(package_dir.rglob("*.py")):
        if path.name in _HELPER_MODULES:
            continue
        rel = path.relative_to(package_dir).with_suffix("")
        module_name = f"{__name__}." + ".".join(rel.parts)
        importlib.import_module(module_name)


register_catalog_types()
_import_descendants()

__all__: list[str] = []
