# Derivatives — quotient rule

**type_id:** `calc_diff_quotient_rule` · **leaf:** `derivative_quotient_rule`  
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
| **C=0** | $\frac{d}{dx}\left[\frac{x - 1}{x + 1}\right]$ | $\frac{d}{dx}\left[\frac{x - 1}{x + 1}\right]$ | $\frac{d}{dx}\left[\frac{x - 1}{x + 1}\right]$ | $\frac{d}{dx}\left[\frac{x - 1}{x + 1}\right]$ | $\frac{d}{dx}\left[\frac{x - 1}{x + 1}\right]$ |
| **C=4** | $\text{Find }\frac{d}{dx}\left(\frac{3x^{3} - 2x - 1}{2x - 1}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{3x^{3} - 2x - 1}{2x - 1}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{3x^{3} - 2x - 1}{2x - 1}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{3x^{3} - 2x - 1}{2x - 1}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{3x^{3} - 2x - 1}{2x - 1}\right)$ |
| **C=8** | $\text{Find }\frac{d}{dx}\left(\frac{\cos(5x)}{5x + 3}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\cos(5x)}{5x + 3}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\cos(5x)}{5x + 3}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\cos(5x)}{5x + 3}\right)$ | $\text{Find }\frac{d}{dx}\left(\frac{\cos(5x)}{5x + 3}\right)$ |
| **C=12** | $\frac{d}{dx}\left[\frac{2x^{4} - 2x^{2}}{4x - 4}\right]$ | $\frac{d}{dx}\left[\frac{2x^{4} - 2x^{2}}{4x - 4}\right]$ | $\frac{d}{dx}\left[\frac{2x^{4} - 2x^{2}}{4x - 4}\right]$ | $\frac{d}{dx}\left[\frac{2x^{4} - 2x^{2}}{4x - 4}\right]$ | $\frac{d}{dx}\left[\frac{2x^{4} - 2x^{2}}{4x - 4}\right]$ |
| **C=16** | $\frac{d}{dx}\left[\frac{e^{e^{5x}}}{4x - 4}\right]$ | $\frac{d}{dx}\left[\frac{e^{e^{5x}}}{4x - 4}\right]$ | $\frac{d}{dx}\left[\frac{e^{e^{5x}}}{4x - 4}\right]$ | $\frac{d}{dx}\left[\frac{e^{e^{5x}}}{4x - 4}\right]$ | $\frac{d}{dx}\left[\frac{e^{e^{5x}}}{4x - 4}\right]$ |
| **C=20** | $\frac{d}{dx}\left[\frac{e^{\left(4x + 3\right)}}{4x - 5}\right]$ | $\frac{d}{dx}\left[\frac{e^{\left(4x + 3\right)}}{4x - 5}\right]$ | $\frac{d}{dx}\left[\frac{e^{\left(4x + 3\right)}}{4x - 5}\right]$ | $\frac{d}{dx}\left[\frac{e^{\left(4x + 3\right)}}{4x - 5}\right]$ | $\frac{d}{dx}\left[\frac{e^{\left(4x + 3\right)}}{4x - 5}\right]$ |
| **C=25** | $\frac{d}{dx}\left[\frac{2x^{4}}{4x + 1}\right]$ | $\frac{d}{dx}\left[\frac{2x^{4}}{4x + 1}\right]$ | $\frac{d}{dx}\left[\frac{2x^{4}}{4x + 1}\right]$ | $\frac{d}{dx}\left[\frac{2x^{4}}{4x + 1}\right]$ | $\frac{d}{dx}\left[\frac{2x^{4}}{4x + 1}\right]$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\frac{\left(1\right)\left(x + 1\right)-\left(x - 1\right)\left(1\right)}{\left(x + 1\right)^{2}}$ | $\frac{\left(1\right)\left(x + 1\right)-\left(x - 1\right)\left(1\right)}{\left(x + 1\right)^{2}}$ | $\frac{\left(1\right)\left(x + 1\right)-\left(x - 1\right)\left(1\right)}{\left(x + 1\right)^{2}}$ | $\frac{\left(1\right)\left(x + 1\right)-\left(x - 1\right)\left(1\right)}{\left(x + 1\right)^{2}}$ | $\frac{\left(1\right)\left(x + 1\right)-\left(x - 1\right)\left(1\right)}{\left(x + 1\right)^{2}}$ |
| **C=4** | $\frac{\left(9x^{2} - 2\right)\left(2x - 1\right)-\left(3x^{3} - 2x - 1\right)\left(2\right)}{\left(2x - 1\right)^{2}}$ | $\frac{\left(9x^{2} - 2\right)\left(2x - 1\right)-\left(3x^{3} - 2x - 1\right)\left(2\right)}{\left(2x - 1\right)^{2}}$ | $\frac{\left(9x^{2} - 2\right)\left(2x - 1\right)-\left(3x^{3} - 2x - 1\right)\left(2\right)}{\left(2x - 1\right)^{2}}$ | $\frac{\left(9x^{2} - 2\right)\left(2x - 1\right)-\left(3x^{3} - 2x - 1\right)\left(2\right)}{\left(2x - 1\right)^{2}}$ | $\frac{\left(9x^{2} - 2\right)\left(2x - 1\right)-\left(3x^{3} - 2x - 1\right)\left(2\right)}{\left(2x - 1\right)^{2}}$ |
| **C=8** | $\frac{\left(-5\sin(5x)\right)\left(5x + 3\right)-\left(\cos(5x)\right)\left(5\right)}{\left(5x + 3\right)^{2}}$ | $\frac{\left(-5\sin(5x)\right)\left(5x + 3\right)-\left(\cos(5x)\right)\left(5\right)}{\left(5x + 3\right)^{2}}$ | $\frac{\left(-5\sin(5x)\right)\left(5x + 3\right)-\left(\cos(5x)\right)\left(5\right)}{\left(5x + 3\right)^{2}}$ | $\frac{\left(-5\sin(5x)\right)\left(5x + 3\right)-\left(\cos(5x)\right)\left(5\right)}{\left(5x + 3\right)^{2}}$ | $\frac{\left(-5\sin(5x)\right)\left(5x + 3\right)-\left(\cos(5x)\right)\left(5\right)}{\left(5x + 3\right)^{2}}$ |
| **C=12** | $\frac{\left(8x^{3} - 4x\right)\left(4x - 4\right)-\left(2x^{4} - 2x^{2}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$ | $\frac{\left(8x^{3} - 4x\right)\left(4x - 4\right)-\left(2x^{4} - 2x^{2}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$ | $\frac{\left(8x^{3} - 4x\right)\left(4x - 4\right)-\left(2x^{4} - 2x^{2}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$ | $\frac{\left(8x^{3} - 4x\right)\left(4x - 4\right)-\left(2x^{4} - 2x^{2}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$ | $\frac{\left(8x^{3} - 4x\right)\left(4x - 4\right)-\left(2x^{4} - 2x^{2}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$ |
| **C=16** | $\frac{\left(e^{e^{5x}}e^{5x}\left(5\right)\right)\left(4x - 4\right)-\left(e^{e^{5x}}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$ | $\frac{\left(e^{e^{5x}}e^{5x}\left(5\right)\right)\left(4x - 4\right)-\left(e^{e^{5x}}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$ | $\frac{\left(e^{e^{5x}}e^{5x}\left(5\right)\right)\left(4x - 4\right)-\left(e^{e^{5x}}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$ | $\frac{\left(e^{e^{5x}}e^{5x}\left(5\right)\right)\left(4x - 4\right)-\left(e^{e^{5x}}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$ | $\frac{\left(e^{e^{5x}}e^{5x}\left(5\right)\right)\left(4x - 4\right)-\left(e^{e^{5x}}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$ |
| **C=20** | $\frac{\left(e^{\left(4x + 3\right)}\left(4\right)\right)\left(4x - 5\right)-\left(e^{\left(4x + 3\right)}\right)\left(4\right)}{\left(4x - 5\right)^{2}}$ | $\frac{\left(e^{\left(4x + 3\right)}\left(4\right)\right)\left(4x - 5\right)-\left(e^{\left(4x + 3\right)}\right)\left(4\right)}{\left(4x - 5\right)^{2}}$ | $\frac{\left(e^{\left(4x + 3\right)}\left(4\right)\right)\left(4x - 5\right)-\left(e^{\left(4x + 3\right)}\right)\left(4\right)}{\left(4x - 5\right)^{2}}$ | $\frac{\left(e^{\left(4x + 3\right)}\left(4\right)\right)\left(4x - 5\right)-\left(e^{\left(4x + 3\right)}\right)\left(4\right)}{\left(4x - 5\right)^{2}}$ | $\frac{\left(e^{\left(4x + 3\right)}\left(4\right)\right)\left(4x - 5\right)-\left(e^{\left(4x + 3\right)}\right)\left(4\right)}{\left(4x - 5\right)^{2}}$ |
| **C=25** | $\frac{\left(8x^{3}\right)\left(4x + 1\right)-\left(2x^{4}\right)\left(4\right)}{\left(4x + 1\right)^{2}}$ | $\frac{\left(8x^{3}\right)\left(4x + 1\right)-\left(2x^{4}\right)\left(4\right)}{\left(4x + 1\right)^{2}}$ | $\frac{\left(8x^{3}\right)\left(4x + 1\right)-\left(2x^{4}\right)\left(4\right)}{\left(4x + 1\right)^{2}}$ | $\frac{\left(8x^{3}\right)\left(4x + 1\right)-\left(2x^{4}\right)\left(4\right)}{\left(4x + 1\right)^{2}}$ | $\frac{\left(8x^{3}\right)\left(4x + 1\right)-\left(2x^{4}\right)\left(4\right)}{\left(4x + 1\right)^{2}}$ |

## Cell detail

### C=0 · S=0

- Prompt: $\frac{d}{dx}\left[\frac{x - 1}{x + 1}\right]$
- Answer: $\frac{\left(1\right)\left(x + 1\right)-\left(x - 1\right)\left(1\right)}{\left(x + 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\frac{d}{dx}\left[\frac{x - 1}{x + 1}\right]$
- Answer: $\frac{\left(1\right)\left(x + 1\right)-\left(x - 1\right)\left(1\right)}{\left(x + 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\frac{d}{dx}\left[\frac{x - 1}{x + 1}\right]$
- Answer: $\frac{\left(1\right)\left(x + 1\right)-\left(x - 1\right)\left(1\right)}{\left(x + 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\frac{d}{dx}\left[\frac{x - 1}{x + 1}\right]$
- Answer: $\frac{\left(1\right)\left(x + 1\right)-\left(x - 1\right)\left(1\right)}{\left(x + 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\frac{d}{dx}\left[\frac{x - 1}{x + 1}\right]$
- Answer: $\frac{\left(1\right)\left(x + 1\right)-\left(x - 1\right)\left(1\right)}{\left(x + 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{3x^{3} - 2x - 1}{2x - 1}\right)$
- Answer: $\frac{\left(9x^{2} - 2\right)\left(2x - 1\right)-\left(3x^{3} - 2x - 1\right)\left(2\right)}{\left(2x - 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25 · shortfall=4

### C=4 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{3x^{3} - 2x - 1}{2x - 1}\right)$
- Answer: $\frac{\left(9x^{2} - 2\right)\left(2x - 1\right)-\left(3x^{3} - 2x - 1\right)\left(2\right)}{\left(2x - 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=4 · S=4 · amax=25 · shortfall=4

### C=4 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{3x^{3} - 2x - 1}{2x - 1}\right)$
- Answer: $\frac{\left(9x^{2} - 2\right)\left(2x - 1\right)-\left(3x^{3} - 2x - 1\right)\left(2\right)}{\left(2x - 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=4 · S=8 · amax=25 · shortfall=4

### C=4 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{3x^{3} - 2x - 1}{2x - 1}\right)$
- Answer: $\frac{\left(9x^{2} - 2\right)\left(2x - 1\right)-\left(3x^{3} - 2x - 1\right)\left(2\right)}{\left(2x - 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=4 · S=16 · amax=25 · shortfall=4

### C=4 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{3x^{3} - 2x - 1}{2x - 1}\right)$
- Answer: $\frac{\left(9x^{2} - 2\right)\left(2x - 1\right)-\left(3x^{3} - 2x - 1\right)\left(2\right)}{\left(2x - 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=4 · S=32 · amax=25 · shortfall=4

### C=8 · S=0

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\cos(5x)}{5x + 3}\right)$
- Answer: $\frac{\left(-5\sin(5x)\right)\left(5x + 3\right)-\left(\cos(5x)\right)\left(5\right)}{\left(5x + 3\right)^{2}}$
- From: `form:quotient_trig_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25

### C=8 · S=4

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\cos(5x)}{5x + 3}\right)$
- Answer: $\frac{\left(-5\sin(5x)\right)\left(5x + 3\right)-\left(\cos(5x)\right)\left(5\right)}{\left(5x + 3\right)^{2}}$
- From: `form:quotient_trig_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\cos(5x)}{5x + 3}\right)$
- Answer: $\frac{\left(-5\sin(5x)\right)\left(5x + 3\right)-\left(\cos(5x)\right)\left(5\right)}{\left(5x + 3\right)^{2}}$
- From: `form:quotient_trig_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\cos(5x)}{5x + 3}\right)$
- Answer: $\frac{\left(-5\sin(5x)\right)\left(5x + 3\right)-\left(\cos(5x)\right)\left(5\right)}{\left(5x + 3\right)^{2}}$
- From: `form:quotient_trig_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\text{Find }\frac{d}{dx}\left(\frac{\cos(5x)}{5x + 3}\right)$
- Answer: $\frac{\left(-5\sin(5x)\right)\left(5x + 3\right)-\left(\cos(5x)\right)\left(5\right)}{\left(5x + 3\right)^{2}}$
- From: `form:quotient_trig_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\frac{d}{dx}\left[\frac{2x^{4} - 2x^{2}}{4x - 4}\right]$
- Answer: $\frac{\left(8x^{3} - 4x\right)\left(4x - 4\right)-\left(2x^{4} - 2x^{2}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=8.5

### C=12 · S=4

- Prompt: $\frac{d}{dx}\left[\frac{2x^{4} - 2x^{2}}{4x - 4}\right]$
- Answer: $\frac{\left(8x^{3} - 4x\right)\left(4x - 4\right)-\left(2x^{4} - 2x^{2}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=12 · S=4 · amax=25 · shortfall=8.5

### C=12 · S=8

- Prompt: $\frac{d}{dx}\left[\frac{2x^{4} - 2x^{2}}{4x - 4}\right]$
- Answer: $\frac{\left(8x^{3} - 4x\right)\left(4x - 4\right)-\left(2x^{4} - 2x^{2}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=12 · S=8 · amax=25 · shortfall=8.5

### C=12 · S=16

- Prompt: $\frac{d}{dx}\left[\frac{2x^{4} - 2x^{2}}{4x - 4}\right]$
- Answer: $\frac{\left(8x^{3} - 4x\right)\left(4x - 4\right)-\left(2x^{4} - 2x^{2}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=12 · S=16 · amax=25 · shortfall=8.5

### C=12 · S=32

- Prompt: $\frac{d}{dx}\left[\frac{2x^{4} - 2x^{2}}{4x - 4}\right]$
- Answer: $\frac{\left(8x^{3} - 4x\right)\left(4x - 4\right)-\left(2x^{4} - 2x^{2}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=12 · S=32 · amax=25 · shortfall=8.5

### C=16 · S=0

- Prompt: $\frac{d}{dx}\left[\frac{e^{e^{5x}}}{4x - 4}\right]$
- Answer: $\frac{\left(e^{e^{5x}}e^{5x}\left(5\right)\right)\left(4x - 4\right)-\left(e^{e^{5x}}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25

### C=16 · S=4

- Prompt: $\frac{d}{dx}\left[\frac{e^{e^{5x}}}{4x - 4}\right]$
- Answer: $\frac{\left(e^{e^{5x}}e^{5x}\left(5\right)\right)\left(4x - 4\right)-\left(e^{e^{5x}}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=16 · S=4 · amax=25

### C=16 · S=8

- Prompt: $\frac{d}{dx}\left[\frac{e^{e^{5x}}}{4x - 4}\right]$
- Answer: $\frac{\left(e^{e^{5x}}e^{5x}\left(5\right)\right)\left(4x - 4\right)-\left(e^{e^{5x}}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=16 · S=8 · amax=25

### C=16 · S=16

- Prompt: $\frac{d}{dx}\left[\frac{e^{e^{5x}}}{4x - 4}\right]$
- Answer: $\frac{\left(e^{e^{5x}}e^{5x}\left(5\right)\right)\left(4x - 4\right)-\left(e^{e^{5x}}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=16 · S=16 · amax=25

### C=16 · S=32

- Prompt: $\frac{d}{dx}\left[\frac{e^{e^{5x}}}{4x - 4}\right]$
- Answer: $\frac{\left(e^{e^{5x}}e^{5x}\left(5\right)\right)\left(4x - 4\right)-\left(e^{e^{5x}}\right)\left(4\right)}{\left(4x - 4\right)^{2}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=16 · S=32 · amax=25

### C=20 · S=0

- Prompt: $\frac{d}{dx}\left[\frac{e^{\left(4x + 3\right)}}{4x - 5}\right]$
- Answer: $\frac{\left(e^{\left(4x + 3\right)}\left(4\right)\right)\left(4x - 5\right)-\left(e^{\left(4x + 3\right)}\right)\left(4\right)}{\left(4x - 5\right)^{2}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=4

### C=20 · S=4

- Prompt: $\frac{d}{dx}\left[\frac{e^{\left(4x + 3\right)}}{4x - 5}\right]$
- Answer: $\frac{\left(e^{\left(4x + 3\right)}\left(4\right)\right)\left(4x - 5\right)-\left(e^{\left(4x + 3\right)}\right)\left(4\right)}{\left(4x - 5\right)^{2}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=4 · amax=25 · shortfall=4

### C=20 · S=8

- Prompt: $\frac{d}{dx}\left[\frac{e^{\left(4x + 3\right)}}{4x - 5}\right]$
- Answer: $\frac{\left(e^{\left(4x + 3\right)}\left(4\right)\right)\left(4x - 5\right)-\left(e^{\left(4x + 3\right)}\right)\left(4\right)}{\left(4x - 5\right)^{2}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=8 · amax=25 · shortfall=4

### C=20 · S=16

- Prompt: $\frac{d}{dx}\left[\frac{e^{\left(4x + 3\right)}}{4x - 5}\right]$
- Answer: $\frac{\left(e^{\left(4x + 3\right)}\left(4\right)\right)\left(4x - 5\right)-\left(e^{\left(4x + 3\right)}\right)\left(4\right)}{\left(4x - 5\right)^{2}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=16 · amax=25 · shortfall=4

### C=20 · S=32

- Prompt: $\frac{d}{dx}\left[\frac{e^{\left(4x + 3\right)}}{4x - 5}\right]$
- Answer: $\frac{\left(e^{\left(4x + 3\right)}\left(4\right)\right)\left(4x - 5\right)-\left(e^{\left(4x + 3\right)}\right)\left(4\right)}{\left(4x - 5\right)^{2}}$
- From: `form:quotient_exp_poly` · `conceptual:chain+power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=32 · amax=25 · shortfall=4

### C=25 · S=0

- Prompt: $\frac{d}{dx}\left[\frac{2x^{4}}{4x + 1}\right]$
- Answer: $\frac{\left(8x^{3}\right)\left(4x + 1\right)-\left(2x^{4}\right)\left(4\right)}{\left(4x + 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=15.5

### C=25 · S=4

- Prompt: $\frac{d}{dx}\left[\frac{2x^{4}}{4x + 1}\right]$
- Answer: $\frac{\left(8x^{3}\right)\left(4x + 1\right)-\left(2x^{4}\right)\left(4\right)}{\left(4x + 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=25 · S=4 · amax=25 · shortfall=15.5

### C=25 · S=8

- Prompt: $\frac{d}{dx}\left[\frac{2x^{4}}{4x + 1}\right]$
- Answer: $\frac{\left(8x^{3}\right)\left(4x + 1\right)-\left(2x^{4}\right)\left(4\right)}{\left(4x + 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=25 · S=8 · amax=25 · shortfall=15.5

### C=25 · S=16

- Prompt: $\frac{d}{dx}\left[\frac{2x^{4}}{4x + 1}\right]$
- Answer: $\frac{\left(8x^{3}\right)\left(4x + 1\right)-\left(2x^{4}\right)\left(4\right)}{\left(4x + 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=25 · S=16 · amax=25 · shortfall=15.5

### C=25 · S=32

- Prompt: $\frac{d}{dx}\left[\frac{2x^{4}}{4x + 1}\right]$
- Answer: $\frac{\left(8x^{3}\right)\left(4x + 1\right)-\left(2x^{4}\right)\left(4\right)}{\left(4x + 1\right)^{2}}$
- From: `form:quotient_poly` · `conceptual:power+quotient+sum` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=25 · S=32 · amax=25 · shortfall=15.5
