# Figure diversity (textbook figure families)



We do **not** copy OpenStax (or any publisher) bitmaps. Generators procedurally

recreate standard textbook figure *kinds* — number lines, angle diagrams, area

models, circle sectors, right triangles, function sketches, etc. — with a

parameter space so a worksheet of 10 items is not 10 clones of one silhouette.



## Registry



Module: [`question_engine/diagrams/figure_families.py`](../../question_engine/diagrams/figure_families.py)



| Family id | Description | Complexity scales with D |

|-----------|-------------|---------------------------|

| `angle_rays` | Two rays + measure | Wider orientation pool; non-benchmark measures |

| `adjacent_angles` | Multi-ray fan | Piece count / combine modes (via generators) |

| `complementary_angles` | Right angle split | Rotation, reflection, which wedge is `?` |

| `supplementary_angles` | Straight line + ray | Rotation / reflection |

| `vertical_angles` | Intersecting lines | Rotation of the pair |

| `parallel_transversal` | Parallels + transversal | Slant, relation unlock, reflect |

| `triangle_angles` | Labeled triangle | Rotation / reflection; varied angles |

| `right_triangle` | Pythagorean / trig | Orientation, reflect, which side unknown |

| `triangle_area` | Base + altitude | `right` → `interior` → `exterior` layouts |

| `parallelogram` | Parallelogram / rhombus | Skew magnitude + lean direction |

| `trapezoid` | Trapezoid area | Shares skew-style diversity |

| `circle_radius` | Circle + radius | Radius angle; diameter at high D |

| `circle_sector` | Central angle / sector | Start angle + central measure |

| `number_line` | 1D plot / inequality | Range + tick density |

| `coordinate_plane` | Axes + objects | Window size + object budget |

| `percent_shade` | Grid / bar / circle | Figure kind + shade pattern |

| `area_model` | Distributive rectangle | Split orientation |

| `tape_diagram` | Tape / hanger | Part count; unequal segments |

| `function_sketch` | Calc curve / tangent / area | Curve kind + feature unlock; procedural SVG |

| `decimal_grid` | Place-value / hundredths | Style + places unlock with D |

| `box_plot` | Box-and-whisker layout | Orientation / outlier unlock |



API:



```python

from question_engine.diagrams import sample_figure, sample_figure_from_settings



sample = sample_figure("angle_rays", difficulty=12, seed=7, batch_index=3, build=True)

# sample.params, sample.complexity, sample.figure, sample.diagram_spec

```



Worksheet batches: `make_questions` / `QuestionFramework.generate_batch` call

`apply_batch_seed(settings, i)` so `seed` + item index reseed global RNG and set

`_batch_index` for family sampling.



## type_id → family (primary)



See `TYPE_ID_FAMILY` in `figure_families.py`. High-impact wired generators:



| type_id / generator | Family |

|---------------------|--------|

| `geo_basics_classifying_angles` | `angle_rays` |

| `geo_basics_angle_relationships`, `pa_angle_relationships` | complementary / supplementary / vertical |

| `geo_basics_angle_addition_postulate` | `adjacent_angles` |

| `g6_triangles`, `geo` triangle area leaves | `triangle_area` |

| `geo_triangles_and_quadrilaterals_area` | `triangle_area` / `parallelogram` / `trapezoid` (mix) |

| `geo_quadrilateral_area` | `parallelogram` / `trapezoid` (quad mix) |

| `geo_right_pythagorean_theorem`, `pythagorean_theorem` | `right_triangle` |

| `geo_congruent_*` triangle sum / midsegment | `triangle_angles` |

| `geo_parallel_parallel_lines_and_transversals` | `parallel_transversal` (family sample + reflect) |

| `geo_basics_segment_addition_postulate` | `number_line` (family complexity metadata) |

| `pa_circles`, `geo_circles_circumference_and_area` | `circle_radius` |

| `g6_introduction_to_percents` | `percent_shade` |

| `g6_solving_percent_problems_with_diagrams` | `percent_shade` (blank + answer shade) |

| `g6_decimal_addition_with_diagrams` / subtraction | `decimal_grid` (place-value / hundredths) |

| `g6_decimal_multiplication_with_area_diagrams` | `area_model` |

| `g6_numbers_on_a_number_line` | `number_line` (params + continuous D) |

| `calc_app_diff_slope_tangent_and_normal_lines` | `function_sketch` |

| `calc_app_diff_related_rates` | `function_sketch` (ladder / circle) |

| `calc_def_int_approximating_area_under_a_curve` | `function_sketch` (Riemann bars) |



## Continuous difficulty



Figure-heavy setting profiles expose numeric `difficulty` (not EMH-only):



- `geometry_basic` / `geometry_angles` / `geometry_triangles` / `geometry_circles`

- `number_line`, `coordinate_plane`, `coordinate_geometry`, `graphing`

- `percent`, `equation`, `inequality` (tape/hanger leaves)

- `radical` (geo review leaves)



Higher D unlocks more complex family variants (layouts, orientations, shade

patterns, multi-panel percent, exterior altitudes, etc.).



## Remaining gaps



- Calc `function_sketch` now covers parabola / cubic / sine / exp / reciprocal /

  abs-linear with tangent, normal, Riemann, asymptote, and related-rates silhouettes;

  more app-diff leaves (curve sketching UI, f/f′/f″ comparison) still deferred.

- Construction / solid isometric sketches still use limited templates.

- Coordinate / inequality graph metadata varies numerically; silhouette diversity

  is milder than geometry SVG families.

- Most RemainingGeometry modes still lightly templated; `midsegment` (and

  congruence) now sample `triangle_angles` for orientation diversity; parallel

  transversals sample `parallel_transversal` for relation / reflect unlock.

- `g6_drawing_box_plots` still lacks a student-draw UI (interpret path is Ready).



Effort-scorer coverage for continuous-D catalog types: see

[`UNSCORED_EFFORT.md`](UNSCORED_EFFORT.md) (**COMPLETE:** **0** unscored / **601** scored).



## Catalog orphans (resolved)



Previously missing generators referenced by catalog / `test_diagrams.py`:



| Generator key | Wiring |

|---------------|--------|

| `geo_triangles_and_quadrilaterals_area` | `PlaneFiguresAreaFramework(include_triangle=True)` |

| `geo_quadrilateral_area` | `PlaneFiguresAreaFramework(include_triangle=False)` |



These are thin mixes over existing triangle / square / rectangle / parallelogram /

rhombus / trapezoid / kite builders (not new formula engines).


