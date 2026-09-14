# Notes — `pc_fundamental_identities` (`Fundamental identities`)

> **LOW_VARIETY**

- **Course:** Precalculus
- **Category:** Precalculus — Trigonometry
- **Generator:** `trig_basic_identities`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student simplify for fundamental identities.
- **D=0:** Pythagorean/reciprocal/quotient simplify; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Simplify: } 1 + \cot^2 \theta$` | `$\csc^2 \theta$` | simplify |
| 8 | 101 | `$\text{Simplify: } 1 + \cot^2 \theta$` | `$\csc^2 \theta$` | simplify |
| 16 | 101 | `$\text{Simplify: } 1 + \cot^2 \theta$` | `$\csc^2 \theta$` | simplify |
| 22 | 101 | `$\text{Simplify: } 1 + \cot^2 \theta$` | `$\csc^2 \theta$` | simplify |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §7.1 | https://openstax.org/books/precalculus-2e/pages/7-1-simplifying-and-verifying-trigonometric-identities | Pythagorean/reciprocal/quotient simplify |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/7-1-simplifying-and-verifying-trigonometric-identities.md`

## Variety notes / flags

- Simplify only — OpenStax 7.1 also has verify LHS=RHS (partial).
- Identical prompt across all D bands sampled.
- Answer shape flat across D — difficulty may be cosmetic.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Trig identity rewrite skeleton + `precalculus_trig_identities.json`.
- **Pilot wired:** `trig_skeleton.TrigRewrite` is live default; opt-out `use_sample_trig_identities=True`.
- **Not this pass:** sum/difference leaves; full verify catalog (partial at D≥8).



## Limitations

> **LIMITATIONS**

- **Variety:** Old-path table shows one prompt shape across D bands sampled (seed=101) — `$\text{Simplify: } 1 + \cot^2 \theta$`.
- **Trig identities:** Simplify-only catalog; OpenStax §7.1 also verify LHS=RHS. Same Pythagorean stem across D → red-header.
- **Difficulty scaling:** Answer latex flat across D in notes table — D may be cosmetic until form unlocks change the student-visible stem.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Live skeleton/reuse default — limitations are variety/D/OpenStax coverage, not a missing engine.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
