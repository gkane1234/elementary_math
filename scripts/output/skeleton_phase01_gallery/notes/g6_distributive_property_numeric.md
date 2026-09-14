# Notes — `g6_distributive_property_numeric` (`g6_distributive_property_numeric`)

- **Display name:** Distributive property, numeric
- **Catalog chapter:** Grade 6 — Numeric Expressions, Exponents, and the Order of Operations
- **Generator key:** `g6_distributive_property_numeric`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Expand a numeric distributive product and simplify to a single number (or leave expanded product if that is the named step).
- **D=0:** small integers, e.g. $2(3+4)$ or $(1+2)(-2)$.
- **High D (≈16–22):** larger factors / more addends inside; still **numeric** (no $x$).
- **Must not:** jump to algebraic $k(x+b)$ (that is `g6_distributive_property_algebraic`); dump FOIL of two binomials as the only mode.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`, seed 101.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\left(1 + 2\right)\left(-2\right)$` | `$-2\cdot 2 - 2\cdot 1$` | |
| 8 | 101 | `$\left(-1 + 2 + 4\right)\left(-2\right)$` | `$- -2\cdot 1 - 2\cdot 2 - 2\cdot 4$` | |
| 16 | 101 | `$7.8\left(2 + \frac{1}{5} + \frac{1}{3}\right)$` | `$7.8\cdot 2 + 7.8\cdot \frac{1}{3} + 7.8\cdot \frac{1}{5}$` | |
| 22 | 101 | `$7.8\left(\frac{1}{5} + \frac{1}{9} + 2\right)$` | `$7.8\cdot 2 + 7.8\cdot \frac{1}{5} + 7.8\cdot \frac{1}{9}$` | |

Opt-out flag used: _none (live default)._

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§7.3 Distributive Property** | https://openstax.org/books/prealgebra-2e/pages/7-3-distributive-property | Numeric $a(b+c)=ab+ac$; Try Its with integers |
| OpenStax Elementary Algebra 2e **§1.5** | https://openstax.org/books/elementary-algebra-2e/pages/1-5-properties-of-real-numbers | Distributive over ± |

## Variety notes / UNCLEAR flag

**UNCLEAR:** old answers are often left as uncombined distributed products (e.g. $-2\cdot 2 - 2\cdot 1$) rather than a simplified integer. Confirm whether gold is “rewrite with distributive” or “evaluate”.

## Limitations

- Flags: **UNCLEAR**.
- Answer key may stay as an uncombined distributed form instead of a single integer — gold not locked for evaluate-vs-rewrite.
- Difficulty mainly grows coefficients; form variety is thin vs OpenStax 7.3 (factor on the right, fractions).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** existing `PRIM_DISTRIBUTIVE` / `sample_distributive_numeric` (already wired).
- **New:** none this pass.
- **Not this pass:** no generator rewrite until gold (rewrite vs evaluate) is locked.

Suggested family: **affine** / number distributive.
