# Question Engine Architecture

## Overview

The question engine separates **catalog data** (what types exist), **registration** (how they are loaded), and **generators** (how questions are produced).

```
question_engine/
  catalogs/          # Per-course catalog data (no cross-imports)
    base.py          # TypeCatalogEntry dataclass + entry() helper
    grade_6.py
    pre_algebra.py
    algebra_1.py     # Canonical shared types (deduplicated IDs)
    geometry.py
    algebra_2.py
    precalculus.py
    calculus.py
  registry.py        # Aggregates catalogs → TYPE_CATALOG, CATEGORY_ORDER
  catalog.py         # Back-compat re-exports from registry
  scaffold.py        # Factory for scaffold-backed catalog types
  types/             # Question type modules (generators + registration)
    _from_generator.py
    {course}/{chapter}/{type_id}.py
  generators/
    basic.py         # Shared generator functions (GENERATORS dict)
```

## Catalog layer

Each `catalogs/{course}.py` exports:

- `COURSE_ID` — snake_case course id (e.g. `grade_6`, `algebra_1`)
- `CATEGORY_ORDER` — tuple of `"Course — Chapter"` display categories
- `CATALOG` — tuple of `TypeCatalogEntry` instances

Course catalogs do **not** import each other. Shared/canonical types live once in `algebra_1.py` (home course category reflects earliest appearance).

## Registry layer

`registry.py` imports each course catalog independently and builds:

- `CATEGORY_ORDER` — concatenation of per-course orders
- `TYPE_CATALOG` — concatenation of per-course catalogs
- `get_catalog_entry(type_id)` — lookup helper

## Types layer

On import, `types/__init__.py`:

1. Recursively imports all modules under `types/` (except `_`-prefixed helpers)
2. Calls `register_catalog_types()` for scaffold entries

Type modules follow `{course}/{chapter}/{type_id}.py`:

| Module kind | Example | Registration |
|---|---|---|
| Hand-written generator | `algebra_1/polynomials/quadratic_factoring.py` | `@register` class |
| Catalog generator stub | `pre_algebra/equations/one_step_equations.py` | `register_from_catalog("one_step_equations")` |
| Scaffold (no module yet) | — | `register_catalog_types()` from catalog |

Generator stubs delegate to functions in `generators/basic.py` via the catalog entry's `generator` field.

## Adding a new type

1. Add a `TypeCatalogEntry` to the appropriate `catalogs/{course}.py`
2. If it needs a real generator: add function to `generators/basic.py` and create `types/{course}/{chapter}/{id}.py` stub
3. If hand-written: create full `QuestionType` subclass under `types/{course}/{chapter}/`
4. For cross-course shared types: add once to `catalogs/algebra_1.py` with canonical id

## Curriculum alignment

`lib/curriculum.ts` chapter ids use snake_case (e.g. `equations`, `ratios`) matching the `types/` folder chapter segments. Topic `type_id` fields reference canonical catalog ids.
