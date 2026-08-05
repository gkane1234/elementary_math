# Limits — essential discontinuities

**type_id:** `calc_limits_at_essential_discontinuities` · **leaf:** `limit_essential`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_exp`, `allow_trig`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\lim_{x \to 0^{-}} \frac{1}{x}$ | $\lim_{x \to 0^{-}} \frac{1}{x}$ | $\lim_{x \to 0^{-}} \frac{1}{x}$ | $\lim_{x \to 0^{-}} \frac{1}{x}$ | $\lim_{x \to 0^{-}} \frac{1}{x}$ |
| **C=4** | $\lim_{x \to 0} \frac{1}{x^{2}}$ | $\lim_{x \to 0} \frac{1}{x^{2}}$ | $\lim_{x \to 0} \frac{1}{x^{2}}$ | $\lim_{x \to 0} \frac{1}{x^{2}}$ | $\lim_{x \to 0} \frac{1}{x^{2}}$ |
| **C=8** | $\lim_{x \to 0} \frac{4(x+2)}{4\left(((x+2))(x^{2})\right)}$ | $\lim_{x \to 0} \frac{4(x+2)}{4\left(((x+2))(x^{2})\right)}$ | $\lim_{x \to 0} \frac{4(x+2)}{4\left(((x+2))(x^{2})\right)}$ | $\lim_{x \to 0} \frac{4(x+2)}{4\left(((x+2))(x^{2})\right)}$ | $\lim_{x \to 0} \frac{4(x+2)}{4\left(((x+2))(x^{2})\right)}$ |
| **C=12** | $\lim_{x \to 0} 3\sin\left(\frac{1}{x}\right)$ | $\lim_{x \to 0} 3\sin\left(\frac{1}{x}\right)$ | $\lim_{x \to 0} 3\sin\left(\frac{1}{x}\right)$ | $\lim_{x \to 0} 3\sin\left(\frac{1}{x}\right)$ | $\lim_{x \to 0} 3\sin\left(\frac{1}{x}\right)$ |
| **C=16** | $\lim_{x \to 0} \frac{x}{x^{2}}$ | $\lim_{x \to 0} \frac{x}{x^{2}}$ | $\lim_{x \to 0} \frac{x}{x^{2}}$ | $\lim_{x \to 0} \frac{x}{x^{2}}$ | $\lim_{x \to 0} \frac{x}{x^{2}}$ |
| **C=20** | $\lim_{x \to \frac{\pi}{2}} 3\tan(x)$ | $\lim_{x \to \frac{\pi}{2}} 3\tan(x)$ | $\lim_{x \to \frac{\pi}{2}} 3\tan(x)$ | $\lim_{x \to \frac{\pi}{2}} 3\tan(x)$ | $\lim_{x \to \frac{\pi}{2}} 3\tan(x)$ |
| **C=25** | $\lim_{x \to 0} \frac{x}{x^{3}}$ | $\lim_{x \to 0} \frac{x}{x^{3}}$ | $\lim_{x \to 0} \frac{x}{x^{3}}$ | $\lim_{x \to 0} \frac{x}{x^{3}}$ | $\lim_{x \to 0} \frac{x}{x^{3}}$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $-\infty$ | $-\infty$ | $-\infty$ | $-\infty$ | $-\infty$ |
| **C=4** | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ |
| **C=8** | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ |
| **C=12** | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ |
| **C=16** | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ |
| **C=20** | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ |
| **C=25** | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ |

## Cell detail

### C=0 · S=0

- Prompt: $\lim_{x \to 0^{-}} \frac{1}{x}$
- Answer: $-\infty$
- From: `form:essential_1_over_x` · `conceptual:essential_dne` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\lim_{x \to 0^{-}} \frac{1}{x}$
- Answer: $-\infty$
- From: `form:essential_1_over_x` · `conceptual:essential_dne` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\lim_{x \to 0^{-}} \frac{1}{x}$
- Answer: $-\infty$
- From: `form:essential_1_over_x` · `conceptual:essential_dne` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\lim_{x \to 0^{-}} \frac{1}{x}$
- Answer: $-\infty$
- From: `form:essential_1_over_x` · `conceptual:essential_dne` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\lim_{x \to 0^{-}} \frac{1}{x}$
- Answer: $-\infty$
- From: `form:essential_1_over_x` · `conceptual:essential_dne` · `allow:trig` · `allow:exp` · `allow:one_sided` · `effort:spec_high`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\lim_{x \to 0} \frac{1}{x^{2}}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\lim_{x \to 0} \frac{1}{x^{2}}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\lim_{x \to 0} \frac{1}{x^{2}}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\lim_{x \to 0} \frac{1}{x^{2}}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\lim_{x \to 0} \frac{1}{x^{2}}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `allow:trig` · `allow:exp` · `allow:one_sided` · `effort:spec_high`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\lim_{x \to 0} \frac{4(x+2)}{4\left(((x+2))(x^{2})\right)}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `prereq:cancel_factor` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=8 · S=0 · amax=25 · shortfall=1.5

### C=8 · S=4

- Prompt: $\lim_{x \to 0} \frac{4(x+2)}{4\left(((x+2))(x^{2})\right)}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `prereq:cancel_factor` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=8 · S=4 · amax=25 · shortfall=1.5

### C=8 · S=8

- Prompt: $\lim_{x \to 0} \frac{4(x+2)}{4\left(((x+2))(x^{2})\right)}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `prereq:cancel_factor` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=8 · S=8 · amax=25 · shortfall=1.5

### C=8 · S=16

- Prompt: $\lim_{x \to 0} \frac{4(x+2)}{4\left(((x+2))(x^{2})\right)}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `prereq:cancel_factor` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=8 · S=16 · amax=25 · shortfall=1.5

### C=8 · S=32

- Prompt: $\lim_{x \to 0} \frac{4(x+2)}{4\left(((x+2))(x^{2})\right)}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `prereq:cancel_factor` · `allow:trig` · `allow:exp` · `allow:one_sided` · `effort:spec_high`
- Flags: C=8 · S=32 · amax=25 · shortfall=1.5

### C=12 · S=0

- Prompt: $\lim_{x \to 0} 3\sin\left(\frac{1}{x}\right)$
- Answer: $\text{DNE}$
- From: `form:essential_sin_1_over_x` · `conceptual:essential_dne` · `effort:constant_multiple` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=12 · S=0 · amax=25 · shortfall=3

### C=12 · S=4

- Prompt: $\lim_{x \to 0} 3\sin\left(\frac{1}{x}\right)$
- Answer: $\text{DNE}$
- From: `form:essential_sin_1_over_x` · `conceptual:essential_dne` · `effort:constant_multiple` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=12 · S=4 · amax=25 · shortfall=3

### C=12 · S=8

- Prompt: $\lim_{x \to 0} 3\sin\left(\frac{1}{x}\right)$
- Answer: $\text{DNE}$
- From: `form:essential_sin_1_over_x` · `conceptual:essential_dne` · `effort:constant_multiple` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=12 · S=8 · amax=25 · shortfall=3

### C=12 · S=16

- Prompt: $\lim_{x \to 0} 3\sin\left(\frac{1}{x}\right)$
- Answer: $\text{DNE}$
- From: `form:essential_sin_1_over_x` · `conceptual:essential_dne` · `effort:constant_multiple` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=12 · S=16 · amax=25 · shortfall=3

### C=12 · S=32

- Prompt: $\lim_{x \to 0} 3\sin\left(\frac{1}{x}\right)$
- Answer: $\text{DNE}$
- From: `form:essential_sin_1_over_x` · `conceptual:essential_dne` · `effort:constant_multiple` · `allow:trig` · `allow:exp` · `allow:one_sided` · `effort:spec_high`
- Flags: C=12 · S=32 · amax=25 · shortfall=3

### C=16 · S=0

- Prompt: $\lim_{x \to 0} \frac{x}{x^{2}}$
- Answer: $\text{DNE}$
- From: `form:essential_1_over_x` · `conceptual:essential_dne` · `effort:unfactored_poly` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=16 · S=0 · amax=25 · shortfall=11.5

### C=16 · S=4

- Prompt: $\lim_{x \to 0} \frac{x}{x^{2}}$
- Answer: $\text{DNE}$
- From: `form:essential_1_over_x` · `conceptual:essential_dne` · `effort:unfactored_poly` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=16 · S=4 · amax=25 · shortfall=11.5

### C=16 · S=8

- Prompt: $\lim_{x \to 0} \frac{x}{x^{2}}$
- Answer: $\text{DNE}$
- From: `form:essential_1_over_x` · `conceptual:essential_dne` · `effort:unfactored_poly` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=16 · S=8 · amax=25 · shortfall=11.5

### C=16 · S=16

- Prompt: $\lim_{x \to 0} \frac{x}{x^{2}}$
- Answer: $\text{DNE}$
- From: `form:essential_1_over_x` · `conceptual:essential_dne` · `effort:unfactored_poly` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=16 · S=16 · amax=25 · shortfall=11.5

### C=16 · S=32

- Prompt: $\lim_{x \to 0} \frac{x}{x^{2}}$
- Answer: $\text{DNE}$
- From: `form:essential_1_over_x` · `conceptual:essential_dne` · `effort:unfactored_poly` · `allow:trig` · `allow:exp` · `allow:one_sided` · `effort:spec_high`
- Flags: C=16 · S=32 · amax=25 · shortfall=11.5

### C=20 · S=0

- Prompt: $\lim_{x \to \frac{\pi}{2}} 3\tan(x)$
- Answer: $\text{DNE}$
- From: `form:essential_tan_asymptote` · `conceptual:essential_dne` · `effort:sign_flip` · `effort:constant_multiple` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=20 · S=0 · amax=25 · shortfall=8.5

### C=20 · S=4

- Prompt: $\lim_{x \to \frac{\pi}{2}} 3\tan(x)$
- Answer: $\text{DNE}$
- From: `form:essential_tan_asymptote` · `conceptual:essential_dne` · `effort:sign_flip` · `effort:constant_multiple` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=20 · S=4 · amax=25 · shortfall=8.5

### C=20 · S=8

- Prompt: $\lim_{x \to \frac{\pi}{2}} 3\tan(x)$
- Answer: $\text{DNE}$
- From: `form:essential_tan_asymptote` · `conceptual:essential_dne` · `effort:sign_flip` · `effort:constant_multiple` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=20 · S=8 · amax=25 · shortfall=8.5

### C=20 · S=16

- Prompt: $\lim_{x \to \frac{\pi}{2}} 3\tan(x)$
- Answer: $\text{DNE}$
- From: `form:essential_tan_asymptote` · `conceptual:essential_dne` · `effort:sign_flip` · `effort:constant_multiple` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=20 · S=16 · amax=25 · shortfall=8.5

### C=20 · S=32

- Prompt: $\lim_{x \to \frac{\pi}{2}} 3\tan(x)$
- Answer: $\text{DNE}$
- From: `form:essential_tan_asymptote` · `conceptual:essential_dne` · `effort:sign_flip` · `effort:constant_multiple` · `allow:trig` · `allow:exp` · `allow:one_sided` · `effort:spec_high`
- Flags: C=20 · S=32 · amax=25 · shortfall=8.5

### C=25 · S=0

- Prompt: $\lim_{x \to 0} \frac{x}{x^{3}}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `effort:unfactored_poly` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=25 · S=0 · amax=25 · shortfall=19.5

### C=25 · S=4

- Prompt: $\lim_{x \to 0} \frac{x}{x^{3}}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `effort:unfactored_poly` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=25 · S=4 · amax=25 · shortfall=19.5

### C=25 · S=8

- Prompt: $\lim_{x \to 0} \frac{x}{x^{3}}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `effort:unfactored_poly` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=25 · S=8 · amax=25 · shortfall=19.5

### C=25 · S=16

- Prompt: $\lim_{x \to 0} \frac{x}{x^{3}}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `effort:unfactored_poly` · `allow:trig` · `allow:exp` · `allow:one_sided`
- Flags: C=25 · S=16 · amax=25 · shortfall=19.5

### C=25 · S=32

- Prompt: $\lim_{x \to 0} \frac{x}{x^{3}}$
- Answer: $\infty$
- From: `form:essential_1_over_x_sq` · `conceptual:essential_dne` · `effort:unfactored_poly` · `allow:trig` · `allow:exp` · `allow:one_sided` · `effort:spec_high`
- Flags: C=25 · S=32 · amax=25 · shortfall=19.5
