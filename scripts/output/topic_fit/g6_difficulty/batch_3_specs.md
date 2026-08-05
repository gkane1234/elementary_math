# Grade 6 effort-based difficulty — batch 3

**Branch:** `experiment/difficulty-slider`  
**Date:** 2026-07-27  
**Slice:** ordered Ready G6 minus first-11 SKIP, indices **[30, 40)**  
**Verification:** `scripts/verify_g6_effort_difficulty_batch3.py` → `batch_3_verification.json` (n=40 per D ∈ {0,5,10,15,20,25})

## Design principle (shared)

Difficulty is **effort / meaningful steps**, not raw magnitude.

- Continuous `difficulty` (LLM prior / slider) remains the generator prior; sampling maps D → **effort targets**.
- **Mode / structure splits** matter more than larger integers alone.
- Place-value ÷10ⁿ free where relevant (less central in this algebraic batch).
- Classroom G6 constraints: prefer `x`/`y`/`z` (no Greek), integers until mid/high D.

### Effort scale anchors

| D | Meaning |
|---|---|
| 0 | Very easy / minimal time |
| 5 | Standard simple |
| 10 | More involved / maybe extra trick |
| 15 | Clearly more work |
| 20 | Hard / awkward extras |
| 25 | Mean-to-assign-five-examples level |

### Batch type_ids

| # | type_id |
|---|---------|
| 30 | `g6_writing_algebraic_expressions` |
| 31 | `g6_evaluating_algebraic_expressions` |
| 32 | `g6_combining_like_terms` |
| 33 | `g6_distributive_property_area_diagrams_algebraic` |
| 34 | `g6_distributive_property_algebraic` |
| 35 | `g6_solutions_to_equations` |
| 36 | `g6_equations_tape_diagrams` |
| 37 | `g6_equations_hanger_diagrams` |
| 38 | `g6_equations_word_problems` |
| 39 | `g6_solutions_to_inequalities` |

---

## 1. `g6_writing_algebraic_expressions` — Writing algebraic expressions

**Generator:** `_verbal_expressions` (`generators/misc.py`)  
**Profile:** `algebra_expression` + continuous `difficulty`

### What increases difficulty
- Phrase **structure**: one-op → grouped “times the sum/quantity” → consecutive / binomial products / squares
- Max phrase operations and nested language
- Slightly larger constants at high D (secondary)

### What does NOT count
- Bigger constants alone on a one-op phrase (`17 more than a number` ≈ `3 more than a number`)
- Advanced wording that is still a single sum

### Mode split
| D | Pool |
|---|------|
| &lt;3 | simple one-op only |
| 3–8 | ~55% simple / ~45% standard |
| 8–14 | standard (grouped) only |
| 14–18 | mix standard + advanced |
| ≥18 | advanced-only (consecutive, products of binomials, powers) |

### Anchors
- **5:** mix; often `3 times the sum of a number and 7`
- **15:** standard grouping / two-op
- **25:** consecutive integers / squared quantities / binomial products

### Verification
**Ramp verified.** Means: 4.0 → 9.5 → 9.0 → 8.1 → 16.6 → 17.4 (mid plateau on standard pool; hard jump at advanced-only).

---

## 2. `g6_evaluating_algebraic_expressions` — Evaluating linear expressions

**Generator:** `evaluate_algebraic_expressions` (primitive evaluate + `expression_structure`)  
**G6 constraints:** `allow_greek=False`, `only_x` / `xyz` by D, integers until D≈12

### What increases difficulty
- Leaf / nest / scale budgets from continuous D (terms, parentheses, × unlock)
- Substitution arithmetic with signed values
- Nested `(w-2)*(-5)+…` style

### What does NOT count
- Larger substitution value alone on `3x+1`
- Greek variable letters (blocked for G6)

### Continuous D map
Shared structure engine: `n_terms ≈ 1+⌊log₂(1+D/1.5)⌋`, nest/scale unlocks with D.

### Anchors
- **5:** short affine `4x+2`
- **15:** parens + several ops
- **25:** deeper nest / more ops (linear policy)

### Verification
**Ramp verified.** Means: 8.2 → 10.4 → 14.8 → 13.9 → 14.8 → 14.9 (strong early climb; high-D soft plateau under linear policy).

---

## 3. `g6_combining_like_terms` — Combining like terms

**Generator:** `combining_like_terms` (primitive like_terms)  
**G6 tweak:** classroom D stretched ×1.8 so upgrade ladder fits 0–25 slider

### What increases difficulty
- Negatives; more like terms; many terms; second variable
- Term count past the mid mild band

### What does NOT count
- Larger positive coeffs alone on `2x+3x+1+4`
- Greek letters (blocked)

### Continuous D map
Primitive upgrades (negatives / more_like / many_terms / second_variable) after mid band; G6 stretch makes D≈10 already buy structure.

### Anchors
- **5:** ~3–4 positive terms
- **15:** negatives + extra likes
- **25:** many terms / second variable pressure

### Verification
**Ramp verified.** Means: 5.5 → 9.5 → 16.0 → 19.9 → 22.4 → 22.0.

---

## 4. `g6_distributive_property_area_diagrams_algebraic` — Area-model distributive

**Generator:** `Grade6VisualFramework(mode=area_model_algebraic)`

### What increases difficulty
- Larger outer/constant (secondary)
- **Subtraction inside** `k(x−c)`
- **Negative outer** `−k(x±c)`

### What does NOT count
- Same `k(x+c)` with only slightly larger k
- Asking to factor (wrong skill)

### Continuous D map
| D | Spec |
|---|------|
| &lt;4 | outer 2–4, const 1–5, + only |
| &lt;10 | outer 2–7, + only |
| &lt;16 | mix − inside |
| &lt;22 | − inside dominant; sometimes negative outer |
| ≥22 | negative outer common; larger awkward products |

### Anchors
- **5:** `6(x+4)` style
- **15:** `k(x−c)` mix
- **25:** `−11(x−4)` style

### Verification
**Ramp verified.** Means: 5.0 → 5.5 → 9.2 → 8.2 → 12.2 → 16.0.

---

## 5. `g6_distributive_property_algebraic` — Distributive, algebraic

**Generator:** G6 effort ladder `_g6_sample_distributive_algebraic` (non-G6 keeps constructive primitive)

### What increases difficulty
- Form: easy `k(x+c)` → signed inside → var-outer `x(a+b)` → negative outer → fraction outer
- Expansion bookkeeping with signs / fractions

### What does NOT count
- Weird cancel-clutter presentations at low D (ladder avoids them)
- Magnitude-only on positive `k(x+c)`

### Continuous D map
| D | Form mix |
|---|----------|
| &lt;4 | small positive const-outer |
| &lt;10 | larger const-outer, light − |
| &lt;16 | signed inside + some var-outer |
| &lt;22 | negative outer common |
| ≥22 | fraction outer or hard signed |

### Anchors
- **5:** `5(x+3)`
- **15:** `x(4+7)` / `6(x−9)`
- **25:** `½(x−5)` or large signed outer

### Verification
**Ramp verified.** Means: 5.0 → 8.1 → 11.2 → 11.3 → 15.3 → 14.3.

---

## 6. `g6_solutions_to_equations` — Solutions to equations

**Generator:** `check_equation_solution` (rewritten for continuous D)

### What increases difficulty
- Equation structure to **check by substitution**: one-step → two-step `ax+b` → negatives → both-sides-x → fractional coeffs
- Nearby distractor candidates

### What does NOT count
- Asking students to *solve* for x (wrong topic — this is check-yes/no)
- Huge RHS alone on `2x+3=…`

### Continuous D map
| D | Equation family |
|---|---------------|
| &lt;4 | `x+b=c` or `ax=c` |
| &lt;10 | `ax+b=c` positive |
| &lt;16 | negatives / subtraction |
| &lt;21 | larger / both-sides x |
| ≥21 | fractional `a` |

### Anchors
- **5:** `7x+4=74?`
- **15:** signed two-step
- **25:** `⅘x + 4 = …`

### Verification
**Ramp verified.** Means: 5.5 → 9.9 → 11.5 → 11.6 → 12.9 → 15.6.

---

## 7. `g6_equations_tape_diagrams` — Tape diagrams

**Generator:** `Grade6VisualFramework._build_tape_diagram`

### What increases difficulty
- Style: uniform equal-x → mix → **nonuniform missing-part**
- More segments / larger part values on nonuniform

### What does NOT count
- Same uniform `3x=total` with only a larger solution

### Continuous D map
| D | Style |
|---|-------|
| &lt;5 | uniform, 2–3 parts |
| &lt;12 | mix uniform/nonuniform |
| &lt;18 | mostly nonuniform |
| ≥18 | nonuniform, 4–6 segments, larger values |

### Anchors
- **5:** small uniform or early missing-part
- **15:** nonuniform missing value
- **25:** longer nonuniform tapes

### Verification
**Ramp verified.** Means: 6.6 → 9.6 → 10.9 → 13.4 → 14.6 → 15.0.

---

## 8. `g6_equations_hanger_diagrams` — Hanger diagrams

**Generator:** `Grade6VisualFramework` hanger branch

### What increases difficulty
- Number of equal hanging parts
- Solution size (division bookkeeping)
- Still one-step `parts·x = total` (topic skill)

### What does NOT count
- Multi-step hanger equations (not generated)
- Inequality hangers (separate leaf)

### Continuous D map
| D | parts / solution |
|---|------------------|
| &lt;4 | 2–3 parts, sol 2–6 |
| &lt;10 | 2–4 / 3–10 |
| &lt;16 | 3–6 / 4–14 |
| &lt;22 | 4–7 / 5–18 |
| ≥22 | 5–9 / 6–24 |

### Anchors
- **5:** `4x=28`
- **15:** more parts
- **25:** `7x=42`–scale with larger parts

### Verification
**Ramp verified.** Means: 6.1 → 8.0 → 12.0 → 11.0 → 15.7 → 20.5.

---

## 9. `g6_equations_word_problems` — Equations word problems

**Generator:** primitive `wp_one_step_equation` with G6 classroom constraints

### What increases difficulty
- Underlying one-step equation number lane / signs / fractions from continuous D
- Integer-only until mid D; fractions / negatives unlock later

### What does NOT count
- Two-step story equations (different leaf)
- Story vocabulary alone without harder equation

### Continuous D map
Equation primitive spends D; G6 forces `integers_only` for D&lt;12 and `xyz`/`only_x` lanes.

### Anchors
- **5:** `x+1=3` style
- **15:** messier one-step
- **25:** fractional / signed one-step

### Verification
**Ramp verified.** Means: 9.0 → 12.1 → 14.8 → 18.5 → 19.1 → 18.2.

---

## 10. `g6_solutions_to_inequalities` — Solutions to inequalities

**Generator:** `GraphInequalityFramework` (number line) + `_continuous_inequality_boundary`

### What increases difficulty
- Strict → inclusive symbols
- Negative / zero / awkward integer boundaries
- Half-integer boundaries at high D
- (Writing leaf separately uses word→symbol; this leaf is graph-given)

### What does NOT count
- Larger positive boundary alone on `x>3`
- Solving one-step inequalities (different leaf: `g6_solving_and_graphing_one_step_inequalities`)

### Continuous D map
| D | Boundary / symbol |
|---|-------------------|
| &lt;4 | strict, 1–6 |
| &lt;9 | open/closed, negatives |
| &lt;15 | awkward non-benchmark ints |
| &lt;20 | larger awkward ints |
| ≥20 | half-integers common |

### Anchors
- **5:** `x≥−3` style
- **15:** awkward integers + inclusive
- **25:** half-integer marks / wide window

### Verification
**Ramp verified.** Means: 4.0 → 6.9 → 7.4 → 9.4 → 17.3 → 13.1 (high-D half-integer mix; slight 25 dip vs 20).

---

## Implementation map (this batch)

| Piece | Location |
|-------|----------|
| Writing continuous phrase ladder | `generators/misc.py` `_verbal_complexity_from_continuous` |
| G6 algebra constraints + like-terms stretch | `generators/primitive_g6.py` `_g6_algebra_settings` |
| G6 distributive ladder | `generators/primitive_g6.py` `_g6_sample_distributive_algebraic` |
| Check-solution continuous families | `generators/grade_level.py` `check_equation_solution` |
| Tape / hanger / area-model continuous | `frameworks/number.py` `Grade6VisualFramework` |
| Inequality boundary continuous + halves | `frameworks/graphing.py` `_continuous_inequality_boundary` |
| WP G6 integer/var constraints | `generators/primitive_linear.py` `_wp_generator` |
| Verifier | `scripts/verify_g6_effort_difficulty_batch3.py` |

## How to re-verify

```powershell
$env:PYTHONPATH='.'; $env:QE_LOG_GENERATED='0'
python scripts/verify_g6_effort_difficulty_batch3.py
```

Raw means: `scripts/output/topic_fit/g6_difficulty/batch_3_verification.json`.
