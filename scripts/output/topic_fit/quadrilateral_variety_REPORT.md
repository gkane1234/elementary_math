# Topic-fit: Quadrilateral variety

| Type | E/M/H samples | Topic? | Method? | Hard harder? | Status |
|------|---------------|--------|---------|--------------|--------|
| `pa_area_of_triangles_and_quadrilaterals` | 40 each | Pass | Named area formulas | Yes (kite/trap/rhombus on M/H) | Fixed |
| `geo_quadrilaterals_area_of_triangles_and_quadrilaterals` | 40 each | Pass | Named area formulas | Yes | Fixed |
| `pa_quadrilaterals` | 40 each | Pass | Quad area mix | Yes | Fixed |
| `geo_quadrilaterals_rhombuses` | 40 each | Pass | Rhombus base×height | n/a | Fixed wiring |
| `geo_quadrilaterals_classifying` | 40 each | Pass | Classify named quads | n/a | Expanded |
| `g6_parallelograms` / `g6_trapezoids` / `g6_kites` | 40 each | Pass | Dedicated | n/a | Unchanged (correct) |

## Evidence (n=40 / tier)

### Combined triangle + quad area
`pa_area_of_triangles_and_quadrilaterals`
- easy: Δ17 · □11 · ▭5 · ▱7
- medium: Δ11 · □3 · ▭3 · ◇3 · ▱8 · trap4 · kite8
- hard: Δ9 · □2 · ▭4 · ◇3 · ▱7 · trap9 · kite6

`geo_quadrilaterals_area_of_triangles_and_quadrilaterals` similarly mixes all seven families on medium/hard.

### Within-quad (`pa_quadrilaterals`)
- easy: □11 · ▭15 · ▱14
- medium/hard: all of square, rectangle, parallelogram, rhombus, trapezoid, kite

### Dedicated (stay single-shape)
- `geo_quadrilaterals_rhombuses` → 100% rhombus (was parallelogram prompt)
- `g6_parallelograms` / `g6_trapezoids` / `g6_kites` → named shape only

## Fixes
- New frameworks: square, rectangle, rhombus (+ `rhombus_figure`)
- Expanded `geo_triangles_and_quadrilaterals_area` mix
- New `geo_quadrilateral_area` for `pa_quadrilaterals`
- `geo_rhombus_area` for rhombus types; classifying includes square + kite
- Grid polygons include squares in the shape pool
