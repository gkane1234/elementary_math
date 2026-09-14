# Notes — `g6_what_fraction_of_a_whole` (`g6_what_fraction_of_a_whole`)

- **Display name:** What fraction of a whole?
- **Catalog chapter:** Grade 6 — Dividing Fractions
- **Generator key:** `g6_fraction_of_whole`
- **Already on skeleton:** no (old path is the live default)
- **Flags:** _none_ (stem is now “what fraction of B is A”, not multiply-by-½)

---

## What the question should look like (D=0 vs high D)

- **Skill:** What fraction of a whole?
- **D=0:** What fraction of a whole: $a$ is what fraction of $b$ with small wholes.
- **High D (≈16–22):** Larger or mixed numbers; still 'what fraction of'.
- **Must not:** dump an equation; change topic at high D (e.g. addition emitting subtraction); skip the named method (diagram / equivalent-fraction rewrite) while keeping the sibling's bare arithmetic.

Live instruction latex: `\text{Solve the problem.}`

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`. These leaves are **not** on equation/poly skeletons.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 41 | `\text{What fraction of a whole is } \frac{1}{2} \text{ of } \frac{3}{2}\text{?}` | `\frac{3}{4}` | D=0 easy |
| 8 | 41 | `\text{What fraction of a whole is } \frac{1}{2} \text{ of } \frac{22}{5}\text{?}` | `\frac{11}{5}` | mid |
| 16 | 41 | `\text{What fraction of a whole is } \frac{1}{2} \text{ of } \frac{43}{8}\text{?}` | `\frac{43}{16}` | high D |
| 22 | 41 | `\text{What fraction of a whole is } \frac{1}{2} \text{ of } \frac{43}{4}\text{?}` | `\frac{43}{8}` | high D |

Opt-out flag used: _none (not on skeleton; live default is the old number framework)._

topic_fit: `scripts/output/topic_fit/by_topic/g6_what_fraction_of_a_whole/` **not present** (live table is the record).

## OpenStax examples + chapter/section cites

G6 is a curriculum unit (IM-style), not an OpenStax book. Equivalent: **OpenStax Prealgebra 2e** (local `textbooks/openstax/html/prealgebra-2e/`).

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§4.2** divide-as-fraction-of and **§4.1 Visualize Fractions**. | | |
| OpenStax 4.2 also: divide by writing a complex fraction. G6 wants the 'what fraction of a whole' language. | | |

## Variety notes / UNCLEAR flag

**Stem:** live prompt is now “What fraction of $B$ is $A$?” (part of a whole). D=0 uses small wholes.

## Limitations

- Flags: **UNCLEAR**.
- **Stem:** live prompt is now “What fraction of $B$ is $A$?” (part of a whole). D=0 uses small wholes.

## Proposed engine (reuse vs new) — proposal only

- **Reuse / family:** Reuse `g6_fraction_of_whole` (**number**). No new engine.
- **New:** do not invent a number skeleton this pass.
- **Not this pass:** no generator implementation.

Suggested family: **number** (WP leaves: **wp** frames on the same number core; plot leaf: **other** / graphing).
