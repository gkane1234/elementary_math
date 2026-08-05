# c1: Power Rule

`calc_diff_power_rule` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` → `_generate_for_type`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

- generator: ``
- difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each
- generated: 2026-07-29T16:29:55.936892+00:00

### Structure inventory

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `derivative_power_rule:power+sum` | 8 |
| `derivative_power_rule:power` | 4 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\frac{d}{dx}\left[-2x^{3}\right]$ | $-6x^{2}$ | `derivative_power_rule:power · classes=algebraic; band=easy` |
| 0 | $\text{Find }\frac{d}{dx}\left(2x^{2}\right)$ | $4x$ | `derivative_power_rule:power · classes=algebraic; band=easy` |
| 5 | $\text{Find }\frac{d}{dx}\left(3x^{2} - x\right)$ | $6x - 1$ | `derivative_power_rule:power+sum · classes=algebraic; ups=class_roots,extra_term,higher_power; band=medium` |
| 5 | $\frac{d}{dx}\left[x^{3/2}\right]$ | $\frac{3}{2}x^{1/2}$ | `derivative_power_rule:power · classes=algebraic,roots; ups=class_roots,extra_term,higher_power; band=medium` |
| 10 | $\frac{d}{dx}\left[2x^{3} + 5x^{2} - 2x + 4\right]$ | $6x^{2} + 10x - 2$ | `derivative_power_rule:power+sum · classes=algebraic; ups=class_roots,extra_term,higher_power,mix_classes; band=hard` |
| 10 | $\frac{d}{dx}\left[x^{1/2}\right]$ | $\frac{1}{2}x^{-1/2}$ | `derivative_power_rule:power · classes=algebraic,roots; ups=class_roots,extra_term,higher_power,mix_classes; band=hard` |
| 15 | $\text{Find }\frac{d}{dx}\left(x^{2} - 4x + 1\right)$ | $2x - 4$ | `derivative_power_rule:power+sum · classes=algebraic; ups=class_roots,extra_term,higher_power,mix_classes; band=hard` |
| 15 | $\frac{d}{dx}\left[2x^{3} + 5x^{2} + x + 2\right]$ | $6x^{2} + 10x + 1$ | `derivative_power_rule:power+sum · classes=algebraic; ups=class_roots,extra_term,higher_power,mix_classes; band=hard` |
| 20 | $\frac{d}{dx}\left[x^{3} - x^{2} - x - 1\right]$ | $3x^{2} - 2x - 1$ | `derivative_power_rule:power+sum · classes=algebraic; ups=class_roots,extra_term,higher_power,mix_classes; band=hard` |
| 20 | $\text{Find }\frac{d}{dx}\left(x^{3} - 4x^{2} + 3x - 4\right)$ | $3x^{2} - 8x + 3$ | `derivative_power_rule:power+sum · classes=algebraic; ups=class_roots,extra_term,higher_power,mix_classes; band=hard` |
| 25 | $\text{Find }\frac{d}{dx}\left(3x^{2} + 2x - 3\right)$ | $6x + 2$ | `derivative_power_rule:power+sum · classes=algebraic; ups=class_roots,extra_term,higher_power,mix_classes; band=hard` |
| 25 | $\frac{d}{dx}\left[2x^{3} - 2x^{2} + 7x + 4\right]$ | $6x^{2} - 4x + 7$ | `derivative_power_rule:power+sum · classes=algebraic; ups=class_roots,extra_term,higher_power,mix_classes; band=hard` |
