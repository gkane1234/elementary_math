# Derivatives — inverse trig

**type_id:** `calc_diff_inverse_trigonometric` · **leaf:** `derivative_inverse_trig`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_invtrig`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\text{Find }\frac{d}{dx}\left(\arctan(x)\right)$ | $\text{Find }\frac{d}{dx}\left(\arctan(x)+\left(2x\right)-\left(2x\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{-\left(1-x\right)\left(-\left(-\arctan(x)\right)\right)}{-\left(1-x\right)}\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\frac{-\left(2-x\right)\left(\arctan(x)+6-6\right)}{-\left(2-x\right)}\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(-\left(-\left(\left(\arctan(x)+4\right)-4\right)\right)\right)+1-1\right)$ |
| **C=4** | $\text{Find }\frac{d}{dx}\left(\arctan(x)\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\left(x+3\right)\arctan(x)}{x+3}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{-\left(2+x\right)\left(\arctan(x)+\left(3x-1\right)-\left(3x-1\right)\right)}{-\left(2+x\right)}\right)$ | $\text{Find }\frac{d}{dx}\left(\left(-\left(-\left(\arctan(x)+\left(x-1\right)\right)-\left(x-1\right)\right)\right)+2-2\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\left(\left(\frac{-\left(3-x\right)\arctan(x)}{-\left(3-x\right)}+6\right)-6\right)+\left(-x-1\right)\right)-\left(-x-1\right)\right)$ |
| **C=8** | $\text{Find }\frac{d}{dx}\left(\arctan^{2}(5x)\right)$ | $\text{Find }\frac{d}{dx}\left(\arctan^{2}(5x)+\left(3x+3\right)-\left(3x+3\right)\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\left(\arctan^{2}(5x)+\left(-x\right)-\left(-x\right)\right)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\left(x-3\right)\left(\arctan^{2}(5x)+\left(x-1\right)\right)-\left(x-1\right)}{x-3}+\left(3x-2\right)-\left(3x-2\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\frac{\left(x-2\right)\left(\arctan^{2}(5x)+1-1\right)}{x-2}+\left(-x+3\right)\right)-\left(-x+3\right)\right)$ |
| **C=12** | $\frac{d^{2}}{dx^{2}}\left[\arcsin(x)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{-\left(3+x\right)\arcsin(x)}{-\left(3+x\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[\frac{-\left(1-x\right)\left(\arcsin(x)+5-5\right)}{-\left(1-x\right)}\right]$ | $\frac{d^{2}}{dx^{2}}\left[-\left(-\frac{2\left(x+1\right)\left(\arcsin(x)+\left(-2x+3\right)\right)-\left(-2x+3\right)}{2\left(x+1\right)}\right)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\left(\left(\left(\arcsin(x)+6\right)-6\right)+1-1\right)+1\right)-1\right]$ |
| **C=16** | $\frac{d}{dx}\left[\arcsin(x)\right]$ | $\frac{d}{dx}\left[\arcsin(x)+\left(-2x+1\right)-\left(-2x+1\right)\right]$ | $\frac{d}{dx}\left[\left(\left(-\left(-\arcsin(x)\right)\right)+\left(2x+1\right)\right)-\left(2x+1\right)\right]$ | $\frac{d}{dx}\left[\frac{4\left(x-3\right)\left(\left(\left(\left(\arcsin(x)+6\right)-6\right)+4\right)-4\right)}{4\left(x-3\right)}\right]$ | $\frac{d}{dx}\left[\left(\left(-\left(-\arcsin(x)\right)\right)+\left(-2x+1\right)-\left(-2x+1\right)+\left(2x+3\right)\right)-\left(2x+3\right)\right]$ |
| **C=20** | $\frac{d^{2}}{dx^{2}}\left[\arccos(x)\right]$ | $\frac{d^{2}}{dx^{2}}\left[\arccos(x)+2-2\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\left(-\left(-\arccos(x)\right)\right)+2\right)-2\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\left(\left(\left(\arccos(x)+\left(-2x-1\right)\right)-\left(-2x-1\right)+4\right)-4\right)+2\right)-2\right]$ | $\frac{d^{2}}{dx^{2}}\left[\left(\left(\frac{-\left(1+x\right)\arccos(x)}{-\left(1+x\right)}+\left(-x\right)\right)-\left(-x\right)+\left(2x-1\right)\right)-\left(2x-1\right)\right]$ |
| **C=25** | $\frac{d}{dx}\left[\arccos(x)\right]$ | $\frac{d}{dx}\left[\left(\arccos(x)+\left(-x+1\right)\right)-\left(-x+1\right)\right]$ | $\frac{d}{dx}\left[\frac{3\left(x+1\right)\arccos(x)}{3\left(x+1\right)}+\left(2x-1\right)-\left(2x-1\right)\right]$ | $\frac{d}{dx}\left[\left(\frac{2\left(x+1\right)\arccos(x)}{2\left(x+1\right)}+\left(-x-2\right)-\left(-x-2\right)\right)+1-1\right]$ | $\frac{d}{dx}\left[\left(\left(\frac{\left(x-1\right)\arccos(x)}{x-1}+5\right)-5\right)+\left(x+1\right)-\left(x+1\right)\right]$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\frac{1}{1+x^{2}}$ | $\frac{1}{1+x^{2}}$ | $\frac{1}{1+x^{2}}$ | $\frac{1}{1+x^{2}}$ | $\frac{1}{1+x^{2}}$ |
| **C=4** | $\frac{1}{1+x^{2}}$ | $\frac{1}{1+x^{2}}$ | $\frac{1}{1+x^{2}}$ | $\frac{1}{1+x^{2}}$ | $\frac{1}{1+x^{2}}$ |
| **C=8** | $2\left(\arctan(5x)\right)\left(\frac{5}{1+(5x)^{2}}\right)$ | $2\left(\arctan(5x)\right)\left(\frac{5}{1+(5x)^{2}}\right)$ | $2\left(\arctan(5x)\right)\left(\frac{5}{1+(5x)^{2}}\right)$ | $2\left(\arctan(5x)\right)\left(\frac{5}{1+(5x)^{2}}\right)$ | $2\left(\arctan(5x)\right)\left(\frac{5}{1+(5x)^{2}}\right)$ |
| **C=12** | $x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$ | $x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$ | $x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$ | $x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$ | $x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$ |
| **C=16** | $\frac{1}{\sqrt{1-x^{2}}}$ | $\frac{1}{\sqrt{1-x^{2}}}$ | $\frac{1}{\sqrt{1-x^{2}}}$ | $\frac{1}{\sqrt{1-x^{2}}}$ | $\frac{1}{\sqrt{1-x^{2}}}$ |
| **C=20** | $-x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$ | $-x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$ | $-x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$ | $-x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$ | $-x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$ |
| **C=25** | $-\frac{1}{\sqrt{1-x^{2}}}$ | $-\frac{1}{\sqrt{1-x^{2}}}$ | $-\frac{1}{\sqrt{1-x^{2}}}$ | $-\frac{1}{\sqrt{1-x^{2}}}$ | $-\frac{1}{\sqrt{1-x^{2}}}$ |

## Cell detail

### C=0 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\arctan(x)\right)$
- Answer: $\frac{1}{1+x^{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\arctan(x)+\left(2x\right)-\left(2x\right)\right)$
- Answer: $\frac{1}{1+x^{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `effort:add_cancel_linear` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{-\left(1-x\right)\left(-\left(-\arctan(x)\right)\right)}{-\left(1-x\right)}\right)$
- Answer: $\frac{1}{1+x^{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:double_neg` · `prereq:cancel_quot_bait`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\frac{-\left(2-x\right)\left(\arctan(x)+6-6\right)}{-\left(2-x\right)}\right)\right)$
- Answer: $\frac{1}{1+x^{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(-\left(-\left(\left(\arctan(x)+4\right)-4\right)\right)\right)+1-1\right)$
- Answer: $\frac{1}{1+x^{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `effort:add_cancel_const` · `effort:double_neg` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:double_neg`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\arctan(x)\right)$
- Answer: $\frac{1}{1+x^{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\left(x+3\right)\arctan(x)}{x+3}\right)$
- Answer: $\frac{1}{1+x^{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `prereq:cancel_quot_bait` · `allow:invtrig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{-\left(2+x\right)\left(\arctan(x)+\left(3x-1\right)-\left(3x-1\right)\right)}{-\left(2+x\right)}\right)$
- Answer: $\frac{1}{1+x^{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(-\left(-\left(\arctan(x)+\left(x-1\right)\right)-\left(x-1\right)\right)\right)+2-2\right)$
- Answer: $\frac{1}{1+x^{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `effort:add_cancel_linear` · `effort:double_neg` · `effort:add_cancel_const` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\left(\left(\frac{-\left(3-x\right)\arctan(x)}{-\left(3-x\right)}+6\right)-6\right)+\left(-x-1\right)\right)-\left(-x-1\right)\right)$
- Answer: $\frac{1}{1+x^{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:invtrig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\arctan^{2}(5x)\right)$
- Answer: $2\left(\arctan(5x)\right)\left(\frac{5}{1+(5x)^{2}}\right)$
- From: `form:invtrig_chained` · `conceptual:chain+power` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25

### C=8 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\arctan^{2}(5x)+\left(3x+3\right)-\left(3x+3\right)\right)$
- Answer: $2\left(\arctan(5x)\right)\left(\frac{5}{1+(5x)^{2}}\right)$
- From: `form:invtrig_chained` · `conceptual:chain+power` · `effort:add_cancel_linear` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\left(\arctan^{2}(5x)+\left(-x\right)-\left(-x\right)\right)\right)\right)$
- Answer: $2\left(\arctan(5x)\right)\left(\frac{5}{1+(5x)^{2}}\right)$
- From: `form:invtrig_chained` · `conceptual:chain+power` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:double_neg`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\left(x-3\right)\left(\arctan^{2}(5x)+\left(x-1\right)\right)-\left(x-1\right)}{x-3}+\left(3x-2\right)-\left(3x-2\right)\right)$
- Answer: $2\left(\arctan(5x)\right)\left(\frac{5}{1+(5x)^{2}}\right)$
- From: `form:invtrig_chained` · `conceptual:chain+power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\frac{\left(x-2\right)\left(\arctan^{2}(5x)+1-1\right)}{x-2}+\left(-x+3\right)\right)-\left(-x+3\right)\right)$
- Answer: $2\left(\arctan(5x)\right)\left(\frac{5}{1+(5x)^{2}}\right)$
- From: `form:invtrig_chained` · `conceptual:chain+power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\arcsin(x)\right]$
- Answer: $x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=3

### C=12 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{-\left(3+x\right)\arcsin(x)}{-\left(3+x\right)}\right]$
- Answer: $x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `prereq:cancel_quot_bait` · `allow:invtrig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=12 · S=4 · amax=25 · shortfall=2

### C=12 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\frac{-\left(1-x\right)\left(\arcsin(x)+5-5\right)}{-\left(1-x\right)}\right]$
- Answer: $x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `prereq:cancel_quot_bait`
- Flags: C=12 · S=8 · amax=25 · shortfall=1

### C=12 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[-\left(-\frac{2\left(x+1\right)\left(\arcsin(x)+\left(-2x+3\right)\right)-\left(-2x+3\right)}{2\left(x+1\right)}\right)\right]$
- Answer: $x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=12 · S=16 · amax=25

### C=12 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\left(\left(\left(\arcsin(x)+6\right)-6\right)+1-1\right)+1\right)-1\right]$
- Answer: $x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$
- From: `form:invtrig_arctan` · `conceptual:power` · `effort:add_cancel_const` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:add_cancel_const` · `effort:add_cancel_const`
- Flags: C=12 · S=32 · amax=25

### C=16 · S=0

- Prompt: $\frac{d}{dx}\left[\arcsin(x)\right]$
- Answer: $\frac{1}{\sqrt{1-x^{2}}}$
- From: `form:invtrig_arcsin` · `conceptual:power` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=8.5

### C=16 · S=4

- Prompt: $\frac{d}{dx}\left[\arcsin(x)+\left(-2x+1\right)-\left(-2x+1\right)\right]$
- Answer: $\frac{1}{\sqrt{1-x^{2}}}$
- From: `form:invtrig_arcsin` · `conceptual:power` · `effort:add_cancel_linear` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=16 · S=4 · amax=25 · shortfall=7.5

### C=16 · S=8

- Prompt: $\frac{d}{dx}\left[\left(\left(-\left(-\arcsin(x)\right)\right)+\left(2x+1\right)\right)-\left(2x+1\right)\right]$
- Answer: $\frac{1}{\sqrt{1-x^{2}}}$
- From: `form:invtrig_arcsin` · `conceptual:power` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:add_cancel_linear`
- Flags: C=16 · S=8 · amax=25 · shortfall=6.5

### C=16 · S=16

- Prompt: $\frac{d}{dx}\left[\frac{4\left(x-3\right)\left(\left(\left(\left(\arcsin(x)+6\right)-6\right)+4\right)-4\right)}{4\left(x-3\right)}\right]$
- Answer: $\frac{1}{\sqrt{1-x^{2}}}$
- From: `form:invtrig_arcsin` · `conceptual:power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:add_cancel_const`
- Flags: C=16 · S=16 · amax=25 · shortfall=5.5

### C=16 · S=32

- Prompt: $\frac{d}{dx}\left[\left(\left(-\left(-\arcsin(x)\right)\right)+\left(-2x+1\right)-\left(-2x+1\right)+\left(2x+3\right)\right)-\left(2x+3\right)\right]$
- Answer: $\frac{1}{\sqrt{1-x^{2}}}$
- From: `form:invtrig_arcsin` · `conceptual:power` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:add_cancel_linear`
- Flags: C=16 · S=32 · amax=25 · shortfall=5.5

### C=20 · S=0

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\arccos(x)\right]$
- Answer: $-x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$
- From: `form:invtrig_arcsin` · `conceptual:power` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=11

### C=20 · S=4

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\arccos(x)+2-2\right]$
- Answer: $-x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$
- From: `form:invtrig_arcsin` · `conceptual:power` · `effort:add_cancel_const` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=20 · S=4 · amax=25 · shortfall=10

### C=20 · S=8

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\left(-\left(-\arccos(x)\right)\right)+2\right)-2\right]$
- Answer: $-x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$
- From: `form:invtrig_arcsin` · `conceptual:power` · `effort:double_neg` · `effort:add_cancel_const` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:add_cancel_const`
- Flags: C=20 · S=8 · amax=25 · shortfall=9

### C=20 · S=16

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\left(\left(\left(\arccos(x)+\left(-2x-1\right)\right)-\left(-2x-1\right)+4\right)-4\right)+2\right)-2\right]$
- Answer: $-x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$
- From: `form:invtrig_arcsin` · `conceptual:power` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:add_cancel_const`
- Flags: C=20 · S=16 · amax=25 · shortfall=8

### C=20 · S=32

- Prompt: $\frac{d^{2}}{dx^{2}}\left[\left(\left(\frac{-\left(1+x\right)\arccos(x)}{-\left(1+x\right)}+\left(-x\right)\right)-\left(-x\right)+\left(2x-1\right)\right)-\left(2x-1\right)\right]$
- Answer: $-x\left(\left(-x^{2} + 1\right)\right)^{-\frac{3}{2}}$
- From: `form:invtrig_arcsin` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:invtrig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear`
- Flags: C=20 · S=32 · amax=25 · shortfall=8

### C=25 · S=0

- Prompt: $\frac{d}{dx}\left[\arccos(x)\right]$
- Answer: $-\frac{1}{\sqrt{1-x^{2}}}$
- From: `form:invtrig_chained` · `conceptual:power` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=10

### C=25 · S=4

- Prompt: $\frac{d}{dx}\left[\left(\arccos(x)+\left(-x+1\right)\right)-\left(-x+1\right)\right]$
- Answer: $-\frac{1}{\sqrt{1-x^{2}}}$
- From: `form:invtrig_chained` · `conceptual:power` · `effort:add_cancel_linear` · `allow:invtrig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=25 · S=4 · amax=25 · shortfall=9

### C=25 · S=8

- Prompt: $\frac{d}{dx}\left[\frac{3\left(x+1\right)\arccos(x)}{3\left(x+1\right)}+\left(2x-1\right)-\left(2x-1\right)\right]$
- Answer: $-\frac{1}{\sqrt{1-x^{2}}}$
- From: `form:invtrig_chained` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:invtrig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear`
- Flags: C=25 · S=8 · amax=25 · shortfall=8

### C=25 · S=16

- Prompt: $\frac{d}{dx}\left[\left(\frac{2\left(x+1\right)\arccos(x)}{2\left(x+1\right)}+\left(-x-2\right)-\left(-x-2\right)\right)+1-1\right]$
- Answer: $-\frac{1}{\sqrt{1-x^{2}}}$
- From: `form:invtrig_chained` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:invtrig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=25 · S=16 · amax=25 · shortfall=7

### C=25 · S=32

- Prompt: $\frac{d}{dx}\left[\left(\left(\frac{\left(x-1\right)\arccos(x)}{x-1}+5\right)-5\right)+\left(x+1\right)-\left(x+1\right)\right]$
- Answer: $-\frac{1}{\sqrt{1-x^{2}}}$
- From: `form:invtrig_chained` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:invtrig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=25 · S=32 · amax=25 · shortfall=7
