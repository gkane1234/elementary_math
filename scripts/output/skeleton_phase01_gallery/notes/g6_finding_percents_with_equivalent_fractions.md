# Notes — `g6_finding_percents_with_equivalent_fractions` (`g6_finding_percents_with_equivalent_fractions`)

- **Display name:** Finding percents with equivalent fractions
- **Catalog chapter:** Grade 6 — Percents
- **Generator key:** `g6_finding_percents_with_equivalent_fractions`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** `LOW_VARIETY`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Finding percents with equivalent fractions
- **D=0:** Unit fraction with denom dividing 100: $\frac{1}{4}\to 25\%$ via denom 100.
- **High D (≈16–22):** Reduce a bulky fraction first, then scale to 100 (e.g. $\frac{352}{512}$).
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Write as a percent using equivalent fractions.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{Write } \frac{3}{5} \text{ as a percent by finding an equivalent fraction with denominator 100.}` | `60\%` | D=0 easy |
| 8 | 41 | `\text{Write } \frac{6}{25} \text{ as a percent by finding an equivalent fraction with denominator 100.}` | `24\%` | mid |
| 16 | 41 | `\text{Write } 37.5\% \text{ as a fraction in simplest form (use an equivalent fraction with denominator 100).}` | `\frac{3}{8}` | high D |
| 22 | 41 | `\text{Write } 25\% \text{ as a fraction in simplest form (use an equivalent fraction with denominator 100).}` | `\frac{1}{4}` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_finding_percents_with_equivalent_fractions/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§6.1 Understand Percent** — convert fraction to percent via $/100$. | | |
| OpenStax often uses $\times 100\%$ rather than forcing denominator 100; equivalent-fraction-to-100 is the G6 IM method. | | |

## Variety notes / UNCLEAR flag

**LOW_VARIETY:** single stem ('write as a percent by finding an equivalent fraction with denominator 100'). Skill is real; only the wrapper is one template.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** single stem ('write as a percent by finding an equivalent fraction with denominator 100'). Skill is real; only the wrapper is one template.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `FindingPercentsEquivalentFractionsFramework`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
