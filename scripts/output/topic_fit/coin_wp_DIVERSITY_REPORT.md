# Coin / age / consecutive WP diversity — spot-check

## Root cause

`CoinProblemFramework` / `AgeProblemFramework` used a **single fill-in-the-blank script**
(jar + quarters/nickels + total; or sum+difference ages). Continuous `difficulty`
only changed integer ranges, so worksheets looked identical.

## Fix (framework path — not Mad-Libs piles)

- New sampler: `question_engine/frameworks/primitives/narrative_wp.py`
- Continuous D → `build_context` → `DifficultyFactor` upgrades (knobs in
  `difficulty_knobs.json` → `narrative_wp`)
- **Sample structure** (required coin counts/values; optional ratio / 3rd denom /
  trade / age time-shift / three people) → **compose** prompts from short phrase
  fragments (frame pool + constraint clauses)
- Thin adapters: `CoinProblemFramework` / `AgeProblemFramework` /
  `ConsecutiveIntegersFramework` call the sampler and emit
  `shape_id`, `n_constraints`, `upgrades`, `spend`

## Before → after (coin)

**Before (any D):**  
`A jar contains N coins, all quarters and nickels, worth $X. How many quarters are in the jar?`

**After — easy D=0 (2 constraints, base shape):**
1. Quinn has 16 coins in a pocket, all quarters and nickels. The coins are worth $1.80 in total. How many quarters are there? → 5  
   `[coin:count_value] n=2`
2. A vending change box has 9 coins, all quarters and nickels. The coins are worth $1.85 in total. How many quarters are there? → 7  
   `[coin:count_value] n=2`
3. Casey has 15 coins in a pocket, all quarters and nickels. The coins are worth $2.75 in total. How many quarters are there? → 10  
   `[coin:count_value] n=2`

**After — hard D=20 (extra relations / denoms / asks):**
1. A jar contains 20 coins, all quarters and pennies. There are 6 more quarters than pennies. What is the total value of the coins? → $3.32  
   `[coin:diff+ask_value]` upgrades: rel_diff, ask_value, alt_pair, …
2. A jar contains 33 coins, all quarters, dimes, and nickels. There is 1 more nickel than dimes. The coins are worth $4.20 in total. How many quarters are there? → 10  
   `[coin:three+diff] n=3`
3. A vending change box has 17 coins, all quarters and pennies. There are 5 more quarters than pennies. What is the total value of the coins? → $2.81  
   `[coin:diff+ask_value]`

## Verification

- `pytest question_engine/tests/test_narrative_wp_diversity.py` — pass  
  (D=0 vs D=20: shape/fingerprint diversity; hard has higher `n_constraints` + three/trade upgrades)
- Live `_generate_for_type` spot-checks above
- Galleries regenerated: `scripts/output/topic_fit/by_topic/{coin,age,consecutive_integers}_word_problems/`
