# Grade 6 effort-based difficulty specs — batch 2

**Branch:** `experiment/difficulty-slider`  
**Date:** 2026-07-27  
**Batch:** ordered Ready G6 minus SKIP (first 11 ratio/percent topics), indices **[20, 30)**  
**Verification:** live `_generate_for_type` (presets applied) → `scripts/output/topic_fit/g6_difficulty/batch_2_verification.json` (n=40 per D ∈ {0,5,10,15,20,25})

## Design principle (shared)

Difficulty is **effort / meaningful steps**, not raw magnitude.

- Continuous `difficulty` (slider) remains the generator prior; sampling maps D → **effort targets**.
- **Mode / structure splits** matter: task type, closeness, nest depth, property class — not “bigger integers.”
- Place-value / grid-span alone does **not** count as high effort when the skill is unchanged.

### Effort scale anchors

| D | Meaning |
|---|---|
| 0 | Very easy / minimal time |
| 5 | Standard simple |
| 10 | More involved / maybe extra trick |
| 15 | Clearly more work |
| 20 | Hard / awkward extras |
| 25 | Mean-to-assign-five-examples level |

### Batch topic order (indices 20–29 after SKIP)

20. `g6_ordering_with_absolute_values`  
21. `g6_points_on_the_coordinate_plane`  
22. `g6_distances_on_the_coordinate_plane`  
23. `g6_shapes_and_perimeter_on_the_coordinate_plane`  
24. `g6_coordinate_plane_distances_word_problems`  
25. `g6_writing_numeric_expressions`  
26. `g6_numeric_expressions_with_exponents`  
27. `g6_properties_of_addition_and_multiplication`  
28. `g6_numeric_expressions_and_order_of_operations`  
29. `g6_distributive_property_numeric`

### Status summary

| Status | Count |
|--------|------:|
| verified_ramp | 4 |
| weak_ramp | 2 |
| failed_ramp | 4 |
| blocked | 0 |

---

## 20. `g6_ordering_with_absolute_values` — Ordering with absolute values

**Generator:** `AbsoluteValueFramework(mode="order")` via `g6_ordering_with_absolute_values`  
**Profile:** `integer` + continuous `difficulty`

### What increases difficulty
- **Set size:** 3 → 4 → 5 values (D thresholds ≈8 / 16)
- **Sign mix:** negatives forced at D≥5 so |·| is required
- **Closeness of absolute values** (primary): far gaps at low D; near-ties at high D
- Modest magnitude growth only as a side effect of packing gaps

### What does NOT count
- Huge magnitudes with large, obvious |·| gaps
- Ordering by signed value instead of absolute value (wrong skill)

### Continuous D → effort
`_sample_abs_order_values(d)`: count from D; `_abs_separation` shrinks gaps; `_abs_apply_sign` mixes signs.

### Anchors
- **5:** 3 values, ≥1 negative, still readable gaps  
- **15:** 4 values, mixed signs, tighter |·| gaps  
- **25:** 5 values, near-ties on absolute values

### Verification
**verified_ramp.** Means: 4.3 → 7.5 → 14.9 → 15.1 → 21.1 → 21.3.

---

## 21. `g6_points_on_the_coordinate_plane` — Points on the coordinate plane

**Generator:** `plotting_points` (graphing adapter; blank plane + plot given coordinate)  
**Profile:** `coordinate_plane`

### What increases difficulty (spec / intended)
- Axis / origin → Q1 → other quadrants  
- Read denser grids only as a minor secondary  
- Optional later: name-the-point from a marked graph (inverse task) at high D

### What does NOT count
- Larger |x|,|y| alone on the same “plot this ordered pair” skill  
- Non-integer coordinates at G6 (not this topic)

### Continuous D map (current)
EMH presets grow `coord_min`/`coord_max` (−5…5 → −8…8 → −12…12). No task-mode ladder.

### Anchors (intended)
- **5:** mostly Q1 / axis-adjacent small ints  
- **15:** mixed quadrants on mid grid  
- **25:** all quadrants; optional identify-from-graph

### Verification
**weak_ramp.** Means: 7.2 → 7.3 → 8.1 → 9.0 → 8.1 → 8.9. Coord-range only; structure flat.

---

## 22. `g6_distances_on_the_coordinate_plane` — Distances on the coordinate plane

**Generator:** `geo_coordinate_distance` → `CoordinateDistanceFramework`  
**Profile:** `coordinate_geometry`

### What increases difficulty (spec / intended)
- Same-axis short segments → longer spans / cross-origin  
- Same row/column with one endpoint on an axis  
- **Not** diagonal Pythagorean at G6 (axis-aligned skill)

### What does NOT count
- Diagonal √(dx²+dy²) “because hard” (wrong grade skill for this leaf)  
- Larger coord box with the same |Δx| or |Δy|

### Continuous D map (current)
Presets keep `axis_aligned_only=True` at **all** bands; only `coord_min`/`coord_max` grow (−5…5 → −10…10). No continuous effort targeting of span / origin-crossing.

### Anchors (intended)
- **5:** short axis-aligned, same quadrant  
- **15:** longer spans; often cross an axis  
- **25:** awkward multi-quadrant same-row/column

### Verification
**failed_ramp.** Means: 6.2 → 6.6 → 6.3 → 7.5 → 6.8 → 6.6. Always axis-aligned (good), but effort flat (magnitude-only coords).

---

## 23. `g6_shapes_and_perimeter_on_the_coordinate_plane` — Shapes and perimeter

**Generator:** `g6_coordinate_perimeter` → `CoordinatePerimeterFramework`  
**Profile:** `coordinate_geometry` (defaults: `allow_l_shape=False`, `coord_min=0`, `coord_max=8`)

### What increases difficulty (spec / intended)
- Axis-aligned **rectangle** → **L-shaped** 6-vertex polygon  
- Counting more sides / subtracting a cut  
- Negative / Q2–Q3 placements as secondary

### What does NOT count
- Larger rectangle sides alone  
- Diagonal sides (framework is axis-aligned only)

### Continuous D map (broken)
EMH presets set `allow_l_shape=True` at medium/hard, but `setting_defaults.allow_l_shape=False` wins in `_resolve_generation_settings` → presets never unlock L-shapes. Coord span also stuck at defaults (0…8).

### Anchors (intended)
- **5:** small rectangles  
- **15:** mix rectangles + L  
- **25:** L-shapes dominant; larger outer spans

### Verification
**failed_ramp.** Means: 6.0 flat. 0/240 L-shapes across all D.

---

## 24. `g6_coordinate_plane_distances_word_problems` — Distances, word problems

**Generator:** `wp_coordinate_distance` → `CoordinateDistanceWordFramework`  
**Profile:** `word_problem`

### What increases difficulty (spec / intended)
- Story + **axis-aligned** distance first (match topic 22)  
- Then longer spans / cross-origin  
- Optional: multi-leg path perimeter on a grid at high D  
- Keep integer answers for G6

### What does NOT count
- Always-on diagonal Pythagorean with opaque decimal/integer hypotenuses  
- Ignoring continuous D entirely

### Continuous D map (current)
Framework samples fixed `dx,dy ∈ [3,8]` and **never reads** `difficulty`. Resolved settings only carry word-problem term knobs.

### Anchors (intended)
- **5:** axis-aligned “how far on the map”  
- **15:** longer axis-aligned / cross axes  
- **25:** two-segment path or near-miss same-row distractors

### Verification
**failed_ramp.** Means: 17.6 → 17.7 → 17.7 → 17.4 → 17.3 → 17.5 (flat high — always diagonal).

---

## 25. `g6_writing_numeric_expressions` — Writing numeric expressions

**Generator:** `writing_numeric_expressions` (`advanced._writing_numeric_expressions`)  
**Profile:** `writing_numeric_expressions`

### What increases difficulty
- Phrase complexity: one-op (“more than”) → sum/product nesting → **exponents in words** (“squared/cubed”)  
- Parentheses required in the written expression  
- EMH presets map continuous D → `expression_complexity` simple/standard/advanced

### What does NOT count
- Larger operands alone (`18 times 18` is not harder than `3 times 4` for this skill)

### Continuous D map
| D band | Preset |
|--------|--------|
| ≤4 | `simple` |
| ≤11 | `standard` |
| ≥12 | `advanced` (exponents / nested quantity language) |

### Anchors
- **5:** “times the sum of …”  
- **15:** squared/cubed phrases  
- **25:** nested product-of-sum with square

### Verification
**verified_ramp.** Means: 4.0 → 7.5 → 7.5 → 13.4 → 14.1 → 13.0 (high-D plateau on advanced bank).

---

## 26. `g6_numeric_expressions_with_exponents` — Numeric expressions with exponents

**Generator:** `primitive_g6.numeric_expressions_with_exponents` → OOO primitive with `require_exponents=True`  
**Profile:** `order_of_operations`

### What increases difficulty
- Shared expression-structure DNA: leaf count, nest budget, ×/÷ unlocks  
- Always ≥1 exponent; more exponents / paren nests at higher D  
- Longer op chains (not bigger bases alone)

### What does NOT count
- Huge bases without structural growth (`99²` as a one-op item)

### Continuous D map
`sample_ooo_expression` via `target_n_leaves` / nest / scale budgets; exponents forced.

### Anchors
- **5:** short `a^b × c − d`  
- **15:** multi-op with parens + exponents  
- **25:** long chains; multiple exponents / deep nests

### Verification
**verified_ramp.** Means: 12.6 → 15.2 → 23.5 → 25 → 25 → 25 (saturates mid-high by design).

---

## 27. `g6_properties_of_addition_and_multiplication` — Properties of + / ×

**Generator:** `IdentifyPropertyFramework`  
**Profile:** `integer` (MC among property names)

### What increases difficulty (spec / intended)
- Property class: identity/zero/commutative → **associative** → **distributive** (incl. subtract form)  
- Bias the pool toward harder properties as D rises (not uniform after unlock)  
- Milder: larger ints / both expand directions for distributive

### What does NOT count
- Bigger numbers on an identity example (`0 + 99 = 99`)  
- Random easy identities at D=25

### Continuous D map (current)
`_difficulty_band`: easy (D≤4) excludes associative/distributive; medium+ uses full pool **uniformly**. No progressive hard bias.

### Anchors (intended)
- **5:** commutative / identity still common; distributive unlocked  
- **15:** associative + distributive majority  
- **25:** distributive / associative-only bank

### Verification
**weak_ramp.** Means: 4.4 → 8.3 → 6.6 → 8.6 → 8.8 → 6.6. Easy→full unlock at D≈5 only; hard-prop rate at D=25 still ~23%.

---

## 28. `g6_numeric_expressions_and_order_of_operations` — Numeric expressions & OOO

**Generator:** `primitive_g6.order_of_operations`  
**Profile:** `order_of_operations`

### What increases difficulty
- Same structure engine as topic 26 without forced exponents  
- Ops unlock: +/− → × → ÷ wrappers; exponents appear when D unlocks them  
- Nest depth / leaf count from continuous D

### What does NOT count
- Magnitude-only with a fixed 2-op skeleton

### Continuous D map
`expression_structure` leaf/nest/scale budgets; optional exponents at higher D.

### Anchors
- **5:** short ×/− chains  
- **15:** parens + early exponents  
- **25:** long nested mixed ops

### Verification
**verified_ramp.** Means: 5.8 → 9.6 → 17.8 → 24.9 → 25 → 25.

---

## 29. `g6_distributive_property_numeric` — Distributive property, numeric

**Generator:** `primitive_g6.distributive_property` → `sample_distributive_numeric`  
**Profile:** `distributive` (G6 presets: `allow_negative=False`, growing `coef_max`)

### What increases difficulty (spec / intended for G6)
- Outer·(a+b) → three inner terms → awkward integer coefficients  
- Expand either direction; keep **positive integers** for G6  
- Structure upgrades via distributive difficulty factors — **not** fraction/decimal lanes

### What does NOT count
- Negatives / fractions / decimals as “hard G6 distributive” (wrong number profile; presets say `allow_negative=False` but primitive number lane ignores them)
- Larger integers alone with two easy terms

### Continuous D map (current)
Primitive upgrades add terms and unlock number-lane complexity (neg/frac/dec). G6 EMH presets are ignored by the primitive path.

### Anchors (intended)
- **5:** small positive `k(a+b)`  
- **15:** three positive integer inners  
- **25:** awkward positive composites; still integer

### Verification
**failed_ramp** (wrong effort drivers). Means rise 4.9 → 15.1, but D=0 already has negatives (~30%) and mid/high D floods fractions/decimals — not G6 effort.

---

## Implementation map (batch 2)

| Piece | Location / note |
|-------|-----------------|
| Abs order closeness ladder | `AbsoluteValueFramework` / `_sample_abs_order_values` in `frameworks/number.py` |
| Points / distances / perimeter | `plotting_points`, `CoordinateDistanceFramework`, `CoordinatePerimeterFramework` |
| Perimeter L unlock blocked | `generator_profiles` defaults override EMH `allow_l_shape` |
| WP distances ignore D | `CoordinateDistanceWordFramework.build_prompt` |
| Writing phrases | `generators/advanced.py` + EMH complexity presets |
| OOO / exponents / distributive | `generators/primitive_g6.py` + expression-structure / distributive primitives |
| Properties pool | `IdentifyPropertyFramework._build_example` band gate only |
| Verify artifact | `scripts/output/topic_fit/g6_difficulty/batch_2_verification.json` |

## How to re-verify

```powershell
$env:PYTHONPATH='.'; $env:QE_LOG_GENERATED='0'
# Prefer live path (presets applied), same as batch_2_verification.json
python -c "from question_engine.api.handler import _generate_for_type; ..."
```

Fix priorities implied by statuses: perimeter defaults vs presets; WP distance continuous map; distances span targeting; G6 distributive number-lane clamp; properties hard-pool bias; points task-mode ladder.
