# Definite — substitution / change of variables

**type_id:** `calc_def_int_substitution_with_change_of_variables` · **leaf:** `integral_substitution`  
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
| **C=0** | $\int \frac{4}{4x + 2}\,dx$ | $\int  \left(\frac{4}{4x + 2}+4\right)-4\,dx$ | $\int  \left(\left(-\left(-\frac{4}{4x + 2}\right)\right)+2\right)-2\,dx$ | $\int  -\left(-\left(\left(\left(\frac{4}{4x + 2}+5\right)-5\right)+\left(-x+3\right)\right)-\left(-x+3\right)\right)\,dx$ | $\int  \left(\left(-\left(-\left(\frac{4}{4x + 2}+\left(2x+1\right)\right)-\left(2x+1\right)\right)\right)+3\right)-3\,dx$ |
| **C=4** | $\int \frac{2}{2x - 1}\,dx$ | $\int  \frac{3\left(x+1\right)\frac{2}{2x - 1}}{3\left(x+1\right)}\,dx$ | $\int  \left(\left(-\left(-\frac{2}{2x - 1}\right)\right)+6\right)-6\,dx$ | $\int  -\left(-\left(\left(\left(\frac{2}{2x - 1}+5\right)-5\right)+4-4\right)\right)\,dx$ | $\int  \left(\frac{2\left(x-2\right)\frac{2}{2x - 1}}{2\left(x-2\right)}+4-4\right)+1-1\,dx$ |
| **C=8** | $\int e^{\cos(x)}\sin(x)\,dx$ | $\int  \frac{-\left(3+x\right)e^{\cos(x)}\sin(x)}{-\left(3+x\right)}\,dx$ | $\int  \left(e^{\cos(x)}\sin(x)+\left(3x+3\right)-\left(3x+3\right)\right)+\left(-x-2\right)-\left(-x-2\right)\,dx$ | $\int  -\left(-\frac{4\left(x-2\right)\left(\left(e^{\cos(x)}\sin(x)+1\right)-1\right)}{4\left(x-2\right)}\right)\,dx$ | $\int  \frac{2\left(x-2\right)\left(-\left(-e^{\cos(x)}\sin(x)\right)\right)}{2\left(x-2\right)}+\left(x\right)-\left(x\right)\,dx$ |
| **C=12** | $\int \frac{\cos(x)}{\sin^{2}(x)}\,dx$ | $\int  \frac{\cos(x)}{\sin^{2}(x)}+\left(-2x-1\right)-\left(-2x-1\right)\,dx$ | $\int  \left(\frac{-\left(2+x\right)\frac{\cos(x)}{\sin^{2}(x)}}{-\left(2+x\right)}+\left(3x-1\right)\right)-\left(3x-1\right)\,dx$ | $\int  \left(\left(\frac{\cos(x)}{\sin^{2}(x)}+4\right)-4\right)+\left(-x-2\right)-\left(-x-2\right)+6-6\,dx$ | $\int  \left(\left(\left(-\left(-\frac{\cos(x)}{\sin^{2}(x)}\right)\right)+1-1\right)+5\right)-5\,dx$ |
| **C=16** | $\int e^{\sin(x)}\cos(x)\,dx$ | $\int  e^{\sin(x)}\cos(x)+4-4\,dx$ | $\int  \left(\left(-\left(-e^{\sin(x)}\cos(x)\right)\right)+\left(-x+2\right)\right)-\left(-x+2\right)\,dx$ | $\int  \frac{2\left(x+3\right)\left(\left(\left(e^{\sin(x)}\cos(x)+\left(-2x-1\right)-\left(-2x-1\right)\right)+5\right)-5\right)}{2\left(x+3\right)}\,dx$ | $\int  \left(\frac{4\left(x-3\right)\left(-\left(-e^{\sin(x)}\cos(x)\right)\right)}{4\left(x-3\right)}+1\right)-1\,dx$ |
| **C=20** | $\int e^{\sin(x)}\cos(x)\,dx$ | $\int  \frac{\left(x+3\right)e^{\sin(x)}\cos(x)}{x+3}\,dx$ | $\int  \frac{\left(x-1\right)e^{\sin(x)}\cos(x)}{x-1}+\left(2x-2\right)-\left(2x-2\right)\,dx$ | $\int  \left(\left(-\left(-\frac{-\left(2+x\right)e^{\sin(x)}\cos(x)}{-\left(2+x\right)}\right)\right)+\left(x+3\right)\right)-\left(x+3\right)\,dx$ | $\int  \frac{\left(x-1\right)\left(\left(\left(\left(e^{\sin(x)}\cos(x)+3\right)-3\right)+2\right)-2\right)}{x-1}\,dx$ |
| **C=25** | $\int e^{\cos(x)}\sin(x)\,dx$ | $\int  -\left(-e^{\cos(x)}\sin(x)\right)\,dx$ | $\int  \frac{-\left(3+x\right)e^{\cos(x)}\sin(x)}{-\left(3+x\right)}+\left(-2x+1\right)-\left(-2x+1\right)\,dx$ | $\int  \frac{-\left(3+x\right)\left(\left(\left(\left(e^{\cos(x)}\sin(x)+4\right)-4\right)+6\right)-6\right)}{-\left(3+x\right)}\,dx$ | $\int  \left(\left(\frac{\left(x+3\right)e^{\cos(x)}\sin(x)}{x+3}+\left(-2x+1\right)-\left(-2x+1\right)\right)+\left(x-2\right)\right)-\left(x-2\right)\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\ln|4x + 2|+C$ | $\ln|4x + 2|+C$ | $\ln|4x + 2|+C$ | $\ln|4x + 2|+C$ | $\ln|4x + 2|+C$ |
| **C=4** | $\ln|2x - 1|+C$ | $\ln|2x - 1|+C$ | $\ln|2x - 1|+C$ | $\ln|2x - 1|+C$ | $\ln|2x - 1|+C$ |
| **C=8** | $-e^{\cos(x)}+C$ | $-e^{\cos(x)}+C$ | $-e^{\cos(x)}+C$ | $-e^{\cos(x)}+C$ | $-e^{\cos(x)}+C$ |
| **C=12** | $-\frac{1}{\sin(x)}+C$ | $-\frac{1}{\sin(x)}+C$ | $-\frac{1}{\sin(x)}+C$ | $-\frac{1}{\sin(x)}+C$ | $-\frac{1}{\sin(x)}+C$ |
| **C=16** | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ |
| **C=20** | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ | $e^{\sin(x)}+C$ |
| **C=25** | $-e^{\cos(x)}+C$ | $-e^{\cos(x)}+C$ | $-e^{\cos(x)}+C$ | $-e^{\cos(x)}+C$ | $-e^{\cos(x)}+C$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int \frac{4}{4x + 2}\,dx$
- Answer: $\ln|4x + 2|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int  \left(\frac{4}{4x + 2}+4\right)-4\,dx$
- Answer: $\ln|4x + 2|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int  \left(\left(-\left(-\frac{4}{4x + 2}\right)\right)+2\right)-2\,dx$
- Answer: $\ln|4x + 2|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int  -\left(-\left(\left(\left(\frac{4}{4x + 2}+5\right)-5\right)+\left(-x+3\right)\right)-\left(-x+3\right)\right)\,dx$
- Answer: $\ln|4x + 2|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int  \left(\left(-\left(-\left(\frac{4}{4x + 2}+\left(2x+1\right)\right)-\left(2x+1\right)\right)\right)+3\right)-3\,dx$
- Answer: $\ln|4x + 2|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_linear` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int \frac{2}{2x - 1}\,dx$
- Answer: $\ln|2x - 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25 · shortfall=0.5

### C=4 · S=4

- Prompt: $\int  \frac{3\left(x+1\right)\frac{2}{2x - 1}}{3\left(x+1\right)}\,dx$
- Answer: $\ln|2x - 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\int  \left(\left(-\left(-\frac{2}{2x - 1}\right)\right)+6\right)-6\,dx$
- Answer: $\ln|2x - 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\int  -\left(-\left(\left(\left(\frac{2}{2x - 1}+5\right)-5\right)+4-4\right)\right)\,dx$
- Answer: $\ln|2x - 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\int  \left(\frac{2\left(x-2\right)\frac{2}{2x - 1}}{2\left(x-2\right)}+4-4\right)+1-1\,dx$
- Answer: $\ln|2x - 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\int e^{\cos(x)}\sin(x)\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=0 · amax=25 · shortfall=3

### C=8 · S=4

- Prompt: $\int  \frac{-\left(3+x\right)e^{\cos(x)}\sin(x)}{-\left(3+x\right)}\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=8 · S=4 · amax=25 · shortfall=2

### C=8 · S=8

- Prompt: $\int  \left(e^{\cos(x)}\sin(x)+\left(3x+3\right)-\left(3x+3\right)\right)+\left(-x-2\right)-\left(-x-2\right)\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_linear` · `effort:add_cancel_linear`
- Flags: C=8 · S=8 · amax=25 · shortfall=1

### C=8 · S=16

- Prompt: $\int  -\left(-\frac{4\left(x-2\right)\left(\left(e^{\cos(x)}\sin(x)+1\right)-1\right)}{4\left(x-2\right)}\right)\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\int  \frac{2\left(x-2\right)\left(-\left(-e^{\cos(x)}\sin(x)\right)\right)}{2\left(x-2\right)}+\left(x\right)-\left(x\right)\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\int \frac{\cos(x)}{\sin^{2}(x)}\,dx$
- Answer: $-\frac{1}{\sin(x)}+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=8.5

### C=12 · S=4

- Prompt: $\int  \frac{\cos(x)}{\sin^{2}(x)}+\left(-2x-1\right)-\left(-2x-1\right)\,dx$
- Answer: $-\frac{1}{\sin(x)}+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=12 · S=4 · amax=25 · shortfall=7.5

### C=12 · S=8

- Prompt: $\int  \left(\frac{-\left(2+x\right)\frac{\cos(x)}{\sin^{2}(x)}}{-\left(2+x\right)}+\left(3x-1\right)\right)-\left(3x-1\right)\,dx$
- Answer: $-\frac{1}{\sin(x)}+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=8 · amax=25 · shortfall=6.5

### C=12 · S=16

- Prompt: $\int  \left(\left(\frac{\cos(x)}{\sin^{2}(x)}+4\right)-4\right)+\left(-x-2\right)-\left(-x-2\right)+6-6\,dx$
- Answer: $-\frac{1}{\sin(x)}+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=16 · amax=25 · shortfall=5.5

### C=12 · S=32

- Prompt: $\int  \left(\left(\left(-\left(-\frac{\cos(x)}{\sin^{2}(x)}\right)\right)+1-1\right)+5\right)-5\,dx$
- Answer: $-\frac{1}{\sin(x)}+C$
- From: `form:du_over_u_trig` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=32 · amax=25 · shortfall=5.5

### C=16 · S=0

- Prompt: $\int e^{\sin(x)}\cos(x)\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=0 · amax=25 · shortfall=11

### C=16 · S=4

- Prompt: $\int  e^{\sin(x)}\cos(x)+4-4\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=16 · S=4 · amax=25 · shortfall=10

### C=16 · S=8

- Prompt: $\int  \left(\left(-\left(-e^{\sin(x)}\cos(x)\right)\right)+\left(-x+2\right)\right)-\left(-x+2\right)\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `effort:double_neg`
- Flags: C=16 · S=8 · amax=25 · shortfall=9

### C=16 · S=16

- Prompt: $\int  \frac{2\left(x+3\right)\left(\left(\left(e^{\sin(x)}\cos(x)+\left(-2x-1\right)-\left(-2x-1\right)\right)+5\right)-5\right)}{2\left(x+3\right)}\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=16 · amax=25 · shortfall=8

### C=16 · S=32

- Prompt: $\int  \left(\frac{4\left(x-3\right)\left(-\left(-e^{\sin(x)}\cos(x)\right)\right)}{4\left(x-3\right)}+1\right)-1\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=32 · amax=25 · shortfall=8

### C=20 · S=0

- Prompt: $\int e^{\sin(x)}\cos(x)\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=0 · amax=25 · shortfall=15

### C=20 · S=4

- Prompt: $\int  \frac{\left(x+3\right)e^{\sin(x)}\cos(x)}{x+3}\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=20 · S=4 · amax=25 · shortfall=14

### C=20 · S=8

- Prompt: $\int  \frac{\left(x-1\right)e^{\sin(x)}\cos(x)}{x-1}+\left(2x-2\right)-\left(2x-2\right)\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait`
- Flags: C=20 · S=8 · amax=25 · shortfall=13

### C=20 · S=16

- Prompt: $\int  \left(\left(-\left(-\frac{-\left(2+x\right)e^{\sin(x)}\cos(x)}{-\left(2+x\right)}\right)\right)+\left(x+3\right)\right)-\left(x+3\right)\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=16 · amax=25 · shortfall=12

### C=20 · S=32

- Prompt: $\int  \frac{\left(x-1\right)\left(\left(\left(\left(e^{\sin(x)}\cos(x)+3\right)-3\right)+2\right)-2\right)}{x-1}\,dx$
- Answer: $e^{\sin(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_const`
- Flags: C=20 · S=32 · amax=25 · shortfall=12

### C=25 · S=0

- Prompt: $\int e^{\cos(x)}\sin(x)\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=0 · amax=25 · shortfall=20

### C=25 · S=4

- Prompt: $\int  -\left(-e^{\cos(x)}\sin(x)\right)\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=25 · S=4 · amax=25 · shortfall=19

### C=25 · S=8

- Prompt: $\int  \frac{-\left(3+x\right)e^{\cos(x)}\sin(x)}{-\left(3+x\right)}+\left(-2x+1\right)-\left(-2x+1\right)\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait`
- Flags: C=25 · S=8 · amax=25 · shortfall=18

### C=25 · S=16

- Prompt: $\int  \frac{-\left(3+x\right)\left(\left(\left(\left(e^{\cos(x)}\sin(x)+4\right)-4\right)+6\right)-6\right)}{-\left(3+x\right)}\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_const`
- Flags: C=25 · S=16 · amax=25 · shortfall=17

### C=25 · S=32

- Prompt: $\int  \left(\left(\frac{\left(x+3\right)e^{\cos(x)}\sin(x)}{x+3}+\left(-2x+1\right)-\left(-2x+1\right)\right)+\left(x-2\right)\right)-\left(x-2\right)\,dx$
- Answer: $-e^{\cos(x)}+C$
- From: `form:exp_of_trig` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait`
- Flags: C=25 · S=32 · amax=25 · shortfall=17
