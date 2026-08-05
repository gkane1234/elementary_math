# Calculus derivative-rules gallery

Generated: 2026-07-29T16:29:56.182161+00:00

Continuous-D samples via live `_generate_for_type` (D = 0, 5, 10, 15, 20, 25, 2/level).

Open [gallery.html](gallery.html) in a browser for KaTeX.

## Structure inventory (all types)

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **66** · samples: **180**

| Structure / family | Count |
|--------|------:|
| `derivative_product_rule:power+product+sum` | 10 |
| `derivative_quotient_rule:power+quotient+sum` | 10 |
| `derivative_inverse_trig:chain` | 9 |
| `derivative_power_rule:power+sum` | 8 |
| `derivative_logarithmic:power` | 7 |
| `derivative_chain_rule:chain` | 6 |
| `derivative_chain_rule:chain+power` | 6 |
| `derivative_higher_order:poly3_second` | 5 |
| `average_rate_of_change:linear` | 4 |
| `derivative_higher_order:poly4_third` | 4 |
| `derivative_implicit:trig` | 4 |
| `derivative_logarithmic:root` | 4 |
| `derivative_power_rule:power` | 4 |
| `derivative_trigonometric:power+quotient+sum` | 4 |
| `average_rate_of_change:quad` | 3 |
| `definition_of_derivative:limit_x` | 3 |
| `definition_of_derivative:linear_coef` | 3 |
| `derivative_implicit:circle` | 3 |
| `derivative_inverse_functions:linear` | 3 |
| `derivative_ln_exp:chain+power+product` | 3 |
| `derivative_ln_exp:power+product` | 3 |
| `derivative_other_base:log_x` | 3 |
| `instantaneous_rate_of_change:power` | 3 |
| `average_rate_of_change:poly` | 2 |
| `average_rate_of_change:quad_const` | 2 |
| `definition_of_derivative:cube` | 2 |
| `definition_of_derivative:named` | 2 |
| `derivative_implicit:ellipse` | 2 |
| `derivative_implicit:line_prod` | 2 |
| `derivative_inverse_functions:cubic` | 2 |
| `derivative_inverse_functions:exp` | 2 |
| `derivative_inverse_functions:power` | 2 |
| `derivative_inverse_trig:power` | 2 |
| `derivative_ln_exp:chain+power+product+sum` | 2 |
| `derivative_ln_exp:power` | 2 |
| `derivative_other_base:a_kx` | 2 |
| `derivative_other_base:a_x` | 2 |
| `derivative_other_base:log_linear` | 2 |
| `derivative_other_base:log_power` | 2 |
| `derivative_product_rule:power+product` | 2 |
| `derivative_quotient_rule:power+quotient` | 2 |
| `derivative_trigonometric:chain` | 2 |
| `derivative_trigonometric:chain+power+quotient` | 2 |
| `derivative_trigonometric:power` | 2 |
| `derivative_trigonometric:power+quotient` | 2 |
| `instantaneous_rate_of_change:cubic` | 2 |
| `instantaneous_rate_of_change:exp` | 2 |
| `instantaneous_rate_of_change:poly` | 2 |
| `average_rate_of_change:reciprocal` | 1 |
| `definition_of_derivative:limit_h` | 1 |
| `definition_of_derivative:poly` | 1 |
| `derivative_higher_order:eval` | 1 |
| `derivative_higher_order:exp` | 1 |
| `derivative_higher_order:exp_k` | 1 |
| `derivative_implicit:cubes` | 1 |
| `derivative_inverse_functions:ln` | 1 |
| `derivative_inverse_functions:power_med` | 1 |
| `derivative_inverse_functions:table` | 1 |
| `derivative_inverse_trig:chain+power` | 1 |
| `derivative_ln_exp:chain` | 1 |
| `derivative_ln_exp:chain+power` | 1 |
| `derivative_logarithmic:product_powers` | 1 |
| `derivative_other_base:change_order` | 1 |
| `instantaneous_rate_of_change:reciprocal` | 1 |
| `instantaneous_rate_of_change:sqrt` | 1 |
| `instantaneous_rate_of_change:trig` | 1 |

## c1: Average rates of change

`calc_diff_average_rates_of_change`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **5** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `average_rate_of_change:linear` | 4 |
| `average_rate_of_change:quad` | 3 |
| `average_rate_of_change:poly` | 2 |
| `average_rate_of_change:quad_const` | 2 |
| `average_rate_of_change:reciprocal` | 1 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[3,4].$ | $7$ | `average_rate_of_change:quad · band=easy` |
| 0 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[2,4].$ | $6$ | `average_rate_of_change:quad · band=easy` |
| 5 | $\text{Find the average rate of change of }f(x)=3x - 3\text{ on }[2,4].$ | $3$ | `average_rate_of_change:linear · band=medium` |
| 5 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,4].$ | $5$ | `average_rate_of_change:quad · band=medium` |
| 10 | $\text{Find the average rate of change of }f(x)=-4x - 2\text{ on }[0,1].$ | $-4$ | `average_rate_of_change:linear · band=hard` |
| 10 | $\text{Find the average rate of change of }f(x)=3x^{2} - 3\text{ on }[2,6].$ | $24$ | `average_rate_of_change:quad_const · band=hard` |
| 15 | $\text{Find the average rate of change of }f(x)=-4x\text{ on }[0,2].$ | $-4$ | `average_rate_of_change:linear · band=hard` |
| 15 | $\text{Find the average rate of change of }f(x)=\frac{1}{x}\text{ on }[2,4].$ | $-\frac{1}{8}$ | `average_rate_of_change:reciprocal · band=hard` |
| 20 | $\text{Find the average rate of change of }f(x)=2x^{2} - 3x - 1\text{ on }[1,5].$ | $9$ | `average_rate_of_change:poly · band=hard` |
| 20 | $\text{Find the average rate of change of }f(x)=2x^{2} + 4\text{ on }[3,8].$ | $22$ | `average_rate_of_change:quad_const · band=hard` |
| 25 | $\text{Find the average rate of change of }f(x)=x^{2} - 3x + 1\text{ on }[2,4].$ | $3$ | `average_rate_of_change:poly · band=hard` |
| 25 | $\text{Find the average rate of change of }f(x)=-3x - 2\text{ on }[0,4].$ | $-3$ | `average_rate_of_change:linear · band=hard` |

## c1: Chain Rule

`calc_diff_chain_rule`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `derivative_chain_rule:chain` | 6 |
| `derivative_chain_rule:chain+power` | 6 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\text{Find }\frac{d}{dx}\left(\left(2x - 3\right)^{4}\right)$ | $4\left(2x - 3\right)^{3}\left(2\right)$ | `derivative_chain_rule:chain+power · classes=algebraic; ups=use_chain; chain=1` |
| 0 | $\text{Find }\frac{d}{dx}\left(\left(x + 3\right)^{2}\right)$ | $2\left(x + 3\right)$ | `derivative_chain_rule:chain+power · classes=algebraic; ups=use_chain; chain=1` |
| 5 | $\frac{d}{dx}\left[\sqrt{x + 3}\right]$ | $\frac{1}{2\sqrt{x + 3}}$ | `derivative_chain_rule:chain · classes=algebraic,roots; ups=extra_term,higher_power,use_chain; chain=1` |
| 5 | $\frac{d}{dx}\left[\left(x^{2} + 2\right)^{3}\right]$ | $3\left(x^{2} + 2\right)^{2}\left(2x\right)$ | `derivative_chain_rule:chain+power · classes=algebraic; ups=extra_term,higher_power,use_chain; chain=1` |
| 10 | $\frac{d}{dx}\left[\sqrt{4x + 2}\right]$ | $\frac{4}{2\sqrt{4x + 2}}$ | `derivative_chain_rule:chain · classes=algebraic,roots; ups=extra_term,higher_power,mix_classes,use_chain,use_product; chain=1` |
| 10 | $\frac{d}{dx}\left[\sqrt{4x + 5}\right]$ | $\frac{4}{2\sqrt{4x + 5}}$ | `derivative_chain_rule:chain · classes=algebraic,roots; ups=extra_term,higher_power,mix_classes,use_chain,use_product; chain=1` |
| 15 | $\text{Find }\frac{d}{dx}\left(\sqrt{4x}\right)$ | $\frac{4}{2\sqrt{4x}}$ | `derivative_chain_rule:chain · classes=algebraic,roots; ups=chain_depth_2,class_roots,extra_term,higher_power,use_chain; chain=1` |
| 15 | $\frac{d}{dx}\left[\left(\left(x^{2} + 3\right)^{2}\right)^{2}\right]$ | $2\left(\left(x^{2} + 3\right)^{2}\right)\left(2\left(x^{2} + 3\right)\left(2x\right)\right)$ | `derivative_chain_rule:chain+power · classes=algebraic; ups=chain_depth_2,class_roots,extra_term,higher_power,use_chain; chain=2` |
| 20 | $\frac{d}{dx}\left[\left(\left(2x^{2} - 3\right)^{4}\right)^{3}\right]$ | $3\left(\left(2x^{2} - 3\right)^{4}\right)^{2}\left(4\left(2x^{2} - 3\right)^{3}\left(4x\right)\right)$ | `derivative_chain_rule:chain+power · classes=algebraic; ups=chain_depth_2,class_roots,extra_term,higher_power,mix_classes; chain=2` |
| 20 | $\frac{d}{dx}\left[\sqrt{4x + 7}\right]$ | $\frac{4}{2\sqrt{4x + 7}}$ | `derivative_chain_rule:chain · classes=algebraic,roots; ups=chain_depth_2,class_roots,extra_term,higher_power,mix_classes; chain=1` |
| 25 | $\text{Find }\frac{d}{dx}\left(\left(\left(3x^{2} + 8\right)^{3}\right)^{2}\right)$ | $2\left(\left(3x^{2} + 8\right)^{3}\right)\left(3\left(3x^{2} + 8\right)^{2}\left(6x\right)\right)$ | `derivative_chain_rule:chain+power · classes=algebraic; ups=chain_depth_2,class_roots,extra_term,higher_power,mix_classes; chain=2` |
| 25 | $\frac{d}{dx}\left[\sqrt{9x + 2}\right]$ | $\frac{9}{2\sqrt{9x + 2}}$ | `derivative_chain_rule:chain · classes=algebraic,roots; ups=chain_depth_2,class_roots,extra_term,higher_power,mix_classes; chain=1` |

## c1: Definition of the derivative

`calc_diff_definition_of_the_derivative`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **6** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `definition_of_derivative:limit_x` | 3 |
| `definition_of_derivative:linear_coef` | 3 |
| `definition_of_derivative:cube` | 2 |
| `definition_of_derivative:named` | 2 |
| `definition_of_derivative:limit_h` | 1 |
| `definition_of_derivative:poly` | 1 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\lim_{x\to 2}\frac{x^{2}-4}{x-2}$ | $4$ | `definition_of_derivative:limit_x · band=easy` |
| 0 | $\lim_{x\to 1}\frac{x^{2}-1}{x-1}$ | $2$ | `definition_of_derivative:limit_x · band=easy` |
| 5 | $\lim_{h\to 0}\frac{2(2+h)^{2}-8}{h}$ | $8$ | `definition_of_derivative:linear_coef · band=medium` |
| 5 | $\text{Use the definition to find }f'(1)\text{ for }f(x)=3x^{2}.$ | $6$ | `definition_of_derivative:named · band=medium` |
| 10 | $\text{Use the definition to find }f'(5)\text{ for }f(x)=1 + x^{2}.$ | $10$ | `definition_of_derivative:poly · band=hard` |
| 10 | $\text{Use the definition to find }f'(1)\text{ for }f(x)=4x^{2}.$ | $8$ | `definition_of_derivative:named · band=hard` |
| 15 | $\lim_{h\to 0}\frac{(1+h)^{2}-1}{h}$ | $2$ | `definition_of_derivative:limit_h · band=hard` |
| 15 | $\lim_{h\to 0}\frac{(5+h)^{3}-125}{h}$ | $75$ | `definition_of_derivative:cube · band=hard` |
| 20 | $\lim_{h\to 0}\frac{4(3+h)^{2}-36}{h}$ | $24$ | `definition_of_derivative:linear_coef · band=hard` |
| 20 | $\lim_{h\to 0}\frac{(2+h)^{3}-8}{h}$ | $12$ | `definition_of_derivative:cube · band=hard` |
| 25 | $\lim_{h\to 0}\frac{3(1+h)^{2}-3}{h}$ | $6$ | `definition_of_derivative:linear_coef · band=hard` |
| 25 | $\lim_{x\to 3}\frac{x^{2}-9}{x-3}$ | $6$ | `definition_of_derivative:limit_x · band=hard` |

## c1: Higher order derivatives

`calc_diff_higher_order_derivatives`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **5** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `derivative_higher_order:poly3_second` | 5 |
| `derivative_higher_order:poly4_third` | 4 |
| `derivative_higher_order:eval` | 1 |
| `derivative_higher_order:exp` | 1 |
| `derivative_higher_order:exp_k` | 1 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\text{Find }f''(x)\text{ for }f(x)=2x^{3} + x^{2} - 3x - 3.$ | $12x + 2$ | `derivative_higher_order:poly3_second · band=easy` |
| 0 | $\text{Find }f''(x)\text{ for }f(x)=x^{3} + 2x^{2} - 3x.$ | $6x + 4$ | `derivative_higher_order:poly3_second · band=easy` |
| 5 | $\text{Find }f''(x)\text{ for }f(x)=-4 + 2x + 5x^{2} + 2x^{3}.$ | $12x + 10$ | `derivative_higher_order:poly3_second · band=medium` |
| 5 | $\text{Find }f''(x)\text{ for }f(x)=x^{3} + 3x^{2} + 5x - 1.$ | $6x + 6$ | `derivative_higher_order:poly3_second · band=medium` |
| 10 | $\text{Find }f'''(x)\text{ for }f(x)=4x^{4} + x^{3} + 4x^{2} - 2x + 1.$ | $96x + 6$ | `derivative_higher_order:poly4_third · band=hard` |
| 10 | $\text{Find }f'''(x)\text{ for }f(x)=x^{4} + x^{3} + 3x^{2} + 3x + 1.$ | $24x + 6$ | `derivative_higher_order:poly4_third · band=hard` |
| 15 | $\text{Find }\frac{d^{2}}{dx^{2}}e^{2x}.$ | $4e^{2x}$ | `derivative_higher_order:exp_k · band=hard` |
| 15 | $\text{Find }f'''(x)\text{ for }f(x)=3x^{4} - 4x^{3} + 6x^{2} + 4x - 1.$ | $72x - 24$ | `derivative_higher_order:poly4_third · band=hard` |
| 20 | $\text{Find }\frac{d^{2}}{dx^{2}}e^{x}.$ | $e^{x}$ | `derivative_higher_order:exp · band=hard` |
| 20 | $\text{Find }f''(x)\text{ for }f(x)=3x^{3} - 6x^{2} - 4x + 2.$ | $18x - 12$ | `derivative_higher_order:poly3_second · band=hard` |
| 25 | $\text{Find }f''(2)\text{ for }f(x)=4x^{3} - x^{2} + 3x - 4.$ | $46$ | `derivative_higher_order:eval · band=hard` |
| 25 | $\text{Find }f'''(x)\text{ for }f(x)=-7 - 3x + x^{2} - 2x^{3} + 4x^{4}.$ | $96x - 12$ | `derivative_higher_order:poly4_third · band=hard` |

## c1: Implicit

`calc_diff_implicit`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **5** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `derivative_implicit:trig` | 4 |
| `derivative_implicit:circle` | 3 |
| `derivative_implicit:ellipse` | 2 |
| `derivative_implicit:line_prod` | 2 |
| `derivative_implicit:cubes` | 1 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\text{Differentiate implicitly: }x^{2}+y^{2}=3.\text{ Solve for }\frac{dy}{dx}.$ | $\frac{dy}{dx}=-\frac{x}{y}$ | `derivative_implicit:circle · band=easy` |
| 0 | $\text{Differentiate implicitly: }x^{2}+y^{2}=2.\text{ Solve for }\frac{dy}{dx}.$ | $\frac{dy}{dx}=-\frac{x}{y}$ | `derivative_implicit:circle · band=easy` |
| 5 | $\text{Differentiate implicitly: }x^{2}+y^{2}=3.\text{ Solve for }\frac{dy}{dx}.$ | $\frac{dy}{dx}=-\frac{x}{y}$ | `derivative_implicit:circle · band=medium` |
| 5 | $\text{Differentiate implicitly: }xy=3.\text{ Solve for }\frac{dy}{dx}.$ | $\frac{dy}{dx}=-\frac{y}{x}$ | `derivative_implicit:line_prod · band=medium` |
| 10 | $\text{Differentiate implicitly: }x^{3}+y^{3}=3.\text{ Solve for }\frac{dy}{dx}.$ | $\frac{dy}{dx}=-\frac{x^{2}}{y^{2}}$ | `derivative_implicit:cubes · band=hard` |
| 10 | $\text{Differentiate implicitly: }\sin(x)+\cos(y)=0.\text{ Solve for }\frac{dy}{dx}.$ | $\frac{dy}{dx}=\frac{\cos(x)}{\sin(y)}$ | `derivative_implicit:trig · band=hard` |
| 15 | $\text{Differentiate implicitly: }xy=4.\text{ Solve for }\frac{dy}{dx}.$ | $\frac{dy}{dx}=-\frac{y}{x}$ | `derivative_implicit:line_prod · band=hard` |
| 15 | $\text{Differentiate implicitly: }\sin(x)+\cos(y)=0.\text{ Solve for }\frac{dy}{dx}.$ | $\frac{dy}{dx}=\frac{\cos(x)}{\sin(y)}$ | `derivative_implicit:trig · band=hard` |
| 20 | $\text{Differentiate implicitly: }\sin(x)+\cos(y)=0.\text{ Solve for }\frac{dy}{dx}.$ | $\frac{dy}{dx}=\frac{\cos(x)}{\sin(y)}$ | `derivative_implicit:trig · band=hard` |
| 20 | $\text{Differentiate implicitly: }5x^{2}+y^{2}=1.\text{ Solve for }\frac{dy}{dx}.$ | $\frac{dy}{dx}=-\frac{10x}{y}$ | `derivative_implicit:ellipse · band=hard` |
| 25 | $\text{Differentiate implicitly: }\sin(x)+\cos(y)=0.\text{ Solve for }\frac{dy}{dx}.$ | $\frac{dy}{dx}=\frac{\cos(x)}{\sin(y)}$ | `derivative_implicit:trig · band=hard` |
| 25 | $\text{Differentiate implicitly: }3x^{2}+y^{2}=2.\text{ Solve for }\frac{dy}{dx}.$ | $\frac{dy}{dx}=-\frac{6x}{y}$ | `derivative_implicit:ellipse · band=hard` |

## c1: Instantaneous rates of change

`calc_diff_instantaneous_rates_of_change`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **7** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `instantaneous_rate_of_change:power` | 3 |
| `instantaneous_rate_of_change:cubic` | 2 |
| `instantaneous_rate_of_change:exp` | 2 |
| `instantaneous_rate_of_change:poly` | 2 |
| `instantaneous_rate_of_change:reciprocal` | 1 |
| `instantaneous_rate_of_change:sqrt` | 1 |
| `instantaneous_rate_of_change:trig` | 1 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\text{Find the instantaneous rate of change of }f(x)=x^{2}\text{ at }x=1.$ | $2$ | `instantaneous_rate_of_change:power · band=easy` |
| 0 | $\text{Find the instantaneous rate of change of }f(x)=x^{2}\text{ at }x=2.$ | $4$ | `instantaneous_rate_of_change:power · band=easy` |
| 5 | $\text{Find the instantaneous rate of change of }f(x)=x^{2} - 1\text{ at }x=1.$ | $2$ | `instantaneous_rate_of_change:poly · band=medium` |
| 5 | $\text{Find the instantaneous rate of change of }f(x)=-1 + 2x^{2}\text{ at }x=1.$ | $4$ | `instantaneous_rate_of_change:poly · band=medium` |
| 10 | $\text{Find the instantaneous rate of change of }f(x)=-x + 2x^{3}\text{ at }x=2.$ | $23$ | `instantaneous_rate_of_change:cubic · band=hard` |
| 10 | $\text{Find the instantaneous rate of change of }f(x)=e^{3x}\text{ at }x=0.$ | $3$ | `instantaneous_rate_of_change:exp · band=hard` |
| 15 | $\text{Find the instantaneous rate of change of }f(x)=\cos(x)\text{ at }x=0.$ | $0$ | `instantaneous_rate_of_change:trig · band=hard` |
| 15 | $\text{Find the instantaneous rate of change of }f(x)=x^{3} - x\text{ at }x=4.$ | $47$ | `instantaneous_rate_of_change:cubic · band=hard` |
| 20 | $\text{Find the instantaneous rate of change of }f(x)=e^{3x}\text{ at }x=0.$ | $3$ | `instantaneous_rate_of_change:exp · band=hard` |
| 20 | $\text{Find the instantaneous rate of change of }f(x)=x^{1/2}\text{ at }x=1.$ | $\frac{1}{2}$ | `instantaneous_rate_of_change:sqrt · band=hard` |
| 25 | $\text{Find the instantaneous rate of change of }f(x)=x^{-1}\text{ at }x=3.$ | $-\frac{1}{9}$ | `instantaneous_rate_of_change:reciprocal · band=hard` |
| 25 | $\text{Find the instantaneous rate of change of }f(x)=x^{4}\text{ at }x=4.$ | $256$ | `instantaneous_rate_of_change:power · band=hard` |

## c1: Inverse functions

`calc_diff_inverse_functions`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **7** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `derivative_inverse_functions:linear` | 3 |
| `derivative_inverse_functions:cubic` | 2 |
| `derivative_inverse_functions:exp` | 2 |
| `derivative_inverse_functions:power` | 2 |
| `derivative_inverse_functions:ln` | 1 |
| `derivative_inverse_functions:power_med` | 1 |
| `derivative_inverse_functions:table` | 1 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $f(x)=x^{2};\quad f'(2)=4.\quad\text{Find }(f^{-1})'(4).$ | $\frac{1}{4}$ | `derivative_inverse_functions:power · band=easy` |
| 0 | $f(x)=x^{2};\quad f'(2)=4.\quad\text{Find }(f^{-1})'(4).$ | $\frac{1}{4}$ | `derivative_inverse_functions:power · band=easy` |
| 5 | $f(x)=2x - 3.\quad\text{Find }(f^{-1})'(x).$ | $\frac{1}{2}$ | `derivative_inverse_functions:linear · band=medium` |
| 5 | $f(x)=2x - 3.\quad\text{Find }(f^{-1})'(x).$ | $\frac{1}{2}$ | `derivative_inverse_functions:linear · band=medium` |
| 10 | $f(2)=2,\ f'(2)=6.\quad\text{Find }(f^{-1})'(2).$ | $\frac{1}{6}$ | `derivative_inverse_functions:table · band=hard` |
| 10 | $f(x)=e^{x};\quad f(0)=1,\ f'(0)=1.\quad\text{Find }(f^{-1})'(1).$ | $1$ | `derivative_inverse_functions:exp · band=hard` |
| 15 | $f(x)=\ln(x);\quad f(e)=1,\ f'(e)=\frac{1}{e}.\quad\text{Find }(f^{-1})'(1).$ | $e$ | `derivative_inverse_functions:ln · band=hard` |
| 15 | $f(x)=3x + 2.\quad\text{Find }(f^{-1})'(x).$ | $\frac{1}{3}$ | `derivative_inverse_functions:linear · band=hard` |
| 20 | $f(x)=x^{3}+x;\quad f'(2)=13.\quad\text{Find }(f^{-1})'(10).$ | $\frac{1}{13}$ | `derivative_inverse_functions:cubic · band=hard` |
| 20 | $f(x)=e^{x};\quad f(0)=1,\ f'(0)=1.\quad\text{Find }(f^{-1})'(1).$ | $1$ | `derivative_inverse_functions:exp · band=hard` |
| 25 | $f(x)=x^{3}+x;\quad f'(2)=13.\quad\text{Find }(f^{-1})'(10).$ | $\frac{1}{13}$ | `derivative_inverse_functions:cubic · band=hard` |
| 25 | $f(x)=x^{3};\quad f'(2)=12.\quad\text{Find }(f^{-1})'(8).$ | $\frac{1}{12}$ | `derivative_inverse_functions:power_med · band=hard` |

## c1: Inverse trigonometric

`calc_diff_inverse_trigonometric`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **3** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `derivative_inverse_trig:chain` | 9 |
| `derivative_inverse_trig:power` | 2 |
| `derivative_inverse_trig:chain+power` | 1 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\frac{d}{dx}\left[\arctan(x)\right]$ | $\frac{1}{1+x^{2}}$ | `derivative_inverse_trig:power · classes=invtrig; band=easy` |
| 0 | $\text{Find }\frac{d}{dx}\left(\arctan(x)\right)$ | $\frac{1}{1+x^{2}}$ | `derivative_inverse_trig:power · classes=invtrig; band=easy` |
| 5 | $\text{Find }\frac{d}{dx}\left(\arccos(2x)\right)$ | $-\frac{2}{\sqrt{1-(2x)^{2}}}$ | `derivative_inverse_trig:chain · classes=algebraic,invtrig; ups=extra_term,higher_power,use_chain; chain=1` |
| 5 | $\frac{d}{dx}\left[\arctan(5x)\right]$ | $\frac{5}{1+(5x)^{2}}$ | `derivative_inverse_trig:chain · classes=algebraic,invtrig; ups=extra_term,higher_power,use_chain; chain=1` |
| 10 | $\frac{d}{dx}\left[\arccos(2x)\right]$ | $-\frac{2}{\sqrt{1-(2x)^{2}}}$ | `derivative_inverse_trig:chain · classes=algebraic,invtrig; ups=chain_depth_2,extra_term,higher_power,use_chain; chain=1` |
| 10 | $\text{Find }\frac{d}{dx}\left(\arctan(2x)\right)$ | $\frac{2}{1+(2x)^{2}}$ | `derivative_inverse_trig:chain · classes=algebraic,invtrig; ups=chain_depth_2,extra_term,higher_power,use_chain; chain=1` |
| 15 | $\frac{d}{dx}\left[\arctan(3x)\right]$ | $\frac{3}{1+(3x)^{2}}$ | `derivative_inverse_trig:chain · classes=algebraic,invtrig; ups=chain_depth_2,class_invtrig,extra_term,higher_power,use_chain; chain=1` |
| 15 | $\frac{d}{dx}\left[\left(\left(x^{2} + 3\right)^{4}\right)^{3}\right]$ | $3\left(\left(x^{2} + 3\right)^{4}\right)^{2}\left(4\left(x^{2} + 3\right)^{3}\left(2x\right)\right)$ | `derivative_inverse_trig:chain+power · classes=algebraic; ups=chain_depth_2,class_invtrig,extra_term,higher_power,use_chain; chain=2` |
| 20 | $\text{Find }\frac{d}{dx}\left(\arcsin(5x)\right)$ | $\frac{5}{\sqrt{1-(5x)^{2}}}$ | `derivative_inverse_trig:chain · classes=algebraic,invtrig; ups=chain_depth_2,class_invtrig,extra_term,higher_power,mix_classes; chain=1` |
| 20 | $\frac{d}{dx}\left[\arctan(3x)\right]$ | $\frac{3}{1+(3x)^{2}}$ | `derivative_inverse_trig:chain · classes=algebraic,invtrig; ups=chain_depth_2,class_invtrig,extra_term,higher_power,mix_classes; chain=1` |
| 25 | $\frac{d}{dx}\left[\arctan(2x)\right]$ | $\frac{2}{1+(2x)^{2}}$ | `derivative_inverse_trig:chain · classes=algebraic,invtrig; ups=chain_depth_2,class_invtrig,extra_term,higher_power,mix_classes; chain=1` |
| 25 | $\frac{d}{dx}\left[\arctan(5x)\right]$ | $\frac{5}{1+(5x)^{2}}$ | `derivative_inverse_trig:chain · classes=algebraic,invtrig; ups=chain_depth_2,class_invtrig,extra_term,higher_power,mix_classes; chain=1` |

## c1: Logarithmic

`calc_diff_logarithmic`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **3** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `derivative_logarithmic:power` | 7 |
| `derivative_logarithmic:root` | 4 |
| `derivative_logarithmic:product_powers` | 1 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\text{Use logarithmic differentiation to find }\frac{d}{dx}\left[x^{3}\right].$ | $3x^{2}$ | `derivative_logarithmic:power · band=easy` |
| 0 | $\text{Use logarithmic differentiation to find }\frac{d}{dx}\left[x^{3}\right].$ | $3x^{2}$ | `derivative_logarithmic:power · band=easy` |
| 5 | $\text{Use logarithmic differentiation to find }\frac{d}{dx}\left[x^{4}\right].$ | $4x^{3}$ | `derivative_logarithmic:power · band=medium` |
| 5 | $\text{Use logarithmic differentiation to find }\frac{d}{dx}\left[x^{4}\right].$ | $4x^{3}$ | `derivative_logarithmic:power · band=medium` |
| 10 | $\text{Use logarithmic differentiation: }y=\sqrt{x(x+1)}.\ \text{Find }y'.$ | $\sqrt{x(x+1)}\cdot\frac{1}{2}\left(\frac{1}{x}+\frac{1}{x+1}\right)$ | `derivative_logarithmic:root · band=hard` |
| 10 | $\text{Use logarithmic differentiation: }y=\sqrt{x(x+1)}.\ \text{Find }y'.$ | $\sqrt{x(x+1)}\cdot\frac{1}{2}\left(\frac{1}{x}+\frac{1}{x+1}\right)$ | `derivative_logarithmic:root · band=hard` |
| 15 | $\text{Use logarithmic differentiation to find }\frac{d}{dx}\left[x^{4}\right].$ | $4x^{3}$ | `derivative_logarithmic:power · band=hard` |
| 15 | $\text{Use logarithmic differentiation: }y=x^{4}(x+1)^{4}.\ \text{Find }y'.$ | $x^{4}(x+1)^{4}\left(\frac{4}{x}+\frac{4}{x+1}\right)$ | `derivative_logarithmic:product_powers · band=hard` |
| 20 | $\text{Use logarithmic differentiation: }y=\sqrt{x(x+1)}.\ \text{Find }y'.$ | $\sqrt{x(x+1)}\cdot\frac{1}{2}\left(\frac{1}{x}+\frac{1}{x+1}\right)$ | `derivative_logarithmic:root · band=hard` |
| 20 | $\text{Use logarithmic differentiation: }y=\sqrt{x(x+1)}.\ \text{Find }y'.$ | $\sqrt{x(x+1)}\cdot\frac{1}{2}\left(\frac{1}{x}+\frac{1}{x+1}\right)$ | `derivative_logarithmic:root · band=hard` |
| 25 | $\text{Use logarithmic differentiation to find }\frac{d}{dx}\left[x^{5}\right].$ | $5x^{4}$ | `derivative_logarithmic:power · band=hard` |
| 25 | $\text{Use logarithmic differentiation to find }\frac{d}{dx}\left[x^{4}\right].$ | $4x^{3}$ | `derivative_logarithmic:power · band=hard` |

## c1: Natural logarithms and exponentials

`calc_diff_natural_logarithms_and_exponentials`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **6** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `derivative_ln_exp:chain+power+product` | 3 |
| `derivative_ln_exp:power+product` | 3 |
| `derivative_ln_exp:chain+power+product+sum` | 2 |
| `derivative_ln_exp:power` | 2 |
| `derivative_ln_exp:chain` | 1 |
| `derivative_ln_exp:chain+power` | 1 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\text{Find }\frac{d}{dx}\left(e^{x}\right)$ | $e^{x}$ | `derivative_ln_exp:power · band=easy` |
| 0 | $\text{Find }\frac{d}{dx}\left(e^{x}\right)$ | $e^{x}$ | `derivative_ln_exp:power · band=easy` |
| 5 | $\frac{d}{dx}\left[\left(3x^{2} - 2\right)^{3}\right]$ | $3\left(3x^{2} - 2\right)^{2}\left(6x\right)$ | `derivative_ln_exp:chain+power · classes=algebraic; ups=extra_term,higher_power,use_chain; chain=1` |
| 5 | $\text{Find }\frac{d}{dx}\left(\ln\left\|2x + 3\right\|\right)$ | $\frac{2}{2x + 3}$ | `derivative_ln_exp:chain · classes=algebraic,log; ups=extra_term,higher_power,use_chain; chain=1` |
| 10 | $\frac{d}{dx}\left[\left(\ln\left\|4x + 2\right\|\right)\left(-3x^{5}\right)\right]$ | $\left(\frac{4}{4x + 2}\right)\left(-3x^{5}\right)+\left(\ln\left\|4x + 2\right\|\right)\left(-15x^{4}\right)$ | `derivative_ln_exp:chain+power+product · classes=algebraic,log; ups=extra_term,higher_power,mix_classes,use_chain,use_product; chain=1` |
| 10 | $\text{Find }\frac{d}{dx}\left(\left(e^{x}\right)\left(2x^{5}\right)\right)$ | $\left(e^{x}\right)\left(2x^{5}\right)+\left(e^{x}\right)\left(10x^{4}\right)$ | `derivative_ln_exp:power+product · classes=algebraic,exp; ups=extra_term,higher_power,mix_classes,use_chain,use_product; band=hard` |
| 15 | $\text{Find }\frac{d}{dx}\left(\left(4x^{5}\right)\left(\ln\left\|3x + 3\right\|\right)\right)$ | $\left(20x^{4}\right)\left(\ln\left\|3x + 3\right\|\right)+\left(4x^{5}\right)\left(\frac{3}{3x + 3}\right)$ | `derivative_ln_exp:chain+power+product · classes=algebraic,log; ups=chain_depth_2,extra_term,higher_power,mix_classes,use_chain; chain=1` |
| 15 | $\text{Find }\frac{d}{dx}\left(\left(\ln(x)\right)\left(5x^{5}\right)\right)$ | $\left(\frac{1}{x}\right)\left(5x^{5}\right)+\left(\ln(x)\right)\left(25x^{4}\right)$ | `derivative_ln_exp:power+product · classes=algebraic,log; ups=chain_depth_2,extra_term,higher_power,mix_classes,use_chain; band=hard` |
| 20 | $\frac{d}{dx}\left[\left(3x^{3} - 5x^{2} + 7x - 1\right)\left(\ln\left\|4x + 4\right\|\right)\right]$ | $\left(9x^{2} - 10x + 7\right)\left(\ln\left\|4x + 4\right\|\right)+\left(3x^{3} - 5x^{2} + 7x - 1\right)\left(\frac{4}{4x + 4}\right)$ | `derivative_ln_exp:chain+power+product+sum · classes=algebraic,log; ups=chain_depth_2,class_exp,class_log,extra_term,higher_power; chain=1` |
| 20 | $\frac{d}{dx}\left[\left(\ln\left\|5x + 6\right\|\right)\left(2x^{3} - 4x^{2} + 3x + 6\right)\right]$ | $\left(\frac{5}{5x + 6}\right)\left(2x^{3} - 4x^{2} + 3x + 6\right)+\left(\ln\left\|5x + 6\right\|\right)\left(6x^{2} - 8x + 3\right)$ | `derivative_ln_exp:chain+power+product+sum · classes=algebraic,log; ups=chain_depth_2,class_exp,class_log,extra_term,higher_power; chain=1` |
| 25 | $\text{Find }\frac{d}{dx}\left(\left(-7x^{2}\right)\left(\ln(x)\right)\right)$ | $\left(-14x\right)\left(\ln(x)\right)+\left(-7x^{2}\right)\left(\frac{1}{x}\right)$ | `derivative_ln_exp:power+product · classes=algebraic,log; ups=chain_depth_2,class_exp,class_log,extra_term,higher_power; band=hard` |
| 25 | $\frac{d}{dx}\left[\left(-x^{2}\right)\left(e^{x + 3}\right)\right]$ | $\left(-2x\right)\left(e^{x + 3}\right)+\left(-x^{2}\right)\left(1e^{x + 3}\right)$ | `derivative_ln_exp:chain+power+product · classes=algebraic,exp; ups=chain_depth_2,class_exp,class_log,extra_term,higher_power; chain=1` |

## c1: Other base logarithms and exponentials

`calc_diff_other_base_logarithms_and_exponentials`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **6** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `derivative_other_base:log_x` | 3 |
| `derivative_other_base:a_kx` | 2 |
| `derivative_other_base:a_x` | 2 |
| `derivative_other_base:log_linear` | 2 |
| `derivative_other_base:log_power` | 2 |
| `derivative_other_base:change_order` | 1 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\frac{d}{dx}\log_{2}(x)$ | $\frac{1}{x\ln(2)}$ | `derivative_other_base:log_x · band=easy` |
| 0 | $\frac{d}{dx}\left[3^{x}\right]$ | $3^{x}\ln(3)$ | `derivative_other_base:a_x · band=easy` |
| 5 | $\frac{d}{dx}\log_{3}(x)$ | $\frac{1}{x\ln(3)}$ | `derivative_other_base:log_x · band=medium` |
| 5 | $\frac{d}{dx}\log_{2}(x - 1)$ | $\frac{1}{x - 1\ln(2)}$ | `derivative_other_base:log_linear · band=medium` |
| 10 | $\frac{d}{dx}\left[3^{x}\right]$ | $3^{x}\ln(3)$ | `derivative_other_base:a_x · band=hard` |
| 10 | $\frac{d}{dx}4^{4x}$ | $44^{4x}\ln(4)$ | `derivative_other_base:a_kx · band=hard` |
| 15 | $\frac{d}{dx}\left[3\log_{2}(x)\right]$ | $\frac{3}{x\ln(2)}$ | `derivative_other_base:log_power · band=hard` |
| 15 | $\frac{d}{dx}\log_{3}(x)$ | $\frac{1}{x\ln(3)}$ | `derivative_other_base:log_x · band=hard` |
| 20 | $\frac{d}{dx}\left[x\cdot 5^{x}\right]$ | $5^{x}+x5^{x}\ln(5)$ | `derivative_other_base:change_order · band=hard` |
| 20 | $\frac{d}{dx}2^{2x}$ | $22^{2x}\ln(2)$ | `derivative_other_base:a_kx · band=hard` |
| 25 | $\frac{d}{dx}\left[\log_{3}(x^{3})\right]$ | $\frac{3}{x\ln(3)}$ | `derivative_other_base:log_power · band=hard` |
| 25 | $\frac{d}{dx}\log_{3}(x + 2)$ | $\frac{1}{x + 2\ln(3)}$ | `derivative_other_base:log_linear · band=hard` |

## c1: Power Rule

`calc_diff_power_rule`

### Structures in this type

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

## c1: Product Rule

`calc_diff_product_rule`

### Structures in this type

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

## c1: Quotient Rule

`calc_diff_quotient_rule`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `derivative_quotient_rule:power+quotient+sum` | 10 |
| `derivative_quotient_rule:power+quotient` | 2 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\frac{d}{dx}\left[\frac{-3x^{2}}{2x - 3}\right]$ | $\frac{\left(-6x\right)\left(2x - 3\right)-\left(-3x^{2}\right)\left(2\right)}{\left(2x - 3\right)^{2}}$ | `derivative_quotient_rule:power+quotient · classes=algebraic; ups=use_quotient; band=easy` |
| 0 | $\frac{d}{dx}\left[\frac{2x^{3}}{3x - 1}\right]$ | $\frac{\left(6x^{2}\right)\left(3x - 1\right)-\left(2x^{3}\right)\left(3\right)}{\left(3x - 1\right)^{2}}$ | `derivative_quotient_rule:power+quotient · classes=algebraic; ups=use_quotient; band=easy` |
| 5 | $\text{Find }\frac{d}{dx}\left(\frac{x^{3} + x^{2} - 3x + 2}{4x - 2}\right)$ | $\frac{\left(3x^{2} + 2x - 3\right)\left(4x - 2\right)-\left(x^{3} + x^{2} - 3x + 2\right)\left(4\right)}{\left(4x - 2\right)^{2}}$ | `derivative_quotient_rule:power+quotient+sum · classes=algebraic; ups=extra_term,higher_power,use_chain,use_quotient; band=medium` |
| 5 | $\text{Find }\frac{d}{dx}\left(\frac{2x^{3} + 3x^{2} - 4x}{x + 5}\right)$ | $\frac{\left(6x^{2} + 6x - 4\right)\left(x + 5\right)-\left(2x^{3} + 3x^{2} - 4x\right)\left(1\right)}{\left(x + 5\right)^{2}}$ | `derivative_quotient_rule:power+quotient+sum · classes=algebraic; ups=extra_term,higher_power,use_chain,use_quotient; band=medium` |
| 10 | $\text{Find }\frac{d}{dx}\left(\frac{x^{3} - x^{2} + 1}{3x + 5}\right)$ | $\frac{\left(3x^{2} - 2x\right)\left(3x + 5\right)-\left(x^{3} - x^{2} + 1\right)\left(3\right)}{\left(3x + 5\right)^{2}}$ | `derivative_quotient_rule:power+quotient+sum · classes=algebraic; ups=extra_term,higher_power,use_chain,use_quotient; band=hard` |
| 10 | $\frac{d}{dx}\left[\frac{3x^{2} - x + 1}{5x + 5}\right]$ | $\frac{\left(6x - 1\right)\left(5x + 5\right)-\left(3x^{2} - x + 1\right)\left(5\right)}{\left(5x + 5\right)^{2}}$ | `derivative_quotient_rule:power+quotient+sum · classes=algebraic; ups=extra_term,higher_power,use_chain,use_quotient; band=hard` |
| 15 | $\text{Find }\frac{d}{dx}\left(\frac{x^{3} - 5x^{2} - 2x + 3}{5x + 5}\right)$ | $\frac{\left(3x^{2} - 10x - 2\right)\left(5x + 5\right)-\left(x^{3} - 5x^{2} - 2x + 3\right)\left(5\right)}{\left(5x + 5\right)^{2}}$ | `derivative_quotient_rule:power+quotient+sum · classes=algebraic; ups=chain_depth_2,extra_term,higher_power,use_chain,use_quotient; band=hard` |
| 15 | $\text{Find }\frac{d}{dx}\left(\frac{2x^{3} - 3x^{2} - x - 5}{2x - 2}\right)$ | $\frac{\left(6x^{2} - 6x - 1\right)\left(2x - 2\right)-\left(2x^{3} - 3x^{2} - x - 5\right)\left(2\right)}{\left(2x - 2\right)^{2}}$ | `derivative_quotient_rule:power+quotient+sum · classes=algebraic; ups=chain_depth_2,extra_term,higher_power,use_chain,use_quotient; band=hard` |
| 20 | $\text{Find }\frac{d}{dx}\left(\frac{2x^{2} + 6x + 1}{4x + 7}\right)$ | $\frac{\left(4x + 6\right)\left(4x + 7\right)-\left(2x^{2} + 6x + 1\right)\left(4\right)}{\left(4x + 7\right)^{2}}$ | `derivative_quotient_rule:power+quotient+sum · classes=algebraic; ups=chain_depth_2,extra_term,higher_power,use_chain,use_quotient; band=hard` |
| 20 | $\frac{d}{dx}\left[\frac{3x^{3} - 3x^{2} - 5x - 4}{2x - 2}\right]$ | $\frac{\left(9x^{2} - 6x - 5\right)\left(2x - 2\right)-\left(3x^{3} - 3x^{2} - 5x - 4\right)\left(2\right)}{\left(2x - 2\right)^{2}}$ | `derivative_quotient_rule:power+quotient+sum · classes=algebraic; ups=chain_depth_2,extra_term,higher_power,use_chain,use_quotient; band=hard` |
| 25 | $\frac{d}{dx}\left[\frac{3x^{2} - 3x - 8}{8x + 3}\right]$ | $\frac{\left(6x - 3\right)\left(8x + 3\right)-\left(3x^{2} - 3x - 8\right)\left(8\right)}{\left(8x + 3\right)^{2}}$ | `derivative_quotient_rule:power+quotient+sum · classes=algebraic; ups=chain_depth_2,extra_term,higher_power,use_chain,use_quotient; band=hard` |
| 25 | $\frac{d}{dx}\left[\frac{x^{3} + 5x^{2} + 7x + 7}{7x - 5}\right]$ | $\frac{\left(3x^{2} + 10x + 7\right)\left(7x - 5\right)-\left(x^{3} + 5x^{2} + 7x + 7\right)\left(7\right)}{\left(7x - 5\right)^{2}}$ | `derivative_quotient_rule:power+quotient+sum · classes=algebraic; ups=chain_depth_2,extra_term,higher_power,use_chain,use_quotient; band=hard` |

## c1: Trigonometric

`calc_diff_trigonometric`

### Structures in this type

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **5** · samples: **12**

| Structure / family | Count |
|--------|------:|
| `derivative_trigonometric:power+quotient+sum` | 4 |
| `derivative_trigonometric:chain` | 2 |
| `derivative_trigonometric:chain+power+quotient` | 2 |
| `derivative_trigonometric:power` | 2 |
| `derivative_trigonometric:power+quotient` | 2 |

| D | Prompt | Answer | Structure |
|--:|--------|--------|-----------|
| 0 | $\frac{d}{dx}\left[\tan(x)\right]$ | $\sec^{2}(x)$ | `derivative_trigonometric:power · band=easy` |
| 0 | $\frac{d}{dx}\left[\cos(x)\right]$ | $-\sin(x)$ | `derivative_trigonometric:power · band=easy` |
| 5 | $\text{Find }\frac{d}{dx}\left(\cos(3x)\right)$ | $-3\sin(3x)$ | `derivative_trigonometric:chain · classes=algebraic,trig; ups=extra_term,higher_power,use_chain; chain=1` |
| 5 | $\frac{d}{dx}\left[\tan(4x)\right]$ | $4\sec^{2}(4x)$ | `derivative_trigonometric:chain · classes=algebraic,trig; ups=extra_term,higher_power,use_chain; chain=1` |
| 10 | $\text{Find }\frac{d}{dx}\left(\frac{x^{3} + x^{2} - 2x + 3}{5x + 1}\right)$ | $\frac{\left(3x^{2} + 2x - 2\right)\left(5x + 1\right)-\left(x^{3} + x^{2} - 2x + 3\right)\left(5\right)}{\left(5x + 1\right)^{2}}$ | `derivative_trigonometric:power+quotient+sum · classes=algebraic; ups=extra_term,higher_power,use_product,use_quotient; band=hard` |
| 10 | $\frac{d}{dx}\left[\frac{\cos(x)}{3x - 4}\right]$ | $\frac{\left(-\sin(x)\right)\left(3x - 4\right)-\left(\cos(x)\right)\left(3\right)}{\left(3x - 4\right)^{2}}$ | `derivative_trigonometric:power+quotient · classes=algebraic,trig; ups=extra_term,higher_power,use_product,use_quotient; band=hard` |
| 15 | $\frac{d}{dx}\left[\frac{3x^{3} - 5x^{2} - 4x - 3}{3x - 4}\right]$ | $\frac{\left(9x^{2} - 10x - 4\right)\left(3x - 4\right)-\left(3x^{3} - 5x^{2} - 4x - 3\right)\left(3\right)}{\left(3x - 4\right)^{2}}$ | `derivative_trigonometric:power+quotient+sum · classes=algebraic; ups=class_trig,extra_term,higher_power,use_chain,use_product; band=hard` |
| 15 | $\frac{d}{dx}\left[\frac{2x^{3} + 5x^{2} - 2x - 5}{2x + 2}\right]$ | $\frac{\left(6x^{2} + 10x - 2\right)\left(2x + 2\right)-\left(2x^{3} + 5x^{2} - 2x - 5\right)\left(2\right)}{\left(2x + 2\right)^{2}}$ | `derivative_trigonometric:power+quotient+sum · classes=algebraic; ups=class_trig,extra_term,higher_power,use_chain,use_product; band=hard` |
| 20 | $\frac{d}{dx}\left[\frac{\cos(2x)}{3x + 2}\right]$ | $\frac{\left(-2\sin(2x)\right)\left(3x + 2\right)-\left(\cos(2x)\right)\left(3\right)}{\left(3x + 2\right)^{2}}$ | `derivative_trigonometric:chain+power+quotient · classes=algebraic,trig; ups=chain_depth_2,class_trig,extra_term,higher_power,use_chain; chain=1` |
| 20 | $\text{Find }\frac{d}{dx}\left(\frac{2x^{3} + 7x^{2} + 3x + 3}{2x + 3}\right)$ | $\frac{\left(6x^{2} + 14x + 3\right)\left(2x + 3\right)-\left(2x^{3} + 7x^{2} + 3x + 3\right)\left(2\right)}{\left(2x + 3\right)^{2}}$ | `derivative_trigonometric:power+quotient+sum · classes=algebraic; ups=chain_depth_2,class_trig,extra_term,higher_power,use_chain; band=hard` |
| 25 | $\text{Find }\frac{d}{dx}\left(\frac{\sin(4x)}{-x^{6}}\right)$ | $\frac{\left(4\cos(4x)\right)\left(-x^{6}\right)-\left(\sin(4x)\right)\left(-6x^{5}\right)}{\left(-x^{6}\right)^{2}}$ | `derivative_trigonometric:chain+power+quotient · classes=algebraic,trig; ups=chain_depth_2,class_trig,extra_term,higher_power,mix_classes; chain=1` |
| 25 | $\frac{d}{dx}\left[\frac{-4x^{4}}{\tan(x)}\right]$ | $\frac{\left(-16x^{3}\right)\left(\tan(x)\right)-\left(-4x^{4}\right)\left(\sec^{2}(x)\right)}{\left(\tan(x)\right)^{2}}$ | `derivative_trigonometric:power+quotient · classes=algebraic,trig; ups=chain_depth_2,class_trig,extra_term,higher_power,mix_classes; band=hard` |
