# Topic-fit QA report — geometric transformations

Scope: `pa_transformations`, `geo_transformations_translations_rotations_reflections_and_dilations`

Sample packs from the original QA run were removed in the 2026-07-28 `scripts/output` cleanup (dated `20260713T*` dumps). Findings below are retained from that review.

## Rubric

| Criterion | Pass when |
|-----------|-----------|
| Topic? | Prompt asks for geometric shape transforms on a plane |
| Method? | Translation / reflection / rotation / dilation of a figure |
| Hard harder? | Hard uses dilations or compositions within the same skill |
| Ready integrity? | No scaffold / stub under Ready types |
| Wiring? | Not aliased to quadratic/`graph_transformations` |

## Verification table

| Type | E sample | M sample | H sample | Topic? | Method? | Hard harder? | Status |
|------|----------|----------|----------|--------|---------|--------------|--------|
| `pa_transformations` | triangle translated 1R/3D | reflected across y-axis | translate then reflect | Y | Y | Y | Pass |
| `geo_transformations_…` | triangle translated 2R/1U | rotate 90° CW | composition | Y | Y | Y | Pass |

## Diagnosis (before)

- `pa_transformations` was wired to generator `graph_transformations` → quadratic `f(x)=x^2` prompts.
- Geo type already used `geo_transformations`, but that previously hit a thin RemainingGeometry stub.
- No Grade 6 transform type_id exists.
- `pc_transformations_of_graphs` correctly keeps `graph_transformations` (function graphs).

## Fix

- Rewired `pa_transformations` → `geo_transformations`.
- Implemented `GeometricTransformationsFramework` (plane figures + graph/diagram metadata).
- Easy translations; medium reflections/rotations; hard dilations/compositions.

## Files touched

- `question_engine/frameworks/geometry_extended.py`
- `question_engine/generators/geometry.py`
- `question_engine/catalogs/pre_algebra.py`
- `question_engine/settings/generator_profiles.py` / `presets.py`
- `lib/difficulty-presets.ts`
- `question_engine/qa/topic_fit.py`
- `question_engine/tests/test_geometric_transformations.py`
