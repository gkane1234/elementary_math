# `percents` — Percents

> **NOT_IMPLEMENTED / LIMITATIONS** — Notes backfill stub; leaf not on a phase-01 skeleton this wave.

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Percents
- **Generator:** `percents`
- **Already on skeleton?** no

## What the question should look like (D=0 vs high D)

- **Skill:** Find part/whole/percent. Distinct from percent_word_problems.
- **D=0:** small whole-number percents / simple change.
- **High D:** decimals, multi-step find-whole, or compound change only if old path did.
- **Must not:** dump retail markup WP onto this leaf (`pa_markup_discount_and_tax` / `percent_word_problems`).

## What old path actually produced (real latex, D=0/8/16/22)

_Not sampled in this stub pass — fill before implementing._

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 |  |  |  |  |
| 8 |  |  |  |  |
| 16 |  |  |  |  |
| 22 |  |  |  |  |

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy |
|------|-----|--------------|
| OpenStax Prealgebra 2e §6.1–6.2 | https://openstax.org/books/prealgebra-2e/pages/6-1-understanding-percent | percent-of / find whole |
| OpenStax Prealgebra 2e §6.2 (change) | https://openstax.org/books/prealgebra-2e/pages/6-2-solve-general-applications-of-percent | percent increase/decrease shapes |

## Variety notes / UNCLEAR flag

`NOT_IMPLEMENTED` until old-path table is filled and an existing number core can match honestly.

## Limitations

- NOT_IMPLEMENTED / LIMITATIONS: gallery stub only; no skeleton wiring this pass.
- Fill live old-path D=0/8/16/22 before implementing.
- Keep distinct from `percent_word_problems` and G6 percent diagram leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** number / PercentWP family if shapes match.
- **New:** leave leaf until notes lock gold.
- Suggested family: `number`
