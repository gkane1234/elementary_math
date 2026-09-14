# Notes — `eq_cancel` (`rational_expressions_equations`)

Also covers: `rational_expressions_equations`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve a rational equation; check extraneous solutions.
- **D=0:** A proportion (two fractions).
- **High D (≈16–22):** One linear denominator, then LCD, then extraneous check.
- **Must not:** Simplify-an-expression (no equation); mixture/DRT story dumps.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_hand_rational_equations=True`.

- **D=0 seed=101:** $\frac{x - 6}{4} = 1$ → $x = 10$
- **D=0 seed=207:** $\frac{x + 4}{3} = -6$ → $x = -22$
- **D=8 seed=101:** $\frac{15}{x} = \frac{5}{3}$ → $x = 9$
- **D=8 seed=207:** $\frac{-15}{x - 6} - 5 = -10$ → $x = 9$
- **D=16 seed=101:** $\frac{-4}{x + 10} + \frac{4}{x - 6} = -1$ → $x = -2$
- **D=16 seed=207:** $\frac{-3}{x + 7} - \frac{5}{x - 1} = 2$ → $x = -9 \text{ or } x = -1$
- **D=22 seed=101:** $\frac{-4}{x + 10} + \frac{4}{x - 6} = -1$ → $x = -2$
- **D=22 seed=207:** $\frac{-3}{x + 7} - \frac{5}{x - 1} = 2$ → $x = -9 \text{ or } x = -1$

Opt-out flag used: `use_hand_rational_equations=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Solve: } \frac{1}{2} = \frac{x}{3}$ → $x = \frac{3}{2}$ — form_id=rational_equation, pattern=EqCancel
- **D=0 seed=207:** $\text{Solve: } \frac{2}{3} = \frac{x}{4}$ → $x = \frac{8}{3}$ — form_id=rational_equation, pattern=EqCancel
- **D=8 seed=101:** $\text{Solve: } \frac{5}{3} = \frac{z}{6}$ → $z = 10$ — form_id=rational_equation, pattern=EqCancel
- **D=8 seed=207:** $\text{Solve: } \frac{3}{3} = \frac{z}{5}$ → $z = 5$ — form_id=rational_equation, pattern=EqCancel
- **D=16 seed=101:** $\text{Solve: } \frac{4}{v + 5} = \frac{1}{v - 2}$ → $v = \frac{13}{3},\; v \neq -5, 2$ — form_id=rational_equation, pattern=EqCancel
- **D=16 seed=207:** $\text{Solve: } \frac{3}{z - 9} = \frac{2}{2z - 11}$ → $z = \frac{15}{4},\; z \neq \frac{11}{2}, 9$ — form_id=rational_equation, pattern=EqCancel
- **D=22 seed=101:** $\text{Solve: } \frac{\tau}{\tau - 4} = \frac{4}{\tau - 4}$ → $\emptyset$ — form_id=rational_equation, pattern=EqCancel
- **D=22 seed=207:** $\text{Solve: } \frac{t}{t - 8} = \frac{8}{t - 8}$ → $\emptyset$ — form_id=rational_equation, pattern=EqCancel

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §8.6 | https://openstax.org/books/elementary-algebra-2e/pages/8-6-solve-rational-equations | Clear dens; proportion first; extraneous values. |
| OpenStax Elementary Algebra 2e §8.7 | https://openstax.org/books/elementary-algebra-2e/pages/8-7-solve-proportion-and-similar-figure-applications | Proportion shape at D=0 — applications stay on WP leaves. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP. Old D=0 is $\frac{x+a}{b}=c$ (one fraction = constant), not a two-fraction
proportion. Default D=0 is $\frac{a}{b}=\frac{x}{c}$ (OpenStax EA §8.6/§8.7 proportion).
Old D≥16 is two rational terms = constant (LCD / extraneous). Default high D adds
explicit excluded values / empty set.

## Limitations

- UNCLEAR: gold look not fully locked — keep red gallery header; do not invent a new engine.
- Gallery section slug: `eq_cancel` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** EqCancel / rational_skeleton (already wired). Opt-out: `use_hand_rational_equations`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `other`

_Catalog:_ Algebra 1 — Rational Expressions — Rational equations. Generator `rational_equations`.
