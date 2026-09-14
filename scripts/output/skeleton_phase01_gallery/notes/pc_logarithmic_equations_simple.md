# Notes — `pc_logarithmic_equations_simple` (`Logarithmic equations, simple`)

- **Course:** Precalculus
- **Category:** Precalculus — Exponential and Logarithmic Expressions
- **Generator:** `log_equation_simple` (OpenStax form catalog `precalculus_exp_log`)
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve one-log / definition logarithmic equations (optional algebra around a single log).
- **D=0:** Bare `log_b(x)=k` → `x=b^k` (OpenStax §4.6 definition / Ex. 11).
- **High D (≈16–22):** Numeric hardness (larger bases) then format unlocks — `log_b(ax+c)=k`, `a log_b(x)+c=d`. No product/quotient/extraneous (those belong on the hard leaf).
- **Must not:** Multi-log product equations or planted extraneous on this leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` (old path = default). Seed=101 before/after engine work.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\log_{3}(x) = 3$` | `$x = 27$` | definition (after fix; D=0 no longer coerced to 6) |
| 8 | 101 | `$\log_{5}\left(3x + 101\right) = 3$` | `$x = 8$` | linear argument unlock |
| 16 | 101 | `$\log_{5}\left(4x + 121\right) = 3$` | `$x = 1$` | linear / algebra mix across seeds |
| 22 | 101 | `$\log_{5}\left(4x + 121\right) = 3$` | `$x = 1$` | same pool; algebra_coeff also common |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §4.6 | https://openstax.org/books/precalculus-2e/pages/4-6-exponential-and-logarithmic-equations | one-log definition; optional linear argument / coeff algebra |

Local HTML (if mined): `scripts/output/example_mining/precalculus-2e/stage1/4-6-exponential-and-logarithmic-equations.md`

## Variety notes / flags

- D=0 is definition-only across seeds. Mid/high D rotates definition / linear_argument / algebra_coeff.

## Proposed engine (reuse vs new)

- **Reuse:** `log_equation_simple` + simple-leaf forms in `precalculus_exp_log`.
- **New:** not needed.

## Limitations

- **Difficulty scaling:** Structural unlocks are modest by design (stay “simple”). Residual: fixed seed can repeat a linear stem from D=16→22; across seeds algebra_coeff appears.
- **OpenStax:** Definition + algebra-before-definition covered; product/extraneous intentionally deferred to hard leaf.
- **Engine:** Wired. Bugfix: `difficulty or 6` no longer collapses D=0 to 6 for form selection.
