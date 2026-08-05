# g6: Numeric expressions with exponents

`g6_numeric_expressions_with_exponents` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` / `_generate_for_type` / seed / `include_answer_key`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

Difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each.

| D | Prompt | Answer | Engine / spend |
|--:|--------|--------|----------------|
| 0 | $5^{2} - 2 \times 12$ | $1$ | ooo; numbers=0.0, variable=0.0, ooo=0.0; n_ops=3; ups=flat_ooo,power,product_absorb |
| 0 | $4^{3} - 61$ | $3$ | ooo; numbers=0.0, variable=0.0, ooo=0.0; n_ops=2; ups=flat_ooo,power,absorb |
| 5 | $9 \div 3 + 5^{3} - 125$ | $3$ | ooo; numbers=0.414, variable=0.407, ooo=4.179; n_ops=4; ups=flat_ooo,quotient,power,absorb |
| 5 | $2 \times 3 + 3^{2} \times 3 - 30$ | $3$ | ooo; numbers=0.599, variable=0.972, ooo=3.429; n_ops=5; ups=flat_ooo,product,product_power,absorb |
| 10 | $3^{2} \times 2 - 2 \times 2 - 2 \times 3 + 3 \times 3 - 17$ | $0$ | ooo; numbers=0.078, variable=0.03, ooo=9.892; n_ops=9; ups=flat_ooo,product_power,product,product |
| 10 | $2 \times 3 - 2^{2} - 15 \div 5 - 2 \times 2 + 4$ | $-1$ | ooo; numbers=0.085, variable=1.532, ooo=8.383; n_ops=8; ups=flat_ooo,product,power,quotient |
| 15 | $4^{2} \times 2 + 4 \times 4 + 4 \times 4 - 3 - \left(3 + 4\right) \times 4^{2} - 2 + 56$ | $3$ | ooo; numbers=1.04, variable=4.621, ooo=9.339; n_ops=12; ups=flat_ooo,product_power,product,product |
| 15 | $2 \times 3 + 4 \div 2 + 2 \times 3 + 4^{3} - 12 \div 6 - 6 \div 3 - 73$ | $1$ | ooo; numbers=0.555, variable=6.833, ooo=7.612; n_ops=12; ups=flat_ooo,product,quotient,product |
| 20 | $\left(3 - 2\right) \times 3 - 1 - 3 \times 3 + 1 + 3^{2} + \left(3 - 2\right) \times 2 + 12 \div 6 - 2 \times 3$ | $1$ | ooo; numbers=0.053, variable=3.301, ooo=16.647; n_ops=13; ups=flat_ooo,group_sub,plain,product |
| 20 | $3 \times 2 + 10 \div 5 - 2^{2} \times 3 + 1 - 2^{2} + \left(3 + 2\right)^{2} - 3 \times 3 - 2 \times 6$ | $-3$ | ooo; numbers=0.742, variable=8.47, ooo=10.788; n_ops=15; ups=flat_ooo,product,quotient,product_power |
| 25 | $6^{2} \times 6^{2} - 3^{2} \times 4 - 4 - \left(4 + 2\right) \times 6 - 4 \times 4 - 12 \div 6 - 5 \times 3 + 3 \times 6 + 2 \times 6 - 1218$ | $-1$ | ooo; numbers=3.372, variable=5.68, ooo=15.948; n_ops=20; ups=flat_ooo,product_power_both,product_power,plain |
| 25 | $\left(3 + 2\right)^{2} + 2^{2} \times 2 - 2 \times 2 - 1 - 3 \times 2 - 2 \times 7^{2} - 2^{3} \times 2 + 2 \times 2^{3} + 2^{3} + 70$ | $2$ | ooo; numbers=4.446, variable=3.05, ooo=17.504; n_ops=21; ups=flat_ooo,group_power_add,product_power,product |
