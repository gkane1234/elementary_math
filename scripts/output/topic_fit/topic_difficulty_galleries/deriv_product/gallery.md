# Derivatives — product rule

**type_id:** `calc_diff_product_rule` · **leaf:** `derivative_product_rule`  
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
| **C=0** | $\text{Find }\frac{d}{dx}\left(\ln\left(\left(2x + 1\right)\right)\ln\left(\left(2x - 1\right)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\left(\ln\left(\left(2x + 1\right)\right)\ln\left(\left(2x - 1\right)\right)\right)+\left(2x\right)\right)-\left(2x\right)\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\frac{-\left(2-x\right)\left(\ln\left(\left(2x + 1\right)\right)\ln\left(\left(2x - 1\right)\right)\right)}{-\left(2-x\right)}\right)\right)$ | $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\left(\left(\left(\ln\left(\left(2x + 1\right)\right)\ln\left(\left(2x - 1\right)\right)\right)+5-5\right)+\left(-x\right)\right)-\left(-x\right)\right)}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{2\left(x-2\right)\left(-\left(-\left(\ln\left(\left(2x + 1\right)\right)\ln\left(\left(2x - 1\right)\right)\right)\right)\right)}{2\left(x-2\right)}+6-6\right)$ |
| **C=4** | $\text{Find }\frac{d}{dx}\left(\arctan(x)\sin(3x)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\arctan(x)\sin(3x)+6\right)-6\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{3\left(x+2\right)\arctan(x)\sin(3x)}{3\left(x+2\right)}+1-1\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-e^{\ln\left(\frac{2\left(x-1\right)\arctan(x)\sin(3x)}{2\left(x-1\right)}\right)}\right)\right)$ | $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\left(-\left(-\arctan(x)\sin(3x)\right)\right)+\left(3x-1\right)-\left(3x-1\right)\right)}\right)$ |
| **C=8** | $\frac{d}{dx}\left[\sqrt{\left(4x + 2\right)}\cos(2x)\right]$ | $\frac{d}{dx}\left[-\left(-\sqrt{\left(4x + 2\right)}\cos(2x)\right)\right]$ | $\frac{d}{dx}\left[\frac{-\left(1-x\right)\sqrt{\left(4x + 2\right)}\cos(2x)}{-\left(1-x\right)}+1-1\right]$ | $\frac{d}{dx}\left[-\left(-e^{\ln\left(\left(\sqrt{\left(4x + 2\right)}\cos(2x)+6-6\right)\right)}\right)\right]$ | $\frac{d}{dx}\left[\left(\frac{2\left(x-1\right)e^{\ln\left(\sqrt{\left(4x + 2\right)}\cos(2x)\right)}}{2\left(x-1\right)}+\left(3x-1\right)\right)-\left(3x-1\right)\right]$ |
| **C=12** | $\text{Find }\frac{d}{dx}\left(\arcsin^{3}(3x)\tan\left(\tan\left(\left(5x - 4\right)\right)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\left(\arcsin^{3}(3x)\tan\left(\tan\left(\left(5x - 4\right)\right)\right)\right)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\left(-\left(-\left(\arcsin^{3}(3x)\tan\left(\tan\left(\left(5x - 4\right)\right)\right)\right)\right)\right)+\left(-x+3\right)\right)-\left(-x+3\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\left(x-1\right)\left(\left(\arcsin^{3}(3x)\tan\left(\tan\left(\left(5x - 4\right)\right)\right)\right)+\left(3x\right)\right)-\left(3x\right)}{x-1}+\left(-x+3\right)-\left(-x+3\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(-\left(-\ln\left(e^{\left(\arcsin^{3}(3x)\tan\left(\tan\left(\left(5x - 4\right)\right)\right)\right)}\right)\right)\right)+5-5\right)$ |
| **C=16** | $\text{Find }\frac{d}{dx}\left(\sqrt{\left(4x + 1\right)}\arccos(x)\left(2x^{2}\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\sqrt{\left(4x + 1\right)}\arccos(x)\left(2x^{2}\right)+\left(3x-1\right)-\left(3x-1\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(-\left(-\sqrt{\left(4x + 1\right)}\arccos(x)\left(2x^{2}\right)\right)\right)+4-4\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\left(e^{\ln\left(\sqrt{\left(4x + 1\right)}\arccos(x)\left(2x^{2}\right)\right)}+\left(3x\right)-\left(3x\right)\right)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(-\left(-\left(\ln\left(e^{\sqrt{\left(4x + 1\right)}\arccos(x)\left(2x^{2}\right)}\right)+3-3\right)\right)\right)$ |
| **C=20** | $\text{Find }\frac{d}{dx}\left(\sqrt{\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\left(x-3\right)\sqrt{\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)}{x-3}\right)$ | $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\ln\left(e^{\sqrt{\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)}\right)\right)}\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\left(-\left(-\frac{2\left(x+1\right)\sqrt{\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)}{2\left(x+1\right)}\right)\right)+5\right)-5\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\frac{\left(x-3\right)\sqrt{\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)}{x-3}+\left(3x+1\right)\right)-\left(3x+1\right)+\left(2x\right)-\left(2x\right)\right)$ |
| **C=25** | $\text{Find }\frac{d}{dx}\left(\sin(2x)\ln^{2}(3x)\arccos^{3}(x)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(\sin(2x)\ln^{2}(3x)\arccos^{3}(x)+4\right)-4\right)$ | $\text{Find }\frac{d}{dx}\left(\ln\left(e^{\left(\sin(2x)\ln^{2}(3x)\arccos^{3}(x)+6-6\right)}\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\ln\left(e^{e^{\ln\left(\left(-\left(-\sin(2x)\ln^{2}(3x)\arccos^{3}(x)\right)\right)\right)}}\right)\right)$ | $\text{Find }\frac{d}{dx}\left(\left(e^{\ln\left(\sin(2x)\ln^{2}(3x)\arccos^{3}(x)\right)}+4-4\right)+6-6\right)$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $2\frac{1}{\left(2x + 1\right)}\ln\left(\left(2x - 1\right)\right)+\ln\left(\left(2x + 1\right)\right)\left(2\frac{1}{\left(2x - 1\right)}\right)$ | $2\frac{1}{\left(2x + 1\right)}\ln\left(\left(2x - 1\right)\right)+\ln\left(\left(2x + 1\right)\right)\left(2\frac{1}{\left(2x - 1\right)}\right)$ | $2\frac{1}{\left(2x + 1\right)}\ln\left(\left(2x - 1\right)\right)+\ln\left(\left(2x + 1\right)\right)\left(2\frac{1}{\left(2x - 1\right)}\right)$ | $2\frac{1}{\left(2x + 1\right)}\ln\left(\left(2x - 1\right)\right)+\ln\left(\left(2x + 1\right)\right)\left(2\frac{1}{\left(2x - 1\right)}\right)$ | $2\frac{1}{\left(2x + 1\right)}\ln\left(\left(2x - 1\right)\right)+\ln\left(\left(2x + 1\right)\right)\left(2\frac{1}{\left(2x - 1\right)}\right)$ |
| **C=4** | $\frac{1}{1+x^{2}}\sin(3x)+\arctan(x)\left(3\cos(3x)\right)$ | $\frac{1}{1+x^{2}}\sin(3x)+\arctan(x)\left(3\cos(3x)\right)$ | $\frac{1}{1+x^{2}}\sin(3x)+\arctan(x)\left(3\cos(3x)\right)$ | $\frac{1}{1+x^{2}}\sin(3x)+\arctan(x)\left(3\cos(3x)\right)$ | $\frac{1}{1+x^{2}}\sin(3x)+\arctan(x)\left(3\cos(3x)\right)$ |
| **C=8** | $4\frac{1}{2\sqrt{\left(4x + 2\right)}}\cos(2x)+\sqrt{\left(4x + 2\right)}\left(-2\sin(2x)\right)$ | $4\frac{1}{2\sqrt{\left(4x + 2\right)}}\cos(2x)+\sqrt{\left(4x + 2\right)}\left(-2\sin(2x)\right)$ | $4\frac{1}{2\sqrt{\left(4x + 2\right)}}\cos(2x)+\sqrt{\left(4x + 2\right)}\left(-2\sin(2x)\right)$ | $4\frac{1}{2\sqrt{\left(4x + 2\right)}}\cos(2x)+\sqrt{\left(4x + 2\right)}\left(-2\sin(2x)\right)$ | $4\frac{1}{2\sqrt{\left(4x + 2\right)}}\cos(2x)+\sqrt{\left(4x + 2\right)}\left(-2\sin(2x)\right)$ |
| **C=12** | $9\arcsin^{2}(3x)\frac{1}{\sqrt{1-(3x)^{2}}}\tan\left(\tan\left(\left(5x - 4\right)\right)\right)+\arcsin^{3}(3x)\left(5\sec^{2}(\tan\left(\left(5x - 4\right)\right))\sec^{2}(\left(5x - 4\right))\right)$ | $9\arcsin^{2}(3x)\frac{1}{\sqrt{1-(3x)^{2}}}\tan\left(\tan\left(\left(5x - 4\right)\right)\right)+\arcsin^{3}(3x)\left(5\sec^{2}(\tan\left(\left(5x - 4\right)\right))\sec^{2}(\left(5x - 4\right))\right)$ | $9\arcsin^{2}(3x)\frac{1}{\sqrt{1-(3x)^{2}}}\tan\left(\tan\left(\left(5x - 4\right)\right)\right)+\arcsin^{3}(3x)\left(5\sec^{2}(\tan\left(\left(5x - 4\right)\right))\sec^{2}(\left(5x - 4\right))\right)$ | $9\arcsin^{2}(3x)\frac{1}{\sqrt{1-(3x)^{2}}}\tan\left(\tan\left(\left(5x - 4\right)\right)\right)+\arcsin^{3}(3x)\left(5\sec^{2}(\tan\left(\left(5x - 4\right)\right))\sec^{2}(\left(5x - 4\right))\right)$ | $9\arcsin^{2}(3x)\frac{1}{\sqrt{1-(3x)^{2}}}\tan\left(\tan\left(\left(5x - 4\right)\right)\right)+\arcsin^{3}(3x)\left(5\sec^{2}(\tan\left(\left(5x - 4\right)\right))\sec^{2}(\left(5x - 4\right))\right)$ |
| **C=16** | $8\frac{1}{2\sqrt{\left(4x + 1\right)}}\arccos(x)x^{2} + 2\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sqrt{\left(4x + 1\right)}x^{2} + 4\sqrt{\left(4x + 1\right)}\arccos(x)x$ | $8\frac{1}{2\sqrt{\left(4x + 1\right)}}\arccos(x)x^{2} + 2\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sqrt{\left(4x + 1\right)}x^{2} + 4\sqrt{\left(4x + 1\right)}\arccos(x)x$ | $8\frac{1}{2\sqrt{\left(4x + 1\right)}}\arccos(x)x^{2} + 2\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sqrt{\left(4x + 1\right)}x^{2} + 4\sqrt{\left(4x + 1\right)}\arccos(x)x$ | $8\frac{1}{2\sqrt{\left(4x + 1\right)}}\arccos(x)x^{2} + 2\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sqrt{\left(4x + 1\right)}x^{2} + 4\sqrt{\left(4x + 1\right)}\arccos(x)x$ | $8\frac{1}{2\sqrt{\left(4x + 1\right)}}\arccos(x)x^{2} + 2\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sqrt{\left(4x + 1\right)}x^{2} + 4\sqrt{\left(4x + 1\right)}\arccos(x)x$ |
| **C=20** | $5\frac{1}{2\sqrt{\sqrt{5x}}}\frac{1}{2\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)+\sqrt{\sqrt{5x}}\left(3\frac{1}{\ln\left(x^{3}\right)}\frac{1}{x^{3}}x^{2}\right)$ | $5\frac{1}{2\sqrt{\sqrt{5x}}}\frac{1}{2\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)+\sqrt{\sqrt{5x}}\left(3\frac{1}{\ln\left(x^{3}\right)}\frac{1}{x^{3}}x^{2}\right)$ | $5\frac{1}{2\sqrt{\sqrt{5x}}}\frac{1}{2\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)+\sqrt{\sqrt{5x}}\left(3\frac{1}{\ln\left(x^{3}\right)}\frac{1}{x^{3}}x^{2}\right)$ | $5\frac{1}{2\sqrt{\sqrt{5x}}}\frac{1}{2\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)+\sqrt{\sqrt{5x}}\left(3\frac{1}{\ln\left(x^{3}\right)}\frac{1}{x^{3}}x^{2}\right)$ | $5\frac{1}{2\sqrt{\sqrt{5x}}}\frac{1}{2\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)+\sqrt{\sqrt{5x}}\left(3\frac{1}{\ln\left(x^{3}\right)}\frac{1}{x^{3}}x^{2}\right)$ |
| **C=25** | $2\cos(2x)\ln^{2}(3x)\arccos^{3}(x) + 6\ln\left(3x\right)\frac{1}{3x}\sin(2x)\arccos^{3}(x) + 3\arccos^{2}(x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sin(2x)\ln^{2}(3x)$ | $2\cos(2x)\ln^{2}(3x)\arccos^{3}(x) + 6\ln\left(3x\right)\frac{1}{3x}\sin(2x)\arccos^{3}(x) + 3\arccos^{2}(x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sin(2x)\ln^{2}(3x)$ | $2\cos(2x)\ln^{2}(3x)\arccos^{3}(x) + 6\ln\left(3x\right)\frac{1}{3x}\sin(2x)\arccos^{3}(x) + 3\arccos^{2}(x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sin(2x)\ln^{2}(3x)$ | $2\cos(2x)\ln^{2}(3x)\arccos^{3}(x) + 6\ln\left(3x\right)\frac{1}{3x}\sin(2x)\arccos^{3}(x) + 3\arccos^{2}(x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sin(2x)\ln^{2}(3x)$ | $2\cos(2x)\ln^{2}(3x)\arccos^{3}(x) + 6\ln\left(3x\right)\frac{1}{3x}\sin(2x)\arccos^{3}(x) + 3\arccos^{2}(x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sin(2x)\ln^{2}(3x)$ |

## Cell detail

### C=0 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\ln\left(\left(2x + 1\right)\right)\ln\left(\left(2x - 1\right)\right)\right)$
- Answer: $2\frac{1}{\left(2x + 1\right)}\ln\left(\left(2x - 1\right)\right)+\ln\left(\left(2x + 1\right)\right)\left(2\frac{1}{\left(2x - 1\right)}\right)$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\left(\ln\left(\left(2x + 1\right)\right)\ln\left(\left(2x - 1\right)\right)\right)+\left(2x\right)\right)-\left(2x\right)\right)$
- Answer: $2\frac{1}{\left(2x + 1\right)}\ln\left(\left(2x - 1\right)\right)+\ln\left(\left(2x + 1\right)\right)\left(2\frac{1}{\left(2x - 1\right)}\right)$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\frac{-\left(2-x\right)\left(\ln\left(\left(2x + 1\right)\right)\ln\left(\left(2x - 1\right)\right)\right)}{-\left(2-x\right)}\right)\right)$
- Answer: $2\frac{1}{\left(2x + 1\right)}\ln\left(\left(2x - 1\right)\right)+\ln\left(\left(2x + 1\right)\right)\left(2\frac{1}{\left(2x - 1\right)}\right)$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\left(\left(\left(\ln\left(\left(2x + 1\right)\right)\ln\left(\left(2x - 1\right)\right)\right)+5-5\right)+\left(-x\right)\right)-\left(-x\right)\right)}\right)$
- Answer: $2\frac{1}{\left(2x + 1\right)}\ln\left(\left(2x - 1\right)\right)+\ln\left(\left(2x + 1\right)\right)\left(2\frac{1}{\left(2x - 1\right)}\right)$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{2\left(x-2\right)\left(-\left(-\left(\ln\left(\left(2x + 1\right)\right)\ln\left(\left(2x - 1\right)\right)\right)\right)\right)}{2\left(x-2\right)}+6-6\right)$
- Answer: $2\frac{1}{\left(2x + 1\right)}\ln\left(\left(2x - 1\right)\right)+\ln\left(\left(2x + 1\right)\right)\left(2\frac{1}{\left(2x - 1\right)}\right)$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\arctan(x)\sin(3x)\right)$
- Answer: $\frac{1}{1+x^{2}}\sin(3x)+\arctan(x)\left(3\cos(3x)\right)$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\arctan(x)\sin(3x)+6\right)-6\right)$
- Answer: $\frac{1}{1+x^{2}}\sin(3x)+\arctan(x)\left(3\cos(3x)\right)$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{3\left(x+2\right)\arctan(x)\sin(3x)}{3\left(x+2\right)}+1-1\right)$
- Answer: $\frac{1}{1+x^{2}}\sin(3x)+\arctan(x)\left(3\cos(3x)\right)$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-e^{\ln\left(\frac{2\left(x-1\right)\arctan(x)\sin(3x)}{2\left(x-1\right)}\right)}\right)\right)$
- Answer: $\frac{1}{1+x^{2}}\sin(3x)+\arctan(x)\left(3\cos(3x)\right)$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\left(-\left(-\arctan(x)\sin(3x)\right)\right)+\left(3x-1\right)-\left(3x-1\right)\right)}\right)$
- Answer: $\frac{1}{1+x^{2}}\sin(3x)+\arctan(x)\left(3\cos(3x)\right)$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\frac{d}{dx}\left[\sqrt{\left(4x + 2\right)}\cos(2x)\right]$
- Answer: $4\frac{1}{2\sqrt{\left(4x + 2\right)}}\cos(2x)+\sqrt{\left(4x + 2\right)}\left(-2\sin(2x)\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power+product` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=8 · S=0 · amax=25

### C=8 · S=4

- Prompt: $\frac{d}{dx}\left[-\left(-\sqrt{\left(4x + 2\right)}\cos(2x)\right)\right]$
- Answer: $4\frac{1}{2\sqrt{\left(4x + 2\right)}}\cos(2x)+\sqrt{\left(4x + 2\right)}\left(-2\sin(2x)\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power+product` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\frac{d}{dx}\left[\frac{-\left(1-x\right)\sqrt{\left(4x + 2\right)}\cos(2x)}{-\left(1-x\right)}+1-1\right]$
- Answer: $4\frac{1}{2\sqrt{\left(4x + 2\right)}}\cos(2x)+\sqrt{\left(4x + 2\right)}\left(-2\sin(2x)\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\frac{d}{dx}\left[-\left(-e^{\ln\left(\left(\sqrt{\left(4x + 2\right)}\cos(2x)+6-6\right)\right)}\right)\right]$
- Answer: $4\frac{1}{2\sqrt{\left(4x + 2\right)}}\cos(2x)+\sqrt{\left(4x + 2\right)}\left(-2\sin(2x)\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power+product` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\frac{d}{dx}\left[\left(\frac{2\left(x-1\right)e^{\ln\left(\sqrt{\left(4x + 2\right)}\cos(2x)\right)}}{2\left(x-1\right)}+\left(3x-1\right)\right)-\left(3x-1\right)\right]$
- Answer: $4\frac{1}{2\sqrt{\left(4x + 2\right)}}\cos(2x)+\sqrt{\left(4x + 2\right)}\left(-2\sin(2x)\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\arcsin^{3}(3x)\tan\left(\tan\left(\left(5x - 4\right)\right)\right)\right)$
- Answer: $9\arcsin^{2}(3x)\frac{1}{\sqrt{1-(3x)^{2}}}\tan\left(\tan\left(\left(5x - 4\right)\right)\right)+\arcsin^{3}(3x)\left(5\sec^{2}(\tan\left(\left(5x - 4\right)\right))\sec^{2}(\left(5x - 4\right))\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=12 · S=0 · amax=25

### C=12 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\left(\arcsin^{3}(3x)\tan\left(\tan\left(\left(5x - 4\right)\right)\right)\right)\right)\right)$
- Answer: $9\arcsin^{2}(3x)\frac{1}{\sqrt{1-(3x)^{2}}}\tan\left(\tan\left(\left(5x - 4\right)\right)\right)+\arcsin^{3}(3x)\left(5\sec^{2}(\tan\left(\left(5x - 4\right)\right))\sec^{2}(\left(5x - 4\right))\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=12 · S=4 · amax=25

### C=12 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\left(-\left(-\left(\arcsin^{3}(3x)\tan\left(\tan\left(\left(5x - 4\right)\right)\right)\right)\right)\right)+\left(-x+3\right)\right)-\left(-x+3\right)\right)$
- Answer: $9\arcsin^{2}(3x)\frac{1}{\sqrt{1-(3x)^{2}}}\tan\left(\tan\left(\left(5x - 4\right)\right)\right)+\arcsin^{3}(3x)\left(5\sec^{2}(\tan\left(\left(5x - 4\right)\right))\sec^{2}(\left(5x - 4\right))\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=12 · S=8 · amax=25

### C=12 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\left(x-1\right)\left(\left(\arcsin^{3}(3x)\tan\left(\tan\left(\left(5x - 4\right)\right)\right)\right)+\left(3x\right)\right)-\left(3x\right)}{x-1}+\left(-x+3\right)-\left(-x+3\right)\right)$
- Answer: $9\arcsin^{2}(3x)\frac{1}{\sqrt{1-(3x)^{2}}}\tan\left(\tan\left(\left(5x - 4\right)\right)\right)+\arcsin^{3}(3x)\left(5\sec^{2}(\tan\left(\left(5x - 4\right)\right))\sec^{2}(\left(5x - 4\right))\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=12 · S=16 · amax=25

### C=12 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(-\left(-\ln\left(e^{\left(\arcsin^{3}(3x)\tan\left(\tan\left(\left(5x - 4\right)\right)\right)\right)}\right)\right)\right)+5-5\right)$
- Answer: $9\arcsin^{2}(3x)\frac{1}{\sqrt{1-(3x)^{2}}}\tan\left(\tan\left(\left(5x - 4\right)\right)\right)+\arcsin^{3}(3x)\left(5\sec^{2}(\tan\left(\left(5x - 4\right)\right))\sec^{2}(\left(5x - 4\right))\right)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=12 · S=32 · amax=25

### C=16 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\sqrt{\left(4x + 1\right)}\arccos(x)\left(2x^{2}\right)\right)$
- Answer: $8\frac{1}{2\sqrt{\left(4x + 1\right)}}\arccos(x)x^{2} + 2\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sqrt{\left(4x + 1\right)}x^{2} + 4\sqrt{\left(4x + 1\right)}\arccos(x)x$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=16 · S=0 · amax=25 · shortfall=6

### C=16 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\sqrt{\left(4x + 1\right)}\arccos(x)\left(2x^{2}\right)+\left(3x-1\right)-\left(3x-1\right)\right)$
- Answer: $8\frac{1}{2\sqrt{\left(4x + 1\right)}}\arccos(x)x^{2} + 2\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sqrt{\left(4x + 1\right)}x^{2} + 4\sqrt{\left(4x + 1\right)}\arccos(x)x$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=16 · S=4 · amax=25 · shortfall=5

### C=16 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(-\left(-\sqrt{\left(4x + 1\right)}\arccos(x)\left(2x^{2}\right)\right)\right)+4-4\right)$
- Answer: $8\frac{1}{2\sqrt{\left(4x + 1\right)}}\arccos(x)x^{2} + 2\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sqrt{\left(4x + 1\right)}x^{2} + 4\sqrt{\left(4x + 1\right)}\arccos(x)x$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=16 · S=8 · amax=25 · shortfall=4

### C=16 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\left(e^{\ln\left(\sqrt{\left(4x + 1\right)}\arccos(x)\left(2x^{2}\right)\right)}+\left(3x\right)-\left(3x\right)\right)\right)\right)$
- Answer: $8\frac{1}{2\sqrt{\left(4x + 1\right)}}\arccos(x)x^{2} + 2\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sqrt{\left(4x + 1\right)}x^{2} + 4\sqrt{\left(4x + 1\right)}\arccos(x)x$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=16 · S=16 · amax=25 · shortfall=3

### C=16 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(-\left(-\left(\ln\left(e^{\sqrt{\left(4x + 1\right)}\arccos(x)\left(2x^{2}\right)}\right)+3-3\right)\right)\right)$
- Answer: $8\frac{1}{2\sqrt{\left(4x + 1\right)}}\arccos(x)x^{2} + 2\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sqrt{\left(4x + 1\right)}x^{2} + 4\sqrt{\left(4x + 1\right)}\arccos(x)x$
- From: `form:product_two_poly` · `conceptual:chain+power+product` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=16 · S=32 · amax=25 · shortfall=3

### C=20 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\sqrt{\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)\right)$
- Answer: $5\frac{1}{2\sqrt{\sqrt{5x}}}\frac{1}{2\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)+\sqrt{\sqrt{5x}}\left(3\frac{1}{\ln\left(x^{3}\right)}\frac{1}{x^{3}}x^{2}\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power+product` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=20 · S=0 · amax=25 · shortfall=2

### C=20 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\left(x-3\right)\sqrt{\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)}{x-3}\right)$
- Answer: $5\frac{1}{2\sqrt{\sqrt{5x}}}\frac{1}{2\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)+\sqrt{\sqrt{5x}}\left(3\frac{1}{\ln\left(x^{3}\right)}\frac{1}{x^{3}}x^{2}\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=20 · S=4 · amax=25 · shortfall=1

### C=20 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(e^{\ln\left(\ln\left(e^{\sqrt{\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)}\right)\right)}\right)$
- Answer: $5\frac{1}{2\sqrt{\sqrt{5x}}}\frac{1}{2\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)+\sqrt{\sqrt{5x}}\left(3\frac{1}{\ln\left(x^{3}\right)}\frac{1}{x^{3}}x^{2}\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power+product` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=20 · S=8 · amax=25

### C=20 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\left(-\left(-\frac{2\left(x+1\right)\sqrt{\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)}{2\left(x+1\right)}\right)\right)+5\right)-5\right)$
- Answer: $5\frac{1}{2\sqrt{\sqrt{5x}}}\frac{1}{2\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)+\sqrt{\sqrt{5x}}\left(3\frac{1}{\ln\left(x^{3}\right)}\frac{1}{x^{3}}x^{2}\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=16 · amax=25

### C=20 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\frac{\left(x-3\right)\sqrt{\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)}{x-3}+\left(3x+1\right)\right)-\left(3x+1\right)+\left(2x\right)-\left(2x\right)\right)$
- Answer: $5\frac{1}{2\sqrt{\sqrt{5x}}}\frac{1}{2\sqrt{5x}}\ln\left(\ln\left(x^{3}\right)\right)+\sqrt{\sqrt{5x}}\left(3\frac{1}{\ln\left(x^{3}\right)}\frac{1}{x^{3}}x^{2}\right)$
- From: `form:product_poly_exp` · `conceptual:chain+power+product` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=20 · S=32 · amax=25

### C=25 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\sin(2x)\ln^{2}(3x)\arccos^{3}(x)\right)$
- Answer: $2\cos(2x)\ln^{2}(3x)\arccos^{3}(x) + 6\ln\left(3x\right)\frac{1}{3x}\sin(2x)\arccos^{3}(x) + 3\arccos^{2}(x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sin(2x)\ln^{2}(3x)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `allow:triple_product`
- Flags: C=25 · S=0 · amax=25 · shortfall=3

### C=25 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(\sin(2x)\ln^{2}(3x)\arccos^{3}(x)+4\right)-4\right)$
- Answer: $2\cos(2x)\ln^{2}(3x)\arccos^{3}(x) + 6\ln\left(3x\right)\frac{1}{3x}\sin(2x)\arccos^{3}(x) + 3\arccos^{2}(x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sin(2x)\ln^{2}(3x)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=4 · amax=25 · shortfall=2

### C=25 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\ln\left(e^{\left(\sin(2x)\ln^{2}(3x)\arccos^{3}(x)+6-6\right)}\right)\right)$
- Answer: $2\cos(2x)\ln^{2}(3x)\arccos^{3}(x) + 6\ln\left(3x\right)\frac{1}{3x}\sin(2x)\arccos^{3}(x) + 3\arccos^{2}(x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sin(2x)\ln^{2}(3x)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=8 · amax=25 · shortfall=1

### C=25 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\ln\left(e^{e^{\ln\left(\left(-\left(-\sin(2x)\ln^{2}(3x)\arccos^{3}(x)\right)\right)\right)}}\right)\right)$
- Answer: $2\cos(2x)\ln^{2}(3x)\arccos^{3}(x) + 6\ln\left(3x\right)\frac{1}{3x}\sin(2x)\arccos^{3}(x) + 3\arccos^{2}(x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sin(2x)\ln^{2}(3x)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=16 · amax=25

### C=25 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\left(e^{\ln\left(\sin(2x)\ln^{2}(3x)\arccos^{3}(x)\right)}+4-4\right)+6-6\right)$
- Answer: $2\cos(2x)\ln^{2}(3x)\arccos^{3}(x) + 6\ln\left(3x\right)\frac{1}{3x}\sin(2x)\arccos^{3}(x) + 3\arccos^{2}(x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\sin(2x)\ln^{2}(3x)$
- From: `form:product_poly_trig` · `conceptual:chain+power+product` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=32 · amax=25
