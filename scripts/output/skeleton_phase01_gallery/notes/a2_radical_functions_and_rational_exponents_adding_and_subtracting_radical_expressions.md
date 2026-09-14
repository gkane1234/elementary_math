# Notes — `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions`

> **UNCLEAR** — A2 type_id samples differ from A1 alias at same D/seeds — verify intended divergence.

- **Display name:** Adding and subtracting radical expressions
- **Category:** Algebra 2 — Radical Functions and Rational Exponents
- **Generator:** `radical_add_subtract`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice adding and subtracting radical expressions (catalog: radical_add_subtract).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $3\sqrt{15} + 4\sqrt{15}$ | $7\sqrt{15}$ | pattern=RadicalAddSub, form=add_like_radicals |
| 0 | 207 | $2\sqrt{14} - \sqrt{14}$ | $\sqrt{14}$ | pattern=RadicalAddSub, form=add_like_radicals |
| 8 | 101 | $\sqrt{135} + \sqrt{135}$ | $6\sqrt{15}$ | pattern=RadicalAddSub, form=add_unsimplified_radicals |
| 8 | 207 | $\sqrt{224} + \sqrt{14}$ | $5\sqrt{14}$ | pattern=RadicalAddSub, form=add_unsimplified_radicals |
| 16 | 101 | $\sqrt{240} + \sqrt{135} - \sqrt{60}$ | $5\sqrt{15}$ | pattern=RadicalAddSub, form=add_unsimplified_radicals |
| 16 | 207 | $\sqrt{224} + \sqrt{14} + \sqrt{56}$ | $7\sqrt{14}$ | pattern=RadicalAddSub, form=add_unsimplified_radicals |
| 22 | 101 | $\sqrt{240} + \sqrt{135} - \sqrt{60}$ | $5\sqrt{15}$ | pattern=RadicalAddSub, form=add_unsimplified_radicals |
| 22 | 207 | $\sqrt{224} + \sqrt{224} + \sqrt{56} - \sqrt{14} - \sqrt{56}$ | $7\sqrt{14}$ | pattern=RadicalAddSub, form=add_unsimplified_radicals |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `radical_add_subtract` (same generator `radical_add_subtract` unless noted).
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.
  - D=0.0 seed=101: A2 `3\sqrt{15} + 4\sqrt{15}` ≠ A1 `4\sqrt{14} + \sqrt{14}`
  - D=0.0 seed=207: A2 `2\sqrt{14} - \sqrt{14}` ≠ A1 `3\sqrt{5} - 2\sqrt{5}`
  - D=8.0 seed=101: A2 `\sqrt{135} + \sqrt{135}` ≠ A1 `\sqrt{224} - \sqrt{56} - \sqrt{224}`
  - D=8.0 seed=207: A2 `\sqrt{224} + \sqrt{14}` ≠ A1 `\sqrt{80} + \sqrt{20}`
  - D=16.0 seed=101: A2 `\sqrt{240} + \sqrt{135} - \sqrt{60}` ≠ A1 `5\sqrt{350} - 4\sqrt{126} - \sqrt{686} + \sqrt{504}`
  - D=16.0 seed=207: A2 `\sqrt{224} + \sqrt{14} + \sqrt{56}` ≠ A1 `\sqrt{245} - \sqrt{245} + 2\sqrt{45}`
  - D=22.0 seed=101: A2 `\sqrt{240} + \sqrt{135} - \sqrt{60}` ≠ A1 `5\sqrt{350} - 4\sqrt{126} - \sqrt{686} + \sqrt{504}`
  - D=22.0 seed=207: A2 `\sqrt{224} + \sqrt{224} + \sqrt{56} - \sqrt{14} - \sqrt{56}` ≠ A1 `\sqrt{245} - \sqrt{245} + 2\sqrt{45}`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §8.1 | https://openstax.org/books/intermediate-algebra-2e/pages/8-1-simplify-expressions-with-roots | 8.1 Simplify Expressions with Roots — e.g. Example 8.1: Simplify: ⓐ $\sqrt{144}$ ⓑ $− \sqrt{289} .$; Example 8.2: Simplify: ⓐ $\sqrt{−196}$ ⓑ $− \sqrt{64} .$ |
| Intermediate Algebra 2e §8.2 | https://openstax.org/books/intermediate-algebra-2e/pages/8-2-simplify-radical-expressions | 8.2 Simplify Radical Expressions — e.g. Example 8.13: Simplify Square Roots Using the Product Property of Roots Simplify: $\sqrt{98} .$; Example 8.14: Simplify: ⓐ $\sqrt{500}$ ⓑ $\sqrt[3]{16}$ ⓒ $\sqrt[4]{243} .$ |
| Intermediate Algebra 2e §8.3 | https://openstax.org/books/intermediate-algebra-2e/pages/8-3-simplify-rational-exponents | 8.3 Simplify Rational Exponents — e.g. Example 8.26: Write as a radical expression: ⓐ $x^{\frac{1}{2}}$ ⓑ $y^{\frac{1}{3}}$ ⓒ $z^{\frac{1}{4}} .$; Example 8.27: Write with a rational exponent: ⓐ $\sqrt{5 y}$ ⓑ $\sqrt[3]{4 x}$ ⓒ $3 \sqrt[4]{5 z} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

A2 type_id samples differ from A1 alias at same D/seeds — verify intended divergence.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `UNCLEAR`.

- **UNCLEAR gold:** old path and OpenStax skill intent diverge, or dump/wrong-skill shapes — do not wire a new core until notes lock.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Share A1 `radical_add_subtract` generator; wire A2 catalog id when skeleton lands.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `radical_add_subtract`; equations/WP agent owns solve/WP siblings._
