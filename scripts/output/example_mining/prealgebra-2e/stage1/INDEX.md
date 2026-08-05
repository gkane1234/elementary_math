# Stage 1 inventories — `prealgebra-2e`

First tranche: **integers** (Ch 3), **fractions** (Ch 4), **decimals** (Ch 5.1–5.4), **percents** (Ch 6.1–6.4).  
Inspect these markdown files before Stage 2 (family tagging / EMH).

Mined from local HTML: `textbooks/openstax/html/prealgebra-2e/` (2026-07-28).

| Section | Items | Breakdown | Markdown |
|---------|------:|-----------|----------|
| `3-1-introduction-to-integers` | 103 | example=13, other_exercise=28, section_exercise=62 | [3-1-introduction-to-integers.md](3-1-introduction-to-integers.md) |
| `3-2-add-integers` | 115 | example=16, other_exercise=35, section_exercise=64 | [3-2-add-integers.md](3-2-add-integers.md) |
| `3-3-subtract-integers` | 138 | example=17, other_exercise=37, section_exercise=84 | [3-3-subtract-integers.md](3-3-subtract-integers.md) |
| `3-4-multiply-and-divide-integers` | 116 | example=13, other_exercise=29, section_exercise=74 | [3-4-multiply-and-divide-integers.md](3-4-multiply-and-divide-integers.md) |
| `3-5-solve-equations-using-integers-the-division-property-of-equality` | 98 | example=9, other_exercise=21, section_exercise=68 | [3-5-solve-equations-using-integers-the-division-property-of-equality.md](3-5-solve-equations-using-integers-the-division-property-of-equality.md) |
| `4-1-visualize-fractions` | 132 | example=18, other_exercise=38, section_exercise=76 | [4-1-visualize-fractions.md](4-1-visualize-fractions.md) |
| `4-2-multiply-and-divide-fractions` | 156 | example=18, other_exercise=39, section_exercise=99 | [4-2-multiply-and-divide-fractions.md](4-2-multiply-and-divide-fractions.md) |
| `4-3-multiply-and-divide-mixed-numbers-and-complex-fractions` | 126 | example=15, other_exercise=33, section_exercise=78 | [4-3-multiply-and-divide-mixed-numbers-and-complex-fractions.md](4-3-multiply-and-divide-mixed-numbers-and-complex-fractions.md) |
| `4-4-add-and-subtract-fractions-with-common-denominators` | 98 | example=11, other_exercise=25, section_exercise=62 | [4-4-add-and-subtract-fractions-with-common-denominators.md](4-4-add-and-subtract-fractions-with-common-denominators.md) |
| `4-5-add-and-subtract-fractions-with-different-denominators` | 176 | example=18, other_exercise=38, section_exercise=120 | [4-5-add-and-subtract-fractions-with-different-denominators.md](4-5-add-and-subtract-fractions-with-different-denominators.md) |
| `4-6-add-and-subtract-mixed-numbers` | 107 | example=14, other_exercise=31, section_exercise=62 | [4-6-add-and-subtract-mixed-numbers.md](4-6-add-and-subtract-mixed-numbers.md) |
| `4-7-solve-equations-with-fractions` | 121 | example=14, other_exercise=31, section_exercise=76 | [4-7-solve-equations-with-fractions.md](4-7-solve-equations-with-fractions.md) |
| `5-1-decimals` | 127 | example=10, other_exercise=23, section_exercise=94 | [5-1-decimals.md](5-1-decimals.md) |
| `5-2-decimal-operations` | 160 | example=17, other_exercise=37, section_exercise=106 | [5-2-decimal-operations.md](5-2-decimal-operations.md) |
| `5-3-decimals-and-fractions` | 123 | example=12, other_exercise=27, section_exercise=84 | [5-3-decimals-and-fractions.md](5-3-decimals-and-fractions.md) |
| `5-4-solve-equations-with-decimals` | 102 | example=9, other_exercise=21, section_exercise=72 | [5-4-solve-equations-with-decimals.md](5-4-solve-equations-with-decimals.md) |
| `6-1-understand-percent` | 138 | example=13, other_exercise=29, section_exercise=96 | [6-1-understand-percent.md](6-1-understand-percent.md) |
| `6-2-solve-general-applications-of-percent` | 90 | example=11, other_exercise=25, section_exercise=54 | [6-2-solve-general-applications-of-percent.md](6-2-solve-general-applications-of-percent.md) |
| `6-3-solve-sales-tax-commission-and-discount-applications` | 76 | example=8, other_exercise=18, section_exercise=50 | [6-3-solve-sales-tax-commission-and-discount-applications.md](6-3-solve-sales-tax-commission-and-discount-applications.md) |
| `6-4-solve-simple-interest-applications` | 65 | example=7, other_exercise=16, section_exercise=42 | [6-4-solve-simple-interest-applications.md](6-4-solve-simple-interest-applications.md) |

## PA catalog mappings + effort drivers

Beyond raw magnitude (larger |n|, bigger denominators), what typically makes items harder in each section:

| Section | PA / related `type_id` | Status vs catalog | Effort drivers (non-magnitude) |
|---------|------------------------|-------------------|--------------------------------|
| 3.1 Intro integers | — (G6 signed/absolute; no dedicated PA intro type) | gap / covered upstream | opposites language; absolute value; number-line locate; compare signed |
| 3.2 Add integers | `pa_integers_adding_and_subtracting` | wired | unlike signs; 3+ addends; abs-value addends; parenthetical grouping; application translate |
| 3.3 Subtract integers | `pa_integers_adding_and_subtracting` | wired | rewrite as add-opposite; double negatives; mixed ± chains; applications |
| 3.4 Mul/div integers | `pa_integers_multiplying`, `pa_integers_dividing` | wired | sign with 3+ factors; OOPs with signed ops; evaluate variable expressions |
| 3.5 Eqns w/ integers | `pa_equations_*` (one-/multi-step); division property | partial | negative coefficients; isolate via ÷; integer ops inside solve |
| 4.1 Visualize fractions | `pa_simplifying_fractions` (equiv/simplify only) | partial; diagrams → defer UI | improper↔mixed; equivalent forms; model/read fraction; simplify by GCF |
| 4.2 ×÷ fractions | `pa_fractions_multiply`, `pa_fractions_divide` (→ `g6_fraction_*`) | **wired** (PA aliases) | cancel-before-multiply; reciprocal for ÷; improper intermediate; multi-factor products |
| 4.3 Mixed ×÷ / complex | — | **missing** (complex: A2 algebraic only) | mixed↔improper; nested complex fractions; multi-op chains |
| 4.4 ± like denominators | `pa_fractions_{add,subtract}_like` (→ `g6_fraction_*`) | **wired** (PA aliases) | simplify after; improper result; signed fractions |
| 4.5 ± unlike denominators | `pa_fractions_{add,subtract}_unlike` | **wired** (PA aliases) | LCD construction (not just product); 3+ terms; cancel after |
| 4.6 ± mixed numbers | — | **missing** | regroup/borrow; unlike denoms + mixed; simplify |
| 4.7 Eqns w/ fractions | `pa_equations_multi_step_equations` | partial (want dedicated mode) | clear denominators / LCD; fraction coefficients |
| 5.1 Decimals | `pa_naming_decimal_places_and_rounding`, `pa_writing_numbers_with_words` | wired | place-name depth; round vs name; expanded form |
| 5.2 Decimal ops | G6 `g6_decimal_*` | PA thin — ops live on G6 | place alignment; ×÷ point placement; trailing zeros |
| 5.3 Decimals ↔ fractions | `pa_converting_fractions_and_decimals` | wired | terminating vs repeating; simplify after convert |
| 5.4 Eqns w/ decimals | `pa_equations_multi_step_equations` | partial | clear decimals (×10ⁿ); mixed decimal/fraction coeffs |
| 6.1 Understand percent | `pa_fractions_decimals_and_percents` (+ G6 relating) | wired | conversion triad direction; % as /100 models |
| 6.2 Percent applications | `percents` | wired (shared) | unknown part/whole/%; % > 100; translate “is/of” |
| 6.3 Tax / commission / discount | `pa_markup_discount_and_tax` | wired; commission mode may need extend | multi-step (discount then tax); original vs sale; commission base |
| 6.4 Simple interest | `pa_simple_and_compound_interest` | wired | solve for P/r/t; time in months/days; simple vs compound prompt |

### Highest-priority follow-ups (from this mine)

1. **Mixed-number arithmetic** (4.3 ×÷, 4.6 ±) — clear `missing` (fraction ±×÷ now wired as PA aliases).
2. **Dedicated fraction/decimal coefficient equation modes** (4.7, 5.4) — currently folded into multi-step.
3. Fix **`pa_markup_discount_and_tax`** generator stubs (6.3).

## What to check

1. Are examples / checkpoints / section exercises classified correctly?
2. Is the prompt text readable (math roughly intact as `$...$`)?
3. Are learning objectives present?
4. Anything duplicated, empty, or clearly truncated?

## Not in this tranche

- Ch 5.5 averages/probability, 5.6 ratios/rate, 5.7 square roots
- Ch 6.5 proportions applications (covered under PA proportions chapter)
- Ch 1–2 language/factors (upstream of integers/fractions)
