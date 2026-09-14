# Notes — `pc_logarithms_and_exponents_as_inverses` (`Logarithms and exponents as inverses`)

- **Course:** Precalculus
- **Category:** Precalculus — Exponential and Logarithmic Expressions
- **Generator:** `log_evaluate`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student rewrite using inverses for logarithms and exponents as inverses.
- **D=0:** inverse relationship exp/log; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\log_{3}\left(3\right)$` | `$1$` | evaluate/rewrite |
| 8 | 101 | `$\log_{9}\left(59049\right)$` | `$5$` | evaluate/rewrite |
| 16 | 101 | `$\log_{7}\left(49\right)$` | `$2$` | evaluate/rewrite |
| 22 | 101 | `$\log_{9}\left(2672\right)$` | `$3.59$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §4.3 | https://openstax.org/books/precalculus-2e/pages/4-3-logarithmic-functions | inverse relationship exp/log |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/4-3-logarithmic-functions.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Log evaluate constructive; inverse rewrite forms.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
