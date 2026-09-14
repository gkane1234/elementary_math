# Notes — `g6_dividing_fractions` (`g6_dividing_fractions`)

- **Display name:** Dividing fractions
- **Catalog chapter:** Grade 6 — Dividing Fractions
- **Generator key:** `g6_fraction_divide`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Dividing fractions
- **D=0:** Unit-fraction ÷ same-denominator unit fraction ($\frac{3}{4}\div\frac{1}{4}=3$).
- **High D (≈16–22):** Unreduced fractions or a nested complex-fraction display; cancel both parts.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Divide.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\frac{3}{5} \div \frac{1}{5}` | `3` | D=0 easy |
| 8 | 41 | `\left(\frac{5}{18}\right) / \left(\frac{5}{6}\right)` | `\frac{1}{3}` | mid |
| 16 | 41 | `\frac{\frac{22}{45}}{\frac{55}{63}}` | `\frac{14}{25}` | high D |
| 22 | 41 | `\frac{154}{64} \div \frac{22}{64}` | `7` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_dividing_fractions/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§4.2 Multiply and Divide Fractions** | | |
| Ex 4.31–4.32 model then algorithm; later examples: multiply by the reciprocal (find reciprocal Ex 4.29-style chart). | | |

## Variety notes / UNCLEAR flag

Bare $a\div b$ (or stacked complex fraction). OpenStax 4.2 also models with bars; we skip models on this Ready leaf (interpretations are the disabled siblings).

## Limitations

- Flags: **UNCLEAR**.
- Bare $a\div b$ (or stacked complex fraction). OpenStax 4.2 also models with bars; we skip models on this Ready leaf (interpretations are the disabled siblings).

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `g6_fraction_divide` / RationalFramework divide. No new skeleton.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
