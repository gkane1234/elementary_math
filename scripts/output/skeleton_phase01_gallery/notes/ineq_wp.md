# Notes — `ineq_wp` (`g6_inequalities_word_problems`)

Also covers: `g6_inequalities_word_problems`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Translate a comparison / budget into a linear inequality and solve.
- **D=0:** One-step compare / height / checkout / points — no two-step budget.
- **High D (≈16–22):** Car-rental / phone / tablet budget ($ax+b \le c$) at format_tier ≥ 1.
- **Must not:** Dump $x>12$ as the whole story; bike-only Mad-Lib at high D.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_inequality=True`.

- **D=0 seed=101:** $\text{Jordan wants a score more than } 12\text{. Write an inequality for the score } x\text{.}$ → $x > 12$
- **D=0 seed=207:** $\text{Sam wants a score at least } 5\text{. Write an inequality for the score } x\text{.}$ → $x \ge 5$
- **D=8 seed=101:** $\text{Jordan already has } 5\text{ points and needs at least } 17\text{ points in total. What scores } x \text{ on the next round work?}$ → $x \ge 12$
- **D=8 seed=207:** $\text{Sam already has } 4\text{ points and needs at least } 23\text{ points in total. What scores } x \text{ on the next round work?}$ → $x \ge 19$
- **D=16 seed=101:** $\text{Jordan buys } x \text{ notebooks at \}3\text{ each and a } \5\text{ pen. The total must be at most \}20\text{. How many notebooks can } Jordan\text{ buy?}$ → $x \le 5$
- **D=16 seed=207:** $\text{Sam buys } x \text{ notebooks at \}3\text{ each and a } \8\text{ pen. The total must be at most \}32\text{. How many notebooks can } Sam\text{ buy?}$ → $x \le 8$
- **D=22 seed=101:** $\text{Jordan rents a bike for \}12\text{ plus \}7\text{ per hour. } Jordan\text{ can spend less than \}68\text{. For how many hours } x \text{ can } Jordan\text{ ride?}$ → $x < 8$
- **D=22 seed=207:** $\text{Sam rents a bike for \}20\text{ plus \}4\text{ per hour. } Sam\text{ can spend less than \}40\text{. For how many hours } x \text{ can } Sam\text{ ride?}$ → $x < 5$

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Will wants a score at most 10. Write an inequality for the score.}$ → $x \le 10$ — frame_id=ineq_score, steps=one
- **D=0 seed=207:** $\text{Kevin had some points, lost 1, and now has at least 3. What starting scores work?}$ → $x \ge 4$ — frame_id=ineq_lost, steps=one
- **D=8 seed=101:** $\text{The number of items a shopper can have in the express check-out lane is less than 5. Write an inequality for the number of items n.}$ → $n < 5$ — frame_id=ineq_checkout, steps=one
- **D=8 seed=207:** $\text{Tickets cost \$4 each. Kevin can spend at least \$44. How many tickets can Kevin buy?}$ → $x \ge 11$ — frame_id=ineq_tickets, steps=one
- **D=16 seed=101:** $\text{Hannah has \$65 to buy tablets that cost \$7 each, plus a \$2 delivery fee. How many tablets can Hannah buy?}$ → $x < 9$ — frame_id=ineq_budget, variant=tablets, steps=two
- **D=16 seed=207:** $\text{Wesley rents a car for \$3 plus \$7 per mile. Wesley can spend at most \$52. For how many miles can Wesley drive?}$ → $x \le 7$ — frame_id=ineq_budget, variant=car_rental, steps=two
- **D=22 seed=101:** $\text{Hannah has \$114 to buy tablets that cost \$7 each, plus a \$2 delivery fee. How many tablets can Hannah buy?}$ → $x < 16$ — frame_id=ineq_budget, variant=tablets, steps=two
- **D=22 seed=207:** $\text{Wesley rents a car for \$3 plus \$7 per mile. Wesley can spend at most \$94. For how many miles can Wesley drive?}$ → $x \le 13$ — frame_id=ineq_budget, variant=car_rental, steps=two

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.7** — Translate to an inequality: score, height #504, express checkout #507 — https://openstax.org/books/elementary-algebra-2e/pages/2-7-solve-linear-inequalities
- **OpenStax Intermediate Algebra 2e §2.5** — Tablets / juice (one-step mul); car rental / phone / tablets budget — https://openstax.org/books/intermediate-algebra-2e/pages/2-5-solve-linear-inequalities

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Old high-D is a **bike-rental Mad-Lib**. Default D=0 rotates score / lost / checkout / tickets (EA §2.7). D≥16 prefers IA §2.5 budget vehicles (tablets, car rental, phone) rather than bike-only.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveInequality + `wp_packaging` (wired; budget vehicles rotate at high D).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `wp`
