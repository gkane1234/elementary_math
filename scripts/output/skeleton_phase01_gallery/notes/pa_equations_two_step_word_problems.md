# Notes — `two_step_wp` (`pa_equations_two_step_word_problems`)

Also covers: `pa_equations_two_step_word_problems`

Flags:

- `UNCLEAR` / `LOW_VARIETY`

---

## What the question should look like (D=0 vs high D)

- **Skill:** $ax\pm b=c$ as a story (number, twice-more, earnings, unit+fee).
- **D=0:** One two-step OpenStax frame; small ints.
- **High D (≈16–22):** Same two-step species; harder numbers — not multi-step algebra.
- **Must not:** Dump the hidden equation into the prompt.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_linear_equation=True`.

- **D=0 seed=101:** $\text{Alex starts with a number and applies two operations, giving 2x + 2 = 2. What was the starting number?}$ → $x = 0$
- **D=0 seed=207:** $\text{Casey starts with a number and applies two operations, giving x + 2 = -1. What was the starting number?}$ → $x = -3$
- **D=8 seed=101:** $\text{Alex starts with a number and applies two operations, giving -2x - 2 = -14. What was the starting number?}$ → $x = 6$
- **D=8 seed=207:** $\text{Riley starts with a number and applies two operations, giving x + 2 = -7. What was the starting number?}$ → $x = -9$
- **D=16 seed=101:** $\text{Alex starts with a number and applies two operations, giving -x - 4 = -19. What was the starting number?}$ → $x = 15$
- **D=16 seed=207:** $\text{Riley starts with a number and applies two operations, giving x + 2 = -12. What was the starting number?}$ → $x = -14$
- **D=22 seed=101:** $\text{Alex starts with a number and applies two operations, giving -x - 4 = -14. What was the starting number?}$ → $x = 10$
- **D=22 seed=207:** $\text{Riley starts with a number and applies two operations, giving x + 2 = -18. What was the starting number?}$ → $x = -20$

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Julian and Kim together earn \9. Julian earns \3 less than twice what Kim earns. How much does Kim earn?}$ → $\4$ — frame_id=earnings_two_step, steps=two
- **D=0 seed=207:** $\text{Casey and Ethan together earn \9. Casey earns \3 less than twice what Ethan earns. How much does Ethan earn?}$ → $\4$ — frame_id=earnings_two_step, steps=two
- **D=8 seed=101:** $\text{Julian and Kim together earn \12. Julian earns \3 less than twice what Kim earns. How much does Kim earn?}$ → $\5$ — frame_id=earnings_two_step, steps=two
- **D=8 seed=207:** $\text{Casey and Ethan together earn \12. Casey earns \3 less than twice what Ethan earns. How much does Ethan earn?}$ → $\5$ — frame_id=earnings_two_step, steps=two
- **D=16 seed=101:** $\text{Julian and Kim together earn \12. Julian earns \3 less than twice what Kim earns. How much does Kim earn?}$ → $\5$ — frame_id=earnings_two_step, steps=two
- **D=16 seed=207:** $\text{Casey and Ethan together earn \12. Casey earns \3 less than twice what Ethan earns. How much does Ethan earn?}$ → $\5$ — frame_id=earnings_two_step, steps=two
- **D=22 seed=101:** $\text{Julian and Kim together earn \15. Julian earns \3 less than twice what Kim earns. How much does Kim earn?}$ → $\6$ — frame_id=earnings_two_step, steps=two
- **D=22 seed=207:** $\text{Casey and Ethan together earn \15. Casey earns \3 less than twice what Ethan earns. How much does Ethan earn?}$ → $\6$ — frame_id=earnings_two_step, steps=two

## OpenStax examples + chapter/section cites

- **OpenStax Intermediate Algebra 2e §2.2 Example 2.15** — Number two-step: seven times a number plus eight — https://openstax.org/books/intermediate-algebra-2e/pages/2-2-use-a-problem-solving-strategy
- **OpenStax Intermediate Algebra 2e §2.2 Example 2.14 / 2.19** — k more than twice (notebooks); earnings (one earns k less than twice the other) — https://openstax.org/books/intermediate-algebra-2e/pages/2-2-use-a-problem-solving-strategy

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

**UNCLEAR** — old path dumps “applies two operations, giving $2x+2=2$”. **LOW_VARIETY** — default gallery is almost only `earnings_two_step` + `money_two_step`; catalog also has `number_two_step` and `compare_twice` (IA §2.2) that rarely appear.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **UNCLEAR** — old path dumps “applies two operations, giving $2x+2=2$”. **LOW_VARIETY** — default gallery is almost only `earnings_two_step` + `money_two_step`; catalog also has `number_two_step` and `compare_twice` (IA §2.2) that rarely appear.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveLinear two-step + `wp_packaging` (already wired; rotate remaining frames).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `wp`
