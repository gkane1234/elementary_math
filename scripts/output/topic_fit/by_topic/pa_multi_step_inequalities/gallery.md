# pa: Multi-step inequalities

`pa_multi_step_inequalities` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` / `_generate_for_type` / seed / `include_answer_key`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

Difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each.

| D | Prompt | Answer | Engine / spend |
|--:|--------|--------|----------------|
| 0 | $-3\left(x + 1\right) + 4x + 5 < -1$ | $x < -3$ | inequalities; numbers=0.0, variable=0.0, inequalities=0.0; n_ops=3; ups=compose_simplify,ops:3,groups:1,nested |
| 0 | $\left(x + 2\right)3 - 2x - 8 < -2$ | $x < 0$ | inequalities; numbers=0.0, variable=0.0, inequalities=0.0; n_ops=3; ups=compose_simplify,ops:3,groups:1,nested |
| 5 | $-3x - 1 + 2\left(x + 1\right) \ge -6x + 4 + 3\left(x - 3\right)$ | $x \ge -3$ | inequalities; numbers=0.037, variable=0.507, inequalities=4.456; n_ops=5; ups=compose_simplify,ops:5,groups:1,nested |
| 5 | $3x + 5 - 2\left(x + 3\right) > 2x + 9 + 3\left(x - 2\right)$ | $x < -1$ | inequalities; numbers=0.698, variable=2.067, inequalities=2.235; n_ops=4; ups=compose_simplify,ops:4,groups:1,nested |
| 10 | $6x - 4 - 3\left(x - 2\right) < 8x - 21 + 2\left(x + 1\right)$ | $x > 3$ | inequalities; numbers=0.462, variable=3.758, inequalities=5.78; n_ops=5; ups=compose_simplify,ops:5,groups:1,nested |
| 10 | $\left(z + 1\right)5 - 3 > \left(z - 1\right)3 - 5z + 40$ | $z > 5$ | inequalities; numbers=2.172, variable=3.31, inequalities=4.518; n_ops=5; ups=compose_simplify,ops:5,groups:1,nested |
| 15 | $5 * \left(x - 2\right) - x + 9 > 3 * \left(x - 3\right) - x$ | $x > -4$ | inequalities; numbers=3.366, variable=0.753, inequalities=10.881; n_ops=8; ups=compose_simplify,ops:8,groups:1,nested |
| 15 | $\left(-z - 2\right)\left(-2\right) + 2z - 3 \le \left(z + 1\right)2 + 6z - 5$ | $z \ge 1$ | inequalities; numbers=1.63, variable=5.199, inequalities=8.171; n_ops=7; ups=compose_simplify,ops:7,groups:1,nested |
| 20 | $-2x - 6 + \left(x + 2\right) * 3 \ge -11 + \left(x - 1\right) * (-2)$ | $x \ge -3$ | inequalities; numbers=0.119, variable=3.427, inequalities=16.453; n_ops=11; ups=compose_simplify,ops:11,groups:2,nested |
| 20 | $\left(2x - 2\right)\left(-2\right) + 8x - 1 < \left(x + 2\right)3 - 2x + 3$ | $x < 2$ | inequalities; numbers=2.836, variable=0.987, inequalities=16.177; n_ops=11; ups=compose_simplify,ops:11,groups:2,nested |
| 25 | $-y + 1 + 4 < 2\left(3y - 1\right)$ | $y > 1$ | inequalities; numbers=3.257, variable=4.665, inequalities=17.078; n_ops=11; ups=compose_simplify,ops:11,groups:1,nested |
| 25 | $-2h - 7 + 3\left(h + 2\right) \le 3h - 17 + 2\left(h + 2\right)$ | $h \ge 3$ | inequalities; numbers=0.017, variable=8.659, inequalities=16.324; n_ops=11; ups=compose_simplify,ops:11,groups:2,nested |
