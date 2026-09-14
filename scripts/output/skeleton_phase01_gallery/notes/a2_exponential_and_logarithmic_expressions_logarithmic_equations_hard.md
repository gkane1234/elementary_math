# Notes — `a2_exponential_and_logarithmic_expressions_logarithmic_equations_hard`

- **Display name:** Logarithmic equations, hard
- **Category:** Algebra 2 — Exponential and Logarithmic Expressions
- **Generator:** `log_equation_simple`
- **Already on skeleton?** no (stub gallery)
- **Suggested family:** solve

---

## What the question should look like (D=0 vs high D)

- **Skill:** Multi-step logarithmic equations with properties / extraneous checks (IA §10.5).
- **D=0:** `log_b(ax+c)=k` (simplest multi-step).
- **High D (≈16–22):** One-to-one, product property + extraneous, quadratic one-to-one.
- **Must not:** Bare `log_b(x)=k` (simple leaf).

## What live path actually produced (real latex, D=0/8/16/22)

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\log_{3}\left(3x + 3\right) = 3$` | `$x = 8$` | linear argument |
| 8 | 101 | `$\log_{5}\left(2x + 9\right) = \log_{5}\left(x + 15\right)$` | `$x = 6$` | one-to-one |
| 16 | 101 | `$\log_{2}(x) + \log_{2}(x - 2) = 3$` | `$x = 4;\ x = -2 \text{ (extraneous)}$` | product + extraneous |
| 22 | 101 | `$\log_{2}(x) + \log_{2}(x - 2) = 3$` | `$x = 4;\ x = -2 \text{ (extraneous)}$` | product + extraneous |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Intermediate Algebra 2e §10.5 | https://openstax.org/books/intermediate-algebra-2e/pages/10-5-solve-exponential-and-logarithmic-equations | Harder log equations (extraneous / multi-log) |

## Variety notes / flags

- Wired to A2 catalog forms (`log_equation_hard_*`, `log_equation_properties`, `log_equation_one_to_one`, `log_equation_quadratic_1to1`).

## Limitations

- **Difficulty scaling:** Honest form unlocks; D=0 no longer stamps definition-only.
- **OpenStax:** Quotient-diff form is PC-tagged; A2 high D leans product / quadratic 1-to-1.
- **Engine:** Shared `log_equation_simple` with PC.

## Proposed engine (reuse vs new)

- **Reuse:** `log_equation_simple` + `algebra2_exp_log` forms — implemented.
