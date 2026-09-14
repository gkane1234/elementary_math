# Notes — `g6_greatest_common_factor` (`g6_greatest_common_factor`)

- **Display name:** Greatest common factor
- **Catalog chapter:** Grade 6 — Common Factors and Common Multiples
- **Generator key:** `g6_greatest_common_factor`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Greatest common factor
- **D=0:** GCF of two small numbers ($6,9\to 3$).
- **High D (≈16–22):** Three numbers, larger composites that share a big GCF ($72,144,216$).
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Find the GCF.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{Find the GCF of } 22, 11` | `11` | D=0 easy |
| 8 | 41 | `\text{Find the GCF of } 30, 18` | `6` | mid |
| 16 | 41 | `\text{Find the GCF of } 42, 84, 126` | `42` | high D |
| 22 | 41 | `\text{Find the GCF of } 72, 144, 216` | `72` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_greatest_common_factor/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§2.4 Find Multiples and Factors** (common factors) and **§2.5** (prime factors used for GCF/LCM). | | |
| OpenStax names GCF more heavily in Elementary Algebra 2e **§7.1** (polynomials) — numeric GCF for G6 is Prealgebra 2.4/2.5. | | |

## Variety notes / UNCLEAR flag

Always 'Find the GCF of …'. Numbers/count of arguments ramp. Fine for the skill; OpenStax 2.4 also asks factor lists first.

## Limitations

- Flags: **UNCLEAR**.
- Always 'Find the GCF of …'. Numbers/count of arguments ramp. Fine for the skill; OpenStax 2.4 also asks factor lists first.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `g6_greatest_common_factor`. Not the poly FactorGCF skeleton.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
