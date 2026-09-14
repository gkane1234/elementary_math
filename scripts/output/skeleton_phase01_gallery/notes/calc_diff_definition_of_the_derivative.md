# Notes — `calc_diff_definition_of_the_derivative`

- **Display name:** Definition of the derivative
- **Category:** Calculus — Differentiation
- **Generator:** `definition_of_derivative`
- **Suggested family:** diff / other

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `definition_of_derivative`
- **Remaining limits:** Dedicated constructive / Mad-Lib-meta generators (not expr_skeleton gallery topics). Shared leftover lockout with `calc_app_diff_limits_in_form_of_definition_of_derivative` (easy \(x^{2}\) limits drop at high D). Gaps: no general \(f\) / trig / exp definition limits.

## What the question should look like (D=0 vs high D)

- **Skill:** Definition of the derivative — match OpenStax shape below.
- **D=0:** As simple as live easy samples.
- **High D (≈16–22):** Numeric / structure unlocks via continuous D (not metadata pads).
- **Must not:** Wrong-topic dump; Diff skeleton on non-Diff leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` (default path).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\lim_{x\to 1}\frac{x^{2}-1}{x-1}$ | $2$ | Diff(structured_definition_of_derivative) |
| 0 | 207 | $\lim_{h\to 0}\frac{(1+h)^{2}-1}{h}$ | $2$ | Diff(structured_definition_of_derivative) |
| 8 | 101 | $\text{Use the definition to find }f'(2)\text{ for }f(x)=3x^{2}.$ | $12$ | Diff(structured_definition_of_derivative) |
| 8 | 207 | $\lim_{x\to 2}\frac{x^{2}-4}{x-2}$ | $4$ | Diff(structured_definition_of_derivative) |
| 16 | 101 | $\lim_{h\to 0}\frac{4(5+h)^{2}-100}{h}$ | $40$ | Diff(structured_definition_of_derivative) |
| 16 | 207 | $\lim_{h\to 0}\frac{4(5+h)^{2}-100}{h}$ | $40$ | Diff(structured_definition_of_derivative) |
| 22 | 101 | $\lim_{h\to 0}\frac{4(5+h)^{2}-100}{h}$ | $40$ | Diff(structured_definition_of_derivative) |
| 22 | 207 | $\lim_{h\to 0}\frac{4(5+h)^{2}-100}{h}$ | $40$ | Diff(structured_definition_of_derivative) |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.1 | https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative | limit definition f'(a) |

Local HTML / mine: `scripts/output/example_mining/calculus-volume-1/stage1/`

## Variety notes

Shapes follow live samples; OpenStax frames win for story variety when applicable.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** current catalog generator `definition_of_derivative`.
- **Not this pass:** gallery stub + Limitations; flesh only if gold locked.
