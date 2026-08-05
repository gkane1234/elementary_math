# Grade 6 effort-based difficulty — batch 6 specs

**Branch:** `experiment/difficulty-slider`  
**Date:** 2026-07-27  
**Batch:** remaining Ready G6 indices **[60, end]** (7 topics)  
**Verification:** `scripts/verify_g6_batch6_effort.py` → `batch_6_verification.json` (n=40 per D ∈ {0,5,10,15,20,25})

## Design principle (shared)

Difficulty is **effort / meaningful steps**, not raw magnitude.

- Fraction products: awkward denominators, improper sides, and cancel work count; trailing-zero-only convenience does not.
- Data displays: **task mode** (count → compare → mode/mean; median → IQR) drives effort more than bigger numbers alone.
- Drawing: more points / wider sparse support / **drop blank-axis scaffolding** at high D.

### Effort scale anchors

| D | Meaning |
|---|---|
| 0 | Very easy / minimal time |
| 5 | Standard simple |
| 10 | More involved / maybe extra trick |
| 15 | Clearly more work |
| 20 | Hard / awkward extras |
| 25 | Mean-to-assign-five-examples level |

### Batch topics (curriculum Ready order, after SKIP of first 11)

60. `g6_right_rectangular_prisms_with_fraction_side_lengths`
61. `g6_interpreting_dot_plots`
62. `g6_drawing_dot_plots`
63. `g6_interpreting_histograms`
64. `g6_drawing_histograms`
65. `g6_data_center_and_spread`
66. `g6_interpreting_box_plots`

(Nearby not Ready: `g6_drawing_box_plots` — diagram / readiness gap.)

---

## 1. `g6_right_rectangular_prisms_with_fraction_side_lengths` — Prism volume with fraction sides

**Generator:** `Grade6VisualFramework(mode="fraction_prism")` → `g6_fraction_prism_volume`

### What increases difficulty
- **Count of non-integer sides:** 1 → 2 → 3 as D rises
- Awkward denominators (6,8,9,10,12) and improper / mixed-range lengths
- Cross-cancel work when multiplying three fractions

### What does NOT count
- Three large whole-number sides (wrong skill for this leaf)
- Pure place-value “easy” dens that multiply without leftover work as a fake high-D item

### Continuous D map
| D | Spec |
|---|------|
| &lt;5 | 1 fractional side + wholes; dens 2–4 |
| &lt;12 | 2 fractional sides |
| ≥12 | 3 fractional sides; improper more often; dens escalate |

### Anchors
- **5:** e.g. `2 × 1 × 1/3`
- **15:** three fractions with mid dens
- **25:** improper × awkward dens (e.g. `17/6 × …`)

### Verification
**Ramp verified.** Means: 6.8 → 12.6 → 13.7 → 20.8 → 21.3 → 21.9.

---

## 2. `g6_interpreting_dot_plots` — Interpreting dot plots

**Generator:** `DotPlotReadFramework` (`stats_dot_plot_read`)

### What increases difficulty
- Task ladder: **count at value** → total → compare two stacks → mode → mean/median from the plot
- Larger n / more distinct values (more visual search)

### What does NOT count
- Only stretching value_max while still asking “how many at 3?” at D=25

### Mode split
| D | Modes |
|---|-------|
| &lt;5 | count |
| &lt;11 | count / total / compare |
| &lt;17 | compare / mode |
| ≥17 | mode / mean / median |

### Anchors
- **5:** count dots at a value
- **15:** mode / compare stacks
- **25:** mean or median from the listed plot

### Verification
**Ramp verified.** Means: 3.3 → 6.2 → 6.4 → 9.6 → 14.0 → 14.6.

---

## 3. `g6_drawing_dot_plots` — Drawing dot plots

**Generator:** `Grade6VisualFramework(mode="draw_dot_plot")`

### What increases difficulty
- More points, wider / sparser value support (more axis ticks)
- At D≥14: **draw and label your own axis** (blank scaffolding removed unless `include_axis` forced)

### What does NOT count
- Same 6–10 points on 1–12 forever with a pre-drawn axis at high D

### Anchors
- **5:** small clustered set + blank axis
- **15:** larger n, wider span, often own-axis
- **25:** sparse wide support, own axis

### Verification
**Ramp verified.** Means: 8.5 → 11.0 → 14.0 → 19.2 → 21.1 → 21.8.

---

## 4. `g6_interpreting_histograms` — Interpreting histograms

**Generator:** `HistogramReadFramework` (`stats_histogram_read`)

### What increases difficulty
- Task: count in one bin → which bin has most → compare two bins → combined multi-bin span
- Narrower bins / larger data at high D

### What does NOT count
- Always single-bin count with tiny n at high D

### Mode split
| D | Modes |
|---|-------|
| &lt;5 | count_bin |
| &lt;11 | count_bin / most |
| &lt;17 | most / compare |
| ≥17 | compare / span_total |

### Anchors
- **5:** count one interval
- **15:** compare two intervals
- **25:** combined span total

### Verification
**Ramp verified.** Means: 4.4 → 6.6 → 7.1 → 11.3 → 14.3 → 15.5.

---

## 5. `g6_drawing_histograms` — Drawing histograms

**Generator:** `Grade6VisualFramework(mode="draw_histogram")`

### What increases difficulty
- Same drawing ladder as dots, plus **bin width choices** (2 → 3 → 4/5)
- Own-axis scaffolding drop at high D

### Anchors
- **5:** small set, bin width 2, blank axis
- **15:** larger n, mixed bin widths, often own axis
- **25:** sparse wide data, awkward bins, own axis

### Verification
**Ramp verified.** Means: 10.5 → 13.3 → 17.6 → 23.0 → 23.8 → 24.5.

---

## 6. `g6_data_center_and_spread` — Center and spread

**Generator:** `CenterSpreadFramework` (`stats_center_spread`)

### What increases difficulty
- Measure ladder: **range/mode** → median → **mean** (prefer non-integer mean; even-n median at high D)
- Larger data sets from continuous size targets

### What does NOT count
- Asking range on tiny sets at D=25 as “hard”
- Magnitude-only value_max growth without measure shift

### Mode split
| D | Bias |
|---|------|
| &lt;4 | range / mode |
| &lt;8 | mode / median |
| &lt;13 | median / mean |
| ≥13 | mostly mean (+ even-n median) |

### Anchors
- **5:** mode or range on small set
- **15:** mean with non-integer result
- **25:** mean on larger awkward sets

### Verification
**Ramp verified.** Means: 3.6 → 6.2 → 11.0 → 14.9 → 15.6 → 15.7.

---

## 7. `g6_interpreting_box_plots` — Interpreting box plots

**Generator:** `BoxPlotBasicsFramework` (`stats_box_plot_basics`)

### What increases difficulty
- Task: **median** (read) → range → **IQR** → Q1 / Q3 alone
- Larger n for a stabler five-number summary at mid/high D

### What does NOT count
- Only median-read forever at high D

### Mode split
| D | Modes |
|---|-------|
| &lt;5 | median |
| &lt;10 | median / range |
| &lt;16 | range / IQR |
| ≥16 | IQR / Q1 / Q3 |

### Anchors
- **5:** read median
- **15:** IQR
- **25:** IQR or quartile read on larger sets

### Verification
**Ramp verified.** Means: 4.4 → 6.4 → 11.6 → 12.6 → 14.8 → 15.5.

---

## Implementation map (code)

| Piece | Location |
|-------|----------|
| Fraction side / prism side sampling | `Grade6VisualFramework._fraction_side_for_difficulty`, `_prism_fraction_sides` in `frameworks/number.py` |
| Drawing effort + axis scaffolding | `draw_dot_plot` / `draw_histogram` branch in `Grade6VisualFramework` |
| Stats continuous params + mode ladders | `frameworks/statistics.py` (`continuous_statistics_params`, task-mode helpers) |
| Continuous D on statistics profile | `settings/profiles.py` → `statistics_profile` |
| Drawing no longer forces `include_axis=True` | `generator_profiles.py` |
| Verify script | `scripts/verify_g6_batch6_effort.py` |

## How to re-verify

```powershell
$env:PYTHONPATH='.'; $env:QE_LOG_GENERATED='0'
python scripts/verify_g6_batch6_effort.py
```
