# Notes — `pc_vectors_diagrams` (`Diagrams`)

- **Course:** Precalculus
- **Category:** Precalculus — Vectors
- **Generator:** `vector_diagrams`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student interpret the tip-to-tail diagram for diagrams.
- **D=0:** tip-to-tail diagram interpretation; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{On the tip-to-tail diagram, } \langle 6, 2 \rangle \text{ is followed by } \langle -1, -3 \rangle. \text{Find the magnitude of the resultant.}$` | `$5.1$` | evaluate/rewrite |
| 8 | 101 | `$\text{On the tip-to-tail diagram, } \langle 6, -1 \rangle \text{ is followed by } \langle -3, 4 \rangle. \text{Find the magnitude of the resultant.}$` | `$4.24$` | evaluate/rewrite |
| 16 | 101 | `$\text{On the tip-to-tail diagram, } \langle 0, -3 \rangle \text{ is followed by } \langle -5, 0 \rangle. \text{Find the magnitude of the resultant.}$` | `$5.83$` | evaluate/rewrite |
| 22 | 101 | `$\text{The diagram shows vector } \mathbf{u} = \langle -2, -3 \rangle.\ \text{Find the opposite vector } -\mathbf{u}.$` | `$\langle 2, 3 \rangle$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §9.8 | https://openstax.org/books/precalculus-2e/pages/9-8-vectors | tip-to-tail diagram interpretation |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/9-8-vectors.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Vector diagram framework.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

> **LIMITATIONS**

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Diagram:** Leaf is diagram-named but live stem is textual tip-to-tail / component wording — no SVG diagram in gallery samples; OpenStax §9.8 expects figure reading.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
