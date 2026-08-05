# pa: Multi-step equations

`pa_equations_multi_step_equations` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` / `_generate_for_type` / seed / `include_answer_key`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

Difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each.

| D | Prompt | Answer | Engine / spend |
|--:|--------|--------|----------------|
| 0 | $\left(x - 3\right)2 - x + 9 = \left(x + 2\right)2 - 3x + 1$ | $x = 1$ | equations; numbers=0.0, variable=0.0, equations=0.0; n_ops=4; ups=compose_simplify,ops:4,chunks:1,groups:1 |
| 0 | $1 + \left(x - 1\right)3 = -3x + \left(x - 3\right)2$ | $x = -1$ | equations; numbers=0.0, variable=0.0, equations=0.0; n_ops=4; ups=compose_simplify,ops:4,chunks:1,groups:1 |
| 5 | $-3\left(x - 2\right) + 4x - 3 = -2\left(x + 2\right) - 2x + 17$ | $x = 2$ | equations; numbers=0.313, variable=1.743, equations=2.944; n_ops=5; ups=compose_simplify,ops:5,chunks:1,groups:1 |
| 5 | $3\left(x + 1\right) = -2x - 4 + 3\left(x - 3\right)$ | $x = -8$ | equations; numbers=0.493, variable=0.961, equations=3.546; n_ops=5; ups=compose_simplify,ops:5,chunks:1,groups:1 |
| 10 | $\left(x + 3\right)2 - x - 5 = \left(x + 2\right)2 - 3x + \frac{5}{3}$ | $x = \frac{7}{3}$ | equations; numbers=0.576, variable=0.657, equations=8.766; n_ops=8; ups=compose_simplify,ops:8,chunks:1,groups:1 |
| 10 | $\left(-x - 3\right)\left(-3\right) - x - 10 = \left(x + 1\right)2 + 4x - \frac{53}{5}$ | $x = \frac{19}{10}$ | equations; numbers=1.413, variable=3.755, equations=4.832; n_ops=8; ups=compose_simplify,ops:8,chunks:1,groups:1 |
| 15 | $6 + 3 * \left(k - 2\right) + \left(-4k - 3 + 3 * \left(k + 1\right)\right) = 5k + 5 - 3 * \left(k + 3\right) + \left(-2k + \frac{45}{2} - 3 * \left(k + 2\right)\right)$ | $k = \frac{5}{2}$ | equations; numbers=1.615, variable=8.354, equations=5.032; n_ops=10; ups=compose_simplify,ops:10,chunks:2,groups:2 |
| 15 | $5\rho - 8 + \left(-\rho + 2\right)3 + \left(-5\rho - 3 + \left(2\rho + 2\right)3\right) = -4\rho - 7 + \left(\rho + 2\right)2 + \left(7\rho - \frac{41}{10} + \left(\rho - 3\right)\left(-3\right)\right)$ | $\rho = \frac{9}{10}$ | equations; numbers=0.257, variable=14.18, equations=0.563; n_ops=10; ups=compose_simplify,ops:10,chunks:2,groups:2 |
| 20 | $-2\left(\lambda + 2\right) + 5\lambda + 3 + \left(-2\left(\lambda - 1\right)\right) = 2\left(\lambda + 1\right) - 8\lambda + \frac{120}{13} + \left(2\left(2\lambda - 1\right) - 2\lambda + 1\right)$ | $\lambda = \frac{24}{13}$ | equations; numbers=2.346, variable=14.57, equations=3.084; n_ops=13; ups=compose_simplify,ops:13,chunks:2,groups:2 |
| 20 | $3 * \left(x - 1\right) - 4x + 1 + \left(3 * \left(x + 1\right) - 6x + 2\right) = 3 * \left(x + 2\right) - 6x - \frac{83}{8} + \left(3 * \left(-x + 2\right) + 4x - 3\right)$ | $x = \frac{35}{16}$ | equations; numbers=1.544, variable=1.112, equations=17.344; n_ops=13; ups=compose_simplify,ops:13,chunks:2,groups:2 |
| 25 | $5 + \left(z - 2\right)3 + \left(2z + 10 + \left(z + 3\right)\left(-4\right)\right) + \left(z - 5 + \left(z - 3\right)\left(-3\right)\right) = 5z - 5 + \left(z - 3\right)\left(-2\right) + \left(-4z + 3 + \left(-z + 1\right)\left(-2\right)\right) + \left(-2z + \frac{77}{16} + \left(-z + 2\right)\left(-3\right)\right)$ | $z = \frac{1}{16}$ | equations; numbers=1.89, variable=5.96, equations=17.15; n_ops=15; ups=compose_simplify,ops:15,chunks:3,groups:3 |
| 25 | $6 + \left(z - 2\right)3 + \left(z + 5 + \left(z - 2\right)2\right) + \left(-z - 3 + \left(2z - 2\right)\left(-2\right)\right) = -7z - \frac{181}{11} + \left(z + 3\right)2 + \left(\left(z + 1\right)\left(-2\right)\right) + \left(1 + \left(z + 1\right)3\right)$ | $z = -\frac{23}{11}$ | equations; numbers=4.454, variable=11.995, equations=8.551; n_ops=15; ups=compose_simplify,ops:15,chunks:3,groups:3 |
