# Notes — `g6_comparing_rates` (`g6_comparing_rates`)

- **Display name:** Comparing rates
- **Catalog chapter:** Grade 6 — Rates
- **Generator key:** `g6_comparing_rates`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `LOW_VARIETY`, `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Comparing rates
- **D=0:** Same unit already (\$4/1 lb vs \$2/1 lb) — who paid more.
- **High D (≈16–22):** Both rates need dividing; larger totals; grapes vs cars still the only stories.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Solve each problem. Two double number lines representing the two rates are provided.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{Sofia paid \$3 for 1 pound of rice. Liam paid \$8 for 6 pounds of rice. Who paid the higher unit price?}` | `\text{Sofia}` | D=0 easy |
| 8 | 41 | `\text{Sofia paid \$20 for 16 pounds of rice. Liam paid \$18 for 12 pounds of rice. Who paid the higher unit price?}` | `\text{Liam}` | mid |
| 16 | 41 | `\text{Sofia paid \$72 for 60 pounds of grapes. Liam paid \$16 for 40 pounds of grapes. Who paid the higher unit price?}` | `\text{Sofia}` | high D |
| 22 | 41 | `\text{Sofia paid \$208 for 64 pounds of almonds. Liam paid \$224 for 80 pounds of almonds. Who paid the higher unit price?}` | `\text{Sofia}` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_comparing_rates/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§5.6 Ratios and Rate** (compare two rates / unit prices). | | |
| Catalog instruction mentions double number lines; OpenStax 5.6 is fraction-of-rate, not double-number-line. | | |

## Variety notes / UNCLEAR flag

**LOW_VARIETY:** instruction-level two stories (unit price vs whose car is faster); this seed's D=0/8/16/22 were **all unit-price** (rice/grapes/almonds, Sofia vs Liam). **UNCLEAR:** instruction promises double number lines; live prompts are text-only.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** instruction-level two stories (unit price vs whose car is faster); this seed's D=0/8/16/22 were **all unit-price** (rice/grapes/almonds, Sofia vs Liam). **UNCLEAR:** instruction promises double number lines; live prompts are text-only.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `ComparingRatesFramework`. Diagram/double-number-line is UI, not a new algebra engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
