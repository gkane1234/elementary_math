# Notes — `simplify_cancel` (`rational_simplification`)

Also covers: `rational_simplification`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Simplify a single rational expression and state excluded values.
- **D=0:** Cancel a linear common factor; monomial or simple binomial dens.
- **High D (≈16–22):** Quadratic factors; more excluded values. Not add/subtract unlike dens.
- **Must not:** Add/subtract two rationals; complex fractions (A2 leaf).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_constructive_rational=True`.

- **D=0 seed=101:** $\text{Simplify: } \frac{2x^{2} - 4x - 6}{x^{2} - 4x + 3}$ → $\frac{2x + 2}{x - 1},\; x \neq 3$ — form_id=simplify_cancel
- **D=0 seed=207:** $\text{Simplify: } \frac{x^{2} - 5x + 6}{x^{2} + x - 6}$ → $\frac{x - 3}{x + 3},\; x \neq 2$ — form_id=simplify_cancel
- **D=8 seed=101:** $\text{Simplify: } \frac{4x^{2} - 12x + 8}{x^{2} + x - 2}$ → $\frac{4x - 8}{x + 2},\; x \neq 1$ — form_id=simplify_cancel
- **D=8 seed=207:** $\text{Simplify: } \frac{y^{2} - 2y - 3}{y^{2} - y - 6}$ → $\frac{y + 1}{y + 2},\; y \neq 3$ — form_id=simplify_cancel
- **D=16 seed=101:** $\text{Simplify: } \frac{-2\left(g - 2\right)\left(g + 2\right)\left(g + 3\right)}{\left(g + 1\right)\left(g + 4\right)\left(g + 2\right)\left(g + 3\right)}$ → $\frac{-2g + 4}{g^{2} + 5g + 4},\; g \neq -3, -2$ — form_id=simplify_cancel
- **D=16 seed=207:** $\text{Simplify: } \frac{12\left(t - 2\right)\left(t - 1\right)\left(t - 9\right)}{\left(t + 2\right)\left(t + 1\right)\left(t - 1\right)\left(t - 9\right)}$ → $\frac{12t - 24}{t^{2} + 3t + 2},\; t \neq 1, 9$ — form_id=simplify_cancel
- **D=22 seed=101:** $\text{Simplify: } \frac{-8\left(\delta - 2\right)\left(\delta + 2\right)\left(\delta + 5\right)}{\left(\delta + 1\right)\left(\delta - 3\right)\left(\delta + 2\right)\left(\delta + 5\right)}$ → $\frac{-8\delta + 16}{\delta^{2} - 2\delta - 3},\; \delta \neq -5, -2$ — form_id=simplify_cancel
- **D=22 seed=207:** $\text{Simplify: } \frac{\left(\left(-4 + 6\right)\right)\left(6\left(l + 5\right)\left(l - 5\right)\left(l - 7\right)\right)}{\left(\left(-4 + 6\right)\right)\left(\left(l - 1\right)\left(l\right)\left(l - 5\right)\left(l - 7\right)\right)}$ → $\frac{6l + 30}{l^{2} - l},\; l \neq 5, 7$ — form_id=simplify_cancel

Opt-out flag used: `use_constructive_rational=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Simplify: } \frac{3x + 3}{x + 1}$ → $3,\; x \neq -1$ — form_id=simplify_cancel, pattern=SimplifyCancel
- **D=0 seed=207:** $\text{Simplify: } \frac{x^{2} - 3x}{\left(x + 5\right)\left(x - 3\right)}$ → $\frac{x}{x + 5},\; x \neq 3$ — form_id=simplify_cancel, pattern=SimplifyCancel
- **D=8 seed=101:** $\text{Simplify: } \frac{3x + 3}{x + 1}$ → $3,\; x \neq -1$ — form_id=simplify_cancel, pattern=SimplifyCancel
- **D=8 seed=207:** $\text{Simplify: } \frac{x^{2} - 6x}{\left(x + 8\right)\left(x - 6\right)}$ → $\frac{x}{x + 8},\; x \neq 6$ — form_id=simplify_cancel, pattern=SimplifyCancel
- **D=16 seed=101:** $\text{Simplify: } \frac{7\left(c - 2\right)\left(c - 5\right)}{\left(c + 4\right)\left(2c - 3\right)\left(c - 2\right)\left(c - 5\right)}$ → $\frac{7}{\left(c + 4\right)\left(2c - 3\right)},\; c \neq 2, 5$ — form_id=simplify_cancel, pattern=SimplifyCancel
- **D=16 seed=207:** $\text{Simplify: } \frac{2\left(y - 1\right)\left(2y + 1\right)}{\left(y - 7\right)\left(y - 4\right)\left(y - 1\right)\left(2y + 1\right)}$ → $\frac{2}{\left(y - 7\right)\left(y - 4\right)},\; y \neq 1, -\frac{1}{2}$ — form_id=simplify_cancel, pattern=SimplifyCancel
- **D=22 seed=101:** $\text{Simplify: } \frac{-2\left(3p - 8\right)\left(2p - 1\right)}{\left(4p - 5\right)\left(2p + 3\right)\left(3p - 8\right)\left(2p - 1\right)}$ → $\frac{-2}{\left(4p - 5\right)\left(2p + 3\right)},\; p \neq \frac{8}{3}, \frac{1}{2}$ — form_id=simplify_cancel, pattern=SimplifyCancel
- **D=22 seed=207:** $\text{Simplify: } \frac{2\left(q - 2\right)\left(2q + 1\right)}{\left(q - 7\right)\left(q - 4\right)\left(q - 2\right)\left(2q + 1\right)}$ → $\frac{2}{\left(q - 7\right)\left(q - 4\right)},\; q \neq 2, -\frac{1}{2}$ — form_id=simplify_cancel, pattern=SimplifyCancel

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §8.1 | https://openstax.org/books/elementary-algebra-2e/pages/8-1-simplify-rational-expressions | Factor numerator and denominator; cancel; state $x
eq$ excluded. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP. Old D=0 is already quadratic/quadratic cancel (harder than OpenStax §8.1 easy).
Default D=0 is linear cancel $\frac{3x+3}{x+1}$ — simpler, closer to “as simple as old
easy” than the constructive opt-out.

## Limitations

- UNCLEAR: gold look not fully locked — keep red gallery header; do not invent a new engine.
- Gallery section slug: `simplify_cancel` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SimplifyCancel / rational_skeleton (already wired). Opt-out: `use_constructive_rational`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `other`

_Catalog:_ Algebra 1 — Rational Expressions — Simplifying and excluded values. Generator `rational_simplification`.
