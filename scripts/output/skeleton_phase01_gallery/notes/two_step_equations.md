# Notes — `two_step` (`two_step_equations`)

Also covers: `two_step_equations`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve $ax\pm b=c$ (undo add/sub then mul/div).
- **D=0:** Small positive $a$, $b$, $c$ — e.g. $2x+3=15$.
- **High D (≈16–22):** Larger coeffs and negatives before fractions.
- **Must not:** Collapse to one-step $x+b=c$; no distribute / both sides.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_equation=True`.

- **D=0 seed=101:** $2x + 2 = 2$ → $x = 0$ — steps=two
- **D=0 seed=207:** $x + 2 = -1$ → $x = -3$ — steps=two
- **D=8 seed=101:** $-2x - 2 = -14$ → $x = 6$ — steps=two
- **D=8 seed=207:** $x + 2 = -7$ → $x = -9$ — steps=two
- **D=16 seed=101:** $-x - 4 = -19$ → $x = 15$ — steps=two
- **D=16 seed=207:** $x + 2 = -12$ → $x = -14$ — steps=two
- **D=22 seed=101:** $-x - 4 = -14$ → $x = 10$ — steps=two
- **D=22 seed=207:** $x + 2 = -18$ → $x = -20$ — steps=two

## Current default (same D/seeds)

- **D=0 seed=101:** $2x + 3 = 15$ → $x = 6$ — form_id=two_step, steps=two
- **D=0 seed=207:** $3x + 2 = 11$ → $x = 3$ — form_id=two_step, steps=two
- **D=8 seed=101:** $4x - 3 = 45$ → $x = 12$ — form_id=two_step, steps=two
- **D=8 seed=207:** $-3x - 15 = 3$ → $x = -6$ — form_id=two_step, steps=two
- **D=16 seed=101:** $-9x - 7 = 56$ → $x = -7$ — form_id=two_step, steps=two
- **D=16 seed=207:** $-4x + 19 = 63$ → $x = -11$ — form_id=two_step, steps=two
- **D=22 seed=101:** $7x - 5 = 156$ → $x = 23$ — form_id=two_step, steps=two
- **D=22 seed=207:** $-4x + 37 = 81$ → $x = -11$ — form_id=two_step, steps=two

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.2–2.3** — $ax\pm b=c$ before variables on both sides — https://openstax.org/books/elementary-algebra-2e/pages/2-2-solve-equations-using-the-division-and-multiplication-properties-of-equality

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Not a WP. Old opt-out often **degenerates to one-step** at D=0 ($x+2=-1$) and high D ($x+2=-18$). Default keeps two-step $ax\pm b=c$.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveLinear two-step species (already wired).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `solve`
