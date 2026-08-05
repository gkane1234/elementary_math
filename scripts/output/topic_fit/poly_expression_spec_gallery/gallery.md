# ExpressionSpec / constraint-pack gallery (Phases 0–3)

Generated: 2026-07-31T19:01:51.190827+00:00

Live samples via `_generate_for_type` for Spec-driven derivative packs (D = 0, 3, 8, 12, 20, 25; 3 seeds each). No Easy/Medium/Hard band labels — continuous **D=** only.

Open [gallery.html](gallery.html) in a browser for KaTeX (local `_assets/katex`).

- samples ok: **126** · errors: **0**
- inventory: `shape_id`, ops, nest, methods, function_classes, `paren_style` (from pack)

## Structure inventory (all packs)

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **18** · samples: **126**

| Structure / family | Count |
|--------|------:|
| `derivative_trigonometric:chain+power` | 15 |
| `derivative_ln_exp:chain+power` | 13 |
| `derivative_chain_rule:chain+power` | 12 |
| `derivative_product_rule:chain+power+product` | 12 |
| `derivative_general:chain+power` | 9 |
| `derivative_power_rule:power` | 9 |
| `derivative_power_rule:power+sum` | 9 |
| `derivative_inverse_trig:power` | 7 |
| `derivative_chain_rule:chain+power+product` | 6 |
| `derivative_inverse_trig:chain+power` | 6 |
| `derivative_product_rule:power+product` | 6 |
| `derivative_ln_exp:chain+power+product` | 5 |
| `derivative_inverse_trig:power+product` | 4 |
| `derivative_general:chain+power+product` | 3 |
| `derivative_general:power` | 3 |
| `derivative_general:power+sum` | 3 |
| `derivative_trigonometric:chain+power+product` | 3 |
| `derivative_inverse_trig:chain+power+product` | 1 |

## Packs

- [Power rule](#power) — `pack_power_rule`, paren=`minimal`
- [Product rule](#product) — `pack_product_rule`, paren=`minimal`
- [Algebraic chain](#alg_chain) — `pack_algebraic_chain`, paren=`always_powers`
- [Trigonometric](#trig) — `pack_special_atom (trig)`, paren=`minimal`
- [Natural logarithms & exponentials](#ln_exp) — `pack_special_atom (ln/exp)`, paren=`minimal`
- [Inverse trigonometric](#invtrig) — `pack_special_atom (invtrig)`, paren=`minimal`
- [General derivatives](#general) — `pack_general_derivatives`, paren=`minimal`

## Power rule

<a id="power"></a>

`calc_diff_power_rule` · Spec pack `pack_power_rule` · `paren_style=minimal` · topic label: c1: Power Rule

### Structures in this pack

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **18**

| Structure / family | Count |
|--------|------:|
| `derivative_power_rule:power` | 9 |
| `derivative_power_rule:power+sum` | 9 |

| D | Prompt | Answer | shape_id | Inventory |
|--:|--------|--------|----------|-----------|
| 0 | $\frac{d}{dx}\left[-3x^{3}\right]$ | $-9x^{2}$ | `power` | `shape=power · ops=[^] · nest=0 · methods=power · classes=algebraic · paren=minimal · D=0 · terms=1` |
| 0 | $\text{Find }\frac{d}{dx}\left(x^{4}\right)$ | $4x^{3}$ | `power` | `shape=power · ops=[^] · nest=0 · methods=power · classes=algebraic · paren=minimal · D=0 · terms=1` |
| 0 | $\text{Find }\frac{d}{dx}\left(-x^{2}\right)$ | $-2x$ | `power` | `shape=power · ops=[^] · nest=0 · methods=power · classes=algebraic · paren=minimal · D=0 · terms=1` |
| 3 | $\frac{d}{dx}\left[3x^{3} + x^{2} + 3x - 1\right]$ | $9x^{2} + 2x + 3$ | `sum+power` | `shape=sum+power · ops=[+,^,^] · nest=0 · methods=power,sum · classes=algebraic · paren=minimal · D=3 · terms=4` |
| 3 | $\frac{d}{dx}\left[3x^{3} + 2x^{2} - x - 2\right]$ | $9x^{2} + 4x - 1$ | `sum+power` | `shape=sum+power · ops=[+,^,^] · nest=0 · methods=power,sum · classes=algebraic · paren=minimal · D=3 · terms=4` |
| 3 | $\text{Find }\frac{d}{dx}\left(x^{3} + x^{2} + 2x - 3\right)$ | $3x^{2} + 2x + 2$ | `sum+power` | `shape=sum+power · ops=[+,^,^] · nest=0 · methods=power,sum · classes=algebraic · paren=minimal · D=3 · terms=4` |
| 8 | $\frac{d}{dx}\left[4x^{5}\right]$ | $20x^{4}$ | `power` | `shape=power · ops=[^] · nest=0 · methods=power · classes=algebraic · paren=minimal · D=8 · terms=1` |
| 8 | $\text{Find }\frac{d}{dx}\left(x^{\frac{3}{2}}\right)$ | $\frac{3}{2}x^{\frac{1}{2}}$ | `power` | `shape=power · ops=[^] · nest=0 · methods=power · classes=algebraic,roots · paren=minimal · D=8 · terms=1` |
| 8 | $\text{Find }\frac{d}{dx}\left(2x^{3} - 4x^{2} + 4x - 1\right)$ | $6x^{2} - 8x + 4$ | `sum+power` | `shape=sum+power · ops=[+,^,^] · nest=0 · methods=power,sum · classes=algebraic · paren=minimal · D=8 · terms=4` |
| 12 | $\text{Find }\frac{d}{dx}\left(2x^{3} - 4x^{2} - 3x + 2\right)$ | $6x^{2} - 8x - 3$ | `sum+power` | `shape=sum+power · ops=[+,^,^] · nest=0 · methods=power,sum · classes=algebraic · paren=minimal · D=12 · terms=4` |
| 12 | $\text{Find }\frac{d}{dx}\left(x^{\frac{1}{2}}\right)$ | $\frac{1}{2}x^{-\frac{1}{2}}$ | `power` | `shape=power · ops=[^] · nest=0 · methods=power · classes=algebraic,roots · paren=minimal · D=12 · terms=1` |
| 12 | $\text{Find }\frac{d}{dx}\left(2x^{2} + 4x\right)$ | $4x + 4$ | `sum+power` | `shape=sum+power · ops=[+,^] · nest=0 · methods=power,sum · classes=algebraic · paren=minimal · D=12 · terms=2` |
| 20 | $\frac{d}{dx}\left[x^{-\frac{3}{2}}\right]$ | $-\frac{3}{2}x^{-\frac{5}{2}}$ | `power` | `shape=power · ops=[^] · nest=0 · methods=power · classes=algebraic,roots · paren=minimal · D=20 · terms=1` |
| 20 | $\frac{d}{dx}\left[x^{2} + 2x - 2\right]$ | $2x + 2$ | `sum+power` | `shape=sum+power · ops=[+,^] · nest=0 · methods=power,sum · classes=algebraic · paren=minimal · D=20 · terms=3` |
| 20 | $\frac{d^{2}}{dx^{2}}\left[2x^{3} + 3x^{2} + 4x\right]$ | $12x + 6$ | `sum+power` | `shape=sum+power · ops=[+,^,^] · nest=0 · methods=power,sum · classes=algebraic · paren=minimal · D=20 · terms=3` |
| 25 | $\text{Find }\frac{d}{dx}\left(-x^{\pi}\right)$ | $-\pi x^{\pi-1}$ | `power` | `shape=power · ops=[^] · nest=0 · methods=power · classes=algebraic · paren=minimal · D=25 · terms=1` |
| 25 | $\frac{d^{3}}{dx^{3}}\left[x^{3} + 5x^{2} + 4x - 3\right]$ | $6$ | `sum+power` | `shape=sum+power · ops=[+,^,^] · nest=0 · methods=power,sum · classes=algebraic · paren=minimal · D=25 · terms=4` |
| 25 | $\frac{d}{dx}\left[x^{-\frac{3}{2}}\right]$ | $-\frac{3}{2}x^{-\frac{5}{2}}$ | `power` | `shape=power · ops=[^] · nest=0 · methods=power · classes=algebraic,roots · paren=minimal · D=25 · terms=1` |

## Product rule

<a id="product"></a>

`calc_diff_product_rule` · Spec pack `pack_product_rule` · `paren_style=minimal` · topic label: c1: Product Rule

### Structures in this pack

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **18**

| Structure / family | Count |
|--------|------:|
| `derivative_product_rule:chain+power+product` | 12 |
| `derivative_product_rule:power+product` | 6 |

| D | Prompt | Answer | shape_id | Inventory |
|--:|--------|--------|----------|-----------|
| 0 | $\text{Find }\frac{d}{dx}\left(\left(-x^{3}\right)\left(3x\right)\right)$ | $\left(-3x^{2}\right)\left(3x\right)+\left(-x^{3}\right)\left(3\right)$ | `product+power` | `shape=product+power · ops=[*,^] · nest=0 · methods=power,product · classes=algebraic · paren=minimal · D=0 · terms=1 · factors=2` |
| 0 | $\text{Find }\frac{d}{dx}\left(\left(-2x\right)\left(-2x^{4}\right)\right)$ | $\left(-2\right)\left(-2x^{4}\right)+\left(-2x\right)\left(-8x^{3}\right)$ | `product+power` | `shape=product+power · ops=[*,^] · nest=0 · methods=power,product · classes=algebraic · paren=minimal · D=0 · terms=1 · factors=2` |
| 0 | $\frac{d}{dx}\left[x^{2}\left(-2x\right)\right]$ | $2x\left(-2x\right)+x^{2}\left(-2\right)$ | `product+power` | `shape=product+power · ops=[*,^] · nest=0 · methods=power,product · classes=algebraic · paren=minimal · D=0 · terms=1 · factors=2` |
| 3 | $\text{Find }\frac{d}{dx}\left(\left(-2x^{2}\right)\left(2x^{4}\right)\right)$ | $\left(-4x\right)\left(2x^{4}\right)+\left(-2x^{2}\right)\left(8x^{3}\right)$ | `product+power` | `shape=product+power · ops=[*,^,^] · nest=0 · methods=power,product · classes=algebraic · paren=minimal · D=3 · terms=1 · factors=2` |
| 3 | $\text{Find }\frac{d}{dx}\left(3x^{4}\left(x^{3} - x^{2} - x + 2\right)\right)$ | $12x^{3}\left(x^{3} - x^{2} - x + 2\right)+3x^{4}\left(3x^{2} - 2x - 1\right)$ | `product+sum+power` | `shape=product+sum+power · ops=[*,^,+,^,^] · nest=0 · methods=power,product · classes=algebraic · paren=minimal · D=3 · terms=4 · factors=2` |
| 3 | $\text{Find }\frac{d}{dx}\left(\left(3x^{3} - 3x^{2} - 3x - 3\right)\left(2x\right)\right)$ | $\left(9x^{2} - 6x - 3\right)\left(2x\right)+\left(3x^{3} - 3x^{2} - 3x - 3\right)\left(2\right)$ | `product+sum+power` | `shape=product+sum+power · ops=[*,+,^,^] · nest=0 · methods=power,product · classes=algebraic · paren=minimal · D=3 · terms=4 · factors=2` |
| 8 | $\frac{d}{dx}\left[\left(-2x^{4}\right)\cos(5x)\right]$ | $\left(-8x^{3}\right)\cos(5x)+\left(-2x^{4}\right)\left(-5\sin(5x)\right)$ | `fn:cos+product+power` | `shape=fn:cos+product+power · ops=[*,^] · nest=1 · methods=chain,power,product · classes=algebraic,trig · paren=minimal · D=8 · terms=1 · factors=2` |
| 8 | $\frac{d}{dx}\left[\left(-2x^{3}\right)e^{5x - 5}\right]$ | $\left(-6x^{2}\right)e^{5x - 5}+\left(-2x^{3}\right)\left(5e^{5x - 5}\right)$ | `fn:exp+product+sum+power` | `shape=fn:exp+product+sum+power · ops=[*,^,+] · nest=1 · methods=chain,power,product · classes=algebraic,exp · paren=minimal · D=8 · terms=2 · factors=2` |
| 8 | $\frac{d}{dx}\left[\sin(3x)\left(-5x^{4}\right)\right]$ | $3\cos(3x)\left(-5x^{4}\right)+\sin(3x)\left(-20x^{3}\right)$ | `fn:sin+product+power` | `shape=fn:sin+product+power · ops=[*,^] · nest=1 · methods=chain,power,product · classes=algebraic,trig · paren=minimal · D=8 · terms=1 · factors=2` |
| 12 | $\frac{d}{dx}\left[e^{5x - 5}e^{4x - 4}\right]$ | $5e^{5x - 5}e^{4x - 4}+e^{5x - 5}\left(4e^{4x - 4}\right)$ | `fn:exp+product+sum` | `shape=fn:exp+product+sum · ops=[*,+,+] · nest=1 · methods=chain,power,product · classes=algebraic,exp · paren=minimal · D=12 · terms=2 · factors=2` |
| 12 | $\text{Find }\frac{d}{dx}\left(\left(-4x^{3}\right)\ln\left(x + 4\right)\right)$ | $\left(-12x^{2}\right)\ln\left(x + 4\right)+\left(-4x^{3}\right)\frac{1}{x + 4}$ | `fn:ln+product+sum+power` | `shape=fn:ln+product+sum+power · ops=[*,^,+] · nest=1 · methods=chain,power,product · classes=algebraic,log · paren=minimal · D=12 · terms=2 · factors=2` |
| 12 | $\text{Find }\frac{d}{dx}\left(\left(-5x^{4}\right)\ln^{3}(4x)\right)$ | $\left(-20x^{3}\right)\ln^{3}(4x)+\left(-5x^{4}\right)\left(12\ln^{2}(4x)\frac{1}{4x}\right)$ | `fn:ln+fn_power+product+power` | `shape=fn:ln+fn_power+product+power · ops=[*,^,^] · nest=2 · methods=chain,power,product · classes=algebraic,log · paren=minimal · D=12 · terms=1 · factors=2` |
| 20 | $\frac{d}{dx}\left[\left(-2x^{4}\right)\cos^{4}\left(4x - 5\right)\left(2x^{2}\right)\ln^{4}(3x)\right]$ | $-16x^{3}\cos^{4}\left(4x - 5\right)x^{2}\ln^{4}(3x) + 64\cos^{3}\left(4x - 5\right)\sin\left(4x - 5\right)x^{4}x^{2}\ln^{4}(3x) - 8xx^{4}\cos^{4}\left(4x - 5\right)\ln^{4}(3x) - 48\ln^{3}(3x)\frac{1}{3x}x^{4}\cos^{4}\left(4x - 5\right)x^{2}$ | `fn:cos+ln+fn_power+product+sum+power` | `shape=fn:cos+ln+fn_power+product+sum+power · ops=[*,^,^,+,^,^] · nest=2 · methods=chain,power,product · classes=algebraic,log,trig · paren=minimal · D=20 · terms=2 · factors=4` |
| 20 | $\frac{d}{dx}\left[\sin(4x)\left(-2x\right)\left(-4x^{3}\right)e^{e^{e^{4x}}}\right]$ | $32\cos(4x)xx^{3}e^{e^{e^{4x}}} + 8\sin(4x)x^{3}e^{e^{e^{4x}}} + 24x^{2}\sin(4x)xe^{e^{e^{4x}}} + 32e^{e^{e^{4x}}}e^{e^{4x}}e^{4x}\sin(4x)xx^{3}$ | `fn:exp+sin+product+power` | `shape=fn:exp+sin+product+power · ops=[*,^] · nest=3 · methods=chain,power,product · classes=algebraic,exp,trig · paren=minimal · D=20 · terms=1 · factors=4` |
| 20 | $\frac{d}{dx}\left[x^{4}e^{2x - 3}\right]$ | $4x^{3}e^{2x - 3}+x^{4}\left(2e^{2x - 3}\right)$ | `fn:exp+product+sum+power` | `shape=fn:exp+product+sum+power · ops=[*,^,+] · nest=1 · methods=chain,power,product · classes=algebraic,exp · paren=minimal · D=20 · terms=2 · factors=2` |
| 25 | $\text{Find }\frac{d}{dx}\left(\tan\left(\ln\left(\tan\left(x + 6\right)\right)\right)\left(-6x^{2}\right)\sin(2x)\right)$ | $-6\sec^{2}(\ln\left(\tan\left(x + 6\right)\right))\frac{1}{\tan\left(x + 6\right)}\sec^{2}(x + 6)x^{2}\sin(2x) - 12x\tan\left(\ln\left(\tan\left(x + 6\right)\right)\right)\sin(2x) - 12\cos(2x)\tan\left(\ln\left(\tan\left(x + 6\right)\right)\right)x^{2}$ | `fn:ln+sin+tan+product+sum+power` | `shape=fn:ln+sin+tan+product+sum+power · ops=[*,+,^] · nest=3 · methods=chain,power,product · classes=algebraic,log,trig · paren=minimal · D=25 · terms=2 · factors=3` |
| 25 | $\text{Find }\frac{d}{dx}\left(e^{5x + 4}\left(3x^{3}\right)\cos(6x)\ln\left(5x + 6\right)\right)$ | $15e^{5x + 4}x^{3}\cos(6x)\ln\left(5x + 6\right) + 9x^{2}e^{5x + 4}\cos(6x)\ln\left(5x + 6\right) - 18\sin(6x)e^{5x + 4}x^{3}\ln\left(5x + 6\right) + 15\frac{1}{5x + 6}e^{5x + 4}x^{3}\cos(6x)$ | `fn:cos+exp+ln+product+sum+power` | `shape=fn:cos+exp+ln+product+sum+power · ops=[*,+,^,+] · nest=1 · methods=chain,power,product · classes=algebraic,exp,log,trig · paren=minimal · D=25 · terms=2 · factors=4` |
| 25 | $\frac{d}{dx}\left[5x^{2}\tan\left(\ln\left(\cos(6x)\right)\right)\right]$ | $10x\tan\left(\ln\left(\cos(6x)\right)\right)+5x^{2}\left(-6\sec^{2}(\ln\left(\cos(6x)\right))\frac{1}{\cos(6x)}\sin(6x)\right)$ | `fn:cos+ln+tan+product+power` | `shape=fn:cos+ln+tan+product+power · ops=[*,^] · nest=3 · methods=chain,power,product · classes=algebraic,log,trig · paren=minimal · D=25 · terms=1 · factors=2` |

## Algebraic chain

<a id="alg_chain"></a>

`calc_diff_chain_rule` · Spec pack `pack_algebraic_chain` · `paren_style=always_powers` · topic label: c1: Chain Rule

### Structures in this pack

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **18**

| Structure / family | Count |
|--------|------:|
| `derivative_chain_rule:chain+power` | 12 |
| `derivative_chain_rule:chain+power+product` | 6 |

| D | Prompt | Answer | shape_id | Inventory |
|--:|--------|--------|----------|-----------|
| 0 | $\frac{d}{dx}\left[\left(2x + 2\right)^{3}\right]$ | $3\left(2x + 2\right)^{2}\left(2\right)$ | `sum+power` | `shape=sum+power · ops=[^,+] · nest=1 · methods=chain,power · classes=algebraic · paren=always_powers · D=0 · terms=2` |
| 0 | $\frac{d}{dx}\left[\left(x + 3\right)^{2}\right]$ | $2\left(x + 3\right)$ | `sum+power` | `shape=sum+power · ops=[^,+] · nest=1 · methods=chain,power · classes=algebraic · paren=always_powers · D=0 · terms=2` |
| 0 | $\frac{d}{dx}\left[\left(2x + 1\right)^{2}\right]$ | $2\left(2x + 1\right)\left(2\right)$ | `sum+power` | `shape=sum+power · ops=[^,+] · nest=1 · methods=chain,power · classes=algebraic · paren=always_powers · D=0 · terms=2` |
| 3 | $\frac{d}{dx}\left[\left(x^{2} - 1\right)^{2}\right]$ | $2\left(x^{2} - 1\right)\left(2x\right)$ | `sum+power` | `shape=sum+power · ops=[^,+,^] · nest=1 · methods=chain,power · classes=algebraic · paren=always_powers · D=3 · terms=2` |
| 3 | $\text{Find }\frac{d}{dx}\left(\left(2x^{2} - 2\right)^{4}\right)$ | $4\left(2x^{2} - 2\right)^{3}\left(4x\right)$ | `sum+power` | `shape=sum+power · ops=[^,+,^] · nest=1 · methods=chain,power · classes=algebraic · paren=always_powers · D=3 · terms=2` |
| 3 | $\text{Find }\frac{d}{dx}\left(\left(3x^{2} - 2\right)^{2}\right)$ | $2\left(3x^{2} - 2\right)\left(6x\right)$ | `sum+power` | `shape=sum+power · ops=[^,+,^] · nest=1 · methods=chain,power · classes=algebraic · paren=always_powers · D=3 · terms=2` |
| 8 | $\frac{d}{dx}\left[e^{2x + 1}e^{2x + 3}\right]$ | $2e^{2x + 1}e^{2x + 3} + 2e^{2x + 3}e^{2x + 1}$ | `fn:exp+product+sum` | `shape=fn:exp+product+sum · ops=[*,+,+] · nest=1 · methods=chain,power,product · classes=algebraic,exp · paren=always_powers · D=8 · terms=2 · factors=2` |
| 8 | $\frac{d}{dx}\left[e^{3x - 2}\right]$ | $e^{3x - 2}\left(3\right)$ | `fn:exp+sum` | `shape=fn:exp+sum · ops=[+] · nest=1 · methods=chain,power · classes=algebraic,exp · paren=always_powers · D=8 · terms=2` |
| 8 | $\frac{d}{dx}\left[\sqrt{x}\sin(5x)\right]$ | $\frac{1}{2\sqrt{x}}\sin(5x) + 5\cos(5x)\sqrt{x}$ | `fn:sin+sqrt+product` | `shape=fn:sin+sqrt+product · ops=[*] · nest=1 · methods=chain,power,product · classes=algebraic,roots,trig · paren=always_powers · D=8 · terms=1 · factors=2` |
| 12 | $\text{Find }\frac{d}{dx}\left(\sin(3x)\sqrt{9x + 4}\right)$ | $3\cos(3x)\sqrt{9x + 4} + 9\frac{1}{2\sqrt{9x + 4}}\sin(3x)$ | `fn:sin+sqrt+product+sum` | `shape=fn:sin+sqrt+product+sum · ops=[*,+] · nest=1 · methods=chain,power,product · classes=algebraic,roots,trig · paren=always_powers · D=12 · terms=2 · factors=2` |
| 12 | $\frac{d}{dx}\left[\sqrt{4x + 3}\ln\left(4x + 3\right)\right]$ | $4\frac{1}{2\sqrt{4x + 3}}\ln\left(4x + 3\right) + 4\frac{1}{4x + 3}\sqrt{4x + 3}$ | `fn:ln+sqrt+product+sum` | `shape=fn:ln+sqrt+product+sum · ops=[*,+,+] · nest=1 · methods=chain,power,product · classes=algebraic,log,roots · paren=always_powers · D=12 · terms=2 · factors=2` |
| 12 | $\frac{d}{dx}\left[\ln^{3}\left(3x + 3\right)\right]$ | $3\left(\ln\left(3x + 3\right)\right)^{2}\left(\frac{1}{3x + 3}\left(3\right)\right)$ | `fn:ln+fn_power+sum+power` | `shape=fn:ln+fn_power+sum+power · ops=[^,+] · nest=2 · methods=chain,power · classes=algebraic,log · paren=always_powers · D=12 · terms=2` |
| 20 | $\text{Find }\frac{d}{dx}\left(e^{\sin\left(\ln\left(\ln\left(2x\right)\right)\right)}\right)$ | $e^{\sin\left(\ln\left(\ln\left(2x\right)\right)\right)}\cos\left(\ln\left(\ln\left(2x\right)\right)\right)\frac{1}{\ln\left(2x\right)}\frac{1}{2x}\left(2\right)$ | `fn:exp+ln+sin` | `shape=fn:exp+ln+sin · nest=4 · methods=chain,power · classes=algebraic,exp,log,trig · paren=always_powers · D=20 · terms=1` |
| 20 | $\text{Find }\frac{d}{dx}\left(\cos^{2}(3x)\cos^{\frac{1}{2}}(3x)\cos(4x)\cos(4x)\right)$ | $-6\cos(3x)\sin(3x)\cos^{\frac{1}{2}}(3x)\cos(4x)\cos(4x) - 3\frac{1}{2}\cos^{-\frac{1}{2}}(3x)\sin(3x)\cos^{2}(3x)\cos(4x)\cos(4x) - 4\sin(4x)\cos^{2}(3x)\cos^{\frac{1}{2}}(3x)\cos(4x) - 4\sin(4x)\cos^{2}(3x)\cos^{\frac{1}{2}}(3x)\cos(4x)$ | `fn:cos+fn_power+product+power` | `shape=fn:cos+fn_power+product+power · ops=[*,^,^] · nest=2 · methods=chain,power,product · classes=algebraic,roots,trig · paren=always_powers · D=20 · terms=1 · factors=4` |
| 20 | $\frac{d}{dx}\left[\ln^{3}(5x)\right]$ | $3\left(\ln\left(5x\right)\right)^{2}\left(\frac{5}{5x}\right)$ | `fn:ln+fn_power+power` | `shape=fn:ln+fn_power+power · ops=[^] · nest=2 · methods=chain,power · classes=algebraic,log · paren=always_powers · D=20 · terms=1` |
| 25 | $\frac{d}{dx}\left[\cos(3x)\sin(4x)\cos(3x)\ln\left(6x + 4\right)\right]$ | $-3\sin(3x)\sin(4x)\cos(3x)\ln\left(6x + 4\right) + 4\cos(4x)\cos(3x)\cos(3x)\ln\left(6x + 4\right) - 3\sin(3x)\cos(3x)\sin(4x)\ln\left(6x + 4\right) + 6\frac{1}{6x + 4}\cos(3x)\sin(4x)\cos(3x)$ | `fn:cos+ln+sin+product+sum` | `shape=fn:cos+ln+sin+product+sum · ops=[*,+] · nest=1 · methods=chain,power,product · classes=algebraic,log,trig · paren=always_powers · D=25 · terms=2 · factors=4` |
| 25 | $\frac{d}{dx}\left[\left(x^{2} - 5\right)^{\sqrt{3}}\right]$ | $\sqrt{3}\left(x^{2} - 5\right)^{\sqrt{3}-1}\left(2x\right)$ | `sum+power` | `shape=sum+power · ops=[^,+,^] · nest=1 · methods=chain,power · classes=algebraic · paren=always_powers · D=25 · terms=2` |
| 25 | $\text{Find }\frac{d}{dx}\left(\ln^{4}\left(\ln\left(\ln\left(5x - 6\right)\right)\right)\right)$ | $4\left(\ln\left(\ln\left(\ln\left(5x - 6\right)\right)\right)\right)^{3}\left(\frac{1}{\ln\left(\ln\left(5x - 6\right)\right)}\frac{1}{\ln\left(5x - 6\right)}\frac{1}{5x - 6}\left(5\right)\right)$ | `fn:ln+fn_power+sum+power` | `shape=fn:ln+fn_power+sum+power · ops=[^,+] · nest=4 · methods=chain,power · classes=algebraic,log · paren=always_powers · D=25 · terms=2` |

## Trigonometric

<a id="trig"></a>

`calc_diff_trigonometric` · Spec pack `pack_special_atom (trig)` · `paren_style=minimal` · topic label: c1: Trigonometric

### Structures in this pack

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **18**

| Structure / family | Count |
|--------|------:|
| `derivative_trigonometric:chain+power` | 15 |
| `derivative_trigonometric:chain+power+product` | 3 |

| D | Prompt | Answer | shape_id | Inventory |
|--:|--------|--------|----------|-----------|
| 0 | $\frac{d}{dx}\left[\tan(2x)\right]$ | $2\sec^{2}(2x)$ | `fn:tan` | `shape=fn:tan · nest=1 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=0 · terms=1` |
| 0 | $\text{Find }\frac{d}{dx}\left(\tan(3x)\right)$ | $3\sec^{2}(3x)$ | `fn:tan` | `shape=fn:tan · nest=1 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=0 · terms=1` |
| 0 | $\text{Find }\frac{d}{dx}\left(\sin(3x)\right)$ | $3\cos(3x)$ | `fn:sin` | `shape=fn:sin · nest=1 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=0 · terms=1` |
| 3 | $\frac{d}{dx}\left[\cos(2x)\right]$ | $-2\sin(2x)$ | `fn:cos` | `shape=fn:cos · nest=1 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=3 · terms=1` |
| 3 | $\text{Find }\frac{d}{dx}\left(\sin(2x)\right)$ | $2\cos(2x)$ | `fn:sin` | `shape=fn:sin · nest=1 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=3 · terms=1` |
| 3 | $\frac{d}{dx}\left[\cos(3x)\right]$ | $-3\sin(3x)$ | `fn:cos` | `shape=fn:cos · nest=1 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=3 · terms=1` |
| 8 | $\text{Find }\frac{d}{dx}\left(\cos\left(2x + 3\right)\right)$ | $\left(-\sin\left(2x + 3\right)\right)\left(2\right)$ | `fn:cos+sum` | `shape=fn:cos+sum · ops=[+] · nest=1 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=8 · terms=2` |
| 8 | $\text{Find }\frac{d}{dx}\left(\sin(5x)\tan^{2}(2x)\right)$ | $5\cos(5x)\tan^{2}(2x) + 4\tan(2x)\sec^{2}(2x)\sin(5x)$ | `fn:sin+tan+fn_power+product+power` | `shape=fn:sin+tan+fn_power+product+power · ops=[*,^] · nest=2 · methods=chain,power,product · classes=algebraic,trig · paren=minimal · D=8 · terms=1 · factors=2` |
| 8 | $\frac{d}{dx}\left[\tan^{2}(3x)\right]$ | $2\left(\tan(3x)\right)\left(3\sec^{2}(3x)\right)$ | `fn:tan+fn_power+power` | `shape=fn:tan+fn_power+power · ops=[^] · nest=2 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=8 · terms=1` |
| 12 | $\text{Find }\frac{d}{dx}\left(\tan^{2}(3x)\right)$ | $2\left(\tan(3x)\right)\left(3\sec^{2}(3x)\right)$ | `fn:tan+fn_power+power` | `shape=fn:tan+fn_power+power · ops=[^] · nest=2 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=12 · terms=1` |
| 12 | $\text{Find }\frac{d}{dx}\left(\sin(4x)\sin^{2}\left(\sin\left(3x - 5\right)\right)\right)$ | $4\cos(4x)\sin^{2}\left(\sin\left(3x - 5\right)\right) + 6\sin\left(\sin\left(3x - 5\right)\right)\cos\left(\sin\left(3x - 5\right)\right)\cos\left(3x - 5\right)\sin(4x)$ | `fn:sin+fn_power+product+sum+power` | `shape=fn:sin+fn_power+product+sum+power · ops=[*,^,+] · nest=3 · methods=chain,power,product · classes=algebraic,trig · paren=minimal · D=12 · terms=2 · factors=2` |
| 12 | $\text{Find }\frac{d}{dx}\left(\tan^{3}\left(\tan\left(3x + 2\right)\right)\right)$ | $3\left(\tan\left(\tan\left(3x + 2\right)\right)\right)^{2}\left(\sec^{2}(\tan\left(3x + 2\right))\sec^{2}(3x + 2)\left(3\right)\right)$ | `fn:tan+fn_power+sum+power` | `shape=fn:tan+fn_power+sum+power · ops=[^,+] · nest=3 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=12 · terms=2` |
| 20 | $\text{Find }\frac{d}{dx}\left(\sin^{2}(4x)\right)$ | $2\left(\sin(4x)\right)\left(4\cos(4x)\right)$ | `fn:sin+fn_power+power` | `shape=fn:sin+fn_power+power · ops=[^] · nest=2 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=20 · terms=1` |
| 20 | $\frac{d}{dx}\left[\cos^{2}\left(\cos(2x)\right)\right]$ | $2\left(\cos\left(\cos(2x)\right)\right)\left(\left(-\sin\left(\cos(2x)\right)\right)\left(-\sin(2x)\right)\left(2\right)\right)$ | `fn:cos+fn_power+power` | `shape=fn:cos+fn_power+power · ops=[^] · nest=3 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=20 · terms=1` |
| 20 | $\frac{d^{2}}{dx^{2}}\left[\cos\left(\cos(x)\right)\right]$ | $-\cos\left(\cos(x)\right)\sin(x)\sin(x) + \cos(x)\sin\left(\cos(x)\right)$ | `fn:cos` | `shape=fn:cos · nest=1 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=20 · terms=1` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[\cos^{2}(x)\right]$ | $2\sin(x)\sin(x) - 2\cos(x)\cos(x)$ | `fn:cos+fn_power+power` | `shape=fn:cos+fn_power+power · ops=[^] · nest=1 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=25 · terms=1` |
| 25 | $\frac{d}{dx}\left[\cos(2x)\left(2x^{3}\right)\cos^{4}(5x)\cos(5x)\right]$ | $-4\sin(2x)x^{3}\cos^{4}(5x)\cos(5x) + 6x^{2}\cos(2x)\cos^{4}(5x)\cos(5x) - 40\cos^{3}(5x)\sin(5x)\cos(2x)x^{3}\cos(5x) - 10\sin(5x)\cos(2x)x^{3}\cos^{4}(5x)$ | `fn:cos+fn_power+product+power` | `shape=fn:cos+fn_power+product+power · ops=[*,^,^] · nest=2 · methods=chain,power,product · classes=algebraic,trig · paren=minimal · D=25 · terms=1 · factors=4` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[\tan^{2}(x)\right]$ | $2\sec^{2}(x)\sec^{2}(x) + 4\sec^{2}(x)\tan(x)\tan(x)$ | `fn:tan+fn_power+power` | `shape=fn:tan+fn_power+power · ops=[^] · nest=1 · methods=chain,power · classes=algebraic,trig · paren=minimal · D=25 · terms=1` |

## Natural logarithms & exponentials

<a id="ln_exp"></a>

`calc_diff_natural_logarithms_and_exponentials` · Spec pack `pack_special_atom (ln/exp)` · `paren_style=minimal` · topic label: c1: Natural logarithms and exponentials

### Structures in this pack

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **18**

| Structure / family | Count |
|--------|------:|
| `derivative_ln_exp:chain+power` | 13 |
| `derivative_ln_exp:chain+power+product` | 5 |

| D | Prompt | Answer | shape_id | Inventory |
|--:|--------|--------|----------|-----------|
| 0 | $\frac{d}{dx}\left[e^{2x + 2}\right]$ | $e^{2x + 2}\left(2\right)$ | `fn:exp+sum` | `shape=fn:exp+sum · ops=[+] · nest=1 · methods=chain,power · classes=algebraic,exp · paren=minimal · D=0 · terms=2` |
| 0 | $\text{Find }\frac{d}{dx}\left(e^{x + 3}\right)$ | $e^{x + 3}$ | `fn:exp+sum` | `shape=fn:exp+sum · ops=[+] · nest=1 · methods=chain,power · classes=algebraic,exp · paren=minimal · D=0 · terms=2` |
| 0 | $\text{Find }\frac{d}{dx}\left(\ln\left(3x + 3\right)\right)$ | $\frac{1}{3x + 3}\left(3\right)$ | `fn:ln+sum` | `shape=fn:ln+sum · ops=[+] · nest=1 · methods=chain,power · classes=algebraic,log · paren=minimal · D=0 · terms=2` |
| 3 | $\text{Find }\frac{d}{dx}\left(e^{3x + 3}\right)$ | $e^{3x + 3}\left(3\right)$ | `fn:exp+sum` | `shape=fn:exp+sum · ops=[+] · nest=1 · methods=chain,power · classes=algebraic,exp · paren=minimal · D=3 · terms=2` |
| 3 | $\text{Find }\frac{d}{dx}\left(\ln\left(x - 2\right)\right)$ | $\frac{1}{x - 2}$ | `fn:ln+sum` | `shape=fn:ln+sum · ops=[+] · nest=1 · methods=chain,power · classes=algebraic,log · paren=minimal · D=3 · terms=2` |
| 3 | $\text{Find }\frac{d}{dx}\left(e^{x - 1}\right)$ | $e^{x - 1}$ | `fn:exp+sum` | `shape=fn:exp+sum · ops=[+] · nest=1 · methods=chain,power · classes=algebraic,exp · paren=minimal · D=3 · terms=2` |
| 8 | $\frac{d}{dx}\left[e^{4x + 3}\ln^{2}(4x)\right]$ | $4e^{4x + 3}\ln^{2}(4x) + 8\ln\left(4x\right)\frac{1}{4x}e^{4x + 3}$ | `fn:exp+ln+fn_power+product+sum+power` | `shape=fn:exp+ln+fn_power+product+sum+power · ops=[*,+,^] · nest=2 · methods=chain,power,product · classes=algebraic,exp,log · paren=minimal · D=8 · terms=2 · factors=2` |
| 8 | $\frac{d}{dx}\left[e^{x - 5}\ln\left(5x - 2\right)\right]$ | $e^{x - 5}\ln\left(5x - 2\right) + 5\frac{1}{5x - 2}e^{x - 5}$ | `fn:exp+ln+product+sum` | `shape=fn:exp+ln+product+sum · ops=[*,+,+] · nest=1 · methods=chain,power,product · classes=algebraic,exp,log · paren=minimal · D=8 · terms=2 · factors=2` |
| 8 | $\text{Find }\frac{d}{dx}\left(e^{5x + 2}e^{3x - 3}\right)$ | $5e^{5x + 2}e^{3x - 3} + 3e^{3x - 3}e^{5x + 2}$ | `fn:exp+product+sum` | `shape=fn:exp+product+sum · ops=[*,+,+] · nest=1 · methods=chain,power,product · classes=algebraic,exp · paren=minimal · D=8 · terms=2 · factors=2` |
| 12 | $\text{Find }\frac{d}{dx}\left(e^{5x + 3}\right)$ | $e^{5x + 3}\left(5\right)$ | `fn:exp+sum` | `shape=fn:exp+sum · ops=[+] · nest=1 · methods=chain,power · classes=algebraic,exp · paren=minimal · D=12 · terms=2` |
| 12 | $\text{Find }\frac{d}{dx}\left(\ln^{3}(4x)\right)$ | $3\left(\ln\left(4x\right)\right)^{2}\left(\frac{4}{4x}\right)$ | `fn:ln+fn_power+power` | `shape=fn:ln+fn_power+power · ops=[^] · nest=2 · methods=chain,power · classes=algebraic,log · paren=minimal · D=12 · terms=1` |
| 12 | $\text{Find }\frac{d}{dx}\left(\ln^{2}(x)\right)$ | $2\left(\ln(x)\right)\left(\frac{1}{x}\right)$ | `fn:ln+fn_power+power` | `shape=fn:ln+fn_power+power · ops=[^] · nest=1 · methods=chain,power · classes=algebraic,log · paren=minimal · D=12 · terms=1` |
| 20 | $\frac{d^{2}}{dx^{2}}\left[\ln^{2}(x)\right]$ | $2x^{-1}x^{-1} - 2x^{-2}\ln(x)$ | `fn:ln+fn_power+power` | `shape=fn:ln+fn_power+power · ops=[^] · nest=1 · methods=chain,power · classes=algebraic,log · paren=minimal · D=20 · terms=1` |
| 20 | $\frac{d}{dx}\left[\ln^{4}\left(\ln\left(\ln\left(3x\right)\right)\right)\right]$ | $4\left(\ln\left(\ln\left(\ln\left(3x\right)\right)\right)\right)^{3}\left(\frac{1}{\ln\left(\ln\left(3x\right)\right)}\frac{1}{\ln\left(3x\right)}\frac{1}{3x}\left(3\right)\right)$ | `fn:ln+fn_power+power` | `shape=fn:ln+fn_power+power · ops=[^] · nest=4 · methods=chain,power · classes=algebraic,log · paren=minimal · D=20 · terms=1` |
| 20 | $\frac{d}{dx}\left[\ln^{4}(x)\right]$ | $4\left(\ln(x)\right)^{3}\left(\frac{1}{x}\right)$ | `fn:ln+fn_power+power` | `shape=fn:ln+fn_power+power · ops=[^] · nest=1 · methods=chain,power · classes=algebraic,log · paren=minimal · D=20 · terms=1` |
| 25 | $\text{Find }\frac{d}{dx}\left(\ln\left(6x - 5\right)\ln^{2}(x)\left(-4x^{2}\right)\ln^{2}\left(3x + 3\right)\right)$ | $-24\frac{1}{6x - 5}\ln^{2}(x)x^{2}\ln^{2}\left(3x + 3\right) - 8\ln(x)x^{-1}\ln\left(6x - 5\right)x^{2}\ln^{2}\left(3x + 3\right) - 8x\ln\left(6x - 5\right)\ln^{2}(x)\ln^{2}\left(3x + 3\right) - 24\ln\left(3x + 3\right)\frac{1}{3x + 3}\ln\left(6x - 5\right)\ln^{2}(x)x^{2}$ | `fn:ln+fn_power+product+sum+power` | `shape=fn:ln+fn_power+product+sum+power · ops=[*,+,^,^,^,+] · nest=2 · methods=chain,power,product · classes=algebraic,log · paren=minimal · D=25 · terms=2 · factors=4` |
| 25 | $\frac{d}{dx}\left[\ln^{2}(4x)\right]$ | $2\left(\ln\left(4x\right)\right)\left(\frac{4}{4x}\right)$ | `fn:ln+fn_power+power` | `shape=fn:ln+fn_power+power · ops=[^] · nest=2 · methods=chain,power · classes=algebraic,log · paren=minimal · D=25 · terms=1` |
| 25 | $\frac{d}{dx}\left[\ln^{2}\left(\ln\left(\ln\left(6x\right)\right)\right)\ln\left(2x - 6\right)\left(5x\right)\right]$ | $60\ln\left(\ln\left(\ln\left(6x\right)\right)\right)\frac{1}{\ln\left(\ln\left(6x\right)\right)}\frac{1}{\ln\left(6x\right)}\frac{1}{6x}\ln\left(2x - 6\right)x + 10\frac{1}{2x - 6}\ln^{2}\left(\ln\left(\ln\left(6x\right)\right)\right)x + 5\ln^{2}\left(\ln\left(\ln\left(6x\right)\right)\right)\ln\left(2x - 6\right)$ | `fn:ln+fn_power+product+sum+power` | `shape=fn:ln+fn_power+product+sum+power · ops=[*,^,+] · nest=4 · methods=chain,power,product · classes=algebraic,log · paren=minimal · D=25 · terms=2 · factors=3` |

## Inverse trigonometric

<a id="invtrig"></a>

`calc_diff_inverse_trigonometric` · Spec pack `pack_special_atom (invtrig)` · `paren_style=minimal` · topic label: c1: Inverse trigonometric

### Structures in this pack

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **4** · samples: **18**

| Structure / family | Count |
|--------|------:|
| `derivative_inverse_trig:power` | 7 |
| `derivative_inverse_trig:chain+power` | 6 |
| `derivative_inverse_trig:power+product` | 4 |
| `derivative_inverse_trig:chain+power+product` | 1 |

| D | Prompt | Answer | shape_id | Inventory |
|--:|--------|--------|----------|-----------|
| 0 | $\text{Find }\frac{d}{dx}\left(\arcsin(x)\right)$ | $\frac{1}{\sqrt{1-x^{2}}}$ | `fn:arcsin` | `shape=fn:arcsin · nest=0 · methods=power · classes=invtrig · paren=minimal · D=0 · terms=1` |
| 0 | $\frac{d}{dx}\left[\arccos(x)\right]$ | $-\frac{1}{\sqrt{1-x^{2}}}$ | `fn:arccos` | `shape=fn:arccos · nest=0 · methods=power · classes=invtrig · paren=minimal · D=0 · terms=1` |
| 0 | $\frac{d}{dx}\left[\arccos(x)\right]$ | $-\frac{1}{\sqrt{1-x^{2}}}$ | `fn:arccos` | `shape=fn:arccos · nest=0 · methods=power · classes=invtrig · paren=minimal · D=0 · terms=1` |
| 3 | $\text{Find }\frac{d}{dx}\left(\arctan(x)\right)$ | $\frac{1}{1+x^{2}}$ | `fn:arctan` | `shape=fn:arctan · nest=0 · methods=power · classes=invtrig · paren=minimal · D=3 · terms=1` |
| 3 | $\frac{d}{dx}\left[\arcsin(x)\right]$ | $\frac{1}{\sqrt{1-x^{2}}}$ | `fn:arcsin` | `shape=fn:arcsin · nest=0 · methods=power · classes=invtrig · paren=minimal · D=3 · terms=1` |
| 3 | $\text{Find }\frac{d}{dx}\left(\arcsin(x)\right)$ | $\frac{1}{\sqrt{1-x^{2}}}$ | `fn:arcsin` | `shape=fn:arcsin · nest=0 · methods=power · classes=invtrig · paren=minimal · D=3 · terms=1` |
| 8 | $\frac{d}{dx}\left[\arctan(x)\arctan(x)\right]$ | $\frac{1}{1+(x)^{2}}\arctan(x) + \frac{1}{1+(x)^{2}}\arctan(x)$ | `fn:arctan+product` | `shape=fn:arctan+product · ops=[*] · nest=0 · methods=power,product · classes=algebraic,invtrig · paren=minimal · D=8 · terms=1 · factors=2` |
| 8 | $\text{Find }\frac{d}{dx}\left(\arctan(x)\arctan(x)\right)$ | $\frac{1}{1+(x)^{2}}\arctan(x) + \frac{1}{1+(x)^{2}}\arctan(x)$ | `fn:arctan+product` | `shape=fn:arctan+product · ops=[*] · nest=0 · methods=power,product · classes=algebraic,invtrig · paren=minimal · D=8 · terms=1 · factors=2` |
| 8 | $\text{Find }\frac{d}{dx}\left(\arccos(x)\arctan(x)\right)$ | $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arctan(x) + \frac{1}{1+(x)^{2}}\arccos(x)$ | `fn:arccos+arctan+product` | `shape=fn:arccos+arctan+product · ops=[*] · nest=0 · methods=power,product · classes=algebraic,invtrig · paren=minimal · D=8 · terms=1 · factors=2` |
| 12 | $\frac{d}{dx}\left[\arctan(x)\arcsin(x)\right]$ | $\frac{1}{1+(x)^{2}}\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arctan(x)$ | `fn:arcsin+arctan+product` | `shape=fn:arcsin+arctan+product · ops=[*] · nest=0 · methods=power,product · classes=algebraic,invtrig · paren=minimal · D=12 · terms=1 · factors=2` |
| 12 | $\text{Find }\frac{d}{dx}\left(\arcsin^{3}(3x)\right)$ | $3\left(\arcsin(3x)\right)^{2}\left(\frac{3}{\sqrt{1-(3x)^{2}}}\right)$ | `fn:arcsin+fn_power+power` | `shape=fn:arcsin+fn_power+power · ops=[^] · nest=2 · methods=chain,power · classes=algebraic,invtrig · paren=minimal · D=12 · terms=1` |
| 12 | $\frac{d}{dx}\left[\arctan^{3}(5x)\right]$ | $3\left(\arctan(5x)\right)^{2}\left(\frac{5}{1+(5x)^{2}}\right)$ | `fn:arctan+fn_power+power` | `shape=fn:arctan+fn_power+power · ops=[^] · nest=2 · methods=chain,power · classes=algebraic,invtrig · paren=minimal · D=12 · terms=1` |
| 20 | $\frac{d}{dx}\left[\arcsin(x)\arccos(x)\left(-4x^{2}\right)\arccos^{2}(4x)\right]$ | $-4\frac{1}{\sqrt{1-(x)^{2}}}\arccos(x)x^{2}\arccos^{2}(4x) - 4\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x)x^{2}\arccos^{2}(4x) - 8x\arcsin(x)\arccos(x)\arccos^{2}(4x) - 32\arccos(4x)\left(-\frac{1}{\sqrt{1-(4x)^{2}}}\right)\arcsin(x)\arccos(x)x^{2}$ | `fn:arccos+arcsin+fn_power+product+power` | `shape=fn:arccos+arcsin+fn_power+product+power · ops=[*,^,^] · nest=2 · methods=chain,power,product · classes=algebraic,invtrig · paren=minimal · D=20 · terms=1 · factors=4` |
| 20 | $\text{Find }\frac{d}{dx}\left(\arctan\left(\arcsin\left(\arccos(2x)\right)\right)\right)$ | $\frac{1}{1+(\arcsin\left(\arccos(2x)\right))^{2}}\frac{1}{\sqrt{1-(\arccos(2x))^{2}}}\left(-\frac{1}{\sqrt{1-(2x)^{2}}}\right)\left(2\right)$ | `fn:arccos+arcsin+arctan` | `shape=fn:arccos+arcsin+arctan · nest=3 · methods=chain,power · classes=algebraic,invtrig · paren=minimal · D=20 · terms=1` |
| 20 | $\frac{d}{dx}\left[\arcsin\left(\arcsin(2x)\right)\right]$ | $\frac{1}{\sqrt{1-(\arcsin(2x))^{2}}}\frac{1}{\sqrt{1-(2x)^{2}}}\left(2\right)$ | `fn:arcsin` | `shape=fn:arcsin · nest=2 · methods=chain,power · classes=algebraic,invtrig · paren=minimal · D=20 · terms=1` |
| 25 | $\frac{d^{3}}{dx^{3}}\left[\arccos(x)\right]$ | $-\left(-x^{2} + 1\right)^{-\frac{3}{2}} + 2\cdot\left(-\frac{3}{2}\left(-x^{2} + 1\right)^{-\frac{5}{2}}xx\right)$ | `fn:arccos` | `shape=fn:arccos · nest=0 · methods=power · classes=invtrig · paren=minimal · D=25 · terms=1` |
| 25 | $\frac{d^{3}}{dx^{3}}\left[\arcsin(3x)\right]$ | $27\left(1 - \left(3x\right)^{2}\right)^{-\frac{3}{2}} - 486\cdot\left(-\frac{3}{2}\left(1 - \left(3x\right)^{2}\right)^{-\frac{5}{2}}xx\right)$ | `fn:arcsin` | `shape=fn:arcsin · nest=1 · methods=chain,power · classes=algebraic,invtrig · paren=minimal · D=25 · terms=1` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[\arcsin^{2}(x)\right]$ | $2\frac{1}{\sqrt{1-(x)^{2}}}\frac{1}{\sqrt{1-(x)^{2}}} + 2x\left(-x^{2} + 1\right)^{-\frac{3}{2}}\arcsin(x)$ | `fn:arcsin+fn_power+power` | `shape=fn:arcsin+fn_power+power · ops=[^] · nest=1 · methods=chain,power · classes=algebraic,invtrig · paren=minimal · D=25 · terms=1` |

## General derivatives

<a id="general"></a>

`calc_diff_general` · Spec pack `pack_general_derivatives` · `paren_style=minimal` · topic label: c1: General derivatives

### Structures in this pack

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **4** · samples: **18**

| Structure / family | Count |
|--------|------:|
| `derivative_general:chain+power` | 9 |
| `derivative_general:chain+power+product` | 3 |
| `derivative_general:power` | 3 |
| `derivative_general:power+sum` | 3 |

| D | Prompt | Answer | shape_id | Inventory |
|--:|--------|--------|----------|-----------|
| 0 | $\frac{d}{dx}\left[-x^{3}\right]$ | $-3x^{2}$ | `power` | `shape=power · ops=[^] · nest=0 · methods=power · classes=algebraic · paren=minimal · D=0 · terms=1` |
| 0 | $\frac{d}{dx}\left[x^{3} - x^{2}\right]$ | $3x^{2} - 2x$ | `sum+power` | `shape=sum+power · ops=[+,^,^] · nest=0 · methods=power,sum · classes=algebraic · paren=minimal · D=0 · terms=2` |
| 0 | $\frac{d}{dx}\left[x^{4}\right]$ | $4x^{3}$ | `power` | `shape=power · ops=[^] · nest=0 · methods=power · classes=algebraic · paren=minimal · D=0 · terms=1` |
| 3 | $\frac{d}{dx}\left[2x^{2} - 3x + 2\right]$ | $4x - 3$ | `sum+power` | `shape=sum+power · ops=[+,^] · nest=0 · methods=power,sum · classes=algebraic · paren=minimal · D=3 · terms=3` |
| 3 | $\text{Find }\frac{d}{dx}\left(3x^{3}\right)$ | $9x^{2}$ | `power` | `shape=power · ops=[^] · nest=0 · methods=power · classes=algebraic · paren=minimal · D=3 · terms=1` |
| 3 | $\text{Find }\frac{d}{dx}\left(2x^{3} - x^{2} - 2x - 2\right)$ | $6x^{2} - 2x - 2$ | `sum+power` | `shape=sum+power · ops=[+,^,^] · nest=0 · methods=power,sum · classes=algebraic · paren=minimal · D=3 · terms=4` |
| 8 | $\frac{d}{dx}\left[e^{\sqrt{4x + 5}}\right]$ | $e^{\sqrt{4x + 5}}\frac{1}{2\sqrt{4x + 5}}\left(4\right)$ | `fn:exp+sqrt+sum` | `shape=fn:exp+sqrt+sum · ops=[+] · nest=2 · methods=chain,power · classes=algebraic,exp,roots · paren=minimal · D=8 · terms=2` |
| 8 | $\text{Find }\frac{d}{dx}\left(\ln^{2}(x)\right)$ | $2\left(\ln(x)\right)\left(\frac{1}{x}\right)$ | `fn:ln+fn_power+power` | `shape=fn:ln+fn_power+power · ops=[^] · nest=1 · methods=chain,power · classes=algebraic,log · paren=minimal · D=8 · terms=1` |
| 8 | $\text{Find }\frac{d}{dx}\left(\ln^{3}(x)\right)$ | $3\left(\ln(x)\right)^{2}\left(\frac{1}{x}\right)$ | `fn:ln+fn_power+power` | `shape=fn:ln+fn_power+power · ops=[^] · nest=1 · methods=chain,power · classes=algebraic,log · paren=minimal · D=8 · terms=1` |
| 12 | $\text{Find }\frac{d}{dx}\left(e^{3x + 2}\right)$ | $e^{3x + 2}\left(3\right)$ | `fn:exp+sum` | `shape=fn:exp+sum · ops=[+] · nest=1 · methods=chain,power · classes=algebraic,exp · paren=minimal · D=12 · terms=2` |
| 12 | $\frac{d^{2}}{dx^{2}}\left[e^{e^{x - 1}}\right]$ | $e^{e^{x - 1}}e^{x - 1}e^{x - 1} + e^{x - 1}e^{e^{x - 1}}$ | `fn:exp+sum` | `shape=fn:exp+sum · ops=[+] · nest=2 · methods=chain,power · classes=algebraic,exp · paren=minimal · D=12 · terms=2` |
| 12 | $\frac{d}{dx}\left[\arcsin^{2}(5x)\right]$ | $2\left(\arcsin(5x)\right)\left(\frac{5}{\sqrt{1-(5x)^{2}}}\right)$ | `fn:arcsin+fn_power+power` | `shape=fn:arcsin+fn_power+power · ops=[^] · nest=2 · methods=chain,power · classes=algebraic,invtrig · paren=minimal · D=12 · terms=1` |
| 20 | $\text{Find }\frac{d}{dx}\left(\arctan^{2}(5x)\right)$ | $2\left(\arctan(5x)\right)\left(\frac{5}{1+(5x)^{2}}\right)$ | `fn:arctan+fn_power+power` | `shape=fn:arctan+fn_power+power · ops=[^] · nest=2 · methods=chain,power · classes=algebraic,invtrig · paren=minimal · D=20 · terms=1` |
| 20 | $\frac{d^{2}}{dx^{2}}\left[\cos(5x)\arccos(x)\right]$ | $-25\cos(5x)\arccos(x) - 5\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sin(5x) - x\left(-x^{2} + 1\right)^{-\frac{3}{2}}\cos(5x) - 5\sin(5x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)$ | `fn:arccos+cos+product` | `shape=fn:arccos+cos+product · ops=[*] · nest=1 · methods=chain,power,product · classes=algebraic,invtrig,trig · paren=minimal · D=20 · terms=1 · factors=2` |
| 20 | $\frac{d}{dx}\left[\arctan^{2}(4x)x^{4}\sqrt{e^{2x + 2}}e^{e^{x^{3}}}\right]$ | $8\arctan(4x)\frac{1}{1+(4x)^{2}}x^{4}\sqrt{e^{2x + 2}}e^{e^{x^{3}}} + 4x^{3}\arctan^{2}(4x)\sqrt{e^{2x + 2}}e^{e^{x^{3}}} + 2\frac{1}{2\sqrt{e^{2x + 2}}}e^{2x + 2}\arctan^{2}(4x)x^{4}e^{e^{x^{3}}} + 3e^{e^{x^{3}}}e^{x^{3}}x^{2}\arctan^{2}(4x)x^{4}\sqrt{e^{2x + 2}}$ | `fn:arctan+exp+sqrt+fn_power+product+sum+power` | `shape=fn:arctan+exp+sqrt+fn_power+product+sum+power · ops=[*,^,^,+,^] · nest=2 · methods=chain,power,product · classes=algebraic,exp,invtrig,roots · paren=minimal · D=20 · terms=2 · factors=4` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[e^{5x + 3}\right]$ | $25e^{5x + 3}$ | `fn:exp+sum` | `shape=fn:exp+sum · ops=[+] · nest=1 · methods=chain,power · classes=algebraic,exp · paren=minimal · D=25 · terms=2` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[\tan\left(\arcsin(x)\right)\right]$ | $2\sec^{2}(\arcsin(x))\tan\left(\arcsin(x)\right)\frac{1}{\sqrt{1-(x)^{2}}}\frac{1}{\sqrt{1-(x)^{2}}} + x\left(-x^{2} + 1\right)^{-\frac{3}{2}}\sec^{2}(\arcsin(x))$ | `fn:arcsin+tan` | `shape=fn:arcsin+tan · nest=1 · methods=chain,power · classes=algebraic,invtrig,trig · paren=minimal · D=25 · terms=1` |
| 25 | $\frac{d}{dx}\left[\arctan^{3}(x)\arctan^{4}(3x)\right]$ | $3\arctan^{2}(x)\frac{1}{1+(x)^{2}}\arctan^{4}(3x) + 12\arctan^{3}(3x)\frac{1}{1+(3x)^{2}}\arctan^{3}(x)$ | `fn:arctan+fn_power+product+power` | `shape=fn:arctan+fn_power+product+power · ops=[*,^,^] · nest=2 · methods=chain,power,product · classes=algebraic,invtrig · paren=minimal · D=25 · terms=1 · factors=2` |
