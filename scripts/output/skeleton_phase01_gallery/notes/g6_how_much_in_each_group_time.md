# Notes — `g6_how_much_in_each_group_time` (`g6_how_much_in_each_group_time`)

- **Display name:** How much in each group/time?
- **Catalog chapter:** Grade 6 — Dividing Fractions
- **Generator key:** `g6_fraction_divide_each`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** How much in each group/time?
- **D=0:** How-much-in-each-group: share a small amount into a unit-fraction number of groups.
- **High D (≈16–22):** Non-unit fractions; still sharing interpretation.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Solve the problem.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{If } 20 \text{ is shared equally into } 5 \text{ groups, how much is in each group?}` | `4` | D=0 easy |
| 8 | 41 | `\text{If } 50 \text{ is used in } 8\frac{1}{3} \text{ of a period, how much is used in one full period?}` | `6` | mid |
| 16 | 41 | `\text{If } 2\frac{5}{8} \text{ is used in } 3\frac{1}{2} \text{ of a period, how much is used in one full period?}` | `\frac{3}{4}` | high D |
| 22 | 41 | `\text{If } 2\frac{5}{8} \text{ is used in } 3\frac{1}{2} \text{ of a period, how much is used in one full period?}` | `\frac{3}{4}` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_how_much_in_each_group_time/` **not present** (live table is the record).

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§4.2 Multiply and Divide Fractions** (sharing / 'how much in each group'). | | |
| Ex 4.32-style $2\div\frac{1}{4}$ can be read either as groups or as each-group depending on story. | | |

## Variety notes / UNCLEAR flag

Live stems stay the sharing / 'how much in each period' interpretation and do not collapse into the groups sibling. D=0 is whole÷whole share; high D uses mixed numbers. Disabled in the picker. D=16/22 can duplicate.

## Limitations

- Flags: **UNCLEAR**.
- Live stems stay the sharing / 'how much in each period' interpretation and do not collapse into the groups sibling. D=0 is whole÷whole share; high D uses mixed numbers. Disabled in the picker. D=16/22 can duplicate.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse `g6_fraction_divide_each` (**number**). No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
