# Notes — `a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple`

- **Display name:** Logarithmic equations, simple
- **Category:** Algebra 2 — Exponential and Logarithmic Expressions
- **Generator:** `log_equation_simple`
- **Already on skeleton?** no (stub gallery / shared generator)
- **Suggested family:** solve

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve simple logarithmic equations via definition / light algebra.
- **D=0:** `log_b(x)=k`.
- **High D (≈16–22):** `log_b(ax+c)=k` (linear argument).
- **Must not:** Multi-log / extraneous (hard leaf).

## What live path actually produced (real latex, D=0/8/16/22)

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\log_{3}(x) = 3$` | `$x = 27$` | definition |
| 8 | 101 | `$\log_{5}\left(3x + 101\right) = 3$` | `$x = 8$` | linear argument |
| 16 | 101 | `$\log_{5}\left(4x + 121\right) = 3$` | `$x = 1$` | linear argument |
| 22 | 101 | `$\log_{5}\left(4x + 121\right) = 3$` | `$x = 1$` | linear argument |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Intermediate Algebra 2e §10.3 / §10.5 | https://openstax.org/books/intermediate-algebra-2e/pages/10-5-solve-exponential-and-logarithmic-equations | Simple log equations |

## Variety notes / flags

- Shares engine with PC simple leaf; A2 catalog forms `log_equation_basic` / `log_equation_linear_argument`.

## Limitations

- **Difficulty scaling:** Definition → linear argument unlocks; no multi-log on this leaf.
- **OpenStax:** Matches IA simple log-equation shapes.
- **Engine:** Shared `log_equation_simple`.

## Proposed engine (reuse vs new)

- **Reuse:** `log_equation_simple` — implemented.
