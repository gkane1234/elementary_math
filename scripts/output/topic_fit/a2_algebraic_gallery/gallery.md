# Algebra 2 algebraic gallery

Generated: 2026-08-03T16:45:03.689407+00:00

Live samples via `_generate_for_type` (D = 0, 3, 6, 8, 12, 16, 20, 25; 3 seeds each). No Easy/Medium/Hard labels — continuous **D=** only.

Open [gallery.html](gallery.html) in a browser for KaTeX (local `_assets/katex`).

- topics ok: **8** · skipped missing: **0**
- samples ok: **192** · errors: **0**
- metadata: `tricks_required`, `spec_snapshot` pack, form/shape when present

## Structure inventory

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **14** · samples: **192**

| Structure / family | Count |
|--------|------:|
| `exponential_equation_simple:exp_same_base` | 24 |
| `log_change_of_base:log_properties_condense` | 24 |
| `rational_expression_simplification:add_subtract_rationals` | 24 |
| `rational_simplification:simplify_rational` | 24 |
| `polynomial_factoring_sum_diff_cubes:difference_of_cubes` | 16 |
| `polynomial_multiply:distribute` | 16 |
| `polynomial_factoring_grouping:grouping_cubic` | 13 |
| `polynomial_factoring_grouping:grouping_quadratic` | 11 |
| `function_operations:add` | 9 |
| `function_operations:subtract` | 8 |
| `polynomial_factoring_sum_diff_cubes:sum_of_cubes` | 8 |
| `polynomial_multiply:foil` | 8 |
| `function_operations:product` | 4 |
| `function_operations:compose` | 3 |

## Topics

- [A2 rational expressions simplifying](#rational_simplify) — `a2_rational_expressions_simplifying`
- [A2 rational add/subtract (shared constructive core)](#rational_add) — `a2_rational_expressions_adding_and_subtracting`
- [A2 multiply polynomials (inherits A1 primitive)](#poly_multiply) — `a2_polynomial_functions_multiplying`
- [A2 factor by grouping](#poly_factor_grouping) — `a2_polynomial_functions_factoring_by_grouping`
- [A2 sum/difference of cubes](#sum_diff_cubes) — `a2_polynomial_functions_factoring_sum_difference_of_cubes`
- [A2 properties of logarithms](#log_props) — `a2_exponential_and_logarithmic_expressions_properties_of_logarithms`
- [A2 exponential equations (same base)](#exp_equation) — `a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms`
- [A2 function operations algebraic](#function_ops) — `a2_general_functions_operations`

## A2 rational expressions simplifying

<a id="rational_simplify"></a>

`a2_rational_expressions_simplifying` · pack `rational_simplify` · topic label: a2: Simplifying rational expressions · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **1** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `rational_simplification:simplify_rational` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Simplify: } \frac{3x^{2} - 12x + 9}{x^{2} - 3x + 2}$ | $\frac{3x - 9}{x - 2},\; x \neq 1$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=0` |
| 0 | $\text{Simplify: } \frac{3x^{2} - 6x}{x^{2} - 3x}$ | $\frac{3x - 6}{x - 3},\; x \neq 0$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=0` |
| 0 | $\text{Simplify: } \frac{-x^{2} - 2x + 3}{x^{2} - 9}$ | $\frac{-x + 1}{x - 3},\; x \neq -3$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=0` |
| 3 | $\text{Simplify: } \frac{-3x^{2} + 6x}{x^{2} - 3x}$ | $\frac{-3x + 6}{x - 3},\; x \neq 0$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=3` |
| 3 | $\text{Simplify: } \frac{3x^{2} - 6x - 24}{x^{2} - x - 6}$ | $\frac{3x - 12}{x - 3},\; x \neq -2$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=3` |
| 3 | $\text{Simplify: } \frac{x^{2} + 2x - 3}{x^{2} - 4x + 3}$ | $\frac{x + 3}{x - 3},\; x \neq 1$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=3` |
| 6 | $\text{Simplify: } \frac{2z^{2} - 6z}{z^{2} + 3z}$ | $\frac{2z - 6}{z + 3},\; z \neq 0$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=6` |
| 6 | $\text{Simplify: } \frac{x^{2} - 25}{x^{2} - 6x + 5}$ | $\frac{x + 5}{x - 1},\; x \neq 5$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=6` |
| 6 | $\text{Simplify: } \frac{3y^{2} - 12}{y^{2} - 5y + 6}$ | $\frac{3y + 6}{y - 3},\; y \neq 2$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=6` |
| 8 | $\text{Simplify: } \frac{3z^{2} - 18z + 24}{z^{2} + z - 6}$ | $\frac{3z - 12}{z + 3},\; z \neq 2$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=8` |
| 8 | $\text{Simplify: } \frac{4a^{2} - 16a + 12}{a^{2} - 7a + 12}$ | $\frac{4a - 4}{a - 4},\; a \neq 3$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=8` |
| 8 | $\text{Simplify: } \frac{-b^{2} + b + 2}{b^{2} + 3b + 2}$ | $\frac{-b + 2}{b + 2},\; b \neq -1$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=8` |
| 12 | $\text{Simplify: } \frac{-2\left(k - 1\right)\left(k - 4\right)\left(k - 2\right)\left(k + 5\right)}{\left(k\right)\left(k + 1\right)\left(k - 2\right)\left(k + 5\right)}$ | $\frac{-2k^{2} + 10k - 8}{k^{2} + k},\; k \neq -5, 2$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=12` |
| 12 | $\text{Simplify: } \frac{6\left(y - 8\right)\left(y - 4\right)\left(y - 6\right)\left(y\right)}{\left(y + 5\right)\left(y - 3\right)\left(y - 6\right)\left(y\right)}$ | $\frac{6y^{2} - 72y + 192}{y^{2} + 2y - 15},\; y \neq 0, 6$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=12` |
| 12 | $\text{Simplify: } \frac{-1\left(u - 2\right)\left(u - 1\right)\left(u - 5\right)}{\left(u - 6\right)\left(u - 4\right)\left(u - 1\right)\left(u - 5\right)}$ | $\frac{-u + 2}{u^{2} - 10u + 24},\; u \neq 1, 5$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=12` |
| 16 | $\text{Simplify: } \frac{-4\left(x\right)\left(x - 8\right)\left(x + 8\right)\left(x - 6\right)}{\left(x - 5\right)\left(x + 8\right)\left(x - 6\right)}$ | $\frac{-4x^{2} + 32x}{x - 5},\; x \neq -8, 6$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=16` |
| 16 | $\text{Simplify: } \frac{11\left(x - 7\right)\left(x + 1\right)\left(x - 5\right)\left(x - 2\right)}{\left(x - 6\right)\left(x + 7\right)\left(x - 5\right)\left(x - 2\right)}$ | $\frac{11x^{2} - 66x - 77}{x^{2} + x - 42},\; x \neq 2, 5$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=16` |
| 16 | $\text{Simplify: } \frac{4\left(i - 4\right)\left(i - 6\right)\left(i - 5\right)}{\left(i - 2\right)\left(i - 6\right)\left(i - 5\right)}$ | $\frac{4i - 16}{i - 2},\; i \neq 5, 6$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=16` |
| 20 | $\text{Simplify: } \frac{4\left(w - 3\right)\left(w + 1\right)\left(w - 4\right)}{\left(w - 1\right)\left(w - 2\right)\left(w + 1\right)\left(w - 4\right)}$ | $\frac{4w - 12}{w^{2} - 3w + 2},\; w \neq -1, 4$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=20` |
| 20 | $\text{Simplify: } \frac{-15\left(x\right)\left(x - 19\right)\left(x + 7\right)\left(x + 14\right)}{\left(x - 6\right)\left(x - 10\right)\left(x + 7\right)\left(x + 14\right)}$ | $\frac{-15x^{2} + 285x}{x^{2} - 16x + 60},\; x \neq -14, -7$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=20` |
| 20 | $\text{Simplify: } \frac{7\left(y - 2\right)\left(y - 15\right)\left(y + 2\right)}{\left(y - 3\right)\left(y - 15\right)\left(y + 2\right)}$ | $\frac{7y - 14}{y - 3},\; y \neq -2, 15$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=20` |
| 25 | $\text{Simplify: } \frac{5\left(d\right)\left(d - 1\right)\left(d - 9\right)\left(d - 2\right)}{\left(d + 8\right)\left(d - 9\right)\left(d - 2\right)}$ | $\frac{5d^{2} - 5d}{d + 8},\; d \neq 2, 9$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=25` |
| 25 | $\text{Simplify: } \frac{-1\left(\rho - 3\right)\left(\rho\right)\left(\rho - 7\right)\left(\rho - 8\right)}{\left(\rho - 2\right)\left(\rho - 7\right)\left(\rho - 8\right)}$ | $\frac{-\rho^{2} + 3\rho}{\rho - 2},\; \rho \neq 7, 8$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=25` |
| 25 | $\text{Simplify: } \frac{10\left(\mu + 3\right)\left(\mu - 2\right)\left(\mu - 9\right)\left(\mu - 1\right)}{\left(\mu - 4\right)\left(\mu - 3\right)\left(\mu - 9\right)\left(\mu - 1\right)}$ | $\frac{10\mu^{2} + 10\mu - 60}{\mu^{2} - 7\mu + 12},\; \mu \neq 1, 9$ | `—` | `spec_pack=structured_rational_simplify · methods=rational,cancel · form_id=simplify_cancel · shape=simplify_cancel · D=25` |

## A2 rational add/subtract (shared constructive core)

<a id="rational_add"></a>

`a2_rational_expressions_adding_and_subtracting` · pack `rational_add` · topic label: a2: Adding and subtracting rational expressions · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **1** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `rational_expression_simplification:add_subtract_rationals` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Combine and simplify: } \frac{2}{x - 2} + \frac{1}{x - 2}$ | $\frac{3}{x - 2},\; x \neq 2$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_common_den · shape=add_common_den · D=0` |
| 0 | $\text{Combine and simplify: } \frac{2}{x - 1} - \frac{1}{x - 1}$ | $\frac{1}{x - 1},\; x \neq 1$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_common_den · shape=add_common_den · D=0` |
| 0 | $\text{Combine and simplify: } \frac{2}{x + 1} + \frac{3}{x + 1}$ | $\frac{5}{x + 1},\; x \neq -1$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_common_den · shape=add_common_den · D=0` |
| 3 | $\text{Combine and simplify: } \frac{3}{x} + \frac{2}{x}$ | $\frac{5}{x},\; x \neq 0$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_common_den · shape=add_common_den · D=3` |
| 3 | $\text{Combine and simplify: } \frac{-2}{x - 2} - \frac{3}{x - 2}$ | $\frac{-5}{x - 2},\; x \neq 2$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_common_den · shape=add_common_den · D=3` |
| 3 | $\text{Combine and simplify: } \frac{1}{x} + \frac{4}{x}$ | $\frac{5}{x},\; x \neq 0$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_common_den · shape=add_common_den · D=3` |
| 6 | $\text{Combine and simplify: } \frac{4z - 4}{z^{2} - 5z + 4}+\frac{3z - 3}{z^{2} + 3z - 4}$ | $\frac{7z + 4}{z^{2} - 16},\; z \neq 1$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_dens · shape=add_unlike_dens · D=6` |
| 6 | $\text{Combine and simplify: } \frac{-4}{x - 1} - \frac{4}{x - 1}$ | $\frac{-8}{x - 1},\; x \neq 1$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_common_den · shape=add_common_den · D=6` |
| 6 | $\text{Combine and simplify: } \frac{-x + 3}{x^{2} - 9}+\frac{-3}{x}$ | $\frac{-4x - 9}{x^{2} + 3x},\; x \neq 3$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_dens · shape=add_unlike_dens · D=6` |
| 8 | $\text{Combine and simplify: } \frac{-4}{w} + \frac{1}{w}$ | $\frac{-3}{w},\; w \neq 0$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_common_den · shape=add_common_den · D=8` |
| 8 | $\text{Combine and simplify: } \frac{6y - 6}{y^{2} - 5y + 4}+\frac{1}{y + 5}$ | $\frac{7y + 26}{y^{2} + y - 20},\; y \neq 1$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_dens · shape=add_unlike_dens · D=8` |
| 8 | $\text{Combine and simplify: } \frac{5}{x - 3} + \frac{-4}{x - 3}$ | $\frac{1}{x - 3},\; x \neq 3$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_common_den · shape=add_common_den · D=8` |
| 12 | $\text{Combine and simplify: } \frac{-6}{q - 5}+\frac{-6q^{2} + 24q - 18}{\left(q - 4\right)\left(q - 3\right)\left(q - 1\right)}+\frac{-5}{q - 2}$ | $\frac{-17q^{2} + 123q - 208}{q^{3} - 11q^{2} + 38q - 40},\; q \neq 1, 3$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_with_cancel · shape=add_unlike_with_cancel · D=12` |
| 12 | $\text{Combine and simplify: } \frac{4x^{2} + 8x - 32}{\left(x - 4\right)\left(x + 4\right)\left(x - 2\right)}+\frac{3x^{2} + 6x - 24}{\left(x - 1\right)\left(x + 4\right)\left(x - 2\right)}$ | $\frac{7x - 16}{x^{2} - 5x + 4},\; x \neq -4, 2$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_dens · shape=add_unlike_dens · D=12` |
| 12 | $\text{Combine and simplify: } \frac{2r + 4}{r^{2} - r - 6}+\frac{-1}{r + 3}+\frac{2r^{2} + 6r + 4}{\left(r\right)\left(r + 1\right)\left(r + 2\right)}$ | $\frac{3r^{2} + 9r - 18}{r^{3} - 9r},\; r \neq -2, -1$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_with_cancel · shape=add_unlike_with_cancel · D=12` |
| 16 | $\text{Combine and simplify: } \frac{-6r + 24}{r^{2} - 5r + 4}+\frac{6r - 36}{r^{2} - 6r}$ | $\frac{-6}{r^{2} - r},\; r \neq 4, 6$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_dens · shape=add_unlike_dens · D=16` |
| 16 | $\text{Combine and simplify: } \frac{2j^{2} - 12j + 16}{\left(j\right)\left(j - 4\right)\left(j - 2\right)}+\frac{-4j + 8}{j^{2} - 5j + 6}+\frac{3}{j - 6}$ | $\frac{j^{2} - 3j + 36}{j^{3} - 9j^{2} + 18j},\; j \neq 2, 4$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_with_cancel · shape=add_unlike_with_cancel · D=16` |
| 16 | $\text{Combine and simplify: } \frac{z}{z^{2} - 2z}+\frac{-3z + 3}{z^{2} - 4z + 3}$ | $\frac{-2z + 3}{z^{2} - 5z + 6},\; z \neq 0, 1$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_dens · shape=add_unlike_dens · D=16` |
| 20 | $\text{Combine and simplify: } \frac{5n^{2} + 25n - 520}{\left(n + 6\right)\left(n - 8\right)\left(n + 13\right)}+\frac{9n + 117}{n^{2} + 8n - 65}$ | $\frac{14n + 29}{n^{2} + n - 30},\; n \neq -13, 8$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_dens · shape=add_unlike_dens · D=20` |
| 20 | $\text{Combine and simplify: } \frac{8h + 40}{h^{2} + h - 20}+\frac{11h^{2} - 11h - 330}{\left(h + 7\right)\left(h + 5\right)\left(h - 6\right)}+\frac{4h - 24}{h^{2} - 6h}$ | $\frac{23h^{2} + 24h - 112}{h^{3} + 3h^{2} - 28h},\; h \neq -5, 6$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_with_cancel · shape=add_unlike_with_cancel · D=20` |
| 20 | $\text{Combine and simplify: } \frac{13p - 78}{p^{2} - 17p + 66}+\frac{-9p^{2} + 81p - 162}{\left(p - 2\right)\left(p - 3\right)\left(p - 6\right)}+\frac{p - 6}{p^{2} + 8p - 84}$ | $\frac{5p^{2} + 116p + 1044}{p^{3} + p^{2} - 160p + 308},\; p \neq 3, 6$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_with_cancel · shape=add_unlike_with_cancel · D=20` |
| 25 | $\text{Combine and simplify: } \frac{10\gamma^{2} - 640}{\left(\gamma - 10\right)\left(\gamma + 8\right)\left(\gamma - 8\right)}+\frac{-9\gamma^{2} + 576}{\left(\gamma - 7\right)\left(\gamma + 8\right)\left(\gamma - 8\right)}$ | $\frac{\gamma + 20}{\gamma^{2} - 17\gamma + 70},\; \gamma \neq -8, 8$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_dens · shape=add_unlike_dens · D=25` |
| 25 | $\text{Combine and simplify: } \frac{7\xi^{2} - 28\xi - 147}{\left(\xi + 11\right)\left(\xi + 3\right)\left(\xi - 7\right)}+\frac{6\xi^{2} - 24\xi - 126}{\left(\xi - 9\right)\left(\xi + 3\right)\left(\xi - 7\right)}+\frac{-2\xi + 14}{\xi^{2} - 9\xi + 14}$ | $\frac{11\xi^{2} - 27\xi + 192}{\xi^{3} - 103\xi + 198},\; \xi \neq -3, 7$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_with_cancel · shape=add_unlike_with_cancel · D=25` |
| 25 | $\text{Combine and simplify: } \frac{3g^{2} - 3g - 6}{\left(g + 2\right)\left(g - 2\right)\left(g + 1\right)}+\frac{g - 2}{g^{2} - 7g + 10}$ | $\frac{4g - 13}{g^{2} - 3g - 10},\; g \neq -1, 2$ | `—` | `spec_pack=structured_rational_add · methods=rational,combine,cancel · form_id=add_unlike_dens · shape=add_unlike_dens · D=25` |

## A2 multiply polynomials (inherits A1 primitive)

<a id="poly_multiply"></a>

`a2_polynomial_functions_multiplying` · pack `poly_multiply` · topic label: a2: Multiplying · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `polynomial_multiply:distribute` | 16 |
| `polynomial_multiply:foil` | 8 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Multiply: } \left(x + 2\right)\left(x + 2\right)$ | $x^{2} + 4x + 4$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=0` |
| 0 | $\text{Multiply: } \left(2x - 2\right)\left(3x\right)$ | $6x^{2} - 6x$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=0` |
| 0 | $\text{Multiply: } \left(x + 3\right)\left(x\right)$ | $x^{2} + 3x$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=0` |
| 3 | $\text{Multiply: } \left(x + 1\right)\left(x - 3\right)$ | $x^{2} - 2x - 3$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=3` |
| 3 | $\text{Multiply: } \left(2x - 3\right)\left(2x + 1\right)$ | $4x^{2} - 4x - 3$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=foil · shape=foil · D=3` |
| 3 | $\text{Multiply: } \left(2x - 3\right)\left(-2x + 1\right)$ | $-4x^{2} + 8x - 3$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=foil · shape=foil · D=3` |
| 6 | $\text{Multiply: } \left(2x + 3\right)\left(x + 1\right)$ | $2x^{2} + 5x + 3$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=foil · shape=foil · D=6` |
| 6 | $\text{Multiply: } \left(-2z + 2\right)\left(-z + 1\right)$ | $2z^{2} - 4z + 2$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=foil · shape=foil · D=6` |
| 6 | $\text{Multiply: } \left(-x - 1\right)\left(3x + 1\right)$ | $-3x^{2} - 4x - 1$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=foil · shape=foil · D=6` |
| 8 | $\text{Multiply: } \left(4y + 2\right)\left(2y + 2\right)$ | $8y^{2} + 12y + 4$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=foil · shape=foil · D=8` |
| 8 | $\text{Multiply: } \left(x + 3\right)\left(x^{2} + x + 2\right)$ | $x^{3} + 4x^{2} + 5x + 6$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=8` |
| 8 | $\text{Multiply: } \left(x^{2} + 2x + 1\right)\left(2x\right)$ | $2x^{3} + 4x^{2} + 2x$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=8` |
| 12 | $\text{Multiply: } \left(x^{2} + 3\right)\left(-2x + 1\right)$ | $-2x^{3} + x^{2} - 6x + 3$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=foil · shape=foil · D=12` |
| 12 | $\text{Multiply: } \left(2x^{2}\right)\left(x + 1\right)$ | $2x^{3} + 2x^{2}$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=12` |
| 12 | $\text{Multiply: } \left(-x^{2} + x - 1\right)\left(2x\right)$ | $-2x^{3} + 2x^{2} - 2x$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=12` |
| 16 | $\text{Multiply: } \left(3y + 1\right)\left(-2y^{2} - y + 1\right)$ | $-6y^{3} - 5y^{2} + 2y + 1$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=16` |
| 16 | $\text{Multiply: } \left(3x^{2} + 2x + 3\right)\left(-3x^{2}\right)$ | $-9x^{4} - 6x^{3} - 9x^{2}$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=16` |
| 16 | $\text{Multiply: } \left(-2x^{2} - 3x - 3\right)\left(3x\right)$ | $-6x^{3} - 9x^{2} - 9x$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=16` |
| 20 | $\text{Multiply: } \left(3x + 2\right)\left(x^{2} + 4\right)$ | $3x^{3} + 2x^{2} + 12x + 8$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=foil · shape=foil · D=20` |
| 20 | $\text{Multiply: } \left(7y - 5\right)\left(8y^{2} - 10y - 3\right)$ | $56y^{3} - 110y^{2} + 29y + 15$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=20` |
| 20 | $\text{Multiply: } \left(x + 1\right)\left(5x^{2} + 4x - 7\right)$ | $5x^{3} + 9x^{2} - 3x - 7$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=20` |
| 25 | $\text{Multiply: } \left(2x^{2} + 3x - 2\right)\left(2x - 3\right)$ | $4x^{3} - 13x + 6$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=25` |
| 25 | $\text{Multiply: } \left(3x^{3}\right)\left(-2x + 4\right)$ | $-6x^{4} + 12x^{3}$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=25` |
| 25 | $\text{Multiply: } \left(4x^{2} + 3x - 4\right)\left(2x^{2}\right)$ | $8x^{4} + 6x^{3} - 8x^{2}$ | `—` | `spec_pack=structured_polynomial_multiply · methods=product · form_id=distribute · shape=distribute · D=25` |

## A2 factor by grouping

<a id="poly_factor_grouping"></a>

`a2_polynomial_functions_factoring_by_grouping` · pack `poly_factor_grouping` · topic label: a2: Factoring by grouping · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `polynomial_factoring_grouping:grouping_cubic` | 13 |
| `polynomial_factoring_grouping:grouping_quadratic` | 11 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $x^{2} + 8x + 15$ | $\left(x + 5\right)\left(x + 3\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=0` |
| 0 | $4x^{2} + 21x + 20$ | $\left(x + 4\right)\left(4x + 5\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=0` |
| 0 | $x^{2} + 7x + 12$ | $\left(x + 3\right)\left(x + 4\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=0` |
| 3 | $3x^{2} + 8x + 5$ | $\left(x + 1\right)\left(3x + 5\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=3` |
| 3 | $3x^{2} - 8x + 5$ | $\left(x - 1\right)\left(3x - 5\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=3` |
| 3 | $x^{2} - x - 20$ | $\left(x - 5\right)\left(x + 4\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=3` |
| 6 | $3x^{3} + 12x^{2} - 2x - 8$ | $\left(x + 4\right)\left(3x^{2} - 2\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=6` |
| 6 | $x^{2} - 6x + 5$ | $\left(x - 1\right)\left(x - 5\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=6` |
| 6 | $2x^{3} + 4x^{2} - 4x - 8$ | $2\left(x + 2\right)\left(x^{2} - 2\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=6` |
| 8 | $4x^{3} - 8x^{2} + 5x - 10$ | $\left(x - 2\right)\left(4x^{2} + 5\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=8` |
| 8 | $3x^{2} - 8x - 16$ | $\left(x - 4\right)\left(3x + 4\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=8` |
| 8 | $2x^{3} + 4x^{2} + 3x + 6$ | $\left(x + 2\right)\left(2x^{2} + 3\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=8` |
| 12 | $16x - 10x + 8 + x^{2}$ | $\left(x + 2\right)\left(x + 4\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=12` |
| 12 | $-3z - 2\left(z^{3} - 1\right) + 3z^{3} - 4z^{2} + 10$ | $\left(z - 4\right)\left(z^{2} - 3\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=12` |
| 12 | $-2y^{2} + y - 26 + 3\left(y^{2} + 2\right)$ | $\left(y + 5\right)\left(y - 4\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=12` |
| 16 | $2\left(u^{3} - u\right) - 8 + 8u^{2}$ | $2\left(u + 4\right)\left(u^{2} - 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=16` |
| 16 | $-9 + 2s^{2} - s^{2}$ | $\left(s + 3\right)\left(s - 3\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=16` |
| 16 | $-8x^{2} - 3x + 12 - 2\left(-x^{3}\right)$ | $\left(x - 4\right)\left(2x^{2} - 3\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=16` |
| 20 | $-4x^{2} + 7x^{3} - 6x^{3} + 2x^{2} + 3x - 6$ | $\left(x - 2\right)\left(x^{2} + 3\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=20` |
| 20 | $2\left(x^{3} + 1\right) + 2\left(-3x^{2} + 2\right) - 5x + 9$ | $\left(x - 3\right)\left(2x^{2} - 5\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=20` |
| 20 | $t^{3} - 3t^{3} + 5t^{3} + 9t^{2} + 6 + 2t$ | $\left(t + 3\right)\left(3t^{2} + 2\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=20` |
| 25 | $3\left(u^{3} - 2\right) - u^{3} + 6u^{2} + 2u + 12$ | $2\left(u + 3\right)\left(u^{2} + 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=25` |
| 25 | $9x - 4x + 5 + 15 + 16x^{2} + 4x^{3}$ | $\left(x + 4\right)\left(4x^{2} + 5\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=25` |
| 25 | $2\left(\theta^{3} + 1\right) - \theta^{3} - 4\theta^{2} + 4\theta - 18$ | $\left(\theta - 4\right)\left(\theta^{2} + 4\right)$ | `—` | `spec_pack=structured_polynomial_factoring_grouping · methods=factor · form_id=factor_by_grouping · shape=factor_by_grouping · D=25` |

## A2 sum/difference of cubes

<a id="sum_diff_cubes"></a>

`a2_polynomial_functions_factoring_sum_difference_of_cubes` · pack `sum_diff_cubes` · topic label: a2: Factoring a sum/difference of cubes · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `polynomial_factoring_sum_diff_cubes:difference_of_cubes` | 16 |
| `polynomial_factoring_sum_diff_cubes:sum_of_cubes` | 8 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $x^{3} - 8$ | $\left(x - 2\right)\left(x^{2} + 2x + 4\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=0` |
| 0 | $x^{3} - 1$ | $\left(x - 1\right)\left(x^{2} + x + 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=0` |
| 0 | $x^{3} - 1$ | $\left(x - 1\right)\left(x^{2} + x + 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=0` |
| 3 | $x^{3} - 1$ | $\left(x - 1\right)\left(x^{2} + x + 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=3` |
| 3 | $x^{3} - 1$ | $\left(x - 1\right)\left(x^{2} + x + 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=3` |
| 3 | $x^{3} + 8$ | $\left(x + 2\right)\left(x^{2} - 2x + 4\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=sum_of_cubes · shape=sum_of_cubes · D=3` |
| 6 | $y^{3} - 125$ | $\left(y - 5\right)\left(y^{2} + 5y + 25\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=6` |
| 6 | $x^{3} - 27$ | $\left(x - 3\right)\left(x^{2} + 3x + 9\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=6` |
| 6 | $x^{3} + 8$ | $\left(x + 2\right)\left(x^{2} - 2x + 4\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=sum_of_cubes · shape=sum_of_cubes · D=6` |
| 8 | $27x^{3} - 64$ | $\left(3x - 4\right)\left(9x^{2} + 12x + 16\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=8` |
| 8 | $x^{3} - 1$ | $\left(x - 1\right)\left(x^{2} + x + 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=8` |
| 8 | $8x^{3} - 1$ | $\left(2x - 1\right)\left(4x^{2} + 2x + 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=8` |
| 12 | $-3x^{3} + 4x^{3} + 1$ | $\left(x + 1\right)\left(x^{2} - x + 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=sum_of_cubes · shape=sum_of_cubes · D=12` |
| 12 | $2y^{3} - y^{3} - 1$ | $\left(y - 1\right)\left(y^{2} + y + 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=12` |
| 12 | $2\left(k^{3} + 2\right) - k^{3} + 60$ | $\left(k + 4\right)\left(k^{2} - 4k + 16\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=sum_of_cubes · shape=sum_of_cubes · D=12` |
| 16 | $-y^{3} - 125 + 2y^{3}$ | $\left(y - 5\right)\left(y^{2} + 5y + 25\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=16` |
| 16 | $-x^{3} - 68 + 2\left(x^{3} + 2\right)$ | $\left(x - 4\right)\left(x^{2} + 4x + 16\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=16` |
| 16 | $-64 + 3y^{3} - 2y^{3}$ | $\left(y - 4\right)\left(y^{2} + 4y + 16\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=16` |
| 20 | $3\left(x^{3} - 1\right) - 2x^{3} - 5$ | $\left(x - 2\right)\left(x^{2} + 2x + 4\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=20` |
| 20 | $24 + 5z^{3} - 4z^{3} + 3$ | $\left(z + 3\right)\left(z^{2} - 3z + 9\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=sum_of_cubes · shape=sum_of_cubes · D=20` |
| 20 | $-5\sigma^{3} - 1 + 4\sigma^{3} + 2\left(\sigma^{3} + 1\right)$ | $\left(\sigma + 1\right)\left(\sigma^{2} - \sigma + 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=sum_of_cubes · shape=sum_of_cubes · D=20` |
| 25 | $3 + 24 + 31m^{3} - 4m^{3}$ | $27\left(m + 1\right)\left(m^{2} - m + 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=sum_of_cubes · shape=sum_of_cubes · D=25` |
| 25 | $-1 - 26 - x^{3} + 2x^{3}$ | $\left(x - 3\right)\left(x^{2} + 3x + 9\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=difference_of_cubes · shape=difference_of_cubes · D=25` |
| 25 | $4k^{3} + 23k^{3} + 27$ | $27\left(k + 1\right)\left(k^{2} - k + 1\right)$ | `—` | `spec_pack=structured_polynomial_factoring_sum_diff_cubes · methods=factor · form_id=sum_of_cubes · shape=sum_of_cubes · D=25` |

## A2 properties of logarithms

<a id="log_props"></a>

`a2_exponential_and_logarithmic_expressions_properties_of_logarithms` · pack `log_props` · topic label: a2: Properties of logarithms · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **1** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `log_change_of_base:log_properties_condense` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Expand: } \log_{2}\left(\frac{6}{2}\right)$ | $\log_{2}(6)-\log_{2}(2)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=0` |
| 0 | $\text{Expand: } \log_{3}\left(\frac{12}{2}\right)$ | $\log_{3}(12)-\log_{3}(2)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=0` |
| 0 | $\text{Expand: } \log_{3}\left(56\right)$ | $\log_{3}(8)+\log_{3}(7)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=0` |
| 3 | $\text{Expand: } \log_{5}\left(15\right)$ | $\log_{5}(3)+\log_{5}(5)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=3` |
| 3 | $\text{Expand: } \log_{3}\left(5^{5}\right)$ | $5\log_{3}(5)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=3` |
| 3 | $\text{Expand: } \log_{3}\left(12\right)$ | $\log_{3}(6)+\log_{3}(2)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=3` |
| 6 | $\text{Expand: } \log_{3}\left(\frac{21}{7}\right)$ | $\log_{3}(21)-\log_{3}(7)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=6` |
| 6 | $\text{Expand: } \log_{10}\left(6^{2}\right)$ | $2\log_{10}(6)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=6` |
| 6 | $\text{Expand: } \log_{6}\left(9^{2}\right)$ | $2\log_{6}(9)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=6` |
| 8 | $\text{Expand: } \log_{2}\left(12\right)$ | $\log_{2}(4)+\log_{2}(3)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=8` |
| 8 | $\text{Expand: } \log_{5}\left(\frac{18}{6}\right)$ | $\log_{5}(18)-\log_{5}(6)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=8` |
| 8 | $\text{Expand: } \log_{2}\left(6^{3}\right)$ | $3\log_{2}(6)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=8` |
| 12 | $\text{Expand: } \log_{9}\left(28\right)$ | $\log_{9}(4)+\log_{9}(7)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=12` |
| 12 | $\text{Expand: } \log_{5}\left(5^{2}\right)$ | $2\log_{5}(5)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=12` |
| 12 | $\text{Expand: } \log_{9}\left(\frac{28}{7}\right)$ | $\log_{9}(28)-\log_{9}(7)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=12` |
| 16 | $\text{Expand: } \log_{12}\left(\frac{30}{6}\right)$ | $\log_{12}(30)-\log_{12}(6)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=16` |
| 16 | $\text{Expand: } \log_{8}\left(\frac{9}{3}\right)$ | $\log_{8}(9)-\log_{8}(3)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=16` |
| 16 | $\text{Expand: } \log_{2}\left(6^{5}\right)$ | $5\log_{2}(6)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=16` |
| 20 | $\text{Expand: } \log_{2}\left(7^{5}\right)$ | $5\log_{2}(7)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=20` |
| 20 | $\text{Expand: } \log_{10}\left(\frac{24}{4}\right)$ | $\log_{10}(24)-\log_{10}(4)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=20` |
| 20 | $\text{Expand: } \log_{7}\left(14\right)$ | $\log_{7}(7)+\log_{7}(2)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=20` |
| 25 | $\text{Expand: } \log_{6}\left(9^{2}\right)$ | $2\log_{6}(9)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=25` |
| 25 | $\text{Expand: } \log_{12}\left(18\right)$ | $\log_{12}(3)+\log_{12}(6)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=25` |
| 25 | $\text{Expand: } \log_{6}\left(4^{5}\right)$ | $5\log_{6}(4)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_properties_condense · shape=log_properties_condense · D=25` |

## A2 exponential equations (same base)

<a id="exp_equation"></a>

`a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms` · pack `exp_equation` · topic label: a2: Exponential equations not requiring logarithms · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **1** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `exponential_equation_simple:exp_same_base` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $2^{x} = 2$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=0` |
| 0 | $3^{x} = 3$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=0` |
| 0 | $2^{x} = 4$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=0` |
| 3 | $4^{x} = 64$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=3` |
| 3 | $2^{x} = 8$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=3` |
| 3 | $4^{x} = 4$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=3` |
| 6 | $6^{x} = 36$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=6` |
| 6 | $5^{x} = 25$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=6` |
| 6 | $3^{x} = 81$ | $x = 4$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=6` |
| 8 | $5^{x} = 5$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=8` |
| 8 | $4^{x} = 256$ | $x = 4$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=8` |
| 8 | $5^{x} = 625$ | $x = 4$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=8` |
| 12 | $6^{x} = 7776$ | $x = 5$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=12` |
| 12 | $6^{x} = 6$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=12` |
| 12 | $8^{x} = 8$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=12` |
| 16 | $3^{x} = 243$ | $x = 5$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=16` |
| 16 | $3^{x} = 3$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=16` |
| 16 | $4^{x} = 16$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=16` |
| 20 | $6^{x} = 36$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=20` |
| 20 | $9^{x} = 6561$ | $x = 4$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=20` |
| 20 | $11^{x} = 121$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=20` |
| 25 | $4^{x} = 64$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=25` |
| 25 | $8^{x} = 512$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=25` |
| 25 | $11^{x} = 1331$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=25` |

## A2 function operations algebraic

<a id="function_ops"></a>

`a2_general_functions_operations` · pack `function_ops` · topic label: a2: Operations · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **4** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `function_operations:add` | 9 |
| `function_operations:subtract` | 8 |
| `function_operations:product` | 4 |
| `function_operations:compose` | 3 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{If } f(x) = 3x + 0 \text{ and } g(x) = 3x + 4, \text{ find } (f \cdot g)(1).$ | $21$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_product · shape=fn_product · D=0` |
| 0 | $\text{If } f(x) = 3x - 1 \text{ and } g(x) = 3x + 2, \text{ find } (f - g)(-5).$ | $-3$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_subtract · shape=fn_subtract · D=0` |
| 0 | $\text{If } f(x) = 3x - 1 \text{ and } g(x) = -3x - 1, \text{ find } (f + g)(3).$ | $-2$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_add · shape=fn_add · D=0` |
| 3 | $\text{If } f(x) = 3x - 1 \text{ and } g(x) = -3x + 3, \text{ find } (f - g)(3).$ | $14$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_subtract · shape=fn_subtract · D=3` |
| 3 | $\text{If } f(x) = -3x - 1 \text{ and } g(x) = 3x - 3, \text{ find } (f + g)(1).$ | $-4$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_add · shape=fn_add · D=3` |
| 3 | $\text{If } f(x) = -3x - 3 \text{ and } g(x) = 3x - 3, \text{ find } (f - g)(-4).$ | $24$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_subtract · shape=fn_subtract · D=3` |
| 6 | $\text{If } f(x) = 6x - 7 \text{ and } g(x) = 6x - 4, \text{ find } (f \cdot g)(4).$ | $340$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_product · shape=fn_product · D=6` |
| 6 | $\text{If } f(x) = -6x + 7 \text{ and } g(x) = -6x + 6, \text{ find } (f \cdot g)(1).$ | $0$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_product · shape=fn_product · D=6` |
| 6 | $\text{If } f(x) = 6x + 8 \text{ and } g(x) = 6x - 5, \text{ find } (f + g)(-6).$ | $-69$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_add · shape=fn_add · D=6` |
| 8 | $\text{If } f(x) = 6x - 6 \text{ and } g(x) = -6x - 3, \text{ find } (f + g)(-7).$ | $-9$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_add · shape=fn_add · D=8` |
| 8 | $\text{If } f(x) = -6x - 4 \text{ and } g(x) = 6x - 2, \text{ find } (f - g)(-4).$ | $46$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_subtract · shape=fn_subtract · D=8` |
| 8 | $\text{If } f(x) = 6x + 1 \text{ and } g(x) = -6x - 8, \text{ find } (f + g)(-2).$ | $-7$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_add · shape=fn_add · D=8` |
| 12 | $\text{If } f(x) = -8x - 10 \text{ and } g(x) = -8x - 4, \text{ find } (f + g)(-4).$ | $50$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_add · shape=fn_add · D=12` |
| 12 | $\text{If } f(x) = 8x + 3 \text{ and } g(x) = -8x + 8, \text{ find } (f - g)(-6).$ | $-101$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_subtract · shape=fn_subtract · D=12` |
| 12 | $\text{If } f(x) = -8x + 3 \text{ and } g(x) = 8x + 6, \text{ find } (f \cdot g)(5).$ | $-1702$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_product · shape=fn_product · D=12` |
| 16 | $\text{If } f(x) = -8x - 1 \text{ and } g(x) = -8x + 7, \text{ find } (f + g)(-7).$ | $118$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_add · shape=fn_add · D=16` |
| 16 | $\text{If } f(x) = -8x + 1 \text{ and } g(x) = -8x + 3, \text{ find } (f \circ g)(0).$ | $-23$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_compose · shape=fn_compose · D=16` |
| 16 | $\text{If } f(x) = -8x + 5 \text{ and } g(x) = -8x + 5, \text{ find } (f - g)(1).$ | $0$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_subtract · shape=fn_subtract · D=16` |
| 20 | $\text{If } f(x) = 9x - 5 \text{ and } g(x) = 9x - 6, \text{ find } (f + g)(-6).$ | $-119$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_add · shape=fn_add · D=20` |
| 20 | $\text{If } f(x) = -9x - 8 \text{ and } g(x) = -9x - 5, \text{ find } (f - g)(-2).$ | $-3$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_subtract · shape=fn_subtract · D=20` |
| 20 | $\text{If } f(x) = 9x + 9 \text{ and } g(x) = 9x - 7, \text{ find } (f \circ g)(-1).$ | $-135$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_compose · shape=fn_compose · D=20` |
| 25 | $\text{If } f(x) = -11x + 7 \text{ and } g(x) = -11x - 4, \text{ find } (f \circ g)(-7).$ | $-796$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_compose · shape=fn_compose · D=25` |
| 25 | $\text{If } f(x) = -11x + 1 \text{ and } g(x) = -11x - 10, \text{ find } (f + g)(-5).$ | $101$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_add · shape=fn_add · D=25` |
| 25 | $\text{If } f(x) = 11x + 11 \text{ and } g(x) = -11x + 8, \text{ find } (f - g)(5).$ | $113$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=fn_subtract · shape=fn_subtract · D=25` |
