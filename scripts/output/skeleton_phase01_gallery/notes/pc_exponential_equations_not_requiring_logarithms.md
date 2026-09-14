# Notes — `pc_exponential_equations_not_requiring_logarithms` (`Exponential equations not requiring logarithms`)

- **Course:** Precalculus
- **Category:** Precalculus — Exponential and Logarithmic Expressions
- **Generator:** `exponential_equation_simple`
- **Suggested family:** solve

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve same-base / rewrite-to-common-base exponential equations (no logs).
- **D=0:** `$b^{x}=b^{k}$` / `$b^{x}=b^{k}$` style integer exponent.
- **High D (≈16–22):** Rewrite both sides to a common base (OpenStax §4.6 Ex. 2).
- **Must not:** Equations that require taking logs.

## What live path actually produced (real latex, D=0/8/16/22)

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$4^{x} = 4$` | `$x = 1$` | same base |
| 8 | 101 | `$8^{x + 2} = 16^{x + 1}$` | `$x = 2$` | rewrite common base |
| 16 | 101 | `$8^{x + 2} = 16^{x + 1}$` | `$x = 2$` | rewrite (seed-locked template) |
| 22 | 101 | `$8^{x + 2} = 16^{x + 1}$` | `$x = 2$` | rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §4.6 | https://openstax.org/books/precalculus-2e/pages/4-6-exponential-and-logarithmic-equations | same-base; rewrite common base |

## Variety notes / flags

- D≥6 unlocks rewrite templates; pool is small (4 textbook pairs) so same seed can plateau.

## Proposed engine (reuse vs new)

- **Reuse:** `exponential_equation_simple` + PC forms `exp_same_base` / `exp_rewrite_common_base`.

## Limitations

- **LIMITATIONS** — Rewrite template pool is small; high-D stems often recycle the same OpenStax pairs across seeds.
- **Difficulty scaling:** Real unlock same-base → rewrite; not bare number inflation.
- **OpenStax:** Fractional-root common-base (Ex. 3) not yet a separate form.
