# Grade 6 effort-based difficulty — batch 1 (Ready indices [10, 20))

**Branch:** `experiment/difficulty-slider`  
**Date:** 2026-07-27  
**Verification:** `scripts/verify_g6_effort_difficulty_batch1.py` → `scripts/output/topic_fit/g6_difficulty/batch_1_verification.json` (n=30 per D ∈ {0,5,10,15,20,25})

## Design principle (shared)

Difficulty is **effort / meaningful steps**, not raw magnitude.

- Factoring / GCF / LCM: prime Ω and meaningful cancel steps — not large near-coprime products or `2×67`-style semiprime theater.
- Number line: locating harder points / multi-step moves — not wider integer ranges alone.
- Compare / order / abs: form mix and closeness — not bigger integers.

### Batch topics (ordered Ready G6 − SKIP, indices [10, 20))

| i | type_id | status |
|---|---------|--------|
| 10 | `g6_factoring` | verified_ramp |
| 11 | `g6_greatest_common_factor` | verified_ramp |
| 12 | `g6_least_common_multiple` | verified_ramp |
| 13 | `g6_gcf_and_lcm_word_problems` | verified_ramp |
| 14 | `g6_numbers_on_a_number_line` | verified_ramp |
| 15 | `g6_number_line_word_problems` | verified_ramp |
| 16 | `g6_comparing_numbers` | verified_ramp |
| 17 | `g6_ordering_numbers` | verified_ramp |
| 18 | `g6_absolute_values` | verified_ramp |
| 19 | `g6_comparing_with_absolute_values` | verified_ramp |

**Status counts:** verified_ramp **10** · weak_ramp **0** · failed_ramp **0** · blocked **0**

---

## 1. `g6_factoring` — Factoring

**Generator:** `PrimeFactorizationFramework`  
**Profile:** `factor` + continuous `difficulty`

### What increases difficulty
- Target **Ω(n)** (prime factors with multiplicity): ~2 → 3 → 4 → 5+
- More **distinct** primes in the factor tree
- Slightly larger allowed primes (≤5 → ≤23), still classroom-sized products

### What does NOT count
- Large semiprimes (`2×53`, `2×67`) as “hard”
- Magnitude alone via unbounded `continuous_abs_max` range sampling

### Continuous D → effort
`_sample_prime_product_effort(d)` builds composites to `_target_prime_omega(d)` under `_factor_product_cap` / `_prime_max_for_difficulty`.

### Anchors
- **5:** two-prime products (`15`, `21`)
- **15:** Ω≈4 trees (`2²·3·5`-family)
- **25:** Ω≈5–6 multi-prime products (capped ≤~720)

### Verification
**verified_ramp.** Means: 6.5 → 6.5 → 10.4 → 14.0 → 16.7 → 19.0.

---

## 2. `g6_greatest_common_factor` — Greatest common factor

**Generator:** `GcfLcmFramework(mode="gcf")`

### What increases difficulty
- **Meaningful cancel steps** on the shared GCF (`_target_meaningful_cancel_steps`)
- More 3-number sets at mid/high D
- Composite GCFs (12, 18, 24, …) over single ÷2/÷3

### What does NOT count
- Huge numbers with GCF=2 (“find GCF of 136, 150”)
- Pure place-value shared factors as high effort

### Continuous D map
Build `g` via `_build_k_with_meaningful_steps`, then coprime multipliers so GCF is exactly `g`. Soft magnitude cap from `_factor_product_cap`.

### Anchors
- **5:** GCF ∈ {2,3,5}, two numbers
- **15:** Ω≈3 GCFs, sometimes three numbers
- **25:** multi-prime GCF + three-number sets

### Verification
**verified_ramp.** Means: 6.2 → 6.2 → 10.2 → 14.4 → 17.3 → 20.8.

---

## 3. `g6_least_common_multiple` — Least common multiple

**Generator:** `GcfLcmFramework(mode="lcm")`

### What increases difficulty
- Combined prime-factor work across the set (Ω + distinct primes)
- Less shared core at high D; more 3-number LCMs ≥18
- Classroom LCM size cap (not 100k+ products)

### What does NOT count
- Near-coprime large integers whose LCM is just the product
- Magnitude-only growth of `_factor_bounds`

### Continuous D map
| D | Spec |
|---|------|
| &lt;3 | tiny related pairs (`2,4`, `3,6`, …) |
| &lt;6 | small shared pairs (`6,8`, `8,12`, …) |
| mid | shared core + extras |
| ≥18 | prefer 3 numbers, higher Ω, less sharing |

### Anchors
- **5:** small related pairs
- **15:** multi-prime two-number LCM
- **25:** three-number / higher Ω (mild high-D plateau)

### Verification
**verified_ramp** (mild high-D plateau). Means: 6.4 → 8.0 → 16.2 → 17.3 → 19.0 → 18.3.

---

## 4. `g6_gcf_and_lcm_word_problems` — GCF and LCM word problems

**Generator:** `GcfLcmWordFramework`

### What increases difficulty
- Same effort sampling as GCF/LCM numeric
- Mode mix shifts toward **LCM pack** stories as D rises
- Same-first-letter nouns at D≥20 (`SAME_LETTER_MIN_DIFFICULTY`)

### What does NOT count
- Longer noun lists / bigger pack sizes without harder factor structure

### Mode split
| D | lcm_p (approx) |
|---|----------------|
| &lt;5 | 0.35 |
| &lt;12 | 0.45 |
| &lt;18 | 0.55 |
| ≥18 | 0.65 |

### Anchors
- **5:** small GCF bag stories
- **15:** mixed; LCM packs with mid effort
- **25:** LCM-heavy + same-letter noun friction

### Verification
**verified_ramp.** Means: 7.9 → 9.5 → 12.6 → 13.5 → 14.3 → 16.7.

---

## 5. `g6_numbers_on_a_number_line` — Numbers on a number line

**Generator:** `NumberLinePlotFramework` (`number_line_plot`)

### What increases difficulty
- **Point type:** positive ints → signed ints → halves → quarters
- Tick interval shrinks (1 → 0.5 → 0.25) with denser locating work

### What does NOT count
- Wider ±N integer ranges alone (old flat −10…10)

### Continuous D map
| D | Spec |
|---|------|
| &lt;4 | positives 0–8 |
| &lt;10 | signed ints |
| &lt;16 | forced halves (tick 0.5) |
| ≥16 | quarters (prefer non-halves; tick 0.5→0.25) |

### Anchors
- **5:** signed integers
- **15:** halves like `15/2`
- **25:** quarters like `7/4`, `13/4`

### Verification
**verified_ramp.** Means: 3.6 → 4.6 → 10.0 → 10.0 → 13.1 → 13.5.

---

## 6. `g6_number_line_word_problems` — Number line word problems

**Generator:** `NumberLineWordFramework` (`wp_number_line`)

### What increases difficulty
- Cross-zero moves (sign change)
- Context mix: temperature → elevation → account
- **Two-step** changes (rose then dropped / climbed then descended) at D≥14

### What does NOT count
- Larger °F swings alone without crossing zero / multi-step

### Continuous D map
| D | Spec |
|---|------|
| low | single-step temp; rare cross |
| mid | more cross-zero; elevation unlocks |
| ≥14 | two-step mix; account contexts ≥16 |

### Anchors
- **5:** single-step temperature
- **15:** cross-zero / early two-step
- **25:** two-step + varied contexts

### Verification
**verified_ramp.** Means: 6.7 → 7.4 → 9.1 → 12.9 → 13.5 → 15.3.

---

## 7. `g6_comparing_numbers` — Comparing numbers

**Generator:** `CompareOrderFramework(mode="compare")` (pre-existing form ladder)

### What increases difficulty
- Form mix: whole–whole → whole–decimal → decimal–decimal → decimal–frac / frac–whole → frac–frac
- Closeness tightens with D (secondary)

### What does NOT count
- Unbounded integer magnitude compare

### Anchors
- **5:** signed wholes / early decimals
- **15:** decimal–frac mix
- **25:** frac–frac / close values

### Verification
**verified_ramp.** Means: 5.5 → 6.2 → 9.9 → 12.2 → 12.9 → 13.9.

---

## 8. `g6_ordering_numbers` — Ordering numbers

**Generator:** `CompareOrderFramework(mode="order")`

### What increases difficulty
- Count 3 → 4 → 5
- Hardest unlocked forms forced into the set
- Closeness of the pack

### What does NOT count
- Ordering five huge integers far apart

### Anchors
- **5:** 3 values, early decimals
- **15:** 4 values with fractions
- **25:** 5-value mixed packs

### Verification
**verified_ramp** (mild high-D plateau). Means: 6.9 → 9.5 → 14.0 → 18.1 → 20.9 → 20.7.

---

## 9. `g6_absolute_values` — Absolute values

**Generator:** `AbsoluteValueFramework(mode="evaluate")`

### What increases difficulty
- Sign: mostly positive → mostly negative
- **Expression interior:** `|a−b|` / `|a+(−b)|` → `|a−(−b)|`, `|−a−b|`, …

### What does NOT count
- `|146|` vs `|8|` magnitude theater (removed continuous `_int_bounds` path for evaluate)

### Continuous D map
| D | Spec |
|---|------|
| &lt;4 | mostly `|n|` positive |
| &lt;10 | negatives / rare zero |
| &lt;16 | `|a−b|` / `|a+(−b)|` |
| ≥16 | mixed-sign interiors |

### Anchors
- **5:** `|−n|`
- **15:** simple difference inside abs
- **25:** double-negative interiors

### Verification
**verified_ramp** (plateaus once expressions unlock). Means: 3.6 → 9.6 → 13.2 → 13.5 → 14.0 → 14.1.

---

## 10. `g6_comparing_with_absolute_values` — Comparing with absolute values

**Generator:** `AbsoluteValueFramework(mode="compare")` (pre-existing closeness ladder)

### What increases difficulty
- Far `|·|` gaps → near-ties
- Mixed signs so students must take abs

### What does NOT count
- Larger magnitudes with obvious gaps

### Anchors
- **5:** clear gaps, mostly same sign
- **15:** closer gaps, mixed signs
- **25:** near-ties

### Verification
**verified_ramp.** Means: 8.7 → 12.3 → 14.2 → 14.4 → 16.2 → 17.0.

---

## Implementation map (code)

| Piece | Location |
|-------|----------|
| Prime-product / GCF / LCM effort sampling | `question_engine/frameworks/number.py` (`_sample_prime_product_effort`, `_sample_gcf_values_effort`, `_sample_lcm_values_effort`, frameworks) |
| Abs evaluate structure ladder | `AbsoluteValueFramework._build_evaluate` |
| Number-line plot form ladder + fractional ticks | `NumberLinePlotFramework`, `_number_line_bounds` in `graphing.py` |
| Number-line word cross-zero / two-step | `NumberLineWordFramework` in `word_problem.py` |
| Verify script | `scripts/verify_g6_effort_difficulty_batch1.py` |

## How to re-verify

```powershell
$env:PYTHONPATH='.'; $env:QE_LOG_GENERATED='0'
python scripts/verify_g6_effort_difficulty_batch1.py
```

Raw means and representatives: `scripts/output/topic_fit/g6_difficulty/batch_1_verification.json`.
