# g6: Numeric expressions and the order of operations

`g6_numeric_expressions_and_order_of_operations` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` / `_generate_for_type` / seed / `include_answer_key`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

Difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each.

| D | Prompt | Answer | Engine / spend |
|--:|--------|--------|----------------|
| 0 | $3 \times 2 - 2 \times 2$ | $2$ | ooo; numbers=0.0, variable=0.0, ooo=0.0; n_ops=3; ups=flat_ooo,product,product_absorb |
| 0 | $2 \times 3 - 5$ | $1$ | ooo; numbers=0.0, variable=0.0, ooo=0.0; n_ops=2; ups=flat_ooo,product,absorb |
| 5 | $3 \times 2 - 2 \times 3 + 2$ | $2$ | ooo; numbers=0.704, variable=1.009, ooo=3.287; n_ops=4; ups=flat_ooo,product,product,absorb |
| 5 | $6 \div 2 - 1 - 2$ | $0$ | ooo; numbers=0.336, variable=1.648, ooo=3.016; n_ops=3; ups=flat_ooo,quotient,plain,absorb |
| 10 | $3 \times 2 + 2 \times 3 + 3 \times 3 + 2 \times 2 - 27$ | $-2$ | ooo; numbers=0.243, variable=0.674, ooo=9.083; n_ops=8; ups=flat_ooo,product,product,product |
| 10 | $2 + 3 \times 3 - 3 \times 5 - \left(3 - 2\right) \times 2 + 2 \times 4$ | $2$ | ooo; numbers=4.526, variable=2.881, ooo=2.593; n_ops=8; ups=flat_ooo,plain,product,product |
| 15 | $3 \times 3^{3} + 4 \times 4^{3} + 16 \div 4 + 9 \div 3 - 3 \times 2 - 4 \times 3 - 328$ | $-2$ | ooo; numbers=1.649, variable=5.313, ooo=8.038; n_ops=14; ups=flat_ooo,product_power,product_power,quotient |
| 15 | $2 - 18 \div 6 - 3 \times 3 + 2 \times 3 - \left(4 - 2\right) \times 3 - 3 \times 3 + 2 \times 8$ | $-3$ | ooo; numbers=1.229, variable=1.139, ooo=12.632; n_ops=12; ups=flat_ooo,plain,quotient,product |
| 20 | $3 \times 4^{3} + 4 \times 3 - \left(4 - 3\right) \times 5 + 1 + 25 \div 5 - 3 \times 5 - 2^{2} \times 2 - 185$ | $-3$ | ooo; numbers=2.271, variable=1.254, ooo=16.475; n_ops=15; ups=flat_ooo,product_power,product,group_sub |
| 20 | $2 \times 3 + \left(3 - 2\right) \times 2 + 3 \times 3 - 3 \times 3 - 2 \times 2 + 15 \div 5 - 3 \times 2^{2} + 2 \times 2 - 2$ | $-3$ | ooo; numbers=0.094, variable=0.349, ooo=19.557; n_ops=17; ups=flat_ooo,product,group_sub,product |
| 25 | $2 \times 2^{2} - 4^{2} + 12 \div 6 + \left(3 - 2\right) \times 3^{3} - 3 \times 2^{3} - 8 \div 4 - 3 \times 3 - 2 \times 3 + 3^{3} \times 3^{2} - 223$ | $0$ | ooo; numbers=0.741, variable=2.416, ooo=21.843; n_ops=23; ups=flat_ooo,product_power,power,quotient |
| 25 | $\left(3 + 2\right) \times 2 + 2 \times 2 + \left(2 + 3\right) \times 3^{3} + \left(2 + 3\right) \times 2 - 10 \div 5 - 3 \times 3 - 2^{2} \times 3 - 4 \div 2 - 1 - 133$ | $0$ | ooo; numbers=0.037, variable=9.556, ooo=15.407; n_ops=19; ups=flat_ooo,group_add,product,group_add_power |
