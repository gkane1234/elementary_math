# Notes — `a2_radical_functions_and_rational_exponents_simplifying_radicals`

> **LOW_VARIETY / UNCLEAR** — One template across seeds at D=0.

- **Display name:** Simplifying radicals
- **Category:** Algebra 2 — Radical Functions and Rational Exponents
- **Generator:** `radical_simplification`
- **Already on skeleton?** yes (`radical_simplification`)
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice simplifying radicals (catalog: radical_simplification).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\sqrt{120}$ | $2\sqrt{30}$ | pattern=RadicalSimplify |
| 0 | 207 | $\sqrt{96}$ | $4\sqrt{6}$ | pattern=RadicalSimplify |
| 8 | 101 | $\sqrt{80}$ | $4\sqrt{5}$ | pattern=RadicalSimplify |
| 8 | 207 | $\sqrt{72}$ | $6\sqrt{2}$ | pattern=RadicalSimplify |
| 16 | 101 | $\sqrt{368}$ | $4\sqrt{23}$ | pattern=RadicalSimplify |
| 16 | 207 | $\sqrt{160}$ | $4\sqrt{10}$ | pattern=RadicalSimplify |
| 22 | 101 | $\sqrt{288}$ | $12\sqrt{2}$ | pattern=RadicalSimplify |
| 22 | 207 | $\sqrt{432}$ | $12\sqrt{3}$ | pattern=RadicalSimplify |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `radical_simplification` (same generator `radical_simplification` unless noted).
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.
  - D=0.0 seed=101: A2 `\sqrt{120}` ≠ A1 `\sqrt{72}`
  - D=0.0 seed=207: A2 `\sqrt{96}` ≠ A1 `\sqrt{72}`
  - D=8.0 seed=101: A2 `\sqrt{80}` ≠ A1 `\sqrt{180}`
  - D=8.0 seed=207: A2 `\sqrt{72}` ≠ A1 `\sqrt{180}`
  - D=16.0 seed=101: A2 `\sqrt{368}` ≠ A1 `\sqrt{208}`
  - D=16.0 seed=207: A2 `\sqrt{160}` ≠ A1 `\sqrt{216}`
  - D=22.0 seed=101: A2 `\sqrt{288}` ≠ A1 `\sqrt{384}`
  - D=22.0 seed=207: A2 `\sqrt{432}` ≠ A1 `\sqrt{216}`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §8.1 | https://openstax.org/books/intermediate-algebra-2e/pages/8-1-simplify-expressions-with-roots | 8.1 Simplify Expressions with Roots — e.g. Example 8.1: Simplify: ⓐ $\sqrt{144}$ ⓑ $− \sqrt{289} .$; Example 8.2: Simplify: ⓐ $\sqrt{−196}$ ⓑ $− \sqrt{64} .$ |
| Intermediate Algebra 2e §8.2 | https://openstax.org/books/intermediate-algebra-2e/pages/8-2-simplify-radical-expressions | 8.2 Simplify Radical Expressions — e.g. Example 8.13: Simplify Square Roots Using the Product Property of Roots Simplify: $\sqrt{98} .$; Example 8.14: Simplify: ⓐ $\sqrt{500}$ ⓑ $\sqrt[3]{16}$ ⓒ $\sqrt[4]{243} .$ |
| Intermediate Algebra 2e §8.3 | https://openstax.org/books/intermediate-algebra-2e/pages/8-3-simplify-rational-exponents | 8.3 Simplify Rational Exponents — e.g. Example 8.26: Write as a radical expression: ⓐ $x^{\frac{1}{2}}$ ⓑ $y^{\frac{1}{3}}$ ⓒ $z^{\frac{1}{4}} .$; Example 8.27: Write with a rational exponent: ⓐ $\sqrt{5 y}$ ⓑ $\sqrt[3]{4 x}$ ⓒ $3 \sqrt[4]{5 z} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

One template across seeds at D=0.
Flags: `LOW_VARIETY`, `UNCLEAR`.

## Limitations

Flags for gallery red header: `UNCLEAR`, `LOW_VARIETY`.

- **Variety:** one template / Mad-Lib across seeds at easy D — rotate OpenStax-derived frames or algebraic shapes before claiming shipped variety.
- **UNCLEAR gold:** old path and OpenStax skill intent diverge, or dump/wrong-skill shapes — do not wire a new core until notes lock.
- **Difficulty scaling:** Variety thin at fixed D; D may still bump coeffs — check live ladder.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing skeleton slug `radical_simplification` / shared `radical_simplification` family.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `radical_simplification`; equations/WP agent owns solve/WP siblings._
