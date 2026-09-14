# Notes — `one_step_wp` (`g6_equations_word_problems`)

Also covers: `g6_equations_word_problems`, `pa_equations_one_step_word_problems`

Flags:

- `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** One-step equation **as a story** (number, money, tickets) — prompt is the story.
- **D=0:** One easy OpenStax frame (number plus / spent / shares). G6 stays one-step at every D.
- **High D (≈16–22):** Same one-step algebra; harder numbers; extra frames (groups) later.
- **Must not:** Dump stub: “the equation is $x+1=3$”. Mixture / systems.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_equation=True`.

- **D=0 seed=101:** $\text{Sam thinks of a number. After a one-step change, the equation is x - 2 = -3. What was the number?}$ → $x = -1$
- **D=0 seed=207:** $\text{Jordan thinks of a number. After a one-step change, the equation is x + 2 = 5. What was the number?}$ → $x = 3$
- **D=8 seed=101:** $\text{Jordan thinks of a number. After a one-step change, the equation is -2x = 0. What was the number?}$ → $x = 0$
- **D=8 seed=207:** $\text{Sam thinks of a number. After a one-step change, the equation is y - 1 = 6. What was the number?}$ → $y = 7$
- **D=16 seed=101:** $\text{Jordan thinks of a number. After a one-step change, the equation is -4x = -8. What was the number?}$ → $x = 2$
- **D=16 seed=207:** $\text{Sam thinks of a number. After a one-step change, the equation is y - 1 = 14. What was the number?}$ → $y = 15$
- **D=22 seed=101:** $\text{Jordan thinks of a number. After a one-step change, the equation is -4x = 12. What was the number?}$ → $x = -3$
- **D=22 seed=207:** $\text{Sam thinks of a number. After a one-step change, the equation is y - 1 = 14. What was the number?}$ → $y = 15$

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{A number plus }4\text{ is }5\text{. What is the number?}$ → $1$ — frame_id=number_one_step, steps=one
- **D=0 seed=207:** $\text{Kevin collected 2 equal donations totaling \8. How much was each donation?}$ → $\4$ — frame_id=money_donations, steps=one
- **D=8 seed=101:** $\text{A number plus }15\text{ is }17\text{. What is the number?}$ → $2$ — frame_id=number_one_step, steps=one
- **D=8 seed=207:** $\text{Kevin collected 2 equal donations totaling \14. How much was each donation?}$ → $\7$ — frame_id=money_donations, steps=one
- **D=16 seed=101:** $\text{Kim shared \20 equally among 5 friends. How much did each friend receive?}$ → $\4$ — frame_id=money_shared, steps=one
- **D=16 seed=207:** $\text{Lena divided some folders into 7 equal groups with 11 in each group. How many folders were there?}$ → $77\text{ folders}$ — frame_id=count_groups, steps=one
- **D=22 seed=101:** $\text{Kim shared \35 equally among 5 friends. How much did each friend receive?}$ → $\7$ — frame_id=money_shared, steps=one
- **D=22 seed=207:** $\text{Lena divided some folders into 7 equal groups with 20 in each group. How many folders were there?}$ → $140\text{ folders}$ — frame_id=count_groups, steps=one

## OpenStax examples + chapter/section cites

- **OpenStax Intermediate Algebra 2e §2.2** — Number WP, money spent/received/shares, unit amount — https://openstax.org/books/intermediate-algebra-2e/pages/2-2-use-a-problem-solving-strategy
- **OpenStax Elementary Algebra 2e §2.1–2.2** — Translate to an equation and solve (one-step apps) — https://openstax.org/books/elementary-algebra-2e/pages/2-1-solve-equations-using-the-subtraction-and-addition-properties-of-equality

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

**UNCLEAR** — old opt-out is the **dump stub** (“After a one-step change, the equation is $x-2=-3$”). Default uses OpenStax frames (number, donations, received, shared, tickets, groups). OpenStax is richer than the old stub.

## Limitations

- Flags: **UNCLEAR**.
- **UNCLEAR** — old opt-out is the **dump stub** (“After a one-step change, the equation is $x-2=-3$”). Default uses OpenStax frames (number, donations, received, shared, tickets, groups). OpenStax is richer than the old stub.
- Old path can dump a bare equation / identity instead of the named skill.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveLinear one-step + `wp_packaging` (already wired).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `wp`
