# Grade 6 effort-based difficulty — batch 5

**Branch:** `experiment/difficulty-slider`  
**Date:** 2026-07-27  
**Scope:** Ordered Ready G6 minus first-11 SKIP, indices **[50, 60)**  
**Verification:** `scripts/verify_g6_batch5_effort.py` → `batch_5_verification.json` (n=40 per D ∈ {0,5,10,15,20,25})

## Design principle (shared)

Difficulty is **effort / meaningful steps**, not raw magnitude.

- Area formulas: **half-integer results** (odd products / odd \((b_1+b_2)h\)) count as real arithmetic work; place-value-only “bigger cm” does not.
- Diagram reading: right-triangle altitude → interior altitude → **exterior** altitude; grid shape family → L / irregular.
- Solid naming: familiar cube/rect prism → triangular prism / pyramids.
- Fraction sides: denom awkwardness + improper + cross-cancel; triangle adds ÷2.
- Continuous `difficulty` remains the generator prior; sampling maps D → **effort targets**.

### Effort scale anchors

| D | Meaning |
|---|---|
| 0 | Very easy / minimal time |
| 5 | Standard simple |
| 10 | More involved / maybe extra trick |
| 15 | Clearly more work |
| 20 | Hard / awkward extras |
| 25 | Mean-to-assign-five-examples level |

### This batch (curriculum order)

50. `g6_triangles`  
51. `g6_trapezoids`  
52. `g6_kites`  
53. `g6_polygons_on_a_grid_or_coordinate_plane`  
54. `g6_polygons_and_shaded_regions`  
55. `g6_classifying_and_naming`  
56. `g6_volume_and_surface_area_using_isometric_drawings`  
57. `g6_formulas_for_volume_and_surface_area_of_a_cube`  
58. `g6_rectangles_with_fraction_side_lengths`  
59. `g6_triangles_with_fraction_side_lengths`

---

## 1. `g6_triangles` — Triangles

**Generator:** `TriangleAreaFramework` (`geo_triangle_area`)  
**Profile:** `geometry_triangles` + continuous `difficulty`

### What increases difficulty
- **Altitude layout:** right (legs as base/height) → interior altitude → exterior altitude to a base extension
- Half-area when \(bh\) is odd
- Modest side growth (secondary)

### What does NOT count
- Huge sides alone with a right-triangle layout
- Treating continuous D as an EMH string (layout now uses `settings_difficulty`)

### Continuous D → layout
| D | Mix |
|---|-----|
| &lt;4 | ~92% right |
| &lt;8 | right + light interior |
| &lt;13 | interior-heavy |
| &lt;18 | exterior rises |
| ≥18 | exterior preferred |

### Anchors
- **5:** mostly right, integer area
- **15:** interior / early exterior + half areas
- **25:** exterior altitude + half-integer areas

### Verification
**Ramp verified.** Means: 5.2 → 7.7 → 11.1 → 16.5 → 19.6 → 19.5.

---

## 2. `g6_trapezoids` — Trapezoids

**Generator:** `TrapezoidAreaFramework` (`geo_trapezoid_area`)

### What increases difficulty
- Base gap (close bases → clearly different \(b_1,b_2\)) — more add-then-average work
- Half-area when \((b_1+b_2)h\) is odd
- Modest dimension growth (secondary)

### What does NOT count
- Only inflating all three lengths while keeping \(b_1\approx b_2\) and even products

### Continuous D map
| D | Spec |
|---|------|
| &lt;5 | close bases; rare half |
| &lt;12 | moderate gap; ~half mix |
| ≥12 | forced min gap; high half rate |

### Anchors
- **5:** near-equal bases, integer area
- **15:** clear base gap + half
- **25:** large gap + half almost always

### Verification
**Ramp verified.** Means: 5.8 → 7.4 → 9.0 → 12.7 → 15.9 → 16.1.

---

## 3. `g6_kites` — Kites

**Generator:** `KiteAreaFramework` (`geo_kite_area`)

### What increases difficulty
- Half-area when \(d_1 d_2\) is odd
- Unequal diagonals (reading the kite diagram)
- Modest diagonal growth (secondary)

### What does NOT count
- Equal-ish diagonals with only larger numbers

### Anchors
- **5:** small diagonals, integer area
- **15:** half-area + unequal diagonals
- **25:** high half rate

### Verification
**Ramp verified.** Means: 5.8 → 7.8 → 9.5 → 11.5 → 13.5 → 13.1 (high-D plateau on half/gap, not magnitude).

---

## 4. `g6_polygons_on_a_grid_or_coordinate_plane` — Polygons on a grid

**Generator:** `Grade6VisualFramework("grid_polygon")` (`g6_polygon_grid_area`)

### What increases difficulty
- Shape family: square/rect → triangle/parallelogram → trapezoid → **L-shape / irregular**
- Half-square-unit areas (odd shoelace double) at mid/high D

### What does NOT count
- Same rectangle with a larger bounding box on the fixed 8×5 grid

### Continuous D → shape pool
| D | Pool bias |
|---|-----------|
| &lt;4 | square / rectangle / triangle |
| &lt;8 | + parallelogram |
| &lt;13 | + trapezoid |
| &lt;18 | + L / irregular |
| ≥18 | L / irregular / trapezoid heavy |

### Anchors
- **5:** axis-aligned rect/triangle
- **15:** trapezoid / early L
- **25:** L-shape / irregular quads

### Verification
**Ramp verified.** Means: 4.5 → 5.8 → 9.6 → 12.2 → 12.9 → 11.8.

---

## 5. `g6_polygons_and_shaded_regions` — Polygons and shaded regions

**Generator:** `Grade6VisualFramework("shaded_polygon")` (`g6_shaded_polygon_area`)

Same effort ladder as grid polygons (shaded fill is presentation; counting strategy is the skill).

### Verification
**Ramp verified.** Means: 4.3 → 7.0 → 9.0 → 11.2 → 13.2 → 13.1.

---

## 6. `g6_classifying_and_naming` — Classifying and naming

**Generator:** `Grade6VisualFramework("classify_polyhedron")` (`g6_classify_polyhedron`)

### What increases difficulty
- Solid pool: cube / rectangular prism → triangular prism / square pyramid → **triangular pyramid**
- High D excludes the most familiar cube

### What does NOT count
- Harder MC distractors alone without changing the target solid family
- Random uniform over all five kinds at every D

### Continuous D → pool
| D | Pool |
|---|------|
| &lt;5 | cube, rectangular prism |
| &lt;10 | + triangular prism, square pyramid |
| &lt;16 | drop cube; include triangular pyramid |
| ≥16 | triangular prism / pyramids only |

### Anchors
- **5:** cube or rectangular prism
- **15:** mix including triangular pyramid
- **25:** non-cube only

### Verification
**Ramp verified.** Means: 4.0 → 8.9 → 11.5 → 13.3 → 14.8 → 14.8.

---

## 7. `g6_volume_and_surface_area_using_isometric_drawings` — Isometric measure

**Generator:** `Grade6VisualFramework("isometric_measure")` (`g6_isometric_measure`)

### What increases difficulty
- Ask type: **volume** (count unit cubes) → **surface area** (careful face count)
- Near-cube dims → elongated spans (harder to read from the drawing)
- Modest dimension growth within SVG-readable range

### What does NOT count
- Asking volume on a 2×2×2 forever while only growing labels in text

### Continuous D map
| D | Spec |
|---|------|
| &lt;5 | dims 2–3, near-cube, ~80% volume |
| &lt;10 | dims 2–4, ~55% volume |
| &lt;16 | dims 3–5, elongated, ~35% volume |
| ≥16 | dims 3–6, elongated, ~22% volume |

### Anchors
- **5:** small near-cube, volume
- **15:** elongated + SA mix
- **25:** SA-heavy elongated prisms

### Verification
**Ramp verified.** Means: 10.4 → 12.3 → 15.2 → 16.4 → 18.4 → 19.2.

---

## 8. `g6_formulas_for_volume_and_surface_area_of_a_cube` — Cube formulas

**Generator:** `SolidVolumeSurfaceFramework` (`geo_solid_volume_surface`)  
**Wiring:** type setting_defaults `solid_shapes: ["cube"]` (was leaking prism/cylinder)

### What increases difficulty
- Unknown: volume \(s^3\) → surface area \(6s^2\)
- Side length multi-digit arithmetic
- Continuous side bounds (classroom-sized)

### What does NOT count
- Rectangular prism or cylinder prompts under this type_id
- Only “bigger side” with volume forever

### Mode split
| D | Bias |
|---|------|
| &lt;5 | ~80% volume |
| &lt;12 | ~55% volume |
| ≥18 | ~30% volume (SA-heavy) |

### Anchors
- **5:** small cube volume
- **15:** SA mix, mid sides
- **25:** SA + larger sides

### Verification
**Ramp verified.** Means: 7.2 → 8.9 → 9.6 → 11.9 → 13.8 → 14.9. Cube-only integrity checked.

---

## 9. `g6_rectangles_with_fraction_side_lengths` — Fraction rectangles

**Generator:** `Grade6VisualFramework("fraction_rectangle")`

### What increases difficulty
- Denom banks: halves/quarters → thirds/fifths → sixths/eighths → tenths/twelfths
- Improper / mixed-style lengths
- Cross-cancel between factors at high D

### What does NOT count
- Same \(\tfrac12\times\tfrac12\) with only unit changes
- Integer×integer disguised as “fraction” topic

### Continuous D map
Uses shared `_fraction_side_for_difficulty` / `_fraction_pair_for_difficulty` (cancel bias ≥12).

### Anchors
- **5:** unit / halves-quarters
- **15:** awkward denoms + cancel
- **25:** tenths/twelfths + improper

### Verification
**Ramp verified.** Means: 8.6 → 8.9 → 10.7 → 16.1 → 16.4 → 16.6.

---

## 10. `g6_triangles_with_fraction_side_lengths` — Fraction triangles

**Generator:** `Grade6VisualFramework("fraction_triangle")`

Same fraction-side ladder as rectangles, plus the **÷2** for triangle area.

### Anchors
- **5:** simple fractions + ÷2
- **15:** awkward denoms + ÷2 + cancel
- **25:** hard denoms + improper + ÷2

### Verification
**Ramp verified.** Means: 11.9 → 12.6 → 12.8 → 19.1 → 19.5 → 19.4.

---

## Implementation map (code)

| Piece | Location |
|-------|----------|
| Continuous layout + half-area sides | `frameworks/geometry.py` (`_triangle_area_layout`, `_sample_pair_for_half`, `_area_side_bounds`) |
| Trapezoid / kite / cube solids | `frameworks/geometry_extended.py` |
| Grid shapes, classify pool, isometric, fraction pairs | `frameworks/number.py` |
| Continuous D on geometry profile | `settings/profiles.py` `geometry_basic_profile` |
| Cube-only + G6 type aliases | `settings/generator_profiles.py` |
| Verify | `scripts/verify_g6_batch5_effort.py` |

## How to re-verify

```powershell
$env:PYTHONPATH='.'; $env:QE_LOG_GENERATED='0'
python scripts/verify_g6_batch5_effort.py
```

Raw means: `scripts/output/topic_fit/g6_difficulty/batch_5_verification.json`.
