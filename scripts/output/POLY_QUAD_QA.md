# Polynomial / factoring / quadratic solve — QA

Scope: Algebra 1 polynomials + quadratic solve methods (naming through completing the square).

## Verification table

| Type | E sample | M sample | H sample | Topic? | Easy monic? | Hard harder? | Answers? | Status |
|------|----------|----------|----------|--------|-------------|--------------|----------|--------|
| `polynomial_naming` | `x-3` → linear | cubic | quartic | Y | n/a | Y (degree ↑) | Y | Pass |
| `polynomial_add_subtract` | deg≤2 | deg≤3 | deg≤5 | Y | n/a | Y | Y | Pass |
| `polynomial_multiply` | monic binoms | non-monic / tri | long products | Y | Y | Y | Y | Pass |
| `polynomial_multiply_special` | `(x+4)²` | larger monic | `(5x+1)²` | Y | Y | Y (a≠1) | Y | **Fixed** |
| `polynomial_factoring_common_factor` | `2(x²+3x+1)` | numeric GCF | `9x(…)` | Y | Y (remaining) | Y | Y | **Fixed** |
| `quadratic_factoring` | monic normal | a≠1 normal | DOS/PST deg 2 | Y | Y | Y (methods) | Y | **Fixed** |
| `polynomial_factoring_special_cases` | monic PST/DOS | cubes / a≠1 | higher powers | Y | Y | Y | Y | **Fixed** (easy monic) |
| `polynomial_factoring_grouping` | cubic grouping | non-monic cubic | non-monic cubic | Y | Y | Y (a≠1) | Y | **Fixed** |
| `quadratic_solve_by_graphing` | monic =0 | a≠1 / factored | wider roots, deg 2 | Y | Y | Y | Y | **Fixed** |
| `quadratic_square_roots` | `x²=k` | vertex a≠1 | CTS / radicals | Y | Y | Y | Y | Pass |
| `quadratic_factoring_equations` | monic roots | a≠1 int roots | fractional roots | Y | Y | Y | Y | **Fixed** |
| `quadratic_formula` | int monic | int a≠1 | exact radicals | Y | Y | Y | Y | **Fixed** |
| `quadratic_discriminant` | monic D | a≠1 D | larger D | Y | Y | Y | Y | Pass‡ |
| `quadratic_completing_square_constant` | `c=(b/2)²` | larger \|b\| | fractional c | Y | Y | Y | Y | **Fixed** |
| `quadratic_completing_square_solve` | monic CTS | a≠1 | radicals / none | Y | Y | Y | Y | **Fixed** |

† Grouping medium/hard now uses leading a≠1 via `_leading_coefficient`.  
‡ Degenerate `x²`-only prompts avoided; D classification verified.

## Failures fixed (samples)

### Completing the square — wrong answer keys
- **Before:** `x²−4x+c` → answer `5` (used `h²+k`). **After:** `c=4`.
- **Before:** `x²−6x+11=0` → `x=3±1.41` (sign of k inverted). **After:** no real / correct ± form from `(x+h)²=−k/a`.

### Factoring equations — integer division on non-monic factors
- **Before:** `9x²+6x+1=0` → `x=-1,-1` (`-1//3`). **After:** `x=-1/3`.

### Common factor only — wrong topic
- **Before:** full binomial factoring (`x²+4x−5→(x−1)(x+5)`). **After:** GCF only (`2x²+6x+2→2(x²+3x+1)`).

### Quadratic expressions hard — not quadratic
- **Before:** hard used cubes/substitution deg 3–4. **After:** stays deg 2; unlocks DOS/PST + larger coeffs.

### Grouping easy/medium — not grouping
- **Before:** easy deg-2 presets fell back to normal/PST. **After:** all tiers deg 3 + `grouping` method.

### Multiply special — flat difficulty
- **Before:** E/M/H identical monic patterns. **After:** hard uses `(ax±b)²` / `(ax+b)(ax−b)`.

### Quadratic formula — float keys + ignored `integer_only`
- **Before:** `2x²+7x−8=0` → `x=0.908,-4.41`. **After:** integer-root construction when `integer_only`; else exact `\frac{-b\pm\sqrt{D}}{2a}`.

### Quadratic formula — unreduced radicals
- **Before:** `3x²+20x+16=0` → `\frac{-20\pm4\sqrt{13}}{6}`. **After:** `\frac{-10\pm2\sqrt{13}}{3}`.

### Grouping — ignored non-monic presets
- **Before:** medium/hard still `(x−r)(x²+k)`. **After:** `(a x²+b)(x+r)` with a≠1 when `monic_only=False`.

### Solve by graphing hard — cubics under Quadratic Functions
- **Before:** hard `max_degree=3`. **After:** stays quadratic; wider roots / a≠1.

## Deferred (with evidence)

| Item | Evidence | Why deferred |
|------|----------|--------------|
| Common-factor medium always numeric GCF | ~45% of medium omit `x^k` by design | Acceptable mix; could force variable GCF on medium if desired |
| `polynomial_factoring` profile hard still cubes/grouping | Profile used by shared “all techniques” paths | Correct for that profile; `quadratic_factoring` now has its own tiers |
| Long division (edge of scope) | Spot-checked clean; not deeply audited this pass | Outside core solve-method focus |

## Files touched
- `question_engine/generators/basic.py`
- `question_engine/settings/presets.py`
- `packages/polynomial_core/special_products.py`
- `packages/polynomial_core/factoring.py`
- `question_engine/tests/test_difficulty_presets.py`
- `question_engine/tests/test_poly_quad_polish.py`
- `lib/difficulty-presets.ts`
