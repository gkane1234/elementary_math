# Derivatives — trigonometric

**type_id:** `calc_diff_trigonometric` · **leaf:** `derivative_trigonometric`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_trig`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\frac{d}{dx}\left[\sin(2x)\right]$ | $\frac{d}{dx}\left[\frac{2\left(x-1\right)\sin(2x)}{2\left(x-1\right)}\right]$ | $\frac{d}{dx}\left[\left(\frac{\left(x-3\right)\sin(2x)}{x-3}+\left(-2x-2\right)\right)-\left(-2x-2\right)\right]$ | $\frac{d}{dx}\left[\left(\sin(2x)+\left(-2x-1\right)\right)-\left(-2x-1\right)+\left(2x+3\right)-\left(2x+3\right)+\left(3x+3\right)-\left(3x+3\right)\right]$ | $\frac{d}{dx}\left[-\left(-\left(\left(\left(\sin(2x)+5\right)-5\right)+1-1\right)\right)\right]$ |
| **C=4** | $\frac{d}{dx}\left[\sin(4x)\right]$ | $\frac{d}{dx}\left[\sin(4x)+2-2\right]$ | $\frac{d}{dx}\left[\frac{\left(x-2\right)\left(\sin(4x)+\left(-x+3\right)\right)-\left(-x+3\right)}{x-2}\right]$ | $\frac{d}{dx}\left[-\left(-\frac{-\left(3-x\right)\left(\sin(4x)+\left(3x-1\right)\right)-\left(3x-1\right)}{-\left(3-x\right)}\right)\right]$ | $\frac{d}{dx}\left[\left(\left(\frac{-\left(1-x\right)\sin(4x)}{-\left(1-x\right)}+5\right)-5\right)+4-4\right]$ |
| **C=8** | $\text{Find }\frac{d}{dx}\left(\cos^{3}(3x)\sin(2x)\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\cos^{3}(3x)\sin(2x)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\left(x+1\right)\left(\cos^{3}(3x)\sin(2x)+\left(-x-2\right)\right)-\left(-x-2\right)}{x+1}\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\left(\frac{-\left(2+x\right)\cos^{3}(3x)\sin(2x)}{-\left(2+x\right)}+\left(3x+1\right)-\left(3x+1\right)\right)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\frac{\left(x+3\right)\cos^{3}(3x)\sin(2x)}{x+3}+\left(-2x\right)\right)-\left(-2x\right)+\left(-2x+1\right)-\left(-2x+1\right)\right)$ |
| **C=12** | $\frac{d^{2}}{dx^{2}}\left[\tan^{2}(x)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\tan^{2}(x)+\left(x-2\right)\right)-\left(x-2\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{4\left(x+1\right)\tan^{2}(x)}{4\left(x+1\right)}+\left(2x+2\right)-\left(2x+2\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(-\left(-\left(\tan^{2}(x)+\left(x+1\right)\right)-\left(x+1\right)\right)\right)+3-3\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(-\left(-\left(\left(\tan^{2}(x)+4\right)-4\right)\right)\right)+4-4\right]$ |
| **C=16** | $\text{Find }\frac{d}{dx}\left(\sin^{3}(4x)\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{-\left(1-x\right)\sin^{3}(4x)}{-\left(1-x\right)}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\left(x-1\right)\left(-\left(-\sin^{3}(4x)\right)\right)}{x-1}\right)$ | $\text{Find }\frac{d}{dx}\left(\left(-\left(-\frac{3\left(x+3\right)\sin^{3}(4x)}{3\left(x+3\right)}\right)\right)+3-3\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\sin^{3}(4x)+\left(-2x+2\right)-\left(-2x+2\right)\right)+\left(2x-2\right)-\left(2x-2\right)+1-1\right)$ |
| **C=20** | $\text{Find }\frac{d}{dx}\left(\tan\left(\cos\left(\left(4x + 2\right)\right)\right)\sin\left(\cos(3x)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\left(\tan\left(\cos\left(\left(4x + 2\right)\right)\right)\sin\left(\cos(3x)\right)\right)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\left(-\left(-\left(\tan\left(\cos\left(\left(4x + 2\right)\right)\right)\sin\left(\cos(3x)\right)\right)\right)\right)+\left(2x+1\right)\right)-\left(2x+1\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\left(\left(\tan\left(\cos\left(\left(4x + 2\right)\right)\right)\sin\left(\cos(3x)\right)\right)+\left(2x-1\right)\right)-\left(2x-1\right)+5-5\right)+2-2\right)$ | $\text{Find }\frac{d}{dx}\left(\left(-\left(-\left(\left(\tan\left(\cos\left(\left(4x + 2\right)\right)\right)\sin\left(\cos(3x)\right)\right)+\left(-x+3\right)\right)-\left(-x+3\right)\right)\right)+\left(x-1\right)-\left(x-1\right)\right)$ |
| **C=25** | $\frac{d^{2}}{dx^{2}}\left[\tan^{2}(x)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\tan^{2}(x)+4-4\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{4\left(x+2\right)\tan^{2}(x)}{4\left(x+2\right)}+\left(-x+1\right)-\left(-x+1\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\frac{\left(x+3\right)\left(\tan^{2}(x)+\left(x+1\right)\right)-\left(x+1\right)}{x+3}+\left(x-1\right)\right)-\left(x-1\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\left(\left(\left(\tan^{2}(x)+\left(2x+3\right)-\left(2x+3\right)\right)+4\right)-4\right)+\left(-2x\right)\right)-\left(-2x\right)\right]$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $2\cos(2x)$ | $2\cos(2x)$ | $2\cos(2x)$ | $2\cos(2x)$ | $2\cos(2x)$ |
| **C=4** | $4\cos(4x)$ | $4\cos(4x)$ | $4\cos(4x)$ | $4\cos(4x)$ | $4\cos(4x)$ |
| **C=8** | $\left(-9\cos^{2}(3x)\sin(3x)\right)\sin(2x)+\cos^{3}(3x)\left(2\cos(2x)\right)$ | $\left(-9\cos^{2}(3x)\sin(3x)\right)\sin(2x)+\cos^{3}(3x)\left(2\cos(2x)\right)$ | $\left(-9\cos^{2}(3x)\sin(3x)\right)\sin(2x)+\cos^{3}(3x)\left(2\cos(2x)\right)$ | $\left(-9\cos^{2}(3x)\sin(3x)\right)\sin(2x)+\cos^{3}(3x)\left(2\cos(2x)\right)$ | $\left(-9\cos^{2}(3x)\sin(3x)\right)\sin(2x)+\cos^{3}(3x)\left(2\cos(2x)\right)$ |
| **C=12** | $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$ | $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$ | $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$ | $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$ | $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$ |
| **C=16** | $3\left(\sin(4x)\right)^{2}\left(4\cos(4x)\right)$ | $3\left(\sin(4x)\right)^{2}\left(4\cos(4x)\right)$ | $3\left(\sin(4x)\right)^{2}\left(4\cos(4x)\right)$ | $3\left(\sin(4x)\right)^{2}\left(4\cos(4x)\right)$ | $3\left(\sin(4x)\right)^{2}\left(4\cos(4x)\right)$ |
| **C=20** | $-4\sec^{2}(\cos\left(\left(4x + 2\right)\right))\sin\left(\left(4x + 2\right)\right)\sin\left(\cos(3x)\right) - 3\cos\left(\cos(3x)\right)\sin(3x)\tan\left(\cos\left(\left(4x + 2\right)\right)\right)$ | $-4\sec^{2}(\cos\left(\left(4x + 2\right)\right))\sin\left(\left(4x + 2\right)\right)\sin\left(\cos(3x)\right) - 3\cos\left(\cos(3x)\right)\sin(3x)\tan\left(\cos\left(\left(4x + 2\right)\right)\right)$ | $-4\sec^{2}(\cos\left(\left(4x + 2\right)\right))\sin\left(\left(4x + 2\right)\right)\sin\left(\cos(3x)\right) - 3\cos\left(\cos(3x)\right)\sin(3x)\tan\left(\cos\left(\left(4x + 2\right)\right)\right)$ | $-4\sec^{2}(\cos\left(\left(4x + 2\right)\right))\sin\left(\left(4x + 2\right)\right)\sin\left(\cos(3x)\right) - 3\cos\left(\cos(3x)\right)\sin(3x)\tan\left(\cos\left(\left(4x + 2\right)\right)\right)$ | $-4\sec^{2}(\cos\left(\left(4x + 2\right)\right))\sin\left(\left(4x + 2\right)\right)\sin\left(\cos(3x)\right) - 3\cos\left(\cos(3x)\right)\sin(3x)\tan\left(\cos\left(\left(4x + 2\right)\right)\right)$ |
| **C=25** | $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$ | $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$ | $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$ | $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$ | $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$ |

## Cell detail

### C=0 · S=0

- Prompt: $\frac{d}{dx}\left[\sin(2x)\right]$
- Answer: $2\cos(2x)$
- From: `form:trig_basic` · `conceptual:chain+power` · `allow:trig` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\frac{d}{dx}\left[\frac{2\left(x-1\right)\sin(2x)}{2\left(x-1\right)}\right]$
- Answer: $2\cos(2x)$
- From: `form:trig_basic` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\frac{d}{dx}\left[\left(\frac{\left(x-3\right)\sin(2x)}{x-3}+\left(-2x-2\right)\right)-\left(-2x-2\right)\right]$
- Answer: $2\cos(2x)$
- From: `form:trig_basic` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\frac{d}{dx}\left[\left(\sin(2x)+\left(-2x-1\right)\right)-\left(-2x-1\right)+\left(2x+3\right)-\left(2x+3\right)+\left(3x+3\right)-\left(3x+3\right)\right]$
- Answer: $2\cos(2x)$
- From: `form:trig_basic` · `conceptual:chain+power` · `effort:add_cancel_linear` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:add_cancel_linear` · `effort:add_cancel_linear`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\frac{d}{dx}\left[-\left(-\left(\left(\left(\sin(2x)+5\right)-5\right)+1-1\right)\right)\right]$
- Answer: $2\cos(2x)$
- From: `form:trig_basic` · `conceptual:chain+power` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:add_cancel_const`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\frac{d}{dx}\left[\sin(4x)\right]$
- Answer: $4\cos(4x)$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `allow:trig` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\frac{d}{dx}\left[\sin(4x)+2-2\right]$
- Answer: $4\cos(4x)$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `effort:add_cancel_const` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\frac{d}{dx}\left[\frac{\left(x-2\right)\left(\sin(4x)+\left(-x+3\right)\right)-\left(-x+3\right)}{x-2}\right]$
- Answer: $4\cos(4x)$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\frac{d}{dx}\left[-\left(-\frac{-\left(3-x\right)\left(\sin(4x)+\left(3x-1\right)\right)-\left(3x-1\right)}{-\left(3-x\right)}\right)\right]$
- Answer: $4\cos(4x)$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\frac{d}{dx}\left[\left(\left(\frac{-\left(1-x\right)\sin(4x)}{-\left(1-x\right)}+5\right)-5\right)+4-4\right]$
- Answer: $4\cos(4x)$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:add_cancel_const`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\cos^{3}(3x)\sin(2x)\right)$
- Answer: $\left(-9\cos^{2}(3x)\sin(3x)\right)\sin(2x)+\cos^{3}(3x)\left(2\cos(2x)\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `allow:trig` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25

### C=8 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\cos^{3}(3x)\sin(2x)\right)\right)$
- Answer: $\left(-9\cos^{2}(3x)\sin(3x)\right)\sin(2x)+\cos^{3}(3x)\left(2\cos(2x)\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `effort:double_neg` · `allow:trig` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\left(x+1\right)\left(\cos^{3}(3x)\sin(2x)+\left(-x-2\right)\right)-\left(-x-2\right)}{x+1}\right)$
- Answer: $\left(-9\cos^{2}(3x)\sin(3x)\right)\sin(2x)+\cos^{3}(3x)\left(2\cos(2x)\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\left(\frac{-\left(2+x\right)\cos^{3}(3x)\sin(2x)}{-\left(2+x\right)}+\left(3x+1\right)-\left(3x+1\right)\right)\right)\right)$
- Answer: $\left(-9\cos^{2}(3x)\sin(3x)\right)\sin(2x)+\cos^{3}(3x)\left(2\cos(2x)\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\frac{\left(x+3\right)\cos^{3}(3x)\sin(2x)}{x+3}+\left(-2x\right)\right)-\left(-2x\right)+\left(-2x+1\right)-\left(-2x+1\right)\right)$
- Answer: $\left(-9\cos^{2}(3x)\sin(3x)\right)\sin(2x)+\cos^{3}(3x)\left(2\cos(2x)\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\tan^{2}(x)\right]$
- Answer: $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `allow:trig` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25

### C=12 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\tan^{2}(x)+\left(x-2\right)\right)-\left(x-2\right)\right]$
- Answer: $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `effort:add_cancel_linear` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=12 · S=4 · amax=25

### C=12 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{4\left(x+1\right)\tan^{2}(x)}{4\left(x+1\right)}+\left(2x+2\right)-\left(2x+2\right)\right]$
- Answer: $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear`
- Flags: C=12 · S=8 · amax=25

### C=12 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(-\left(-\left(\tan^{2}(x)+\left(x+1\right)\right)-\left(x+1\right)\right)\right)+3-3\right]$
- Answer: $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `effort:add_cancel_linear` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=12 · S=16 · amax=25

### C=12 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(-\left(-\left(\left(\tan^{2}(x)+4\right)-4\right)\right)\right)+4-4\right]$
- Answer: $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:double_neg`
- Flags: C=12 · S=32 · amax=25

### C=16 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\sin^{3}(4x)\right)$
- Answer: $3\left(\sin(4x)\right)^{2}\left(4\cos(4x)\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `allow:trig` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25

### C=16 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{-\left(1-x\right)\sin^{3}(4x)}{-\left(1-x\right)}\right)$
- Answer: $3\left(\sin(4x)\right)^{2}\left(4\cos(4x)\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=16 · S=4 · amax=25

### C=16 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\left(x-1\right)\left(-\left(-\sin^{3}(4x)\right)\right)}{x-1}\right)$
- Answer: $3\left(\sin(4x)\right)^{2}\left(4\cos(4x)\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `answer:unkind_or_messy` · `effort:double_neg` · `prereq:cancel_quot_bait`
- Flags: C=16 · S=8 · amax=25

### C=16 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(-\left(-\frac{3\left(x+3\right)\sin^{3}(4x)}{3\left(x+3\right)}\right)\right)+3-3\right)$
- Answer: $3\left(\sin(4x)\right)^{2}\left(4\cos(4x)\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=16 · S=16 · amax=25

### C=16 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\sin^{3}(4x)+\left(-2x+2\right)-\left(-2x+2\right)\right)+\left(2x-2\right)-\left(2x-2\right)+1-1\right)$
- Answer: $3\left(\sin(4x)\right)^{2}\left(4\cos(4x)\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:add_cancel_linear`
- Flags: C=16 · S=32 · amax=25

### C=20 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\tan\left(\cos\left(\left(4x + 2\right)\right)\right)\sin\left(\cos(3x)\right)\right)$
- Answer: $-4\sec^{2}(\cos\left(\left(4x + 2\right)\right))\sin\left(\left(4x + 2\right)\right)\sin\left(\cos(3x)\right) - 3\cos\left(\cos(3x)\right)\sin(3x)\tan\left(\cos\left(\left(4x + 2\right)\right)\right)$
- From: `form:trig_basic` · `conceptual:chain+power+product` · `allow:trig` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=3

### C=20 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\left(\tan\left(\cos\left(\left(4x + 2\right)\right)\right)\sin\left(\cos(3x)\right)\right)\right)\right)$
- Answer: $-4\sec^{2}(\cos\left(\left(4x + 2\right)\right))\sin\left(\left(4x + 2\right)\right)\sin\left(\cos(3x)\right) - 3\cos\left(\cos(3x)\right)\sin(3x)\tan\left(\cos\left(\left(4x + 2\right)\right)\right)$
- From: `form:trig_basic` · `conceptual:chain+power+product` · `effort:double_neg` · `allow:trig` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=20 · S=4 · amax=25 · shortfall=2

### C=20 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\left(-\left(-\left(\tan\left(\cos\left(\left(4x + 2\right)\right)\right)\sin\left(\cos(3x)\right)\right)\right)\right)+\left(2x+1\right)\right)-\left(2x+1\right)\right)$
- Answer: $-4\sec^{2}(\cos\left(\left(4x + 2\right)\right))\sin\left(\left(4x + 2\right)\right)\sin\left(\cos(3x)\right) - 3\cos\left(\cos(3x)\right)\sin(3x)\tan\left(\cos\left(\left(4x + 2\right)\right)\right)$
- From: `form:trig_basic` · `conceptual:chain+power+product` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:add_cancel_linear`
- Flags: C=20 · S=8 · amax=25 · shortfall=1

### C=20 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\left(\left(\tan\left(\cos\left(\left(4x + 2\right)\right)\right)\sin\left(\cos(3x)\right)\right)+\left(2x-1\right)\right)-\left(2x-1\right)+5-5\right)+2-2\right)$
- Answer: $-4\sec^{2}(\cos\left(\left(4x + 2\right)\right))\sin\left(\left(4x + 2\right)\right)\sin\left(\cos(3x)\right) - 3\cos\left(\cos(3x)\right)\sin(3x)\tan\left(\cos\left(\left(4x + 2\right)\right)\right)$
- From: `form:trig_basic` · `conceptual:chain+power+product` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:add_cancel_const`
- Flags: C=20 · S=16 · amax=25

### C=20 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(-\left(-\left(\left(\tan\left(\cos\left(\left(4x + 2\right)\right)\right)\sin\left(\cos(3x)\right)\right)+\left(-x+3\right)\right)-\left(-x+3\right)\right)\right)+\left(x-1\right)-\left(x-1\right)\right)$
- Answer: $-4\sec^{2}(\cos\left(\left(4x + 2\right)\right))\sin\left(\left(4x + 2\right)\right)\sin\left(\cos(3x)\right) - 3\cos\left(\cos(3x)\right)\sin(3x)\tan\left(\cos\left(\left(4x + 2\right)\right)\right)$
- From: `form:trig_basic` · `conceptual:chain+power+product` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:double_neg`
- Flags: C=20 · S=32 · amax=25

### C=25 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\tan^{2}(x)\right]$
- Answer: $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `allow:trig` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=5.5

### C=25 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\tan^{2}(x)+4-4\right]$
- Answer: $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `effort:add_cancel_const` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=25 · S=4 · amax=25 · shortfall=4.5

### C=25 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{4\left(x+2\right)\tan^{2}(x)}{4\left(x+2\right)}+\left(-x+1\right)-\left(-x+1\right)\right]$
- Answer: $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear`
- Flags: C=25 · S=8 · amax=25 · shortfall=3.5

### C=25 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\frac{\left(x+3\right)\left(\tan^{2}(x)+\left(x+1\right)\right)-\left(x+1\right)}{x+3}+\left(x-1\right)\right)-\left(x-1\right)\right]$
- Answer: $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait`
- Flags: C=25 · S=16 · amax=25 · shortfall=2.5

### C=25 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\left(\left(\left(\tan^{2}(x)+\left(2x+3\right)-\left(2x+3\right)\right)+4\right)-4\right)+\left(-2x\right)\right)-\left(-2x\right)\right]$
- Answer: $2\left(\sec^{2}(x)\right)^{2} + 4\sec^{2}(x)\tan^{2}(x)$
- From: `form:product_poly_trig` · `conceptual:chain+power` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:add_cancel_const`
- Flags: C=25 · S=32 · amax=25 · shortfall=2.5
