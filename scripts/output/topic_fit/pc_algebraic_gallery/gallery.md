# Precalculus algebraic gallery

Generated: 2026-08-03T16:43:29.126164+00:00

Live samples via `_generate_for_type` (D = 0, 3, 6, 8, 12, 16, 20, 25; 3 seeds each). No Easy/Medium/Hard labels — continuous **D=** only.

Open [gallery.html](gallery.html) in a browser for KaTeX (local `_assets/katex`).

- topics ok: **8** · skipped missing: **0**
- samples ok: **192** · errors: **0**
- metadata: `tricks_required`, `spec_snapshot` pack, form/shape when present

## Structure inventory

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **17** · samples: **192**

| Structure / family | Count |
|--------|------:|
| `(unlabeled)` | 48 |
| `exponential_equation_with_log:exp_needs_logarithm` | 24 |
| `partial_fraction_decomposition:pfd` | 24 |
| `exponential_equation_simple:exp_same_base` | 16 |
| `derivative_power_rule:power` | 13 |
| `function_operations:add` | 11 |
| `log_change_of_base:log_product_rule_expand` | 9 |
| `derivative_power_rule:power+sum` | 8 |
| `exponential_equation_simple:exp_rewrite_common_base` | 8 |
| `log_change_of_base:log_change_of_base` | 7 |
| `function_operations:quotient` | 5 |
| `log_change_of_base:log_quotient_rule_expand` | 5 |
| `function_operations:compose` | 4 |
| `log_change_of_base:log_power_rule_expand` | 3 |
| `derivative_power_rule:chain+power` | 2 |
| `function_operations:product` | 2 |
| `function_operations:subtract` | 2 |
| `derivative_power_rule:chain+power+product` | 1 |

## Topics

- [Precalc properties of logarithms](#log_props) — `pc_properties_of_logarithms`
- [Precalc exponential equations (same base)](#exp_equation) — `pc_exponential_equations_not_requiring_logarithms`
- [Precalc intro-calc power rule (shared Spec with calc)](#power_rule) — `pc_power_rule_for_differentiation`
- [Precalc PFD (construct_pfd; reverse of rational add)](#pfd) — `pc_partial_fraction_decomposition`
- [Precalc function operations algebraic](#function_ops) — `pc_functions_operations`
- [Precalc rational equations](#rational_equations) — `pc_rational_equations`
- [Precalc simple log equations](#log_equation) — `pc_logarithmic_equations_simple`
- [Precalc exponential equations requiring logs](#exp_equation_log) — `pc_exponential_equations_requiring_logarithms`

## Precalc properties of logarithms

<a id="log_props"></a>

`pc_properties_of_logarithms` · pack `log_props` · topic label: pc: Properties of logarithms · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **4** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `log_change_of_base:log_product_rule_expand` | 9 |
| `log_change_of_base:log_change_of_base` | 7 |
| `log_change_of_base:log_quotient_rule_expand` | 5 |
| `log_change_of_base:log_power_rule_expand` | 3 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Expand: } \log_{2}\left(32\right)$ | $\log_{2}(8)+\log_{2}(4)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_product_rule_expand · shape=log_product_rule_expand · D=0` |
| 0 | $\text{Expand: } \log_{5}\left(24\right)$ | $\log_{5}(3)+\log_{5}(8)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_product_rule_expand · shape=log_product_rule_expand · D=0` |
| 0 | $\text{Rewrite using change of base: } \log_{5}(3125)$ | $\frac{\log_{2}(3125)}{\log_{2}(5)}$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_change_of_base · shape=log_change_of_base · D=0` |
| 3 | $\text{Expand: } \log_{5}\left(18\right)$ | $\log_{5}(6)+\log_{5}(3)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_product_rule_expand · shape=log_product_rule_expand · D=3` |
| 3 | $\text{Expand: } \log_{3}\left(9^{4}\right)$ | $4\log_{3}(9)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_power_rule_expand · shape=log_power_rule_expand · D=3` |
| 3 | $\text{Expand: } \log_{2}\left(\frac{30}{5}\right)$ | $\log_{2}(30)-\log_{2}(5)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_quotient_rule_expand · shape=log_quotient_rule_expand · D=3` |
| 6 | $\text{Expand: } \log_{10}\left(\frac{24}{8}\right)$ | $\log_{10}(24)-\log_{10}(8)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_quotient_rule_expand · shape=log_quotient_rule_expand · D=6` |
| 6 | $\text{Expand: } \log_{7}\left(32\right)$ | $\log_{7}(8)+\log_{7}(4)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_product_rule_expand · shape=log_product_rule_expand · D=6` |
| 6 | $\text{Expand: } \log_{9}\left(72\right)$ | $\log_{9}(9)+\log_{9}(8)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_product_rule_expand · shape=log_product_rule_expand · D=6` |
| 8 | $\text{Rewrite using change of base: } \log_{2}(16)$ | $\frac{\log_{9}(16)}{\log_{9}(2)}$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_change_of_base · shape=log_change_of_base · D=8` |
| 8 | $\text{Rewrite using change of base: } \log_{4}(256)$ | $\frac{\log_{8}(256)}{\log_{8}(4)}$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_change_of_base · shape=log_change_of_base · D=8` |
| 8 | $\text{Expand: } \log_{2}\left(3^{5}\right)$ | $5\log_{2}(3)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_power_rule_expand · shape=log_power_rule_expand · D=8` |
| 12 | $\text{Expand: } \log_{9}\left(\frac{4}{2}\right)$ | $\log_{9}(4)-\log_{9}(2)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_quotient_rule_expand · shape=log_quotient_rule_expand · D=12` |
| 12 | $\text{Expand: } \log_{7}\left(48\right)$ | $\log_{7}(6)+\log_{7}(8)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_product_rule_expand · shape=log_product_rule_expand · D=12` |
| 12 | $\text{Rewrite using change of base: } \log_{3}(27)$ | $\frac{\log_{2}(27)}{\log_{2}(3)}$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_change_of_base · shape=log_change_of_base · D=12` |
| 16 | $\text{Expand: } \log_{9}\left(27\right)$ | $\log_{9}(3)+\log_{9}(9)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_product_rule_expand · shape=log_product_rule_expand · D=16` |
| 16 | $\text{Rewrite using change of base: } \log_{5}(125)$ | $\frac{\log_{11}(125)}{\log_{11}(5)}$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_change_of_base · shape=log_change_of_base · D=16` |
| 16 | $\text{Expand: } \log_{4}\left(\frac{8}{2}\right)$ | $\log_{4}(8)-\log_{4}(2)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_quotient_rule_expand · shape=log_quotient_rule_expand · D=16` |
| 20 | $\text{Expand: } \log_{12}\left(18\right)$ | $\log_{12}(6)+\log_{12}(3)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_product_rule_expand · shape=log_product_rule_expand · D=20` |
| 20 | $\text{Expand: } \log_{7}\left(\frac{12}{6}\right)$ | $\log_{7}(12)-\log_{7}(6)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_quotient_rule_expand · shape=log_quotient_rule_expand · D=20` |
| 20 | $\text{Expand: } \log_{7}\left(6^{5}\right)$ | $5\log_{7}(6)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_power_rule_expand · shape=log_power_rule_expand · D=20` |
| 25 | $\text{Rewrite using change of base: } \log_{10}(100)$ | $\frac{\log_{2}(100)}{\log_{2}(10)}$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_change_of_base · shape=log_change_of_base · D=25` |
| 25 | $\text{Expand: } \log_{2}\left(42\right)$ | $\log_{2}(7)+\log_{2}(6)$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_product_rule_expand · shape=log_product_rule_expand · D=25` |
| 25 | $\text{Rewrite using change of base: } \log_{9}(59049)$ | $\frac{\log_{6}(59049)}{\log_{6}(9)}$ | `—` | `spec_pack=structured_log_props · methods=log_props · form_id=log_change_of_base · shape=log_change_of_base · D=25` |

## Precalc exponential equations (same base)

<a id="exp_equation"></a>

`pc_exponential_equations_not_requiring_logarithms` · pack `exp_equation` · topic label: pc: Exponential equations not requiring logarithms · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `exponential_equation_simple:exp_same_base` | 16 |
| `exponential_equation_simple:exp_rewrite_common_base` | 8 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $9^{x} = 27^{x - 1}$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_rewrite_common_base · shape=exp_rewrite_common_base · D=0` |
| 0 | $25^{x} = 5^{x + 2}$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_rewrite_common_base · shape=exp_rewrite_common_base · D=0` |
| 0 | $4^{x} = 4$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=0` |
| 3 | $3^{x} = 3$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=3` |
| 3 | $2^{x} = 8$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=3` |
| 3 | $3^{x} = 27$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=3` |
| 6 | $2^{x} = 2$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=6` |
| 6 | $4^{x} = 4$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=6` |
| 6 | $25^{x} = 5^{x + 2}$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_rewrite_common_base · shape=exp_rewrite_common_base · D=6` |
| 8 | $6^{x} = 1296$ | $x = 4$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=8` |
| 8 | $3^{x} = 81$ | $x = 4$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=8` |
| 8 | $2^{x} = 2$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=8` |
| 12 | $8^{x + 2} = 16^{x + 1}$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_rewrite_common_base · shape=exp_rewrite_common_base · D=12` |
| 12 | $2^{x} = 8$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=12` |
| 12 | $6^{x} = 36$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=12` |
| 16 | $8^{x} = 4096$ | $x = 4$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=16` |
| 16 | $3^{x} = 3$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=16` |
| 16 | $4^{x} = 16$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=16` |
| 20 | $4^{x} = 64$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=20` |
| 20 | $8^{x + 2} = 16^{x + 1}$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_rewrite_common_base · shape=exp_rewrite_common_base · D=20` |
| 20 | $8^{x + 2} = 16^{x + 1}$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_rewrite_common_base · shape=exp_rewrite_common_base · D=20` |
| 25 | $8^{x} = 262144$ | $x = 6$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_same_base · shape=exp_same_base · D=25` |
| 25 | $25^{x} = 5^{x + 2}$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_rewrite_common_base · shape=exp_rewrite_common_base · D=25` |
| 25 | $9^{x} = 27^{x - 1}$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=exp_equation · form_id=exp_rewrite_common_base · shape=exp_rewrite_common_base · D=25` |

## Precalc intro-calc power rule (shared Spec with calc)

<a id="power_rule"></a>

`pc_power_rule_for_differentiation` · pack `power_rule` · topic label: pc: Power rule for differentiation · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **4** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `derivative_power_rule:power` | 13 |
| `derivative_power_rule:power+sum` | 8 |
| `derivative_power_rule:chain+power` | 2 |
| `derivative_power_rule:chain+power+product` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Find }\frac{d}{dx}\left(2x^{4}\right)$ | $8x^{3}$ | `—` | `pack=power_rule · methods=power · form_id=power_poly · shape=power · D=0` |
| 0 | $\text{Find }\frac{d}{dx}\left(x^{2}\right)$ | $2x$ | `—` | `pack=power_rule · methods=power · form_id=power_poly · shape=power · D=0` |
| 0 | $\frac{d}{dx}\left[-x^{4}\right]$ | $-4x^{3}$ | `—` | `pack=power_rule · methods=power · form_id=power_poly · shape=power · D=0` |
| 3 | $\text{Find }\frac{d}{dx}\left(2x^{3} + 3x^{2} - 1\right)$ | $6x^{2} + 6x$ | `—` | `pack=power_rule · methods=power,sum · form_id=power_poly · shape=sum+power · D=3` |
| 3 | $\frac{d}{dx}\left[2x^{3} - 3x^{2} + 2x - 2\right]$ | $6x^{2} - 6x + 2$ | `—` | `pack=power_rule · methods=power,sum · form_id=power_poly · shape=sum+power · D=3` |
| 3 | $\text{Find }\frac{d}{dx}\left(3x^{3} - 3x^{2} - x\right)$ | $9x^{2} - 6x - 1$ | `—` | `pack=power_rule · methods=power,sum · form_id=power_poly · shape=sum+power · D=3` |
| 6 | $\text{Find }\frac{d}{dx}\left(x^{-\frac{3}{2}}\right)$ | $-\frac{3}{2}x^{-\frac{5}{2}}$ | `—` | `pack=power_rule · methods=power · form_id=power_negative · shape=power · D=6` |
| 6 | $\frac{d}{dx}\left[x^{5}\right]$ | $5x^{4}$ | `—` | `pack=power_rule · methods=power · form_id=power_root · shape=power · D=6` |
| 6 | $\text{Find }\frac{d}{dx}\left(2x^{2} + 3x\right)$ | $4x + 3$ | `—` | `pack=power_rule · methods=power,sum · form_id=power_poly · shape=sum+power · D=6` |
| 8 | $\text{Find }\frac{d}{dx}\left(x^{-\frac{1}{2}}\right)$ | $-\frac{1}{2}x^{-\frac{3}{2}}$ | `—` | `pack=power_rule · methods=power · form_id=power_poly · shape=power · D=8` |
| 8 | $\frac{d}{dx}\left[4x^{-5}\right]$ | $-20x^{-6}$ | `—` | `pack=power_rule · methods=power · form_id=power_negative · shape=power · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(x^{-\frac{3}{2}}\right)$ | $-\frac{3}{2}x^{-\frac{5}{2}}$ | `—` | `pack=power_rule · methods=power · form_id=power_negative · shape=power · D=8` |
| 12 | $\frac{d^{2}}{dx^{2}}\left[3x^{3} - 5x^{2} + x + 2\right]$ | $18x - 10$ | `—` | `pack=power_rule · methods=power,sum · form_id=power_poly · shape=sum+power · D=12` |
| 12 | $\text{Find }\frac{d}{dx}\left(\sqrt{\sqrt{3x}}\right)$ | $\frac{1}{2\sqrt{\sqrt{3x}}}\frac{1}{2\sqrt{3x}}\left(3\right)$ | `—` | `pack=power_rule · methods=chain,power · form_id=chain_power_linear · shape=fn:sqrt · D=12` |
| 12 | $\frac{d}{dx}\left[\sqrt{4x + 5}\sqrt{x}\right]$ | $4\frac{1}{2\sqrt{4x + 5}}\sqrt{x} + \frac{1}{2\sqrt{x}}\sqrt{4x + 5}$ | `—` | `pack=power_rule · methods=chain,power,product · form_id=chain_power_linear · shape=fn:sqrt+product+sum · D=12` |
| 16 | $\frac{d^{2}}{dx^{2}}\left[2x^{2} - 3x - 4\right]$ | $4$ | `—` | `pack=power_rule · methods=power,sum · form_id=power_root · shape=sum+power · D=16` |
| 16 | $\frac{d}{dx}\left[-4x^{3}\right]$ | $-12x^{2}$ | `—` | `pack=power_rule · methods=power · form_id=power_negative · shape=power · D=16` |
| 16 | $\text{Find }\frac{d}{dx}\left(\left(x^{2} + 1\right)^{e}\right)$ | $e\left(x^{2} + 1\right)^{e-1}\left(2x\right)$ | `—` | `pack=power_rule · methods=chain,power · form_id=chain_power_linear · shape=sum+power · D=16` |
| 20 | $\text{Find }\frac{d}{dx}\left(x^{-\frac{1}{2}}\right)$ | $-\frac{1}{2}x^{-\frac{3}{2}}$ | `—` | `pack=power_rule · methods=power · form_id=power_root · shape=power · D=20` |
| 20 | $\text{Find }\frac{d}{dx}\left(x^{\frac{2}{3}}\right)$ | $\frac{2}{3}x^{-\frac{1}{3}}$ | `—` | `pack=power_rule · methods=power · form_id=power_poly · shape=power · D=20` |
| 20 | $\text{Find }\frac{d}{dx}\left(3x^{3} + 3x^{2} - 2x - 3\right)$ | $9x^{2} + 6x - 2$ | `—` | `pack=power_rule · methods=power,sum · form_id=power_poly · shape=sum+power · D=20` |
| 25 | $\frac{d}{dx}\left[x^{\frac{1}{2}}\right]$ | $\frac{1}{2}x^{-\frac{1}{2}}$ | `—` | `pack=power_rule · methods=power · form_id=power_poly · shape=power · D=25` |
| 25 | $\text{Find }\frac{d}{dx}\left(2x^{\frac{7}{2}}\right)$ | $7x^{\frac{5}{2}}$ | `—` | `pack=power_rule · methods=power · form_id=power_root · shape=power · D=25` |
| 25 | $\text{Find }\frac{d}{dx}\left(2x^{2} - 5x - 3\right)$ | $4x - 5$ | `—` | `pack=power_rule · methods=power,sum · form_id=power_poly · shape=sum+power · D=25` |

## Precalc PFD (construct_pfd; reverse of rational add)

<a id="pfd"></a>

`pc_partial_fraction_decomposition` · pack `pfd` · topic label: pc: Partial fraction decomposition · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **1** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `partial_fraction_decomposition:pfd` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Decompose } \frac{2x - 1}{x^{2} - 3x + 2}$ | $\frac{-1}{x - 1}+\frac{3}{x - 2}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=0` |
| 0 | $\text{Decompose } \frac{-2x + 8}{x^{2} - 4x + 3}$ | $\frac{-3}{x - 1}+\frac{1}{x - 3}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=0` |
| 0 | $\text{Decompose } \frac{x - 4}{x^{2} - 5x + 6}$ | $\frac{2}{x - 2}+\frac{-1}{x - 3}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=0` |
| 3 | $\text{Decompose } \frac{-2}{x^{2} - x}$ | $\frac{2}{x}+\frac{-2}{x - 1}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=3` |
| 3 | $\text{Decompose } \frac{4x - 6}{x^{2} - 4x + 3}$ | $\frac{1}{x - 1}+\frac{3}{x - 3}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=3` |
| 3 | $\text{Decompose } \frac{2x + 1}{x^{2} - x}$ | $\frac{3}{x - 1}+\frac{-1}{x}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=3` |
| 6 | $\text{Decompose } \frac{10x - 34}{2x^{2} - 16x + 30}$ | $\frac{4}{x - 5}+\frac{1}{x - 3}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=6` |
| 6 | $\text{Decompose } \frac{12}{x^{2} - 3x}$ | $\frac{4}{x - 3}+\frac{-4}{x}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=6` |
| 6 | $\text{Decompose } \frac{9x - 16}{x^{2} - 4x}$ | $\frac{5}{x - 4}+\frac{4}{x}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=6` |
| 8 | $\text{Decompose } \frac{-9x - 6}{3x^{2} - 6x}$ | $\frac{1}{x}+\frac{-4}{x - 2}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=8` |
| 8 | $\text{Decompose } \frac{2x - 3}{x^{2} - 5x + 6}$ | $\frac{3}{x - 3}+\frac{-1}{x - 2}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=8` |
| 8 | $\text{Decompose } \frac{6x - 12}{2x^{2} - 6x}$ | $\frac{1}{x - 3}+\frac{2}{x}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=8` |
| 12 | $\text{Decompose } \frac{6x^{2} + 2x + 2}{2x^{3} - 4x^{2} + 2x - 4}$ | $\frac{3}{x - 2}+\frac{1}{x^{2} + 1}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_irreducible_quadratic · shape=nonrepeated_irreducible_quadratic · D=12` |
| 12 | $\text{Decompose } \frac{4x}{2x^{2} - 16x + 30}$ | $\frac{-3}{x - 3}+\frac{5}{x - 5}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_2 · shape=nonrepeated_linear_2 · D=12` |
| 12 | $\text{Decompose } \frac{6x^{2} - 2x - 18}{\left(x + 2\right)\left(x\right)\left(x - 3\right)}$ | $\frac{1}{x + 2}+\frac{3}{x}+\frac{2}{x - 3}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_3 · shape=nonrepeated_linear_3 · D=12` |
| 16 | $\text{Decompose } \frac{x^{3} - 8x^{2} - 12x - 80}{\left(x - 2\right)\left(x + 2\right)\left(x^{2} + 4\right)}$ | $\frac{-4}{x - 2}+\frac{3}{x + 2}+\frac{2x + 6}{x^{2} + 4}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=mixed_linear_quadratic · shape=mixed_linear_quadratic · D=16` |
| 16 | $\text{Decompose } \frac{-3x^{2} + 7x - 83}{x^{3} - 5x^{2} + 16x - 80}$ | $\frac{-3}{x - 5}+\frac{7}{x^{2} + 16}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_irreducible_quadratic · shape=nonrepeated_irreducible_quadratic · D=16` |
| 16 | $\text{Decompose } \frac{27x^{2} - 414x + 675}{3\left(x - 9\right)\left(x - 1\right)\left(x - 3\right)}$ | $\frac{-6}{x - 9}+\frac{6}{x - 1}+\frac{9}{x - 3}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_3 · shape=nonrepeated_linear_3 · D=16` |
| 20 | $\text{Decompose } \frac{12x^{2} - 15x - 36}{3\left(x - 2\right)\left(x\right)\left(x - 3\right)}$ | $\frac{3}{x - 2}+\frac{-2}{x}+\frac{3}{x - 3}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_3 · shape=nonrepeated_linear_3 · D=20` |
| 20 | $\text{Decompose } \frac{3x^{2} - 7x + 43}{x^{3} + 3x^{2} + 4x + 12}$ | $\frac{7}{x + 3}+\frac{-4x + 5}{x^{2} + 4}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_irreducible_quadratic · shape=nonrepeated_irreducible_quadratic · D=20` |
| 20 | $\text{Decompose } \frac{7x^{2} - 44x + 60}{\left(x\right)\left(x - 4\right)\left(x - 3\right)}$ | $\frac{5}{x}+\frac{-1}{x - 4}+\frac{3}{x - 3}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_linear_3 · shape=nonrepeated_linear_3 · D=20` |
| 25 | $\text{Decompose } \frac{66x^{2} + 12}{3x^{3} + 3x}$ | $\frac{4}{x}+\frac{18x}{x^{2} + 1}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=nonrepeated_irreducible_quadratic · shape=nonrepeated_irreducible_quadratic · D=25` |
| 25 | $\text{Decompose } \frac{x^{3} - 37x^{2} + 4x - 128}{\left(x - 4\right)\left(x + 4\right)\left(x^{2} + 4\right)}$ | $\frac{-4}{x - 4}+\frac{5}{x + 4}+\frac{-1}{x^{2} + 4}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=mixed_linear_quadratic · shape=mixed_linear_quadratic · D=25` |
| 25 | $\text{Decompose } \frac{16x^{3} - 84x^{2} + 274x + 10}{\left(x - 12\right)\left(x + 1\right)\left(x^{2} + 1\right)}$ | $\frac{10}{x - 12}+\frac{14}{x + 1}+\frac{-8x - 14}{x^{2} + 1}$ | `—` | `spec_pack=structured_pfd · methods=partial_fractions,combine · form_id=mixed_linear_quadratic · shape=mixed_linear_quadratic · D=25` |

## Precalc function operations algebraic

<a id="function_ops"></a>

`pc_functions_operations` · pack `function_ops` · topic label: pc: Operations · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **5** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `function_operations:add` | 11 |
| `function_operations:quotient` | 5 |
| `function_operations:compose` | 4 |
| `function_operations:product` | 2 |
| `function_operations:subtract` | 2 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{If } f(x) = 3x + 3 \text{ and } g(x) = 3x - 3, \text{ find } (f + g)(-4).$ | $-24$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_sum · shape=algebraic_sum · D=0` |
| 0 | $\text{If } f(x) = 3x - 4 \text{ and } g(x) = 3x + 4, \text{ find } (f + g)(-3).$ | $-18$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_sum · shape=algebraic_sum · D=0` |
| 0 | $\text{If } f(x) = 3x - 3 \text{ and } g(x) = -3x + 1, \text{ find } (f + g)(-3).$ | $-2$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_sum · shape=algebraic_sum · D=0` |
| 3 | $\text{If } f(x) = 3x + 3 \text{ and } g(x) = 3x - 4, \text{ find } (f + g)(3).$ | $17$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_sum · shape=algebraic_sum · D=3` |
| 3 | $\text{If } f(x) = -3x + 0 \text{ and } g(x) = -3x - 2, \text{ find } (f - g)(-1).$ | $2$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_difference · shape=algebraic_difference · D=3` |
| 3 | $\text{If } f(x) = 3x + 4 \text{ and } g(x) = -3x - 1, \text{ find } (f + g)(-4).$ | $3$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_sum · shape=algebraic_sum · D=3` |
| 6 | $\text{If } f(x) = 6x + 4 \text{ and } g(x) = -6x + 0, \text{ find } (f + g)(3).$ | $4$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_sum · shape=algebraic_sum · D=6` |
| 6 | $\text{If } f(x) = -6x + 7 \text{ and } g(x) = -6x + 8, \text{ find } (f + g)(0).$ | $15$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_sum · shape=algebraic_sum · D=6` |
| 6 | $\text{If } f(x) = 6x - 4 \text{ and } g(x) = -6x + 2, \text{ find } (f \cdot g)(-2).$ | $-224$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_product · shape=algebraic_product · D=6` |
| 8 | $\text{If } f(x) = 6x + 5 \text{ and } g(x) = -6x + 3, \text{ find } \left(\frac{f}{g}\right)(3).$ | $\frac{-23}{15}$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_quotient · shape=algebraic_quotient · D=8` |
| 8 | $\text{If } f(x) = 6x + 6 \text{ and } g(x) = 6x + 2, \text{ find } \left(\frac{f}{g}\right)(4).$ | $\frac{15}{13}$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_quotient · shape=algebraic_quotient · D=8` |
| 8 | $\text{If } f(x) = -6x + 6 \text{ and } g(x) = 6x + 0, \text{ find } (f + g)(-2).$ | $6$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_sum · shape=algebraic_sum · D=8` |
| 12 | $\text{If } f(x) = 8x - 4 \text{ and } g(x) = -8x - 2, \text{ find } (f \cdot g)(-7).$ | $-3240$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_product · shape=algebraic_product · D=12` |
| 12 | $\text{If } f(x) = 8x - 1 \text{ and } g(x) = 8x + 8, \text{ find } (f + g)(6).$ | $103$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_sum · shape=algebraic_sum · D=12` |
| 12 | $\text{If } f(x) = 8x - 8 \text{ and } g(x) = 8x - 4, \text{ find } (f \circ g)(6).$ | $344$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=compose_evaluate · shape=compose_evaluate · D=12` |
| 16 | $\text{If } f(x) = 8x + 6 \text{ and } g(x) = -8x - 5, \text{ find } \left(\frac{f}{g}\right)(-2).$ | $\frac{-10}{11}$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_quotient · shape=algebraic_quotient · D=16` |
| 16 | $\text{If } f(x) = 8x + 3 \text{ and } g(x) = 8x + 0, \text{ find } \left(\frac{f}{g}\right)(-8).$ | $\frac{61}{64}$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_quotient · shape=algebraic_quotient · D=16` |
| 16 | $\text{If } f(x) = 8x + 2 \text{ and } g(x) = 8x - 2, \text{ find } (f \circ g)(4).$ | $242$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=compose_evaluate · shape=compose_evaluate · D=16` |
| 20 | $\text{If } f(x) = -9x - 8 \text{ and } g(x) = 9x + 2, \text{ find } (f \circ g)(-8).$ | $622$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=compose_evaluate · shape=compose_evaluate · D=20` |
| 20 | $\text{If } f(x) = -9x + 3 \text{ and } g(x) = -9x + 2, \text{ find } (f \circ g)(1).$ | $66$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=compose_evaluate · shape=compose_evaluate · D=20` |
| 20 | $\text{If } f(x) = 9x - 5 \text{ and } g(x) = 9x - 5, \text{ find } (f - g)(-9).$ | $0$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_difference · shape=algebraic_difference · D=20` |
| 25 | $\text{If } f(x) = -11x - 1 \text{ and } g(x) = -11x + 2, \text{ find } (f + g)(-10).$ | $221$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_sum · shape=algebraic_sum · D=25` |
| 25 | $\text{If } f(x) = 11x - 4 \text{ and } g(x) = 11x + 11, \text{ find } \left(\frac{f}{g}\right)(-10).$ | $\frac{38}{33}$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_quotient · shape=algebraic_quotient · D=25` |
| 25 | $\text{If } f(x) = -11x + 4 \text{ and } g(x) = 11x - 6, \text{ find } (f + g)(-3).$ | $-2$ | `—` | `spec_pack=structured_function_ops · methods=function_ops · form_id=algebraic_sum · shape=algebraic_sum · D=25` |

## Precalc rational equations

<a id="rational_equations"></a>

`pc_rational_equations` · pack `rational_equations` · topic label: pc: Rational equations · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **0** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `(unlabeled)` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\frac{5}{x} = \frac{1}{4}$ | $x = 20$ | `—` | `pack=rational_equations · D=0` |
| 0 | $\frac{x + 5}{4} = \frac{12}{6}$ | $x = 3$ | `—` | `pack=rational_equations · D=0` |
| 0 | $\frac{5}{x} = \frac{5}{7}$ | $x = 7$ | `—` | `pack=rational_equations · D=0` |
| 3 | $\frac{12}{x} = \frac{3}{2}$ | $x = 8$ | `—` | `pack=rational_equations · D=3` |
| 3 | $\frac{x + 2}{8} = -1$ | $x = -10$ | `—` | `pack=rational_equations · D=3` |
| 3 | $\frac{x + 3}{5} = \frac{-2}{2}$ | $x = -8$ | `—` | `pack=rational_equations · D=3` |
| 6 | $\frac{6}{x - 8} - \frac{4}{x + 4} = -2$ | $x = -1 \text{ or } x = 4$ | `—` | `pack=rational_equations · D=6` |
| 6 | $\frac{-4}{x - 6} - \frac{15}{x - 5} = -4$ | $x = 10$ | `—` | `pack=rational_equations · D=6` |
| 6 | $\frac{-1}{x + 5} + \frac{3}{x + 7} = 4$ | $x = -6$ | `—` | `pack=rational_equations · D=6` |
| 8 | $\frac{3}{x - 9} - \frac{16}{x - 10} = 5$ | $x = 8$ | `—` | `pack=rational_equations · D=8` |
| 8 | $\frac{-6}{x + 3} - \frac{12}{x + 11} = -5$ | $x = -9$ | `—` | `pack=rational_equations · D=8` |
| 8 | $\frac{2}{x - 3} - \frac{4}{x - 4} = -3$ | $x = 5$ | `—` | `pack=rational_equations · D=8` |
| 12 | $\frac{-2}{x + 6} - \frac{10}{x + 3} = 3$ | $x = -8 \text{ or } x = -5$ | `—` | `pack=rational_equations · D=12` |
| 12 | $\frac{5}{x - 8} + \frac{18}{x + 2} = 4$ | $x = 10$ | `—` | `pack=rational_equations · D=12` |
| 12 | $\frac{6}{x + 6} + \frac{15}{x - 11} = 2$ | $x = -4$ | `—` | `pack=rational_equations · D=12` |
| 16 | $\frac{6}{x - 4} + \frac{20}{x + 8} = -1$ | $x = -32 \text{ or } x = 2$ | `—` | `pack=rational_equations · D=16` |
| 16 | $\frac{5}{x - 5} - \frac{12}{x + 1} = 1$ | $x = -10 \text{ or } x = 7$ | `—` | `pack=rational_equations · D=16` |
| 16 | $\frac{2}{x + 8} - \frac{17}{x - 8} = -1$ | $x = -9 \text{ or } x = 24$ | `—` | `pack=rational_equations · D=16` |
| 20 | $\frac{-5}{x + 4} - \frac{16}{x + 7} = -3$ | $x = -5 \text{ or } x = 1$ | `—` | `pack=rational_equations · D=20` |
| 20 | $\frac{-3}{x + 7} - \frac{14}{x + 1} = -5$ | $x = 2$ | `—` | `pack=rational_equations · D=20` |
| 20 | $\frac{-4}{x + 7} - \frac{6}{x + 9} = -2$ | $x = -8 \text{ or } x = -3$ | `—` | `pack=rational_equations · D=20` |
| 25 | $\frac{-4}{x + 1} - \frac{11}{x - 8} = 3$ | $x = -3 \text{ or } x = 5$ | `—` | `pack=rational_equations · D=25` |
| 25 | $\frac{4}{x + 5} + \frac{10}{x - 6} = 3$ | $x = -4$ | `—` | `pack=rational_equations · D=25` |
| 25 | $\frac{4}{x - 2} - \frac{18}{x + 11} = -3$ | $x = -2$ | `—` | `pack=rational_equations · D=25` |

## Precalc simple log equations

<a id="log_equation"></a>

`pc_logarithmic_equations_simple` · pack `log_equation` · topic label: pc: Logarithmic equations, simple · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **0** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `(unlabeled)` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\log_{4}(x) = 5$ | $x = 1024$ | `—` | `pack=log_equation · D=0` |
| 0 | $\log_{2}(x) = 1$ | $x = 2$ | `—` | `pack=log_equation · D=0` |
| 0 | $\log_{5}(x) = 4$ | $x = 625$ | `—` | `pack=log_equation · D=0` |
| 3 | $\log_{5}(x) = 4$ | $x = 625$ | `—` | `pack=log_equation · D=3` |
| 3 | $\log_{5}(x) = 4$ | $x = 625$ | `—` | `pack=log_equation · D=3` |
| 3 | $\log_{5}(x) = 5$ | $x = 3125$ | `—` | `pack=log_equation · D=3` |
| 6 | $\log_{3}(x) = 4$ | $x = 81$ | `—` | `pack=log_equation · D=6` |
| 6 | $\log(x) = 4$ | $x = 10000$ | `—` | `pack=log_equation · D=6` |
| 6 | $\log_{8}(x) = 3$ | $x = 512$ | `—` | `pack=log_equation · D=6` |
| 8 | $\log_{6}(x) = 5$ | $x = 7776$ | `—` | `pack=log_equation · D=8` |
| 8 | $\log_{2}(x) = 1$ | $x = 2$ | `—` | `pack=log_equation · D=8` |
| 8 | $\log_{3}(x) = 4$ | $x = 81$ | `—` | `pack=log_equation · D=8` |
| 12 | $\log_{5}(x) = 4$ | $x = 625$ | `—` | `pack=log_equation · D=12` |
| 12 | $\log_{8}(x) = 5$ | $x = 32768$ | `—` | `pack=log_equation · D=12` |
| 12 | $\log_{2}(x) = 4$ | $x = 16$ | `—` | `pack=log_equation · D=12` |
| 16 | $\log(x) = 2$ | $x = 100$ | `—` | `pack=log_equation · D=16` |
| 16 | $\log_{8}(x) = 2$ | $x = 64$ | `—` | `pack=log_equation · D=16` |
| 16 | $\log_{2}(x) = 4$ | $x = 16$ | `—` | `pack=log_equation · D=16` |
| 20 | $\log_{3}(x) = 2$ | $x = 9$ | `—` | `pack=log_equation · D=20` |
| 20 | $\log_{11}(x) = 3$ | $x = 1331$ | `—` | `pack=log_equation · D=20` |
| 20 | $\log_{10}(x) = 4$ | $x = 10000$ | `—` | `pack=log_equation · D=20` |
| 25 | $\log_{11}(x) = 2$ | $x = 121$ | `—` | `pack=log_equation · D=25` |
| 25 | $\log_{10}(x) = 4$ | $x = 10000$ | `—` | `pack=log_equation · D=25` |
| 25 | $\log_{12}(x) = 3$ | $x = 1728$ | `—` | `pack=log_equation · D=25` |

## Precalc exponential equations requiring logs

<a id="exp_equation_log"></a>

`pc_exponential_equations_requiring_logarithms` · pack `exp_equation_log` · topic label: pc: Exponential equations requiring logarithms · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **1** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `exponential_equation_with_log:exp_needs_logarithm` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $4^{3x} = 64$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=0` |
| 0 | $3^{-x} = 0.037037037037037035$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=0` |
| 0 | $3^{-x} = 0.3333333333333333$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=0` |
| 3 | $4^{3x} = 64$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=3` |
| 3 | $4^{-x} = 0.0625$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=3` |
| 3 | $4^{x} = 64$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=3` |
| 6 | $2^{-x} = 0.125$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=6` |
| 6 | $5^{-3x} = 4.096e-09$ | $x = 4$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=6` |
| 6 | $3^{3x} = 27$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=6` |
| 8 | $6^{2x} = 36$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=8` |
| 8 | $6^{-5x} = 2.1268224907304786e-12$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=8` |
| 8 | $6^{x} = 216$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=8` |
| 12 | $5^{3x} = 125$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=12` |
| 12 | $6^{-4x} = 5.953741807651273e-07$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=12` |
| 12 | $10^{-3x} = 1e-09$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=12` |
| 16 | $5^{-6x} = 6.4e-05$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=16` |
| 16 | $6^{-10x} = 2.7351112277912534e-16$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=16` |
| 16 | $6^{7x} = 6140942214464815497216$ | $x = 4$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=16` |
| 20 | $3^{3x} = 729$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=20` |
| 20 | $7^{4x} = 2401$ | $x = 1$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=20` |
| 20 | $4^{-9x} = 8.077935669463161e-28$ | $x = 5$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=20` |
| 25 | $10^{13x} = 10000000000000000000000000000000000000000000000000000$ | $x = 4$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=25` |
| 25 | $9^{5x} = 205891132094649$ | $x = 3$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=25` |
| 25 | $8^{12x} = 4722366482869645213696$ | $x = 2$ | `—` | `spec_pack=structured_exp_equation · methods=take_log · form_id=exp_needs_logarithm · shape=exp_needs_logarithm · D=25` |
