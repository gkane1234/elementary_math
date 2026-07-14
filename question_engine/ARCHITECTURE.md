# Question Engine Architecture

## What generation is

A **curriculum topic** resolves to a **registered question type**, which uses a
**settings schema** (profile + difficulty) to call a **producer family** that
returns `Question` objects (LaTeX prompt/answer + optional stimulus in
`metadata`).

## Five responsibilities

| Layer | Job | Owner |
|-------|-----|--------|
| **1. Declare** | Navigation + skill identity | `lib/curriculum.ts` → `question_engine/catalogs/` |
| **2. Configure** | Settings schema ≠ difficulty values | `settings/domains` → `profiles` → `generator_profiles`; values in `presets` |
| **3. Produce** | Math / prompts | `frameworks/` (primary); `generators/` as thin key adapters; rare `@register` hand-written types |
| **4. Package** | Stable payload | `Question` / `QuestionSet` + typed stimulus keys in `metadata` |
| **5. Verify** | Topic fit / readiness | `qa/topic_fit.py`, curriculum picker readiness |

```
Curriculum topic.id
        │ type_id
        ▼
Catalog entry (type_id, generator/family, intent)
        │
        ├─► Settings schema (by family) + difficulty presets
        │
        └─► Producer family.generate_batch(type_id, settings)
                    │
                    ▼
              Question(+ metadata) → QuestionSet JSON → UI
```

### Three IDs (keep them distinct)

1. **Curriculum topic `id`** — UI tree key  
2. **`type_id`** — catalog / `QUESTION_TYPES` key used to generate  
3. **`generator` (family key)** — producer + default settings lookup in `GENERATORS`

Intentional curriculum redirects may set `type_id` ≠ topic `id`. Catalog entries
whose `generator` ≠ `id` are **shared-family** wirings (same math engine,
different skill label/instructions).

### Catalog intent

Each catalog entry exposes `intent`:

| Value | Meaning |
|-------|---------|
| `scaffold` | Placeholder producer (`generator="scaffold"` or missing key) |
| `shared_family` | Uses another skill’s producer family (`generator` ≠ `id`) |
| `ready` | Own family key (`generator` == `id`, real producer) |

## End-to-end request path

```
UI / CLI / scripts
  → handle_generate (api/handler.py)
  → apply_difficulty_presets + schema defaults
  → QUESTION_TYPES[type_id].generate(settings)
  → producer (framework / GENERATORS[key] / hand-written)
  → QuestionSet.to_dict()
```

Same core path: worksheet UI (`lib/api.ts`), FastAPI (`backend/main.py`),
local Python API, CLI, and `scripts/topic_fit_sample.py`.

## Package layout

```
question_engine/
  catalogs/           # Per-course TypeCatalogEntry rows (no cross-imports)
  core/
    base.py           # QuestionType, QUESTION_TYPES, @register
    models.py         # Question, QuestionSet, SettingField
    registry.py       # Aggregates catalogs → TYPE_CATALOG
    scaffold.py       # make_catalog_type / register_catalog_types
    metadata.py       # Stimulus / scaffold typed keys
  types/              # Specializations only (framework / hand-written)
    _framework_type.py
    _from_generator.py  # Optional setting overrides over catalog defaults
    {course}/{chapter}/{type_id}.py
  frameworks/         # Primary producers (QuestionFramework families)
  generators/         # GENERATORS[key] → thin adapters / legacy functions
  settings/
    domains/          # Atomic SettingField builders
    profiles.py       # Named schemas composed from domains
    generator_profiles.py  # Per-family TypeSettingConfig
    presets.py        # Easy/Medium/Hard values (not schema)
    resolve.py        # resolve_type_settings()
  diagrams/           # SVG / TikZ builders → metadata
  qa/                 # Topic-fit helpers
  api/                # HTTP handlers + local server
```

## Registration (catalog declares; modules specialize)

On import, `types/__init__.py`:

1. `register_catalog_types()` — every catalog entry becomes a `QuestionType`
   via its `generator` key (scaffold fallback if missing).
2. Imports type modules under `types/` — **only** when needed to:
   - bind a framework with richer settings (`register_framework_type`), or
   - provide hand-written `@register` math, or
   - override settings via `register_from_catalog(..., setting_profile=…)`.

Do **not** add one-liner `register_from_catalog("id")` stubs; catalog
registration already covers wired keys.

## Settings: schema ≠ values

```
domains/*.py        atomic fields
    ↓
profiles.py         named schema packs (equation, polynomial, …)
    ↓
generator_profiles  per family key → TypeSettingConfig
    ↓
resolve.py          final UI schema
```

Difficulty presets live in `presets.py` (and the TS mirror for the settings
form). Lookup prefers an explicit family/type override, then the catalog’s
`generator` key, then the setting profile.

## Producers

- Prefer **`QuestionFramework.generate_batch`** for new skill families.
- Register the family under a stable `generator` key; catalog entries point at
  that key. Shared-family types reuse the key with different `id` /
  instructions.
- `GENERATORS` remains the catalog lookup table: framework-backed entries should
  be thin wrappers (`frameworks/adapters.py`), not a second copy of the math.
- Hand-written `@register` types are for one-off symbolic pipelines (e.g.
  factoring via `polynomial_core`).

## Stimulus

Diagrams and graphs live in `Question.metadata`:

| Kind | Typical keys | Who draws |
|------|--------------|-----------|
| Geometry / charts | `diagram_svg` (+ optional TikZ) | Backend SVG; UI injects |
| Graphs | `graph_spec` / `answer_graph_spec` | Backend declares; UI draws |
| Number lines | `number_line_spec` | Backend declares; UI draws |

Prefer one stimulus channel per question unless the UI intentionally shows both.

## Curriculum alignment

`lib/curriculum.ts` leaf topics optionally set `type_id` to a catalog id.
Readiness (`lib/curriculum-picker.ts`) requires a real, non-denylisted type.

## Adding a new type

1. Add a `TypeCatalogEntry` in the appropriate `catalogs/{course}.py` with the
   correct `generator` family key (or `"scaffold"` until wired).
2. If the family is new: implement a `QuestionFramework`, expose it via
   `GENERATORS` with `framework_generators(...)`, and add a
   `TypeSettingConfig` under that family key.
3. Add a type module **only** for framework setting specialization or
   hand-written logic.
4. Link the curriculum leaf `type_id` when the topic should appear Ready.
5. Prefer profile-level difficulty presets; add family overrides in
   `GENERATOR_DIFFICULTY_PRESETS` only when needed.

## Related docs

- [FRAMEWORK.md](FRAMEWORK.md) — producer families, settings inheritance, wiring patterns
