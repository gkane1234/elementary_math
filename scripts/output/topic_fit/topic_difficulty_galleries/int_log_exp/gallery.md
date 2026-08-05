# Integrals — log / exp

**type_id:** `calc_indef_int_logarithmic_rule_and_exponentials` · **leaf:** `integral_substitution`  
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
| **C=0** | $\int e^{x}\,dx$ | $\int  \frac{-\left(2-x\right)e^{x}}{-\left(2-x\right)}\,dx$ | $\int  \left(\left(e^{x}+4-4\right)+2\right)-2\,dx$ | $\int  \left(\left(-\left(-\frac{-\left(1-x\right)e^{x}}{-\left(1-x\right)}\right)\right)+\left(3x+3\right)\right)-\left(3x+3\right)\,dx$ | $\int  \left(\left(\left(e^{x}+4-4\right)+\left(-2x+1\right)\right)-\left(-2x+1\right)+\left(-x+3\right)\right)-\left(-x+3\right)\,dx$ |
| **C=4** | $\int 3^{x}\,dx$ | $\int  -\left(-3^{x}\right)\,dx$ | $\int  -\left(-\frac{2\left(x-3\right)3^{x}}{2\left(x-3\right)}\right)\,dx$ | $\int  \left(\left(\frac{\left(x+2\right)3^{x}}{x+2}+\left(3x+1\right)\right)-\left(3x+1\right)+5\right)-5\,dx$ | $\int  \left(-\left(-\frac{3\left(x-3\right)3^{x}}{3\left(x-3\right)}\right)\right)+\left(-2x-1\right)-\left(-2x-1\right)\,dx$ |
| **C=8** | $\int e^{5x}\,dx$ | $\int  e^{5x}+4-4\,dx$ | $\int  -\left(-\left(e^{5x}+6-6\right)\right)\,dx$ | $\int  \left(-\left(-\frac{4\left(x-2\right)e^{5x}}{4\left(x-2\right)}\right)\right)+\left(x-1\right)-\left(x-1\right)\,dx$ | $\int  -\left(-\left(\left(e^{5x}+6-6\right)+3-3\right)\right)\,dx$ |
| **C=12** | $\int 3^{x}\,dx$ | $\int  \left(3^{x}+1\right)-1\,dx$ | $\int  \left(\left(3^{x}+\left(-x+3\right)-\left(-x+3\right)\right)+\left(x-2\right)\right)-\left(x-2\right)\,dx$ | $\int  \frac{2\left(x-1\right)\left(-\left(-\left(3^{x}+\left(3x\right)-\left(3x\right)\right)\right)\right)}{2\left(x-1\right)}\,dx$ | $\int  \left(\left(-\left(-\frac{\left(x-1\right)3^{x}}{x-1}\right)\right)+4\right)-4\,dx$ |
| **C=16** | $\int e^{3x}\,dx$ | $\int  e^{3x}+2-2\,dx$ | $\int  \left(-\left(-e^{3x}\right)\right)+\left(-x\right)-\left(-x\right)\,dx$ | $\int  \left(-\left(-\frac{-\left(2+x\right)e^{3x}}{-\left(2+x\right)}\right)\right)+5-5\,dx$ | $\int  \frac{4\left(x+2\right)\left(-\left(-e^{3x}\right)\right)}{4\left(x+2\right)}+\left(2x\right)-\left(2x\right)\,dx$ |
| **C=20** | $\int \frac{1}{x}\,dx$ | $\int  \frac{1}{x}+\left(x-2\right)-\left(x-2\right)\,dx$ | $\int  \left(\left(\frac{1}{x}+5\right)-5\right)+\left(x+2\right)-\left(x+2\right)\,dx$ | $\int  \left(\left(\frac{1}{x}+\left(-x+3\right)-\left(-x+3\right)\right)+\left(x+2\right)-\left(x+2\right)+5\right)-5\,dx$ | $\int  \left(-\left(-\frac{\left(x-2\right)\frac{1}{x}}{x-2}\right)\right)+2-2\,dx$ |
| **C=25** | $\int \frac{3}{3x + 1}\,dx$ | $\int  \frac{3}{3x + 1}+4-4\,dx$ | $\int  \left(\frac{3}{3x + 1}+\left(-2x+1\right)-\left(-2x+1\right)\right)+\left(2x-2\right)-\left(2x-2\right)\,dx$ | $\int  \frac{-\left(3+x\right)\left(-\left(-\left(\left(\frac{3}{3x + 1}+2\right)-2\right)\right)\right)}{-\left(3+x\right)}\,dx$ | $\int  \frac{\left(x+2\right)\left(\left(-\left(-\frac{3}{3x + 1}\right)\right)+\left(-x+3\right)\right)-\left(-x+3\right)}{x+2}\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $e^{x}+C$ | $e^{x}+C$ | $e^{x}+C$ | $e^{x}+C$ | $e^{x}+C$ |
| **C=4** | $\frac{3^{x}}{\ln 3}+C$ | $\frac{3^{x}}{\ln 3}+C$ | $\frac{3^{x}}{\ln 3}+C$ | $\frac{3^{x}}{\ln 3}+C$ | $\frac{3^{x}}{\ln 3}+C$ |
| **C=8** | $\frac{1}{5}e^{5x}+C$ | $\frac{1}{5}e^{5x}+C$ | $\frac{1}{5}e^{5x}+C$ | $\frac{1}{5}e^{5x}+C$ | $\frac{1}{5}e^{5x}+C$ |
| **C=12** | $\frac{3^{x}}{\ln 3}+C$ | $\frac{3^{x}}{\ln 3}+C$ | $\frac{3^{x}}{\ln 3}+C$ | $\frac{3^{x}}{\ln 3}+C$ | $\frac{3^{x}}{\ln 3}+C$ |
| **C=16** | $\frac{1}{3}e^{3x}+C$ | $\frac{1}{3}e^{3x}+C$ | $\frac{1}{3}e^{3x}+C$ | $\frac{1}{3}e^{3x}+C$ | $\frac{1}{3}e^{3x}+C$ |
| **C=20** | $\ln|x|+C$ | $\ln|x|+C$ | $\ln|x|+C$ | $\ln|x|+C$ | $\ln|x|+C$ |
| **C=25** | $\ln|3x + 1|+C$ | $\ln|3x + 1|+C$ | $\ln|3x + 1|+C$ | $\ln|3x + 1|+C$ | $\ln|3x + 1|+C$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int e^{x}\,dx$
- Answer: $e^{x}+C$
- From: `form:exp` · `conceptual:ln_exp` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int  \frac{-\left(2-x\right)e^{x}}{-\left(2-x\right)}\,dx$
- Answer: $e^{x}+C$
- From: `form:exp` · `conceptual:ln_exp` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int  \left(\left(e^{x}+4-4\right)+2\right)-2\,dx$
- Answer: $e^{x}+C$
- From: `form:exp` · `conceptual:ln_exp` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_const` · `effort:add_cancel_const`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int  \left(\left(-\left(-\frac{-\left(1-x\right)e^{x}}{-\left(1-x\right)}\right)\right)+\left(3x+3\right)\right)-\left(3x+3\right)\,dx$
- Answer: $e^{x}+C$
- From: `form:exp` · `conceptual:ln_exp` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int  \left(\left(\left(e^{x}+4-4\right)+\left(-2x+1\right)\right)-\left(-2x+1\right)+\left(-x+3\right)\right)-\left(-x+3\right)\,dx$
- Answer: $e^{x}+C$
- From: `form:exp` · `conceptual:ln_exp` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_const`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int 3^{x}\,dx$
- Answer: $\frac{3^{x}}{\ln 3}+C$
- From: `form:base_a` · `conceptual:ln_exp` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25 · shortfall=0.5

### C=4 · S=4

- Prompt: $\int  -\left(-3^{x}\right)\,dx$
- Answer: $\frac{3^{x}}{\ln 3}+C$
- From: `form:base_a` · `conceptual:ln_exp` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\int  -\left(-\frac{2\left(x-3\right)3^{x}}{2\left(x-3\right)}\right)\,dx$
- Answer: $\frac{3^{x}}{\ln 3}+C$
- From: `form:base_a` · `conceptual:ln_exp` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\int  \left(\left(\frac{\left(x+2\right)3^{x}}{x+2}+\left(3x+1\right)\right)-\left(3x+1\right)+5\right)-5\,dx$
- Answer: $\frac{3^{x}}{\ln 3}+C$
- From: `form:base_a` · `conceptual:ln_exp` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\int  \left(-\left(-\frac{3\left(x-3\right)3^{x}}{3\left(x-3\right)}\right)\right)+\left(-2x-1\right)-\left(-2x-1\right)\,dx$
- Answer: $\frac{3^{x}}{\ln 3}+C$
- From: `form:base_a` · `conceptual:ln_exp` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\int e^{5x}\,dx$
- Answer: $\frac{1}{5}e^{5x}+C$
- From: `form:exp_k` · `conceptual:ln_exp` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25 · shortfall=4.5

### C=8 · S=4

- Prompt: $\int  e^{5x}+4-4\,dx$
- Answer: $\frac{1}{5}e^{5x}+C$
- From: `form:exp_k` · `conceptual:ln_exp` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=8 · S=4 · amax=25 · shortfall=3.5

### C=8 · S=8

- Prompt: $\int  -\left(-\left(e^{5x}+6-6\right)\right)\,dx$
- Answer: $\frac{1}{5}e^{5x}+C$
- From: `form:exp_k` · `conceptual:ln_exp` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=8 · amax=25 · shortfall=2.5

### C=8 · S=16

- Prompt: $\int  \left(-\left(-\frac{4\left(x-2\right)e^{5x}}{4\left(x-2\right)}\right)\right)+\left(x-1\right)-\left(x-1\right)\,dx$
- Answer: $\frac{1}{5}e^{5x}+C$
- From: `form:exp_k` · `conceptual:ln_exp` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=16 · amax=25 · shortfall=1.5

### C=8 · S=32

- Prompt: $\int  -\left(-\left(\left(e^{5x}+6-6\right)+3-3\right)\right)\,dx$
- Answer: $\frac{1}{5}e^{5x}+C$
- From: `form:exp_k` · `conceptual:ln_exp` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=32 · amax=25 · shortfall=1.5

### C=12 · S=0

- Prompt: $\int 3^{x}\,dx$
- Answer: $\frac{3^{x}}{\ln 3}+C$
- From: `form:base_a` · `conceptual:ln_exp` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=8.5

### C=12 · S=4

- Prompt: $\int  \left(3^{x}+1\right)-1\,dx$
- Answer: $\frac{3^{x}}{\ln 3}+C$
- From: `form:base_a` · `conceptual:ln_exp` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=12 · S=4 · amax=25 · shortfall=7.5

### C=12 · S=8

- Prompt: $\int  \left(\left(3^{x}+\left(-x+3\right)-\left(-x+3\right)\right)+\left(x-2\right)\right)-\left(x-2\right)\,dx$
- Answer: $\frac{3^{x}}{\ln 3}+C$
- From: `form:base_a` · `conceptual:ln_exp` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=12 · S=8 · amax=25 · shortfall=6.5

### C=12 · S=16

- Prompt: $\int  \frac{2\left(x-1\right)\left(-\left(-\left(3^{x}+\left(3x\right)-\left(3x\right)\right)\right)\right)}{2\left(x-1\right)}\,dx$
- Answer: $\frac{3^{x}}{\ln 3}+C$
- From: `form:base_a` · `conceptual:ln_exp` · `effort:add_cancel_linear` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=16 · amax=25 · shortfall=5.5

### C=12 · S=32

- Prompt: $\int  \left(\left(-\left(-\frac{\left(x-1\right)3^{x}}{x-1}\right)\right)+4\right)-4\,dx$
- Answer: $\frac{3^{x}}{\ln 3}+C$
- From: `form:base_a` · `conceptual:ln_exp` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=32 · amax=25 · shortfall=5.5

### C=16 · S=0

- Prompt: $\int e^{3x}\,dx$
- Answer: $\frac{1}{3}e^{3x}+C$
- From: `form:exp_k` · `conceptual:ln_exp` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=12.5

### C=16 · S=4

- Prompt: $\int  e^{3x}+2-2\,dx$
- Answer: $\frac{1}{3}e^{3x}+C$
- From: `form:exp_k` · `conceptual:ln_exp` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=16 · S=4 · amax=25 · shortfall=11.5

### C=16 · S=8

- Prompt: $\int  \left(-\left(-e^{3x}\right)\right)+\left(-x\right)-\left(-x\right)\,dx$
- Answer: $\frac{1}{3}e^{3x}+C$
- From: `form:exp_k` · `conceptual:ln_exp` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=8 · amax=25 · shortfall=10.5

### C=16 · S=16

- Prompt: $\int  \left(-\left(-\frac{-\left(2+x\right)e^{3x}}{-\left(2+x\right)}\right)\right)+5-5\,dx$
- Answer: $\frac{1}{3}e^{3x}+C$
- From: `form:exp_k` · `conceptual:ln_exp` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=16 · amax=25 · shortfall=9.5

### C=16 · S=32

- Prompt: $\int  \frac{4\left(x+2\right)\left(-\left(-e^{3x}\right)\right)}{4\left(x+2\right)}+\left(2x\right)-\left(2x\right)\,dx$
- Answer: $\frac{1}{3}e^{3x}+C$
- From: `form:exp_k` · `conceptual:ln_exp` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=32 · amax=25 · shortfall=9.5

### C=20 · S=0

- Prompt: $\int \frac{1}{x}\,dx$
- Answer: $\ln|x|+C$
- From: `form:ln` · `conceptual:ln_exp` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=0 · amax=25 · shortfall=16.5

### C=20 · S=4

- Prompt: $\int  \frac{1}{x}+\left(x-2\right)-\left(x-2\right)\,dx$
- Answer: $\ln|x|+C$
- From: `form:ln` · `conceptual:ln_exp` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=20 · S=4 · amax=25 · shortfall=15.5

### C=20 · S=8

- Prompt: $\int  \left(\left(\frac{1}{x}+5\right)-5\right)+\left(x+2\right)-\left(x+2\right)\,dx$
- Answer: $\ln|x|+C$
- From: `form:ln` · `conceptual:ln_exp` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_const`
- Flags: C=20 · S=8 · amax=25 · shortfall=14.5

### C=20 · S=16

- Prompt: $\int  \left(\left(\frac{1}{x}+\left(-x+3\right)-\left(-x+3\right)\right)+\left(x+2\right)-\left(x+2\right)+5\right)-5\,dx$
- Answer: $\ln|x|+C$
- From: `form:ln` · `conceptual:ln_exp` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `effort:add_cancel_linear`
- Flags: C=20 · S=16 · amax=25 · shortfall=13.5

### C=20 · S=32

- Prompt: $\int  \left(-\left(-\frac{\left(x-2\right)\frac{1}{x}}{x-2}\right)\right)+2-2\,dx$
- Answer: $\ln|x|+C$
- From: `form:ln` · `conceptual:ln_exp` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=32 · amax=25 · shortfall=13.5

### C=25 · S=0

- Prompt: $\int \frac{3}{3x + 1}\,dx$
- Answer: $\ln|3x + 1|+C$
- From: `form:ln_linear` · `conceptual:ln_exp` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=21.5

### C=25 · S=4

- Prompt: $\int  \frac{3}{3x + 1}+4-4\,dx$
- Answer: $\ln|3x + 1|+C$
- From: `form:ln_linear` · `conceptual:ln_exp` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=25 · S=4 · amax=25 · shortfall=20.5

### C=25 · S=8

- Prompt: $\int  \left(\frac{3}{3x + 1}+\left(-2x+1\right)-\left(-2x+1\right)\right)+\left(2x-2\right)-\left(2x-2\right)\,dx$
- Answer: $\ln|3x + 1|+C$
- From: `form:ln_linear` · `conceptual:ln_exp` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=25 · S=8 · amax=25 · shortfall=19.5

### C=25 · S=16

- Prompt: $\int  \frac{-\left(3+x\right)\left(-\left(-\left(\left(\frac{3}{3x + 1}+2\right)-2\right)\right)\right)}{-\left(3+x\right)}\,dx$
- Answer: $\ln|3x + 1|+C$
- From: `form:ln_linear` · `conceptual:ln_exp` · `effort:add_cancel_const` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=16 · amax=25 · shortfall=18.5

### C=25 · S=32

- Prompt: $\int  \frac{\left(x+2\right)\left(\left(-\left(-\frac{3}{3x + 1}\right)\right)+\left(-x+3\right)\right)-\left(-x+3\right)}{x+2}\,dx$
- Answer: $\ln|3x + 1|+C$
- From: `form:ln_linear` · `conceptual:ln_exp` · `effort:double_neg` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=32 · amax=25 · shortfall=18.5
