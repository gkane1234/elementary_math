# Notes — `pc_logarithmic_equations_hard` (`Logarithmic equations, hard`)

- **Course:** Precalculus
- **Category:** Precalculus — Exponential and Logarithmic Expressions
- **Generator:** `log_equation_simple` (OpenStax form catalog `precalculus_exp_log`)
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve multi-step logarithmic equations (definition with linear argument → one-to-one → product/quotient properties → quadratic with extraneous).
- **D=0:** Multi-step but simplest hard shapes — `log_b(ax+c)=k` or `a log_b(x)+c=d` (OpenStax §4.6 Ex. 9–10 / easy hard exercises). Not bare `log_b(x)=k` (that is the simple leaf).
- **High D (≈16–22):** Format unlocks — product `log(x)+log(x−p)=k` with extraneous discard; quotient difference; one-to-one with `x^2` (OpenStax §4.6 Ex. 12). Numeric hardness via bases/coefficients first.
- **Must not:** Same easy definition stamp as the simple leaf at every D; wrong-topic shapes.

## What old path actually produced (real latex, D=0/8/16/22)

**Before (flat easy — same as simple leaf):** live default stamped `log_b(x)=k` at all D.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\log_{3}(x) = 5$` | `$x = 243$` | definition only |
| 8 | 101 | `$\log(x) = 2$` | `$x = 100$` | definition only |
| 16 | 101 | `$\log_{11}(x) = 2$` | `$x = 121$` | definition only |
| 22 | 101 | `$\log_{11}(x) = 2$` | `$x = 121$` | definition only |

**After (form-driven D ladder):** live `_generate_for_type` seed=101.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\log_{3}\left(3x + 3\right) = 3$` | `$x = 8$` | linear argument |
| 8 | 101 | `$\log_{5}\left(2x + 9\right) = \log_{5}\left(x + 15\right)$` | `$x = 6$` | one-to-one |
| 16 | 101 | `$\log_{5}\left(x + 27\right) - \log_{5}(x) = \log_{5}(4)$` | `$x = 9$` | quotient / condense |
| 22 | 101 | `$\log_{5}\left(x + 27\right) - \log_{5}(x) = \log_{5}(4)$` | `$x = 9$` | quotient (also product / quadratic across seeds) |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §4.6 | https://openstax.org/books/precalculus-2e/pages/4-6-exponential-and-logarithmic-equations | linear-arg definition; algebra around log; one-to-one; product/quotient; `log(x^2)=log(linear)` + extraneous |
| OpenStax Intermediate Algebra 2e §10.5 | https://openstax.org/books/intermediate-algebra-2e/pages/10-5-solve-exponential-and-logarithmic-equations | product property equations with domain check |

Local HTML (if mined): `scripts/output/example_mining/precalculus-2e/stage1/4-6-exponential-and-logarithmic-equations.md`

## Variety notes / flags

- Hard leaf forms rotate by D (linear → 1-to-1 / algebra → product / quotient / quadratic). Across seeds at D=22: product_sum, quotient_diff, one_to_one_quadratic.

## Proposed engine (reuse vs new)

- **Reuse:** `log_equation_simple` + `precalculus_exp_log` form kinds (`linear_argument`, `algebra_coeff`, `one_to_one`, `product_sum`, `quotient_diff`, `one_to_one_quadratic`).
- **New:** not needed.

## Limitations

- **Variety:** Quotient / product / quadratic dominate high D; linear one-to-one is capped (`d_max`) so it does not crowd D≥16. Change-of-base *as an equation* and applied log models remain out of scope (separate leaves / deferred `exp_log_models`).
- **Difficulty scaling:** Real structural unlocks (not cost-pad). Residual: at a fixed seed, D=16 and D=22 can share a quotient stem; across seeds high-D modes diversify.
- **OpenStax:** §4.6 / IA §10.5 shapes covered; no applied radioactive-decay word problems on this leaf.
- **Engine:** Wired. Simple leaf stays on definition → linear → algebra (no product/extraneous).
