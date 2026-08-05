# Integrals — log/exp with substitution

**type_id:** `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` · **leaf:** `integral_substitution`  
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
| **C=0** | $\int 3e^{3x + 6}\,dx$ | $\int  \frac{3\left(x-2\right)3e^{3x + 6}}{3\left(x-2\right)}\,dx$ | $\int  \left(\left(-\left(-3e^{3x + 6}\right)\right)+1\right)-1\,dx$ | $\int  \frac{-\left(1-x\right)\left(\left(\left(3e^{3x + 6}+\left(-x+3\right)-\left(-x+3\right)\right)+5\right)-5\right)}{-\left(1-x\right)}\,dx$ | $\int  -\left(-\frac{4\left(x-1\right)\left(3e^{3x + 6}+3-3\right)}{4\left(x-1\right)}\right)\,dx$ |
| **C=4** | $\int \frac{3}{3x + 1}\,dx$ | $\int  \left(\frac{3}{3x + 1}+5\right)-5\,dx$ | $\int  \left(\left(-\left(-\frac{3}{3x + 1}\right)\right)+6\right)-6\,dx$ | $\int  -\left(-\left(\left(\frac{3}{3x + 1}+2\right)-2\right)+\left(x+1\right)-\left(x+1\right)\right)\,dx$ | $\int  \left(\left(\frac{-\left(2-x\right)\frac{3}{3x + 1}}{-\left(2-x\right)}+4\right)-4\right)+6-6\,dx$ |
| **C=8** | $\int \frac{3}{3x + 6}\,dx$ | $\int  \frac{-\left(1+x\right)\frac{3}{3x + 6}}{-\left(1+x\right)}\,dx$ | $\int  -\left(-\left(\frac{3}{3x + 6}+\left(x-1\right)-\left(x-1\right)\right)\right)\,dx$ | $\int  -\left(-\left(\left(\frac{3}{3x + 6}+\left(-2x+2\right)-\left(-2x+2\right)\right)+\left(-2x\right)\right)-\left(-2x\right)\right)\,dx$ | $\int  \left(\frac{3\left(x-1\right)\frac{3}{3x + 6}}{3\left(x-1\right)}+\left(x+1\right)\right)-\left(x+1\right)+4-4\,dx$ |
| **C=12** | $\int 4e^{4x - 3}\,dx$ | $\int  -\left(-4e^{4x - 3}\right)\,dx$ | $\int  \frac{\left(x-3\right)\left(\left(4e^{4x - 3}+6\right)-6\right)}{x-3}\,dx$ | $\int  \left(4e^{4x - 3}+5-5\right)+\left(2x\right)-\left(2x\right)+\left(-x+3\right)-\left(-x+3\right)\,dx$ | $\int  \frac{3\left(x-2\right)\left(\left(\left(4e^{4x - 3}+2\right)-2\right)+3-3\right)}{3\left(x-2\right)}\,dx$ |
| **C=16** | $\int 2e^{2x + 5}\,dx$ | $\int  \frac{\left(x-3\right)2e^{2x + 5}}{x-3}\,dx$ | $\int  \frac{2\left(x-3\right)\left(2e^{2x + 5}+\left(-x+1\right)\right)-\left(-x+1\right)}{2\left(x-3\right)}\,dx$ | $\int  \left(\left(\frac{4\left(x+2\right)2e^{2x + 5}}{4\left(x+2\right)}+\left(x-2\right)\right)-\left(x-2\right)+\left(-2x-2\right)\right)-\left(-2x-2\right)\,dx$ | $\int  \left(\left(-\left(-\left(2e^{2x + 5}+\left(2x\right)-\left(2x\right)\right)\right)\right)+6\right)-6\,dx$ |
| **C=20** | $\int 3e^{3x - 2}\,dx$ | $\int  3e^{3x - 2}+\left(2x-2\right)-\left(2x-2\right)\,dx$ | $\int  \frac{3\left(x+1\right)3e^{3x - 2}}{3\left(x+1\right)}+3-3\,dx$ | $\int  \left(-\left(-\frac{-\left(3+x\right)3e^{3x - 2}}{-\left(3+x\right)}\right)\right)+6-6\,dx$ | $\int  \left(\left(\frac{-\left(1-x\right)3e^{3x - 2}}{-\left(1-x\right)}+2\right)-2\right)+6-6\,dx$ |
| **C=25** | $\int \frac{2}{2x + 1}\,dx$ | $\int  -\left(-\frac{2}{2x + 1}\right)\,dx$ | $\int  \left(-\left(-\frac{2}{2x + 1}\right)\right)+6-6\,dx$ | $\int  -\left(-\left(\left(\left(\frac{2}{2x + 1}+5\right)-5\right)+\left(3x-2\right)\right)-\left(3x-2\right)\right)\,dx$ | $\int  \left(\frac{-\left(1+x\right)\left(\left(\frac{2}{2x + 1}+2\right)-2\right)}{-\left(1+x\right)}+\left(3x+3\right)\right)-\left(3x+3\right)\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $e^{3x + 6}+C$ | $e^{3x + 6}+C$ | $e^{3x + 6}+C$ | $e^{3x + 6}+C$ | $e^{3x + 6}+C$ |
| **C=4** | $\ln|3x + 1|+C$ | $\ln|3x + 1|+C$ | $\ln|3x + 1|+C$ | $\ln|3x + 1|+C$ | $\ln|3x + 1|+C$ |
| **C=8** | $\ln|3x + 6|+C$ | $\ln|3x + 6|+C$ | $\ln|3x + 6|+C$ | $\ln|3x + 6|+C$ | $\ln|3x + 6|+C$ |
| **C=12** | $e^{4x - 3}+C$ | $e^{4x - 3}+C$ | $e^{4x - 3}+C$ | $e^{4x - 3}+C$ | $e^{4x - 3}+C$ |
| **C=16** | $e^{2x + 5}+C$ | $e^{2x + 5}+C$ | $e^{2x + 5}+C$ | $e^{2x + 5}+C$ | $e^{2x + 5}+C$ |
| **C=20** | $e^{3x - 2}+C$ | $e^{3x - 2}+C$ | $e^{3x - 2}+C$ | $e^{3x - 2}+C$ | $e^{3x - 2}+C$ |
| **C=25** | $\ln|2x + 1|+C$ | $\ln|2x + 1|+C$ | $\ln|2x + 1|+C$ | $\ln|2x + 1|+C$ | $\ln|2x + 1|+C$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int 3e^{3x + 6}\,dx$
- Answer: $e^{3x + 6}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int  \frac{3\left(x-2\right)3e^{3x + 6}}{3\left(x-2\right)}\,dx$
- Answer: $e^{3x + 6}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int  \left(\left(-\left(-3e^{3x + 6}\right)\right)+1\right)-1\,dx$
- Answer: $e^{3x + 6}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int  \frac{-\left(1-x\right)\left(\left(\left(3e^{3x + 6}+\left(-x+3\right)-\left(-x+3\right)\right)+5\right)-5\right)}{-\left(1-x\right)}\,dx$
- Answer: $e^{3x + 6}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int  -\left(-\frac{4\left(x-1\right)\left(3e^{3x + 6}+3-3\right)}{4\left(x-1\right)}\right)\,dx$
- Answer: $e^{3x + 6}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int \frac{3}{3x + 1}\,dx$
- Answer: $\ln|3x + 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25 · shortfall=0.5

### C=4 · S=4

- Prompt: $\int  \left(\frac{3}{3x + 1}+5\right)-5\,dx$
- Answer: $\ln|3x + 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\int  \left(\left(-\left(-\frac{3}{3x + 1}\right)\right)+6\right)-6\,dx$
- Answer: $\ln|3x + 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\int  -\left(-\left(\left(\frac{3}{3x + 1}+2\right)-2\right)+\left(x+1\right)-\left(x+1\right)\right)\,dx$
- Answer: $\ln|3x + 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\int  \left(\left(\frac{-\left(2-x\right)\frac{3}{3x + 1}}{-\left(2-x\right)}+4\right)-4\right)+6-6\,dx$
- Answer: $\ln|3x + 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\int \frac{3}{3x + 6}\,dx$
- Answer: $\ln|3x + 6|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25 · shortfall=4.5

### C=8 · S=4

- Prompt: $\int  \frac{-\left(1+x\right)\frac{3}{3x + 6}}{-\left(1+x\right)}\,dx$
- Answer: $\ln|3x + 6|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=8 · S=4 · amax=25 · shortfall=3.5

### C=8 · S=8

- Prompt: $\int  -\left(-\left(\frac{3}{3x + 6}+\left(x-1\right)-\left(x-1\right)\right)\right)\,dx$
- Answer: $\ln|3x + 6|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=8 · amax=25 · shortfall=2.5

### C=8 · S=16

- Prompt: $\int  -\left(-\left(\left(\frac{3}{3x + 6}+\left(-2x+2\right)-\left(-2x+2\right)\right)+\left(-2x\right)\right)-\left(-2x\right)\right)\,dx$
- Answer: $\ln|3x + 6|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=16 · amax=25 · shortfall=1.5

### C=8 · S=32

- Prompt: $\int  \left(\frac{3\left(x-1\right)\frac{3}{3x + 6}}{3\left(x-1\right)}+\left(x+1\right)\right)-\left(x+1\right)+4-4\,dx$
- Answer: $\ln|3x + 6|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=32 · amax=25 · shortfall=1.5

### C=12 · S=0

- Prompt: $\int 4e^{4x - 3}\,dx$
- Answer: $e^{4x - 3}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=8.5

### C=12 · S=4

- Prompt: $\int  -\left(-4e^{4x - 3}\right)\,dx$
- Answer: $e^{4x - 3}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=12 · S=4 · amax=25 · shortfall=7.5

### C=12 · S=8

- Prompt: $\int  \frac{\left(x-3\right)\left(\left(4e^{4x - 3}+6\right)-6\right)}{x-3}\,dx$
- Answer: $e^{4x - 3}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=8 · amax=25 · shortfall=6.5

### C=12 · S=16

- Prompt: $\int  \left(4e^{4x - 3}+5-5\right)+\left(2x\right)-\left(2x\right)+\left(-x+3\right)-\left(-x+3\right)\,dx$
- Answer: $e^{4x - 3}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=16 · amax=25 · shortfall=5.5

### C=12 · S=32

- Prompt: $\int  \frac{3\left(x-2\right)\left(\left(\left(4e^{4x - 3}+2\right)-2\right)+3-3\right)}{3\left(x-2\right)}\,dx$
- Answer: $e^{4x - 3}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=32 · amax=25 · shortfall=5.5

### C=16 · S=0

- Prompt: $\int 2e^{2x + 5}\,dx$
- Answer: $e^{2x + 5}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=12.5

### C=16 · S=4

- Prompt: $\int  \frac{\left(x-3\right)2e^{2x + 5}}{x-3}\,dx$
- Answer: $e^{2x + 5}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=16 · S=4 · amax=25 · shortfall=11.5

### C=16 · S=8

- Prompt: $\int  \frac{2\left(x-3\right)\left(2e^{2x + 5}+\left(-x+1\right)\right)-\left(-x+1\right)}{2\left(x-3\right)}\,dx$
- Answer: $e^{2x + 5}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=8 · amax=25 · shortfall=10.5

### C=16 · S=16

- Prompt: $\int  \left(\left(\frac{4\left(x+2\right)2e^{2x + 5}}{4\left(x+2\right)}+\left(x-2\right)\right)-\left(x-2\right)+\left(-2x-2\right)\right)-\left(-2x-2\right)\,dx$
- Answer: $e^{2x + 5}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=16 · amax=25 · shortfall=9.5

### C=16 · S=32

- Prompt: $\int  \left(\left(-\left(-\left(2e^{2x + 5}+\left(2x\right)-\left(2x\right)\right)\right)\right)+6\right)-6\,dx$
- Answer: $e^{2x + 5}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:add_cancel_linear` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=32 · amax=25 · shortfall=9.5

### C=20 · S=0

- Prompt: $\int 3e^{3x - 2}\,dx$
- Answer: $e^{3x - 2}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=16.5

### C=20 · S=4

- Prompt: $\int  3e^{3x - 2}+\left(2x-2\right)-\left(2x-2\right)\,dx$
- Answer: $e^{3x - 2}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=20 · S=4 · amax=25 · shortfall=15.5

### C=20 · S=8

- Prompt: $\int  \frac{3\left(x+1\right)3e^{3x - 2}}{3\left(x+1\right)}+3-3\,dx$
- Answer: $e^{3x - 2}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=8 · amax=25 · shortfall=14.5

### C=20 · S=16

- Prompt: $\int  \left(-\left(-\frac{-\left(3+x\right)3e^{3x - 2}}{-\left(3+x\right)}\right)\right)+6-6\,dx$
- Answer: $e^{3x - 2}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=16 · amax=25 · shortfall=13.5

### C=20 · S=32

- Prompt: $\int  \left(\left(\frac{-\left(1-x\right)3e^{3x - 2}}{-\left(1-x\right)}+2\right)-2\right)+6-6\,dx$
- Answer: $e^{3x - 2}+C$
- From: `form:exp_of_poly` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=32 · amax=25 · shortfall=13.5

### C=25 · S=0

- Prompt: $\int \frac{2}{2x + 1}\,dx$
- Answer: $\ln|2x + 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=21.5

### C=25 · S=4

- Prompt: $\int  -\left(-\frac{2}{2x + 1}\right)\,dx$
- Answer: $\ln|2x + 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=25 · S=4 · amax=25 · shortfall=20.5

### C=25 · S=8

- Prompt: $\int  \left(-\left(-\frac{2}{2x + 1}\right)\right)+6-6\,dx$
- Answer: $\ln|2x + 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=8 · amax=25 · shortfall=19.5

### C=25 · S=16

- Prompt: $\int  -\left(-\left(\left(\left(\frac{2}{2x + 1}+5\right)-5\right)+\left(3x-2\right)\right)-\left(3x-2\right)\right)\,dx$
- Answer: $\ln|2x + 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=16 · amax=25 · shortfall=18.5

### C=25 · S=32

- Prompt: $\int  \left(\frac{-\left(1+x\right)\left(\left(\frac{2}{2x + 1}+2\right)-2\right)}{-\left(1+x\right)}+\left(3x+3\right)\right)-\left(3x+3\right)\,dx$
- Answer: $\ln|2x + 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=32 · amax=25 · shortfall=18.5
