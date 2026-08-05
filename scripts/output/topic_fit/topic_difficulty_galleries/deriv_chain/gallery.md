# Derivatives — chain rule

**type_id:** `calc_diff_chain_rule` · **leaf:** `derivative_chain_rule`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_exp`, `allow_invtrig`, `allow_log`, `allow_roots`, `allow_trig`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\frac{d}{dx}\left[\sqrt{2x}\right]$ | $\frac{d}{dx}\left[\ln\left(e^{\sqrt{2x}}\right)\right]$ | $\frac{d}{dx}\left[\frac{\left(x-1\right)\sqrt{2x}}{x-1}+\left(2x+2\right)-\left(2x+2\right)\right]$ | $\frac{d}{dx}\left[\frac{2\left(x-2\right)\left(-\left(-\left(\left(\sqrt{2x}+1\right)-1\right)\right)\right)}{2\left(x-2\right)}\right]$ | $\frac{d}{dx}\left[e^{\ln\left(\left(-\left(-\frac{2\left(x-2\right)\sqrt{2x}}{2\left(x-2\right)}\right)\right)\right)}\right]$ |
| **C=4** | $\text{Find }\frac{d}{dx}\left(\left(2x^{3} + x - 3\right)^{3}\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\left(2x^{3} + x - 3\right)^{3}\right)+4-4\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{4\left(x-1\right)e^{\ln\left(\left(\left(2x^{3} + x - 3\right)^{3}\right)\right)}}{4\left(x-1\right)}\right)$ | $\text{Find }\frac{d}{dx}\left(\left(-\left(-\left(\left(\left(2x^{3} + x - 3\right)^{3}\right)+6-6\right)\right)\right)+\left(2x+3\right)-\left(2x+3\right)\right)$ | $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\frac{-\left(1+x\right)\left(\left(2x^{3} + x - 3\right)^{3}\right)}{-\left(1+x\right)}\right)}+2-2\right)$ |
| **C=8** | $\text{Find }\frac{d}{dx}\left(\arcsin^{3}(x)\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\left(x-1\right)\arcsin^{3}(x)}{x-1}\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\arcsin^{3}(x)+\left(-2x+2\right)\right)-\left(-2x+2\right)+6-6\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\frac{\left(x-2\right)\left(\left(\arcsin^{3}(x)+1\right)-1\right)}{x-2}\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\frac{\left(x-1\right)\left(-\left(-\arcsin^{3}(x)\right)\right)}{x-1}+4\right)-4\right)$ |
| **C=12** | $\frac{d}{dx}\left[\ln^{2}(5x)\right]$ | $\frac{d}{dx}\left[\left(\ln^{2}(5x)+3\right)-3\right]$ | $\frac{d}{dx}\left[e^{\ln\left(\frac{4\left(x+2\right)\ln^{2}(5x)}{4\left(x+2\right)}\right)}\right]$ | $\frac{d}{dx}\left[\frac{\left(x-2\right)\ln\left(e^{\left(-\left(-\ln^{2}(5x)\right)\right)}\right)}{x-2}\right]$ | $\frac{d}{dx}\left[-\left(-\ln\left(e^{\left(\ln^{2}(5x)+\left(-x+1\right)-\left(-x+1\right)\right)}\right)\right)\right]$ |
| **C=16** | $\frac{d}{dx}\left[\ln\left(\left(x - 5\right)\right)\arccos^{2}(4x)\right]$ | $\frac{d}{dx}\left[\frac{2\left(x-1\right)\left(\ln\left(\left(x - 5\right)\right)\arccos^{2}(4x)\right)}{2\left(x-1\right)}\right]$ | $\frac{d}{dx}\left[\left(-\left(-\left(\ln\left(\left(x - 5\right)\right)\arccos^{2}(4x)\right)\right)\right)+\left(3x-2\right)-\left(3x-2\right)\right]$ | $\frac{d}{dx}\left[\left(\left(\frac{2\left(x+2\right)\left(\ln\left(\left(x - 5\right)\right)\arccos^{2}(4x)\right)}{2\left(x+2\right)}+3\right)-3\right)+5-5\right]$ | $\frac{d}{dx}\left[\left(\ln\left(e^{e^{\ln\left(\left(\ln\left(\left(x - 5\right)\right)\arccos^{2}(4x)\right)\right)}}\right)+\left(x\right)\right)-\left(x\right)\right]$ |
| **C=20** | $\frac{d}{dx}\left[\arccos(x)\arcsin(x)\right]$ | $\frac{d}{dx}\left[e^{\ln\left(\arccos(x)\arcsin(x)\right)}\right]$ | $\frac{d}{dx}\left[\left(\ln\left(e^{\arccos(x)\arcsin(x)}\right)+\left(x+2\right)\right)-\left(x+2\right)\right]$ | $\frac{d}{dx}\left[-\left(-\ln\left(e^{\frac{\left(x-1\right)\arccos(x)\arcsin(x)}{x-1}}\right)\right)\right]$ | $\frac{d}{dx}\left[\left(\left(\arccos(x)\arcsin(x)+3-3\right)+4-4\right)+3-3\right]$ |
| **C=25** | $\frac{d^{2}}{dx^{2}}\left[e^{\cos(x)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(e^{\cos(x)}+\left(-x+3\right)\right)-\left(-x+3\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[e^{\ln\left(\left(-\left(-e^{\cos(x)}\right)\right)\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{4\left(x-2\right)\ln\left(e^{e^{\cos(x)}}\right)}{4\left(x-2\right)}+\left(-2x+2\right)-\left(-2x+2\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\ln\left(e^{\left(e^{\cos(x)}+6-6\right)+\left(-2x-1\right)-\left(-2x-1\right)}\right)\right]$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\frac{2}{2\sqrt{2x}}$ | $\frac{2}{2\sqrt{2x}}$ | $\frac{2}{2\sqrt{2x}}$ | $\frac{2}{2\sqrt{2x}}$ | $\frac{2}{2\sqrt{2x}}$ |
| **C=4** | $3\left(2x^{3} + x - 3\right)^{2}\left(6x^{2} + 1\right)$ | $3\left(2x^{3} + x - 3\right)^{2}\left(6x^{2} + 1\right)$ | $3\left(2x^{3} + x - 3\right)^{2}\left(6x^{2} + 1\right)$ | $3\left(2x^{3} + x - 3\right)^{2}\left(6x^{2} + 1\right)$ | $3\left(2x^{3} + x - 3\right)^{2}\left(6x^{2} + 1\right)$ |
| **C=8** | $3\left(\arcsin(x)\right)^{2}\left(\frac{1}{\sqrt{1-x^{2}}}\right)$ | $3\left(\arcsin(x)\right)^{2}\left(\frac{1}{\sqrt{1-x^{2}}}\right)$ | $3\left(\arcsin(x)\right)^{2}\left(\frac{1}{\sqrt{1-x^{2}}}\right)$ | $3\left(\arcsin(x)\right)^{2}\left(\frac{1}{\sqrt{1-x^{2}}}\right)$ | $3\left(\arcsin(x)\right)^{2}\left(\frac{1}{\sqrt{1-x^{2}}}\right)$ |
| **C=12** | $2\left(\ln\left(5x\right)\right)\left(\frac{5}{5x}\right)$ | $2\left(\ln\left(5x\right)\right)\left(\frac{5}{5x}\right)$ | $2\left(\ln\left(5x\right)\right)\left(\frac{5}{5x}\right)$ | $2\left(\ln\left(5x\right)\right)\left(\frac{5}{5x}\right)$ | $2\left(\ln\left(5x\right)\right)\left(\frac{5}{5x}\right)$ |
| **C=16** | $\frac{1}{\left(x - 5\right)}\arccos^{2}(4x) + 8\arccos(4x)\left(-\frac{1}{\sqrt{1-(4x)^{2}}}\right)\ln\left(\left(x - 5\right)\right)$ | $\frac{1}{\left(x - 5\right)}\arccos^{2}(4x) + 8\arccos(4x)\left(-\frac{1}{\sqrt{1-(4x)^{2}}}\right)\ln\left(\left(x - 5\right)\right)$ | $\frac{1}{\left(x - 5\right)}\arccos^{2}(4x) + 8\arccos(4x)\left(-\frac{1}{\sqrt{1-(4x)^{2}}}\right)\ln\left(\left(x - 5\right)\right)$ | $\frac{1}{\left(x - 5\right)}\arccos^{2}(4x) + 8\arccos(4x)\left(-\frac{1}{\sqrt{1-(4x)^{2}}}\right)\ln\left(\left(x - 5\right)\right)$ | $\frac{1}{\left(x - 5\right)}\arccos^{2}(4x) + 8\arccos(4x)\left(-\frac{1}{\sqrt{1-(4x)^{2}}}\right)\ln\left(\left(x - 5\right)\right)$ |
| **C=20** | $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arccos(x)$ | $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arccos(x)$ | $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arccos(x)$ | $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arccos(x)$ | $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arccos(x)$ |
| **C=25** | $e^{\cos(x)}\sin^{2}(x) - \cos(x)e^{\cos(x)}$ | $e^{\cos(x)}\sin^{2}(x) - \cos(x)e^{\cos(x)}$ | $e^{\cos(x)}\sin^{2}(x) - \cos(x)e^{\cos(x)}$ | $e^{\cos(x)}\sin^{2}(x) - \cos(x)e^{\cos(x)}$ | $e^{\cos(x)}\sin^{2}(x) - \cos(x)e^{\cos(x)}$ |

## Cell detail

### C=0 · S=0

- Prompt: $\frac{d}{dx}\left[\sqrt{2x}\right]$
- Answer: $\frac{2}{2\sqrt{2x}}$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\frac{d}{dx}\left[\ln\left(e^{\sqrt{2x}}\right)\right]$
- Answer: $\frac{2}{2\sqrt{2x}}$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\frac{d}{dx}\left[\frac{\left(x-1\right)\sqrt{2x}}{x-1}+\left(2x+2\right)-\left(2x+2\right)\right]$
- Answer: $\frac{2}{2\sqrt{2x}}$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\frac{d}{dx}\left[\frac{2\left(x-2\right)\left(-\left(-\left(\left(\sqrt{2x}+1\right)-1\right)\right)\right)}{2\left(x-2\right)}\right]$
- Answer: $\frac{2}{2\sqrt{2x}}$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `effort:add_cancel_const` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\frac{d}{dx}\left[e^{\ln\left(\left(-\left(-\frac{2\left(x-2\right)\sqrt{2x}}{2\left(x-2\right)}\right)\right)\right)}\right]$
- Answer: $\frac{2}{2\sqrt{2x}}$
- From: `form:chain_trig_poly` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(2x^{3} + x - 3\right)^{3}\right)$
- Answer: $3\left(2x^{3} + x - 3\right)^{2}\left(6x^{2} + 1\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\left(2x^{3} + x - 3\right)^{3}\right)+4-4\right)$
- Answer: $3\left(2x^{3} + x - 3\right)^{2}\left(6x^{2} + 1\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{4\left(x-1\right)e^{\ln\left(\left(\left(2x^{3} + x - 3\right)^{3}\right)\right)}}{4\left(x-1\right)}\right)$
- Answer: $3\left(2x^{3} + x - 3\right)^{2}\left(6x^{2} + 1\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(-\left(-\left(\left(\left(2x^{3} + x - 3\right)^{3}\right)+6-6\right)\right)\right)+\left(2x+3\right)-\left(2x+3\right)\right)$
- Answer: $3\left(2x^{3} + x - 3\right)^{2}\left(6x^{2} + 1\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `effort:add_cancel_const` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\frac{-\left(1+x\right)\left(\left(2x^{3} + x - 3\right)^{3}\right)}{-\left(1+x\right)}\right)}+2-2\right)$
- Answer: $3\left(2x^{3} + x - 3\right)^{2}\left(6x^{2} + 1\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\arcsin^{3}(x)\right)$
- Answer: $3\left(\arcsin(x)\right)^{2}\left(\frac{1}{\sqrt{1-x^{2}}}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25

### C=8 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\left(x-1\right)\arcsin^{3}(x)}{x-1}\right)$
- Answer: $3\left(\arcsin(x)\right)^{2}\left(\frac{1}{\sqrt{1-x^{2}}}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\arcsin^{3}(x)+\left(-2x+2\right)\right)-\left(-2x+2\right)+6-6\right)$
- Answer: $3\left(\arcsin(x)\right)^{2}\left(\frac{1}{\sqrt{1-x^{2}}}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\frac{\left(x-2\right)\left(\left(\arcsin^{3}(x)+1\right)-1\right)}{x-2}\right)\right)$
- Answer: $3\left(\arcsin(x)\right)^{2}\left(\frac{1}{\sqrt{1-x^{2}}}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\frac{\left(x-1\right)\left(-\left(-\arcsin^{3}(x)\right)\right)}{x-1}+4\right)-4\right)$
- Answer: $3\left(\arcsin(x)\right)^{2}\left(\frac{1}{\sqrt{1-x^{2}}}\right)$
- From: `form:chain_power_linear` · `conceptual:chain+power` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\frac{d}{dx}\left[\ln^{2}(5x)\right]$
- Answer: $2\left(\ln\left(5x\right)\right)\left(\frac{5}{5x}\right)$
- From: `form:chain_nested` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25

### C=12 · S=4

- Prompt: $\frac{d}{dx}\left[\left(\ln^{2}(5x)+3\right)-3\right]$
- Answer: $2\left(\ln\left(5x\right)\right)\left(\frac{5}{5x}\right)$
- From: `form:chain_nested` · `conceptual:chain+power` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=12 · S=4 · amax=25

### C=12 · S=8

- Prompt: $\frac{d}{dx}\left[e^{\ln\left(\frac{4\left(x+2\right)\ln^{2}(5x)}{4\left(x+2\right)}\right)}\right]$
- Answer: $2\left(\ln\left(5x\right)\right)\left(\frac{5}{5x}\right)$
- From: `form:chain_nested` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=12 · S=8 · amax=25

### C=12 · S=16

- Prompt: $\frac{d}{dx}\left[\frac{\left(x-2\right)\ln\left(e^{\left(-\left(-\ln^{2}(5x)\right)\right)}\right)}{x-2}\right]$
- Answer: $2\left(\ln\left(5x\right)\right)\left(\frac{5}{5x}\right)$
- From: `form:chain_nested` · `conceptual:chain+power` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=12 · S=16 · amax=25

### C=12 · S=32

- Prompt: $\frac{d}{dx}\left[-\left(-\ln\left(e^{\left(\ln^{2}(5x)+\left(-x+1\right)-\left(-x+1\right)\right)}\right)\right)\right]$
- Answer: $2\left(\ln\left(5x\right)\right)\left(\frac{5}{5x}\right)$
- From: `form:chain_nested` · `conceptual:chain+power` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=12 · S=32 · amax=25

### C=16 · S=0

- Prompt: $\frac{d}{dx}\left[\ln\left(\left(x - 5\right)\right)\arccos^{2}(4x)\right]$
- Answer: $\frac{1}{\left(x - 5\right)}\arccos^{2}(4x) + 8\arccos(4x)\left(-\frac{1}{\sqrt{1-(4x)^{2}}}\right)\ln\left(\left(x - 5\right)\right)$
- From: `form:chain_nested` · `conceptual:chain+power+product` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25

### C=16 · S=4

- Prompt: $\frac{d}{dx}\left[\frac{2\left(x-1\right)\left(\ln\left(\left(x - 5\right)\right)\arccos^{2}(4x)\right)}{2\left(x-1\right)}\right]$
- Answer: $\frac{1}{\left(x - 5\right)}\arccos^{2}(4x) + 8\arccos(4x)\left(-\frac{1}{\sqrt{1-(4x)^{2}}}\right)\ln\left(\left(x - 5\right)\right)$
- From: `form:chain_nested` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=16 · S=4 · amax=25

### C=16 · S=8

- Prompt: $\frac{d}{dx}\left[\left(-\left(-\left(\ln\left(\left(x - 5\right)\right)\arccos^{2}(4x)\right)\right)\right)+\left(3x-2\right)-\left(3x-2\right)\right]$
- Answer: $\frac{1}{\left(x - 5\right)}\arccos^{2}(4x) + 8\arccos(4x)\left(-\frac{1}{\sqrt{1-(4x)^{2}}}\right)\ln\left(\left(x - 5\right)\right)$
- From: `form:chain_nested` · `conceptual:chain+power+product` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=16 · S=8 · amax=25

### C=16 · S=16

- Prompt: $\frac{d}{dx}\left[\left(\left(\frac{2\left(x+2\right)\left(\ln\left(\left(x - 5\right)\right)\arccos^{2}(4x)\right)}{2\left(x+2\right)}+3\right)-3\right)+5-5\right]$
- Answer: $\frac{1}{\left(x - 5\right)}\arccos^{2}(4x) + 8\arccos(4x)\left(-\frac{1}{\sqrt{1-(4x)^{2}}}\right)\ln\left(\left(x - 5\right)\right)$
- From: `form:chain_nested` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=16 · S=16 · amax=25

### C=16 · S=32

- Prompt: $\frac{d}{dx}\left[\left(\ln\left(e^{e^{\ln\left(\left(\ln\left(\left(x - 5\right)\right)\arccos^{2}(4x)\right)\right)}}\right)+\left(x\right)\right)-\left(x\right)\right]$
- Answer: $\frac{1}{\left(x - 5\right)}\arccos^{2}(4x) + 8\arccos(4x)\left(-\frac{1}{\sqrt{1-(4x)^{2}}}\right)\ln\left(\left(x - 5\right)\right)$
- From: `form:chain_nested` · `conceptual:chain+power+product` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=16 · S=32 · amax=25

### C=20 · S=0

- Prompt: $\frac{d}{dx}\left[\arccos(x)\arcsin(x)\right]$
- Answer: $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arccos(x)$
- From: `form:chain_trig_poly` · `conceptual:power+product` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=5.5

### C=20 · S=4

- Prompt: $\frac{d}{dx}\left[e^{\ln\left(\arccos(x)\arcsin(x)\right)}\right]$
- Answer: $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arccos(x)$
- From: `form:chain_trig_poly` · `conceptual:power+product` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=4 · amax=25 · shortfall=4.5

### C=20 · S=8

- Prompt: $\frac{d}{dx}\left[\left(\ln\left(e^{\arccos(x)\arcsin(x)}\right)+\left(x+2\right)\right)-\left(x+2\right)\right]$
- Answer: $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arccos(x)$
- From: `form:chain_trig_poly` · `conceptual:power+product` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=20 · S=8 · amax=25 · shortfall=3.5

### C=20 · S=16

- Prompt: $\frac{d}{dx}\left[-\left(-\ln\left(e^{\frac{\left(x-1\right)\arccos(x)\arcsin(x)}{x-1}}\right)\right)\right]$
- Answer: $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arccos(x)$
- From: `form:chain_trig_poly` · `conceptual:power+product` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=20 · S=16 · amax=25 · shortfall=2.5

### C=20 · S=32

- Prompt: $\frac{d}{dx}\left[\left(\left(\arccos(x)\arcsin(x)+3-3\right)+4-4\right)+3-3\right]$
- Answer: $\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arccos(x)$
- From: `form:chain_trig_poly` · `conceptual:power+product` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=20 · S=32 · amax=25 · shortfall=2.5

### C=25 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{\cos(x)}\right]$
- Answer: $e^{\cos(x)}\sin^{2}(x) - \cos(x)e^{\cos(x)}$
- From: `form:chain_nested` · `conceptual:chain+power` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=2

### C=25 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(e^{\cos(x)}+\left(-x+3\right)\right)-\left(-x+3\right)\right]$
- Answer: $e^{\cos(x)}\sin^{2}(x) - \cos(x)e^{\cos(x)}$
- From: `form:chain_nested` · `conceptual:chain+power` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=4 · amax=25 · shortfall=1

### C=25 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[e^{\ln\left(\left(-\left(-e^{\cos(x)}\right)\right)\right)}\right]$
- Answer: $e^{\cos(x)}\sin^{2}(x) - \cos(x)e^{\cos(x)}$
- From: `form:chain_nested` · `conceptual:chain+power` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=8 · amax=25

### C=25 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{4\left(x-2\right)\ln\left(e^{e^{\cos(x)}}\right)}{4\left(x-2\right)}+\left(-2x+2\right)-\left(-2x+2\right)\right]$
- Answer: $e^{\cos(x)}\sin^{2}(x) - \cos(x)e^{\cos(x)}$
- From: `form:chain_nested` · `conceptual:chain+power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=25 · S=16 · amax=25

### C=25 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\ln\left(e^{\left(e^{\cos(x)}+6-6\right)+\left(-2x-1\right)-\left(-2x-1\right)}\right)\right]$
- Answer: $e^{\cos(x)}\sin^{2}(x) - \cos(x)e^{\cos(x)}$
- From: `form:chain_nested` · `conceptual:chain+power` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=25 · S=32 · amax=25
