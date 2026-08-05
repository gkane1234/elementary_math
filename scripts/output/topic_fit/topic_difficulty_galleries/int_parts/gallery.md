# Integrals — integration by parts

**type_id:** `calc_indef_int_integration_by_parts` · **leaf:** `integration_by_parts`  
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
| **C=0** | $\int \ln(x)\,dx$ | $\int  \frac{-\left(1+x\right)\ln(x)}{-\left(1+x\right)}\,dx$ | $\int  -\left(-\frac{\left(x-1\right)\ln(x)}{x-1}\right)\,dx$ | $\int  -\left(-\left(\left(\frac{-\left(2+x\right)\ln(x)}{-\left(2+x\right)}+6\right)-6\right)\right)\,dx$ | $\int  \frac{-\left(1-x\right)\left(\left(\ln(x)+3\right)-3\right)+\left(-2x\right)-\left(-2x\right)}{-\left(1-x\right)}\,dx$ |
| **C=4** | $\int x\cos(x)\,dx$ | $\int  -\left(-x\cos(x)\right)\,dx$ | $\int  -\left(-\left(\left(x\cos(x)+5\right)-5\right)\right)\,dx$ | $\int  \frac{3\left(x-1\right)\left(-\left(-\left(\left(x\cos(x)+1\right)-1\right)\right)\right)}{3\left(x-1\right)}\,dx$ | $\int  \left(\left(\frac{\left(x+1\right)x\cos(x)}{x+1}+3\right)-3\right)+3-3\,dx$ |
| **C=8** | $\int xe^{x}\,dx$ | $\int  \frac{\left(x-3\right)xe^{x}}{x-3}\,dx$ | $\int  -\left(-\frac{\left(x-2\right)xe^{x}}{x-2}\right)\,dx$ | $\int  \left(\left(-\left(-xe^{x}\right)\right)+\left(-2x+2\right)\right)-\left(-2x+2\right)+4-4\,dx$ | $\int  \left(\left(-\left(-\frac{-\left(2+x\right)xe^{x}}{-\left(2+x\right)}\right)\right)+\left(x-1\right)\right)-\left(x-1\right)\,dx$ |
| **C=12** | $\int x\cos(x)\,dx$ | $\int  \left(x\cos(x)+\left(x+3\right)\right)-\left(x+3\right)\,dx$ | $\int  \left(\frac{\left(x-1\right)x\cos(x)}{x-1}+\left(x+2\right)\right)-\left(x+2\right)\,dx$ | $\int  \left(\left(\left(-\left(-x\cos(x)\right)\right)+3\right)-3\right)+2-2\,dx$ | $\int  \frac{-\left(1+x\right)\left(\left(-\left(-x\cos(x)\right)\right)+\left(-x\right)\right)-\left(-x\right)}{-\left(1+x\right)}\,dx$ |
| **C=16** | $\int e^{x}\sin(x)\,dx$ | $\int  e^{x}\sin(x)+\left(2x+2\right)-\left(2x+2\right)\,dx$ | $\int  \left(e^{x}\sin(x)+2-2\right)+\left(-x-2\right)-\left(-x-2\right)\,dx$ | $\int  \left(-\left(-\frac{-\left(2-x\right)e^{x}\sin(x)}{-\left(2-x\right)}\right)\right)+4-4\,dx$ | $\int  \frac{\left(x+2\right)\left(-\left(-e^{x}\sin(x)\right)\right)}{x+2}+\left(-x-2\right)-\left(-x-2\right)\,dx$ |
| **C=20** | $\int e^{x}\cos(x)\,dx$ | $\int  \frac{2\left(x-1\right)e^{x}\cos(x)}{2\left(x-1\right)}\,dx$ | $\int  \frac{4\left(x+1\right)\left(-\left(-e^{x}\cos(x)\right)\right)}{4\left(x+1\right)}\,dx$ | $\int  \left(\frac{\left(x+2\right)\left(\left(e^{x}\cos(x)+2\right)-2\right)}{x+2}+6\right)-6\,dx$ | $\int  \left(\left(\left(\frac{2\left(x+2\right)e^{x}\cos(x)}{2\left(x+2\right)}+1\right)-1\right)+\left(3x+1\right)\right)-\left(3x+1\right)\,dx$ |
| **C=25** | $\int xe^{x}\,dx$ | $\int  -\left(-xe^{x}\right)\,dx$ | $\int  \left(\left(xe^{x}+\left(-2x-2\right)\right)-\left(-2x-2\right)+4\right)-4\,dx$ | $\int  \left(\frac{\left(x-1\right)\left(-\left(-xe^{x}\right)\right)}{x-1}+5\right)-5\,dx$ | $\int  \left(\left(\left(\frac{4\left(x+3\right)xe^{x}}{4\left(x+3\right)}+2\right)-2\right)+4\right)-4\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $x\ln(x)-x+C$ | $x\ln(x)-x+C$ | $x\ln(x)-x+C$ | $x\ln(x)-x+C$ | $x\ln(x)-x+C$ |
| **C=4** | $x\sin(x)+\cos(x)+C$ | $x\sin(x)+\cos(x)+C$ | $x\sin(x)+\cos(x)+C$ | $x\sin(x)+\cos(x)+C$ | $x\sin(x)+\cos(x)+C$ |
| **C=8** | $e^{x}(x-1)+C$ | $e^{x}(x-1)+C$ | $e^{x}(x-1)+C$ | $e^{x}(x-1)+C$ | $e^{x}(x-1)+C$ |
| **C=12** | $x\sin(x)+\cos(x)+C$ | $x\sin(x)+\cos(x)+C$ | $x\sin(x)+\cos(x)+C$ | $x\sin(x)+\cos(x)+C$ | $x\sin(x)+\cos(x)+C$ |
| **C=16** | $\frac{1}{2}e^{x}(\sin(x)-\cos(x))+C$ | $\frac{1}{2}e^{x}(\sin(x)-\cos(x))+C$ | $\frac{1}{2}e^{x}(\sin(x)-\cos(x))+C$ | $\frac{1}{2}e^{x}(\sin(x)-\cos(x))+C$ | $\frac{1}{2}e^{x}(\sin(x)-\cos(x))+C$ |
| **C=20** | $\frac{1}{2}e^{x}(\sin(x)+\cos(x))+C$ | $\frac{1}{2}e^{x}(\sin(x)+\cos(x))+C$ | $\frac{1}{2}e^{x}(\sin(x)+\cos(x))+C$ | $\frac{1}{2}e^{x}(\sin(x)+\cos(x))+C$ | $\frac{1}{2}e^{x}(\sin(x)+\cos(x))+C$ |
| **C=25** | $e^{x}(x-1)+C$ | $e^{x}(x-1)+C$ | $e^{x}(x-1)+C$ | $e^{x}(x-1)+C$ | $e^{x}(x-1)+C$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int \ln(x)\,dx$
- Answer: $x\ln(x)-x+C$
- From: `form:ln_alone` · `conceptual:parts` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int  \frac{-\left(1+x\right)\ln(x)}{-\left(1+x\right)}\,dx$
- Answer: $x\ln(x)-x+C$
- From: `form:ln_alone` · `conceptual:parts` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int  -\left(-\frac{\left(x-1\right)\ln(x)}{x-1}\right)\,dx$
- Answer: $x\ln(x)-x+C$
- From: `form:ln_alone` · `conceptual:parts` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int  -\left(-\left(\left(\frac{-\left(2+x\right)\ln(x)}{-\left(2+x\right)}+6\right)-6\right)\right)\,dx$
- Answer: $x\ln(x)-x+C$
- From: `form:ln_alone` · `conceptual:parts` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int  \frac{-\left(1-x\right)\left(\left(\ln(x)+3\right)-3\right)+\left(-2x\right)-\left(-2x\right)}{-\left(1-x\right)}\,dx$
- Answer: $x\ln(x)-x+C$
- From: `form:ln_alone` · `conceptual:parts` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int x\cos(x)\,dx$
- Answer: $x\sin(x)+\cos(x)+C$
- From: `form:poly1_cos` · `conceptual:parts` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\int  -\left(-x\cos(x)\right)\,dx$
- Answer: $x\sin(x)+\cos(x)+C$
- From: `form:poly1_cos` · `conceptual:parts` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\int  -\left(-\left(\left(x\cos(x)+5\right)-5\right)\right)\,dx$
- Answer: $x\sin(x)+\cos(x)+C$
- From: `form:poly1_cos` · `conceptual:parts` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_const`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\int  \frac{3\left(x-1\right)\left(-\left(-\left(\left(x\cos(x)+1\right)-1\right)\right)\right)}{3\left(x-1\right)}\,dx$
- Answer: $x\sin(x)+\cos(x)+C$
- From: `form:poly1_cos` · `conceptual:parts` · `effort:add_cancel_const` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\int  \left(\left(\frac{\left(x+1\right)x\cos(x)}{x+1}+3\right)-3\right)+3-3\,dx$
- Answer: $x\sin(x)+\cos(x)+C$
- From: `form:poly1_cos` · `conceptual:parts` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\int xe^{x}\,dx$
- Answer: $e^{x}(x-1)+C$
- From: `form:poly1_exp` · `conceptual:parts` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25 · shortfall=2.5

### C=8 · S=4

- Prompt: $\int  \frac{\left(x-3\right)xe^{x}}{x-3}\,dx$
- Answer: $e^{x}(x-1)+C$
- From: `form:poly1_exp` · `conceptual:parts` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=8 · S=4 · amax=25 · shortfall=1.5

### C=8 · S=8

- Prompt: $\int  -\left(-\frac{\left(x-2\right)xe^{x}}{x-2}\right)\,dx$
- Answer: $e^{x}(x-1)+C$
- From: `form:poly1_exp` · `conceptual:parts` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=8 · amax=25 · shortfall=0.5

### C=8 · S=16

- Prompt: $\int  \left(\left(-\left(-xe^{x}\right)\right)+\left(-2x+2\right)\right)-\left(-2x+2\right)+4-4\,dx$
- Answer: $e^{x}(x-1)+C$
- From: `form:poly1_exp` · `conceptual:parts` · `effort:double_neg` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\int  \left(\left(-\left(-\frac{-\left(2+x\right)xe^{x}}{-\left(2+x\right)}\right)\right)+\left(x-1\right)\right)-\left(x-1\right)\,dx$
- Answer: $e^{x}(x-1)+C$
- From: `form:poly1_exp` · `conceptual:parts` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\int x\cos(x)\,dx$
- Answer: $x\sin(x)+\cos(x)+C$
- From: `form:poly1_cos` · `conceptual:parts` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=0 · amax=25 · shortfall=6.5

### C=12 · S=4

- Prompt: $\int  \left(x\cos(x)+\left(x+3\right)\right)-\left(x+3\right)\,dx$
- Answer: $x\sin(x)+\cos(x)+C$
- From: `form:poly1_cos` · `conceptual:parts` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=12 · S=4 · amax=25 · shortfall=5.5

### C=12 · S=8

- Prompt: $\int  \left(\frac{\left(x-1\right)x\cos(x)}{x-1}+\left(x+2\right)\right)-\left(x+2\right)\,dx$
- Answer: $x\sin(x)+\cos(x)+C$
- From: `form:poly1_cos` · `conceptual:parts` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait`
- Flags: C=12 · S=8 · amax=25 · shortfall=4.5

### C=12 · S=16

- Prompt: $\int  \left(\left(\left(-\left(-x\cos(x)\right)\right)+3\right)-3\right)+2-2\,dx$
- Answer: $x\sin(x)+\cos(x)+C$
- From: `form:poly1_cos` · `conceptual:parts` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `effort:double_neg`
- Flags: C=12 · S=16 · amax=25 · shortfall=3.5

### C=12 · S=32

- Prompt: $\int  \frac{-\left(1+x\right)\left(\left(-\left(-x\cos(x)\right)\right)+\left(-x\right)\right)-\left(-x\right)}{-\left(1+x\right)}\,dx$
- Answer: $x\sin(x)+\cos(x)+C$
- From: `form:poly1_cos` · `conceptual:parts` · `effort:double_neg` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=32 · amax=25 · shortfall=3.5

### C=16 · S=0

- Prompt: $\int e^{x}\sin(x)\,dx$
- Answer: $\frac{1}{2}e^{x}(\sin(x)-\cos(x))+C$
- From: `form:cyclic_exp_sin` · `conceptual:parts` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=5

### C=16 · S=4

- Prompt: $\int  e^{x}\sin(x)+\left(2x+2\right)-\left(2x+2\right)\,dx$
- Answer: $\frac{1}{2}e^{x}(\sin(x)-\cos(x))+C$
- From: `form:cyclic_exp_sin` · `conceptual:parts` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=16 · S=4 · amax=25 · shortfall=4

### C=16 · S=8

- Prompt: $\int  \left(e^{x}\sin(x)+2-2\right)+\left(-x-2\right)-\left(-x-2\right)\,dx$
- Answer: $\frac{1}{2}e^{x}(\sin(x)-\cos(x))+C$
- From: `form:cyclic_exp_sin` · `conceptual:parts` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=8 · amax=25 · shortfall=3

### C=16 · S=16

- Prompt: $\int  \left(-\left(-\frac{-\left(2-x\right)e^{x}\sin(x)}{-\left(2-x\right)}\right)\right)+4-4\,dx$
- Answer: $\frac{1}{2}e^{x}(\sin(x)-\cos(x))+C$
- From: `form:cyclic_exp_sin` · `conceptual:parts` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=16 · amax=25 · shortfall=2

### C=16 · S=32

- Prompt: $\int  \frac{\left(x+2\right)\left(-\left(-e^{x}\sin(x)\right)\right)}{x+2}+\left(-x-2\right)-\left(-x-2\right)\,dx$
- Answer: $\frac{1}{2}e^{x}(\sin(x)-\cos(x))+C$
- From: `form:cyclic_exp_sin` · `conceptual:parts` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=32 · amax=25 · shortfall=2

### C=20 · S=0

- Prompt: $\int e^{x}\cos(x)\,dx$
- Answer: $\frac{1}{2}e^{x}(\sin(x)+\cos(x))+C$
- From: `form:cyclic_exp_cos` · `conceptual:parts` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=7

### C=20 · S=4

- Prompt: $\int  \frac{2\left(x-1\right)e^{x}\cos(x)}{2\left(x-1\right)}\,dx$
- Answer: $\frac{1}{2}e^{x}(\sin(x)+\cos(x))+C$
- From: `form:cyclic_exp_cos` · `conceptual:parts` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=20 · S=4 · amax=25 · shortfall=6

### C=20 · S=8

- Prompt: $\int  \frac{4\left(x+1\right)\left(-\left(-e^{x}\cos(x)\right)\right)}{4\left(x+1\right)}\,dx$
- Answer: $\frac{1}{2}e^{x}(\sin(x)+\cos(x))+C$
- From: `form:cyclic_exp_cos` · `conceptual:parts` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=8 · amax=25 · shortfall=5

### C=20 · S=16

- Prompt: $\int  \left(\frac{\left(x+2\right)\left(\left(e^{x}\cos(x)+2\right)-2\right)}{x+2}+6\right)-6\,dx$
- Answer: $\frac{1}{2}e^{x}(\sin(x)+\cos(x))+C$
- From: `form:cyclic_exp_cos` · `conceptual:parts` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=16 · amax=25 · shortfall=4

### C=20 · S=32

- Prompt: $\int  \left(\left(\left(\frac{2\left(x+2\right)e^{x}\cos(x)}{2\left(x+2\right)}+1\right)-1\right)+\left(3x+1\right)\right)-\left(3x+1\right)\,dx$
- Answer: $\frac{1}{2}e^{x}(\sin(x)+\cos(x))+C$
- From: `form:cyclic_exp_cos` · `conceptual:parts` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=32 · amax=25 · shortfall=4

### C=25 · S=0

- Prompt: $\int xe^{x}\,dx$
- Answer: $e^{x}(x-1)+C$
- From: `form:poly1_exp` · `conceptual:parts` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=17.5

### C=25 · S=4

- Prompt: $\int  -\left(-xe^{x}\right)\,dx$
- Answer: $e^{x}(x-1)+C$
- From: `form:poly1_exp` · `conceptual:parts` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=25 · S=4 · amax=25 · shortfall=16.5

### C=25 · S=8

- Prompt: $\int  \left(\left(xe^{x}+\left(-2x-2\right)\right)-\left(-2x-2\right)+4\right)-4\,dx$
- Answer: $e^{x}(x-1)+C$
- From: `form:poly1_exp` · `conceptual:parts` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=8 · amax=25 · shortfall=15.5

### C=25 · S=16

- Prompt: $\int  \left(\frac{\left(x-1\right)\left(-\left(-xe^{x}\right)\right)}{x-1}+5\right)-5\,dx$
- Answer: $e^{x}(x-1)+C$
- From: `form:poly1_exp` · `conceptual:parts` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=16 · amax=25 · shortfall=14.5

### C=25 · S=32

- Prompt: $\int  \left(\left(\left(\frac{4\left(x+3\right)xe^{x}}{4\left(x+3\right)}+2\right)-2\right)+4\right)-4\,dx$
- Answer: $e^{x}(x-1)+C$
- From: `form:poly1_exp` · `conceptual:parts` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=32 · amax=25 · shortfall=14.5
