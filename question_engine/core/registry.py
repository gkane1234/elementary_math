"""Global registry: aggregates per-course catalogs without cross-imports between them."""

from __future__ import annotations

from ..catalogs.algebra_1 import CATALOG as ALGEBRA1_CATALOG
from ..catalogs.algebra_1 import CATEGORY_ORDER as ALGEBRA1_CATEGORY_ORDER
from ..catalogs.algebra_2 import CATALOG as ALGEBRA2_CATALOG
from ..catalogs.algebra_2 import CATEGORY_ORDER as ALGEBRA2_CATEGORY_ORDER
from ..catalogs.base import TypeCatalogEntry
from ..catalogs.calculus import CATALOG as CALCULUS_CATALOG
from ..catalogs.calculus import CATEGORY_ORDER as CALCULUS_CATEGORY_ORDER
from ..catalogs.geometry import CATALOG as GEOMETRY_CATALOG
from ..catalogs.geometry import CATEGORY_ORDER as GEOMETRY_CATEGORY_ORDER
from ..catalogs.grade_6 import CATALOG as GRADE6_CATALOG
from ..catalogs.grade_6 import CATEGORY_ORDER as GRADE6_CATEGORY_ORDER
from ..catalogs.pre_algebra import CATALOG as PREALGEBRA_CATALOG
from ..catalogs.pre_algebra import CATEGORY_ORDER as PREALGEBRA_CATEGORY_ORDER
from ..catalogs.precalculus import CATALOG as PRECALC_CATALOG
from ..catalogs.precalculus import CATEGORY_ORDER as PRECALC_CATEGORY_ORDER

CATEGORY_ORDER: tuple[str, ...] = (
    GRADE6_CATEGORY_ORDER
    + PREALGEBRA_CATEGORY_ORDER
    + ALGEBRA1_CATEGORY_ORDER
    + GEOMETRY_CATEGORY_ORDER
    + ALGEBRA2_CATEGORY_ORDER
    + PRECALC_CATEGORY_ORDER
    + CALCULUS_CATEGORY_ORDER
)

TYPE_CATALOG: tuple[TypeCatalogEntry, ...] = (
    ALGEBRA1_CATALOG
    + GRADE6_CATALOG
    + PREALGEBRA_CATALOG
    + ALGEBRA2_CATALOG
    + GEOMETRY_CATALOG
    + PRECALC_CATALOG
    + CALCULUS_CATALOG
)

_CATALOG_BY_ID: dict[str, TypeCatalogEntry] = {entry.id: entry for entry in TYPE_CATALOG}


def get_catalog_entry(type_id: str) -> TypeCatalogEntry:
    entry = _CATALOG_BY_ID.get(type_id)
    if entry is None:
        raise KeyError(f"Unknown catalog type id: {type_id}")
    return entry
