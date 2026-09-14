# Notes — `a2_general_functions_evaluating`

- **Display name:** Evaluating
- **Category:** Algebra 2 — General Functions
- **Generator:** `function_evaluate`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice evaluating (catalog: function_evaluate).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{If } f(x) = 2(x - 3)^2 - 5, \text{ find } f(-2).$ | $45$ | — |
| 0 | 207 | $\text{If } f(x) = -3x - 4, \text{ find } f(1).$ | $-7$ | — |
| 8 | 101 | $\text{If } f(x) = 4x + 1, \text{ find } f(1).$ | $5$ | — |
| 8 | 207 | $\text{If } f(x) = x - 3, \text{ find } f(2).$ | $-1$ | — |
| 16 | 101 | $\text{If } f(x) = -5x + 2, \text{ find } f(-3).$ | $17$ | — |
| 16 | 207 | $\text{If } f(x) = 5x - 2, \text{ find } f(-3).$ | $-17$ | — |
| 22 | 101 | $\text{If } f(x) = 2(x + 1)^2 - 6, \text{ find } f(-2).$ | $-4$ | — |
| 22 | 207 | $\text{If } f(x) = (x - 2)^2 - 1, \text{ find } f(3).$ | $0$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §10.1 | https://openstax.org/books/intermediate-algebra-2e/pages/10-1-finding-composite-and-inverse-functions | 10.1 Finding Composite and Inverse Functions — e.g. Example 10.1: For functions $f (x) = 4 x - 5$ and $g (x) = 2 x + 3 ,$ find: ⓐ $\left(\right. f \circ g \left.\right) (x) ,$ ⓑ $\left(\right. g \circ f \left.\right) (x) ,$ and ⓒ $\left(\right. f \cdot g \left.\r…; Example 10.2: For functions $f (x) = x^{2} - 4 ,$ and $g (x) = 3 x + 2 ,$ find: ⓐ $\left(\right. f \circ g \left.\right) (−3) ,$ ⓑ $\left(\right. g \circ f \left.\right) (−1) ,$ and ⓒ $\left(\right. f \circ f \l… |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP leaf unless the generator is story-based. Algebra shapes follow old path samples above.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `function_evaluate` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `function_evaluate`; equations/WP agent owns solve/WP siblings._
