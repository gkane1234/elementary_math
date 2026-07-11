# Geometry diagram DSL

Reusable drawing layer for geometry questions. Generators build a
`GeometryFigure`, then attach `figure.to_metadata()` so worksheets get:

| Metadata key | Purpose |
|---|---|
| `diagram_svg` | Inline SVG for `QuestionDiagram` (KaTeX cannot draw TikZ) |
| `diagram_latex` | TikZ string for PDF/export/print |
| `diagram_spec` | Structured summary (kind, labels, segments, points) |

## Primitives

| Class | Role |
|---|---|
| `Point` | Named coordinate + optional label |
| `Segment` | Edge; optional congruence `ticks` |
| `Ray` / `Line` | Half-line / extended line |
| `Polygon` | Arbitrary vertex list (closed/open, optional fill) |
| `CirclePrim` | Circle by center + radius |
| `Arc` | Circular arc (degrees) |
| `AngleMark` | Arc mark + optional measure label |
| `RightAngleMark` | Square corner mark |
| `Label` | Free text in figure coords |
| `ShadedRegion` | Filled region by point ids or coords |

## Builders

```python
from question_engine.diagrams import (
    angle_figure,
    triangle_figure,
    circle_figure,
    polygon_figure,
    rectangle_figure,
    GeometryFigure,
    Point,
    Segment,
    Polygon,
)

# Angle with measure on the arc
fig = angle_figure("A", "B", "C", 72, show_measure=True)

# Triangle; mark missing angle with "?"
fig = triangle_figure(["A", "B", "C"], [50, 60, 70], missing="C")

# Circle with radius label
fig = circle_figure(5, unit="cm")

# Arbitrary shape
fig = polygon_figure([("A", 0, 0), ("B", 2, 0), ("C", 2.5, 1.5), ("D", 0.5, 2)])
```

## Custom figure

```python
fig = GeometryFigure(kind="custom")
fig.add_point(Point("A", 0, 0, label="A"))
fig.add_point(Point("B", 2, 0, label="B"))
fig.add_point(Point("C", 1, 1.5, label="C"))
fig.add(Polygon(["A", "B", "C"]), Segment("A", "B"), Segment("B", "C"), Segment("C", "A"))
metadata = fig.to_metadata()
```

## Attach to a question

In a framework, generate the figure from the **same** values as the prompt
(store on `self` in `build_prompt`, emit in `build_question_metadata`):

```python
def build_prompt(self, settings):
    ...
    self._last_figure = triangle_figure(...)
    return prompt, text, answer

def build_question_metadata(self, settings, **_kwargs):
    fig = getattr(self, "_last_figure", None)
    return fig.to_metadata() if fig else {}
```

Wire `QuestionDiagramFromMetadata` next to prompts (same place as
`QuestionGraphFromMetadata`). When the type renders reliably, remove its id
from `REQUIRES_DIAGRAM_TYPE_IDS` in `diagram_readiness.py`.

## Adding a new shape

1. Prefer composing existing primitives (`Polygon` covers most polygons).
2. If needed, add a dataclass in `primitives.py` and draw branches in
   `GeometryFigure._tikz_element` / `_svg_element`.
3. Optionally add a builder in `builders.py`.
4. Emit via `to_metadata()` from the generator.
