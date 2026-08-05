# c1: Differentials

`calc_app_diff_differentials` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` → `_generate_for_type`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

- generator: `differentials`
- difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each
- generated: 2026-07-29T16:33:20.730527+00:00

### Structure inventory

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **6** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `differentials:poly_quad` | 4 |
| `differentials:poly_power` | 2 |
| `differentials:reciprocal` | 2 |
| `differentials:trig` | 2 |
| `differentials:exp` | 1 |
| `differentials:product` | 1 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\text{For }y=x\left(x + 5\right),\text{ find }dy.$ | $dy=\left(2x + 5\right)\,dx$ | `differentials:poly_quad · var=factored_linear; D=0` |
| 0 | $\text{For }y=\cos(x),\text{ find }dy.$ | $dy=-\sin(x)\,dx$ | `differentials:trig · var=cos; D=0` |
| 5 | $\text{For }y=x^{2} + x,\text{ find }dy.$ | $dy=\left(2x + 1\right)\,dx$ | `differentials:poly_quad · var=standard; D=5; ups=allow_roots` |
| 5 | $\text{For }y=x^{2} + 4x,\text{ find }dy.$ | $dy=\left(2x + 4\right)\,dx$ | `differentials:poly_quad · var=standard; D=5; ups=allow_roots` |
| 10 | $\text{For }y=\cos x,\text{ find }dy.$ | $dy=-\sin(x)\,dx$ | `differentials:trig · var=cos; D=10; ups=allow_trig,allow_exp,allow_roots,allow_invtrig` |
| 10 | $\text{For }y=x^{-1},\text{ find }dy.$ | $dy=-\frac{1}{x^{2}}\,dx$ | `differentials:reciprocal · var=frac; D=10; ups=allow_trig,allow_exp,allow_roots,allow_invtrig` |
| 15 | $\text{For }y=x^{-1},\text{ find }dy.$ | $dy=-\frac{1}{x^{2}}\,dx$ | `differentials:reciprocal · var=neg_power; D=15; ups=allow_trig,allow_exp,allow_ln,allow_nested,allow_roots` |
| 15 | $\text{For }y=x\cdot\sin(x),\text{ find }dy.$ | $dy=\left(\sin(x)+x\cos(x)\right)\,dx$ | `differentials:product · var=sin_first; D=15; ups=allow_trig,allow_exp,allow_ln,allow_nested,allow_roots` |
| 20 | $\text{For }y=x + x^{2},\text{ find }dy.$ | $dy=\left(2x + 1\right)\,dx$ | `differentials:poly_quad · var=reversed; D=20; ups=allow_trig,allow_exp,allow_ln,allow_nested,allow_roots` |
| 20 | $\text{For }y=x^{3},\text{ find }dy.$ | $dy=3x^{2}\,dx$ | `differentials:poly_power · var=power:3; D=20; ups=allow_trig,allow_exp,allow_ln,allow_nested,allow_roots` |
| 25 | $\text{For }y=\exp(3x),\text{ find }dy.$ | $dy=3e^{3x}\,dx$ | `differentials:exp · var=e:k3; D=25; ups=allow_trig,allow_exp,allow_ln,allow_nested,allow_roots` |
| 25 | $\text{For }y=x^{3},\text{ find }dy.$ | $dy=3x^{2}\,dx$ | `differentials:poly_power · var=power:3; D=25; ups=allow_trig,allow_exp,allow_ln,allow_nested,allow_roots` |
