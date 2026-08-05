# c1: Product Rule

`calc_diff_product_rule` — continuous difficulty samples for topic-fit / ramp review.

Samples via the **live continuous-D API path** (`QUESTION_TYPES` → `_generate_for_type`).

Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** (markdown preview leaves `$...$` as raw LaTeX).

- generator: ``
- difficulties: 0, 5, 10, 15, 20, 25 · 2 sample(s) each
- generated: 2026-07-29T16:29:55.942483+00:00

### Structure inventory

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `derivative_product_rule:power+product+sum` | 10 |
| `derivative_product_rule:power+product` | 2 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\frac{d}{dx}\left[\left(-x^{3}\right)\left(2x^{4}\right)\right]$ | $\left(-3x^{2}\right)\left(2x^{4}\right)+\left(-x^{3}\right)\left(8x^{3}\right)$ | `derivative_product_rule:power+product · classes=algebraic; ups=use_product; band=easy` |
| 0 | $\frac{d}{dx}\left[\left(-3x^{4}\right)\left(-x^{4}\right)\right]$ | $\left(-12x^{3}\right)\left(-x^{4}\right)+\left(-3x^{4}\right)\left(-4x^{3}\right)$ | `derivative_product_rule:power+product · classes=algebraic; ups=use_product; band=easy` |
| 5 | $\frac{d}{dx}\left[\left(3x^{3} - 2x^{2} + x - 1\right)\left(x^{4}\right)\right]$ | $\left(9x^{2} - 4x + 1\right)\left(x^{4}\right)+\left(3x^{3} - 2x^{2} + x - 1\right)\left(4x^{3}\right)$ | `derivative_product_rule:power+product+sum · classes=algebraic; ups=extra_term,higher_power,use_chain,use_product; band=medium` |
| 5 | $\frac{d}{dx}\left[\left(-3x^{5}\right)\left(x^{3} + x^{2} - 4x + 5\right)\right]$ | $\left(-15x^{4}\right)\left(x^{3} + x^{2} - 4x + 5\right)+\left(-3x^{5}\right)\left(3x^{2} + 2x - 4\right)$ | `derivative_product_rule:power+product+sum · classes=algebraic; ups=extra_term,higher_power,use_chain,use_product; band=medium` |
| 10 | $\text{Find }\frac{d}{dx}\left(\left(-4x^{3}\right)\left(x^{2} - 5x + 5\right)\right)$ | $\left(-12x^{2}\right)\left(x^{2} - 5x + 5\right)+\left(-4x^{3}\right)\left(2x - 5\right)$ | `derivative_product_rule:power+product+sum · classes=algebraic; ups=extra_term,higher_power,use_chain,use_product; band=hard` |
| 10 | $\frac{d}{dx}\left[\left(2x^{3} + 4x^{2} - x - 1\right)\left(-2x^{6}\right)\right]$ | $\left(6x^{2} + 8x - 1\right)\left(-2x^{6}\right)+\left(2x^{3} + 4x^{2} - x - 1\right)\left(-12x^{5}\right)$ | `derivative_product_rule:power+product+sum · classes=algebraic; ups=extra_term,higher_power,use_chain,use_product; band=hard` |
| 15 | $\frac{d}{dx}\left[\left(4x^{6}\right)\left(2x^{3} + 4x^{2} - 5x + 4\right)\right]$ | $\left(24x^{5}\right)\left(2x^{3} + 4x^{2} - 5x + 4\right)+\left(4x^{6}\right)\left(6x^{2} + 8x - 5\right)$ | `derivative_product_rule:power+product+sum · classes=algebraic; ups=chain_depth_2,extra_term,higher_power,use_chain,use_product; band=hard` |
| 15 | $\frac{d}{dx}\left[\left(-x^{6}\right)\left(3x^{3} + 6x^{2} - 2\right)\right]$ | $\left(-6x^{5}\right)\left(3x^{3} + 6x^{2} - 2\right)+\left(-x^{6}\right)\left(9x^{2} + 12x\right)$ | `derivative_product_rule:power+product+sum · classes=algebraic; ups=chain_depth_2,extra_term,higher_power,use_chain,use_product; band=hard` |
| 20 | $\text{Find }\frac{d}{dx}\left(\left(3x^{3} + 2x^{2} - 7x + 7\right)\left(2x^{4}\right)\right)$ | $\left(9x^{2} + 4x - 7\right)\left(2x^{4}\right)+\left(3x^{3} + 2x^{2} - 7x + 7\right)\left(8x^{3}\right)$ | `derivative_product_rule:power+product+sum · classes=algebraic; ups=chain_depth_2,extra_term,higher_power,use_chain,use_product; band=hard` |
| 20 | $\frac{d}{dx}\left[\left(-3x^{3}\right)\left(x^{2} - 2x - 6\right)\right]$ | $\left(-9x^{2}\right)\left(x^{2} - 2x - 6\right)+\left(-3x^{3}\right)\left(2x - 2\right)$ | `derivative_product_rule:power+product+sum · classes=algebraic; ups=chain_depth_2,extra_term,higher_power,use_chain,use_product; band=hard` |
| 25 | $\text{Find }\frac{d}{dx}\left(\left(x^{3} + 5x^{2} - 5x + 4\right)\left(-5x^{3}\right)\right)$ | $\left(3x^{2} + 10x - 5\right)\left(-5x^{3}\right)+\left(x^{3} + 5x^{2} - 5x + 4\right)\left(-15x^{2}\right)$ | `derivative_product_rule:power+product+sum · classes=algebraic; ups=chain_depth_2,extra_term,higher_power,use_chain,use_product; band=hard` |
| 25 | $\frac{d}{dx}\left[\left(3x^{3} - 8x^{2} - 5x + 2\right)\left(-7x^{5}\right)\right]$ | $\left(9x^{2} - 16x - 5\right)\left(-7x^{5}\right)+\left(3x^{3} - 8x^{2} - 5x + 2\right)\left(-35x^{4}\right)$ | `derivative_product_rule:power+product+sum · classes=algebraic; ups=chain_depth_2,extra_term,higher_power,use_chain,use_product; band=hard` |
