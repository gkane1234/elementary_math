# Notes — `a2_complex_numbers_rationalizing_denominators`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Complex Numbers
- **Generator:** `complex_rationalize_denominator`
- **Suggested family:** `number`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Real over $a+bi$ or pure imaginary denominator.
- **D=0:** Real over $a+bi$ or pure imaginary denominator.
- **High D (≈16–22):** Complex conjugate pairs; larger nums.
- **Must not:** Real radical rationalize (radical leaf).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (hand generator)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Rationalize } \dfrac{-2+2i}{0+1i}.$ | $2+2i$ |  |
| 0 | 207 | $\text{Rationalize } \dfrac{2}{3-2i}.$ | $\frac{6}{13}+\frac{4}{13}i$ |  |
| 8 | 101 | $\text{Rationalize } \dfrac{1-1i}{-4-2i}.$ | $-\frac{1}{10}+\frac{3}{10}i$ |  |
| 8 | 207 | $\text{Rationalize } \dfrac{5}{0+4i}.$ | $-\frac{5}{4}i$ |  |
| 16 | 101 | $\text{Rationalize } \dfrac{1}{7-6i}.$ | $\frac{7}{85}+\frac{6}{85}i$ |  |
| 16 | 207 | $\text{Rationalize } \dfrac{7}{3-5i}.$ | $\frac{21}{34}+\frac{35}{34}i$ |  |
| 22 | 101 | $\text{Rationalize } \dfrac{7-4i}{-2-3i}.$ | $-\frac{2}{13}+\frac{29}{13}i$ |  |
| 22 | 207 | $\text{Rationalize } \dfrac{-7-4i}{-9-8i}.$ | $\frac{19}{29}-\frac{4}{29}i$ |  |

Opt-out flag used: `none (hand generator)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax College Algebra 2e §2.4 | https://openstax.org/books/college-algebra-2e/pages/2-4-complex-numbers | Divide; multiply by conjugate |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** New complex rationalize core.
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
