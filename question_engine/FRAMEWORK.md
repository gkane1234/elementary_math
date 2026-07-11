# Question Engine Framework

Architecture overview and roadmap for scaling from **52 implemented** question types to the full **595-type** catalog (543 scaffold placeholders).

## A. Current Generator Architecture

### Registry and base class

All generators register through `QuestionType` in `question_engine/base.py`:

```python
@register
class MyQuestionType(QuestionType):
    id = "my_type"
    name = "Display name"
    category = "Algebra 1 — Equations"
    subcategory: str | None = None

    def settings_schema(self) -> list[SettingField]: ...
    def generate(self, settings: dict) -> list[Question]: ...
```

- `QUESTION_TYPES` — global dict keyed by canonical `id`
- `register()` — instantiates the class and inserts into `QUESTION_TYPES`
- `list_question_types()` — sorted export for `/api/question-types`

### Catalog + scaffold factory

Most types (~590) are declared in course catalogs (`catalog.py`, `grade6_catalog.py`, etc.) as `TypeCatalogEntry` rows. At import time, `scaffold.py` wraps each entry:

1. Look up `entry.generator` in `generators/basic.py` → `GENERATORS`
2. Fall back to `_scaffold` (random `a + b` placeholder) when no generator key matches
3. Attach `standard_question_settings()` from `common_settings.py`

Hand-written types in `question_engine/types/` bypass the catalog factory and register directly via `@register`.

### SettingField and common settings

`SettingField` (`models.py`) drives the UI settings form:

| type     | purpose                          |
|----------|----------------------------------|
| `int`    | numeric setting with min/max     |
| `range`  | bounded slider                   |
| `select` | enumerated options               |
| `bool`   | toggle                           |

`standard_question_settings()` provides cross-cutting fields:

- `count` — number of questions (default 10)
- `max_columns` — layout (`auto`, `1`, `2`, `3`)
- `include_answer_key` — whether to populate `answer_latex`

Domain-specific settings (e.g. `factoring_settings.py`) compose with shared fields.

### Settings inheritance and profiles

Reusable **domain profiles** live in `settings/profiles.py` and compose atomic builders from `settings/domains/`:

| Profile | Typical settings |
|---------|------------------|
| `polynomial` | degree range, coefficient bounds, variable, integer-only |
| `polynomial_factoring` | polynomial + factoring method toggles |
| `polynomial_division` | degree bounds for numerator/denominator, divide cleanly |
| `equation` | coefficients, variable, solution type, allowed operations |
| `inequality` | equation bounds + steps + graph metadata + symbol family |
| `number` | numerator/denominator bounds, allow negative |
| `linear` | slope/intercept/coordinate bounds, integer coordinates |
| `radical` | radicand range, root index, require simplifiable |
| `quadratic` | fixed degree-2 coefficients + factoring methods |

**Resolution** (`settings/resolve.py`):

```python
from question_engine.settings.resolve import TypeSettingConfig, resolve_type_settings

config = TypeSettingConfig(
    setting_profile="polynomial",
    inherits=("equation",),          # optional extra profiles
    exclude_settings=("max_degree",), # opt-out by key
    setting_defaults={"coef_min": -6},
)
schema = resolve_type_settings(config)
```

**Registration patterns:**

- `register_framework_type("one_step_equations", framework, setting_profile="equation")`
- `register_from_catalog("polynomial_multiply")` — looks up `settings/generator_profiles.py` by catalog `generator` key
- Hand-written types: `schema_for_generator("quadratic_factoring")`

`standard_question_settings()` (`count`, `max_columns`, `include_answer_key`) are always prepended. Scaffold catalog types keep standard settings only.

### Question model

```python
@dataclass
class Question:
    id: str
    topic: str              # canonical type_id
    prompt_latex: str       # rendered in worksheet
    prompt_text: str        # plain-text fallback / search
    answer_latex: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
```

`metadata` carries generator-specific data (factoring method, scaffold flag, diagram spec placeholders).

### basic.py generator patterns

`generators/basic.py` defines reusable patterns:

| Pattern | Examples |
|---------|----------|
| `_make_questions` | Loop `count` times, call builder closure |
| Random parameter builders | `_one_step_equations`, `_percents`, … |
| Polynomial core integration | `_polynomial_factoring`, `_polynomial_multiply` |
| Fraction LaTeX helpers | `_frac_latex`, `_random_fraction` |
| Scaffold fallback | `_scaffold` — marks `metadata.scaffolded = True` |

Catalog entries point to generator keys via `generator="one_step_equations"`.

### API flow

`api_handler.py` → `_generate_for_type(type_id, settings)` → `QuestionType.generate()`.

---

## B. Features Needed for All ~595 Types

### Reusable building blocks

| Module (proposed) | Responsibility |
|-------------------|----------------|
| **Number** | Integers, rationals, decimals, percents, scientific notation |
| **Equation** | Linear / absolute-value / radical / rational equations, literal equations |
| **Inequality** | One/multi-step, compound, absolute value, graph specs |
| **Polynomial** | Arithmetic, factoring (via `polynomial_core`), long division |
| **Expression** | Simplify, evaluate, equivalent forms |
| **WordProblem** | Template + numeric parameter injection, unit handling |
| **Geometry** | Figure specs (segments, angles, polygons), area/volume formulas |
| **Graphing** | Coordinate prompts, slope/intercept, inequality shading metadata |
| **Statistics** | Data set generation, plots, center/spread |
| **Trig** | Right-triangle ratios, unit circle, equations |
| **Calculus** | Limit expressions, derivative rules, integral forms |
| **LaTeX** | Fractions, cases, aligned systems, text wrappers |
| **Validation** | Answer equivalence (symbolic / numeric tolerance) |
| **Diagrams** | SVG/TikZ metadata for area models, number lines, coordinate planes |

### Answer formats

- **Free response** — `answer_latex` string (current default)
- **Multiple choice** — extend `Question.metadata` with `choices[]` + `correct_index`
- **Graphing** — `metadata.graph_spec` for client-side renderers

---

## C. Generator Families (595 types)

Priority tiers:

- **Tier 1** — Implemented (real generator, not scaffold)
- **Tier 2** — Shares infrastructure with Tier 1; high reuse
- **Tier 3** — Needs new domain module (geometry figures, trig diagrams, calculus CAS)

| Family | Count | Tier 1 | Tier 2 | Tier 3 | Notes |
|--------|------:|-------:|-------:|-------:|-------|
| Polynomials & quadratics | 42 | 13 | 20 | 9 | Factoring via `polynomial_core`; graphing quadratics Tier 3 |
| Ratios, rates, proportions | 57 | 1 | 40 | 16 | `solving_proportions` done; G6 ratio topics Tier 2 |
| Inequalities | 44 | 5 | 30 | 9 | `_inequality()` covers 1–3 step; graphing Tier 3 |
| Geometry measurement | 64 | 0 | 15 | 49 | Needs figure spec module |
| Other / misc | 145 | 6 | 50 | 89 | Split as domains mature |
| Trigonometry | 38 | 0 | 10 | 28 | Right-triangle ratios Tier 2 |
| Logs & exponentials | 32 | 1 | 18 | 13 | Growth/decay done; log rules Tier 2 |
| Graphing & linear | 29 | 2 | 20 | 7 | `writing_linear_equations`; slope/graph Tier 2–3 |
| Rational numbers | 20 | 3 | 15 | 2 | `rational_add/multiply/divide` done |
| Equation solving | 14 | 5 | 7 | 2 | Core linear pipeline done |
| Word problems | 16 | 0 | 12 | 4 | Template engine Tier 2 |
| Statistics & data | 16 | 0 | 8 | 8 | Data-set builder Tier 2 |
| Radicals | 10 | 5 | 4 | 1 | Simplify + ops done |
| Percents | 8 | 2 | 6 | 0 | `percents`, `percent_of_change` |
| Scientific notation | 3 | 3 | 0 | 0 | Fully covered |
| Sequences & series | 10 | 0 | 8 | 2 | Formula templates Tier 2 |
| Probability & counting | 11 | 0 | 6 | 5 | Combinatorics Tier 2 |
| Conic sections | 9 | 0 | 2 | 7 | Graph + equation Tier 3 |
| Calculus (limits/deriv) | 17 | 0 | 4 | 13 | Symbolic differentiation Tier 3 |
| Calculus (integration) | 4 | 0 | 2 | 2 | Rule templates Tier 2–3 |
| Matrices | 2 | 0 | 2 | 0 | Extend `_systems` pattern |

### Top 10 families to build next (by curriculum coverage × reuse)

1. **Grade 6 ratios & rates** (57 related) — extend `NumberFramework` + proportion templates
2. **Inequality graphing** (44) — `InequalityFramework` + number-line metadata
3. **Geometry area/volume** (64) — `GeometryFigureSpec` module
4. **Word problems** (16 + scattered) — `WordProblemTemplate` with numeric engine
5. **Properties of exponents / integer ops** (Tier 2) — expression simplify builder
6. **Trigonometry ratios** (38) — right-triangle figure + ratio table
7. **Statistics displays** (16) — synthetic data sets + chart metadata
8. **Graphing linear functions** (29) — slope/intercept from two points
9. **Logarithmic expressions** (32) — log property simplify (Tier 2)
10. **Sequences & series** (10) — closed-form term generators

---

## D. Core Infrastructure

Reusable modules that all Tier 2 types should build on:

```
question_engine/
  frameworks/
    base.py          # QuestionFramework ABC — build_prompt + generate_batch
    equation.py      # EquationFramework, OneStepEquationsFramework
    number.py        # NumberFramework, RationalFramework, PercentFramework
    inequality.py    # InequalityFramework, NumberLineSpec (skeleton)
    word_problem.py  # WordProblemFramework, WordProblemTemplate (skeleton)
    geometry.py      # GeometryFramework, GeometryFigureSpec (skeleton)
    graphing.py      # GraphingFramework, CoordinatePlaneSpec (skeleton)
    statistics.py    # StatisticsFramework, DataSetSpec, ChartSpec (skeleton)
    trigonometry.py  # TrigFramework, RightTriangleSpec (skeleton)
  settings/
    standard.py      # standard_question_settings(), merge_settings()
    profiles.py      # polynomial_settings(), equation_settings(), …
    resolve.py       # TypeSettingConfig, resolve_type_settings()
    generator_profiles.py  # per-generator default inheritance
    params.py        # polynomial_params_from_settings(), linear_params_from_settings()
    domains/
      equation.py    # equation_coef_settings(), operation/solution toggles
      polynomial.py  # degree, coef, division, factoring settings
      number.py      # rational, percent, decimal, ratio settings
      linear.py      # slope, intercept, systems, variation settings
      radical.py     # radical_settings()
      inequality.py  # inequality_settings() — steps, graph metadata
      rational.py    # rational-expression extra controls
      misc.py        # expression / verbal phrase settings
      word_problem.py # word_problem_settings() — difficulty, units
      geometry.py    # geometry_settings() — include_diagram
  core/
    metadata.py      # ScaffoldMetadata, GraphSpec, question_metadata()
    validation.py    # answers_equivalent() — numeric now, sympy later
  generators/
    utils.py         # make_questions, frac_latex, random_fraction, helpers
```

Backward-compat shims remain at `common_settings.py` and `factoring_settings.py` (package root).

### QuestionFramework pattern

```python
from question_engine.frameworks.base import QuestionFramework
from question_engine.frameworks.equation import OneStepEquationsFramework
from question_engine.settings.domains.equation import equation_coef_settings

class OneStepEquationsQuestionType(QuestionType):
    _framework = OneStepEquationsFramework()

    def settings_schema(self):
        return QuestionFramework.framework_settings(equation_coef_settings())

    def generate(self, settings):
        return self._framework.generate_batch(self.id, settings)
```

Frameworks own:

- `build_prompt(settings) -> (latex, text, answer)` — single instance
- `generate_batch(topic_id, settings)` — loops via `make_questions`
- `framework_settings(*domain_schemas)` — merges standard + domain `SettingField`s
- Optional `build_metadata(settings)` for per-question metadata (e.g. `steps`)

`generators/basic.py` keeps `GENERATORS` keys for catalog wiring; new types can delegate to the same framework class.

### Metadata and validation

- `question_metadata(**kwargs)` — consistent keys on `Question.metadata`
- Scaffold catalog types always set `metadata.scaffolded = True`
- API generation annotates `metadata.generation_settings` (regeneration snapshot)
- `answers_equivalent(given, expected)` — normalized string + numeric tolerance (sympy extension point documented)

### Adding a new Tier 2 type

1. Add domain settings in `settings/domains/` (or reuse existing)
2. Subclass `QuestionFramework` with `build_prompt`
3. Register a `QuestionType` in `types/` using `framework_settings()` + `generate_batch`
4. Optionally add a `GENERATORS` entry in `basic.py` for catalog `generator="..."` keys

**Reference implementation:** `types/pre_algebra/equations/one_step_equations.py`

---

## D2. Skeleton Domain Frameworks (Tier 2)

Skeleton modules extend `QuestionFramework` with dataclass specs and `build_metadata`;
`build_prompt` raises `NotImplementedError` until wired to real generators. Domain
settings live in `settings/domains/` and compose via `QuestionFramework.framework_settings()`.

| Framework | Module | Settings helper | Catalog family unlocked | Types (approx.) |
|-----------|--------|-----------------|-------------------------|----------------:|
| `InequalityFramework` | `frameworks/inequality.py` | `inequality_settings()` | Inequalities — solving + number-line / coordinate graphing | 44 |
| `WordProblemFramework` | `frameworks/word_problem.py` | `word_problem_settings()` | Word problems (equations, proportions, systems, work/DRT/mixture) | 16+ |
| `GeometryFramework` | `frameworks/geometry.py` | `geometry_settings()` | Geometry measurement (area, volume, composite figures) | 64 |
| `GraphingFramework` | `frameworks/graphing.py` | *(inline: show_grid, quadrant)* | Graphing & linear functions (slope, intercept, coordinate plane) | 29 |
| `StatisticsFramework` | `frameworks/statistics.py` | *(TBD)* | Statistics & data (dot plot, histogram, box plot, center/spread) | 16 |
| `TrigFramework` | `frameworks/trigonometry.py` | *(TBD)* | Trigonometry (right-triangle ratios, solve triangles) | 38 |

### Metadata contracts

| Spec | Stored in `Question.metadata` | Purpose |
|------|----------------------------------|---------|
| `NumberLineSpec` | `number_line_spec` | Inequality shading on a number line |
| `GraphSpec` | `graph_spec` | Coordinate plane bounds, points, functions |
| `GeometryFigureSpec` | `figure_spec`, `diagram_spec` | Legacy labeled figure summary |
| `GeometryFigure` (diagrams DSL) | `diagram_svg`, `diagram_latex`, `diagram_spec` | TikZ + SVG geometry drawings |
| `CoordinatePlaneSpec` | `coordinate_plane`, `graph_spec` | Slope, intercept, sampled points |
| `DataSetSpec` + `ChartSpec` | `data_set`, `chart_spec` | Synthetic data + chart renderer hints |
| `RightTriangleSpec` | `right_triangle_spec`, `diagram_spec` | Legs, angle, trig ratio target |

### Wiring a skeleton type

```python
from question_engine.frameworks import InequalityFramework
from question_engine.settings.domains.inequality import inequality_settings

class GraphingOneStepInequalities(QuestionType):
    _framework = InequalityFramework(steps=1)

    def settings_schema(self):
        return QuestionFramework.framework_settings(inequality_settings())

    def generate(self, settings):
        return self._framework.generate_batch(self.id, settings)
```

Tier 2 implementation order matches §B top priorities: inequality graphing → geometry
figures → word-problem templates → trig ratios → statistics charts → linear graphing.

---

## E. Proposed Framework Modules (legacy sketch)

Skeleton classes live in `question_engine/frameworks/`:

```
frameworks/
  __init__.py      # exports framework bases
  equation.py      # EquationFramework — one/two/multi-step
  number.py        # NumberFramework — rational, percent, scientific notation
```

### Usage pattern (target)

```python
class OneStepEquations(QuestionType):
    _framework = LinearEquationFramework(steps=1)

    def generate(self, settings):
        return self._framework.generate_batch(self.id, settings)
```

Frameworks own:

- Parameter sampling (`coef_min`, `coef_max`, …)
- Prompt / answer LaTeX construction
- Validation rules
- Optional `metadata` for diagrams

New catalog entries set `generator="..."` or subclass a hand-written type that delegates to a framework.

---

## F. Curriculum Integration

TypeScript curriculum leaf topics now carry optional `type_id` linking to the canonical registry:

- `lib/types.ts` — `CurriculumTopic.type_id?: string | null`
- `lib/curriculum.ts` — 109 leaf references → 52 unique implemented types
- `lib/curriculum-types.ts` — `getTopicsWithGenerators`, `findCurriculumReferences`, `getTypeIdToCurriculumPaths`
- `scripts/verify_curriculum_types.py` — CI check

Duplicate curriculum appearances (e.g. `one_step_equations` in Pre-Algebra and Algebra 1) share the same `type_id`.

---

## G. Implementation Status Summary

| Metric | Count |
|--------|------:|
| Total registered types | 595 |
| Real generators | 52 |
| Scaffold-only | 543 |
| Curriculum leaves with `type_id` | 109 |
| Unique types linked in curriculum | 52 |

### Tier 1 — Implemented type IDs

`absolute_value_equations`, `absolute_value_inequalities`, `compound_inequalities`, `continuous_relations`, `direct_inverse_variation`, `discrete_relations`, `distributive_property`, `evaluating_graphing_functions`, `exponential_growth_decay`, `multi_step_equations`, `multi_step_inequalities`, `one_step_equations`, `one_step_inequalities`, `percent_of_change`, `percents`, `polynomial_add_subtract`, `polynomial_factoring_common_factor`, `polynomial_factoring_grouping`, `polynomial_factoring_special_cases`, `polynomial_long_division`, `polynomial_multiply`, `polynomial_multiply_special`, `polynomial_naming`, `quadratic_completing_square_constant`, `quadratic_completing_square_solve`, `quadratic_discriminant`, `quadratic_factoring`, `quadratic_factoring_equations`, `quadratic_formula`, `quadratic_square_roots`, `radical_add_subtract`, `radical_distance_formula`, `radical_divide`, `radical_equations`, `radical_midpoint_formula`, `radical_multiply`, `radical_simplification`, `rational_add_subtract`, `rational_divide`, `rational_expression_multiply_divide`, `rational_expression_simplification`, `rational_multiply`, `rational_simplification`, `scientific_notation_add_subtract`, `scientific_notation_operations`, `scientific_notation_write`, `solving_proportions`, `systems_elimination`, `systems_substitution`, `two_step_equations`, `two_step_inequalities`, `writing_linear_equations`

---

## H. Verification

```bash
python scripts/verify_curriculum_types.py
python scripts/map_curriculum_types.py   # rebuild type_id on curriculum.ts
npx tsc --noEmit
```
