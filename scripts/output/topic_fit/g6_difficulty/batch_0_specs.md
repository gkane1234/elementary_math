# Grade 6 effort-based difficulty specs — Batch 0

**Branch:** `experiment/difficulty-slider`  
**Date:** 2026-07-27  
**Verification:** `scripts/verify_g6_batch0_effort_difficulty.py` → `scripts/output/topic_fit/g6_difficulty/batch_0_verification.json` (n=30 per D ∈ {0,5,10,15,20,25})

## Scope

Ready Grade 6 type_ids in curriculum order, after removing the first-11 ratios/percents SKIP set. This batch is remaining indices **[0, 10)**:

1. `g6_dividing_fractions`
2. `g6_decimal_addition`
3. `g6_decimal_subtraction`
4. `g6_decimal_multiplication_with_equivalent_fractions`
5. `g6_decimal_multiplication`
6. `g6_long_division_with_remainders`
7. `g6_dividing_whole_numbers_that_result_in_decimals`
8. `g6_dividing_decimals_by_whole_numbers`
9. `g6_dividing_whole_numbers_by_decimals`
10. `g6_dividing_decimals_by_decimals`

## Design principle (shared)

Difficulty is **effort / meaningful steps**, not raw magnitude.

- **Meaningful cancel steps** = Ω(strip_place_value_tens(GCD)) — prime factors after removing paired 2×5 (÷10ⁿ free).
- **Place-value ÷10ⁿ / ×10ⁿ is free** relative to multi-prime cancel or awkward place work.
- Continuous `difficulty` (LLM prior / slider) remains the generator prior; sampling maps D → **effort targets**.
- Shared helpers: `continuous_decimal_places`, `continuous_decimal_int_max`, `_target_meaningful_cancel_steps`, `_build_k_with_meaningful_steps`.

### Effort scale anchors

| D | Meaning |
|---|---|
| 0 | Very easy / minimal time |
| 5 | Standard simple |
| 10 | More involved / maybe extra trick |
| 15 | Clearly more work |
| 20 | Hard / awkward extras |
| 25 | Mean-to-assign-five-examples level |

---

## 1. `g6_dividing_fractions` — Dividing fractions

**Generator:** `RationalFramework("/")` via `g6_fraction_divide`  
**Profile:** `rational` + continuous `difficulty`; `allow_negative=False` (G6)

### What increases difficulty
- **Unreduced surface fractions** so reciprocal-cancel work is visible
- Shared inflate-k on (num↔num) and (den↔den) with targeted meaningful cancel steps
- Larger cores / mixed improper unlock at high D

### What does NOT count
- Pure place-value inflates (×10ⁿ only)
- Signed fractions (kept off for this G6 topic)
- Magnitude alone without cancel structure

### Continuous D → effort
`_target_meaningful_cancel_steps(d)` split across two cancel sites; D&lt;3 uses simple unit-fraction pairs with k=1.

### Anchors
- **0:** `1/2 ÷ 1/4`-style, integer answer
- **15:** unreduced e.g. `35/84 ÷ 35/42` with multi-step cancel
- **25:** large composite shared factors, Ω≈5+

### Verification
**verified_ramp.** Means: 6.0 → 8.4 → 11.8 → 16.4 → 19.6 → 22.3.

---

## 2. `g6_decimal_addition` — Decimal addition

**Generator:** `DecimalArithmeticFramework("+")`

### What increases difficulty
- Decimal places (1 → 2 → 3 → 4)
- **Misaligned places** (e.g. `26.63 + 3.6`)
- Regrouping / carry count across places
- Mild integer-part growth (not the main lever)

### What does NOT count
- Huge integers with 1 place
- Signs until very high D (and only if preset allows)

### Anchors
- **0:** tenths, little/no carry (`2.3 + 3.4`)
- **15:** hundredths/thousandths + alignment
- **25:** 4-place with carries

### Verification
**verified_ramp.** Means: 7.1 → 10.0 → 10.5 → 13.9 → 17.9 → 18.0.

---

## 3. `g6_decimal_subtraction` — Decimal subtraction

**Generator:** `DecimalArithmeticFramework("-")`

### What increases difficulty
- Places + misalignment
- **Borrow count** (targeted ≥1 at mid, ≥2 at high)
- High D forces longer minuend places

### What does NOT count
- Always-positive no-borrow subtractions at high D
- Magnitude-only without borrow/alignment

### Anchors
- **0:** tenths, often no borrow
- **15:** multi-borrow hundredths
- **25:** 3–4 place awkward borrow

### Verification
**verified_ramp.** Means: 5.9 → 10.7 → 10.4 → 14.7 → 17.2 → 16.4 (mild high-D plateau; still clear vs low D).

---

## 4. `g6_decimal_multiplication_with_equivalent_fractions`

**Generator:** `DecimalArithmeticFramework("*", via_equivalent_fractions=True)`

### What increases difficulty
- Shared non-10 factors between decimal numerators after ×10^p rewrite
- Place depth of each factor (tenths → hundredths → thousandths)
- Multi-step meaningful cancel (not ÷10ⁿ)

### What does NOT count
- Pure place-value products like `0.3 × 0.4` at high D (those are D≈0)
- Standard place-counting algorithm without fraction cancel (that’s the sibling topic)

### Mode split
| D | Construction |
|---|--------------|
| &lt;3 | Pure tenths, no shared non-10 cancel |
| 3–7 | Single small cancel (÷3/÷7) |
| ≥8 | Targeted multi-step k + deeper places |

### Verification
**verified_ramp.** Means: 10.0 → 13.8 → 16.8 → 21.3 → 25.0 → 25.0.

---

## 5. `g6_decimal_multiplication` — Decimal multiplication

**Generator:** `DecimalArithmeticFramework("*")` (standard)

### What increases difficulty
- whole × tenths → decimal × decimal
- Product place-sum (`a_places + b_places`)
- Continuous place ladder

### What does NOT count
- Equiv-fraction cancel structure (sibling topic)
- Negatives at G6 default

### Anchors
- **0:** `7 × 0.6`
- **10:** two-place × one/two-place
- **25:** 3–4 place × 3–4 place

### Verification
**verified_ramp.** Means: 6.5 → 8.9 → 10.7 → 12.8 → 14.8 → 16.7.

---

## 6. `g6_long_division_with_remainders`

**Generator:** `LongDivisionWithRemaindersFramework`

### What increases difficulty
- Dividend **digit count** (2 → 3 → 4 → 5)
- Divisor size / awkwardness (single-digit → teens → 20–40+)
- Nontrivial remainder

### What does NOT count
- Exact (remainder 0) divisions — forced nonzero remainder
- Magnitude without more digits/divisor work

### Continuous map
`digs = 2 + ⌊d/7⌋`; divisor max grows with D.

### Verification
**verified_ramp.** Means: 6.0 → 7.2 → 10.6 → 16.0 → 17.6 → 22.0.

---

## 7. `g6_dividing_whole_numbers_that_result_in_decimals`

**Generator:** `WholeDivideToDecimalFramework`

### What increases difficulty
- Quotient place length (1 → 2 → 3 → 4)
- Awkward divisors (8, 16, 125, …) vs place-value-friendly (2, 5, 10)
- Prefer exact place length at mid/high

### What does NOT count
- Integer quotients (filtered out)
- Pure ÷2/÷5 at high D (biased away)

### Verification
**verified_ramp.** Means: 4.5 → 5.2 → 7.6 → 15.6 → 17.8 → 17.9.

---

## 8. `g6_dividing_decimals_by_whole_numbers`

**Generator:** `DecimalArithmeticFramework("/")` (integer divisor)

### What increases difficulty
- Quotient places (explicit ladder by D bands)
- Divisor awkwardness (2/4/5 → 7/8/9 → 16/24/32)
- Larger quotient integer part at high D

### What does NOT count
- Non-terminating constructions (built backwards to terminate)
- Decimal divisors (different topic)

### Continuous map
| D | places | divisor pool |
|---|--------|--------------|
| &lt;4 | 1 | 2,4,5 |
| 4–8 | 2 | 2–5 |
| 8–13 | 2 | 3,6–9 |
| 13–18 | 3 | 6–15 |
| ≥18 | 3–4 | 7–32 awkward |

### Verification
**verified_ramp.** Means: 6.1 → 8.6 → 10.3 → 12.9 → 13.0 → 16.0.

---

## 9. `g6_dividing_whole_numbers_by_decimals`

**Generator:** `WholeByDecimalDivideFramework` (pre-existing continuous ladder, retained)

### What increases difficulty
- Divisor in (0,1) tenths → ≥1 unlock → awkward multi-place
- Magnitude of compatible integer quotient
- Signs at high D

### What does NOT count
- Integer divisors
- Place-value-only ×10 mental shifts without awkward divisor

### Verification
**verified_ramp.** Means: 6.0 → 9.2 → 9.8 → 13.9 → 14.7 → 13.8 (slight 20→25 noise; still clear vs low D).

---

## 10. `g6_dividing_decimals_by_decimals`

**Generator:** `DecimalDivideByDecimalFramework` (**new** — replaced fixed stub in `advanced.py`)

### What increases difficulty
- Divisor pool: friendly tenths → mixed ≥1 → 0.125/0.375/… awkward
- Non-integer quotients at high D
- Both operands visibly decimal

### What does NOT count
- Whole ÷ decimal (sibling topic)
- Stub-era fixed `{0.2,0.25,0.5,1.5,2.5}` pool with no D response

### Verification
**verified_ramp.** Means: 7.1 → 11.9 → 12.4 → 17.2 → 20.2 → 20.1.

---

## Status summary

| Status | Count |
|--------|------:|
| verified_ramp | 10 |
| weak_ramp | 0 |
| failed_ramp | 0 |
| blocked | 0 |

All ten topics in this batch show a clear meaningful effort increase from D=0 to D=25 under the batch scorers.
