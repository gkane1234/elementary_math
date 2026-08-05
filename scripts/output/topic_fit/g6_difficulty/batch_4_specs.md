# Grade 6 effort-based difficulty — batch 4

**Branch:** `experiment/difficulty-slider`  
**Date:** 2026-07-27  
**Slice:** ordered Ready G6 minus first-11 SKIP, indices **[40, 50)**  
**Verification:** `scripts/verify_g6_effort_difficulty_batch4.py` → `batch_4_verification.json` (n=40 per D ∈ {0,5,10,15,20,25})

## Design principle (shared)

Difficulty is **effort / meaningful steps**, not raw magnitude.

- Continuous `difficulty` remains the generator prior; sampling maps D → **effort targets**.
- Place-value ÷10ⁿ cancels stay “free” where GCD/inflate applies (proportions).
- Mode splits matter: write-as-given / formula-understanding tasks must not fake high D with bigger numbers alone.

### Effort scale anchors

| D | Meaning |
|---|---|
| 0 | Very easy / minimal time |
| 5 | Standard simple |
| 10 | More involved / maybe extra trick |
| 15 | Clearly more work |
| 20 | Hard / awkward extras |
| 25 | Mean-to-assign-five-examples level |

### Batch topics

| # | type_id |
|---|---------|
| 40 | `g6_writing_and_graphing_inequalities` |
| 41 | `g6_inequalities_word_problems` |
| 42 | `g6_solving_and_graphing_one_step_inequalities` |
| 43 | `g6_inequalities_hanger_diagrams` |
| 44 | `g6_equivalent_ratio_equations` |
| 45 | `g6_constant_rate_equations` |
| 46 | `g6_equations_for_other_relationships` |
| 47 | `g6_parallelograms_understanding_area_formula` |
| 48 | `g6_parallelograms` |
| 49 | `g6_triangles_understanding_area_formula` |

---

## 1. `g6_writing_and_graphing_inequalities`

**Generator:** `GraphInequalityFramework` (`graph_single_variable_inequality`, number-line)

### What increases difficulty
- Inclusive symbols (`≤`/`≥`) vs strict
- Negative / zero / awkward non-benchmark boundaries
- **Write-from-words then graph** (“at least / at most / greater than”)
- Half-integer boundaries at high D

### What does NOT count
- Larger |boundary| alone on an already-given `x > 3`
- Coordinate-plane half-planes (wrong skill for this G6 leaf)

### Mode split
| D | Spec |
|---|------|
| &lt;8 | Graph given symbolic inequality |
| 8–18 | Rising P(write-from-words) |
| ≥18 | Always write-from-words; awkward / half-integer marks |

### Anchors
- **5:** small positive, often strict
- **15:** words + awkward integer
- **25:** words + half-integer / inclusive

### Verification
**Ramp verified.** Means: 3.0 → 5.6 → 10.2 → 13.5 → 16.0 → 16.9.

---

## 2. `g6_inequalities_word_problems`

**Generator:** `wp_inequality` → real story templates (replaced equation-stub WP)

### What increases difficulty
- Compare-only (“score at least k”) → one-step translate → two-step shopping → strict rental with larger coeffs

### What does NOT count
- “Name needs a quantity satisfying `2x+3<6`” stubs (removed)

### Continuous D map
| D | Mode |
|---|------|
| &lt;5 | Compare / write inequality |
| 5–12 | One-step “already has / needs at least” |
| 12–18 | Two-step cost story |
| ≥18 | Strict two-step rental |

### Anchors
- **5:** one-step translate
- **15:** notebooks two-step
- **25:** bike rental strict

### Verification
**Ramp verified.** Means: 4 → 9 → 9 → 14 → 18 → 18.

---

## 3. `g6_solving_and_graphing_one_step_inequalities`

**Generator:** primitive `one_step_inequalities` (+ number-line metadata)

### What increases difficulty
- Add/sub → mul/div forced at higher effective D
- Negative coefficients (direction flip) more often at D≳14
- Modestly larger |coeff| at D≳18
- Non-strict symbols

### What does NOT count
- Purchased upgrades that still render as `x−1≤−1` (sampling tightened to prefer mul/div)

### Anchors
- **5:** mix; some ÷/×
- **15:** mostly mul/div; some flips
- **25:** flips + larger coeffs

### Verification
**Ramp verified.** Means: 4.0 → 6.8 → 9.6 → 10.0 → 12.4 → 11.8 (mild high-D plateau on structure mix).

---

## 4. `g6_inequalities_hanger_diagrams`

**Generator:** visual hanger (`inequality_hanger`)

### What increases difficulty
- More equal parts / larger solution
- `≤` → mix `≥` at mid/high D
- Composite part counts (6,8,9,12) at high D

### What does NOT count
- Same `2x≤24` with only larger totals that stay 2-part

### Anchors
- **5:** 2–4 parts
- **15:** 3–6 parts, inclusive mix
- **25:** large composite parts

### Verification
**Ramp verified.** Means: 5.8 → 7.6 → 12.4 → 12.0 → 16.5 → 20.2.

---

## 5. `g6_equivalent_ratio_equations`

**Generator:** primitive `solving_proportions` / `sample_proportion`

### What increases difficulty
- Meaningful inflate-k (Ω after stripping ÷10ⁿ) on proportion parts
- Variable-in-denominator forms
- Multi-step clear `(x±d)` forms (no longer shadowed by denom-var)
- Larger composite surfaces

### What does NOT count
- Tiny `1/2 = x/2` at high D
- Pure place-value inflate as “hard”

### Anchors
- **5:** small inflate + often denom-var
- **15:** multi-step clear + meaningful cancel
- **25:** large composites

### Verification
**Ramp verified.** Means: 4.0 → 9.4 → 16.9 → 20.4 → 22.3 → 21.4.

---

## 6. `g6_constant_rate_equations`

**Generator:** `write_one_step_equation` (constant-rate branch)

### What increases difficulty
- Find distance → find time → find rate
- Awkward non-nice rates at high D

### What does NOT count
- Only larger mph×hours with the same “find d” stem

### Continuous D map
| D | Modes |
|---|-------|
| &lt;5 | find distance, small |
| 5–12 | distance / occasional time |
| 12–18 | time mix |
| ≥18 | distance / time / rate + awkward rates |

### Anchors
- **5:** small rate×time
- **15:** find time mix
- **25:** find rate / awkward rates

### Verification
**Ramp verified.** Means: 4.2 → 8.0 → 7.5 → 10.4 → 12.0 → 12.1.

---

## 7. `g6_equations_for_other_relationships`

**Generator:** same `write_one_step_equation`, **other-relationship** branch (topic-gated)

### What increases difficulty
- Cost → tickets → perimeter → **invert** (P→s, total→qty)
- Awkward prices at high D

### What does NOT count
- Reusing the bike rate stem (wrong topic)

### Continuous D map
| D | Pool |
|---|------|
| &lt;5 | cost only |
| 5–10 | cost / tickets |
| 10–16 | tickets / perimeter / cost |
| ≥16 | perimeter / invert cost / tickets |

### Anchors
- **5:** simple cost
- **15:** perimeter invert mix
- **25:** invert cost / large perimeter

### Verification
**Ramp verified.** Means: 5.5 → 6.0 → 9.5 → 10.7 → 15.7 → 14.3.

---

## 8. `g6_parallelograms_understanding_area_formula`

**Generator:** `ParallelogramAreaFramework` with `_topic_id` understanding mode

### What increases difficulty
- Continuous side bounds (shared area helper)
- Rising P(missing base/height given area) — formula inversion
- Half-ish products less relevant (integer area); size still mild

### What does NOT count
- Only larger base×height with “find area” at high D on this leaf

### Mode split
| D | missing-dim P |
|---|---------------|
| &lt;5 | ~15% |
| 5–12 | ~45% |
| 12–18 | ~70% |
| ≥18 | ~90% |

### Anchors
- **5:** mostly find area, small sides
- **15:** often missing height/base
- **25:** almost always invert

### Verification
**Ramp verified.** Means: 6.7 → 9.2 → 9.9 → 13.4 → 15.5 → 15.9.

---

## 9. `g6_parallelograms`

**Generator:** same framework, **find-area** dominant (no understanding mode)

### What increases difficulty
- Continuous `_area_side_bounds` / half-product sampling via shared pair helper
- Larger classroom-readable sides as D rises

### What does NOT count
- Missing-dimension inversions (those belong on the understanding leaf)

### Anchors
- **5:** sides ~3–12
- **15:** mid continuous band
- **25:** upper continuous band (~≤36)

### Verification
**Ramp verified (structure-led).** Means: 5.0 → 5.7 → 7.0 → 7.7 → 8.6 → 10.0.

---

## 10. `g6_triangles_understanding_area_formula`

**Generator:** `TriangleAreaFramework`

### What increases difficulty
- Layout: right → interior altitude → exterior altitude (continuous D weights)
- Half-integer areas (odd bh)
- Rising P(missing base/height) on understanding leaf
- Continuous side bounds

### What does NOT count
- Bigger legs on a right triangle alone without layout / invert shift

### Anchors
- **5:** mostly right; some missing
- **15:** interior/exterior + invert mix
- **25:** exterior-heavy + invert

### Verification
**Ramp verified.** Means: 6.9 → 9.6 → 13.0 → 17.2 → 19.4 → 20.0.

---

## Implementation map

| Piece | Location |
|-------|----------|
| Topic id on settings | `QuestionFramework.generate_batch` → `_topic_id` |
| Write/graph inequalities | `frameworks/graphing.py` |
| Inequality WP stories | `frameworks/primitives/word_problems.py` |
| One-step ineq mul/div force | `frameworks/primitives/inequalities.py` |
| Hanger relation mix | `frameworks/number.py` (inequality_hanger) |
| Proportion meaningful inflate | `frameworks/primitives/proportions.py` |
| Constant rate / other relationships | `generators/grade_level.py` |
| Parallelogram understand / area | `frameworks/geometry_extended.py` |
| Triangle understand / layout | `frameworks/geometry.py` |
| Verify | `scripts/verify_g6_effort_difficulty_batch4.py` |

## How to re-verify

```powershell
$env:PYTHONPATH='.'; $env:QE_LOG_GENERATED='0'
python scripts/verify_g6_effort_difficulty_batch4.py
```

## Status summary

| Status | Count |
|--------|------:|
| verified_ramp | 10 |
| weak_ramp | 0 |
| failed_ramp | 0 |
| blocked | 0 |
