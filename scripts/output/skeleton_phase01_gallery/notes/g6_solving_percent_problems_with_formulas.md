# Notes — `g6_solving_percent_problems_with_formulas` (`g6_solving_percent_problems_with_formulas`)

- **Display name:** Solving percent problems with formulas
- **Catalog chapter:** Grade 6 — Percents
- **Generator key:** `percents`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solving percent problems with formulas
- **D=0:** Part = percent × whole with friendly 50%/20%.
- **High D (≈16–22):** Solve for whole or percent; non-integer percents ($36.7\%$ of what number).
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

topic_fit: `scripts/output/topic_fit/by_topic/g6_solving_percent_problems_with_formulas/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§6.2 Solve General Applications of Percent** | | |
| Ex 6.15 $125\%$ of $28$; Ex 6.16 $36$ is $75\%$ of what number; Try It 6.28: What number is $55\%$ of $60$? | | |

## Variety notes / UNCLEAR flag

Three unknown slots (part / percent / whole) appear. OpenStax 6.2 also has story apps (tax is §6.3, G6-out-of-scope). Numeric 'is/of' matches.

## Limitations

- Flags: **UNCLEAR**.
- Three unknown slots (part / percent / whole) appear. OpenStax 6.2 also has story apps (tax is §6.3, G6-out-of-scope). Numeric 'is/of' matches.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `PercentFramework`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
