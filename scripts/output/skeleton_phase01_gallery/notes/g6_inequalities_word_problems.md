# Notes — `ineq_wp` (`g6_inequalities_word_problems`)

Also covers: `g6_inequalities_word_problems`

Flags:

- `LOW_VARIETY`

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
- **D=8 seed=101:** $\text{Will wants a score at most 11. Write an inequality for the score.}$ → $x \le 11$ — frame_id=ineq_score, steps=one
- **D=8 seed=207:** $\text{Kevin had some points, lost 3, and now has at least 6. What starting scores work?}$ → $x \ge 9$ — frame_id=ineq_lost, steps=one
- **D=16 seed=101:** $\text{Kim already has 8 points and needs at least 12 points in total. What scores on the next round work?}$ → $x \ge 4$ — frame_id=ineq_points, steps=one
- **D=16 seed=207:** $\text{Lena buys folders at \7 each and a \8 bag. The total must be at most \85. How many folders can Lena buy?}$ → $x \le 11$ — frame_id=ineq_budget, steps=two
- **D=22 seed=101:** $\text{Kim already has 14 points and needs at least 21 points in total. What scores on the next round work?}$ → $x \ge 7$ — frame_id=ineq_points, steps=one
- **D=22 seed=207:** $\text{Lena buys folders at \7 each and a \8 bag. The total must be at most \148. How many folders can Lena buy?}$ → $x \le 20$ — frame_id=ineq_budget, steps=two

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §2.7** — Translate to an inequality: score, height #504, express checkout #507 — https://openstax.org/books/elementary-algebra-2e/pages/2-7-solve-linear-inequalities
- **OpenStax Intermediate Algebra 2e §2.5** — Tablets / juice (one-step mul); car rental / phone / tablets budget — https://openstax.org/books/intermediate-algebra-2e/pages/2-5-solve-linear-inequalities

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

**LOW_VARIETY** — old high-D is a **bike-rental Mad-Lib**; OpenStax has several budget vehicles. Default D=0 already rotates score/lost/points; D≥16 unlocks `ineq_budget` (folders+fee), richer than bike-only.

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY** — old high-D is a **bike-rental Mad-Lib**; OpenStax has several budget vehicles. Default D=0 already rotates score/lost/points; D≥16 unlocks `ineq_budget` (folders+fee), richer than bike-only.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveInequality + `wp_packaging` (already wired).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `wp`
