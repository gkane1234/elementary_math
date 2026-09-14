# Notes — `write_other` (`g6_equations_for_other_relationships`)

Also covers: `g6_equations_for_other_relationships`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Write a cost / tickets / perimeter formula and evaluate (one-step).
- **D=0:** Cost $c=nq$ or tickets $T=an$.
- **High D (≈16–22):** Square $P=4s$ (solve for $s$) or triangle $P=a+b+c$.
- **Must not:** Two-price ticket systems / mixture.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_equation=True`.

- **D=0 seed=101:** $\text{Pencils cost } 6 \text{ cents each. Write an equation for the cost } c \text{ of } 3 \text{ pencils, then find } c.$ → $c = 6\cdot 3;\; c = 18$
- **D=0 seed=207:** $\text{Pencils cost } 6 \text{ cents each. Write an equation for the cost } c \text{ of } 3 \text{ pencils, then find } c.$ → $c = 6\cdot 3;\; c = 18$
- **D=8 seed=101:** $\text{Tickets cost \}6\text{ each. Write an equation for the total } T \text{ for } 4 \text{ tickets, then find } T.$ → $T = 6\cdot 4;\; T = 24$
- **D=8 seed=207:** $\text{Tickets cost \}6\text{ each. Write an equation for the total } T \text{ for } 3 \text{ tickets, then find } T.$ → $T = 6\cdot 3;\; T = 18$
- **D=16 seed=101:** $\text{A square has perimeter } 88\text{. Write an equation for the side length } s\text{, then find } s.$ → $4s = 88;\; s = 22$
- **D=16 seed=207:** $\text{A square has perimeter } 76\text{. Write an equation for the side length } s\text{, then find } s.$ → $4s = 76;\; s = 19$
- **D=22 seed=101:** $\text{A square has perimeter } 88\text{. Write an equation for the side length } s\text{, then find } s.$ → $4s = 88;\; s = 22$
- **D=22 seed=207:** $\text{A square has perimeter } 76\text{. Write an equation for the side length } s\text{, then find } s.$ → $4s = 76;\; s = 19$

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Erasers cost }2\text{ cents each. Write an equation for the cost c of }6\text{ erasers, then find c.}$ → $c = 2\cdot 6;\; c = 12$ — frame_id=write_cost, steps=one
- **D=0 seed=207:** $\text{Pencils cost }3\text{ cents each. Write an equation for the cost c of }3\text{ pencils, then find c.}$ → $c = 3\cdot 3;\; c = 9$ — frame_id=write_cost, steps=one
- **D=8 seed=101:** $\text{Tickets cost \$}3\text{ each. Write an equation for the total T for }11\text{ tickets, then find T.}$ → $T = 3\cdot 11;\; T = 33$ — frame_id=write_tickets, steps=one
- **D=8 seed=207:** $\text{Pencils cost }4\text{ cents each. Write an equation for the cost c of }4\text{ pencils, then find c.}$ → $c = 4\cdot 4;\; c = 16$ — frame_id=write_cost, steps=one
- **D=16 seed=101:** $\text{A triangle has perimeter 22. Two sides measure 8 and 10. Write an equation for the third side s, then find s.}$ → $8 + 10 + s = 22;\; s = 4$ — frame_id=write_triangle, steps=one
- **D=16 seed=207:** $\text{A square has perimeter }16\text{. Write an equation for the side length s, then find s.}$ → $4s = 16;\; s = 4$ — frame_id=write_square_invert, steps=one
- **D=22 seed=101:** $\text{A triangle has perimeter 35. Two sides measure 13 and 17. Write an equation for the third side s, then find s.}$ → $13 + 17 + s = 35;\; s = 5$ — frame_id=write_triangle, steps=one
- **D=22 seed=207:** $\text{A square has perimeter }24\text{. Write an equation for the side length s, then find s.}$ → $4s = 24;\; s = 6$ — frame_id=write_square_invert, steps=one

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.6** — Cost formula; ticket unit price; perimeter $P=4s$, $P=a+b+c$ — https://openstax.org/books/elementary-algebra-2e/pages/2-6-solve-a-formula-for-a-specific-variable
- **OpenStax Elementary Algebra 2e §8.7 Be Prepared** — Triangular window third side (write $P=a+b+c$) — https://openstax.org/books/elementary-algebra-2e/pages/8-7-solve-proportion-and-similar-figure-applications

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Old D=0 is **pencils-only**; D≥16 always square perimeter. Default D=0 is cost / tickets; high D writes $4s=P$ (solve for $s$) or triangle $P=a+b+c$ (EA §2.6 / §8.7 Be Prepared).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveLinear one-step + write_cost/tickets/square/triangle frames (wired; D-ladder matches old shapes).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `wp`
