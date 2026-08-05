# Integrals — substitution (power)

**type_id:** `calc_indef_int_power_rule_with_substitution` · **leaf:** `integral_substitution`  
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
| **C=0** | $\int \frac{\cos(x)}{\sin^{2}(x)}\,dx$ | $\int  \frac{-\left(2-x\right)\frac{\cos(x)}{\sin^{2}(x)}}{-\left(2-x\right)}\,dx$ | $\int  \left(-\left(-\frac{\cos(x)}{\sin^{2}(x)}\right)\right)+\left(3x-2\right)-\left(3x-2\right)\,dx$ | $\int  \left(\frac{2\left(x-3\right)\frac{\cos(x)}{\sin^{2}(x)}}{2\left(x-3\right)}+3-3\right)+5-5\,dx$ | $\int  \left(\left(\left(\left(-\left(-\frac{\cos(x)}{\sin^{2}(x)}\right)\right)+3\right)-3\right)+4\right)-4\,dx$ |
| **C=4** | $\int 2e^{2x - 3}\,dx$ | $\int  \left(2e^{2x - 3}+\left(3x+2\right)\right)-\left(3x+2\right)\,dx$ | $\int  -\left(-\frac{-\left(3+x\right)2e^{2x - 3}}{-\left(3+x\right)}\right)\,dx$ | $\int  \left(\left(-\left(-2e^{2x - 3}\right)\right)+\left(2x+2\right)\right)-\left(2x+2\right)+2-2\,dx$ | $\int  \frac{-\left(3+x\right)\left(\left(2e^{2x - 3}+2\right)-2\right)}{-\left(3+x\right)}+2-2\,dx$ |
| **C=8** | $\int 4e^{4x + 5}\,dx$ | $\int  \frac{\left(x-3\right)4e^{4x + 5}}{x-3}\,dx$ | $\int  \left(4e^{4x + 5}+\left(x-1\right)-\left(x-1\right)\right)+3-3\,dx$ | $\int  \left(4e^{4x + 5}+\left(3x+2\right)-\left(3x+2\right)\right)+\left(3x+2\right)-\left(3x+2\right)+6-6\,dx$ | $\int  \frac{-\left(2-x\right)\left(-\left(-4e^{4x + 5}\right)\right)}{-\left(2-x\right)}+5-5\,dx$ |
| **C=12** | $\int e^{\cos(x)}\sin(x)\,dx$ | $\int  \frac{\left(x-2\right)e^{\cos(x)}\sin(x)}{x-2}\,dx$ | $\int  -\left(-\left(e^{\cos(x)}\sin(x)+3-3\right)\right)\,dx$ | $\int  \left(\left(\left(-\left(-e^{\cos(x)}\sin(x)\right)\right)+1\right)-1\right)+3-3\,dx$ | $\int  \left(e^{\cos(x)}\sin(x)+\left(2x+3\right)\right)-\left(2x+3\right)+\left(-2x-1\right)-\left(-2x-1\right)+1-1\,dx$ |
| **C=16** | $\int e^{\sin(x)}\cos(x)\,dx$ | $\int  e^{\sin(x)}\cos(x)+5-5\,dx$ | $\int  \left(-\left(-e^{\sin(x)}\cos(x)\right)\right)+4-4\,dx$ | $\int  \frac{4\left(x-2\right)\left(\left(e^{\sin(x)}\cos(x)+6-6\right)+\left(3x\right)\right)-\left(3x\right)}{4\left(x-2\right)}\,dx$ | $\int  \left(\left(\left(-\left(-e^{\sin(x)}\cos(x)\right)\right)+5\right)-5\right)+\left(2x+1\right)-\left(2x+1\right)\,dx$ |
| **C=20** | $\int e^{\sin(x)}\cos(x)\,dx$ | $\int  \frac{2\left(x-3\right)e^{\sin(x)}\cos(x)}{2\left(x-3\right)}\,dx$ | $\int  \left(\left(e^{\sin(x)}\cos(x)+\left(-x-1\right)\right)-\left(-x-1\right)+\left(-2x+1\right)\right)-\left(-2x+1\right)\,dx$ | $\int  \left(\frac{-\left(1-x\right)e^{\sin(x)}\cos(x)}{-\left(1-x\right)}+\left(3x+2\right)\right)-\left(3x+2\right)+\left(x-2\right)-\left(x-2\right)\,dx$ | $\int  \left(-\left(-\frac{\left(x-2\right)e^{\sin(x)}\cos(x)}{x-2}\right)\right)+\left(-2x\right)-\left(-2x\right)\,dx$ |
| **C=25** | $\int \frac{\sin(x)}{\cos^{3}(x)}\,dx$ | $\int  \frac{\sin(x)}{\cos^{3}(x)}+\left(-x-1\right)-\left(-x-1\right)\,dx$ | $\int  \left(-\left(-\frac{\sin(x)}{\cos^{3}(x)}\right)\right)+\left(2x-1\right)-\left(2x-1\right)\,dx$ | $\int  \left(\left(\frac{\sin(x)}{\cos^{3}(x)}+\left(2x+2\right)-\left(2x+2\right)\right)+\left(-2x-1\right)\right)-\left(-2x-1\right)+6-6\,dx$ | $\int  -\left(-\left(\left(\frac{4\left(x-1\right)\frac{\sin(x)}{\cos^{3}(x)}}{4\left(x-1\right)}+6\right)-6\right)\right)\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $-\frac{1}{\sin(x)}+C$ | $-\frac{1}{\sin(x)}+C$ | $-\frac{1}{\sin(x)}+C$ | $-\frac{1}{\sin(x)}+C$ | $-\frac{1}{\sin(x)}+C$ |
| **C=4** | $e^{2x - 3}+C$ | $e^{2x - 3}+C$ | $e^{2x - 3}+C$ | $e^{2x - 3}+C$ | $e^{2x - 3}+C$ |
| **C=8** | $e^{4x + 5}+C$ | $e^{4x + 5}+C$ | $e^{4x + 5}+C$ | $e^{4x + 5}+C$ | $e^{4x + 5}+C$ |
| **C=12** | $-e^{\cos(x)}+C$ | $-e^{\cos(x)}+C$ | $-e^{\cos(x)}+C$ | $-e^{\cos(x)}+C$ | $-e^{\cos(x)}+C$ |
| **C=16** | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ |
| **C=20** | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ |
| **C=25** | $\frac{1}{2}\sec^{2}(x)+C$ | $\frac{1}{2}\sec^{2}(x)+C$ | $\frac{1}{2}\sec^{2}(x)+C$ | $\frac{1}{2}\sec^{2}(x)+C$ | $\frac{1}{2}\sec^{2}(x)+C$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int \frac{\cos(x)}{\sin^{2}(x)}\,dx$
- Answer: $-\frac{1}{\sin(x)}+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int  \frac{-\left(2-x\right)\frac{\cos(x)}{\sin^{2}(x)}}{-\left(2-x\right)}\,dx$
- Answer: $-\frac{1}{\sin(x)}+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int  \left(-\left(-\frac{\cos(x)}{\sin^{2}(x)}\right)\right)+\left(3x-2\right)-\left(3x-2\right)\,dx$
- Answer: $-\frac{1}{\sin(x)}+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int  \left(\frac{2\left(x-3\right)\frac{\cos(x)}{\sin^{2}(x)}}{2\left(x-3\right)}+3-3\right)+5-5\,dx$
- Answer: $-\frac{1}{\sin(x)}+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int  \left(\left(\left(\left(-\left(-\frac{\cos(x)}{\sin^{2}(x)}\right)\right)+3\right)-3\right)+4\right)-4\,dx$
- Answer: $-\frac{1}{\sin(x)}+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int 2e^{2x - 3}\,dx$
- Answer: $e^{2x - 3}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25 · shortfall=0.5

### C=4 · S=4

- Prompt: $\int  \left(2e^{2x - 3}+\left(3x+2\right)\right)-\left(3x+2\right)\,dx$
- Answer: $e^{2x - 3}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\int  -\left(-\frac{-\left(3+x\right)2e^{2x - 3}}{-\left(3+x\right)}\right)\,dx$
- Answer: $e^{2x - 3}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\int  \left(\left(-\left(-2e^{2x - 3}\right)\right)+\left(2x+2\right)\right)-\left(2x+2\right)+2-2\,dx$
- Answer: $e^{2x - 3}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\int  \frac{-\left(3+x\right)\left(\left(2e^{2x - 3}+2\right)-2\right)}{-\left(3+x\right)}+2-2\,dx$
- Answer: $e^{2x - 3}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\int 4e^{4x + 5}\,dx$
- Answer: $e^{4x + 5}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25 · shortfall=4.5

### C=8 · S=4

- Prompt: $\int  \frac{\left(x-3\right)4e^{4x + 5}}{x-3}\,dx$
- Answer: $e^{4x + 5}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=8 · S=4 · amax=25 · shortfall=3.5

### C=8 · S=8

- Prompt: $\int  \left(4e^{4x + 5}+\left(x-1\right)-\left(x-1\right)\right)+3-3\,dx$
- Answer: $e^{4x + 5}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=8 · amax=25 · shortfall=2.5

### C=8 · S=16

- Prompt: $\int  \left(4e^{4x + 5}+\left(3x+2\right)-\left(3x+2\right)\right)+\left(3x+2\right)-\left(3x+2\right)+6-6\,dx$
- Answer: $e^{4x + 5}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=16 · amax=25 · shortfall=1.5

### C=8 · S=32

- Prompt: $\int  \frac{-\left(2-x\right)\left(-\left(-4e^{4x + 5}\right)\right)}{-\left(2-x\right)}+5-5\,dx$
- Answer: $e^{4x + 5}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=32 · amax=25 · shortfall=1.5

### C=12 · S=0

- Prompt: $\int e^{\cos(x)}\sin(x)\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=0 · amax=25 · shortfall=7

### C=12 · S=4

- Prompt: $\int  \frac{\left(x-2\right)e^{\cos(x)}\sin(x)}{x-2}\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=12 · S=4 · amax=25 · shortfall=6

### C=12 · S=8

- Prompt: $\int  -\left(-\left(e^{\cos(x)}\sin(x)+3-3\right)\right)\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_const`
- Flags: C=12 · S=8 · amax=25 · shortfall=5

### C=12 · S=16

- Prompt: $\int  \left(\left(\left(-\left(-e^{\cos(x)}\sin(x)\right)\right)+1\right)-1\right)+3-3\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `effort:double_neg`
- Flags: C=12 · S=16 · amax=25 · shortfall=4

### C=12 · S=32

- Prompt: $\int  \left(e^{\cos(x)}\sin(x)+\left(2x+3\right)\right)-\left(2x+3\right)+\left(-2x-1\right)-\left(-2x-1\right)+1-1\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_linear`
- Flags: C=12 · S=32 · amax=25 · shortfall=4

### C=16 · S=0

- Prompt: $\int e^{\sin(x)}\cos(x)\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=0 · amax=25 · shortfall=11

### C=16 · S=4

- Prompt: $\int  e^{\sin(x)}\cos(x)+5-5\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=16 · S=4 · amax=25 · shortfall=10

### C=16 · S=8

- Prompt: $\int  \left(-\left(-e^{\sin(x)}\cos(x)\right)\right)+4-4\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `effort:double_neg`
- Flags: C=16 · S=8 · amax=25 · shortfall=9

### C=16 · S=16

- Prompt: $\int  \frac{4\left(x-2\right)\left(\left(e^{\sin(x)}\cos(x)+6-6\right)+\left(3x\right)\right)-\left(3x\right)}{4\left(x-2\right)}\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=16 · amax=25 · shortfall=8

### C=16 · S=32

- Prompt: $\int  \left(\left(\left(-\left(-e^{\sin(x)}\cos(x)\right)\right)+5\right)-5\right)+\left(2x+1\right)-\left(2x+1\right)\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=32 · amax=25 · shortfall=8

### C=20 · S=0

- Prompt: $\int e^{\sin(x)}\cos(x)\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=0 · amax=25 · shortfall=15

### C=20 · S=4

- Prompt: $\int  \frac{2\left(x-3\right)e^{\sin(x)}\cos(x)}{2\left(x-3\right)}\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=20 · S=4 · amax=25 · shortfall=14

### C=20 · S=8

- Prompt: $\int  \left(\left(e^{\sin(x)}\cos(x)+\left(-x-1\right)\right)-\left(-x-1\right)+\left(-2x+1\right)\right)-\left(-2x+1\right)\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_linear` · `effort:add_cancel_linear`
- Flags: C=20 · S=8 · amax=25 · shortfall=13

### C=20 · S=16

- Prompt: $\int  \left(\frac{-\left(1-x\right)e^{\sin(x)}\cos(x)}{-\left(1-x\right)}+\left(3x+2\right)\right)-\left(3x+2\right)+\left(x-2\right)-\left(x-2\right)\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait`
- Flags: C=20 · S=16 · amax=25 · shortfall=12

### C=20 · S=32

- Prompt: $\int  \left(-\left(-\frac{\left(x-2\right)e^{\sin(x)}\cos(x)}{x-2}\right)\right)+\left(-2x\right)-\left(-2x\right)\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=32 · amax=25 · shortfall=12

### C=25 · S=0

- Prompt: $\int \frac{\sin(x)}{\cos^{3}(x)}\,dx$
- Answer: $\frac{1}{2}\sec^{2}(x)+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=21.5

### C=25 · S=4

- Prompt: $\int  \frac{\sin(x)}{\cos^{3}(x)}+\left(-x-1\right)-\left(-x-1\right)\,dx$
- Answer: $\frac{1}{2}\sec^{2}(x)+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=25 · S=4 · amax=25 · shortfall=20.5

### C=25 · S=8

- Prompt: $\int  \left(-\left(-\frac{\sin(x)}{\cos^{3}(x)}\right)\right)+\left(2x-1\right)-\left(2x-1\right)\,dx$
- Answer: $\frac{1}{2}\sec^{2}(x)+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=8 · amax=25 · shortfall=19.5

### C=25 · S=16

- Prompt: $\int  \left(\left(\frac{\sin(x)}{\cos^{3}(x)}+\left(2x+2\right)-\left(2x+2\right)\right)+\left(-2x-1\right)\right)-\left(-2x-1\right)+6-6\,dx$
- Answer: $\frac{1}{2}\sec^{2}(x)+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=16 · amax=25 · shortfall=18.5

### C=25 · S=32

- Prompt: $\int  -\left(-\left(\left(\frac{4\left(x-1\right)\frac{\sin(x)}{\cos^{3}(x)}}{4\left(x-1\right)}+6\right)-6\right)\right)\,dx$
- Answer: $\frac{1}{2}\sec^{2}(x)+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=32 · amax=25 · shortfall=18.5
