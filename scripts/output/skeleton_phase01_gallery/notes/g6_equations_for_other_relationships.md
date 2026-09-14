# Notes — `write_other` (`g6_equations_for_other_relationships`)

Also covers: `g6_equations_for_other_relationships`

Flags:

- `LOW_VARIETY`

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

- **D=0 seed=101:** $\text{Tickets cost \}2\text{ each. Write an equation for the total T for }6\text{ tickets, then find T.}$ → $T = 2\cdot 6;\; T = 12$ — frame_id=write_tickets, steps=one
- **D=0 seed=207:** $\text{Pencils cost }3\text{ cents each. Write an equation for the cost c of }3\text{ pencils, then find c.}$ → $c = 3\cdot 3;\; c = 9$ — frame_id=write_cost, steps=one
- **D=8 seed=101:** $\text{Tickets cost \}3\text{ each. Write an equation for the total T for }11\text{ tickets, then find T.}$ → $T = 3\cdot 11;\; T = 33$ — frame_id=write_tickets, steps=one
- **D=8 seed=207:** $\text{Pencils cost }4\text{ cents each. Write an equation for the cost c of }4\text{ pencils, then find c.}$ → $c = 4\cdot 4;\; c = 16$ — frame_id=write_cost, steps=one
- **D=16 seed=101:** $\text{Tickets cost \}5\text{ each. Write an equation for the total T for }11\text{ tickets, then find T.}$ → $T = 5\cdot 11;\; T = 55$ — frame_id=write_tickets, steps=one
- **D=16 seed=207:** $\text{Pencils cost }7\text{ cents each. Write an equation for the cost c of }4\text{ pencils, then find c.}$ → $c = 7\cdot 4;\; c = 28$ — frame_id=write_cost, steps=one
- **D=22 seed=101:** $\text{Tickets cost \}5\text{ each. Write an equation for the total T for }21\text{ tickets, then find T.}$ → $T = 5\cdot 21;\; T = 105$ — frame_id=write_tickets, steps=one
- **D=22 seed=207:** $\text{Pencils cost }7\text{ cents each. Write an equation for the cost c of }6\text{ pencils, then find c.}$ → $c = 7\cdot 6;\; c = 42$ — frame_id=write_cost, steps=one

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.6** — Cost formula; ticket unit price; perimeter $P=4s$, $P=a+b+c$ — https://openstax.org/books/elementary-algebra-2e/pages/2-6-solve-a-formula-for-a-specific-variable
- **OpenStax Elementary Algebra 2e §8.7 Be Prepared** — Triangular window third side (write $P=a+b+c$) — https://openstax.org/books/elementary-algebra-2e/pages/8-7-solve-proportion-and-similar-figure-applications

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

**LOW_VARIETY** — old D=0 is **pencils-only**; D≥16 always square perimeter. Default rotates tickets / cost / triangle / square (OpenStax richer).

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY** — old D=0 is **pencils-only**; D≥16 always square perimeter. Default rotates tickets / cost / triangle / square (OpenStax richer).
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveLinear one-step + write_cost/tickets/square/triangle frames (already wired).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `wp`
