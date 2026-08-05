# Order of operations audit

Open **[gallery.html](gallery.html)** in a browser for KaTeX-rendered math (markdown preview leaves `$...$` as raw LaTeX).

Samples via the <strong>live continuous-D API path</strong> (<code>QUESTION_TYPES</code> → <code>_generate_for_type</code> → <code>primitive_g6.order_of_operations</code> → <code>build_context</code> + <code>sample_ooo_expression</code>). Budget spend / sample_log / upgrades / n_ops appear in metadata. Addend count and product/quotient mix grow with D; exponents unlock via shared expression_structure knobs. Never emits a bare number.

## default

`{"integers_only": true}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $2 \times 2 - 2$ | $2$ | flat_ooo, product, absorb |
| 0 | $3 \times 2 - 5$ | $1$ | flat_ooo, product, absorb |
| 0 | $3 \times 3 - 2 \times 5$ | $-1$ | flat_ooo, product, product_absorb |
| 0 | $18 \div 6 + 0$ | $3$ | flat_ooo, quotient, absorb |
| 5 | $3 \times 3 + 2 \times 2 - 2 \times 6$ | $1$ | flat_ooo, product, product, product_absorb |
| 5 | $2 \times 2 - 3 \times 3 + 5$ | $0$ | flat_ooo, product, product, absorb |
| 5 | $3 \times 2 + 3 \times 2 - 2 \times 5$ | $2$ | flat_ooo, product, product, product_absorb |
| 5 | $1 - 2 \times 2 + 3$ | $0$ | flat_ooo, plain, product, absorb |
| 10 | $2 \times 2 - 1 + 3 \times 3 - 2 \times 2 - 7$ | $1$ | flat_ooo, product, plain, product, product, absorb |
| 10 | $2 \times 4 - 1 - 2 \times 3 - 2 \times 3 + 9$ | $4$ | flat_ooo, product, plain, product, product, absorb |
| 10 | $2 \times 3 - 2 \times 3 + 3 \times 3 - \left(2 + 2\right) \times 3 + 3$ | $0$ | flat_ooo, product, product, product, group_add, absorb |
| 10 | $2 \times 2 + 4 \times 3 + 2 \times 4 - 2 \times 3 - 3 \times 5$ | $3$ | flat_ooo, product, product, product, product, product_absorb |
| 15 | $3 \times 2 - 3 \times 3 - 3 \times 2 + 2 \times 2 - 3 \times 2^{2} + 2 \times 3 + 13$ | $2$ | flat_ooo, product, product, product, product, product_power, product, absorb |
| 15 | $12 \div 3 - 3 \times 6 - 6 \times 4 + 6 + 9 \div 3 + 4^{2} \times 6 - 67$ | $0$ | flat_ooo, quotient, product, product, plain, quotient, product_power, absorb |
| 15 | $15 \div 5 + 18 \div 6 - 2 \times 2 - 3 \times 2 - 3 - 12 \div 4 + 13$ | $3$ | flat_ooo, quotient, quotient, product, product, plain, quotient, absorb |
| 15 | $18 \div 6 - 8 \div 4 + 2 \times 3 - 2 \times 2 - 3^{2} \times 3 - 2 \times 2^{2} + 3 \times 11$ | $1$ | flat_ooo, quotient, quotient, product, product, product_power, product_power, product_absorb |
| 20 | $4 \times 3 - \left(3 - 2\right) \times 3 - 3 \times 3 + 3 \times 2^{3} + 2 \times 3 - 4 \times 3 - \left(4 - 2\right) \times 2 + 4 \times 4 - 28$ | $2$ | flat_ooo, product, group_sub, product, product_power, product, product, group_sub, product, absorb |
| 20 | $4 \times 4 - 4^{2} \times 4 - 4 \times 3 + 2 \times 3 - \left(4 - 2\right) \times 4 - 2 \times 2 - 4 \times 3 + 78$ | $0$ | flat_ooo, product, product_power, product, product, group_sub, product, product, absorb |
| 20 | $12 \div 6 - 18 \div 6 - 10 \div 5 - 3 \times 2 - 1 - 3 \times 2 - 4 \div 2 + 2 \times 10$ | $2$ | flat_ooo, quotient, quotient, quotient, product, plain, product, quotient, product_absorb |
| 20 | $2 \times 2^{2} - 6 \div 2 + 2 \times 2 + 3^{3} \times 2 + 4 \div 2 + \left(4 - 3\right) \times 2 + 2 \times 2 - 3^{3} \times 2^{3} + 147$ | $2$ | flat_ooo, product_power, quotient, product, product_power, quotient, group_sub, product, product_power_both, absorb |
| 25 | $\left(9 + 7\right) \times 7 + 6 \div 3 + 5 \times 3^{3} + 2^{3} \times 4 + 9 \times 5 + 9 \times 6^{2} - 6 \div 3 + 3 + 7 \times 6 - 682$ | $11$ | flat_ooo, group_add, quotient, product_power, product_power, product, product_power, quotient, plain, product, absorb |
| 25 | $\left(3 - 2\right) \times 2 - 4 \times 4 - 4 \times 4 - 4 \div 2 + 4 \times 4^{2} + 15 \div 5 + 2 \times 2 - 3 \times 4 - 4 \times 2 - 18$ | $1$ | flat_ooo, group_sub, product, product, quotient, product_power, quotient, product, product, product, absorb |
| 25 | $\left(7 - 4\right) \times 8 + 20 \div 5 + 35 \div 5 + 20 \div 5 + \left(2 + 5\right) \times 7 - 3 \times 6 - \left(5 + 6\right) \times 7 + 3 \times 2^{3} - 40 \div 5 - 2 \times 9$ | $-9$ | flat_ooo, group_sub, quotient, quotient, quotient, group_add, product, group_add, product_power, quotient, product_absorb |
| 25 | $4 - 3^{2} \times 4 + \left(5 + 2\right) \times 3 + 30 \div 5 + 4 \times 3 - 2 \times 4 + 2 \times 6 + 4^{2} \times 3 + 5 \times 5^{2} - 184$ | $0$ | flat_ooo, plain, product_power, group_add, quotient, product, product, product, product_power, product_power, absorb |

## friendly

`{"integers_only": true, "number_profile": "friendly_wholes"}`

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $3 \times 2 - 5$ | $1$ | flat_ooo, product, absorb |
| 0 | $3 \times 3 - 7$ | $2$ | flat_ooo, product, absorb |
| 0 | $3 \times 3 - 7$ | $2$ | flat_ooo, product, absorb |
| 0 | $2 \times 3 + 3$ | $9$ | flat_ooo, product, absorb |
| 5 | $3 \times 4 - 3 \times 3 - 2$ | $1$ | flat_ooo, product, product, absorb |
| 5 | $2 \times 2 - 2 \times 2 + 3$ | $3$ | flat_ooo, product, product, absorb |
| 5 | $2 \times 3 + 1 - 5$ | $2$ | flat_ooo, product, plain, absorb |
| 5 | $4 \times 3 - 4 \times 2 - 2$ | $2$ | flat_ooo, product, product, absorb |
| 10 | $3 \times 2 + 3 \times 3 + 3 \times 2 - 3 \times 3 - 2 \times 5$ | $2$ | flat_ooo, product, product, product, product, product_absorb |
| 10 | $4 \times 2 - 3 - 4 \times 3 - 3 \times 3 + 16$ | $0$ | flat_ooo, product, plain, product, product, absorb |
| 10 | $15 \div 5 + 9 \div 3 - 12 \div 4 + 6 \div 2 - 4$ | $2$ | flat_ooo, quotient, quotient, quotient, quotient, absorb |
| 10 | $4 - 3 \times 2 - 2 \times 4 - 3 \times 3 + 3 \times 7$ | $2$ | flat_ooo, plain, product, product, product, product_absorb |
| 15 | $3 \times 2 - 2 \times 3 - 9 \div 3 + 2 \times 3 - 6 \div 2 + 1 - 1$ | $0$ | flat_ooo, product, product, quotient, product, quotient, plain, absorb |
| 15 | $5 \times 3 + 2 + 3 \times 4 - 16 \div 4 + 4 - 12 \div 3 - 19$ | $6$ | flat_ooo, product, plain, product, quotient, plain, quotient, absorb |
| 15 | $10 \div 5 - 18 \div 6 + 3 \times 3 + 3 \times 3 + 3^{3} \times 2^{2} - 15 \div 5 - 122$ | $0$ | flat_ooo, quotient, quotient, product, product, product_power_both, quotient, absorb |
| 15 | $2 \times 3 - 3 \times 3^{2} + 3 \times 3 - 3 \times 2 - 3 \times 2 - 6 \div 2 + 3 \times 10$ | $3$ | flat_ooo, product, product_power, product, product, product, quotient, product_absorb |
| 20 | $3 \times 4 + 4 - 12 \div 3 + \left(4 - 3\right) \times 4^{2} + 18 \div 6 - \left(5 - 4\right) \times 2 + 8 \div 4 + 16 \div 4 - 34$ | $1$ | flat_ooo, product, plain, quotient, group_sub_power, quotient, group_sub, quotient, quotient, absorb |
| 20 | $4^{2} \times 3 + 3 \times 3 - 18 \div 6 - 4 \times 4 - 4 \div 2 - 4 - 16 \div 4 - 27$ | $1$ | flat_ooo, product_power, product, quotient, product, quotient, plain, quotient, absorb |
| 20 | $3^{3} - 8 \div 4 - 3 \times 2 - \left(4 - 3\right) \times 2 - 12 \div 4 - 12 \div 4 - 2 \times 3 - 2$ | $3$ | flat_ooo, power, quotient, product, group_sub, quotient, quotient, product, absorb |
| 20 | $3 \times 3 + 2 \times 2 - \left(3 - 2\right) \times 3 + 15 \div 5 + 2^{3} \times 2 + \left(4 - 3\right) \times 2 - 3 \times 3 + 2^{2} \times 3^{3} - 127$ | $3$ | flat_ooo, product, product, group_sub, quotient, product_power, group_sub, product, product_power_both, absorb |
| 25 | $7^{2} \times 3 - 3 + \left(8 - 7\right) \times 4 - 18 \div 2 - 6 \times 2 - 6 - 2^{2} \times 8 + 11 + 24 \div 3 - 104$ | $4$ | flat_ooo, product_power, plain, group_sub, quotient, product, plain, product_power, plain, quotient, absorb |
| 25 | $2 \times 2 + 2 \times 2 + 2^{3} \times 2 - 4 \times 4 - 2 \times 2 - 4 \times 2 + 2 + 2^{2} \times 3^{2} + 10 \div 5 - 33$ | $3$ | flat_ooo, product, product, product_power, product, product, product, plain, product_power_both, quotient, absorb |
| 25 | $\left(8 + 3\right) \times 4 + 10 \div 5 + 2 \times 5 + 12^{2} \div 3 - 3^{2} \times 7 + 9^{2} \times 2^{2} + 2^{2} \times 8 + 9 - 7 \times 7 - 347$ | $10$ | flat_ooo, group_add, quotient, product, power_quotient, product_power, product_power_both, product_power, plain, product, absorb |
| 25 | $4 \times 4 - 2 \times 2 + 10 \div 2 - 6^{2} + 6 \times 2 + 24 \div 4 + 1 - 30 \div 6 - 4 \times 4 + 23$ | $2$ | flat_ooo, product, product, quotient, power, product, quotient, plain, quotient, product, absorb |
