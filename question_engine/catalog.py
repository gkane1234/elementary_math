"""Backward-compatible re-exports from the registry layer."""

from .catalogs.base import TypeCatalogEntry
from .core.registry import CATEGORY_ORDER, TYPE_CATALOG, get_catalog_entry

__all__ = ["TypeCatalogEntry", "CATEGORY_ORDER", "TYPE_CATALOG", "get_catalog_entry"]
