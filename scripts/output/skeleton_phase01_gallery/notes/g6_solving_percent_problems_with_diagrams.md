# Notes — `g6_solving_percent_problems_with_diagrams` (`g6_solving_percent_problems_with_diagrams`)

- **Display name:** Solving percent problems with diagrams
- **Catalog chapter:** Grade 6 — Percents
- **Generator key:** `percents`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solving percent problems with diagrams
- **D=0:** Find a benchmark percent of a whole (What is $50\%$ of $70$?) — same family as formulas.
- **High D (≈16–22):** Find the whole or the percent; messier percents. Still no tape/percent-bar in the prompt.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Solve the problem.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{What is 10\% of 80?}` | `8` | D=0 easy |
| 8 | 41 | `\text{7 is what percent of 70?}` | `10\%` | mid |
| 16 | 41 | `\text{60 is 17.3\% of what number?}` | `346.8` | high D |
| 22 | 41 | `\text{60 is 17.3\% of what number?}` | `346.8` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_solving_percent_problems_with_diagrams/` **not present** (live table is the record).

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§6.2 Solve General Applications of Percent** — https://openstax.org/books/prealgebra-2e/pages/6-2-solve-general-applications-of-percent | | |
| Ex 6.15: $125\%$ of $28$ is what number? | | |
| Ex 6.16: $36$ is $75\%$ of what number? | | |
| OpenStax 6.2 is formula/translate, not diagram. G6 'diagrams' is IM percent-bar / double number line. | | |

## Variety notes / UNCLEAR flag

**UNCLEAR:** catalog/generator is shared `percents` with the formulas leaf; live stem is 'What is p% of n?' with no diagram. OpenStax 6.2 does not supply percent-bar examples either.

## Limitations

- Flags: **UNCLEAR**.
- **UNCLEAR:** catalog/generator is shared `percents` with the formulas leaf; live stem is 'What is p% of n?' with no diagram. OpenStax 6.2 does not supply percent-bar examples either.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse existing **number** `PercentFramework`. Diagram is UI. Do not invent a new engine to fake bars.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
