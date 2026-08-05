# Derivatives — power rule

**type_id:** `calc_diff_power_rule` · **leaf:** `derivative_power_rule`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_roots`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\text{Find }\frac{d}{dx}\left(-x^{2}\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\left(-x^{2}\right)+1\right)-1\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\left(2x^{2} - 3x^{2}\right)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\left(\left(\frac{4\left(x-2\right)\left(-x^{2}\right)}{4\left(x-2\right)}+4\right)-4\right)+2\right)-2\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\left(\left(-3x^{2} + 5x^{2} - 3x^{2}\right)+6-6\right)+2\right)-2\right)$ |
| **C=4** | $\text{Find }\frac{d}{dx}\left(\left(2x^{4} - 3x^{3} + 2\right)^{4}\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\left(\left(2x^{4} - 3x^{3} + 2\right)^{4}\right)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{4\left(x+3\right)\left(\left(\left(\left(2x^{4} - 3x^{3} + 2\right)^{4}\right)+3\right)-3\right)}{4\left(x+3\right)}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{2\left(x-2\right)\left(\left(\left(2x^{4} - 3x^{3} + 2\right)^{4}\right)+\left(x+2\right)-\left(x+2\right)+\left(-x\right)\right)-\left(-x\right)}{2\left(x-2\right)}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{3\left(x-3\right)\left(\left(\left(2x^{4} - 3x^{3} + 2\right)^{4}\right)+\left(2x+2\right)\right)-\left(2x+2\right)}{3\left(x-3\right)}+\left(3x+2\right)-\left(3x+2\right)\right)$ |
| **C=8** | $\frac{d}{dx}\left[x^{3} + 2x^{2} - 2x + 3\right]$ | $\frac{d}{dx}\left[\frac{-\left(3+x\right)\left(x^{3} + 2x^{2} - 2x + 3\right)}{-\left(3+x\right)}\right]$ | $\frac{d}{dx}\left[\left(\left(3x^{3} - 2x^{3} + 2x^{2} - 2x + 3\right)+\left(2x+1\right)\right)-\left(2x+1\right)\right]$ | $\frac{d}{dx}\left[\frac{3\left(x+3\right)\left(-\left(-\left(x^{3} + 2x^{2} - 2x + 3\right)\right)\right)}{3\left(x+3\right)}+\left(2x-2\right)-\left(2x-2\right)\right]$ | $\frac{d}{dx}\left[\frac{2\left(x-2\right)\left(-\left(-\left(\left(x^{3} + 2x^{2} - 2x + 3\right)+\left(-2x+1\right)\right)-\left(-2x+1\right)\right)\right)}{2\left(x-2\right)}\right]$ |
| **C=12** | $\frac{d^{2}}{dx^{2}}\left[x^{3} - 3x^{2} + 4\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{-\left(2-x\right)\left(x^{3} - 3x^{2} + 4\right)}{-\left(2-x\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[-\left(-\left(x^{3} - 3x^{2} + 4\right)+\left(x-2\right)-\left(x-2\right)\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{4\left(x+1\right)\left(\left(\left(x^{3} - 3x^{2} + 4\right)+2-2\right)+\left(-x\right)\right)-\left(-x\right)}{4\left(x+1\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[-\left(-\frac{\left(x+1\right)\left(-x^{3} - 3x^{2} + 2 + 9x^{3} - 7x^{3} + 2\right)}{x+1}\right)\right]$ |
| **C=16** | $\frac{d}{dx}\left[x^{5} - 2x^{3}\right]$ | $\frac{d}{dx}\left[-\left(-\left(x^{5} - 2x^{3}\right)\right)\right]$ | $\frac{d}{dx}\left[\left(\left(x^{5} - 2x^{3}\right)+\left(-2x\right)-\left(-2x\right)+4\right)-4\right]$ | $\frac{d}{dx}\left[\frac{\left(x+3\right)\left(\left(-\left(-\left(x^{5} - 2x^{3}\right)\right)\right)+1-1\right)}{x+3}\right]$ | $\frac{d}{dx}\left[\frac{\left(x-1\right)\left(2x^{5} - 2x^{3} + 10x^{5} - 11x^{5}\right)}{x-1}+3-3\right]$ |
| **C=20** | $\frac{d}{dx}\left[x^{5} - 5x^{2}\right]$ | $\frac{d}{dx}\left[-\left(-\left(x^{5} - 5x^{2}\right)\right)\right]$ | $\frac{d}{dx}\left[\left(\frac{4\left(x-2\right)\left(x^{5} - 5x^{2}\right)}{4\left(x-2\right)}+1\right)-1\right]$ | $\frac{d}{dx}\left[-\left(-\left(\left(\frac{2\left(x-3\right)\left(x^{5} - 5x^{2}\right)}{2\left(x-3\right)}+1\right)-1\right)\right)\right]$ | $\frac{d}{dx}\left[\left(\left(\left(\left(-\left(-\left(x^{5} - 5x^{2}\right)\right)\right)+3\right)-3\right)+\left(2x+2\right)\right)-\left(2x+2\right)\right]$ |
| **C=25** | $\frac{d}{dx}\left[\left(\left(x^{4} + 1\right)\right)^{\pi}\right]$ | $\frac{d}{dx}\left[\frac{-\left(3-x\right)\left(\left(\left(x^{4} + 1\right)\right)^{\pi}\right)}{-\left(3-x\right)}\right]$ | $\frac{d}{dx}\left[\left(\left(\left(\left(\left(x^{4} + 1\right)\right)^{\pi}\right)+1-1\right)+4\right)-4\right]$ | $\frac{d}{dx}\left[\left(\left(-\left(-\frac{2\left(x+1\right)\left(\left(\left(x^{4} + 1\right)\right)^{\pi}\right)}{2\left(x+1\right)}\right)\right)+\left(x\right)\right)-\left(x\right)\right]$ | $\frac{d}{dx}\left[\frac{4\left(x+2\right)\left(\left(\left(\left(x^{4} + 1\right)\right)^{\pi}\right)+\left(-x+3\right)\right)-\left(-x+3\right)}{4\left(x+2\right)}+\left(x+3\right)-\left(x+3\right)\right]$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $-2x$ | $-2x$ | $-2x$ | $-2x$ | $-2x$ |
| **C=4** | $4\left(2x^{4} - 3x^{3} + 2\right)^{3}\left(8x^{3} - 9x^{2}\right)$ | $4\left(2x^{4} - 3x^{3} + 2\right)^{3}\left(8x^{3} - 9x^{2}\right)$ | $4\left(2x^{4} - 3x^{3} + 2\right)^{3}\left(8x^{3} - 9x^{2}\right)$ | $4\left(2x^{4} - 3x^{3} + 2\right)^{3}\left(8x^{3} - 9x^{2}\right)$ | $4\left(2x^{4} - 3x^{3} + 2\right)^{3}\left(8x^{3} - 9x^{2}\right)$ |
| **C=8** | $3x^{2} + 4x - 2$ | $3x^{2} + 4x - 2$ | $3x^{2} + 4x - 2$ | $3x^{2} + 4x - 2$ | $3x^{2} + 4x - 2$ |
| **C=12** | $6x - 6$ | $6x - 6$ | $6x - 6$ | $6x - 6$ | $6x - 6$ |
| **C=16** | $5x^{4} - 6x^{2}$ | $5x^{4} - 6x^{2}$ | $5x^{4} - 6x^{2}$ | $5x^{4} - 6x^{2}$ | $5x^{4} - 6x^{2}$ |
| **C=20** | $5x^{4} - 10x$ | $5x^{4} - 10x$ | $5x^{4} - 10x$ | $5x^{4} - 10x$ | $5x^{4} - 10x$ |
| **C=25** | $\pi\left(x^{4} + 1\right)^{\pi-1}\left(4x^{3}\right)$ | $\pi\left(x^{4} + 1\right)^{\pi-1}\left(4x^{3}\right)$ | $\pi\left(x^{4} + 1\right)^{\pi-1}\left(4x^{3}\right)$ | $\pi\left(x^{4} + 1\right)^{\pi-1}\left(4x^{3}\right)$ | $\pi\left(x^{4} + 1\right)^{\pi-1}\left(4x^{3}\right)$ |

## Cell detail

### C=0 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(-x^{2}\right)$
- Answer: $-2x$
- From: `form:power_poly` · `conceptual:power` · `allow:roots`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\left(-x^{2}\right)+1\right)-1\right)$
- Answer: $-2x$
- From: `form:power_poly` · `conceptual:power` · `effort:add_cancel_const` · `allow:roots` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\left(2x^{2} - 3x^{2}\right)\right)\right)$
- Answer: $-2x$
- From: `form:power_poly` · `conceptual:power` · `effort:double_neg` · `allow:roots` · `effort:poly_inflate` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\left(\left(\frac{4\left(x-2\right)\left(-x^{2}\right)}{4\left(x-2\right)}+4\right)-4\right)+2\right)-2\right)$
- Answer: $-2x$
- From: `form:power_poly` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:roots` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:add_cancel_const`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\left(\left(-3x^{2} + 5x^{2} - 3x^{2}\right)+6-6\right)+2\right)-2\right)$
- Answer: $-2x$
- From: `form:power_poly` · `conceptual:power` · `effort:add_cancel_const` · `allow:roots` · `effort:poly_inflate` · `effort:add_cancel_const` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(2x^{4} - 3x^{3} + 2\right)^{4}\right)$
- Answer: $4\left(2x^{4} - 3x^{3} + 2\right)^{3}\left(8x^{3} - 9x^{2}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\left(\left(2x^{4} - 3x^{3} + 2\right)^{4}\right)\right)\right)$
- Answer: $4\left(2x^{4} - 3x^{3} + 2\right)^{3}\left(8x^{3} - 9x^{2}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{4\left(x+3\right)\left(\left(\left(\left(2x^{4} - 3x^{3} + 2\right)^{4}\right)+3\right)-3\right)}{4\left(x+3\right)}\right)$
- Answer: $4\left(2x^{4} - 3x^{3} + 2\right)^{3}\left(8x^{3} - 9x^{2}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `prereq:cancel_quot_bait`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{2\left(x-2\right)\left(\left(\left(2x^{4} - 3x^{3} + 2\right)^{4}\right)+\left(x+2\right)-\left(x+2\right)+\left(-x\right)\right)-\left(-x\right)}{2\left(x-2\right)}\right)$
- Answer: $4\left(2x^{4} - 3x^{3} + 2\right)^{3}\left(8x^{3} - 9x^{2}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:add_cancel_linear`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{3\left(x-3\right)\left(\left(\left(2x^{4} - 3x^{3} + 2\right)^{4}\right)+\left(2x+2\right)\right)-\left(2x+2\right)}{3\left(x-3\right)}+\left(3x+2\right)-\left(3x+2\right)\right)$
- Answer: $4\left(2x^{4} - 3x^{3} + 2\right)^{3}\left(8x^{3} - 9x^{2}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\frac{d}{dx}\left[x^{3} + 2x^{2} - 2x + 3\right]$
- Answer: $3x^{2} + 4x - 2$
- From: `form:power_negative` · `conceptual:power+sum` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25 · shortfall=0.5

### C=8 · S=4

- Prompt: $\frac{d}{dx}\left[\frac{-\left(3+x\right)\left(x^{3} + 2x^{2} - 2x + 3\right)}{-\left(3+x\right)}\right]$
- Answer: $3x^{2} + 4x - 2$
- From: `form:power_negative` · `conceptual:power+sum` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\frac{d}{dx}\left[\left(\left(3x^{3} - 2x^{3} + 2x^{2} - 2x + 3\right)+\left(2x+1\right)\right)-\left(2x+1\right)\right]$
- Answer: $3x^{2} + 4x - 2$
- From: `form:power_negative` · `conceptual:power+sum` · `effort:add_cancel_linear` · `allow:roots` · `answer:unkind_or_messy` · `effort:poly_inflate` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\frac{d}{dx}\left[\frac{3\left(x+3\right)\left(-\left(-\left(x^{3} + 2x^{2} - 2x + 3\right)\right)\right)}{3\left(x+3\right)}+\left(2x-2\right)-\left(2x-2\right)\right]$
- Answer: $3x^{2} + 4x - 2$
- From: `form:power_negative` · `conceptual:power+sum` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:roots` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\frac{d}{dx}\left[\frac{2\left(x-2\right)\left(-\left(-\left(\left(x^{3} + 2x^{2} - 2x + 3\right)+\left(-2x+1\right)\right)-\left(-2x+1\right)\right)\right)}{2\left(x-2\right)}\right]$
- Answer: $3x^{2} + 4x - 2$
- From: `form:power_negative` · `conceptual:power+sum` · `effort:add_cancel_linear` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[x^{3} - 3x^{2} + 4\right]$
- Answer: $6x - 6$
- From: `form:power_poly` · `conceptual:power+sum` · `allow:roots`
- Flags: C=12 · S=0 · amax=25 · shortfall=10.5

### C=12 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{-\left(2-x\right)\left(x^{3} - 3x^{2} + 4\right)}{-\left(2-x\right)}\right]$
- Answer: $6x - 6$
- From: `form:power_poly` · `conceptual:power+sum` · `prereq:cancel_quot_bait` · `allow:roots` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=12 · S=4 · amax=25 · shortfall=9.5

### C=12 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[-\left(-\left(x^{3} - 3x^{2} + 4\right)+\left(x-2\right)-\left(x-2\right)\right)\right]$
- Answer: $6x - 6$
- From: `form:power_poly` · `conceptual:power+sum` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:roots` · `effort:add_cancel_linear` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=12 · S=8 · amax=25 · shortfall=8.5

### C=12 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{4\left(x+1\right)\left(\left(\left(x^{3} - 3x^{2} + 4\right)+2-2\right)+\left(-x\right)\right)-\left(-x\right)}{4\left(x+1\right)}\right]$
- Answer: $6x - 6$
- From: `form:power_poly` · `conceptual:power+sum` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:roots` · `effort:add_cancel_const` · `effort:add_cancel_linear`
- Flags: C=12 · S=16 · amax=25 · shortfall=7.5

### C=12 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[-\left(-\frac{\left(x+1\right)\left(-x^{3} - 3x^{2} + 2 + 9x^{3} - 7x^{3} + 2\right)}{x+1}\right)\right]$
- Answer: $6x - 6$
- From: `form:power_poly` · `conceptual:power+sum` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:roots` · `effort:poly_inflate` · `prereq:cancel_quot_bait` · `effort:double_neg`
- Flags: C=12 · S=32 · amax=25 · shortfall=7.5

### C=16 · S=0

- Prompt: $\frac{d}{dx}\left[x^{5} - 2x^{3}\right]$
- Answer: $5x^{4} - 6x^{2}$
- From: `form:power_negative` · `conceptual:power+sum` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=8.5

### C=16 · S=4

- Prompt: $\frac{d}{dx}\left[-\left(-\left(x^{5} - 2x^{3}\right)\right)\right]$
- Answer: $5x^{4} - 6x^{2}$
- From: `form:power_negative` · `conceptual:power+sum` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=16 · S=4 · amax=25 · shortfall=7.5

### C=16 · S=8

- Prompt: $\frac{d}{dx}\left[\left(\left(x^{5} - 2x^{3}\right)+\left(-2x\right)-\left(-2x\right)+4\right)-4\right]$
- Answer: $5x^{4} - 6x^{2}$
- From: `form:power_negative` · `conceptual:power+sum` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:add_cancel_const`
- Flags: C=16 · S=8 · amax=25 · shortfall=6.5

### C=16 · S=16

- Prompt: $\frac{d}{dx}\left[\frac{\left(x+3\right)\left(\left(-\left(-\left(x^{5} - 2x^{3}\right)\right)\right)+1-1\right)}{x+3}\right]$
- Answer: $5x^{4} - 6x^{2}$
- From: `form:power_negative` · `conceptual:power+sum` · `effort:double_neg` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=16 · S=16 · amax=25 · shortfall=5.5

### C=16 · S=32

- Prompt: $\frac{d}{dx}\left[\frac{\left(x-1\right)\left(2x^{5} - 2x^{3} + 10x^{5} - 11x^{5}\right)}{x-1}+3-3\right]$
- Answer: $5x^{4} - 6x^{2}$
- From: `form:power_negative` · `conceptual:power+sum` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:roots` · `answer:unkind_or_messy` · `effort:poly_inflate` · `prereq:cancel_quot_bait`
- Flags: C=16 · S=32 · amax=25 · shortfall=5.5

### C=20 · S=0

- Prompt: $\frac{d}{dx}\left[x^{5} - 5x^{2}\right]$
- Answer: $5x^{4} - 10x$
- From: `form:power_negative` · `conceptual:power+sum` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=12.5

### C=20 · S=4

- Prompt: $\frac{d}{dx}\left[-\left(-\left(x^{5} - 5x^{2}\right)\right)\right]$
- Answer: $5x^{4} - 10x$
- From: `form:power_negative` · `conceptual:power+sum` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=20 · S=4 · amax=25 · shortfall=11.5

### C=20 · S=8

- Prompt: $\frac{d}{dx}\left[\left(\frac{4\left(x-2\right)\left(x^{5} - 5x^{2}\right)}{4\left(x-2\right)}+1\right)-1\right]$
- Answer: $5x^{4} - 10x$
- From: `form:power_negative` · `conceptual:power+sum` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:add_cancel_const`
- Flags: C=20 · S=8 · amax=25 · shortfall=10.5

### C=20 · S=16

- Prompt: $\frac{d}{dx}\left[-\left(-\left(\left(\frac{2\left(x-3\right)\left(x^{5} - 5x^{2}\right)}{2\left(x-3\right)}+1\right)-1\right)\right)\right]$
- Answer: $5x^{4} - 10x$
- From: `form:power_negative` · `conceptual:power+sum` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=20 · S=16 · amax=25 · shortfall=9.5

### C=20 · S=32

- Prompt: $\frac{d}{dx}\left[\left(\left(\left(\left(-\left(-\left(x^{5} - 5x^{2}\right)\right)\right)+3\right)-3\right)+\left(2x+2\right)\right)-\left(2x+2\right)\right]$
- Answer: $5x^{4} - 10x$
- From: `form:power_negative` · `conceptual:power+sum` · `effort:double_neg` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:roots` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=20 · S=32 · amax=25 · shortfall=9.5

### C=25 · S=0

- Prompt: $\frac{d}{dx}\left[\left(\left(x^{4} + 1\right)\right)^{\pi}\right]$
- Answer: $\pi\left(x^{4} + 1\right)^{\pi-1}\left(4x^{3}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=14

### C=25 · S=4

- Prompt: $\frac{d}{dx}\left[\frac{-\left(3-x\right)\left(\left(\left(x^{4} + 1\right)\right)^{\pi}\right)}{-\left(3-x\right)}\right]$
- Answer: $\pi\left(x^{4} + 1\right)^{\pi-1}\left(4x^{3}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=25 · S=4 · amax=25 · shortfall=13

### C=25 · S=8

- Prompt: $\frac{d}{dx}\left[\left(\left(\left(\left(\left(x^{4} + 1\right)\right)^{\pi}\right)+1-1\right)+4\right)-4\right]$
- Answer: $\pi\left(x^{4} + 1\right)^{\pi-1}\left(4x^{3}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `effort:add_cancel_const` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=25 · S=8 · amax=25 · shortfall=12

### C=25 · S=16

- Prompt: $\frac{d}{dx}\left[\left(\left(-\left(-\frac{2\left(x+1\right)\left(\left(\left(x^{4} + 1\right)\right)^{\pi}\right)}{2\left(x+1\right)}\right)\right)+\left(x\right)\right)-\left(x\right)\right]$
- Answer: $\pi\left(x^{4} + 1\right)^{\pi-1}\left(4x^{3}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=25 · S=16 · amax=25 · shortfall=11

### C=25 · S=32

- Prompt: $\frac{d}{dx}\left[\frac{4\left(x+2\right)\left(\left(\left(\left(x^{4} + 1\right)\right)^{\pi}\right)+\left(-x+3\right)\right)-\left(-x+3\right)}{4\left(x+2\right)}+\left(x+3\right)-\left(x+3\right)\right]$
- Answer: $\pi\left(x^{4} + 1\right)^{\pi-1}\left(4x^{3}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait`
- Flags: C=25 · S=32 · amax=25 · shortfall=11
