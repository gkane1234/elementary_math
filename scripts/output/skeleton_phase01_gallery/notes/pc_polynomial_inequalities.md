# Notes — `pc_polynomial_inequalities` (`Polynomial inequalities`)

- **Course:** Precalculus
- **Category:** Precalculus — Power, Polynomial, and Rational Functions
- **Generator:** `precalc_foundations`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student solve the inequality for polynomial inequalities.
- **D=0:** sign chart / interval solution; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$(x-6)(x+3)>0.$` | `$x<-3\text{ or }x>6$` | evaluate/rewrite |
| 8 | 101 | `$(x-6)(x+4)>0.$` | `$x<-4\text{ or }x>6$` | evaluate/rewrite |
| 16 | 101 | `$(x-5)(x+2)>0.$` | `$x<-2\text{ or }x>5$` | evaluate/rewrite |
| 22 | 101 | `$(x-6)(x+3)>0.$` | `$x<-3\text{ or }x>6$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §3.8 | https://openstax.org/books/precalculus-2e/pages/3-8-inverses-and-radical-functions | sign chart / interval solution |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/3-8-inverses-and-radical-functions.md`

## Variety notes / flags

- Uses `precalc_foundations` topic branch (thin but topic-shaped).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Keep live `precalc_foundations` until dedicated skeleton; split topic branches per OpenStax section. Topic key `pc_polynomial_inequalities`.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
