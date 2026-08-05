# Grade 6 effort-based difficulty specs (first 11 Ready topics)

**Branch:** `experiment/difficulty-slider`  
**Date:** 2026-07-27  
**Verification:** `scripts/verify_g6_effort_difficulty.py` → `scripts/output/topic_fit/g6_difficulty/verification_summary.json` (n=40 per D ∈ {0,5,10,15,20,25})  
**Unit tests:** `question_engine/tests/test_g6_effort_difficulty.py`

## Design principle (shared)

Difficulty is **effort / meaningful steps**, not raw magnitude.

- **Meaningful cancel steps** = Ω(strip_place_value_tens(GCD)) — total prime factors after removing paired 2×5 (factors of 10).
- **Place-value ÷10ⁿ is free:** `500:1000` (GCD 500 → strip → 5 → 1 leftover step) stays easy vs `24:136` (multi-prime cancel).
- Continuous `difficulty` (LLM prior / slider) remains the generator prior; sampling maps D → **effort targets**, not just larger integers.
- **Mode splits** matter: write-as-given / shade-benchmark tasks must not fake high D.

### Effort scale anchors

| D | Meaning |
|---|---|
| 0 | Very easy / minimal time |
| 5 | Standard simple |
| 10 | More involved / maybe extra trick |
| 15 | Clearly more work |
| 20 | Hard / awkward extras |
| 25 | Mean-to-assign-five-examples level |

### Topic order (curriculum Ready leaves)

1. `g6_introduction_to_ratios`
2. `g6_equivalent_ratios`
3. `g6_part_part_whole_ratios`
4. `g6_comparing_ratios`
5. `g6_unit_rates_and_equivalent_rates`
6. `g6_comparing_rates`
7. `g6_converting_units`
8. `g6_introduction_to_percents`
9. `g6_relating_percents_fractions_and_decimals`
10. `g6_finding_percents_with_equivalent_fractions`
11. `g6_solving_percent_problems_with_formulas`

(Skipped nearby: `g6_solving_percent_problems_with_diagrams` — not Ready / diagram gap.)

---

## 1. `g6_introduction_to_ratios` — Introduction to ratios

**Generator:** `RatioFramework(equivalent=False)`  
**Profile:** `ratio` + continuous `difficulty`

### What increases difficulty
- **Task mode:** write-as-given (word) → simplify-to-fraction
- **Meaningful cancel steps** on GCD of the shown parts (prime Ω after stripping ÷10ⁿ)
- Multi-prime composite GCFs (12, 18, 24, 36, …) over single ÷2/÷3
- At D≥5, inflate-k forced ≥2 so simplify items have real work

### What does NOT count
- Pure place-value cancels (GCD ∈ {10, 100, 1000, …}) — treated as ~0 meaningful steps
- Large parts alone (`500:1000` style) without non-10ⁿ leftover factors
- Write-as-given prompts at high D (forbidden: D≥8 is always simplify)

### Mode split
| D | Form mix |
|---|----------|
| 0–3 | ~75% word write-as-given |
| 3–8 | ~85% simplify |
| ≥8 | 100% simplify |

### Continuous D → effort
`_target_meaningful_cancel_steps(d)` ≈ 0 / 1 / 2 / 3 / 4 / 5+ at D≈0 / 5 / 10 / 15 / 20 / 25; `_build_k_with_meaningful_steps` builds inflate-k to match (avoids pure ×10ⁿ).

### Anchors
- **5:** single small cancel (÷2/÷3), e.g. `8:6`
- **15:** Ω≈3 composites, e.g. `12:48`
- **25:** Ω≈5+ awkward cancels, e.g. `144:24`

### Verification
**Ramp verified.** Means: 0.7 → 6.2 → 10.2 → 13.7 → 16.8 → 19.6. High-D sheets are simplify-only.

---

## 2. `g6_equivalent_ratios` — Equivalent ratios

**Generator:** `RatioFramework(equivalent=True)` → `_sample_equivalent_ratio_missing`

### What increases difficulty
- Inflate-k on the left ratio (unreduced `a:b`)
- **Reduce-then-scale:** surface scale `c/a` not an integer (must cancel GCF then multiply)
- Larger equivalence multiplier `m` from `continuous_ratio_scale_max`
- Fraction form vs colon (minor reading friction)

### What does NOT count
- Barely larger already-simplified ×2/×3 at low D (that's D≈0–3 by design)
- Pure place-value inflate without meaningful leftover (same strip rule via shared `_sample_ratio_inflate_k`)

### Mode split
Missing-value only (`a:b = c:x` or fraction form). No “generate next equivalent” / tables yet.

### Continuous D map
- D&lt;3: k=1, m∈{2,3}, integer surface scale  
- D&lt;10: inflate-k, ~50% reduce-then-scale  
- D≥10: larger m, ~70% reduce-then-scale with `m % k ≠ 0`

### Anchors
- **5:** small inflate, often integer ×3 surface  
- **15:** unreduced left + non-integer surface (e.g. `60/12 = 45/x`)  
- **25:** large composite both sides (e.g. `320/224 = 3840/x`)

### Verification
**Ramp verified.** Means: 3.0 → 7.1 → 10.8 → 13.9 → 16.0 → 17.8.

---

## 3. `g6_part_part_whole_ratios` — Part–part–whole ratios

**Generator:** `PartPartWholeRatioFramework` (**new** — no longer a simplify-ratio stand-in)

### What increases difficulty
- Task: part:part → part:whole / whole:part → missing-part from whole+ratio → both ratios in simplest form
- Requiring simplest form when GCD&gt;1
- Inflated part sizes (meaningful cancel on parts/totals)
- Two-answer “both” prompts

### What does NOT count
- Rewriting the same two counts as `a:b` at high D without part:whole / missing-part skill
- Magnitude-only “bigger marbles” without a harder task type

### Mode split
| D | Modes |
|---|--------|
| &lt;5 | part:part write-as-given |
| 5–12 | part:whole / whole:part mix |
| 12–18 | missing-part + both |
| ≥18 | missing-part / both only |

### Anchors
- **5:** part:whole from small counts  
- **15:** part:whole in simplest form with inflated parts  
- **25:** missing part from whole + simplified ratio (e.g. 408 split 7:10)

### Verification
**Ramp verified.** Means: 4.0 → 7.0 → 10.5 → 14.9 → 16.6 → 16.7 (high-D plateau on task type, not magnitude).

---

## 4. `g6_comparing_ratios` — Comparing ratios

**Generator:** `ComparingRatiosFramework` (**new** — no longer missing-value stand-in)

### What increases difficulty
- Same-part easy compare → independent ratios needing reduce-then-compare  
- **Closeness ladder** — relative unit-rate gap `|v1−v2|/max(v1,v2)` shrinks with D (near-ties at high D)  
- Unreduced surfaces (meaningful cancel steps on both GCDs; awkward non-10ⁿ primes, not just bigger parts)  
- Fraction form at higher D

### What does NOT count
- Asking for a missing proportion value (wrong skill)  
- Huge equal ratios that are obviously equal after canceling trailing zeros only  
- Only larger integers with wide, obvious unit-rate gaps

### Mode split
Binary “which is greater?” (or equal). No three-way order yet.

| D band | Structure |
|--------|-----------|
| &lt;6 | Same first/second part; light/no inflate; clearly different |
| ≥6 | Independent cores forced within relative-gap budget, then inflate |
| ≥12 | Both GCDs need ≥1 meaningful cancel step |
| ≥14 | Both sides unreduced (`min_k≥2`); equals rare |
| ≥18 | Both GCDs meet near-target meaningful cancel steps |

Relative-gap budget ≈ `0.55·e^(−0.08·D)` (floor 0.04) — D≈5 → ~0.37, D≈15 → ~0.17, D≈25 → ~0.07.

### Anchors
- **5:** same first/second part, small/light inflate, easy to tell apart  
- **15:** unreduced independent compare within mid closeness budget  
- **25:** both sides awkward GCF cancel + near-tie unit rates

### Verification
**Ramp verified** (closeness + cancel axes). Re-check mean relative gap ↓ and mean meaningful cancel steps ↑ with D.

---

## 5. `g6_unit_rates_and_equivalent_rates` — Unit rates and equivalent rates

**Generator:** `UnitRateFramework` (`g6_unit_rates`)

### What increases difficulty
- Mode mix shifts toward **equivalent-rate** (scale) vs find-unit-rate  
- Quantity inflate-k with **meaningful** cancel (not ÷10-only)  
- Reduce-then-scale equivalents (non-integer surface scale)  
- Context still speed / reading / unit price

### What does NOT count
- Only larger totals with qty=1 already a unit rate  
- Pure trailing-zero qty cancels as “hard”

### Mode split
| D | equiv_p |
|---|---------|
| &lt;5 | 0.25 |
| &lt;15 | 0.40 |
| ≥15 | 0.55 |

### Anchors
- **5:** small unit rate, often ÷2/÷3  
- **15:** equivalent-rate with scale  
- **25:** composite qty cancel + larger cores

### Verification
**Ramp verified.** Means: 8.1 → 8.6 → 11.0 → 15.1 → 17.4 → 17.9.

---

## 6. `g6_comparing_rates` — Comparing rates

**Generator:** `ComparingRatesFramework` (+ DNL stimulus)

### What increases difficulty
- Unit bottom (per 1) → both non-unit bottoms  
- Meaningful GCF on each given rate  
- DNL tick extension shrinks as amounts grow (less scaffolding)  
- Closer unit rates / larger composites

### What does NOT count
- Name-vs-name with one already unit and tiny numbers at high D (filtered out for D≥12)

### Mode split
Unit price vs speed; ask higher vs lower winner.

### Anchors
- **5:** often one unit bottom  
- **15:** both unreduced non-unit  
- **25:** large composite both sides (effort ceiling in scorer)

### Verification
**Ramp verified.** Means: 10.8 → 12.5 → 22.2 → 24.8 → 25 → 25 (saturates mid-high by design of dual non-unit + inflate).

---

## 7. `g6_converting_units` — Converting units

**Generator:** `ConvertingUnitsFramework` (+ DNL)

### What increases difficulty
- Easy metric (mm↔cm, cm↔m) → mid metric (m↔km, g↔kg) → **approximate customary** (kg≈lb, km≈mi)  
- Partial / off-multiple amounts  
- Larger multiples along the given equivalence

### What does NOT count
- “Bigger cm” on the same mm↔cm fact alone  
- Multi-hop chains (not generated yet — still one given equivalence)

### Continuous D map
| D | Pool |
|---|------|
| &lt;5 | easy metric |
| &lt;10 | all metric |
| &lt;16 | metric + approx |
| ≥16 | prefer approx + mid metric + partials |

### Anchors
- **5:** mid metric whole multiples  
- **15:** mix / early approx  
- **25:** approximate customary with large multiples

### Verification
**Ramp verified (moderate).** Means: 5.0 → 7.7 → 9.3 → 9.0 → 10.0 → 10.7. Structure-led more than number bloat.

---

## 8. `g6_introduction_to_percents` — Introduction to percents

**Generator:** `IntroductionToPercentsFramework` (shade figure)

### What increases difficulty
- **Figure structure:** 100-grid benchmarks → multiples of 5 → awkward % → percent bar → **circle**  
- Awkward percents (not multiples of 5)  
- Prompt names the figure (`100-square grid` / `percent bar` / `circle`)

### What does NOT count
- Larger percent values as hardness (46% is not harder than 50% on a hundred grid)  
- Formula “what is p% of n?” (wrong topic)

### Continuous D map (0–25 classroom band)
| D | Spec |
|---|------|
| ≤4 | benchmarks on hundred grid |
| ≤8 | mid ×5 on grid/bar |
| ≤12 | awkward % on hundred grid/bar |
| ≤18 | awkward + bar |
| ≤28 | awkward + circle |

### Anchors
- **5:** 5%/35%-style on grid  
- **15:** awkward % on bar  
- **25:** awkward % on circle

### Verification
**Ramp verified.** Means: 5.0 → 9.2 → 10.8 → 12.0 → 14.0 → 15.3.

---

## 9. `g6_relating_percents_fractions_and_decimals` — Relating % / fractions / decimals

**Generator:** `FractionDecimalConvertFramework(include_percent=True)` (**fixed** — was fraction↔decimal only)

### What increases difficulty
- Benchmark triples (½↔0.5↔50%) → tenths/fifths → **eighths / sixteenths** (12.5%, 6.25%, …)  
- Direction mix emphasizing %↔frac and %↔dec  
- “Simplest form” after %→frac

### What does NOT count
- Fraction↔decimal without percent (excluded by forcing `include_percent_conversions`)  
- Larger unrelated denominators that don’t appear in terminating % triples

### Continuous D map
| D | Triple bank |
|---|-------------|
| &lt;5 | easy |
| &lt;12 | medium |
| &lt;18 | mostly hard |
| ≥18 | hard-only (exclude easy benchmarks) |

### Anchors
- **5:** 3/20 ↔ 15% style  
- **15:** mix into eighths  
- **25:** 32.5% / 6.25% / 18.75% family

### Verification
**Ramp verified (milder).** Means: 5.3 → 5.9 → 5.9 → 7.2 → 9.9 → 9.1. Pool-based; high D biased to awkward %.

---

## 10. `g6_finding_percents_with_equivalent_fractions` — Finding percents with equivalent fractions

**Generator:** `FindingPercentsEquivalentFractionsFramework` (**new** — not bare `PercentFramework`)

### What increases difficulty
- Scale-to-100 factor: ×2/×5/×10 → ×4 from 25 → eighths (×12.5 path)  
- **Unreduced surface** requiring reduce-then-×100 (display keeps unreduced `a/b`)  
- %→frac via denom-100 method at mid/high D

### What does NOT count
- Formula “what is 40% of 80?” without equivalent-fraction language  
- Place-value-only ×10 to 100 as high effort

### Continuous D map
| D | Bank / surface |
|---|---------------|
| &lt;4 | denoms 2,4,5,10,20,50,100; reduced |
| &lt;9 | 20,25,50,… standard ×4/×5 |
| &lt;14 | eighths/40; sometimes unreduced |
| ≥14 | force unreduced + awkward denoms |

### Anchors
- **5:** `1/2` → 50% via ×50  
- **15:** unreduced `36/48` → reduce → %  
- **25:** 37.5% ↔ 3/8 / sixteenths

### Verification
**Ramp verified.** Means: 6.8 → 7.0 → 11.4 → 13.7 → 15.4 → 15.3.

---

## 11. `g6_solving_percent_problems_with_formulas` — Solving percent problems with formulas

**Generator:** `PercentFramework` (`percents`)

### What increases difficulty
- Unknown position: mostly **p% of n** → more **find %** → more **find whole**  
- Continuous base growth beyond EMH caps  
- Decimal percents unlocked at high D  
- Less “nice” wholes

### What does NOT count
- Equivalent-fraction method prompts (that’s topic 10)  
- Diagram/shade tasks  
- Story tax/tip contexts (not yet; still bare formula stems)

### Mode split
| D | Bias |
|---|------|
| &lt;5 | ~75% percent_of |
| 5–15 | mix find_percent |
| ≥15 | more find_whole; decimal % ≥18 |

### Anchors
- **5:** find-% with nice doubles  
- **15:** mix of find-% / find-whole  
- **25:** find-whole + messier bases / decimal %

### Verification
**Ramp verified.** Means: 5.6 → 7.9 → 8.1 → 8.2 → 10.4 → 10.9.

---

## Implementation map (code)

| Piece | Location |
|-------|----------|
| `strip_place_value_tens`, `meaningful_cancel_steps`, inflate targeting | `question_engine/frameworks/number.py` |
| Intro / equivalent ratios mode + sampling | `RatioFramework`, `_sample_shown_ratio_parts`, `_sample_ratio_inflate_k` |
| Part–part–whole / comparing ratios | `PartPartWholeRatioFramework`, `ComparingRatiosFramework` |
| Finding % via equiv fractions | `FindingPercentsEquivalentFractionsFramework` |
| Relating FDP fix | `generators/grade6.py` forces `include_percent=True` |
| Catalog wiring | `catalogs/grade_6.py` generator keys updated |
| Verify script | `scripts/verify_g6_effort_difficulty.py` |

## How to re-verify

```powershell
$env:PYTHONPATH='.'; $env:QE_LOG_GENERATED='0'
python scripts/verify_g6_effort_difficulty.py
python -m pytest question_engine/tests/test_g6_effort_difficulty.py question_engine/tests/test_g6_pa_continuous_ladders.py question_engine/tests/test_g6_introduction_to_percents.py -q
```

Raw means and representatives: `scripts/output/topic_fit/g6_difficulty/verification_summary.json`.

---

## Later batches (remaining Ready G6)

After these first 11, remaining Ready topics were verified in batches under `scripts/output/topic_fit/g6_difficulty/`:

| Batch | Specs | Verification |
|---|---|---|
| 0 | `batch_0_specs.md` | `batch_0_verification.json` |
| 1 | `batch_1_specs.md` | `batch_1_verification.json` |
| 2 | `batch_2_specs.md` | `batch_2_verification.json` |
| 3 | `batch_3_specs.md` | `batch_3_verification.json` |
| 4 | `batch_4_specs.md` | `batch_4_verification.json` |
| 5 | `batch_5_specs.md` | `batch_5_verification.json` |
| 6 | `batch_6_specs.md` | `batch_6_verification.json` |

Master rollup: `scripts/output/topic_fit/g6_difficulty/TRACKING.md` (+ `TRACKING.json`).
