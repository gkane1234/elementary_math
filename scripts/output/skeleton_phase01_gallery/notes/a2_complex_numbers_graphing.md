# Notes — `a2_complex_numbers_graphing`

> **UNCLEAR / NOT_IMPLEMENTED** — Complex plane graph — IA §8.8; old path may be identity-style.

- **Display name:** Graphing
- **Category:** Algebra 2 — Complex Numbers
- **Generator:** `complex_graph`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice graphing (catalog: complex_graph).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Plot } 1 - i \text{ on the complex plane.}$ | $(1, -1)$ | — |
| 0 | 207 | $\text{Plot } -1 + i \text{ on the complex plane.}$ | $(-1, 1)$ | — |
| 8 | 101 | $\text{Plot } 1 - 5i \text{ on the complex plane.}$ | $(1, -5)$ | — |
| 8 | 207 | $\text{Plot } -4 \text{ on the complex plane.}$ | $(-4, 0)$ | — |
| 16 | 101 | $\text{Plot } -1 - 4i \text{ on the complex plane.}$ | $(-1, -4)$ | — |
| 16 | 207 | $\text{Plot } 3 - i \text{ on the complex plane.}$ | $(3, -1)$ | — |
| 22 | 101 | $\text{Plot } 2 + 8i \text{ on the complex plane.}$ | $(2, 8)$ | — |
| 22 | 207 | $\text{Plot } 7 + 8i \text{ on the complex plane.}$ | $(7, 8)$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §8.8 | https://openstax.org/books/intermediate-algebra-2e/pages/8-8-use-the-complex-number-system | 8.8 Use the Complex Number System — e.g. Example 8.76: Write each expression in terms of i and simplify if possible: ⓐ $\sqrt{−25}$ ⓑ $\sqrt{−7}$ ⓒ $\sqrt{−12} .$; Example 8.77: Add: $\sqrt{−12} + \sqrt{−27} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Complex plane graph — IA §8.8; old path may be identity-style.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `complex_graph` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `complex_graph`; equations/WP agent owns solve/WP siblings._
