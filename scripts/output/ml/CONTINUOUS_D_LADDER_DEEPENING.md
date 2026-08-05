# Continuous-D ladder deepening



Updated: 2026-07-28



Companion to `CONTINUOUS_D_FULL_MIGRATION.md` (schema complete: 601/601).

This pass deepens **D → structure** for high-ROI families so continuous

`difficulty` changes more than EMH bands.



## Pattern



When `settings["difficulty"]` is present, map D to structure knobs (same idea as

`_sci_continuous_knobs` / `_writing_numeric_complexity_from_continuous`).

Absent continuous D → leave settings alone so EMH presets / explicit knobs win.



Shared helpers live in `question_engine/settings/params.py`:



| Helper | Maps D → |

|--------|----------|

| `apply_geometry_continuous_knobs` | angle/side/radius/coord/similarity bounds, protractor step, angle piece count |

| `geometry_angle_structure_from_continuous` | multi-ray piece span + modes + total_cap |

| `geometry_proof_structure_from_continuous` | congruence theorem pool + similarity ratios + transform unlock |

| `apply_exponential_continuous_knobs` | exp base/exponent/coef (+ fractional unlock) |

| `apply_logarithm_continuous_knobs` | base/arg/ln-common unlock |

| `apply_trigonometry_continuous_knobs` | tan/cot unlock + angle span + identity / graph knobs |

| `trig_graph_structure_from_continuous` | parent → amplitude → period/phase transform |

| `apply_sequence_continuous_knobs` | nth/diff/ratio spans + negative-ratio unlock |

| `apply_calculus_continuous_knobs` | poly term/power/coef + `allow_infinity` |

| `apply_matrix_continuous_knobs` | entry/scalar/point spans + det abs max |

| `apply_conic_continuous_knobs` | center/radius/axis/focus + translated forms |

| `derivative_rule_structure_from_continuous` | coef/power + trig/exp/ln/nested unlock |

| `calc_application_structure_from_continuous` | related-rates shapes, volume methods, DE family, opt spans |

| `piecewise_structure_from_continuous` | piece count / coef / breakpoint / quadratic unlock |



Figure complexity: `diagrams/figure_families.py` already maps D →

`simple` / `standard` / `complex`. Adjacent fans scale **piece_count** with complexity.



## Wired (structure ladders)



### Geometry — angles / triangles / circles / proofs / similarity / 3D / constructions



- `frameworks/geometry.py`: continuous piece/mode ladder for measure-from-diagram;

  protractor step + angle/side/radius/coord/similarity via `_geo_local`.

- `frameworks/geometry_extended.py`:

  - `AngleAdditionFramework` continuous piece counts / modes.

  - `RemainingGeometryFramework`: congruence-proof theorem pool, similarity /

    proportional-parts ratio spans, chord/tangent/construction bands, figure

    dims from continuous geo knobs.

  - `GeometricTransformationsFramework`: coord spans + dilation/composition unlock.

  - `SolidVolumeSurfaceFramework`: applies geo knobs; side/radius grow with D.

- Classifying angles + figure_families samples use continuous D for orientation

  complexity; adjacent fans scale piece count.



Representative type_ids: `geo_basics_angles_and_their_measures`,

`geo_basics_angle_addition_postulate`, `geo_basics_classifying_angles`,

`geo_circles_circumference_and_area`, `geo_congruent_proving_triangles_congruent`,

`geo_similarity_similar_polygons`, `geo_constructions_circles`,

`geo_solid_figures_identifying_volume_and_area`, etc.



### Algebra 2 — exp/log, conics, matrices, trig graphing, sequences



- Exp: `exponential_params_from_settings` applies `apply_exponential_continuous_knobs`.

- Log / trig evaluate: continuous via params.

- Conics: center/radius/axis spans + origin-only at low D vs translated at mid/high.

- Matrices: entry/det/scalar/point spans.

- Graphing trig: `trig_graph_structure_from_continuous` (parent → amp → transform).

- Inverse exp/log: base + shift spans from exp/log knobs.

- Sequences (A2 + PC generators): `apply_sequence_continuous_knobs` via

  `sequence_params_from_settings` (nth/diff/ratio + negative ratio).



### Precalc — trig identities / piecewise / remaining trig



- Trig knobs unlock reciprocal / sum-diff / double-angle / product-to-sum by D.

- Sum/difference, multiple-angle, product-to-sum pools filter by those unlocks.

- Piecewise foundations: piece count, coef/breakpoint spans, quadratic unlock.

- Exp equations inherit continuous exponential knobs; log evaluate inherits log knobs.



### Calculus — limits / derivatives / integrals / apps / DE



- Limits / power-rule integrals / poly derivatives: `calculus_params_from_settings`

  + `allow_infinity` unlock at higher D.

- Enriched derivative rules: `derivative_rule_structure_from_continuous`.

- Related rates: circle → sphere/cone + radius/rate spans.

- Volumes (disk/washer, shell, cross-sections): bound span + method unlock.

- Separable DE: poly → exp → homogeneous family.

- Optimization foundations: perimeter / shape variety from calc-app structure.



## Still coarse (debt)



Schema field present; sampling still largely EMH-band or fixed ranges:



- **Geometry**: many right-triangle application leaves, some circle-segment /

  secant numeric paths still fixed triples; interactive construction surfaces

  remain identify-only.

- **A2**: complex polar forms, radical-exponent clusters, systems-in-3D /

  planes numeric spans, non-conic graphing wrappers beyond trig.

- **Precalc**: polynomial zeros / rational inequalities / vectors diagrams

  (scaffold), polar conics beyond identify, induction stubs.

- **Calc**: MVT / series / most app-diff definite-integral variants still

  `_difficulty_tier` EMH inside builders; Newton / motion / Riemann tables

  only lightly structured.



## Tests



`question_engine/tests/test_continuous_d_ladder_deepening.py`



- Knob widen assertions (geo / matrix / conic / exp / sequence / trig /

  proof / calc-app / piecewise / derivative structure).

- Figure complexity + adjacent piece_count D=0 vs D=20.

- Smoke generate D=0 vs D=20 for geo angles/circles/proofs/similarity,

  A2 matrix/conic/trig/sequences, PC log/trig/exp/piecewise,

  Calc limits/power/product/chain/integral/related-rates/volumes/DE/opt.

- Limit term-count average rises with D.

- Related-rates shape unlock + volume washer wording + DE family differ D=0/20.



## Files touched



- `question_engine/settings/params.py`

- `question_engine/frameworks/geometry.py`

- `question_engine/frameworks/geometry_extended.py`

- `question_engine/diagrams/figure_families.py`

- `question_engine/generators/algebra2.py`

- `question_engine/generators/precalc.py`

- `question_engine/generators/calculus.py`

- `question_engine/generators/advanced.py`

- `question_engine/generators/calculus_derivative_rules.py`

- `question_engine/tests/test_continuous_d_ladder_deepening.py`

- `scripts/output/ml/CONTINUOUS_D_LADDER_DEEPENING.md` (this file)

