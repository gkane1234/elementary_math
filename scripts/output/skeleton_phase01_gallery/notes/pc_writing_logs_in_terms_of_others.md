# Notes — `pc_writing_logs_in_terms_of_others` (`Writing logs in terms of others`)

- **Course:** Precalculus
- **Category:** Precalculus — Exponential and Logarithmic Expressions
- **Generator:** `log_change_of_base`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student rewrite the logarithm for writing logs in terms of others.
- **D=0:** change-of-base / rewrite; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Expand: } \log_{3}\left(63\right)$` | `$\log_{3}(7)+\log_{3}(9)$` | evaluate/rewrite |
| 8 | 101 | `$\text{Rewrite using change of base: } \log_{5}(625)$` | `$\frac{\log_{9}(625)}{\log_{9}(5)}$` | evaluate/rewrite |
| 16 | 101 | `$\text{Expand: } \log_{11}\left(35\right)$` | `$\log_{11}(5)+\log_{11}(7)$` | evaluate/rewrite |
| 22 | 101 | `$\text{Rewrite using change of base: } \log_{11}(1331)$` | `$\frac{\log_{10}(1331)}{\log_{10}(11)}$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §4.5 | https://openstax.org/books/precalculus-2e/pages/4-5-logarithmic-properties | change-of-base / rewrite |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/4-5-logarithmic-properties.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Log properties skeleton / form catalog.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
