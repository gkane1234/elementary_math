# Notes — `a2_exponential_and_logarithmic_expressions_continuous_exponential_growth_and_decay_word_problems`

> **UNCLEAR / LOW_VARIETY**

- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Exponential and Logarithmic Expressions
- **Generator:** `exponential_growth_decay`
- **Suggested family:** `wp`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Continuous $A=Pe^{rt}$ or $A=A_0 e^{kt}$ story.
- **D=0:** Continuous $A=Pe^{rt}$ or $A=A_0 e^{kt}$ story.
- **High D (≈16–22):** Find $k$ or doubling time.
- **Must not:** Identical discrete prompts on continuous leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (same generator as discrete — no split)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{An account with \$50 changes by 10\% growth each year. Find the amount after 3 years.}$ | $66.55$ |  |
| 0 | 207 | $\text{A bacterial culture of 800 changes by 5\% growth each hour. Find the amount after 2 hours.}$ | $882$ |  |
| 8 | 101 | $\text{A sample of 800 grams becomes 491.30 grams after 3 years of discrete decay. Find the percent decay rate per year.}$ | $15$ |  |
| 8 | 207 | $\text{An account with \$200 becomes 295.49 dollars after 8 years of discrete growth. Find the percent growth rate per year.}$ | $5$ |  |
| 16 | 101 | $\text{A sample of 512 grams decays by half every 2 years (discrete half-life). How much remains after 8 years?}$ | $32$ |  |
| 16 | 207 | $\text{A population of 100 grows by 5\% each year. After how many years does it first exceed 149.86 people?}$ | $9$ |  |
| 22 | 101 | $\text{A sample of 512 grams decays by half every 2 years (discrete half-life). How much remains after 8 years?}$ | $32$ |  |
| 22 | 207 | $\text{A bacterial culture of 50 grows by 5\% each hour. After how many hours does it first exceed 64.73 cells?}$ | $6$ |  |

Opt-out flag used: `none (same generator as discrete — no split)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax College Algebra 2e §6.7 | https://openstax.org/books/college-algebra-2e/pages/6-7-exponential-and-logarithmic-models | Continuous growth/decay models |
| OpenStax Intermediate Algebra 2e §10.3 | https://openstax.org/books/intermediate-algebra-2e/pages/10-3-evaluate-and-graph-logarithmic-functions | Continuous vs discrete contrast |

## Variety notes / UNCLEAR flag

**UNCLEAR** / **LOW_VARIETY** — Old path is identical to discrete leaf at all D (no $e^{rt}$ / continuous wording).

## Limitations

Flags for gallery red header: `UNCLEAR`, `LOW_VARIETY`.

- **Variety:** one template / Mad-Lib across seeds at easy D — rotate OpenStax-derived frames or algebraic shapes before claiming shipped variety.
- **UNCLEAR gold:** old path and OpenStax skill intent diverge, or dump/wrong-skill shapes — do not wire a new core until notes lock.
- **Difficulty scaling:** Variety thin at fixed D; D may still bump coeffs — check live ladder.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Split continuous vs discrete generator params; new frame set ($A=Pe^{rt}$).
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
