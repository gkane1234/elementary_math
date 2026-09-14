# Notes — `a2_general_functions_operations`

- **Display name:** Operations
- **Category:** Algebra 2 — General Functions
- **Generator:** `function_operations`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice operations (catalog: function_operations).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{If } f(x) = 3x + 4 \text{ and } g(x) = 3x + 4, \text{ find } (f - g)(4).$ | $0$ | form=fn_subtract |
| 0 | 207 | $\text{If } f(x) = 3x - 4 \text{ and } g(x) = -3x + 3, \text{ find } (f - g)(3).$ | $11$ | form=fn_subtract |
| 8 | 101 | $\text{If } f(x) = 6x + 8 \text{ and } g(x) = 6x + 1, \text{ find } (f \cdot g)(-2).$ | $44$ | form=fn_product |
| 8 | 207 | $\text{If } f(x) = 6x - 8 \text{ and } g(x) = -6x + 7, \text{ find } (f - g)(8).$ | $81$ | form=fn_subtract |
| 16 | 101 | $\text{If } f(x) = 8x + 8 \text{ and } g(x) = 8x + 1, \text{ find } (f \circ g)(-2).$ | $-112$ | form=fn_compose |
| 16 | 207 | $\text{If } f(x) = 8x - 8 \text{ and } g(x) = -8x + 7, \text{ find } (f - g)(8).$ | $113$ | form=fn_subtract |
| 22 | 101 | $\text{If } f(x) = 10x + 7 \text{ and } g(x) = 10x + 6, \text{ find } (f \cdot g)(8).$ | $7482$ | form=fn_product |
| 22 | 207 | $\text{If } f(x) = 10x - 10 \text{ and } g(x) = -10x + 5, \text{ find } (f - g)(6).$ | $105$ | form=fn_subtract |

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

- **Reuse:** Existing `function_operations` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `function_operations`; equations/WP agent owns solve/WP siblings._
