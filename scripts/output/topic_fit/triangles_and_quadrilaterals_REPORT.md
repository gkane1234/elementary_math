# Topic-fit: Area of triangles and quadrilaterals

| Type | E/M/H samples | Topic? | Method? | Hard harder? | Status |
|------|---------------|--------|---------|--------------|--------|
| `pa_area_of_triangles_and_quadrilaterals` | 40 each | Pass (after fix) | Area formulas | Yes (trap + harder tri layouts) | Fixed |
| `geo_quadrilaterals_area_of_triangles_and_quadrilaterals` | 40 each | Pass (after fix) | Area formulas | Yes | Fixed |

## Scope checked

**Combined (must mix):**
- `pa_area_of_triangles_and_quadrilaterals`
- `geo_quadrilaterals_area_of_triangles_and_quadrilaterals`

**Related (correctly single-family — no change):**
- `pa_plane_figures_triangles` → 100% triangle
- `pa_quadrilaterals` → 100% parallelogram
- `g6_triangles` → 100% triangle
- `g6_parallelograms` / `g6_trapezoids` → dedicated quads
- No Grade 6 type named “triangles and quadrilaterals”

## Before

Both combined types wired to `geo_triangle_area` → **120/120 triangles** (0% quads).

## After

New generator `geo_triangles_and_quadrilaterals_area` (weighted mix):

| Tier | Mix |
|------|-----|
| Easy | triangle 55%, parallelogram 45% |
| Medium | triangle 40%, parallelogram 35%, trapezoid 25% |
| Hard | triangle 35%, parallelogram 30%, trapezoid 35% |

Empirical (n=40/tier):

| Type | Triangle | Parallelogram | Trapezoid |
|------|----------|---------------|-----------|
| `pa_…` | 41 (34%) | 51 (43%) | 28 (23%) |
| `geo_…` | 53 (44%) | 43 (36%) | 24 (20%) |

Sample prompts: `Find the area of △ABC.` / `Find the area of the parallelogram.` / `Find the area of the trapezoid.`
