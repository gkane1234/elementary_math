# a1: Order of operations

`order_of_operations` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` / `_generate_for_type` / seed / `include_answer_key`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

Difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each.

| D | Prompt | Answer | Engine / spend |
|--:|--------|--------|----------------|
| 0 | $2 \times 3 - 2 \times 4$ | $-2$ | ooo; numbers=0.0, variable=0.0, ooo=0.0; n_ops=3; ups=flat_ooo,product,product_absorb |
| 0 | $3 \times 2 - 5$ | $1$ | ooo; numbers=0.0, variable=0.0, ooo=0.0; n_ops=2; ups=flat_ooo,product,absorb |
| 5 | $1 - 3 \times 2 + 8$ | $3$ | ooo; numbers=0.224, variable=0.415, ooo=4.361; n_ops=3; ups=flat_ooo,plain,product,absorb |
| 5 | $2 \times 3 - 4 \div 2 - 3$ | $1$ | ooo; numbers=0.397, variable=0.191, ooo=4.412; n_ops=4; ups=flat_ooo,product,quotient,absorb |
| 10 | $2 + 4 \div 2 - 3 \times 2 - 3 \times 2 + 9$ | $1$ | ooo; numbers=0.138, variable=6.025, ooo=3.836; n_ops=7; ups=flat_ooo,plain,quotient,product |
| 10 | $2 \times 2 + 8 \div 4 + 12 \div 6 - 3 \times 3 + 1$ | $0$ | ooo; numbers=0.982, variable=2.918, ooo=6.1; n_ops=8; ups=flat_ooo,product,quotient,quotient |
| 15 | $3 \times 2^{2} + 12 \div 6 + 4 \div 2 - 18 \div 6 - 2 \times 2 + 2 - 2 \times 6$ | $-1$ | ooo; numbers=0.15, variable=6.06, ooo=8.79; n_ops=13; ups=flat_ooo,product_power,quotient,quotient |
| 15 | $2 \times 2 - 2 \times 2 + 2 \times 3 + 8 \times 3 + 3^{3} \times 3 + 12 \div 4 - 109$ | $5$ | ooo; numbers=4.326, variable=3.187, ooo=7.487; n_ops=13; ups=flat_ooo,product,product,product |
| 20 | $2 \times 2 - \left(4 - 3\right) \times 3 - 4 \times 4^{2} - 4 \times 2^{3} - 8 \div 4 + 2 \times 2 + 8 \div 2 + 85$ | $-4$ | ooo; numbers=1.25, variable=6.972, ooo=11.778; n_ops=16; ups=flat_ooo,product,group_sub,product_power |
| 20 | $10 \div 5 + 4 \times 3^{3} - 2^{3} \times 2^{3} + 1 - 10 \div 5 - 12 \div 6 + 4 \div 2 - 5 \times 9$ | $0$ | ooo; numbers=1.974, variable=3.844, ooo=14.182; n_ops=17; ups=flat_ooo,quotient,product_power,product_power_both |
| 25 | $3 \times 3 + 3 \times 3 - 2 \times 2 - 3 + 2 \times 4 + 3 \times 3 - 4 \times 2 + 2 \times 4 + 3 \times 4^{2} - 6 \times 12$ | $4$ | ooo; numbers=1.441, variable=1.644, ooo=21.916; n_ops=19; ups=flat_ooo,product,product,product |
| 25 | $1 + \left(5 + 6\right) \times 3^{3} + 12 \div 6 + 3 \times 3 - 3 \times 5^{3} - 5 + 6^{2} \times 2^{2} + 12 \div 2 - 4 \times 5 - 59$ | $0$ | ooo; numbers=3.532, variable=9.389, ooo=12.079; n_ops=20; ups=flat_ooo,plain,group_add_power,quotient |
