# Integrals — invtrig with substitution

**type_id:** `calc_indef_int_inverse_trigonometric_with_substitution` · **leaf:** `integral_substitution`  
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
| **C=0** | $\int 2\left(2x + 4\right)^{3}\,dx$ | $\int  \frac{3\left(x+3\right)\left(2\left(2x + 4\right)^{3}\right)}{3\left(x+3\right)}\,dx$ | $\int  \frac{\left(x+2\right)\left(-\left(-\left(2\left(2x + 4\right)^{3}\right)\right)\right)}{x+2}\,dx$ | $\int  \left(\frac{-\left(1+x\right)\left(2\left(2x + 4\right)^{3}\right)}{-\left(1+x\right)}+\left(-2x\right)-\left(-2x\right)\right)+2-2\,dx$ | $\int  \left(\left(\left(\left(2\left(2x + 4\right)^{3}\right)+2\right)-2\right)+\left(-x+3\right)-\left(-x+3\right)+\left(-x-1\right)\right)-\left(-x-1\right)\,dx$ |
| **C=4** | $\int \frac{2}{2x + 3}\,dx$ | $\int  -\left(-\frac{2}{2x + 3}\right)\,dx$ | $\int  \frac{4\left(x+1\right)\left(\frac{2}{2x + 3}+\left(2x+2\right)\right)-\left(2x+2\right)}{4\left(x+1\right)}\,dx$ | $\int  \left(-\left(-\left(\frac{2}{2x + 3}+5-5\right)\right)\right)+\left(-2x\right)-\left(-2x\right)\,dx$ | $\int  \left(-\left(-\left(\frac{2}{2x + 3}+\left(-2x+3\right)-\left(-2x+3\right)\right)\right)\right)+\left(3x\right)-\left(3x\right)\,dx$ |
| **C=8** | $\int 2\left(2x - 3\right)^{5}\,dx$ | $\int  \frac{\left(x-2\right)\left(2\left(2x - 3\right)^{5}\right)}{x-2}\,dx$ | $\int  \frac{4\left(x+3\right)\left(\left(2\left(2x - 3\right)^{5}\right)+1-1\right)}{4\left(x+3\right)}\,dx$ | $\int  \frac{4\left(x+3\right)\left(\left(2\left(2x - 3\right)^{5}\right)+3-3\right)+\left(2x-1\right)-\left(2x-1\right)}{4\left(x+3\right)}\,dx$ | $\int  \left(\left(2\left(2x - 3\right)^{5}\right)+1-1\right)+\left(-x\right)-\left(-x\right)+5-5\,dx$ |
| **C=12** | $\int \frac{2}{2x + 2}\,dx$ | $\int  \frac{-\left(3-x\right)\frac{2}{2x + 2}}{-\left(3-x\right)}\,dx$ | $\int  \left(-\left(-\frac{2}{2x + 2}\right)\right)+1-1\,dx$ | $\int  \frac{\left(x+1\right)\left(\frac{2}{2x + 2}+\left(2x-1\right)-\left(2x-1\right)\right)+\left(2x+1\right)-\left(2x+1\right)}{x+1}\,dx$ | $\int  \left(\frac{\left(x-1\right)\frac{2}{2x + 2}}{x-1}+3-3\right)+\left(-2x+1\right)-\left(-2x+1\right)\,dx$ |
| **C=16** | $\int 2\left(2x - 5\right)^{5}\,dx$ | $\int  -\left(-\left(2\left(2x - 5\right)^{5}\right)\right)\,dx$ | $\int  \left(\left(2\left(2x - 5\right)^{5}\right)+1-1\right)+\left(3x\right)-\left(3x\right)\,dx$ | $\int  -\left(-\frac{\left(x+1\right)\left(\left(2\left(2x - 5\right)^{5}\right)+\left(2x+1\right)\right)-\left(2x+1\right)}{x+1}\right)\,dx$ | $\int  \frac{2\left(x+3\right)\left(-\left(-\left(2\left(2x - 5\right)^{5}\right)\right)\right)+\left(-2x+2\right)-\left(-2x+2\right)}{2\left(x+3\right)}\,dx$ |
| **C=20** | $\int \frac{3}{3x - 1}\,dx$ | $\int  \frac{3}{3x - 1}+\left(3x+3\right)-\left(3x+3\right)\,dx$ | $\int  \frac{-\left(1+x\right)\left(\frac{3}{3x - 1}+6-6\right)}{-\left(1+x\right)}\,dx$ | $\int  \frac{-\left(3-x\right)\left(-\left(-\left(\left(\frac{3}{3x - 1}+5\right)-5\right)\right)\right)}{-\left(3-x\right)}\,dx$ | $\int  -\left(-\left(\frac{\left(x+2\right)\frac{3}{3x - 1}}{x+2}+\left(x+3\right)-\left(x+3\right)\right)\right)\,dx$ |
| **C=25** | $\int \frac{4}{1+(4x + 8)^{2}}\,dx$ | $\int  \frac{4}{1+(4x + 8)^{2}}+4-4\,dx$ | $\int  -\left(-\left(\frac{4}{1+(4x + 8)^{2}}+\left(x+1\right)-\left(x+1\right)\right)\right)\,dx$ | $\int  \left(\frac{-\left(2+x\right)\frac{4}{1+(4x + 8)^{2}}}{-\left(2+x\right)}+\left(x+2\right)-\left(x+2\right)\right)+6-6\,dx$ | $\int  \frac{\left(x-1\right)\left(\left(\left(\frac{4}{1+(4x + 8)^{2}}+5\right)-5\right)+\left(2x+3\right)\right)-\left(2x+3\right)}{x-1}\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\frac{1}{4}\left(2x + 4\right)^{4}+C$ | $\frac{1}{4}\left(2x + 4\right)^{4}+C$ | $\frac{1}{4}\left(2x + 4\right)^{4}+C$ | $\frac{1}{4}\left(2x + 4\right)^{4}+C$ | $\frac{1}{4}\left(2x + 4\right)^{4}+C$ |
| **C=4** | $\ln|2x + 3|+C$ | $\ln|2x + 3|+C$ | $\ln|2x + 3|+C$ | $\ln|2x + 3|+C$ | $\ln|2x + 3|+C$ |
| **C=8** | $\frac{1}{6}\left(2x - 3\right)^{6}+C$ | $\frac{1}{6}\left(2x - 3\right)^{6}+C$ | $\frac{1}{6}\left(2x - 3\right)^{6}+C$ | $\frac{1}{6}\left(2x - 3\right)^{6}+C$ | $\frac{1}{6}\left(2x - 3\right)^{6}+C$ |
| **C=12** | $\ln|2x + 2|+C$ | $\ln|2x + 2|+C$ | $\ln|2x + 2|+C$ | $\ln|2x + 2|+C$ | $\ln|2x + 2|+C$ |
| **C=16** | $\frac{1}{6}\left(2x - 5\right)^{6}+C$ | $\frac{1}{6}\left(2x - 5\right)^{6}+C$ | $\frac{1}{6}\left(2x - 5\right)^{6}+C$ | $\frac{1}{6}\left(2x - 5\right)^{6}+C$ | $\frac{1}{6}\left(2x - 5\right)^{6}+C$ |
| **C=20** | $\ln|3x - 1|+C$ | $\ln|3x - 1|+C$ | $\ln|3x - 1|+C$ | $\ln|3x - 1|+C$ | $\ln|3x - 1|+C$ |
| **C=25** | $\arctan(4x + 8)+C$ | $\arctan(4x + 8)+C$ | $\arctan(4x + 8)+C$ | $\arctan(4x + 8)+C$ | $\arctan(4x + 8)+C$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int 2\left(2x + 4\right)^{3}\,dx$
- Answer: $\frac{1}{4}\left(2x + 4\right)^{4}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int  \frac{3\left(x+3\right)\left(2\left(2x + 4\right)^{3}\right)}{3\left(x+3\right)}\,dx$
- Answer: $\frac{1}{4}\left(2x + 4\right)^{4}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int  \frac{\left(x+2\right)\left(-\left(-\left(2\left(2x + 4\right)^{3}\right)\right)\right)}{x+2}\,dx$
- Answer: $\frac{1}{4}\left(2x + 4\right)^{4}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int  \left(\frac{-\left(1+x\right)\left(2\left(2x + 4\right)^{3}\right)}{-\left(1+x\right)}+\left(-2x\right)-\left(-2x\right)\right)+2-2\,dx$
- Answer: $\frac{1}{4}\left(2x + 4\right)^{4}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int  \left(\left(\left(\left(2\left(2x + 4\right)^{3}\right)+2\right)-2\right)+\left(-x+3\right)-\left(-x+3\right)+\left(-x-1\right)\right)-\left(-x-1\right)\,dx$
- Answer: $\frac{1}{4}\left(2x + 4\right)^{4}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int \frac{2}{2x + 3}\,dx$
- Answer: $\ln|2x + 3|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25 · shortfall=0.5

### C=4 · S=4

- Prompt: $\int  -\left(-\frac{2}{2x + 3}\right)\,dx$
- Answer: $\ln|2x + 3|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\int  \frac{4\left(x+1\right)\left(\frac{2}{2x + 3}+\left(2x+2\right)\right)-\left(2x+2\right)}{4\left(x+1\right)}\,dx$
- Answer: $\ln|2x + 3|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\int  \left(-\left(-\left(\frac{2}{2x + 3}+5-5\right)\right)\right)+\left(-2x\right)-\left(-2x\right)\,dx$
- Answer: $\ln|2x + 3|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\int  \left(-\left(-\left(\frac{2}{2x + 3}+\left(-2x+3\right)-\left(-2x+3\right)\right)\right)\right)+\left(3x\right)-\left(3x\right)\,dx$
- Answer: $\ln|2x + 3|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\int 2\left(2x - 3\right)^{5}\,dx$
- Answer: $\frac{1}{6}\left(2x - 3\right)^{6}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25 · shortfall=7

### C=8 · S=4

- Prompt: $\int  \frac{\left(x-2\right)\left(2\left(2x - 3\right)^{5}\right)}{x-2}\,dx$
- Answer: $\frac{1}{6}\left(2x - 3\right)^{6}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=8 · S=4 · amax=25 · shortfall=6

### C=8 · S=8

- Prompt: $\int  \frac{4\left(x+3\right)\left(\left(2\left(2x - 3\right)^{5}\right)+1-1\right)}{4\left(x+3\right)}\,dx$
- Answer: $\frac{1}{6}\left(2x - 3\right)^{6}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=8 · S=8 · amax=25 · shortfall=5

### C=8 · S=16

- Prompt: $\int  \frac{4\left(x+3\right)\left(\left(2\left(2x - 3\right)^{5}\right)+3-3\right)+\left(2x-1\right)-\left(2x-1\right)}{4\left(x+3\right)}\,dx$
- Answer: $\frac{1}{6}\left(2x - 3\right)^{6}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=16 · amax=25 · shortfall=4

### C=8 · S=32

- Prompt: $\int  \left(\left(2\left(2x - 3\right)^{5}\right)+1-1\right)+\left(-x\right)-\left(-x\right)+5-5\,dx$
- Answer: $\frac{1}{6}\left(2x - 3\right)^{6}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=8 · S=32 · amax=25 · shortfall=4

### C=12 · S=0

- Prompt: $\int \frac{2}{2x + 2}\,dx$
- Answer: $\ln|2x + 2|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=8.5

### C=12 · S=4

- Prompt: $\int  \frac{-\left(3-x\right)\frac{2}{2x + 2}}{-\left(3-x\right)}\,dx$
- Answer: $\ln|2x + 2|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=12 · S=4 · amax=25 · shortfall=7.5

### C=12 · S=8

- Prompt: $\int  \left(-\left(-\frac{2}{2x + 2}\right)\right)+1-1\,dx$
- Answer: $\ln|2x + 2|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=12 · S=8 · amax=25 · shortfall=6.5

### C=12 · S=16

- Prompt: $\int  \frac{\left(x+1\right)\left(\frac{2}{2x + 2}+\left(2x-1\right)-\left(2x-1\right)\right)+\left(2x+1\right)-\left(2x+1\right)}{x+1}\,dx$
- Answer: $\ln|2x + 2|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=12 · S=16 · amax=25 · shortfall=5.5

### C=12 · S=32

- Prompt: $\int  \left(\frac{\left(x-1\right)\frac{2}{2x + 2}}{x-1}+3-3\right)+\left(-2x+1\right)-\left(-2x+1\right)\,dx$
- Answer: $\ln|2x + 2|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=32 · amax=25 · shortfall=5.5

### C=16 · S=0

- Prompt: $\int 2\left(2x - 5\right)^{5}\,dx$
- Answer: $\frac{1}{6}\left(2x - 5\right)^{6}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=15

### C=16 · S=4

- Prompt: $\int  -\left(-\left(2\left(2x - 5\right)^{5}\right)\right)\,dx$
- Answer: $\frac{1}{6}\left(2x - 5\right)^{6}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=16 · S=4 · amax=25 · shortfall=14

### C=16 · S=8

- Prompt: $\int  \left(\left(2\left(2x - 5\right)^{5}\right)+1-1\right)+\left(3x\right)-\left(3x\right)\,dx$
- Answer: $\frac{1}{6}\left(2x - 5\right)^{6}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=16 · S=8 · amax=25 · shortfall=13

### C=16 · S=16

- Prompt: $\int  -\left(-\frac{\left(x+1\right)\left(\left(2\left(2x - 5\right)^{5}\right)+\left(2x+1\right)\right)-\left(2x+1\right)}{x+1}\right)\,dx$
- Answer: $\frac{1}{6}\left(2x - 5\right)^{6}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=16 · amax=25 · shortfall=12

### C=16 · S=32

- Prompt: $\int  \frac{2\left(x+3\right)\left(-\left(-\left(2\left(2x - 5\right)^{5}\right)\right)\right)+\left(-2x+2\right)-\left(-2x+2\right)}{2\left(x+3\right)}\,dx$
- Answer: $\frac{1}{6}\left(2x - 5\right)^{6}+C$
- From: `form:power_linear_du` · `conceptual:u_sub` · `effort:double_neg` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=32 · amax=25 · shortfall=12

### C=20 · S=0

- Prompt: $\int \frac{3}{3x - 1}\,dx$
- Answer: $\ln|3x - 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=16.5

### C=20 · S=4

- Prompt: $\int  \frac{3}{3x - 1}+\left(3x+3\right)-\left(3x+3\right)\,dx$
- Answer: $\ln|3x - 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=4 · amax=25 · shortfall=15.5

### C=20 · S=8

- Prompt: $\int  \frac{-\left(1+x\right)\left(\frac{3}{3x - 1}+6-6\right)}{-\left(1+x\right)}\,dx$
- Answer: $\ln|3x - 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=20 · S=8 · amax=25 · shortfall=14.5

### C=20 · S=16

- Prompt: $\int  \frac{-\left(3-x\right)\left(-\left(-\left(\left(\frac{3}{3x - 1}+5\right)-5\right)\right)\right)}{-\left(3-x\right)}\,dx$
- Answer: $\ln|3x - 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=16 · amax=25 · shortfall=13.5

### C=20 · S=32

- Prompt: $\int  -\left(-\left(\frac{\left(x+2\right)\frac{3}{3x - 1}}{x+2}+\left(x+3\right)-\left(x+3\right)\right)\right)\,dx$
- Answer: $\ln|3x - 1|+C$
- From: `form:du_over_u_linear` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=32 · amax=25 · shortfall=13.5

### C=25 · S=0

- Prompt: $\int \frac{4}{1+(4x + 8)^{2}}\,dx$
- Answer: $\arctan(4x + 8)+C$
- From: `form:arctan_of_linear` · `conceptual:u_sub` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=21

### C=25 · S=4

- Prompt: $\int  \frac{4}{1+(4x + 8)^{2}}+4-4\,dx$
- Answer: $\arctan(4x + 8)+C$
- From: `form:arctan_of_linear` · `conceptual:u_sub` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=25 · S=4 · amax=25 · shortfall=20

### C=25 · S=8

- Prompt: $\int  -\left(-\left(\frac{4}{1+(4x + 8)^{2}}+\left(x+1\right)-\left(x+1\right)\right)\right)\,dx$
- Answer: $\arctan(4x + 8)+C$
- From: `form:arctan_of_linear` · `conceptual:u_sub` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=25 · S=8 · amax=25 · shortfall=19

### C=25 · S=16

- Prompt: $\int  \left(\frac{-\left(2+x\right)\frac{4}{1+(4x + 8)^{2}}}{-\left(2+x\right)}+\left(x+2\right)-\left(x+2\right)\right)+6-6\,dx$
- Answer: $\arctan(4x + 8)+C$
- From: `form:arctan_of_linear` · `conceptual:u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=16 · amax=25 · shortfall=18

### C=25 · S=32

- Prompt: $\int  \frac{\left(x-1\right)\left(\left(\left(\frac{4}{1+(4x + 8)^{2}}+5\right)-5\right)+\left(2x+3\right)\right)-\left(2x+3\right)}{x-1}\,dx$
- Answer: $\arctan(4x + 8)+C$
- From: `form:arctan_of_linear` · `conceptual:u_sub` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=32 · amax=25 · shortfall=18
