# Notes — `g6_how_many_groups_times` (`g6_how_many_groups_times`)

- **Display name:** How many groups/times?
- **Catalog chapter:** Grade 6 — Dividing Fractions
- **Generator key:** `g6_fraction_divide_groups`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_

---

## What the question should look like (D=0 vs high D)

- **Skill:** How many groups/times?
- **D=0:** How-many-groups divide: how many $1/4$s in a small whole or unit fraction (IM interpretation).
- **High D (≈16–22):** Messier fractions; still the groups interpretation, not bare $a\div b$.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Solve the problem.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{How many groups of } 5 \text{ are in } 20\text{?}` | `4` | D=0 easy |
| 8 | 41 | `\text{How many groups of } 8\frac{1}{3} \text{ are in } 50\text{?}` | `6` | mid |
| 16 | 41 | `\text{How many groups of } 7\frac{5}{6} \text{ are in } 15\frac{2}{3}\text{?}` | `2` | high D |
| 22 | 41 | `\text{How many groups of } 7\frac{5}{6} \text{ are in } 15\frac{2}{3}\text{?}` | `2` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_how_many_groups_times/` **not present** (live table is the record).

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§4.2 Multiply and Divide Fractions** — https://openstax.org/books/prealgebra-2e/pages/4-2-multiply-and-divide-fractions | | |
| Ex 4.31: Model $\frac{1}{4}\div\frac{1}{8}$ (how many eighths in a fourth). | | |
| Ex 4.32: Model $2\div\frac{1}{4}$. | | |

## Variety notes / UNCLEAR flag

Live stems are the groups interpretation ('How many groups of A are in B?'), not a dump of $a\div b$. D=0 is whole-number groups; high D uses mixed numbers. Disabled in the picker but on-topic. D=16 and D=22 can repeat the same item.

## Limitations

- Flags: **UNCLEAR**.
- Live stems are the groups interpretation ('How many groups of A are in B?'), not a dump of $a\div b$. D=0 is whole-number groups; high D uses mixed numbers. Disabled in the picker but on-topic. D=16 and D=22 can repeat the same item.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse existing G6 fraction-divide-groups generator (**number**). No new engine. Do not merge into algebraic `RationalFramework`.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
