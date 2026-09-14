# Notes — `pc_exponential_equations_requiring_logarithms` (`Exponential equations requiring logarithms`)

- **Course:** Precalculus
- **Category:** Precalculus — Exponential and Logarithmic Expressions
- **Generator:** `exponential_equation_with_log`
- **Suggested family:** solve

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve exponential equations that need logarithms (RHS not a pure power of the same base).
- **D=0:** `b^{x}=k` with answer `$x=\log_b(k)$` (OpenStax “use logs”).
- **High D (≈16–22):** Different bases `a^{x+c}=b^{x}`, then continuous `$A e^{kx}=B$`.
- **Must not:** Same-base pure powers solvable without logs (those belong on not-requiring).

## What live path actually produced (real latex, D=0/8/16/22)

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$3^{x} = 24$` | `$x = \log_{3}(24)$` | needs log |
| 8 | 101 | `$3^{x + 2} = 6^{x}$` | `$x = \dfrac{2\ln(3)}{\ln(6) - \ln(3)}$` | different bases |
| 16 | 101 | `$10 e^{2 x} = 100$` | `$x = \dfrac{\ln\!\left(\dfrac{100}{10}\right)}{2}$` | $A e^{kx}=B$ |
| 22 | 101 | `$10 e^{2 x} = 100$` | `$x = \dfrac{\ln\!\left(\dfrac{100}{10}\right)}{2}$` | $A e^{kx}=B$ |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §4.6 | https://openstax.org/books/precalculus-2e/pages/4-6-exponential-and-logarithmic-equations | take log both sides; different bases; $y=Ae^{kt}$ |

## Variety notes / flags

- Prior path stamped `$b^{cx}=b^{cx}$` integer powers (no log needed) and scientific-notation RHS — fixed.

## Proposed engine (reuse vs new)

- **Reuse:** `exponential_equation_with_log` with D-banded OpenStax shapes.

## Limitations

- **Difficulty scaling:** Shape bands at D≈0 / 8 / 16; within-band variety is numeric.
- **OpenStax:** Applied radioactive-decay word problems still deferred (`exp_log_models`).
- **Answers:** Exact log / ln forms (not decimal approximations).
