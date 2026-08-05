# Calculus derivative function / method knobs

**Date:** 2026-07-28

## Goal

Richer Calc 1 **derivative** generation with continuous-D difficulty and
**selectable function/method allow-lists**, patterned on OpenStax Calculus
Volume 1 Chapter 3 (differentiation rules, trig, chain, exp/log).

## Settings (worksheet UI / API)

| Key | Group | Role |
|-----|-------|------|
| `allow_trig` | `derivative_functions` | sin/cos/tan/… |
| `allow_exp` | `derivative_functions` | \(e^{u}\) |
| `allow_log` | `derivative_functions` | \(\ln\), \(\log_b\) |
| `allow_hyperbolic` | `derivative_functions` | sinh/cosh |
| `allow_roots` | `derivative_functions` | \(\sqrt{\,}\), \(x^{p/q}\) |
| `allow_invtrig` | `derivative_functions` | arcsin/arccos/arctan |
| `allow_chain` / `require_chain` | `derivative_methods` | composition |
| `allow_product` / `require_product` | `derivative_methods` | product rule |
| `allow_quotient` / `require_quotient` | `derivative_methods` | quotient rule |
| `allow_implicit` | `derivative_methods` | implicit (leaf-specific) |

Profile: `derivatives` (`question_engine/settings/domains/calculus.py`).
Per-generator defaults live in `generator_profiles.py`.

## Topic-leaf defaults

| Generator / leaf | Specials | Methods |
|------------------|----------|---------|
| `derivative_power_rule` | OFF (roots ON for fractional powers) | chain/product/quotient OFF |
| `derivative_product_rule` | OFF | `require_product`; chain optional by D |
| `derivative_quotient_rule` | OFF | `require_quotient` |
| `derivative_chain_rule` | OFF (roots ON); unlock specials via settings | `require_chain` |
| `derivative_trigonometric` | **trig ON**; other specials OFF | chain/product/quotient allowed, D-gated |
| `derivative_ln_exp` / `other_base` | exp+log ON | chain (+ product for ln/exp) |
| `derivative_inverse_trig` | invtrig ON | chain allowed |

## Continuous D behavior

Implemented in `question_engine/frameworks/primitives/derivatives.py` using
`DifficultyFactor` + `select_upgrades` (costs in `difficulty_knobs.json` →
`derivatives`).

D spends on:

- **ops** — extra terms / higher powers
- **methods** — product, quotient, chain (when allowed)
- **nesting** — `chain_depth_2` when nested unlock + allow_chain
- **classes** — trig / exp / log / roots / invtrig / hyperbolic (when allowed)
- **mix_classes** — bias toward ≥2 function classes in one prompt

Soft unlock floors (within an allowed class): trig≈6, exp≈7, log≈12,
roots≈4, invtrig≈10, hyperbolic≈16, nested≈14.

**Hard gate:** `allow_*=false` never appears, regardless of D.
**Force-in:** `allow_*=true` on an algebraic leaf spends class upgrades when D
can afford them.

## Metadata

Each sampled question includes:

- `function_classes` — e.g. `["algebraic"]`, `["algebraic","trig"]`
- `methods_used` — e.g. `["power"]`, `["chain","power"]`, `["product"]`
- `chain_depth` — nesting depth (0 = no composition)

## Example prompts

**Easy (power rule, D≈0–3)** — algebraic only:

```tex
\frac{d}{dx}\left[3x^{4}\right]
```

**Hard (chain + specials allowed, D≈20)** — deeper nest / mixed classes:

```tex
\frac{d}{dx}\left[\sin\left(\left(2x+1\right)^{3}\right)\right]
```

```tex
\frac{d}{dx}\left[\left(x^{2}+1\right)\ln(x)\right]
```

**Trig leaf (defaults)** — trig present; exp/log absent unless settings flip:

```tex
\frac{d}{dx}\left[x\sin(x)\right]
```

## OpenStax grounding

Stage-1 inventories under
`scripts/output/example_mining/calculus-volume-1/stage1/`:

- `3-3-differentiation-rules` — power / product / quotient / combined
- `3-5-derivatives-of-trigonometric-functions` — trig × poly product/quotient
- `3-6-the-chain-rule` — \((ax+b)^n\), \(\sin(g(x))\), nested
- `3-9-derivatives-of-exponential-and-logarithmic-functions`

## Code map

| Piece | Path |
|-------|------|
| Sampler / allows / upgrades | `question_engine/frameworks/primitives/derivatives.py` |
| Knob costs / unlock D | `difficulty_knobs.json` → `derivatives` |
| Settings fields | `settings/domains/calculus.py` |
| Leaf defaults | `settings/generator_profiles.py` |
| Generators | `generators/calculus_derivative_rules.py` (framework path) |
| Tests | `tests/test_calc_derivative_function_knobs.py` |
| Galleries | `python scripts/build_calc_continuous_galleries.py` |

## Verify

```powershell
$env:PYTHONPATH='.'
python -m pytest question_engine/tests/test_calc_derivative_function_knobs.py question_engine/tests/test_calculus_derivative_rules.py question_engine/tests/test_continuous_d_ladder_deepening.py -q
python scripts/build_calc_continuous_galleries.py
```
