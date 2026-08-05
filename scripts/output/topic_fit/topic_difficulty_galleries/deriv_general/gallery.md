# Derivatives — general

**type_id:** `calc_diff_general` · **leaf:** `derivative_general`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_exp`, `allow_invtrig`, `allow_log`, `allow_roots`, `allow_trig`, `allow_triple_product`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\frac{d}{dx}\left[e^{\left(2x - 1\right)}\right]$ | $\frac{d}{dx}\left[e^{\left(2x - 1\right)}+4-4\right]$ | $\frac{d}{dx}\left[\frac{-\left(1+x\right)\left(e^{\left(2x - 1\right)}+\left(x-2\right)\right)-\left(x-2\right)}{-\left(1+x\right)}\right]$ | $\frac{d}{dx}\left[\left(\left(\ln\left(e^{e^{\left(2x - 1\right)}}\right)+6-6\right)+\left(2x+2\right)\right)-\left(2x+2\right)\right]$ | $\frac{d}{dx}\left[\ln\left(e^{\left(\left(e^{\left(2x - 1\right)}+2-2\right)+\left(2x+1\right)\right)-\left(2x+1\right)}\right)\right]$ |
| **C=4** | $\text{Find }\frac{d}{dx}\left(\ln\left(\left(x + 1\right)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\ln\left(\left(x + 1\right)\right)\right)+2-2\right)$ | $\text{Find }\frac{d}{dx}\left(\ln\left(e^{e^{\ln\left(\left(\ln\left(\left(x + 1\right)\right)\right)\right)}}\right)\right)$ | $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\left(\ln\left(\left(x + 1\right)\right)\right)+\left(-2x\right)-\left(-2x\right)\right)}+\left(x+1\right)-\left(x+1\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{4\left(x-3\right)\left(\left(\left(\left(\ln\left(\left(x + 1\right)\right)\right)+\left(-x-1\right)\right)-\left(-x-1\right)+5\right)-5\right)}{4\left(x-3\right)}\right)$ |
| **C=8** | $\text{Find }\frac{d}{dx}\left(\sin(2x)\right)$ | $\text{Find }\frac{d}{dx}\left(\sin(2x)+\left(-x+2\right)-\left(-x+2\right)\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\frac{2\left(x-3\right)\sin(2x)}{2\left(x-3\right)}\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\ln\left(e^{\frac{3\left(x-2\right)\left(\sin(2x)+\left(2x+1\right)-\left(2x+1\right)\right)}{3\left(x-2\right)}}\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\left(\frac{-\left(3+x\right)\sin(2x)}{-\left(3+x\right)}+\left(2x+1\right)\right)-\left(2x+1\right)+\left(-x-1\right)\right)-\left(-x-1\right)\right)$ |
| **C=12** | $\frac{d}{dx}\left[\arccos(x)\sinh(3x)\right]$ | $\frac{d}{dx}\left[-\left(-\arccos(x)\sinh(3x)\right)\right]$ | $\frac{d}{dx}\left[e^{\ln\left(\arccos(x)\sinh(3x)\right)}+2-2\right]$ | $\frac{d}{dx}\left[\ln\left(e^{\left(\left(\frac{\left(x+3\right)\arccos(x)\sinh(3x)}{x+3}+5\right)-5\right)}\right)\right]$ | $\frac{d}{dx}\left[\left(-\left(-\left(\arccos(x)\sinh(3x)+2-2\right)\right)\right)+2-2\right]$ |
| **C=16** | $\frac{d}{dx}\left[\sin^{2}(x)\right]$ | $\frac{d}{dx}\left[e^{\ln\left(\sin^{2}(x)\right)}\right]$ | $\frac{d}{dx}\left[e^{\ln\left(\frac{\left(x-1\right)\sin^{2}(x)}{x-1}\right)}\right]$ | $\frac{d}{dx}\left[\ln\left(e^{\frac{4\left(x+1\right)\sin^{2}(x)}{4\left(x+1\right)}}\right)+6-6\right]$ | $\frac{d}{dx}\left[\left(\frac{-\left(3+x\right)\left(\sin^{2}(x)+\left(x-2\right)-\left(x-2\right)\right)}{-\left(3+x\right)}+5\right)-5\right]$ |
| **C=20** | $\frac{d^{2}}{dx^{2}}\left[e^{e^{x}}\right]$ | $\frac{d^{2}}{dx^{2}}\left[e^{e^{x}}+\left(-x\right)-\left(-x\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\ln\left(e^{\left(e^{e^{x}}+\left(-2x+2\right)\right)-\left(-2x+2\right)}\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[e^{\ln\left(\left(\left(\left(e^{e^{x}}+2-2\right)+2\right)-2\right)\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[-\left(-\frac{3\left(x+2\right)\left(\left(e^{e^{x}}+6\right)-6\right)}{3\left(x+2\right)}\right)\right]$ |
| **C=25** | $\frac{d^{3}}{dx^{3}}\left[\sqrt{4x}\right]$ | $\frac{d^{3}}{dx^{3}}\left[-\left(-\sqrt{4x}\right)\right]$ | $\frac{d^{3}}{dx^{3}}\left[\frac{-\left(1+x\right)\ln\left(e^{\sqrt{4x}}\right)}{-\left(1+x\right)}\right]$ | $\frac{d^{3}}{dx^{3}}\left[e^{\ln\left(\ln\left(e^{\sqrt{4x}}\right)\right)}+\left(3x+1\right)-\left(3x+1\right)\right]$ | $\frac{d^{3}}{dx^{3}}\left[\left(\ln\left(e^{\frac{-\left(3+x\right)\sqrt{4x}}{-\left(3+x\right)}}\right)+6\right)-6\right]$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $e^{\left(2x - 1\right)}\left(2\right)$ | $e^{\left(2x - 1\right)}\left(2\right)$ | $e^{\left(2x - 1\right)}\left(2\right)$ | $e^{\left(2x - 1\right)}\left(2\right)$ | $e^{\left(2x - 1\right)}\left(2\right)$ |
| **C=4** | $\frac{1}{\left(x + 1\right)}$ | $\frac{1}{\left(x + 1\right)}$ | $\frac{1}{\left(x + 1\right)}$ | $\frac{1}{\left(x + 1\right)}$ | $\frac{1}{\left(x + 1\right)}$ |
| **C=8** | $2\cos(2x)$ | $2\cos(2x)$ | $2\cos(2x)$ | $2\cos(2x)$ | $2\cos(2x)$ |
| **C=12** | $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sinh(3x) + 3\cosh(3x)\arccos(x)$ | $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sinh(3x) + 3\cosh(3x)\arccos(x)$ | $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sinh(3x) + 3\cosh(3x)\arccos(x)$ | $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sinh(3x) + 3\cosh(3x)\arccos(x)$ | $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sinh(3x) + 3\cosh(3x)\arccos(x)$ |
| **C=16** | $2\left(\sin(x)\right)\left(\cos(x)\right)$ | $2\left(\sin(x)\right)\left(\cos(x)\right)$ | $2\left(\sin(x)\right)\left(\cos(x)\right)$ | $2\left(\sin(x)\right)\left(\cos(x)\right)$ | $2\left(\sin(x)\right)\left(\cos(x)\right)$ |
| **C=20** | $e^{e^{x}}\left(e^{x}\right)^{2} + e^{x}e^{e^{x}}$ | $e^{e^{x}}\left(e^{x}\right)^{2} + e^{x}e^{e^{x}}$ | $e^{e^{x}}\left(e^{x}\right)^{2} + e^{x}e^{e^{x}}$ | $e^{e^{x}}\left(e^{x}\right)^{2} + e^{x}e^{e^{x}}$ | $e^{e^{x}}\left(e^{x}\right)^{2} + e^{x}e^{e^{x}}$ |
| **C=25** | $64\cdot\left(-\frac{3}{2}\left(4x\right)^{-\frac{5}{2}}\left(-\frac{1}{4}\right)\right)$ | $64\cdot\left(-\frac{3}{2}\left(4x\right)^{-\frac{5}{2}}\left(-\frac{1}{4}\right)\right)$ | $64\cdot\left(-\frac{3}{2}\left(4x\right)^{-\frac{5}{2}}\left(-\frac{1}{4}\right)\right)$ | $64\cdot\left(-\frac{3}{2}\left(4x\right)^{-\frac{5}{2}}\left(-\frac{1}{4}\right)\right)$ | $64\cdot\left(-\frac{3}{2}\left(4x\right)^{-\frac{5}{2}}\left(-\frac{1}{4}\right)\right)$ |

## Cell detail

### C=0 · S=0

- Prompt: $\frac{d}{dx}\left[e^{\left(2x - 1\right)}\right]$
- Answer: $e^{\left(2x - 1\right)}\left(2\right)$
- From: `form:product_two_poly` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\frac{d}{dx}\left[e^{\left(2x - 1\right)}+4-4\right]$
- Answer: $e^{\left(2x - 1\right)}\left(2\right)$
- From: `form:product_two_poly` · `conceptual:chain+power` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\frac{d}{dx}\left[\frac{-\left(1+x\right)\left(e^{\left(2x - 1\right)}+\left(x-2\right)\right)-\left(x-2\right)}{-\left(1+x\right)}\right]$
- Answer: $e^{\left(2x - 1\right)}\left(2\right)$
- From: `form:product_two_poly` · `conceptual:chain+power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\frac{d}{dx}\left[\left(\left(\ln\left(e^{e^{\left(2x - 1\right)}}\right)+6-6\right)+\left(2x+2\right)\right)-\left(2x+2\right)\right]$
- Answer: $e^{\left(2x - 1\right)}\left(2\right)$
- From: `form:product_two_poly` · `conceptual:chain+power` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\frac{d}{dx}\left[\ln\left(e^{\left(\left(e^{\left(2x - 1\right)}+2-2\right)+\left(2x+1\right)\right)-\left(2x+1\right)}\right)\right]$
- Answer: $e^{\left(2x - 1\right)}\left(2\right)$
- From: `form:product_two_poly` · `conceptual:chain+power` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\ln\left(\left(x + 1\right)\right)\right)$
- Answer: $\frac{1}{\left(x + 1\right)}$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\ln\left(\left(x + 1\right)\right)\right)+2-2\right)$
- Answer: $\frac{1}{\left(x + 1\right)}$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\ln\left(e^{e^{\ln\left(\left(\ln\left(\left(x + 1\right)\right)\right)\right)}}\right)\right)$
- Answer: $\frac{1}{\left(x + 1\right)}$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\left(\ln\left(\left(x + 1\right)\right)\right)+\left(-2x\right)-\left(-2x\right)\right)}+\left(x+1\right)-\left(x+1\right)\right)$
- Answer: $\frac{1}{\left(x + 1\right)}$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{4\left(x-3\right)\left(\left(\left(\left(\ln\left(\left(x + 1\right)\right)\right)+\left(-x-1\right)\right)-\left(-x-1\right)+5\right)-5\right)}{4\left(x-3\right)}\right)$
- Answer: $\frac{1}{\left(x + 1\right)}$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\sin(2x)\right)$
- Answer: $2\cos(2x)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=8 · S=0 · amax=25

### C=8 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\sin(2x)+\left(-x+2\right)-\left(-x+2\right)\right)$
- Answer: $2\cos(2x)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\frac{2\left(x-3\right)\sin(2x)}{2\left(x-3\right)}\right)\right)$
- Answer: $2\cos(2x)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\ln\left(e^{\frac{3\left(x-2\right)\left(\sin(2x)+\left(2x+1\right)-\left(2x+1\right)\right)}{3\left(x-2\right)}}\right)\right)$
- Answer: $2\cos(2x)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\left(\frac{-\left(3+x\right)\sin(2x)}{-\left(3+x\right)}+\left(2x+1\right)\right)-\left(2x+1\right)+\left(-x-1\right)\right)-\left(-x-1\right)\right)$
- Answer: $2\cos(2x)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\frac{d}{dx}\left[\arccos(x)\sinh(3x)\right]$
- Answer: $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sinh(3x) + 3\cosh(3x)\arccos(x)$
- From: `form:chain_nested` · `conceptual:chain+power+product` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=12 · S=0 · amax=25

### C=12 · S=4

- Prompt: $\frac{d}{dx}\left[-\left(-\arccos(x)\sinh(3x)\right)\right]$
- Answer: $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sinh(3x) + 3\cosh(3x)\arccos(x)$
- From: `form:chain_nested` · `conceptual:chain+power+product` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=12 · S=4 · amax=25

### C=12 · S=8

- Prompt: $\frac{d}{dx}\left[e^{\ln\left(\arccos(x)\sinh(3x)\right)}+2-2\right]$
- Answer: $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sinh(3x) + 3\cosh(3x)\arccos(x)$
- From: `form:chain_nested` · `conceptual:chain+power+product` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=12 · S=8 · amax=25

### C=12 · S=16

- Prompt: $\frac{d}{dx}\left[\ln\left(e^{\left(\left(\frac{\left(x+3\right)\arccos(x)\sinh(3x)}{x+3}+5\right)-5\right)}\right)\right]$
- Answer: $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sinh(3x) + 3\cosh(3x)\arccos(x)$
- From: `form:chain_nested` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=12 · S=16 · amax=25

### C=12 · S=32

- Prompt: $\frac{d}{dx}\left[\left(-\left(-\left(\arccos(x)\sinh(3x)+2-2\right)\right)\right)+2-2\right]$
- Answer: $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sinh(3x) + 3\cosh(3x)\arccos(x)$
- From: `form:chain_nested` · `conceptual:chain+power+product` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=12 · S=32 · amax=25

### C=16 · S=0

- Prompt: $\frac{d}{dx}\left[\sin^{2}(x)\right]$
- Answer: $2\left(\sin(x)\right)\left(\cos(x)\right)$
- From: `form:quotient_trig_poly` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=16 · S=0 · amax=25

### C=16 · S=4

- Prompt: $\frac{d}{dx}\left[e^{\ln\left(\sin^{2}(x)\right)}\right]$
- Answer: $2\left(\sin(x)\right)\left(\cos(x)\right)$
- From: `form:quotient_trig_poly` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=16 · S=4 · amax=25

### C=16 · S=8

- Prompt: $\frac{d}{dx}\left[e^{\ln\left(\frac{\left(x-1\right)\sin^{2}(x)}{x-1}\right)}\right]$
- Answer: $2\left(\sin(x)\right)\left(\cos(x)\right)$
- From: `form:quotient_trig_poly` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=16 · S=8 · amax=25

### C=16 · S=16

- Prompt: $\frac{d}{dx}\left[\ln\left(e^{\frac{4\left(x+1\right)\sin^{2}(x)}{4\left(x+1\right)}}\right)+6-6\right]$
- Answer: $2\left(\sin(x)\right)\left(\cos(x)\right)$
- From: `form:quotient_trig_poly` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=16 · S=16 · amax=25

### C=16 · S=32

- Prompt: $\frac{d}{dx}\left[\left(\frac{-\left(3+x\right)\left(\sin^{2}(x)+\left(x-2\right)-\left(x-2\right)\right)}{-\left(3+x\right)}+5\right)-5\right]$
- Answer: $2\left(\sin(x)\right)\left(\cos(x)\right)$
- From: `form:quotient_trig_poly` · `conceptual:chain+power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=32 · amax=25

### C=20 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{e^{x}}\right]$
- Answer: $e^{e^{x}}\left(e^{x}\right)^{2} + e^{x}e^{e^{x}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=20 · S=0 · amax=25

### C=20 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{e^{x}}+\left(-x\right)-\left(-x\right)\right]$
- Answer: $e^{e^{x}}\left(e^{x}\right)^{2} + e^{x}e^{e^{x}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=20 · S=4 · amax=25

### C=20 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\ln\left(e^{\left(e^{e^{x}}+\left(-2x+2\right)\right)-\left(-2x+2\right)}\right)\right]$
- Answer: $e^{e^{x}}\left(e^{x}\right)^{2} + e^{x}e^{e^{x}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=20 · S=8 · amax=25

### C=20 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{\ln\left(\left(\left(\left(e^{e^{x}}+2-2\right)+2\right)-2\right)\right)}\right]$
- Answer: $e^{e^{x}}\left(e^{x}\right)^{2} + e^{x}e^{e^{x}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=20 · S=16 · amax=25

### C=20 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[-\left(-\frac{3\left(x+2\right)\left(\left(e^{e^{x}}+6\right)-6\right)}{3\left(x+2\right)}\right)\right]$
- Answer: $e^{e^{x}}\left(e^{x}\right)^{2} + e^{x}e^{e^{x}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=32 · amax=25

### C=25 · S=0

- Prompt: $\frac{d^{3}}{dx^{3}}\left[\sqrt{4x}\right]$
- Answer: $64\cdot\left(-\frac{3}{2}\left(4x\right)^{-\frac{5}{2}}\left(-\frac{1}{4}\right)\right)$
- From: `form:chain_nested` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=25 · S=0 · amax=25

### C=25 · S=4

- Prompt: $\frac{d^{3}}{dx^{3}}\left[-\left(-\sqrt{4x}\right)\right]$
- Answer: $64\cdot\left(-\frac{3}{2}\left(4x\right)^{-\frac{5}{2}}\left(-\frac{1}{4}\right)\right)$
- From: `form:chain_nested` · `conceptual:chain+power` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=4 · amax=25

### C=25 · S=8

- Prompt: $\frac{d^{3}}{dx^{3}}\left[\frac{-\left(1+x\right)\ln\left(e^{\sqrt{4x}}\right)}{-\left(1+x\right)}\right]$
- Answer: $64\cdot\left(-\frac{3}{2}\left(4x\right)^{-\frac{5}{2}}\left(-\frac{1}{4}\right)\right)$
- From: `form:chain_nested` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=8 · amax=25

### C=25 · S=16

- Prompt: $\frac{d^{3}}{dx^{3}}\left[e^{\ln\left(\ln\left(e^{\sqrt{4x}}\right)\right)}+\left(3x+1\right)-\left(3x+1\right)\right]$
- Answer: $64\cdot\left(-\frac{3}{2}\left(4x\right)^{-\frac{5}{2}}\left(-\frac{1}{4}\right)\right)$
- From: `form:chain_nested` · `conceptual:chain+power` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=16 · amax=25

### C=25 · S=32

- Prompt: $\frac{d^{3}}{dx^{3}}\left[\left(\ln\left(e^{\frac{-\left(3+x\right)\sqrt{4x}}{-\left(3+x\right)}}\right)+6\right)-6\right]$
- Answer: $64\cdot\left(-\frac{3}{2}\left(4x\right)^{-\frac{5}{2}}\left(-\frac{1}{4}\right)\right)$
- From: `form:chain_nested` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=25 · S=32 · amax=25
