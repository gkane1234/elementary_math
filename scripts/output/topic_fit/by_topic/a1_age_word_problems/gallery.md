# a1: Age word problems

`age_word_problems` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` / `_generate_for_type` / seed / `include_answer_key`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

Difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each.

| D | Prompt | Answer | Engine / spend |
|--:|--------|--------|----------------|
| 0 | $\text{Riley is 4 years older than Morgan. The sum of their ages is 34 years. How old is Morgan?}$ | $15$ | narrative_wp; equations=0.0 |
| 0 | $\text{Alex is 4 years older than Morgan. The sum of their ages is 36 years. How old is Morgan?}$ | $16$ | narrative_wp; equations=0.0 |
| 5 | $\text{Casey is 3 years older than Alex. The sum of their ages is 51 years. How old is Casey?}$ | $27$ | narrative_wp; equations=5.0; ups=ask_older,larger_ages |
| 5 | $\text{Casey is 7 years older than Morgan. 5 years ago, the sum of their ages was 21 years. How old is Morgan?}$ | $12$ | narrative_wp; equations=5.0; ups=past_shift |
| 10 | $\text{Riley is 7 years older than Morgan. In 3 years, the sum of their ages will be 63 years. How old is Riley?}$ | $32$ | narrative_wp; equations=10.0; ups=ask_older,future_shift,larger_ages |
| 10 | $\text{Quinn is twice as old as Sam. The sum of their ages is 39 years. How old is Sam?}$ | $13$ | narrative_wp; equations=10.0; ups=larger_ages,times_as_old |
| 15 | $\text{Casey is 5 years older than Morgan. Jordan is 5 years older than Morgan. The sum of their ages is 70 years. How old is Morgan?}$ | $20$ | narrative_wp; equations=15.0; ups=larger_ages,three_people |
| 15 | $\text{Quinn is 10 years older than Alex. The sum of their ages is 54 years. How old is Quinn?}$ | $32$ | narrative_wp; equations=15.0; ups=ask_older,larger_ages |
| 20 | $\text{Jordan is twice as old as Taylor. The sum of their ages is 60 years. How old is Jordan?}$ | $40$ | narrative_wp; equations=20.0; ups=ask_older,larger_ages,times_as_old |
| 20 | $\text{Alex is 6 years older than Sam. In 6 years, the sum of their ages will be 64 years. How old is Alex?}$ | $29$ | narrative_wp; equations=20.0; ups=ask_older,future_shift,larger_ages |
| 25 | $\text{Sam is 2 years older than Jordan. In 8 years, the sum of their ages will be 72 years. How old is Sam?}$ | $29$ | narrative_wp; equations=25.0; ups=ask_older,future_shift,larger_ages |
| 25 | $\text{Riley is 8 years older than Casey. 6 years ago, the sum of their ages was 46 years. How old is Riley?}$ | $33$ | narrative_wp; equations=25.0; ups=ask_older,larger_ages,past_shift |
