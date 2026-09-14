# Notes — `a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems`

> **UNCLEAR**

- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Exponential and Logarithmic Expressions
- **Generator:** `exponential_growth_decay`
- **Suggested family:** `wp`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Account / bacteria discrete percent growth.
- **D=0:** Account / bacteria discrete percent growth.
- **High D (≈16–22):** Find rate; half-life; first-exceed.
- **Must not:** Continuous $A=Pe^{rt}$ on discrete leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (hand generator)`.

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

Opt-out flag used: `none (hand generator)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Intermediate Algebra 2e §10.2 | https://openstax.org/books/intermediate-algebra-2e/pages/10-2-evaluate-and-graph-exponential-functions | Evaluate $A=A_0 b^t$ in context |
| OpenStax College Algebra 2e §6.1 | https://openstax.org/books/college-algebra-2e/pages/6-1-exponential-functions | Growth/decay applications |

## Variety notes / UNCLEAR flag

**UNCLEAR** — Not in EA TOC; old path rotates account/bacteria/half-life/find-rate — keep frames; IA/CA apps are gold for wording.

## Limitations

Flags for gallery red header: `UNCLEAR`.

- **UNCLEAR gold:** old path and OpenStax skill intent diverge, or dump/wrong-skill shapes — do not wire a new core until notes lock.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** ExponentialGrowthDecay WP core — rotate OpenStax contexts.
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
