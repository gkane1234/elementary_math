# a1: More on slope

`more_on_slope` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` / `_generate_for_type` / seed / `include_answer_key`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

Difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each.

| D | Prompt | Answer | Engine / spend |
|--:|--------|--------|----------------|
| 0 | $\text{Find the slope of the line through } (1, 2) \text{ and } (4, 8).$ | $2$ | slope; numbers=0.0, variable=0.0, equations=0.0 |
| 0 | $\text{Find the slope of the line through } (3, 1) \text{ and } (6, 7).$ | $2$ | slope; numbers=0.0, variable=0.0, equations=0.0 |
| 5 | $\text{Find the slope of the line through } (0, 1) \text{ and } (3, -2).$ | $-1$ | slope; numbers=0.355, variable=2.784, equations=1.861; ups=negative_slope |
| 5 | $\text{Find the slope of the line through } (1, -3) \text{ and } (3, -9).$ | $-3$ | slope; numbers=0.96, variable=2.608, equations=1.432; ups=negative_slope |
| 10 | $\text{Find the slope of the line } y = -x + 1.$ | $-1$ | slope; numbers=0.856, variable=5.71, equations=3.434; ups=from_equation,negative_slope |
| 10 | $\text{Find the slope of the line } y = -4x + 2.$ | $-4$ | slope; numbers=1.386, variable=4.114, equations=4.5; ups=from_equation,negative_slope |
| 15 | $\text{Find the slope of the line } y = -\frac{1}{2}x + 3.$ | $-\frac{1}{2}$ | slope; numbers=1.614, variable=3.188, equations=10.199; ups=fraction_slope,from_equation,negative_slope |
| 15 | $\text{Find the slope of the line } y = -\frac{1}{3}x + 3.$ | $-\frac{1}{3}$ | slope; numbers=0.514, variable=6.48, equations=8.006; ups=fraction_slope,from_equation,negative_slope |
| 20 | $\text{Find the slope of the line } y = -\frac{1}{2}x.$ | $-\frac{1}{2}$ | slope; numbers=3.112, variable=4.105, equations=12.783; ups=fraction_slope,from_equation,negative_slope |
| 20 | $\text{Find the slope of the line } y = -2x + 2.$ | $-2$ | slope; numbers=1.545, variable=2.4, equations=16.055; ups=fraction_slope,from_equation,negative_slope |
| 25 | $\text{Find the slope of the line } y = -x + 1.$ | $-1$ | slope; numbers=0.572, variable=3.489, equations=20.939; ups=fraction_slope,from_equation,negative_slope |
| 25 | $\text{Find the slope of the line } y = -x + 4.$ | $-1$ | slope; numbers=2.37, variable=12.049, equations=10.581; ups=fraction_slope,from_equation,negative_slope |
