# Question Engine Frameworks & Settings

Companion to [ARCHITECTURE.md](ARCHITECTURE.md). Frameworks are the **primary
producers**; settings profiles compose the UI schema; difficulty presets fill
Easy/Medium/Hard values.

## QuestionFramework

```python
from question_engine.frameworks.base import QuestionFramework

class OneStepEquationsFramework(QuestionFramework):
    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        # return prompt_latex, prompt_text, answer_latex
        ...

    # Optional:
    # def build_question_metadata(self, settings) -> dict: ...
```

`generate_batch(topic_id, settings)` loops via `generators.utils.make_questions`
and attaches enrichment metadata.

### Families (modules under `frameworks/`)

| Module | Role |
|--------|------|
| `equation.py` | Linear / absolute-value equations & inequalities |
| `number.py` | Rationals, percents, ratios, order of operations, … |
| `linear.py` | Slope, systems, variation, relations |
| `graphing.py` | Coordinate-plane / inequality graph specs |
| `geometry.py` / `geometry_extended.py` | Measurement & figures |
| `word_problem.py` | Narrative templates + numeric engines |
| `statistics.py` | Data sets / chart metadata |
| `trigonometry.py` | Right-triangle ratios |
| `inequality.py` | Shared inequality / number-line helpers |
| `adapters.py` | `framework_generators()` → `GENERATORS` entries |

Legacy or course-specific function producers still live under `generators/`
(`basic.py`, `algebra2.py`, …). New work should land in a framework first, then
expose a family key through `framework_generators`.

## Wiring a catalog type to a framework

**Preferred (catalog-only):** set `generator="one_step_equations"` on the catalog
entry. `register_catalog_types()` binds `GENERATORS["one_step_equations"]`.

**When settings need a type-module specialization:**

```python
from question_engine.frameworks import OneStepEquationsFramework
from question_engine.types._framework_type import register_framework_type

register_framework_type(
    "one_step_equations",
    OneStepEquationsFramework(),
    setting_profile="equation",
)
```

Domain helpers (`register_linear_type`, `register_geometry_type`,
`register_graphing_type`) are thin wrappers around `register_framework_type`.

**Hand-written** (rare): `@register` a `QuestionType` subclass that owns both
`settings_schema` and `generate`.

Do **not** add type modules that only call `register_from_catalog("id")` with no
overrides — catalog registration already covers those ids.

## Settings inheritance

### Schema layers

1. **`settings/domains/`** — atomic `SettingField` builders  
2. **`settings/profiles.py`** — named packs (`equation`, `polynomial`, …) via
   `PROFILE_BUILDERS`  
3. **`settings/generator_profiles.py`** — per **family / generator key**
   `TypeSettingConfig` (profile + inherits / excludes / extras / defaults)  
4. **`settings/resolve.py`** — merges standard + profile + extras − excludes  

```python
from question_engine.settings.resolve import TypeSettingConfig, resolve_type_settings

config = TypeSettingConfig(
    setting_profile="polynomial",
    inherits=("common_enrichment",),
    exclude_settings=("max_degree",),
    setting_defaults={"coef_min": -6},
)
schema = resolve_type_settings(config)
```

`standard_question_settings()` (`count`, `max_columns`, `include_answer_key`) is
always prepended. Scaffold-only types keep standard settings when no family
config exists.

### Difficulty values (not schema)

`settings/presets.py`:

- `PROFILE_DIFFICULTY_PRESETS` — keyed by profile name  
- `GENERATOR_DIFFICULTY_PRESETS` — optional overrides keyed by family or type id  

`apply_difficulty_presets` resolves overrides in order: explicit type/family
key → catalog `generator` → setting profile → `common_enrichment`. Explicit
request settings always win.

Prefer profile-level presets. Add family overrides only when a skill needs
different bounds than its profile peers.

## Question model & stimulus

```python
@dataclass
class Question:
    id: str
    topic: str                 # type_id
    prompt_latex: str
    prompt_text: str
    answer_latex: str | None = None
    metadata: dict[str, Any]   # stimulus + enrichment
```

Stimulus contracts are documented in `core/metadata.py`. Geometry prefers
server-rendered `diagram_svg`; graphing prefers client-rendered `graph_spec` /
`number_line_spec`.

## Catalog shared-family wiring

When several skills share one producer:

1. Implement one framework + one `GENERATORS` family key.  
2. Point each catalog entry’s `generator` at that key.  
3. Differ `id`, name, instructions, and (if needed) setting overrides.  
4. Expect `entry.intent == "shared_family"` when `generator != id`.  

Avoid pointing unrelated skills at a convenient generator; topic-fit QA flags
known miswires.

## Adding a Tier-2 / family type checklist

1. Domain settings in `settings/domains/` (or reuse a profile).  
2. Subclass `QuestionFramework` with `build_prompt`.  
3. Expose via `framework_generators({...})` in the right `generators/*.py`.  
4. Add `TypeSettingConfig` under that family key.  
5. Catalog `generator="family_key"`; type module only if specializing.  
6. Curriculum `type_id` + topic-fit sample if the skill is Ready.

## Verification

```bash
python -c "import question_engine.types; from question_engine.core.base import QUESTION_TYPES; print(len(QUESTION_TYPES))"
python scripts/verify_curriculum_types.py
python -m pytest question_engine/tests -q
```
