# a1: Coin word problems

`coin_word_problems` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` / `_generate_for_type` / seed / `include_answer_key`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

Difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each.

| D | Prompt | Answer | Engine / spend |
|--:|--------|--------|----------------|
| 0 | $\text{Casey's piggy bank has 14 coins, all quarters and nickels. The coins are worth \$2.10 in total. How many quarters are there?}$ | $7$ | narrative_wp; equations=0.0 |
| 0 | $\text{A jar contains only quarters and nickels. There are 4 quarters. The coins are worth \$1.30 in total. How many quarters are there?}$ | $4$ | narrative_wp; equations=0.0 |
| 5 | $\text{A cash register holds only quarters and nickels. There are 3 times as many quarters as nickels. The coins are worth \$4.00 in total. How many quarters are there?}$ | $15$ | narrative_wp; equations=5.0; ups=rel_ratio |
| 5 | $\text{A vending change box has 9 coins, all quarters and nickels. There are twice as many quarters as nickels. What is the total value of the coins?}$ | $\$1.65$ | narrative_wp; equations=5.0; ups=ask_value |
| 10 | $\text{Quinn has 11 coins in a pocket, all quarters, dimes, and nickels. There are as many nickels as dimes. The coins are worth \$1.35 in total. How many nickels are there?}$ | $4$ | narrative_wp; equations=10.0; ups=ask_other,three_denoms |
| 10 | $\text{Morgan had some quarters and 7 nickels. Morgan traded 2 nickels for 2 dimes. The coins were then worth \$2.20. How many quarters did Morgan have?}$ | $7$ | narrative_wp; equations=10.0; ups=trade_step |
| 15 | $\text{A vending change box has 21 coins, all quarters, dimes, and nickels. There are 3 more nickels than dimes. The coins are worth \$2.20 in total. How many quarters are there?}$ | $4$ | narrative_wp; equations=15.0; ups=alt_pair,ask_value,three_denoms |
| 15 | $\text{Jordan's piggy bank has 18 coins, all quarters and dimes. There are 2 more quarters than dimes. What is the total value of the coins?}$ | $\$3.30$ | narrative_wp; equations=15.0; ups=alt_pair,ask_value,larger_scale,rel_diff |
| 20 | $\text{Morgan had some quarters and 8 nickels. Morgan traded 4 nickels for 4 dimes. The coins were then worth \$3.85. How many quarters did Morgan have?}$ | $13$ | narrative_wp; equations=20.0; ups=alt_pair,larger_scale,trade_step |
| 20 | $\text{Jordan has 54 coins in a pocket, all dimes and nickels. There are twice as many dimes as nickels. What is the total value of the coins?}$ | $\$4.50$ | narrative_wp; equations=20.0; ups=alt_pair,ask_value,larger_scale,rel_ratio |
| 25 | $\text{Morgan had some quarters and 18 nickels. Morgan traded 4 nickels for 4 dimes. The coins were then worth \$4.10. How many quarters did Morgan have?}$ | $12$ | narrative_wp; equations=25.0; ups=alt_pair,ask_other,larger_scale,trade_step |
| 25 | $\text{A jar contains 26 coins, all dimes and nickels. There are 4 more dimes than nickels. What is the total value of the coins?}$ | $\$2.05$ | narrative_wp; equations=25.0; ups=alt_pair,ask_value,larger_scale,rel_diff |
