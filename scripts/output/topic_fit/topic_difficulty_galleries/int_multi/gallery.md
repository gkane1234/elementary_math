# Integrals — multi-trick

**type_id:** `calc_indef_int_multi_trick` · **leaf:** `integration_by_parts`  
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
| **C=0** | $\int \frac{2\left(e^{4x}\right)+2}{\left(e^{4x}-1\right)\left(e^{4x}+3\right)}\cdot 4e^{4x}\,dx$ | $\int  \left(\frac{2\left(e^{4x}\right)+2}{\left(e^{4x}-1\right)\left(e^{4x}+3\right)}\cdot 4e^{4x}+\left(3x+1\right)\right)-\left(3x+1\right)\,dx$ | $\int  -\left(-\left(\frac{2\left(e^{4x}\right)+2}{\left(e^{4x}-1\right)\left(e^{4x}+3\right)}\cdot 4e^{4x}+1-1\right)\right)\,dx$ | $\int  \ln\left(e^{\left(\left(\left(\left(\frac{2\left(e^{4x}\right)+2}{\left(e^{4x}-1\right)\left(e^{4x}+3\right)}\cdot 4e^{4x}+3\right)-3\right)+6\right)-6\right)}\right)\,dx$ | $\int  e^{\ln\left(\left(-\left(-\left(\left(\frac{2\left(e^{4x}\right)+2}{\left(e^{4x}-1\right)\left(e^{4x}+3\right)}\cdot 4e^{4x}+5\right)-5\right)\right)\right)\right)}\,dx$ |
| **C=4** | $\int \frac{3\left(e^{2x}\right)-6}{\left(e^{2x}-3\right)\left(e^{2x}\right)}\cdot 2e^{2x}\,dx$ | $\int  \ln\left(e^{\frac{3\left(e^{2x}\right)-6}{\left(e^{2x}-3\right)\left(e^{2x}\right)}\cdot 2e^{2x}}\right)\,dx$ | $\int  \left(\ln\left(e^{\frac{3\left(e^{2x}\right)-6}{\left(e^{2x}-3\right)\left(e^{2x}\right)}\cdot 2e^{2x}}\right)+\left(x-2\right)\right)-\left(x-2\right)\,dx$ | $\int  \frac{\left(x-3\right)\left(\frac{3\left(e^{2x}\right)-6}{\left(e^{2x}-3\right)\left(e^{2x}\right)}\cdot 2e^{2x}+\left(3x-2\right)\right)-\left(3x-2\right)}{x-3}+6-6\,dx$ | $\int  \left(-\left(-\frac{3\left(x-2\right)\frac{3\left(e^{2x}\right)-6}{\left(e^{2x}-3\right)\left(e^{2x}\right)}\cdot 2e^{2x}}{3\left(x-2\right)}\right)\right)+\left(3x\right)-\left(3x\right)\,dx$ |
| **C=8** | $\int \frac{4\left(\sin(4x)\right)}{\left(\sin(4x)\right)^{2}+9}\cdot 4\cos(4x)\,dx$ | $\int  \frac{-\left(2-x\right)\frac{4\left(\sin(4x)\right)}{\left(\sin(4x)\right)^{2}+9}\cdot 4\cos(4x)}{-\left(2-x\right)}\,dx$ | $\int  \left(\frac{-\left(1-x\right)\frac{4\left(\sin(4x)\right)}{\left(\sin(4x)\right)^{2}+9}\cdot 4\cos(4x)}{-\left(1-x\right)}+\left(x-2\right)\right)-\left(x-2\right)\,dx$ | $\int  -\left(-\frac{3\left(x+3\right)\left(\left(\frac{4\left(\sin(4x)\right)}{\left(\sin(4x)\right)^{2}+9}\cdot 4\cos(4x)+6\right)-6\right)}{3\left(x+3\right)}\right)\,dx$ | $\int  \frac{4\left(x-3\right)\left(\left(\left(\frac{4\left(\sin(4x)\right)}{\left(\sin(4x)\right)^{2}+9}\cdot 4\cos(4x)+3-3\right)+4\right)-4\right)}{4\left(x-3\right)}\,dx$ |
| **C=12** | $\int \frac{-4\left(\sin(x)\right)+2}{\left(\sin(x)\right)^{2}+1}\cdot \cos(x)\,dx$ | $\int  -\left(-\frac{-4\left(\sin(x)\right)+2}{\left(\sin(x)\right)^{2}+1}\cdot \cos(x)\right)\,dx$ | $\int  \left(\left(-\left(-\frac{-4\left(\sin(x)\right)+2}{\left(\sin(x)\right)^{2}+1}\cdot \cos(x)\right)\right)+3\right)-3\,dx$ | $\int  \left(\frac{\left(x-2\right)\left(\frac{-4\left(\sin(x)\right)+2}{\left(\sin(x)\right)^{2}+1}\cdot \cos(x)+\left(3x+2\right)\right)-\left(3x+2\right)}{x-2}+\left(-x-2\right)\right)-\left(-x-2\right)\,dx$ | $\int  \left(\left(\left(\frac{\left(x+1\right)\frac{-4\left(\sin(x)\right)+2}{\left(\sin(x)\right)^{2}+1}\cdot \cos(x)}{x+1}+4\right)-4\right)+\left(x-1\right)\right)-\left(x-1\right)\,dx$ |
| **C=16** | $\int \frac{-1}{\left(e^{2x}\right)^{2}+16}\cdot 2e^{2x}\,dx$ | $\int  -\left(-\frac{-1}{\left(e^{2x}\right)^{2}+16}\cdot 2e^{2x}\right)\,dx$ | $\int  \left(\left(-\left(-\frac{-1}{\left(e^{2x}\right)^{2}+16}\cdot 2e^{2x}\right)\right)+6\right)-6\,dx$ | $\int  \left(\left(\left(\left(\left(\frac{-1}{\left(e^{2x}\right)^{2}+16}\cdot 2e^{2x}+6\right)-6\right)+4\right)-4\right)+\left(-x-2\right)\right)-\left(-x-2\right)\,dx$ | $\int  \frac{4\left(x-2\right)\left(\ln\left(e^{\frac{-1}{\left(e^{2x}\right)^{2}+16}\cdot 2e^{2x}}\right)+5-5\right)}{4\left(x-2\right)}\,dx$ |
| **C=20** | $\int \frac{7\left(\ln|x + 6|\right)-1}{\left(\ln|x + 6|\right)^{2}+1}\frac{1}{x + 6}\,dx$ | $\int  \left(\frac{7\left(\ln|x + 6|\right)-1}{\left(\ln|x + 6|\right)^{2}+1}\frac{1}{x + 6}+\left(-2x-2\right)\right)-\left(-2x-2\right)\,dx$ | $\int  \frac{-\left(2+x\right)\frac{7\left(\ln|x + 6|\right)-1}{\left(\ln|x + 6|\right)^{2}+1}\frac{1}{x + 6}}{-\left(2+x\right)}+\left(3x+3\right)-\left(3x+3\right)\,dx$ | $\int  \left(\left(-\left(-\left(\left(\frac{7\left(\ln|x + 6|\right)-1}{\left(\ln|x + 6|\right)^{2}+1}\frac{1}{x + 6}+4\right)-4\right)\right)\right)+\left(3x+1\right)\right)-\left(3x+1\right)\,dx$ | $\int  \left(\left(\frac{7\left(\ln|x + 6|\right)-1}{\left(\ln|x + 6|\right)^{2}+1}\frac{1}{x + 6}+\left(3x+1\right)\right)-\left(3x+1\right)+\left(3x+1\right)-\left(3x+1\right)+\left(-x+1\right)\right)-\left(-x+1\right)\,dx$ |
| **C=25** | $\int \frac{-3}{\left(\ln|3x|\right)^{2}+16}\frac{3}{3x}\,dx$ | $\int  \frac{-\left(3+x\right)\frac{-3}{\left(\ln|3x|\right)^{2}+16}\frac{3}{3x}}{-\left(3+x\right)}\,dx$ | $\int  \left(\left(\frac{-3}{\left(\ln|3x|\right)^{2}+16}\frac{3}{3x}+\left(-2x-1\right)-\left(-2x-1\right)\right)+\left(3x-2\right)\right)-\left(3x-2\right)\,dx$ | $\int  \left(\left(-\left(-\frac{\left(x+2\right)\frac{-3}{\left(\ln|3x|\right)^{2}+16}\frac{3}{3x}}{x+2}\right)\right)+6\right)-6\,dx$ | $\int  \left(\left(-\left(-\left(\frac{-3}{\left(\ln|3x|\right)^{2}+16}\frac{3}{3x}+3-3\right)\right)\right)+5\right)-5\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\ln|\left(e^{4x}-1\right)|+\ln|\left(e^{4x}+3\right)|+C$ | $\ln|\left(e^{4x}-1\right)|+\ln|\left(e^{4x}+3\right)|+C$ | $\ln|\left(e^{4x}-1\right)|+\ln|\left(e^{4x}+3\right)|+C$ | $\ln|\left(e^{4x}-1\right)|+\ln|\left(e^{4x}+3\right)|+C$ | $\ln|\left(e^{4x}-1\right)|+\ln|\left(e^{4x}+3\right)|+C$ |
| **C=4** | $\ln|\left(e^{2x}-3\right)|+2\ln|\left(e^{2x}\right)|+C$ | $\ln|\left(e^{2x}-3\right)|+2\ln|\left(e^{2x}\right)|+C$ | $\ln|\left(e^{2x}-3\right)|+2\ln|\left(e^{2x}\right)|+C$ | $\ln|\left(e^{2x}-3\right)|+2\ln|\left(e^{2x}\right)|+C$ | $\ln|\left(e^{2x}-3\right)|+2\ln|\left(e^{2x}\right)|+C$ |
| **C=8** | $\ln|\sin(4x) + 4|+2\ln|\sin(4x)^{2}+9|+C$ | $\ln|\sin(4x) + 4|+2\ln|\sin(4x)^{2}+9|+C$ | $\ln|\sin(4x) + 4|+2\ln|\sin(4x)^{2}+9|+C$ | $\ln|\sin(4x) + 4|+2\ln|\sin(4x)^{2}+9|+C$ | $\ln|\sin(4x) + 4|+2\ln|\sin(4x)^{2}+9|+C$ |
| **C=12** | $4\ln|\sin(x) - 1|-2\ln|\sin(x)^{2}+1|+2\arctan(\sin(x))+C$ | $4\ln|\sin(x) - 1|-2\ln|\sin(x)^{2}+1|+2\arctan(\sin(x))+C$ | $4\ln|\sin(x) - 1|-2\ln|\sin(x)^{2}+1|+2\arctan(\sin(x))+C$ | $4\ln|\sin(x) - 1|-2\ln|\sin(x)^{2}+1|+2\arctan(\sin(x))+C$ | $4\ln|\sin(x) - 1|-2\ln|\sin(x)^{2}+1|+2\arctan(\sin(x))+C$ |
| **C=16** | $3\ln|e^{2x}|-\frac{1}{4}\arctan(\frac{e^{2x}}{4})+C$ | $3\ln|e^{2x}|-\frac{1}{4}\arctan(\frac{e^{2x}}{4})+C$ | $3\ln|e^{2x}|-\frac{1}{4}\arctan(\frac{e^{2x}}{4})+C$ | $3\ln|e^{2x}|-\frac{1}{4}\arctan(\frac{e^{2x}}{4})+C$ | $3\ln|e^{2x}|-\frac{1}{4}\arctan(\frac{e^{2x}}{4})+C$ |
| **C=20** | $2\ln|\ln|x + 6| - 1|+\frac{7}{2}\ln|\ln|x + 6|^{2}+1|-\arctan(\ln|x + 6|)+C$ | $2\ln|\ln|x + 6| - 1|+\frac{7}{2}\ln|\ln|x + 6|^{2}+1|-\arctan(\ln|x + 6|)+C$ | $2\ln|\ln|x + 6| - 1|+\frac{7}{2}\ln|\ln|x + 6|^{2}+1|-\arctan(\ln|x + 6|)+C$ | $2\ln|\ln|x + 6| - 1|+\frac{7}{2}\ln|\ln|x + 6|^{2}+1|-\arctan(\ln|x + 6|)+C$ | $2\ln|\ln|x + 6| - 1|+\frac{7}{2}\ln|\ln|x + 6|^{2}+1|-\arctan(\ln|x + 6|)+C$ |
| **C=25** | $-4\ln|\ln|3x| - 2|-\frac{3}{4}\arctan(\frac{\ln|3x|}{4})+C$ | $-4\ln|\ln|3x| - 2|-\frac{3}{4}\arctan(\frac{\ln|3x|}{4})+C$ | $-4\ln|\ln|3x| - 2|-\frac{3}{4}\arctan(\frac{\ln|3x|}{4})+C$ | $-4\ln|\ln|3x| - 2|-\frac{3}{4}\arctan(\frac{\ln|3x|}{4})+C$ | $-4\ln|\ln|3x| - 2|-\frac{3}{4}\arctan(\frac{\ln|3x|}{4})+C$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int \frac{2\left(e^{4x}\right)+2}{\left(e^{4x}-1\right)\left(e^{4x}+3\right)}\cdot 4e^{4x}\,dx$
- Answer: $\ln|\left(e^{4x}-1\right)|+\ln|\left(e^{4x}+3\right)|+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int  \left(\frac{2\left(e^{4x}\right)+2}{\left(e^{4x}-1\right)\left(e^{4x}+3\right)}\cdot 4e^{4x}+\left(3x+1\right)\right)-\left(3x+1\right)\,dx$
- Answer: $\ln|\left(e^{4x}-1\right)|+\ln|\left(e^{4x}+3\right)|+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int  -\left(-\left(\frac{2\left(e^{4x}\right)+2}{\left(e^{4x}-1\right)\left(e^{4x}+3\right)}\cdot 4e^{4x}+1-1\right)\right)\,dx$
- Answer: $\ln|\left(e^{4x}-1\right)|+\ln|\left(e^{4x}+3\right)|+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int  \ln\left(e^{\left(\left(\left(\left(\frac{2\left(e^{4x}\right)+2}{\left(e^{4x}-1\right)\left(e^{4x}+3\right)}\cdot 4e^{4x}+3\right)-3\right)+6\right)-6\right)}\right)\,dx$
- Answer: $\ln|\left(e^{4x}-1\right)|+\ln|\left(e^{4x}+3\right)|+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int  e^{\ln\left(\left(-\left(-\left(\left(\frac{2\left(e^{4x}\right)+2}{\left(e^{4x}-1\right)\left(e^{4x}+3\right)}\cdot 4e^{4x}+5\right)-5\right)\right)\right)\right)}\,dx$
- Answer: $\ln|\left(e^{4x}-1\right)|+\ln|\left(e^{4x}+3\right)|+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int \frac{3\left(e^{2x}\right)-6}{\left(e^{2x}-3\right)\left(e^{2x}\right)}\cdot 2e^{2x}\,dx$
- Answer: $\ln|\left(e^{2x}-3\right)|+2\ln|\left(e^{2x}\right)|+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\int  \ln\left(e^{\frac{3\left(e^{2x}\right)-6}{\left(e^{2x}-3\right)\left(e^{2x}\right)}\cdot 2e^{2x}}\right)\,dx$
- Answer: $\ln|\left(e^{2x}-3\right)|+2\ln|\left(e^{2x}\right)|+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:ln_exp_id` · `effort:spec_answer_preserved`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\int  \left(\ln\left(e^{\frac{3\left(e^{2x}\right)-6}{\left(e^{2x}-3\right)\left(e^{2x}\right)}\cdot 2e^{2x}}\right)+\left(x-2\right)\right)-\left(x-2\right)\,dx$
- Answer: $\ln|\left(e^{2x}-3\right)|+2\ln|\left(e^{2x}\right)|+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:ln_exp_id`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\int  \frac{\left(x-3\right)\left(\frac{3\left(e^{2x}\right)-6}{\left(e^{2x}-3\right)\left(e^{2x}\right)}\cdot 2e^{2x}+\left(3x-2\right)\right)-\left(3x-2\right)}{x-3}+6-6\,dx$
- Answer: $\ln|\left(e^{2x}-3\right)|+2\ln|\left(e^{2x}\right)|+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\int  \left(-\left(-\frac{3\left(x-2\right)\frac{3\left(e^{2x}\right)-6}{\left(e^{2x}-3\right)\left(e^{2x}\right)}\cdot 2e^{2x}}{3\left(x-2\right)}\right)\right)+\left(3x\right)-\left(3x\right)\,dx$
- Answer: $\ln|\left(e^{2x}-3\right)|+2\ln|\left(e^{2x}\right)|+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\int \frac{4\left(\sin(4x)\right)}{\left(\sin(4x)\right)^{2}+9}\cdot 4\cos(4x)\,dx$
- Answer: $\ln|\sin(4x) + 4|+2\ln|\sin(4x)^{2}+9|+C$
- From: `form:u_sub_then_pfd_trig` · `conceptual:u_sub+pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25

### C=8 · S=4

- Prompt: $\int  \frac{-\left(2-x\right)\frac{4\left(\sin(4x)\right)}{\left(\sin(4x)\right)^{2}+9}\cdot 4\cos(4x)}{-\left(2-x\right)}\,dx$
- Answer: $\ln|\sin(4x) + 4|+2\ln|\sin(4x)^{2}+9|+C$
- From: `form:u_sub_then_pfd_trig` · `conceptual:u_sub+pfd` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\int  \left(\frac{-\left(1-x\right)\frac{4\left(\sin(4x)\right)}{\left(\sin(4x)\right)^{2}+9}\cdot 4\cos(4x)}{-\left(1-x\right)}+\left(x-2\right)\right)-\left(x-2\right)\,dx$
- Answer: $\ln|\sin(4x) + 4|+2\ln|\sin(4x)^{2}+9|+C$
- From: `form:u_sub_then_pfd_trig` · `conceptual:u_sub+pfd` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\int  -\left(-\frac{3\left(x+3\right)\left(\left(\frac{4\left(\sin(4x)\right)}{\left(\sin(4x)\right)^{2}+9}\cdot 4\cos(4x)+6\right)-6\right)}{3\left(x+3\right)}\right)\,dx$
- Answer: $\ln|\sin(4x) + 4|+2\ln|\sin(4x)^{2}+9|+C$
- From: `form:u_sub_then_pfd_trig` · `conceptual:u_sub+pfd` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\int  \frac{4\left(x-3\right)\left(\left(\left(\frac{4\left(\sin(4x)\right)}{\left(\sin(4x)\right)^{2}+9}\cdot 4\cos(4x)+3-3\right)+4\right)-4\right)}{4\left(x-3\right)}\,dx$
- Answer: $\ln|\sin(4x) + 4|+2\ln|\sin(4x)^{2}+9|+C$
- From: `form:u_sub_then_pfd_trig` · `conceptual:u_sub+pfd` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\int \frac{-4\left(\sin(x)\right)+2}{\left(\sin(x)\right)^{2}+1}\cdot \cos(x)\,dx$
- Answer: $4\ln|\sin(x) - 1|-2\ln|\sin(x)^{2}+1|+2\arctan(\sin(x))+C$
- From: `form:u_sub_then_pfd_trig` · `conceptual:u_sub+pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25

### C=12 · S=4

- Prompt: $\int  -\left(-\frac{-4\left(\sin(x)\right)+2}{\left(\sin(x)\right)^{2}+1}\cdot \cos(x)\right)\,dx$
- Answer: $4\ln|\sin(x) - 1|-2\ln|\sin(x)^{2}+1|+2\arctan(\sin(x))+C$
- From: `form:u_sub_then_pfd_trig` · `conceptual:u_sub+pfd` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=12 · S=4 · amax=25

### C=12 · S=8

- Prompt: $\int  \left(\left(-\left(-\frac{-4\left(\sin(x)\right)+2}{\left(\sin(x)\right)^{2}+1}\cdot \cos(x)\right)\right)+3\right)-3\,dx$
- Answer: $4\ln|\sin(x) - 1|-2\ln|\sin(x)^{2}+1|+2\arctan(\sin(x))+C$
- From: `form:u_sub_then_pfd_trig` · `conceptual:u_sub+pfd` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=8 · amax=25

### C=12 · S=16

- Prompt: $\int  \left(\frac{\left(x-2\right)\left(\frac{-4\left(\sin(x)\right)+2}{\left(\sin(x)\right)^{2}+1}\cdot \cos(x)+\left(3x+2\right)\right)-\left(3x+2\right)}{x-2}+\left(-x-2\right)\right)-\left(-x-2\right)\,dx$
- Answer: $4\ln|\sin(x) - 1|-2\ln|\sin(x)^{2}+1|+2\arctan(\sin(x))+C$
- From: `form:u_sub_then_pfd_trig` · `conceptual:u_sub+pfd` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=16 · amax=25

### C=12 · S=32

- Prompt: $\int  \left(\left(\left(\frac{\left(x+1\right)\frac{-4\left(\sin(x)\right)+2}{\left(\sin(x)\right)^{2}+1}\cdot \cos(x)}{x+1}+4\right)-4\right)+\left(x-1\right)\right)-\left(x-1\right)\,dx$
- Answer: $4\ln|\sin(x) - 1|-2\ln|\sin(x)^{2}+1|+2\arctan(\sin(x))+C$
- From: `form:u_sub_then_pfd_trig` · `conceptual:u_sub+pfd` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=32 · amax=25

### C=16 · S=0

- Prompt: $\int \frac{-1}{\left(e^{2x}\right)^{2}+16}\cdot 2e^{2x}\,dx$
- Answer: $3\ln|e^{2x}|-\frac{1}{4}\arctan(\frac{e^{2x}}{4})+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=4

### C=16 · S=4

- Prompt: $\int  -\left(-\frac{-1}{\left(e^{2x}\right)^{2}+16}\cdot 2e^{2x}\right)\,dx$
- Answer: $3\ln|e^{2x}|-\frac{1}{4}\arctan(\frac{e^{2x}}{4})+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=16 · S=4 · amax=25 · shortfall=3

### C=16 · S=8

- Prompt: $\int  \left(\left(-\left(-\frac{-1}{\left(e^{2x}\right)^{2}+16}\cdot 2e^{2x}\right)\right)+6\right)-6\,dx$
- Answer: $3\ln|e^{2x}|-\frac{1}{4}\arctan(\frac{e^{2x}}{4})+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=8 · amax=25 · shortfall=2

### C=16 · S=16

- Prompt: $\int  \left(\left(\left(\left(\left(\frac{-1}{\left(e^{2x}\right)^{2}+16}\cdot 2e^{2x}+6\right)-6\right)+4\right)-4\right)+\left(-x-2\right)\right)-\left(-x-2\right)\,dx$
- Answer: $3\ln|e^{2x}|-\frac{1}{4}\arctan(\frac{e^{2x}}{4})+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=16 · amax=25 · shortfall=1

### C=16 · S=32

- Prompt: $\int  \frac{4\left(x-2\right)\left(\ln\left(e^{\frac{-1}{\left(e^{2x}\right)^{2}+16}\cdot 2e^{2x}}\right)+5-5\right)}{4\left(x-2\right)}\,dx$
- Answer: $3\ln|e^{2x}|-\frac{1}{4}\arctan(\frac{e^{2x}}{4})+C$
- From: `form:u_sub_then_pfd_exp` · `conceptual:u_sub+pfd` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=32 · amax=25 · shortfall=1

### C=20 · S=0

- Prompt: $\int \frac{7\left(\ln|x + 6|\right)-1}{\left(\ln|x + 6|\right)^{2}+1}\frac{1}{x + 6}\,dx$
- Answer: $2\ln|\ln|x + 6| - 1|+\frac{7}{2}\ln|\ln|x + 6|^{2}+1|-\arctan(\ln|x + 6|)+C$
- From: `form:u_sub_then_pfd_log` · `conceptual:u_sub+pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=9.5

### C=20 · S=4

- Prompt: $\int  \left(\frac{7\left(\ln|x + 6|\right)-1}{\left(\ln|x + 6|\right)^{2}+1}\frac{1}{x + 6}+\left(-2x-2\right)\right)-\left(-2x-2\right)\,dx$
- Answer: $2\ln|\ln|x + 6| - 1|+\frac{7}{2}\ln|\ln|x + 6|^{2}+1|-\arctan(\ln|x + 6|)+C$
- From: `form:u_sub_then_pfd_log` · `conceptual:u_sub+pfd` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=20 · S=4 · amax=25 · shortfall=8.5

### C=20 · S=8

- Prompt: $\int  \frac{-\left(2+x\right)\frac{7\left(\ln|x + 6|\right)-1}{\left(\ln|x + 6|\right)^{2}+1}\frac{1}{x + 6}}{-\left(2+x\right)}+\left(3x+3\right)-\left(3x+3\right)\,dx$
- Answer: $2\ln|\ln|x + 6| - 1|+\frac{7}{2}\ln|\ln|x + 6|^{2}+1|-\arctan(\ln|x + 6|)+C$
- From: `form:u_sub_then_pfd_log` · `conceptual:u_sub+pfd` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=8 · amax=25 · shortfall=7.5

### C=20 · S=16

- Prompt: $\int  \left(\left(-\left(-\left(\left(\frac{7\left(\ln|x + 6|\right)-1}{\left(\ln|x + 6|\right)^{2}+1}\frac{1}{x + 6}+4\right)-4\right)\right)\right)+\left(3x+1\right)\right)-\left(3x+1\right)\,dx$
- Answer: $2\ln|\ln|x + 6| - 1|+\frac{7}{2}\ln|\ln|x + 6|^{2}+1|-\arctan(\ln|x + 6|)+C$
- From: `form:u_sub_then_pfd_log` · `conceptual:u_sub+pfd` · `effort:add_cancel_const` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=16 · amax=25 · shortfall=6.5

### C=20 · S=32

- Prompt: $\int  \left(\left(\frac{7\left(\ln|x + 6|\right)-1}{\left(\ln|x + 6|\right)^{2}+1}\frac{1}{x + 6}+\left(3x+1\right)\right)-\left(3x+1\right)+\left(3x+1\right)-\left(3x+1\right)+\left(-x+1\right)\right)-\left(-x+1\right)\,dx$
- Answer: $2\ln|\ln|x + 6| - 1|+\frac{7}{2}\ln|\ln|x + 6|^{2}+1|-\arctan(\ln|x + 6|)+C$
- From: `form:u_sub_then_pfd_log` · `conceptual:u_sub+pfd` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=20 · S=32 · amax=25 · shortfall=6.5

### C=25 · S=0

- Prompt: $\int \frac{-3}{\left(\ln|3x|\right)^{2}+16}\frac{3}{3x}\,dx$
- Answer: $-4\ln|\ln|3x| - 2|-\frac{3}{4}\arctan(\frac{\ln|3x|}{4})+C$
- From: `form:u_sub_then_pfd_log` · `conceptual:u_sub+pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=14.5

### C=25 · S=4

- Prompt: $\int  \frac{-\left(3+x\right)\frac{-3}{\left(\ln|3x|\right)^{2}+16}\frac{3}{3x}}{-\left(3+x\right)}\,dx$
- Answer: $-4\ln|\ln|3x| - 2|-\frac{3}{4}\arctan(\frac{\ln|3x|}{4})+C$
- From: `form:u_sub_then_pfd_log` · `conceptual:u_sub+pfd` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=25 · S=4 · amax=25 · shortfall=13.5

### C=25 · S=8

- Prompt: $\int  \left(\left(\frac{-3}{\left(\ln|3x|\right)^{2}+16}\frac{3}{3x}+\left(-2x-1\right)-\left(-2x-1\right)\right)+\left(3x-2\right)\right)-\left(3x-2\right)\,dx$
- Answer: $-4\ln|\ln|3x| - 2|-\frac{3}{4}\arctan(\frac{\ln|3x|}{4})+C$
- From: `form:u_sub_then_pfd_log` · `conceptual:u_sub+pfd` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=25 · S=8 · amax=25 · shortfall=12.5

### C=25 · S=16

- Prompt: $\int  \left(\left(-\left(-\frac{\left(x+2\right)\frac{-3}{\left(\ln|3x|\right)^{2}+16}\frac{3}{3x}}{x+2}\right)\right)+6\right)-6\,dx$
- Answer: $-4\ln|\ln|3x| - 2|-\frac{3}{4}\arctan(\frac{\ln|3x|}{4})+C$
- From: `form:u_sub_then_pfd_log` · `conceptual:u_sub+pfd` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=16 · amax=25 · shortfall=11.5

### C=25 · S=32

- Prompt: $\int  \left(\left(-\left(-\left(\frac{-3}{\left(\ln|3x|\right)^{2}+16}\frac{3}{3x}+3-3\right)\right)\right)+5\right)-5\,dx$
- Answer: $-4\ln|\ln|3x| - 2|-\frac{3}{4}\arctan(\frac{\ln|3x|}{4})+C$
- From: `form:u_sub_then_pfd_log` · `conceptual:u_sub+pfd` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=32 · amax=25 · shortfall=11.5
