# a1: Word problems

`systems_word_problems` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` / `_generate_for_type` / seed / `include_answer_key`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

Difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each.

| D | Prompt | Answer | Engine / spend |
|--:|--------|--------|----------------|
| 0 | $\text{Taylor buys two items. The costs satisfy } \begin{cases} -2x + y = 7 \\ -x - 3y = -7 \end{cases}$ | $x = -2,\ y = 3$ | word_problem; numbers=0.0, variable=0.0, equations=0.0; ups=elimination,unique |
| 0 | $\text{Taylor buys two items. The costs satisfy } \begin{cases} -4x + 3y = -28 \\ 2x + y = 4 \end{cases}$ | $x = 4,\ y = -4$ | word_problem; numbers=0.0, variable=0.0, equations=0.0; ups=elimination,unique |
| 5 | $\text{Jordan buys two items. The costs satisfy } \begin{cases} -3x + 5y = 21 \\ -6x + 6y = 30 \end{cases}$ | $x = -2,\ y = 3$ | word_problem; numbers=0.105, variable=1.805, equations=3.09; ups=elimination,messy_coeffs,unique |
| 5 | $\text{Alex buys two items. The costs satisfy } \begin{cases} -x + y = -6 \\ -2x + 5y = -24 \end{cases}$ | $x = 2,\ y = -4$ | word_problem; numbers=0.477, variable=1.694, equations=2.828; ups=elimination,messy_coeffs,unique |
| 10 | $\text{Sam buys two items. The costs satisfy } \begin{cases} 5x + 3y = 1 \\ 10x + 6y = 1 \end{cases}$ | $\text{no solution}$ | word_problem; numbers=1.209, variable=3.23, equations=5.561; ups=elimination,messy_coeffs,none,special_none |
| 10 | $\text{Taylor buys two items. The costs satisfy } \begin{cases} 3x + 2y = 10 \\ -2x - 5y = -3 \end{cases}$ | $x = 4,\ y = -1$ | word_problem; numbers=1.037, variable=6.952, equations=2.011; ups=elimination,messy_coeffs,unique |
| 15 | $\text{Riley buys two items. The costs satisfy } \begin{cases} 3x + 2y = 5 \\ 9x + 6y = 14 \end{cases}$ | $\text{no solution}$ | word_problem; numbers=0.193, variable=2.89, equations=11.916; ups=elimination,messy_coeffs,none,special_infinite |
| 15 | $\text{Riley buys two items. The costs satisfy } \begin{cases} 5x + y = 2 \\ 20x + 4y = 7 \end{cases}$ | $\text{no solution}$ | word_problem; numbers=0.882, variable=1.495, equations=12.622; ups=elimination,messy_coeffs,none,special_infinite |
| 20 | $\text{Sam buys two items. The costs satisfy } \begin{cases} x + 4y = 3 \\ 4x + 16y = 10 \end{cases}$ | $\text{no solution}$ | word_problem; numbers=1.168, variable=4.598, equations=14.234; ups=elimination,messy_coeffs,none,special_infinite |
| 20 | $\text{Taylor buys two items. The costs satisfy } \begin{cases} x + 4y = 2 \\ 3x + 12y = 5 \end{cases}$ | $\text{no solution}$ | word_problem; numbers=1.174, variable=2.543, equations=16.284; ups=elimination,messy_coeffs,none,special_infinite |
| 25 | $\text{Jordan buys two items. The costs satisfy } \begin{cases} x + 2y = 4 \\ 4x + 8y = 15 \end{cases}$ | $\text{no solution}$ | word_problem; numbers=0.133, variable=4.204, equations=20.663; ups=elimination,messy_coeffs,none,special_infinite |
| 25 | $\text{Taylor buys two items. The costs satisfy } \begin{cases} x - y = 6 \\ -3x + 4y = -22 \end{cases}$ | $x = 2,\ y = -4$ | word_problem; numbers=4.217, variable=19.55, equations=1.232; ups=elimination,unique |
