# Derivatives — higher order

**type_id:** `calc_diff_higher_order_derivatives` · **leaf:** `derivative_higher_order`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_exp`, `allow_log`, `allow_trig`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\frac{d^{2}}{dx^{2}}\left[-x^{2}\right]$ | $\frac{d^{2}}{dx^{2}}\left[e^{\ln\left(\left(-x^{2}\right)\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[-\left(-\frac{2\left(x+2\right)\left(-x^{2}\right)}{2\left(x+2\right)}\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\ln\left(e^{\frac{-\left(2-x\right)\left(-x^{2}\right)}{-\left(2-x\right)}}\right)+4-4\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\left(\left(-x^{2}\right)+\left(2x+2\right)\right)-\left(2x+2\right)+\left(2x-2\right)-\left(2x-2\right)+2\right)-2\right]$ |
| **C=4** | $\frac{d^{2}}{dx^{2}}\left[x^{5} + x^{4}\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(x^{5} + x^{4}\right)+\left(x\right)-\left(x\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[-\left(-\left(-2x^{5} + 3x^{5} + x^{4}\right)\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\frac{3\left(x-3\right)\left(-\left(-\left(x^{5} + x^{4}\right)\right)\right)}{3\left(x-3\right)}+\left(2x+1\right)\right)-\left(2x+1\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\frac{-\left(3+x\right)\left(x^{5} + x^{4}\right)}{-\left(3+x\right)}+\left(x+2\right)-\left(x+2\right)\right)+2-2\right]$ |
| **C=8** | $\frac{d^{2}}{dx^{2}}\left[e^{\left(2x + 2\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(e^{\left(2x + 2\right)}+3\right)-3\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{3\left(x+2\right)\left(e^{\left(2x + 2\right)}+1-1\right)}{3\left(x+2\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\left(-\left(-e^{\left(2x + 2\right)}\right)\right)+\left(2x+2\right)\right)-\left(2x+2\right)+\left(-x+2\right)-\left(-x+2\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\left(\ln\left(e^{e^{\left(2x + 2\right)}}\right)+4\right)-4\right)+\left(-x-2\right)-\left(-x-2\right)\right]$ |
| **C=12** | $\frac{d^{2}}{dx^{2}}\left[e^{\left(3x + 4\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[e^{\ln\left(e^{\left(3x + 4\right)}\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[e^{\ln\left(\frac{4\left(x+1\right)e^{\left(3x + 4\right)}}{4\left(x+1\right)}\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[-\left(-\left(\left(e^{\left(3x + 4\right)}+4-4\right)+3-3\right)\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{-\left(1-x\right)\left(-\left(-e^{\ln\left(e^{\left(3x + 4\right)}\right)}\right)\right)}{-\left(1-x\right)}\right]$ |
| **C=16** | $\frac{d^{2}}{dx^{2}}\left[\ln\left(\left(2x - 4\right)\right)\tan(5x)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\left(\ln\left(\left(2x - 4\right)\right)\tan(5x)\right)+5\right)-5\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{\left(x+2\right)\left(\ln\left(\left(2x - 4\right)\right)\tan(5x)\right)}{x+2}+\left(3x\right)-\left(3x\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\ln\left(e^{\frac{-\left(2-x\right)\left(\ln\left(\left(2x - 4\right)\right)\tan(5x)\right)}{-\left(2-x\right)}}\right)+4\right)-4\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\ln\left(e^{\left(-\left(-\left(\ln\left(\left(2x - 4\right)\right)\tan(5x)\right)\right)\right)}\right)+3\right)-3\right]$ |
| **C=20** | $\frac{d^{2}}{dx^{2}}\left[e^{e^{2x}}\right]$ | $\frac{d^{2}}{dx^{2}}\left[-\left(-e^{e^{2x}}\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[-\left(-\ln\left(e^{e^{e^{2x}}}\right)\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\frac{2\left(x-1\right)e^{\ln\left(e^{e^{2x}}\right)}}{2\left(x-1\right)}+5\right)-5\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\frac{-\left(3+x\right)e^{\ln\left(e^{e^{2x}}\right)}}{-\left(3+x\right)}+\left(x-1\right)\right)-\left(x-1\right)\right]$ |
| **C=25** | $\frac{d^{2}}{dx^{2}}\left[e^{e^{\left(2x + 1\right)}}\right]$ | $\frac{d^{2}}{dx^{2}}\left[-\left(-e^{e^{\left(2x + 1\right)}}\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\left(-\left(-e^{e^{\left(2x + 1\right)}}\right)\right)+\left(-x+2\right)\right)-\left(-x+2\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\ln\left(e^{\left(\frac{\left(x+2\right)e^{e^{\left(2x + 1\right)}}}{x+2}+5-5\right)}\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[e^{\ln\left(\frac{-\left(2-x\right)\left(\left(e^{e^{\left(2x + 1\right)}}+5\right)-5\right)}{-\left(2-x\right)}\right)}\right]$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $-2$ | $-2$ | $-2$ | $-2$ | $-2$ |
| **C=4** | $20x^{3} + 12x^{2}$ | $20x^{3} + 12x^{2}$ | $20x^{3} + 12x^{2}$ | $20x^{3} + 12x^{2}$ | $20x^{3} + 12x^{2}$ |
| **C=8** | $4e^{\left(2x + 2\right)}$ | $4e^{\left(2x + 2\right)}$ | $4e^{\left(2x + 2\right)}$ | $4e^{\left(2x + 2\right)}$ | $4e^{\left(2x + 2\right)}$ |
| **C=12** | $9e^{\left(3x + 4\right)}$ | $9e^{\left(3x + 4\right)}$ | $9e^{\left(3x + 4\right)}$ | $9e^{\left(3x + 4\right)}$ | $9e^{\left(3x + 4\right)}$ |
| **C=16** | $-4\left(2x - 4\right)^{-2}\tan(5x) + 10\sec^{2}(5x)\frac{1}{\left(2x - 4\right)} + 50\sec^{2}(5x)\tan(5x)\ln\left(\left(2x - 4\right)\right) + 10\frac{1}{\left(2x - 4\right)}\sec^{2}(5x)$ | $-4\left(2x - 4\right)^{-2}\tan(5x) + 10\sec^{2}(5x)\frac{1}{\left(2x - 4\right)} + 50\sec^{2}(5x)\tan(5x)\ln\left(\left(2x - 4\right)\right) + 10\frac{1}{\left(2x - 4\right)}\sec^{2}(5x)$ | $-4\left(2x - 4\right)^{-2}\tan(5x) + 10\sec^{2}(5x)\frac{1}{\left(2x - 4\right)} + 50\sec^{2}(5x)\tan(5x)\ln\left(\left(2x - 4\right)\right) + 10\frac{1}{\left(2x - 4\right)}\sec^{2}(5x)$ | $-4\left(2x - 4\right)^{-2}\tan(5x) + 10\sec^{2}(5x)\frac{1}{\left(2x - 4\right)} + 50\sec^{2}(5x)\tan(5x)\ln\left(\left(2x - 4\right)\right) + 10\frac{1}{\left(2x - 4\right)}\sec^{2}(5x)$ | $-4\left(2x - 4\right)^{-2}\tan(5x) + 10\sec^{2}(5x)\frac{1}{\left(2x - 4\right)} + 50\sec^{2}(5x)\tan(5x)\ln\left(\left(2x - 4\right)\right) + 10\frac{1}{\left(2x - 4\right)}\sec^{2}(5x)$ |
| **C=20** | $4e^{e^{2x}}\left(e^{2x}\right)^{2} + 4e^{2x}e^{e^{2x}}$ | $4e^{e^{2x}}\left(e^{2x}\right)^{2} + 4e^{2x}e^{e^{2x}}$ | $4e^{e^{2x}}\left(e^{2x}\right)^{2} + 4e^{2x}e^{e^{2x}}$ | $4e^{e^{2x}}\left(e^{2x}\right)^{2} + 4e^{2x}e^{e^{2x}}$ | $4e^{e^{2x}}\left(e^{2x}\right)^{2} + 4e^{2x}e^{e^{2x}}$ |
| **C=25** | $4e^{e^{\left(2x + 1\right)}}\left(e^{\left(2x + 1\right)}\right)^{2} + 4e^{\left(2x + 1\right)}e^{e^{\left(2x + 1\right)}}$ | $4e^{e^{\left(2x + 1\right)}}\left(e^{\left(2x + 1\right)}\right)^{2} + 4e^{\left(2x + 1\right)}e^{e^{\left(2x + 1\right)}}$ | $4e^{e^{\left(2x + 1\right)}}\left(e^{\left(2x + 1\right)}\right)^{2} + 4e^{\left(2x + 1\right)}e^{e^{\left(2x + 1\right)}}$ | $4e^{e^{\left(2x + 1\right)}}\left(e^{\left(2x + 1\right)}\right)^{2} + 4e^{\left(2x + 1\right)}e^{e^{\left(2x + 1\right)}}$ | $4e^{e^{\left(2x + 1\right)}}\left(e^{\left(2x + 1\right)}\right)^{2} + 4e^{\left(2x + 1\right)}e^{e^{\left(2x + 1\right)}}$ |

## Cell detail

### C=0 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[-x^{2}\right]$
- Answer: $-2$
- From: `form:power_poly` · `conceptual:power` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{\ln\left(\left(-x^{2}\right)\right)}\right]$
- Answer: $-2$
- From: `form:power_poly` · `conceptual:power` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:exp_ln_id` · `effort:spec_answer_preserved`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[-\left(-\frac{2\left(x+2\right)\left(-x^{2}\right)}{2\left(x+2\right)}\right)\right]$
- Answer: $-2$
- From: `form:power_poly` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\ln\left(e^{\frac{-\left(2-x\right)\left(-x^{2}\right)}{-\left(2-x\right)}}\right)+4-4\right]$
- Answer: $-2$
- From: `form:power_poly` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\left(\left(-x^{2}\right)+\left(2x+2\right)\right)-\left(2x+2\right)+\left(2x-2\right)-\left(2x-2\right)+2\right)-2\right]$
- Answer: $-2$
- From: `form:power_poly` · `conceptual:power` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_linear`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[x^{5} + x^{4}\right]$
- Answer: $20x^{3} + 12x^{2}$
- From: `form:higher_order_2` · `conceptual:power+sum` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(x^{5} + x^{4}\right)+\left(x\right)-\left(x\right)\right]$
- Answer: $20x^{3} + 12x^{2}$
- From: `form:higher_order_2` · `conceptual:power+sum` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[-\left(-\left(-2x^{5} + 3x^{5} + x^{4}\right)\right)\right]$
- Answer: $20x^{3} + 12x^{2}$
- From: `form:higher_order_2` · `conceptual:power+sum` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:poly_inflate`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\frac{3\left(x-3\right)\left(-\left(-\left(x^{5} + x^{4}\right)\right)\right)}{3\left(x-3\right)}+\left(2x+1\right)\right)-\left(2x+1\right)\right]$
- Answer: $20x^{3} + 12x^{2}$
- From: `form:higher_order_2` · `conceptual:power+sum` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\frac{-\left(3+x\right)\left(x^{5} + x^{4}\right)}{-\left(3+x\right)}+\left(x+2\right)-\left(x+2\right)\right)+2-2\right]$
- Answer: $20x^{3} + 12x^{2}$
- From: `form:higher_order_2` · `conceptual:power+sum` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{\left(2x + 2\right)}\right]$
- Answer: $4e^{\left(2x + 2\right)}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25

### C=8 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(e^{\left(2x + 2\right)}+3\right)-3\right]$
- Answer: $4e^{\left(2x + 2\right)}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{3\left(x+2\right)\left(e^{\left(2x + 2\right)}+1-1\right)}{3\left(x+2\right)}\right]$
- Answer: $4e^{\left(2x + 2\right)}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\left(-\left(-e^{\left(2x + 2\right)}\right)\right)+\left(2x+2\right)\right)-\left(2x+2\right)+\left(-x+2\right)-\left(-x+2\right)\right]$
- Answer: $4e^{\left(2x + 2\right)}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\left(\ln\left(e^{e^{\left(2x + 2\right)}}\right)+4\right)-4\right)+\left(-x-2\right)-\left(-x-2\right)\right]$
- Answer: $4e^{\left(2x + 2\right)}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{\left(3x + 4\right)}\right]$
- Answer: $9e^{\left(3x + 4\right)}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25

### C=12 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{\ln\left(e^{\left(3x + 4\right)}\right)}\right]$
- Answer: $9e^{\left(3x + 4\right)}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:exp_ln_id` · `effort:spec_answer_preserved`
- Flags: C=12 · S=4 · amax=25

### C=12 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{\ln\left(\frac{4\left(x+1\right)e^{\left(3x + 4\right)}}{4\left(x+1\right)}\right)}\right]$
- Answer: $9e^{\left(3x + 4\right)}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=12 · S=8 · amax=25

### C=12 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[-\left(-\left(\left(e^{\left(3x + 4\right)}+4-4\right)+3-3\right)\right)\right]$
- Answer: $9e^{\left(3x + 4\right)}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=16 · amax=25

### C=12 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{-\left(1-x\right)\left(-\left(-e^{\ln\left(e^{\left(3x + 4\right)}\right)}\right)\right)}{-\left(1-x\right)}\right]$
- Answer: $9e^{\left(3x + 4\right)}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=32 · amax=25

### C=16 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\ln\left(\left(2x - 4\right)\right)\tan(5x)\right]$
- Answer: $-4\left(2x - 4\right)^{-2}\tan(5x) + 10\sec^{2}(5x)\frac{1}{\left(2x - 4\right)} + 50\sec^{2}(5x)\tan(5x)\ln\left(\left(2x - 4\right)\right) + 10\frac{1}{\left(2x - 4\right)}\sec^{2}(5x)$
- From: `form:higher_order_2` · `conceptual:chain+power+product` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25

### C=16 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\left(\ln\left(\left(2x - 4\right)\right)\tan(5x)\right)+5\right)-5\right]$
- Answer: $-4\left(2x - 4\right)^{-2}\tan(5x) + 10\sec^{2}(5x)\frac{1}{\left(2x - 4\right)} + 50\sec^{2}(5x)\tan(5x)\ln\left(\left(2x - 4\right)\right) + 10\frac{1}{\left(2x - 4\right)}\sec^{2}(5x)$
- From: `form:higher_order_2` · `conceptual:chain+power+product` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=16 · S=4 · amax=25

### C=16 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{\left(x+2\right)\left(\ln\left(\left(2x - 4\right)\right)\tan(5x)\right)}{x+2}+\left(3x\right)-\left(3x\right)\right]$
- Answer: $-4\left(2x - 4\right)^{-2}\tan(5x) + 10\sec^{2}(5x)\frac{1}{\left(2x - 4\right)} + 50\sec^{2}(5x)\tan(5x)\ln\left(\left(2x - 4\right)\right) + 10\frac{1}{\left(2x - 4\right)}\sec^{2}(5x)$
- From: `form:higher_order_2` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=8 · amax=25

### C=16 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\ln\left(e^{\frac{-\left(2-x\right)\left(\ln\left(\left(2x - 4\right)\right)\tan(5x)\right)}{-\left(2-x\right)}}\right)+4\right)-4\right]$
- Answer: $-4\left(2x - 4\right)^{-2}\tan(5x) + 10\sec^{2}(5x)\frac{1}{\left(2x - 4\right)} + 50\sec^{2}(5x)\tan(5x)\ln\left(\left(2x - 4\right)\right) + 10\frac{1}{\left(2x - 4\right)}\sec^{2}(5x)$
- From: `form:higher_order_2` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=16 · amax=25

### C=16 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\ln\left(e^{\left(-\left(-\left(\ln\left(\left(2x - 4\right)\right)\tan(5x)\right)\right)\right)}\right)+3\right)-3\right]$
- Answer: $-4\left(2x - 4\right)^{-2}\tan(5x) + 10\sec^{2}(5x)\frac{1}{\left(2x - 4\right)} + 50\sec^{2}(5x)\tan(5x)\ln\left(\left(2x - 4\right)\right) + 10\frac{1}{\left(2x - 4\right)}\sec^{2}(5x)$
- From: `form:higher_order_2` · `conceptual:chain+power+product` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=32 · amax=25

### C=20 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{e^{2x}}\right]$
- Answer: $4e^{e^{2x}}\left(e^{2x}\right)^{2} + 4e^{2x}e^{e^{2x}}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=2.5

### C=20 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[-\left(-e^{e^{2x}}\right)\right]$
- Answer: $4e^{e^{2x}}\left(e^{2x}\right)^{2} + 4e^{2x}e^{e^{2x}}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=20 · S=4 · amax=25 · shortfall=1.5

### C=20 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[-\left(-\ln\left(e^{e^{e^{2x}}}\right)\right)\right]$
- Answer: $4e^{e^{2x}}\left(e^{2x}\right)^{2} + 4e^{2x}e^{e^{2x}}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:ln_exp_id`
- Flags: C=20 · S=8 · amax=25 · shortfall=0.5

### C=20 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\frac{2\left(x-1\right)e^{\ln\left(e^{e^{2x}}\right)}}{2\left(x-1\right)}+5\right)-5\right]$
- Answer: $4e^{e^{2x}}\left(e^{2x}\right)^{2} + 4e^{2x}e^{e^{2x}}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=16 · amax=25

### C=20 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\frac{-\left(3+x\right)e^{\ln\left(e^{e^{2x}}\right)}}{-\left(3+x\right)}+\left(x-1\right)\right)-\left(x-1\right)\right]$
- Answer: $4e^{e^{2x}}\left(e^{2x}\right)^{2} + 4e^{2x}e^{e^{2x}}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=32 · amax=25

### C=25 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{e^{\left(2x + 1\right)}}\right]$
- Answer: $4e^{e^{\left(2x + 1\right)}}\left(e^{\left(2x + 1\right)}\right)^{2} + 4e^{\left(2x + 1\right)}e^{e^{\left(2x + 1\right)}}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=4.5

### C=25 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[-\left(-e^{e^{\left(2x + 1\right)}}\right)\right]$
- Answer: $4e^{e^{\left(2x + 1\right)}}\left(e^{\left(2x + 1\right)}\right)^{2} + 4e^{\left(2x + 1\right)}e^{e^{\left(2x + 1\right)}}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=25 · S=4 · amax=25 · shortfall=3.5

### C=25 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\left(-\left(-e^{e^{\left(2x + 1\right)}}\right)\right)+\left(-x+2\right)\right)-\left(-x+2\right)\right]$
- Answer: $4e^{e^{\left(2x + 1\right)}}\left(e^{\left(2x + 1\right)}\right)^{2} + 4e^{\left(2x + 1\right)}e^{e^{\left(2x + 1\right)}}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=8 · amax=25 · shortfall=2.5

### C=25 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\ln\left(e^{\left(\frac{\left(x+2\right)e^{e^{\left(2x + 1\right)}}}{x+2}+5-5\right)}\right)\right]$
- Answer: $4e^{e^{\left(2x + 1\right)}}\left(e^{\left(2x + 1\right)}\right)^{2} + 4e^{\left(2x + 1\right)}e^{e^{\left(2x + 1\right)}}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=16 · amax=25 · shortfall=1.5

### C=25 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{\ln\left(\frac{-\left(2-x\right)\left(\left(e^{e^{\left(2x + 1\right)}}+5\right)-5\right)}{-\left(2-x\right)}\right)}\right]$
- Answer: $4e^{e^{\left(2x + 1\right)}}\left(e^{\left(2x + 1\right)}\right)^{2} + 4e^{\left(2x + 1\right)}e^{e^{\left(2x + 1\right)}}$
- From: `form:higher_order_2` · `conceptual:chain+power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=32 · amax=25 · shortfall=1.5
