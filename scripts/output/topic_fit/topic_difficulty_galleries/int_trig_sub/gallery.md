# Integrals — trigonometric substitution

**type_id:** `calc_indef_int_trigonometric_with_substitution` · **leaf:** `integral_substitution`  
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
| **C=0** | $\int \sqrt{16-x^{2}}\,dx$ | $\int  \left(\sqrt{16-x^{2}}+1\right)-1\,dx$ | $\int  -\left(-\frac{3\left(x-1\right)\sqrt{16-x^{2}}}{3\left(x-1\right)}\right)\,dx$ | $\int  \frac{3\left(x+1\right)\left(-\left(-\left(\sqrt{16-x^{2}}+\left(3x-1\right)-\left(3x-1\right)\right)\right)\right)}{3\left(x+1\right)}\,dx$ | $\int  \left(\left(\left(\frac{4\left(x-1\right)\sqrt{16-x^{2}}}{4\left(x-1\right)}+1\right)-1\right)+2\right)-2\,dx$ |
| **C=4** | $\int \sqrt{9-x^{2}}\,dx$ | $\int  \sqrt{9-x^{2}}+\left(x-2\right)-\left(x-2\right)\,dx$ | $\int  \left(\sqrt{9-x^{2}}+\left(-2x+1\right)-\left(-2x+1\right)\right)+4-4\,dx$ | $\int  \frac{4\left(x-1\right)\left(-\left(-\sqrt{9-x^{2}}\right)\right)}{4\left(x-1\right)}+\left(2x-1\right)-\left(2x-1\right)\,dx$ | $\int  \frac{\left(x+3\right)\left(-\left(-\sqrt{9-x^{2}}\right)\right)}{x+3}+\left(3x+1\right)-\left(3x+1\right)\,dx$ |
| **C=8** | $\int \frac{1}{\sqrt{x^{2}-16}}\,dx$ | $\int  \frac{\left(x-3\right)\frac{1}{\sqrt{x^{2}-16}}}{x-3}\,dx$ | $\int  \frac{-\left(1+x\right)\left(\frac{1}{\sqrt{x^{2}-16}}+\left(-2x-2\right)-\left(-2x-2\right)\right)}{-\left(1+x\right)}\,dx$ | $\int  -\left(-\left(\left(\left(\left(\frac{1}{\sqrt{x^{2}-16}}+6\right)-6\right)+3\right)-3\right)\right)\,dx$ | $\int  \left(\frac{2\left(x+2\right)\left(-\left(-\frac{1}{\sqrt{x^{2}-16}}\right)\right)}{2\left(x+2\right)}+3\right)-3\,dx$ |
| **C=12** | $\int \frac{1}{\left(16+x^{2}\right)^{\frac{3}{2}}}\,dx$ | $\int  \frac{-\left(3+x\right)\frac{1}{\left(16+x^{2}\right)^{\frac{3}{2}}}}{-\left(3+x\right)}\,dx$ | $\int  \frac{-\left(1+x\right)\left(\frac{1}{\left(16+x^{2}\right)^{\frac{3}{2}}}+5-5\right)}{-\left(1+x\right)}\,dx$ | $\int  \left(\left(\left(\left(\frac{1}{\left(16+x^{2}\right)^{\frac{3}{2}}}+4\right)-4\right)+2\right)-2\right)+3-3\,dx$ | $\int  \left(\left(-\left(-\frac{1}{\left(16+x^{2}\right)^{\frac{3}{2}}}\right)\right)+4-4\right)+3-3\,dx$ |
| **C=16** | $\int \left(25-x^{2}\right)^{\frac{5}{2}}\,dx$ | $\int  \frac{-\left(2+x\right)\left(\left(25-x^{2}\right)^{\frac{5}{2}}\right)}{-\left(2+x\right)}\,dx$ | $\int  \left(\left(-\left(-\left(\left(25-x^{2}\right)^{\frac{5}{2}}\right)\right)\right)+5\right)-5\,dx$ | $\int  \left(\left(\left(\left(\left(\left(25-x^{2}\right)^{\frac{5}{2}}\right)+2\right)-2\right)+\left(-2x-1\right)\right)-\left(-2x-1\right)+\left(x+1\right)\right)-\left(x+1\right)\,dx$ | $\int  \frac{\left(x-2\right)\left(\left(\left(\left(25-x^{2}\right)^{\frac{5}{2}}\right)+5-5\right)+\left(2x+1\right)\right)-\left(2x+1\right)}{x-2}\,dx$ |
| **C=20** | $\int \frac{1}{\left(4-x^{2}\right)^{\frac{3}{2}}}\,dx$ | $\int  -\left(-\frac{1}{\left(4-x^{2}\right)^{\frac{3}{2}}}\right)\,dx$ | $\int  \left(\left(-\left(-\frac{1}{\left(4-x^{2}\right)^{\frac{3}{2}}}\right)\right)+1\right)-1\,dx$ | $\int  \left(\left(\left(\left(\frac{1}{\left(4-x^{2}\right)^{\frac{3}{2}}}+3\right)-3\right)+5\right)-5\right)+\left(-x\right)-\left(-x\right)\,dx$ | $\int  \left(\left(\left(-\left(-\frac{1}{\left(4-x^{2}\right)^{\frac{3}{2}}}\right)\right)+1\right)-1\right)+2-2\,dx$ |
| **C=25** | $\int \left(9+\left(x - 2\right)^{2}\right)^{\frac{3}{2}}\,dx$ | $\int  \frac{3\left(x+1\right)\left(\left(9+\left(x - 2\right)^{2}\right)^{\frac{3}{2}}\right)}{3\left(x+1\right)}\,dx$ | $\int  \left(\left(\left(\left(9+\left(x - 2\right)^{2}\right)^{\frac{3}{2}}\right)+4\right)-4\right)+\left(3x-1\right)-\left(3x-1\right)\,dx$ | $\int  \frac{-\left(1+x\right)\left(\left(\left(\left(9+\left(x - 2\right)^{2}\right)^{\frac{3}{2}}\right)+\left(-2x-2\right)\right)-\left(-2x-2\right)+\left(x+3\right)\right)-\left(x+3\right)}{-\left(1+x\right)}\,dx$ | $\int  \left(\left(\left(-\left(-\left(\left(9+\left(x - 2\right)^{2}\right)^{\frac{3}{2}}\right)\right)\right)+3-3\right)+\left(3x\right)\right)-\left(3x\right)\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ |
| **C=4** | $\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)+C$ | $\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)+C$ | $\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)+C$ | $\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)+C$ | $\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)+C$ |
| **C=8** | $\ln\left|x+\sqrt{x^{2}-16}\right|+C$ | $\ln\left|x+\sqrt{x^{2}-16}\right|+C$ | $\ln\left|x+\sqrt{x^{2}-16}\right|+C$ | $\ln\left|x+\sqrt{x^{2}-16}\right|+C$ | $\ln\left|x+\sqrt{x^{2}-16}\right|+C$ |
| **C=12** | $\frac{x}{16\sqrt{16+x^{2}}}+C$ | $\frac{x}{16\sqrt{16+x^{2}}}+C$ | $\frac{x}{16\sqrt{16+x^{2}}}+C$ | $\frac{x}{16\sqrt{16+x^{2}}}+C$ | $\frac{x}{16\sqrt{16+x^{2}}}+C$ |
| **C=16** | $\frac{x}{48}\left(8x^{2}^{2}+1025x^{2}+1525^{2}\right)\sqrt{25-x^{2}}+\frac{15625}{16}\arcsin\left(\frac{x}{5}\right)+C$ | $\frac{x}{48}\left(8x^{2}^{2}+1025x^{2}+1525^{2}\right)\sqrt{25-x^{2}}+\frac{15625}{16}\arcsin\left(\frac{x}{5}\right)+C$ | $\frac{x}{48}\left(8x^{2}^{2}+1025x^{2}+1525^{2}\right)\sqrt{25-x^{2}}+\frac{15625}{16}\arcsin\left(\frac{x}{5}\right)+C$ | $\frac{x}{48}\left(8x^{2}^{2}+1025x^{2}+1525^{2}\right)\sqrt{25-x^{2}}+\frac{15625}{16}\arcsin\left(\frac{x}{5}\right)+C$ | $\frac{x}{48}\left(8x^{2}^{2}+1025x^{2}+1525^{2}\right)\sqrt{25-x^{2}}+\frac{15625}{16}\arcsin\left(\frac{x}{5}\right)+C$ |
| **C=20** | $\frac{x}{4\sqrt{4-x^{2}}}+C$ | $\frac{x}{4\sqrt{4-x^{2}}}+C$ | $\frac{x}{4\sqrt{4-x^{2}}}+C$ | $\frac{x}{4\sqrt{4-x^{2}}}+C$ | $\frac{x}{4\sqrt{4-x^{2}}}+C$ |
| **C=25** | $\frac{\left(x - 2\right)}{8}\left(2\left(x - 2\right)^{2}+9\right)\sqrt{9+\left(x - 2\right)^{2}}+\frac{81}{8}\ln\left|x - 2+\sqrt{9+\left(x - 2\right)^{2}}\right|+C$ | $\frac{\left(x - 2\right)}{8}\left(2\left(x - 2\right)^{2}+9\right)\sqrt{9+\left(x - 2\right)^{2}}+\frac{81}{8}\ln\left|x - 2+\sqrt{9+\left(x - 2\right)^{2}}\right|+C$ | $\frac{\left(x - 2\right)}{8}\left(2\left(x - 2\right)^{2}+9\right)\sqrt{9+\left(x - 2\right)^{2}}+\frac{81}{8}\ln\left|x - 2+\sqrt{9+\left(x - 2\right)^{2}}\right|+C$ | $\frac{\left(x - 2\right)}{8}\left(2\left(x - 2\right)^{2}+9\right)\sqrt{9+\left(x - 2\right)^{2}}+\frac{81}{8}\ln\left|x - 2+\sqrt{9+\left(x - 2\right)^{2}}\right|+C$ | $\frac{\left(x - 2\right)}{8}\left(2\left(x - 2\right)^{2}+9\right)\sqrt{9+\left(x - 2\right)^{2}}+\frac{81}{8}\ln\left|x - 2+\sqrt{9+\left(x - 2\right)^{2}}\right|+C$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int \sqrt{16-x^{2}}\,dx$
- Answer: $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$
- From: `form:sqrt_a2_minus_x2` · `conceptual:trig_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int  \left(\sqrt{16-x^{2}}+1\right)-1\,dx$
- Answer: $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$
- From: `form:sqrt_a2_minus_x2` · `conceptual:trig_sub` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int  -\left(-\frac{3\left(x-1\right)\sqrt{16-x^{2}}}{3\left(x-1\right)}\right)\,dx$
- Answer: $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$
- From: `form:sqrt_a2_minus_x2` · `conceptual:trig_sub` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int  \frac{3\left(x+1\right)\left(-\left(-\left(\sqrt{16-x^{2}}+\left(3x-1\right)-\left(3x-1\right)\right)\right)\right)}{3\left(x+1\right)}\,dx$
- Answer: $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$
- From: `form:sqrt_a2_minus_x2` · `conceptual:trig_sub` · `effort:add_cancel_linear` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int  \left(\left(\left(\frac{4\left(x-1\right)\sqrt{16-x^{2}}}{4\left(x-1\right)}+1\right)-1\right)+2\right)-2\,dx$
- Answer: $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$
- From: `form:sqrt_a2_minus_x2` · `conceptual:trig_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int \sqrt{9-x^{2}}\,dx$
- Answer: $\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)+C$
- From: `form:sqrt_a2_minus_x2` · `conceptual:trig_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25 · shortfall=0.5

### C=4 · S=4

- Prompt: $\int  \sqrt{9-x^{2}}+\left(x-2\right)-\left(x-2\right)\,dx$
- Answer: $\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)+C$
- From: `form:sqrt_a2_minus_x2` · `conceptual:trig_sub` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\int  \left(\sqrt{9-x^{2}}+\left(-2x+1\right)-\left(-2x+1\right)\right)+4-4\,dx$
- Answer: $\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)+C$
- From: `form:sqrt_a2_minus_x2` · `conceptual:trig_sub` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\int  \frac{4\left(x-1\right)\left(-\left(-\sqrt{9-x^{2}}\right)\right)}{4\left(x-1\right)}+\left(2x-1\right)-\left(2x-1\right)\,dx$
- Answer: $\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)+C$
- From: `form:sqrt_a2_minus_x2` · `conceptual:trig_sub` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\int  \frac{\left(x+3\right)\left(-\left(-\sqrt{9-x^{2}}\right)\right)}{x+3}+\left(3x+1\right)-\left(3x+1\right)\,dx$
- Answer: $\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)+C$
- From: `form:sqrt_a2_minus_x2` · `conceptual:trig_sub` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\int \frac{1}{\sqrt{x^{2}-16}}\,dx$
- Answer: $\ln\left|x+\sqrt{x^{2}-16}\right|+C$
- From: `form:one_over_sqrt_x2_minus_a2` · `conceptual:trig_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25 · shortfall=4.5

### C=8 · S=4

- Prompt: $\int  \frac{\left(x-3\right)\frac{1}{\sqrt{x^{2}-16}}}{x-3}\,dx$
- Answer: $\ln\left|x+\sqrt{x^{2}-16}\right|+C$
- From: `form:one_over_sqrt_x2_minus_a2` · `conceptual:trig_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=8 · S=4 · amax=25 · shortfall=3.5

### C=8 · S=8

- Prompt: $\int  \frac{-\left(1+x\right)\left(\frac{1}{\sqrt{x^{2}-16}}+\left(-2x-2\right)-\left(-2x-2\right)\right)}{-\left(1+x\right)}\,dx$
- Answer: $\ln\left|x+\sqrt{x^{2}-16}\right|+C$
- From: `form:one_over_sqrt_x2_minus_a2` · `conceptual:trig_sub` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=8 · amax=25 · shortfall=2.5

### C=8 · S=16

- Prompt: $\int  -\left(-\left(\left(\left(\left(\frac{1}{\sqrt{x^{2}-16}}+6\right)-6\right)+3\right)-3\right)\right)\,dx$
- Answer: $\ln\left|x+\sqrt{x^{2}-16}\right|+C$
- From: `form:one_over_sqrt_x2_minus_a2` · `conceptual:trig_sub` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=16 · amax=25 · shortfall=1.5

### C=8 · S=32

- Prompt: $\int  \left(\frac{2\left(x+2\right)\left(-\left(-\frac{1}{\sqrt{x^{2}-16}}\right)\right)}{2\left(x+2\right)}+3\right)-3\,dx$
- Answer: $\ln\left|x+\sqrt{x^{2}-16}\right|+C$
- From: `form:one_over_sqrt_x2_minus_a2` · `conceptual:trig_sub` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=32 · amax=25 · shortfall=1.5

### C=12 · S=0

- Prompt: $\int \frac{1}{\left(16+x^{2}\right)^{\frac{3}{2}}}\,dx$
- Answer: $\frac{x}{16\sqrt{16+x^{2}}}+C$
- From: `form:pow_m3_2_a2_plus` · `conceptual:trig_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=8.5

### C=12 · S=4

- Prompt: $\int  \frac{-\left(3+x\right)\frac{1}{\left(16+x^{2}\right)^{\frac{3}{2}}}}{-\left(3+x\right)}\,dx$
- Answer: $\frac{x}{16\sqrt{16+x^{2}}}+C$
- From: `form:pow_m3_2_a2_plus` · `conceptual:trig_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=12 · S=4 · amax=25 · shortfall=7.5

### C=12 · S=8

- Prompt: $\int  \frac{-\left(1+x\right)\left(\frac{1}{\left(16+x^{2}\right)^{\frac{3}{2}}}+5-5\right)}{-\left(1+x\right)}\,dx$
- Answer: $\frac{x}{16\sqrt{16+x^{2}}}+C$
- From: `form:pow_m3_2_a2_plus` · `conceptual:trig_sub` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=8 · amax=25 · shortfall=6.5

### C=12 · S=16

- Prompt: $\int  \left(\left(\left(\left(\frac{1}{\left(16+x^{2}\right)^{\frac{3}{2}}}+4\right)-4\right)+2\right)-2\right)+3-3\,dx$
- Answer: $\frac{x}{16\sqrt{16+x^{2}}}+C$
- From: `form:pow_m3_2_a2_plus` · `conceptual:trig_sub` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=12 · S=16 · amax=25 · shortfall=5.5

### C=12 · S=32

- Prompt: $\int  \left(\left(-\left(-\frac{1}{\left(16+x^{2}\right)^{\frac{3}{2}}}\right)\right)+4-4\right)+3-3\,dx$
- Answer: $\frac{x}{16\sqrt{16+x^{2}}}+C$
- From: `form:pow_m3_2_a2_plus` · `conceptual:trig_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=32 · amax=25 · shortfall=5.5

### C=16 · S=0

- Prompt: $\int \left(25-x^{2}\right)^{\frac{5}{2}}\,dx$
- Answer: $\frac{x}{48}\left(8x^{2}^{2}+1025x^{2}+1525^{2}\right)\sqrt{25-x^{2}}+\frac{15625}{16}\arcsin\left(\frac{x}{5}\right)+C$
- From: `form:pow_5_2_a2_minus` · `conceptual:trig_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=12.5

### C=16 · S=4

- Prompt: $\int  \frac{-\left(2+x\right)\left(\left(25-x^{2}\right)^{\frac{5}{2}}\right)}{-\left(2+x\right)}\,dx$
- Answer: $\frac{x}{48}\left(8x^{2}^{2}+1025x^{2}+1525^{2}\right)\sqrt{25-x^{2}}+\frac{15625}{16}\arcsin\left(\frac{x}{5}\right)+C$
- From: `form:pow_5_2_a2_minus` · `conceptual:trig_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=16 · S=4 · amax=25 · shortfall=11.5

### C=16 · S=8

- Prompt: $\int  \left(\left(-\left(-\left(\left(25-x^{2}\right)^{\frac{5}{2}}\right)\right)\right)+5\right)-5\,dx$
- Answer: $\frac{x}{48}\left(8x^{2}^{2}+1025x^{2}+1525^{2}\right)\sqrt{25-x^{2}}+\frac{15625}{16}\arcsin\left(\frac{x}{5}\right)+C$
- From: `form:pow_5_2_a2_minus` · `conceptual:trig_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=8 · amax=25 · shortfall=10.5

### C=16 · S=16

- Prompt: $\int  \left(\left(\left(\left(\left(\left(25-x^{2}\right)^{\frac{5}{2}}\right)+2\right)-2\right)+\left(-2x-1\right)\right)-\left(-2x-1\right)+\left(x+1\right)\right)-\left(x+1\right)\,dx$
- Answer: $\frac{x}{48}\left(8x^{2}^{2}+1025x^{2}+1525^{2}\right)\sqrt{25-x^{2}}+\frac{15625}{16}\arcsin\left(\frac{x}{5}\right)+C$
- From: `form:pow_5_2_a2_minus` · `conceptual:trig_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=16 · amax=25 · shortfall=9.5

### C=16 · S=32

- Prompt: $\int  \frac{\left(x-2\right)\left(\left(\left(\left(25-x^{2}\right)^{\frac{5}{2}}\right)+5-5\right)+\left(2x+1\right)\right)-\left(2x+1\right)}{x-2}\,dx$
- Answer: $\frac{x}{48}\left(8x^{2}^{2}+1025x^{2}+1525^{2}\right)\sqrt{25-x^{2}}+\frac{15625}{16}\arcsin\left(\frac{x}{5}\right)+C$
- From: `form:pow_5_2_a2_minus` · `conceptual:trig_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=32 · amax=25 · shortfall=9.5

### C=20 · S=0

- Prompt: $\int \frac{1}{\left(4-x^{2}\right)^{\frac{3}{2}}}\,dx$
- Answer: $\frac{x}{4\sqrt{4-x^{2}}}+C$
- From: `form:pow_m3_2_a2_minus` · `conceptual:trig_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=16.5

### C=20 · S=4

- Prompt: $\int  -\left(-\frac{1}{\left(4-x^{2}\right)^{\frac{3}{2}}}\right)\,dx$
- Answer: $\frac{x}{4\sqrt{4-x^{2}}}+C$
- From: `form:pow_m3_2_a2_minus` · `conceptual:trig_sub` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=20 · S=4 · amax=25 · shortfall=15.5

### C=20 · S=8

- Prompt: $\int  \left(\left(-\left(-\frac{1}{\left(4-x^{2}\right)^{\frac{3}{2}}}\right)\right)+1\right)-1\,dx$
- Answer: $\frac{x}{4\sqrt{4-x^{2}}}+C$
- From: `form:pow_m3_2_a2_minus` · `conceptual:trig_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=8 · amax=25 · shortfall=14.5

### C=20 · S=16

- Prompt: $\int  \left(\left(\left(\left(\frac{1}{\left(4-x^{2}\right)^{\frac{3}{2}}}+3\right)-3\right)+5\right)-5\right)+\left(-x\right)-\left(-x\right)\,dx$
- Answer: $\frac{x}{4\sqrt{4-x^{2}}}+C$
- From: `form:pow_m3_2_a2_minus` · `conceptual:trig_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=16 · amax=25 · shortfall=13.5

### C=20 · S=32

- Prompt: $\int  \left(\left(\left(-\left(-\frac{1}{\left(4-x^{2}\right)^{\frac{3}{2}}}\right)\right)+1\right)-1\right)+2-2\,dx$
- Answer: $\frac{x}{4\sqrt{4-x^{2}}}+C$
- From: `form:pow_m3_2_a2_minus` · `conceptual:trig_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=32 · amax=25 · shortfall=13.5

### C=25 · S=0

- Prompt: $\int \left(9+\left(x - 2\right)^{2}\right)^{\frac{3}{2}}\,dx$
- Answer: $\frac{\left(x - 2\right)}{8}\left(2\left(x - 2\right)^{2}+9\right)\sqrt{9+\left(x - 2\right)^{2}}+\frac{81}{8}\ln\left|x - 2+\sqrt{9+\left(x - 2\right)^{2}}\right|+C$
- From: `form:pow_3_2_a2_plus` · `conceptual:u_sub+trig_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=21.5

### C=25 · S=4

- Prompt: $\int  \frac{3\left(x+1\right)\left(\left(9+\left(x - 2\right)^{2}\right)^{\frac{3}{2}}\right)}{3\left(x+1\right)}\,dx$
- Answer: $\frac{\left(x - 2\right)}{8}\left(2\left(x - 2\right)^{2}+9\right)\sqrt{9+\left(x - 2\right)^{2}}+\frac{81}{8}\ln\left|x - 2+\sqrt{9+\left(x - 2\right)^{2}}\right|+C$
- From: `form:pow_3_2_a2_plus` · `conceptual:u_sub+trig_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=25 · S=4 · amax=25 · shortfall=20.5

### C=25 · S=8

- Prompt: $\int  \left(\left(\left(\left(9+\left(x - 2\right)^{2}\right)^{\frac{3}{2}}\right)+4\right)-4\right)+\left(3x-1\right)-\left(3x-1\right)\,dx$
- Answer: $\frac{\left(x - 2\right)}{8}\left(2\left(x - 2\right)^{2}+9\right)\sqrt{9+\left(x - 2\right)^{2}}+\frac{81}{8}\ln\left|x - 2+\sqrt{9+\left(x - 2\right)^{2}}\right|+C$
- From: `form:pow_3_2_a2_plus` · `conceptual:u_sub+trig_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=8 · amax=25 · shortfall=19.5

### C=25 · S=16

- Prompt: $\int  \frac{-\left(1+x\right)\left(\left(\left(\left(9+\left(x - 2\right)^{2}\right)^{\frac{3}{2}}\right)+\left(-2x-2\right)\right)-\left(-2x-2\right)+\left(x+3\right)\right)-\left(x+3\right)}{-\left(1+x\right)}\,dx$
- Answer: $\frac{\left(x - 2\right)}{8}\left(2\left(x - 2\right)^{2}+9\right)\sqrt{9+\left(x - 2\right)^{2}}+\frac{81}{8}\ln\left|x - 2+\sqrt{9+\left(x - 2\right)^{2}}\right|+C$
- From: `form:pow_3_2_a2_plus` · `conceptual:u_sub+trig_sub` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=16 · amax=25 · shortfall=18.5

### C=25 · S=32

- Prompt: $\int  \left(\left(\left(-\left(-\left(\left(9+\left(x - 2\right)^{2}\right)^{\frac{3}{2}}\right)\right)\right)+3-3\right)+\left(3x\right)\right)-\left(3x\right)\,dx$
- Answer: $\frac{\left(x - 2\right)}{8}\left(2\left(x - 2\right)^{2}+9\right)\sqrt{9+\left(x - 2\right)^{2}}+\frac{81}{8}\ln\left|x - 2+\sqrt{9+\left(x - 2\right)^{2}}\right|+C$
- From: `form:pow_3_2_a2_plus` · `conceptual:u_sub+trig_sub` · `effort:double_neg` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=32 · amax=25 · shortfall=18.5
