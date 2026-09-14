# Notes — `g6_relating_percents_fractions_and_decimals` (`g6_relating_percents_fractions_and_decimals`)

- **Display name:** Relating percents, fractions, and decimals
- **Catalog chapter:** Grade 6 — Percents
- **Generator key:** `g6_relating_percents_fractions_and_decimals`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Relating percents, fractions, and decimals
- **D=0:** One-step convert: $0.4$ → fraction, or $75\%$ → decimal.
- **High D (≈16–22):** Awkward percents ($18.75\%$), three-place decimals, or fraction→percent with cancel.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Write the equivalent value.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{Write } 80\% \text{ as a fraction in simplest form.}` | `\frac{4}{5}` | D=0 easy |
| 8 | 41 | `\text{Write } 0.375 \text{ as a percent.}` | `37.5\%` | mid |
| 16 | 41 | `\text{Write } 10\% \text{ as a fraction in simplest form.}` | `\frac{1}{10}` | high D |
| 22 | 41 | `\text{Write } 87.5\% \text{ as a fraction in simplest form.}` | `\frac{7}{8}` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_relating_percents_fractions_and_decimals/` present.

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§6.1 Understand Percent** (convert triad) and **§5.3 Decimals and Fractions**. | | |
| Ex 6.3: $36\%$ and $125\%$ to fractions. | | |
| §5.3 Ex 5.28-style: write $\frac{3}{8}$ as a decimal. | | |

## Variety notes / UNCLEAR flag

Direction of conversion rotates. Matches OpenStax 6.1/5.3 well. High D stays on-topic.

## Limitations

- Flags: **UNCLEAR**.
- Direction of conversion rotates. Matches OpenStax 6.1/5.3 well. High D stays on-topic.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse **number** `FractionDecimalConvertFramework(include_percent=True)`. No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
