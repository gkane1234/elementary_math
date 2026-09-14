# Notes — `a2_complex_numbers_absolute_value`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Complex Numbers
- **Generator:** `complex_absolute_value`
- **Suggested family:** `number`

---

## What the question should look like (D=0 vs high D)

- **Skill:** $|a+bi|=\sqrt{a^2+b^2}$ with small ints.
- **D=0:** $|a+bi|=\sqrt{a^2+b^2}$ with small ints.
- **High D (≈16–22):** Larger components; simplified radical.
- **Must not:** Graph / argument.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (hand generator)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\left\|1 - i\right\|$ | $\sqrt{2}$ |  |
| 0 | 207 | $\left\|2 + i\right\|$ | $\sqrt{5}$ |  |
| 8 | 101 | $\left\|1 + 3i\right\|$ | $\sqrt{10}$ |  |
| 8 | 207 | $\left\|5 - 3i\right\|$ | $\sqrt{34}$ |  |
| 16 | 101 | $\left\|-6 - 5i\right\|$ | $\sqrt{61}$ |  |
| 16 | 207 | $\left\|4 + 6i\right\|$ | $2\sqrt{13}$ |  |
| 22 | 101 | $\left\|-7 + 4i\right\|$ | $\sqrt{65}$ |  |
| 22 | 207 | $\left\|-7 + 2i\right\|$ | $\sqrt{53}$ |  |

Opt-out flag used: `none (hand generator)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax College Algebra 2e §2.4 | https://openstax.org/books/college-algebra-2e/pages/2-4-complex-numbers | Modulus $|a+bi|$ |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** New complex modulus core.
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
