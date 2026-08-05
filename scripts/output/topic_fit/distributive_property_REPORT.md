# Topic-fit QA report — distributive form diversity

Scope: `distributive_property`, `g6_distributive_property_numeric`, `g6_distributive_property_algebraic`

Generated sample pack: `scripts/output/topic_fit/by_topic/a1_distributive_property/` (+ g6 numeric/algebraic siblings)

## Forms added (framework upgrades)

| Upgrade | Cost | Effect |
|---------|-----:|--------|
| `factor_right` | 0.5 | Unlocks left/right mix for scaled sums |
| `signed_inside` | 1.0 | Allows negatives inside the sum |
| `three_terms` | 1.5 | Trinomial inside: `k(a+b+c)` / `(a+b+c)k` |
| `two_binomials` | 4.5 | `(a+b)(c+d)` (numeric) or `(var+a)(b+c)` (algebraic) |

**form_id:** `scaled_sum` | `two_binomials`  
**factor_side:** `left` | `right` | `both`  
**n_terms_inside:** 2 or 3 (per sum group)

Notation (`juxtapose` / `*` / `\cdot` / `\times`) comes from the presentation layer (not separate prompt templates). Rendering uses `render_scaled_sum` / `render_product` / expand helpers.

## D mapping (observed mix, n=80 integers)

| D | scaled_sum | two_binomials | notes |
|--:|----------:|-------------:|-------|
| 0 | 100% | 0% | Classic `k(a+b)`; soft ~12% right factor |
| 10 | ~86% | ~14% | Trinomials common; explicit `*` appears |
| 20 | ~60% | ~40% | Binomial×binomial frequent; right factor + trinomials still present |

## Spot-check (2 easy vs 2 hard)

| Band | Prompt | Answer | Meta |
|------|--------|--------|------|
| Easy D=0 | $2(2+2)$ | $2\cdot2+2\cdot2$ | `scaled_sum` / left / n=2 |
| Easy D=0 | $1(3+1)$ | $1\cdot1+1\cdot3$ | `scaled_sum` / left / n=2 |
| Hard D=20 | $(1/6+1/8+7.55)3$ | trinomial expand | `scaled_sum` / right / n=3 |
| Hard D=20 | $(1/5+7/2)*(1/2+0.5)$ | FOIL-style · products | `two_binomials` / both |

G6 algebraic: easy $3(x+1)$ (`const_outer`); hard $(4+2+z)(-3)$ (right factor, trinomial).

## Verification table

| Type | E sample | M sample | H sample | Topic? | Method? | Hard harder? | Status |
|------|----------|----------|----------|--------|---------|--------------|--------|
| `distributive_property` | $3(1+2)$ | $1*(4+3-1)$ | $(1+1.3)(2/3+0.02)$ | Y | Y distribute | Y | Pass |
| `g6_distributive_property_numeric` | $(3+2)2$ | $(5+2)(3+1)$ | $(8-3.64)*(1.64+1/5)$ | Y | Y | Y | Pass |
| `g6_distributive_property_algebraic` | $x(1+3)$ | $-2(y+1+4)$ | $(4/5+y)(1+1/4)$ | Y | Y | Y | Pass |

## Checks run

- `pytest question_engine/tests/test_distributive_forms.py` + `test_presentation.py` — 27 passed
- Live gallery regen via `build_verified_topic_galleries.py --type-id … --force-live`
- Form-mix Counter at D=0/10/20; answers use `\cdot` expand keys

## Notes

- Removed G6 hardcoded ladder; algebraic path uses the same primitive + classroom settings.
- Algebraic `two_binomials` keeps one variable total (`(x+a)(b+c)`) so it stays distributive, not a full poly-FOIL lesson.
