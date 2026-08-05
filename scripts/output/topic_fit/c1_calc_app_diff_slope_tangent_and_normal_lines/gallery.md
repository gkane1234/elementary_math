# c1: Slope, tangent, and normal lines

`calc_app_diff_slope_tangent_and_normal_lines` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` → `_generate_for_type`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

- generator: ``
- difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each
- generated: 2026-07-29T16:29:55.990780+00:00

### Structure inventory

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **6** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `tangent_normal_line:poly_mono` | 3 |
| `tangent_normal_line:poly_quad` | 3 |
| `tangent_normal_line:trig` | 3 |
| `tangent_normal_line:poly_cubic` | 1 |
| `tangent_normal_line:reciprocal` | 1 |
| `tangent_normal_line:trig_chain` | 1 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\text{Find the tangent line to }y=x^{2}\text{ at }x=3.$ | $y-9=6\left(x-3\right)$ | `tangent_normal_line:poly_mono · var=tangent; band=easy` |
| 0 | $\text{Find the tangent line to }y=x^{2}\text{ at }x=3.$ | $y-9=6\left(x-3\right)$ | `tangent_normal_line:poly_mono · var=tangent; band=easy` |
| 5 | $\text{Find the tangent line to }y=2x^{2} + x - 3\text{ at }x=3.$ | $y-18=13\left(x-3\right)$ | `tangent_normal_line:poly_quad · var=tangent; ups=allow_roots; band=medium` |
| 5 | $\text{Find the tangent line to }y=-2 + 2x + x^{2}\text{ at }x=1.$ | $y-1=4\left(x-1\right)$ | `tangent_normal_line:poly_quad · var=tangent; ups=allow_roots; band=medium` |
| 10 | $\text{Find the normal line to }y=x^{3} - 2x\text{ at }x=2.$ | $y-4=-\frac{1}{10}\left(x-2\right)$ | `tangent_normal_line:poly_cubic · var=normal; ups=allow_trig,allow_exp,allow_roots,allow_invtrig; band=hard` |
| 10 | $\text{Find the normal line to }y=x^{2} + x + 1\text{ at }x=1.$ | $y-3=-\frac{1}{3}\left(x-1\right)$ | `tangent_normal_line:poly_quad · var=normal; ups=allow_trig,allow_exp,allow_roots,allow_invtrig; band=hard` |
| 15 | $\text{Find the tangent line to }y=\sin(x)\text{ at }x=0.$ | $y-0=1\left(x-0\right)$ | `tangent_normal_line:trig · var=tangent; ups=allow_trig,allow_exp,allow_ln,allow_nested,allow_roots; band=hard` |
| 15 | $\text{Find the tangent line to }y=\frac{1}{x}\text{ at }x=4.$ | $y-\frac{1}{4}=-\frac{1}{16}\left(x-4\right)$ | `tangent_normal_line:reciprocal · var=tangent; ups=allow_trig,allow_exp,allow_ln,allow_nested,allow_roots; band=hard` |
| 20 | $\text{Find the tangent line to }y=\cos(4x)\text{ at }x=0.$ | $y=1$ | `tangent_normal_line:trig_chain · var=tangent; ups=allow_trig,allow_exp,allow_ln,allow_nested,allow_roots; band=hard` |
| 20 | $\text{Find the tangent line to }y=\sin(x)\text{ at }x=0.$ | $y-0=1\left(x-0\right)$ | `tangent_normal_line:trig · var=tangent; ups=allow_trig,allow_exp,allow_ln,allow_nested,allow_roots; band=hard` |
| 25 | $\text{Find the tangent line to }y=\cos(x)\text{ at }x=0.$ | $y=1$ | `tangent_normal_line:trig · var=tangent; ups=allow_trig,allow_exp,allow_ln,allow_nested,allow_roots; band=hard` |
| 25 | $\text{Find the tangent line to }y=x^{4}\text{ at }x=2.$ | $y-16=32\left(x-2\right)$ | `tangent_normal_line:poly_mono · var=tangent; ups=allow_trig,allow_exp,allow_ln,allow_nested,allow_roots; band=hard` |
