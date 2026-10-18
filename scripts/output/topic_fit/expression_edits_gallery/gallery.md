# Expression edits gallery

Unseeded draws at difficulty 6, with the edit cap the preview sends (`edit_max` 3).
Each card is one regenerate: the form seed, the coefficient seed, and the edit seed are fresh.

**Generated:** 2026-10-18 17:40 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

## Power Rule

Generator `derivative_power_rule`.

### Power Rule · 1

- Edits: `none`
- Prompt: $\frac{d}{dx}\left[x^{\frac{3}{2}}\right]$
- Answer: $\frac{3}{2}x^{\frac{1}{2}}$

### Power Rule · 2

- Edits: `multiply_sum_unexpanded(-3)`
- Prompt: $\frac{d}{dx}\left[-3\cdot\left(-5x^{2} - x - 1\right)\right]$
- Answer: $-3\cdot\left(-10x - 1\right)$

### Power Rule · 3

- Edits: `none`
- Prompt: $\frac{d}{dx}\left[x^{-3}\right]$
- Answer: $-3x^{-4}$

### Power Rule · 4

- Edits: `negate`
- Prompt: $\frac{d}{dx}\left[-5x^{\frac{1}{3}}\right]$
- Answer: $-\frac{5}{3}x^{-\frac{2}{3}}$

### Power Rule · 5

- Edits: `multiply_sum_unexpanded(3)`
- Prompt: $\text{Find }\frac{d}{dx}\left(3\left(2x^{2} - 5x - 1\right)\right)$
- Answer: $3\left(4x - 5\right)$

### Power Rule · 6

- Edits: `none`
- Prompt: $\text{Find }\frac{d}{dx}\left(-2x^{\frac{5}{3}}\right)$
- Answer: $-\frac{10}{3}x^{\frac{2}{3}}$

## Higher order derivatives

Generator `derivative_higher_order`.

### Higher order derivatives · 1

- Edits: `none`
- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(2x^{3} + 5\right)^{2}\right]$
- Answer: $72x^{2}x^{2} + 24x\left(2x^{3} + 5\right)$

### Higher order derivatives · 2

- Edits: `multiply_sum_unexpanded(2)`
- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(2\cdot\left(-x - 5\right)\right)^{3}\right]$
- Answer: $48\cdot\left(-x - 5\right)$

### Higher order derivatives · 3

- Edits: `none`
- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(-x^{2} + 3\right)^{3}\right]$
- Answer: $24\left(-x^{2} + 3\right)xx - 6\left(-x^{2} + 3\right)^{2}$

### Higher order derivatives · 4

- Edits: `none`
- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(2x^{3} + 3x^{2} - 4x - 3\right)^{3}\right]$
- Answer: $6\left(2x^{3} + 3x^{2} - 4x - 3\right)\left(6x^{2} + 6x - 4\right)\left(6x^{2} + 6x - 4\right) + 3\left(12x + 6\right)\left(2x^{3} + 3x^{2} - 4x - 3\right)^{2}$

### Higher order derivatives · 5

- Edits: `negate`
- Prompt: $\frac{d^{2}}{dx^{2}}\left[-5\left(-2x - 3\right)^{2}\right]$
- Answer: $-40$

### Higher order derivatives · 6

- Edits: `multiply_sum_unexpanded(4)`
- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(4\left(3x^{2} - 4x + 5\right)\right)^{2}\right]$
- Answer: $32\left(6x - 4\right)\left(6x - 4\right) + 192\left(3x^{2} - 4x + 5\right)$

## Product Rule

Generator `derivative_product_rule`.

### Product Rule · 1

- Edits: `none`
- Prompt: $\text{Find }\frac{d}{dx}\left(\left(-x^{2} - 5x\right)\left(-2x - 2\right)\right)$
- Answer: $\left(-2x - 5\right)\left(-2x - 2\right) - 2\cdot\left(-x^{2} - 5x\right)$

### Product Rule · 2

- Edits: `negate, multiply_sum_unexpanded(4)`
- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(2x + 1\right)\left(4\right)\left(-3x + 4\right)\right)$
- Answer: $-8\cdot\left(-3x + 4\right) + 12\left(2x + 1\right)$

### Product Rule · 3

- Edits: `factor_common_sum, multiply_outside(-4)`
- Prompt: $\frac{d}{dx}\left[-4\left(3x - 3\right)\left(4\cdot\left(-x + 1\right)\right)^{3}\right]$
- Answer: $-12\left(4\cdot\left(-x + 1\right)\right)^{3} + 48\left(4\cdot\left(-x + 1\right)\right)^{2}\left(3x - 3\right)$

### Product Rule · 4

- Edits: `multiply_sum_unexpanded(-4)`
- Prompt: $\frac{d}{dx}\left[-4\left(-x^{2} + 4x - 2\right)\left(3x + 2\right)^{3}\right]$
- Answer: $-4\left(-2x + 4\right)\left(3x + 2\right)^{3} - 36\left(3x + 2\right)^{2}\left(-x^{2} + 4x - 2\right)$

### Product Rule · 5

- Edits: `factor_common_sum`
- Prompt: $\text{Find }\frac{d}{dx}\left(5\left(x + 1\right)\left(-x - 2\right)^{3}\right)$
- Answer: $5\left(-x - 2\right)^{3} - 15\left(-x - 2\right)^{2}\left(x + 1\right)$

### Product Rule · 6

- Edits: `negate, factor_common_sum`
- Prompt: $\frac{d}{dx}\left[-4x\left(2\left(x + 2\right)\right)^{3}\right]$
- Answer: $-4\left(2\left(x + 2\right)\right)^{3} - 24\left(2\left(x + 2\right)\right)^{2}x$

## Quotient Rule

Generator `derivative_quotient_rule`.

### Quotient Rule · 1

- Edits: `none`
- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{-4x^{3} - 5x^{2} + x - 2}{-5x^{3} - 2}\right)$
- Answer: $\frac{\left(-12x^{2} - 10x + 1\right)\left(-5x^{3} - 2\right)-\left(-4x^{3} - 5x^{2} + x - 2\right)\left(-15x^{2}\right)}{\left(-5x^{3} - 2\right)^{2}}$

### Quotient Rule · 2

- Edits: `multiply_sum_unexpanded(4)`
- Prompt: $\frac{d}{dx}\left[\frac{x - 4}{4\cdot\left(-3x - 4\right)}\right]$
- Answer: $\frac{\left(1\right)\left(4\cdot\left(-3x - 4\right)\right)-\left(x - 4\right)\left(-12\right)}{\left(4\cdot\left(-3x - 4\right)\right)^{2}}$

### Quotient Rule · 3

- Edits: `none`
- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{-4x^{3} + 4x^{2} + 4x - 3}{-2x^{2} - 2x + 1}\right)$
- Answer: $\frac{\left(-12x^{2} + 8x + 4\right)\left(-2x^{2} - 2x + 1\right)-\left(-4x^{3} + 4x^{2} + 4x - 3\right)\left(-4x - 2\right)}{\left(-2x^{2} - 2x + 1\right)^{2}}$

### Quotient Rule · 4

- Edits: `none`
- Prompt: $\frac{d}{dx}\left[\frac{-5x - 1}{-3x^{3} - 5x^{2} + 2x + 3}\right]$
- Answer: $\frac{\left(-5\right)\left(-3x^{3} - 5x^{2} + 2x + 3\right)-\left(-5x - 1\right)\left(-9x^{2} - 10x + 2\right)}{\left(-3x^{3} - 5x^{2} + 2x + 3\right)^{2}}$

### Quotient Rule · 5

- Edits: `multiply_sum_unexpanded(4)`
- Prompt: $\frac{d}{dx}\left[\frac{3x^{3} - x^{2} + 5x + 1}{4\left(2x^{2} + 4\right)}\right]$
- Answer: $\frac{\left(9x^{2} - 2x + 5\right)\left(4\left(2x^{2} + 4\right)\right)-\left(3x^{3} - x^{2} + 5x + 1\right)\left(16x\right)}{\left(4\left(2x^{2} + 4\right)\right)^{2}}$

### Quotient Rule · 6

- Edits: `factor_common_sum`
- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{-4x + 2}{-2\left(x + 2\right)}\right)$
- Answer: $\frac{\left(-4\right)\left(-2\left(x + 2\right)\right)-\left(-4x + 2\right)\left(-2\right)}{\left(-2\left(x + 2\right)\right)^{2}}$

## Chain Rule

Generator `derivative_chain_rule`.

### Chain Rule · 1

- Edits: `none`
- Prompt: $\frac{d}{dx}\left[\sin^{3}\left(-4x^{2} - 3\right)\right]$
- Answer: $-24\sin^{2}\left(-4x^{2} - 3\right)\cos\left(-4x^{2} - 3\right)x$

### Chain Rule · 2

- Edits: `multiply_sum_unexpanded(3), negate`
- Prompt: $\frac{d}{dx}\left[-\cos^{3}\left(3\left(5x^{3} + x^{2}\right)\right)\right]$
- Answer: $9\cos^{2}\left(3\left(5x^{3} + x^{2}\right)\right)\sin\left(3\left(5x^{3} + x^{2}\right)\right)\left(15x^{2} + 2x\right)$

### Chain Rule · 3

- Edits: `multiply_outside(2), negate`
- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(2\cos\left(\tan(x)\right)\right)^{2}\right)$
- Answer: $8\cos\left(\tan(x)\right)\sin\left(\tan(x)\right)\sec^{2}(x)$

### Chain Rule · 4

- Edits: `multiply_outside(2), multiply_outside(-3)`
- Prompt: $\frac{d}{dx}\left[\left(2\tan\left(-3\ln\left(-x\right)\right)\right)^{3}\right]$
- Answer: $\frac{18\left(2\tan\left(-3\ln\left(-x\right)\right)\right)^{2}\sec^{2}(-3\ln\left(-x\right))}{-x}$

### Chain Rule · 5

- Edits: `negate`
- Prompt: $\frac{d}{dx}\left[-\left(x^{3} + 5x^{2} - 4\right)^{2}\right]$
- Answer: $-2\left(x^{3} + 5x^{2} - 4\right)\left(3x^{2} + 10x\right)$

### Chain Rule · 6

- Edits: `multiply_outside(-4), negate`
- Prompt: $\text{Find }\frac{d}{dx}\left(-\sin\left(-4\tan(x)\right)\right)$
- Answer: $4\cos\left(-4\tan(x)\right)\sec^{2}(x)$

## General derivatives

Generator `derivative_general`.

### General derivatives · 1

- Edits: `none`
- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\cos\left(\tan(3x)\right)}{5x^{2} + 2x + 5}\right)$
- Answer: $\frac{\left(-3\sin\left(\tan(3x)\right)\sec^{2}(3x)\right)\left(5x^{2} + 2x + 5\right)-\left(\cos\left(\tan(3x)\right)\right)\left(10x + 2\right)}{\left(5x^{2} + 2x + 5\right)^{2}}$

### General derivatives · 2

- Edits: `multiply_sum_unexpanded(-3), multiply_outside(-2)`
- Prompt: $\frac{d}{dx}\left[6\left(x^{3} + 4x - 1\right)\left(-4x - 2\right)\right]$
- Answer: $6\left(3x^{2} + 4\right)\left(-4x - 2\right) - 24\left(x^{3} + 4x - 1\right)$

### General derivatives · 3

- Edits: `multiply_outside(2)`
- Prompt: $\text{Find }\frac{d}{dx}\left(2e^{\sin(x)}\right)$
- Answer: $2e^{\sin(x)}\cos(x)$

### General derivatives · 4

- Edits: `multiply_outside(-2)`
- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{-2\cdot\left(-2x^{3} - 5x^{2} + x - 5\right)}{2x - 2}\right)$
- Answer: $\frac{\left(-2\cdot\left(-6x^{2} - 10x + 1\right)\right)\left(2x - 2\right)-\left(-2\cdot\left(-2x^{3} - 5x^{2} + x - 5\right)\right)\left(2\right)}{\left(2x - 2\right)^{2}}$

### General derivatives · 5

- Edits: `none`
- Prompt: $\text{Find }\frac{d}{dx}\left(\left(4x - 2\right)\left(2x + 4\right)^{2}\right)$
- Answer: $4\left(2x + 4\right)^{2} + 4\left(2x + 4\right)\left(4x - 2\right)$

### General derivatives · 6

- Edits: `multiply_sum_unexpanded(-4)`
- Prompt: $\frac{d}{dx}\left[-4\left(5x + 2\right)\left(-3x - 1\right)^{2}\right]$
- Answer: $-20\left(-3x - 1\right)^{2} + 24\left(-3x - 1\right)\left(5x + 2\right)$

## Trigonometric

Generator `derivative_trigonometric`.

### Trigonometric · 1

- Edits: `none`
- Prompt: $\text{Find }\frac{d}{dx}\left(\cos\left(4x^{3} + 1\right)\right)$
- Answer: $-12\sin\left(4x^{3} + 1\right)x^{2}$

### Trigonometric · 2

- Edits: `multiply_outside(-2)`
- Prompt: $\text{Find }\frac{d}{dx}\left(\tan\left(-2\cos(-3x)\right)\right)$
- Answer: $-6\sec^{2}(-2\cos(-3x))\sin(-3x)$

### Trigonometric · 3

- Edits: `multiply_outside(-3)`
- Prompt: $\frac{d}{dx}\left[\sin\left(-3\cos(x)\right)\right]$
- Answer: $3\cos\left(-3\cos(x)\right)\sin(x)$

### Trigonometric · 4

- Edits: `negate`
- Prompt: $\frac{d}{dx}\left[-\tan^{2}\left(-4x^{3} + 5x^{2} + 2x - 3\right)\right]$
- Answer: $-2\tan\left(-4x^{3} + 5x^{2} + 2x - 3\right)\sec^{2}(-4x^{3} + 5x^{2} + 2x - 3)\left(-12x^{2} + 10x + 2\right)$

### Trigonometric · 5

- Edits: `multiply_outside(-3), multiply_outside(3)`
- Prompt: $\frac{d}{dx}\left[-33\tan\left(\sin(x)\right)\right]$
- Answer: $-9\sec^{2}(\sin(x))\cos(x)$

### Trigonometric · 6

- Edits: `multiply_outside(4)`
- Prompt: $\frac{d}{dx}\left[\left(4\tan\left(\sin(x)\right)\right)^{3}\right]$
- Answer: $12\left(4\tan\left(\sin(x)\right)\right)^{2}\sec^{2}(\sin(x))\cos(x)$

## Inverse trigonometric

Generator `derivative_inverse_trig`.

### Inverse trigonometric · 1

- Edits: `none`
- Prompt: $\frac{d}{dx}\left[\arctan\left(-x^{3} - 5x^{2} - x - 4\right)\right]$
- Answer: $\frac{1}{1+(-x^{3} - 5x^{2} - x - 4)^{2}}\left(-3x^{2} - 10x - 1\right)$

### Inverse trigonometric · 2

- Edits: `none`
- Prompt: $\frac{d}{dx}\left[\arctan\left(\arcsin(x)\right)\right]$
- Answer: $\frac{1}{1+(\arcsin(x))^{2}}\frac{1}{\sqrt{1-(x)^{2}}}$

### Inverse trigonometric · 3

- Edits: `multiply_outside(-3), multiply_outside(3)`
- Prompt: $\text{Find }\frac{d}{dx}\left(-3\arctan\left(3\arcsin\left(x + 2\right)\right)\right)$
- Answer: $-9\frac{1}{1+(3\arcsin\left(x + 2\right))^{2}}\frac{1}{\sqrt{1-(x + 2)^{2}}}$

### Inverse trigonometric · 4

- Edits: `multiply_sum_unexpanded(3)`
- Prompt: $\text{Find }\frac{d}{dx}\left(\arcsin\left(\arctan\left(3\left(4x + 4\right)\right)\right)\right)$
- Answer: $12\frac{1}{\sqrt{1-(\arctan\left(3\left(4x + 4\right)\right))^{2}}}\frac{1}{1+(3\left(4x + 4\right))^{2}}$

### Inverse trigonometric · 5

- Edits: `multiply_outside(4)`
- Prompt: $\text{Find }\frac{d}{dx}\left(4\arctan\left(\arcsin\left(2x - 1\right)\right)\right)$
- Answer: $8\frac{1}{1+(\arcsin\left(2x - 1\right))^{2}}\frac{1}{\sqrt{1-(2x - 1)^{2}}}$

### Inverse trigonometric · 6

- Edits: `multiply_outside(2)`
- Prompt: $\text{Find }\frac{d}{dx}\left(2\arctan\left(-2x - 2\right)\right)$
- Answer: $-4\frac{1}{1+(-2x - 2)^{2}}$

## Natural logarithms and exponentials

Generator `derivative_ln_exp`.

### Natural logarithms and exponentials · 1

- Edits: `negate, multiply_sum_unexpanded(4)`
- Prompt: $\text{Find }\frac{d}{dx}\left(-e^{4\left(3x^{3} + 2x^{2} - 4\right)}\right)$
- Answer: $-4e^{4\left(3x^{3} + 2x^{2} - 4\right)}\left(9x^{2} + 4x\right)$

### Natural logarithms and exponentials · 2

- Edits: `none`
- Prompt: $\text{Find }\frac{d}{dx}\left(\ln\left(4x^{3} - 3x - 3\right)\right)$
- Answer: $\frac{12x^{2} - 3}{4x^{3} - 3x - 3}$

### Natural logarithms and exponentials · 3

- Edits: `negate`
- Prompt: $\frac{d}{dx}\left[-e^{-x^{3} + 5x^{2} + 3x - 1}\right]$
- Answer: $-e^{-x^{3} + 5x^{2} + 3x - 1}\left(-3x^{2} + 10x + 3\right)$

### Natural logarithms and exponentials · 4

- Edits: `none`
- Prompt: $\frac{d}{dx}\left[\ln\left(5x\right)\right]$
- Answer: $\frac{5}{5x}$

### Natural logarithms and exponentials · 5

- Edits: `multiply_sum_unexpanded(3)`
- Prompt: $\text{Find }\frac{d}{dx}\left(e^{3\left(4x - 3\right)}\right)$
- Answer: $12e^{3\left(4x - 3\right)}$

### Natural logarithms and exponentials · 6

- Edits: `multiply_outside(-3), multiply_outside(2)`
- Prompt: $\text{Find }\frac{d}{dx}\left(2\cdot\left(-3e^{x - 3}\right)\right)$
- Answer: $-6e^{x - 3}$

## Direct evaluation

Generator `limit_direct_evaluation`.

### Direct evaluation · 1

- Edits: `none`
- Prompt: $\lim_{x \to -1} e^{2x^{2} + 3x - 3}$
- Answer: $e^{-4}$

### Direct evaluation · 2

- Edits: `constant_multiple`
- Prompt: $\lim_{x \to \frac{7\pi}{4}} -3\cos(2x)$
- Answer: $0$

### Direct evaluation · 3

- Edits: `sign`
- Prompt: $\lim_{x \to -1} -e^{2x^{2} + 2x - 2}$
- Answer: $-e^{-2}$

### Direct evaluation · 4

- Edits: `none`
- Prompt: $\lim_{x \to 2} e^{-x^{2} + 2x + 3}$
- Answer: $e^{3}$

## At infinity

Generator `limit_at_infinity`.

### At infinity · 1

- Edits: `none`
- Prompt: $\lim_{x \to -\infty} \frac{\sin(2x)}{x}$
- Answer: $0$

### At infinity · 2

- Edits: `none`
- Prompt: $\lim_{x \to \infty} \frac{2\cos(x)}{x^{2}}$
- Answer: $0$

### At infinity · 3

- Edits: `none`
- Prompt: $\lim_{x \to -\infty} \arctan(2x)$
- Answer: $-\frac{\pi}{2}$

### At infinity · 4

- Edits: `none`
- Prompt: $\lim_{x \to \infty} \frac{4x + 3}{4x}$
- Answer: $1$

## Removable

Generator `limit_removable`.

### Removable · 1

- Edits: `none`
- Prompt: $\lim_{x \to 2} \frac{x^{3} - 4x^{2} + 5x - 2}{x-2}$
- Answer: $1$

### Removable · 2

- Edits: `none`
- Prompt: $\lim_{x \to 1} \frac{x^{3} + 3x^{2} - 5x + 1}{x-1}$
- Answer: $4$

### Removable · 3

- Edits: `none`
- Prompt: $\lim_{x \to 2} \frac{x^{3} - 5x^{2} + 8x - 4}{x-2}$
- Answer: $0$

### Removable · 4

- Edits: `none`
- Prompt: $\lim_{x \to 3} \frac{x^{2} - 9}{x-3}$
- Answer: $6$

## L'Hôpital

Generator `lhopitals_rule`.

### L'Hôpital · 1

- Edits: `none`
- Prompt: $\lim_{x \to 3} \frac{x^{2}-9}{x-3}$
- Answer: $6$

### L'Hôpital · 2

- Edits: `constant_multiple`
- Prompt: $\lim_{x \to 0} \frac{-4\sin(3x)}{x}$
- Answer: $-12$

### L'Hôpital · 3

- Edits: `constant_multiple`
- Prompt: $\lim_{x \to 0} \frac{3\sin(4x)}{x}$
- Answer: $12$

### L'Hôpital · 4

- Edits: `constant_multiple`
- Prompt: $\lim_{x \to \infty} \frac{-9x^{2} - 18}{6x^{2} + 4}$
- Answer: $-\frac{3}{2}$

## Power rule

Generator `integral_power_rule`.

### Power rule · 1

- Edits: `none`
- Prompt: $\int -2x \, dx$
- Answer: $-x^{2}+C$

### Power rule · 2

- Edits: `none`
- Prompt: $\int 6x^{5} + x^{2} - 2 \, dx$
- Answer: $x^{6}+\frac{1}{3}x^{3}-2x+C$

### Power rule · 3

- Edits: `none`
- Prompt: $\int \sqrt{x}\,dx$
- Answer: $\frac{2}{3}x^{\frac{3}{2}}+C$

### Power rule · 4

- Edits: `none`
- Prompt: $\int 2x^{4} - 6x + 3 \, dx$
- Answer: $3x+\frac{2}{5}x^{5}-3x^{2}+C$

## Substitution

Generator `integral_substitution`.

### Substitution · 1

- Edits: `none`
- Prompt: $\int \frac{2}{2x + 1}\,dx$
- Answer: $\ln|2x + 1|+C$

### Substitution · 2

- Edits: `none`
- Prompt: $\int 2\left(2x - 3\right)^{3}\,dx$
- Answer: $\frac{1}{4}\left(2x - 3\right)^{4}+C$

### Substitution · 3

- Edits: `none`
- Prompt: $\int 2x\left(x^{2}+1\right)^{2}\,dx$
- Answer: $\frac{1}{3}\left(x^{2}+1\right)^{3}+C$

### Substitution · 4

- Edits: `none`
- Prompt: $\int 3\left(3x - 1\right)^{2}\,dx$
- Answer: $\frac{1}{3}\left(3x - 1\right)^{3}+C$

## By parts

Generator `integration_by_parts`.

### By parts · 1

- Edits: `none`
- Prompt: $\int x\sin(x)\,dx$
- Answer: $-x\cos(x)+\sin(x)+C$

### By parts · 2

- Edits: `none`
- Prompt: $\int x\ln(x)\,dx$
- Answer: $\frac{1}{2}x^{2}\ln(x)-\frac{1}{4}x^{2}+C$

### By parts · 3

- Edits: `none`
- Prompt: $\int xe^{x}\,dx$
- Answer: $e^{x}(x-1)+C$

### By parts · 4

- Edits: `none`
- Prompt: $\int xe^{x}\,dx$
- Answer: $e^{x}(x-1)+C$
