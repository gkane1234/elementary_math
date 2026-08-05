# a1: Multi-step equations

`multi_step_equations` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` / `_generate_for_type` / seed / `include_answer_key`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

Difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each.

| D | Prompt | Answer | Engine / spend |
|--:|--------|--------|----------------|
| 0 | $-x + 4 + \left(x - 1\right)3 = 11x - 23 + \left(x - 2\right)\left(-3\right)$ | $x = 3$ | equations; numbers=0.0, variable=0.0, equations=0.0; n_ops=4; ups=compose_simplify,ops:4,chunks:1,groups:1 |
| 0 | $\left(x - 1\right)\left(-2\right) + 4x + 1 = \left(x - 2\right)\left(-3\right) + 6x - 5$ | $x = 2$ | equations; numbers=0.0, variable=0.0, equations=0.0; n_ops=4; ups=compose_simplify,ops:4,chunks:1,groups:1 |
| 5 | $\left(x + 3\right)3 - 11 = \left(x + 1\right)2 + 7x - 52$ | $x = 8$ | equations; numbers=0.116, variable=1.412, equations=3.472; n_ops=5; ups=compose_simplify,ops:5,chunks:1,groups:1 |
| 5 | $3\left(x + 3\right) - x - 9 = 8x + 30$ | $x = -5$ | equations; numbers=0.573, variable=0.493, equations=3.934; n_ops=5; ups=compose_simplify,ops:5,chunks:1,groups:1 |
| 10 | $-3\left(x + 3\right) + 5x + 6 = -3\left(2x + 1\right) + 11x - \frac{36}{7}$ | $x = \frac{12}{7}$ | equations; numbers=0.31, variable=2.423, equations=7.267; n_ops=8; ups=compose_simplify,ops:8,chunks:1,groups:1 |
| 10 | $y - \frac{4}{3} = -\frac{4}{3}y - \frac{82}{9}$ | $y = -\frac{10}{3}$ | equations; numbers=0.501, variable=4.83, equations=4.669; n_ops=8; ups=clear_fractions,both_sides,ops:8 |
| 15 | $2z - 4 + \left(z - 1\right) * (-3) + \left(-3z + 10 + \left(z - 2\right) * 3\right) = \left(z + 1\right) * 2 + \left(5z - \frac{19}{2} + \left(z - 3\right) * (-2)\right)$ | $z = \frac{3}{4}$ | equations; numbers=1.62, variable=11.389, equations=1.991; n_ops=10; ups=compose_simplify,ops:10,chunks:2,groups:2 |
| 15 | $-2\left(x - 2\right) + 4x - 3 + \left(-2\left(x - 3\right) - 3x - 5\right) = 2\left(x + 2\right) - 4x - 5 + \left(3\left(x + 2\right) - 2x - \frac{31}{10}\right)$ | $x = \frac{1}{20}$ | equations; numbers=0.541, variable=0.464, equations=13.995; n_ops=10; ups=compose_simplify,ops:10,chunks:2,groups:2 |
| 20 | $-5x + 1 + 2\left(x - 2\right) + \left(2x - 4 + 5\left(x + 2\right)\right) = -3x + 70 + 3\left(x - 3\right) + \left(-5x - 7 + 3\left(x + 1\right)\right)$ | $x = 9$ | equations; numbers=3.013, variable=0.195, equations=16.793; n_ops=13; ups=compose_simplify,ops:13,chunks:2,groups:2 |
| 20 | $-2s - 11 + 4\left(s + 3\right) + \left(-4 - 2\left(2s - 2\right)\right) = -5s - 3 + 4\left(2s + 1\right) + \left(-4s + \frac{97}{14} + 2\left(s - 1\right)\right)$ | $s = -\frac{23}{14}$ | equations; numbers=1.695, variable=10.472, equations=7.833; n_ops=13; ups=compose_simplify,ops:13,chunks:2,groups:2 |
| 25 | $-6u - 10 + \left(u + 2\right) * 5 + \left(9u + 13 + \left(u + 2\right) * (-6)\right) + \left(-3u - 1 + \left(u - 1\right) * 6\right) = \left(u - 2\right) * (-2) + \left(8u + 7 + \left(2u + 2\right) * (-3)\right) + \left(10u - \frac{327}{31} + \left(2u + 1\right) * (-2)\right)$ | $u = \frac{48}{31}$ | equations; numbers=3.294, variable=7.316, equations=14.39; n_ops=15; ups=compose_simplify,ops:15,chunks:3,groups:3 |
| 25 | $-4x - 14 + \left(x + 2\right)5 + \left(-2x + 14 + \left(x - 2\right)5\right) + \left(6x - 7 + \left(x - 2\right)\left(-5\right)\right) = \left(-x - 1\right)\left(-3\right) + \left(-2x - 10 + \left(x + 2\right)4\right) + \left(-4x - \frac{31}{8} + \left(x + 3\right)3\right)$ | $x = \frac{25}{8}$ | equations; numbers=2.329, variable=1.52, equations=21.151; n_ops=15; ups=compose_simplify,ops:15,chunks:3,groups:3 |
