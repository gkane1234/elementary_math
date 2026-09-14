# Notes — `pc_sum_and_difference_identities` (`Sum and Difference Identities`)

- **Course:** Precalculus
- **Category:** Precalculus — Trigonometry
- **Generator:** `trig_sum_difference`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student simplify for sum and difference identities.
- **D=0:** sin(α±β), cos(α±β) exact eval; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Expand }\sin(\alpha-\beta).$` | `$\sin\alpha\cos\beta-\cos\alpha\sin\beta$` | evaluate/rewrite |
| 8 | 101 | `$\text{Expand }\tan(\alpha+\beta).$` | `$\frac{\tan\alpha+\tan\beta}{1-\tan\alpha\tan\beta}$` | evaluate/rewrite |
| 16 | 101 | `$\text{Expand }\tan(\alpha+\beta).$` | `$\frac{\tan\alpha+\tan\beta}{1-\tan\alpha\tan\beta}$` | evaluate/rewrite |
| 22 | 101 | `$\text{Expand }\tan(\alpha+\beta).$` | `$\frac{\tan\alpha+\tan\beta}{1-\tan\alpha\tan\beta}$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §7.2 | https://openstax.org/books/precalculus-2e/pages/7-2-sum-and-difference-identities | sin(α±β), cos(α±β) exact eval |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/7-2-sum-and-difference-identities.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Sum/difference identity rewrite skeleton.
- **Wired:** `trig_skeleton.TrigSumDiff` is live default for this leaf; opt-out `use_sample_trig_identities=True`.
- D=0 expands sin/cos(α±β); tan + OpenStax exact-eval unlock at higher D.



## Limitations

> **LIMITATIONS**

- **Variety:** Only 2 distinct prompts across D=0/8/16/22 in notes table — limited stem rotation at fixed seed.
- **D-scaling:** D=0 expands sin(α−β); D≥8 collapses to the same tan(α+β) expand for seed=101 — plateau, not honest ladder.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Live skeleton/reuse default — limitations are variety/D/OpenStax coverage, not a missing engine.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
