# Derivatives — ln / exp

**type_id:** `calc_diff_natural_logarithms_and_exponentials` · **leaf:** `derivative_ln_exp`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_exp`, `allow_log`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\frac{d}{dx}\left[\ln\left(\left(x + 2\right)\right)\right]$ | $\frac{d}{dx}\left[\left(\ln\left(\left(x + 2\right)\right)\right)+\left(x+2\right)-\left(x+2\right)\right]$ | $\frac{d}{dx}\left[\left(\frac{\left(x+2\right)\left(\ln\left(\left(x + 2\right)\right)\right)}{x+2}+\left(-2x+3\right)\right)-\left(-2x+3\right)\right]$ | $\frac{d}{dx}\left[\left(\left(\left(\left(\left(\left(\ln\left(\left(x + 2\right)\right)\right)+3\right)-3\right)+4\right)-4\right)+\left(x-2\right)\right)-\left(x-2\right)\right]$ | $\frac{d}{dx}\left[\ln\left(e^{\frac{4\left(x+3\right)e^{\ln\left(\left(\ln\left(\left(x + 2\right)\right)\right)\right)}}{4\left(x+3\right)}}\right)\right]$ |
| **C=4** | $\text{Find }\frac{d}{dx}\left(e^{2x}\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-e^{2x}\right)\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\ln\left(e^{e^{2x}}\right)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\ln\left(e^{\frac{2\left(x-1\right)\left(e^{2x}+2-2\right)}{2\left(x-1\right)}}\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\ln\left(e^{\left(\left(e^{2x}+4-4\right)+5-5\right)}\right)\right)$ |
| **C=8** | $\text{Find }\frac{d}{dx}\left(\ln\left(\left(4x + 4\right)\right)e^{\left(x + 3\right)}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{4\left(x+1\right)\left(\ln\left(\left(4x + 4\right)\right)e^{\left(x + 3\right)}\right)}{4\left(x+1\right)}\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\left(\left(\ln\left(\left(4x + 4\right)\right)e^{\left(x + 3\right)}\right)+\left(2x+2\right)\right)-\left(2x+2\right)+5\right)-5\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\frac{\left(x-1\right)\left(\ln\left(\left(4x + 4\right)\right)e^{\left(x + 3\right)}\right)}{x-1}+\left(-x+3\right)-\left(-x+3\right)\right)+4-4\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\left(x-1\right)\left(\left(\left(\left(\left(\ln\left(\left(4x + 4\right)\right)e^{\left(x + 3\right)}\right)+6\right)-6\right)+5\right)-5\right)}{x-1}\right)$ |
| **C=12** | $\frac{d}{dx}\left[e^{\left(3x + 5\right)}\right]$ | $\frac{d}{dx}\left[e^{\left(3x + 5\right)}+\left(-2x+2\right)-\left(-2x+2\right)\right]$ | $\frac{d}{dx}\left[\left(\left(e^{\left(3x + 5\right)}+4\right)-4\right)+\left(-x-2\right)-\left(-x-2\right)\right]$ | $\frac{d}{dx}\left[\frac{-\left(2+x\right)\ln\left(e^{e^{\left(3x + 5\right)}}\right)}{-\left(2+x\right)}+\left(x-1\right)-\left(x-1\right)\right]$ | $\frac{d}{dx}\left[-\left(-\frac{4\left(x-3\right)\left(e^{\left(3x + 5\right)}+\left(x+1\right)-\left(x+1\right)\right)}{4\left(x-3\right)}\right)\right]$ |
| **C=16** | $\frac{d}{dx}\left[e^{e^{\left(x - 3\right)}}e^{\left(4x - 3\right)}\right]$ | $\frac{d}{dx}\left[\frac{\left(x-2\right)e^{e^{\left(x - 3\right)}}e^{\left(4x - 3\right)}}{x-2}\right]$ | $\frac{d}{dx}\left[\frac{\left(x+3\right)\left(-\left(-e^{e^{\left(x - 3\right)}}e^{\left(4x - 3\right)}\right)\right)}{x+3}\right]$ | $\frac{d}{dx}\left[\frac{-\left(3-x\right)\left(\left(\ln\left(e^{e^{e^{\left(x - 3\right)}}e^{\left(4x - 3\right)}}\right)+4\right)-4\right)}{-\left(3-x\right)}\right]$ | $\frac{d}{dx}\left[\left(\left(-\left(-\frac{-\left(2+x\right)e^{e^{\left(x - 3\right)}}e^{\left(4x - 3\right)}}{-\left(2+x\right)}\right)\right)+4\right)-4\right]$ |
| **C=20** | $\text{Find }\frac{d}{dx}\left(\ln^{3}(4x)\right)$ | $\text{Find }\frac{d}{dx}\left(\ln^{3}(4x)+6-6\right)$ | $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\left(\ln^{3}(4x)+\left(-x-2\right)-\left(-x-2\right)\right)\right)}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\left(x-3\right)\ln\left(e^{\left(\ln^{3}(4x)+6-6\right)}\right)}{x-3}\right)$ | $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\frac{\left(x+1\right)\left(-\left(-\ln^{3}(4x)\right)\right)}{x+1}\right)}\right)$ |
| **C=25** | $\frac{d^{2}}{dx^{2}}\left[\ln^{2}(x)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{2\left(x-2\right)\ln^{2}(x)}{2\left(x-2\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{-\left(1-x\right)\left(\ln^{2}(x)+\left(3x-1\right)-\left(3x-1\right)\right)}{-\left(1-x\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[\ln\left(e^{\left(-\left(-\ln^{2}(x)\right)\right)}\right)+\left(x+3\right)-\left(x+3\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{2\left(x-1\right)\left(e^{\ln\left(\ln^{2}(x)\right)}+3-3\right)}{2\left(x-1\right)}\right]$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\frac{1}{\left(x + 2\right)}$ | $\frac{1}{\left(x + 2\right)}$ | $\frac{1}{\left(x + 2\right)}$ | $\frac{1}{\left(x + 2\right)}$ | $\frac{1}{\left(x + 2\right)}$ |
| **C=4** | $2e^{2x}$ | $2e^{2x}$ | $2e^{2x}$ | $2e^{2x}$ | $2e^{2x}$ |
| **C=8** | $4\frac{1}{\left(4x + 4\right)}e^{\left(x + 3\right)} + e^{\left(x + 3\right)}\ln\left(\left(4x + 4\right)\right)$ | $4\frac{1}{\left(4x + 4\right)}e^{\left(x + 3\right)} + e^{\left(x + 3\right)}\ln\left(\left(4x + 4\right)\right)$ | $4\frac{1}{\left(4x + 4\right)}e^{\left(x + 3\right)} + e^{\left(x + 3\right)}\ln\left(\left(4x + 4\right)\right)$ | $4\frac{1}{\left(4x + 4\right)}e^{\left(x + 3\right)} + e^{\left(x + 3\right)}\ln\left(\left(4x + 4\right)\right)$ | $4\frac{1}{\left(4x + 4\right)}e^{\left(x + 3\right)} + e^{\left(x + 3\right)}\ln\left(\left(4x + 4\right)\right)$ |
| **C=12** | $e^{\left(3x + 5\right)}\left(3\right)$ | $e^{\left(3x + 5\right)}\left(3\right)$ | $e^{\left(3x + 5\right)}\left(3\right)$ | $e^{\left(3x + 5\right)}\left(3\right)$ | $e^{\left(3x + 5\right)}\left(3\right)$ |
| **C=16** | $e^{e^{\left(x - 3\right)}}e^{\left(x - 3\right)}e^{\left(4x - 3\right)} + 4e^{\left(4x - 3\right)}e^{e^{\left(x - 3\right)}}$ | $e^{e^{\left(x - 3\right)}}e^{\left(x - 3\right)}e^{\left(4x - 3\right)} + 4e^{\left(4x - 3\right)}e^{e^{\left(x - 3\right)}}$ | $e^{e^{\left(x - 3\right)}}e^{\left(x - 3\right)}e^{\left(4x - 3\right)} + 4e^{\left(4x - 3\right)}e^{e^{\left(x - 3\right)}}$ | $e^{e^{\left(x - 3\right)}}e^{\left(x - 3\right)}e^{\left(4x - 3\right)} + 4e^{\left(4x - 3\right)}e^{e^{\left(x - 3\right)}}$ | $e^{e^{\left(x - 3\right)}}e^{\left(x - 3\right)}e^{\left(4x - 3\right)} + 4e^{\left(4x - 3\right)}e^{e^{\left(x - 3\right)}}$ |
| **C=20** | $3\left(\ln\left(4x\right)\right)^{2}\left(\frac{4}{4x}\right)$ | $3\left(\ln\left(4x\right)\right)^{2}\left(\frac{4}{4x}\right)$ | $3\left(\ln\left(4x\right)\right)^{2}\left(\frac{4}{4x}\right)$ | $3\left(\ln\left(4x\right)\right)^{2}\left(\frac{4}{4x}\right)$ | $3\left(\ln\left(4x\right)\right)^{2}\left(\frac{4}{4x}\right)$ |
| **C=25** | $2x^{-2} - 2\ln(x)x^{-2}$ | $2x^{-2} - 2\ln(x)x^{-2}$ | $2x^{-2} - 2\ln(x)x^{-2}$ | $2x^{-2} - 2\ln(x)x^{-2}$ | $2x^{-2} - 2\ln(x)x^{-2}$ |

## Cell detail

### C=0 · S=0

- Prompt: $\frac{d}{dx}\left[\ln\left(\left(x + 2\right)\right)\right]$
- Answer: $\frac{1}{\left(x + 2\right)}$
- From: `form:exp_basic` · `conceptual:chain+power` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\frac{d}{dx}\left[\left(\ln\left(\left(x + 2\right)\right)\right)+\left(x+2\right)-\left(x+2\right)\right]$
- Answer: $\frac{1}{\left(x + 2\right)}$
- From: `form:exp_basic` · `conceptual:chain+power` · `effort:add_cancel_linear` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\frac{d}{dx}\left[\left(\frac{\left(x+2\right)\left(\ln\left(\left(x + 2\right)\right)\right)}{x+2}+\left(-2x+3\right)\right)-\left(-2x+3\right)\right]$
- Answer: $\frac{1}{\left(x + 2\right)}$
- From: `form:exp_basic` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\frac{d}{dx}\left[\left(\left(\left(\left(\left(\left(\ln\left(\left(x + 2\right)\right)\right)+3\right)-3\right)+4\right)-4\right)+\left(x-2\right)\right)-\left(x-2\right)\right]$
- Answer: $\frac{1}{\left(x + 2\right)}$
- From: `form:exp_basic` · `conceptual:chain+power` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\frac{d}{dx}\left[\ln\left(e^{\frac{4\left(x+3\right)e^{\ln\left(\left(\ln\left(\left(x + 2\right)\right)\right)\right)}}{4\left(x+3\right)}}\right)\right]$
- Answer: $\frac{1}{\left(x + 2\right)}$
- From: `form:exp_basic` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:exp_ln_id` · `prereq:cancel_quot_bait`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(e^{2x}\right)$
- Answer: $2e^{2x}$
- From: `form:product_poly_exp` · `conceptual:chain+power` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-e^{2x}\right)\right)$
- Answer: $2e^{2x}$
- From: `form:product_poly_exp` · `conceptual:chain+power` · `effort:double_neg` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\ln\left(e^{e^{2x}}\right)\right)\right)$
- Answer: $2e^{2x}$
- From: `form:product_poly_exp` · `conceptual:chain+power` · `effort:double_neg` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:ln_exp_id` · `effort:double_neg`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\ln\left(e^{\frac{2\left(x-1\right)\left(e^{2x}+2-2\right)}{2\left(x-1\right)}}\right)\right)$
- Answer: $2e^{2x}$
- From: `form:product_poly_exp` · `conceptual:chain+power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\ln\left(e^{\left(\left(e^{2x}+4-4\right)+5-5\right)}\right)\right)$
- Answer: $2e^{2x}$
- From: `form:product_poly_exp` · `conceptual:chain+power` · `effort:add_cancel_const` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:add_cancel_const`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\ln\left(\left(4x + 4\right)\right)e^{\left(x + 3\right)}\right)$
- Answer: $4\frac{1}{\left(4x + 4\right)}e^{\left(x + 3\right)} + e^{\left(x + 3\right)}\ln\left(\left(4x + 4\right)\right)$
- From: `form:ln_basic` · `conceptual:chain+power+product` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25

### C=8 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{4\left(x+1\right)\left(\ln\left(\left(4x + 4\right)\right)e^{\left(x + 3\right)}\right)}{4\left(x+1\right)}\right)$
- Answer: $4\frac{1}{\left(4x + 4\right)}e^{\left(x + 3\right)} + e^{\left(x + 3\right)}\ln\left(\left(4x + 4\right)\right)$
- From: `form:ln_basic` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\left(\left(\ln\left(\left(4x + 4\right)\right)e^{\left(x + 3\right)}\right)+\left(2x+2\right)\right)-\left(2x+2\right)+5\right)-5\right)$
- Answer: $4\frac{1}{\left(4x + 4\right)}e^{\left(x + 3\right)} + e^{\left(x + 3\right)}\ln\left(\left(4x + 4\right)\right)$
- From: `form:ln_basic` · `conceptual:chain+power+product` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\frac{\left(x-1\right)\left(\ln\left(\left(4x + 4\right)\right)e^{\left(x + 3\right)}\right)}{x-1}+\left(-x+3\right)-\left(-x+3\right)\right)+4-4\right)$
- Answer: $4\frac{1}{\left(4x + 4\right)}e^{\left(x + 3\right)} + e^{\left(x + 3\right)}\ln\left(\left(4x + 4\right)\right)$
- From: `form:ln_basic` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\left(x-1\right)\left(\left(\left(\left(\left(\ln\left(\left(4x + 4\right)\right)e^{\left(x + 3\right)}\right)+6\right)-6\right)+5\right)-5\right)}{x-1}\right)$
- Answer: $4\frac{1}{\left(4x + 4\right)}e^{\left(x + 3\right)} + e^{\left(x + 3\right)}\ln\left(\left(4x + 4\right)\right)$
- From: `form:ln_basic` · `conceptual:chain+power+product` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\frac{d}{dx}\left[e^{\left(3x + 5\right)}\right]$
- Answer: $e^{\left(3x + 5\right)}\left(3\right)$
- From: `form:ln_exp_product` · `conceptual:chain+power` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25

### C=12 · S=4

- Prompt: $\frac{d}{dx}\left[e^{\left(3x + 5\right)}+\left(-2x+2\right)-\left(-2x+2\right)\right]$
- Answer: $e^{\left(3x + 5\right)}\left(3\right)$
- From: `form:ln_exp_product` · `conceptual:chain+power` · `effort:add_cancel_linear` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=12 · S=4 · amax=25

### C=12 · S=8

- Prompt: $\frac{d}{dx}\left[\left(\left(e^{\left(3x + 5\right)}+4\right)-4\right)+\left(-x-2\right)-\left(-x-2\right)\right]$
- Answer: $e^{\left(3x + 5\right)}\left(3\right)$
- From: `form:ln_exp_product` · `conceptual:chain+power` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=12 · S=8 · amax=25

### C=12 · S=16

- Prompt: $\frac{d}{dx}\left[\frac{-\left(2+x\right)\ln\left(e^{e^{\left(3x + 5\right)}}\right)}{-\left(2+x\right)}+\left(x-1\right)-\left(x-1\right)\right]$
- Answer: $e^{\left(3x + 5\right)}\left(3\right)$
- From: `form:ln_exp_product` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:ln_exp_id`
- Flags: C=12 · S=16 · amax=25

### C=12 · S=32

- Prompt: $\frac{d}{dx}\left[-\left(-\frac{4\left(x-3\right)\left(e^{\left(3x + 5\right)}+\left(x+1\right)-\left(x+1\right)\right)}{4\left(x-3\right)}\right)\right]$
- Answer: $e^{\left(3x + 5\right)}\left(3\right)$
- From: `form:ln_exp_product` · `conceptual:chain+power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=32 · amax=25

### C=16 · S=0

- Prompt: $\frac{d}{dx}\left[e^{e^{\left(x - 3\right)}}e^{\left(4x - 3\right)}\right]$
- Answer: $e^{e^{\left(x - 3\right)}}e^{\left(x - 3\right)}e^{\left(4x - 3\right)} + 4e^{\left(4x - 3\right)}e^{e^{\left(x - 3\right)}}$
- From: `form:ln_basic` · `conceptual:chain+power+product` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=1.5

### C=16 · S=4

- Prompt: $\frac{d}{dx}\left[\frac{\left(x-2\right)e^{e^{\left(x - 3\right)}}e^{\left(4x - 3\right)}}{x-2}\right]$
- Answer: $e^{e^{\left(x - 3\right)}}e^{\left(x - 3\right)}e^{\left(4x - 3\right)} + 4e^{\left(4x - 3\right)}e^{e^{\left(x - 3\right)}}$
- From: `form:ln_basic` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=16 · S=4 · amax=25 · shortfall=0.5

### C=16 · S=8

- Prompt: $\frac{d}{dx}\left[\frac{\left(x+3\right)\left(-\left(-e^{e^{\left(x - 3\right)}}e^{\left(4x - 3\right)}\right)\right)}{x+3}\right]$
- Answer: $e^{e^{\left(x - 3\right)}}e^{\left(x - 3\right)}e^{\left(4x - 3\right)} + 4e^{\left(4x - 3\right)}e^{e^{\left(x - 3\right)}}$
- From: `form:ln_basic` · `conceptual:chain+power+product` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=16 · S=8 · amax=25

### C=16 · S=16

- Prompt: $\frac{d}{dx}\left[\frac{-\left(3-x\right)\left(\left(\ln\left(e^{e^{e^{\left(x - 3\right)}}e^{\left(4x - 3\right)}}\right)+4\right)-4\right)}{-\left(3-x\right)}\right]$
- Answer: $e^{e^{\left(x - 3\right)}}e^{\left(x - 3\right)}e^{\left(4x - 3\right)} + 4e^{\left(4x - 3\right)}e^{e^{\left(x - 3\right)}}$
- From: `form:ln_basic` · `conceptual:chain+power+product` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:ln_exp_id`
- Flags: C=16 · S=16 · amax=25

### C=16 · S=32

- Prompt: $\frac{d}{dx}\left[\left(\left(-\left(-\frac{-\left(2+x\right)e^{e^{\left(x - 3\right)}}e^{\left(4x - 3\right)}}{-\left(2+x\right)}\right)\right)+4\right)-4\right]$
- Answer: $e^{e^{\left(x - 3\right)}}e^{\left(x - 3\right)}e^{\left(4x - 3\right)} + 4e^{\left(4x - 3\right)}e^{e^{\left(x - 3\right)}}$
- From: `form:ln_basic` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=32 · amax=25

### C=20 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\ln^{3}(4x)\right)$
- Answer: $3\left(\ln\left(4x\right)\right)^{2}\left(\frac{4}{4x}\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=1

### C=20 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\ln^{3}(4x)+6-6\right)$
- Answer: $3\left(\ln\left(4x\right)\right)^{2}\left(\frac{4}{4x}\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power` · `effort:add_cancel_const` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=20 · S=4 · amax=25

### C=20 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\left(\ln^{3}(4x)+\left(-x-2\right)-\left(-x-2\right)\right)\right)}\right)$
- Answer: $3\left(\ln\left(4x\right)\right)^{2}\left(\frac{4}{4x}\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power` · `effort:add_cancel_linear` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `prereq:exp_ln_id`
- Flags: C=20 · S=8 · amax=25

### C=20 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\left(x-3\right)\ln\left(e^{\left(\ln^{3}(4x)+6-6\right)}\right)}{x-3}\right)$
- Answer: $3\left(\ln\left(4x\right)\right)^{2}\left(\frac{4}{4x}\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=20 · S=16 · amax=25

### C=20 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\frac{\left(x+1\right)\left(-\left(-\ln^{3}(4x)\right)\right)}{x+1}\right)}\right)$
- Answer: $3\left(\ln\left(4x\right)\right)^{2}\left(\frac{4}{4x}\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=20 · S=32 · amax=25

### C=25 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\ln^{2}(x)\right]$
- Answer: $2x^{-2} - 2\ln(x)x^{-2}$
- From: `form:exp_basic` · `conceptual:chain+power` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=10

### C=25 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{2\left(x-2\right)\ln^{2}(x)}{2\left(x-2\right)}\right]$
- Answer: $2x^{-2} - 2\ln(x)x^{-2}$
- From: `form:exp_basic` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=25 · S=4 · amax=25 · shortfall=9

### C=25 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{-\left(1-x\right)\left(\ln^{2}(x)+\left(3x-1\right)-\left(3x-1\right)\right)}{-\left(1-x\right)}\right]$
- Answer: $2x^{-2} - 2\ln(x)x^{-2}$
- From: `form:exp_basic` · `conceptual:chain+power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=25 · S=8 · amax=25 · shortfall=8

### C=25 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\ln\left(e^{\left(-\left(-\ln^{2}(x)\right)\right)}\right)+\left(x+3\right)-\left(x+3\right)\right]$
- Answer: $2x^{-2} - 2\ln(x)x^{-2}$
- From: `form:exp_basic` · `conceptual:chain+power` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=25 · S=16 · amax=25 · shortfall=7

### C=25 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{2\left(x-1\right)\left(e^{\ln\left(\ln^{2}(x)\right)}+3-3\right)}{2\left(x-1\right)}\right]$
- Answer: $2x^{-2} - 2\ln(x)x^{-2}$
- From: `form:exp_basic` · `conceptual:chain+power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:exp_ln_id`
- Flags: C=25 · S=32 · amax=25 · shortfall=7
