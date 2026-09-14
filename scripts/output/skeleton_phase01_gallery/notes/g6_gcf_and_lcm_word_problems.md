# Notes — `g6_gcf_and_lcm_word_problems` (`g6_gcf_and_lcm_word_problems`)

- **Display name:** GCF and LCM word problems
- **Catalog chapter:** Grade 6 — Common Factors and Common Multiples
- **Generator key:** `g6_gcf_and_lcm_word_problems`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `LOW_VARIETY`

---

## What the question should look like (D=0 vs high D)

- **Skill:** GCF and LCM word problems
- **D=0:** GCF 'identical bags' with tiny counts (6 grapes and 9 kites).
- **High D (≈16–22):** Same two stories with bigger numbers; LCM pack leftovers.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Solve the problem.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{You have 22 magnets and 11 highlighters. What is the greatest number of identical bags you can make?}` | `11` | D=0 easy |
| 8 | 41 | `\text{You have 44 magnets and 22 highlighters. What is the greatest number of identical bags you can make?}` | `22` | mid |
| 16 | 41 | `\text{You have 56 magnets and 8 highlighters. What is the greatest number of identical bags you can make?}` | `8` | high D |
| 22 | 41 | `\text{You have 144 magnets and 72 markers. What is the greatest number of identical bags you can make?}` | `72` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_gcf_and_lcm_word_problems/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§2.4 / §2.5** applications (grouping / repeating events). Prealgebra does not have a large GCF/LCM story bank; Elementary Algebra GCF is polynomials. | | |
| Typical OS-style: split items into identical gift bags (GCF); events coinciding (LCM). | | |

## Variety notes / UNCLEAR flag

**LOW_VARIETY:** two Mad-Libs (identical bags / GCF; packs with no leftovers / LCM). This seed's D=0/8/16/22 were **all GCF bags** (magnets/highlighters). OpenStax-style would add schedules, tiling, teams.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** two Mad-Libs (identical bags / GCF; packs with no leftovers / LCM). This seed's D=0/8/16/22 were **all GCF bags** (magnets/highlighters). OpenStax-style would add schedules, tiling, teams.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse existing WP generator. If upgraded, **wp packaging / OpenStax-style frames** on the same GCF/LCM number core — do not invent a new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
