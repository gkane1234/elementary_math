# Notes — `g6_least_common_multiple` (`g6_least_common_multiple`)

- **Display name:** Least common multiple
- **Catalog chapter:** Grade 6 — Common Factors and Common Multiples
- **Generator key:** `g6_least_common_multiple`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Least common multiple
- **D=0:** LCM of two small numbers (listing multiples is enough).
- **High D (≈16–22):** Larger pair / triple; prime-factor LCM is the intended work.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Find the LCM.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{Find the LCM of } 3, 6` | `6` | D=0 easy |
| 8 | 41 | `\text{Find the LCM of } 20, 30` | `60` | mid |
| 16 | 41 | `\text{Find the LCM of } 12, 18, 30` | `180` | high D |
| 22 | 41 | `\text{Find the LCM of } 154, 231, 385` | `2310` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_least_common_multiple/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§2.5 Prime Factorization and the LCM** | | |
| Ex 2.52: LCM of $15$ and $20$ by listing multiples. | | |
| Ex 2.53: LCM of $15$ and $18$ using prime factors. | | |

## Variety notes / UNCLEAR flag

Always 'Find the LCM'. Matches 2.5. We do not force tree vs ladder method in the prompt.

## Limitations

- Flags: **UNCLEAR**.
- Always 'Find the LCM'. Matches 2.5. We do not force tree vs ladder method in the prompt.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `g6_least_common_multiple`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
