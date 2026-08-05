# Integrals — inverse trig

**type_id:** `calc_indef_int_inverse_trigonometric` · **leaf:** `integral_substitution`  
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
| **C=0** | $\int \frac{1}{1+x^{2}}\,dx$ | $\int  \left(\frac{1}{1+x^{2}}+6\right)-6\,dx$ | $\int  \left(\left(\frac{1}{1+x^{2}}+6-6\right)+\left(-x+3\right)\right)-\left(-x+3\right)\,dx$ | $\int  -\left(-\left(\left(\frac{1}{1+x^{2}}+2\right)-2\right)+\left(3x-2\right)-\left(3x-2\right)\right)\,dx$ | $\int  \left(\left(\left(\frac{1}{1+x^{2}}+\left(x+3\right)\right)-\left(x+3\right)+3-3\right)+4\right)-4\,dx$ |
| **C=4** | $\int \frac{1}{1+x^{2}}\,dx$ | $\int  \frac{1}{1+x^{2}}+\left(3x-2\right)-\left(3x-2\right)\,dx$ | $\int  -\left(-\left(\left(\frac{1}{1+x^{2}}+4\right)-4\right)\right)\,dx$ | $\int  \left(-\left(-\frac{-\left(1-x\right)\frac{1}{1+x^{2}}}{-\left(1-x\right)}\right)\right)+4-4\,dx$ | $\int  \left(\left(\left(\frac{1}{1+x^{2}}+\left(3x+2\right)-\left(3x+2\right)\right)+4-4\right)+\left(2x-2\right)\right)-\left(2x-2\right)\,dx$ |
| **C=8** | $\int \frac{1}{9+x^{2}}\,dx$ | $\int  \left(\frac{1}{9+x^{2}}+1\right)-1\,dx$ | $\int  \left(\left(-\left(-\frac{1}{9+x^{2}}\right)\right)+3\right)-3\,dx$ | $\int  \left(\frac{-\left(2+x\right)\left(\left(\frac{1}{9+x^{2}}+1\right)-1\right)}{-\left(2+x\right)}+\left(-2x-2\right)\right)-\left(-2x-2\right)\,dx$ | $\int  \left(\left(-\left(-\frac{1}{9+x^{2}}\right)\right)+\left(-2x-2\right)-\left(-2x-2\right)+4\right)-4\,dx$ |
| **C=12** | $\int \frac{1}{1+x^{2}}\,dx$ | $\int  \frac{4\left(x-2\right)\frac{1}{1+x^{2}}}{4\left(x-2\right)}\,dx$ | $\int  \left(\left(-\left(-\frac{1}{1+x^{2}}\right)\right)+1\right)-1\,dx$ | $\int  \frac{\left(x+2\right)\left(\left(\frac{1}{1+x^{2}}+\left(2x-2\right)-\left(2x-2\right)\right)+3-3\right)}{x+2}\,dx$ | $\int  \left(\left(\frac{\left(x+1\right)\frac{1}{1+x^{2}}}{x+1}+6-6\right)+4\right)-4\,dx$ |
| **C=16** | $\int \frac{1}{4+4x^{2}}\,dx$ | $\int  \frac{2\left(x-1\right)\frac{1}{4+4x^{2}}}{2\left(x-1\right)}\,dx$ | $\int  \frac{4\left(x+2\right)\left(\frac{1}{4+4x^{2}}+\left(x+2\right)-\left(x+2\right)\right)}{4\left(x+2\right)}\,dx$ | $\int  \left(\left(\frac{\left(x+1\right)\frac{1}{4+4x^{2}}}{x+1}+1-1\right)+\left(2x\right)\right)-\left(2x\right)\,dx$ | $\int  \frac{-\left(3+x\right)\left(\left(\frac{1}{4+4x^{2}}+5-5\right)+\left(2x-2\right)\right)-\left(2x-2\right)}{-\left(3+x\right)}\,dx$ |
| **C=20** | $\int \frac{1}{\sqrt{4-x^{2}}}\,dx$ | $\int  -\left(-\frac{1}{\sqrt{4-x^{2}}}\right)\,dx$ | $\int  \frac{-\left(1+x\right)\frac{1}{\sqrt{4-x^{2}}}}{-\left(1+x\right)}+\left(2x-2\right)-\left(2x-2\right)\,dx$ | $\int  \left(\left(\left(\frac{1}{\sqrt{4-x^{2}}}+6\right)-6\right)+\left(3x-2\right)\right)-\left(3x-2\right)+\left(x+3\right)-\left(x+3\right)\,dx$ | $\int  \left(\frac{-\left(2-x\right)\left(-\left(-\frac{1}{\sqrt{4-x^{2}}}\right)\right)}{-\left(2-x\right)}+\left(-x-1\right)\right)-\left(-x-1\right)\,dx$ |
| **C=25** | $\int \frac{1}{\sqrt{16-16x^{2}}}\,dx$ | $\int  \frac{-\left(1-x\right)\frac{1}{\sqrt{16-16x^{2}}}}{-\left(1-x\right)}\,dx$ | $\int  \frac{\left(x+2\right)\left(\frac{1}{\sqrt{16-16x^{2}}}+\left(-x-2\right)-\left(-x-2\right)\right)}{x+2}\,dx$ | $\int  \frac{-\left(3+x\right)\left(\left(\left(\frac{1}{\sqrt{16-16x^{2}}}+4\right)-4\right)+6-6\right)}{-\left(3+x\right)}\,dx$ | $\int  \left(\left(\frac{1}{\sqrt{16-16x^{2}}}+\left(3x+2\right)\right)-\left(3x+2\right)+\left(3x\right)\right)-\left(3x\right)+6-6\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\arctan(x)+C$ | $\arctan(x)+C$ | $\arctan(x)+C$ | $\arctan(x)+C$ | $\arctan(x)+C$ |
| **C=4** | $\arctan(x)+C$ | $\arctan(x)+C$ | $\arctan(x)+C$ | $\arctan(x)+C$ | $\arctan(x)+C$ |
| **C=8** | $\frac{1}{3}\arctan\left(\frac{x}{3}\right)+C$ | $\frac{1}{3}\arctan\left(\frac{x}{3}\right)+C$ | $\frac{1}{3}\arctan\left(\frac{x}{3}\right)+C$ | $\frac{1}{3}\arctan\left(\frac{x}{3}\right)+C$ | $\frac{1}{3}\arctan\left(\frac{x}{3}\right)+C$ |
| **C=12** | $\arctan(x)+C$ | $\arctan(x)+C$ | $\arctan(x)+C$ | $\arctan(x)+C$ | $\arctan(x)+C$ |
| **C=16** | $\frac{1}{4}\arctan\left(\frac{2x}{2}\right)+C$ | $\frac{1}{4}\arctan\left(\frac{2x}{2}\right)+C$ | $\frac{1}{4}\arctan\left(\frac{2x}{2}\right)+C$ | $\frac{1}{4}\arctan\left(\frac{2x}{2}\right)+C$ | $\frac{1}{4}\arctan\left(\frac{2x}{2}\right)+C$ |
| **C=20** | $\arcsin\left(\frac{x}{2}\right)+C$ | $\arcsin\left(\frac{x}{2}\right)+C$ | $\arcsin\left(\frac{x}{2}\right)+C$ | $\arcsin\left(\frac{x}{2}\right)+C$ | $\arcsin\left(\frac{x}{2}\right)+C$ |
| **C=25** | $\frac{1}{4}\arcsin\left(\frac{4x}{4}\right)+C$ | $\frac{1}{4}\arcsin\left(\frac{4x}{4}\right)+C$ | $\frac{1}{4}\arcsin\left(\frac{4x}{4}\right)+C$ | $\frac{1}{4}\arcsin\left(\frac{4x}{4}\right)+C$ | $\frac{1}{4}\arcsin\left(\frac{4x}{4}\right)+C$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int \frac{1}{1+x^{2}}\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int  \left(\frac{1}{1+x^{2}}+6\right)-6\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `effort:add_cancel_const`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int  \left(\left(\frac{1}{1+x^{2}}+6-6\right)+\left(-x+3\right)\right)-\left(-x+3\right)\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int  -\left(-\left(\left(\frac{1}{1+x^{2}}+2\right)-2\right)+\left(3x-2\right)-\left(3x-2\right)\right)\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int  \left(\left(\left(\frac{1}{1+x^{2}}+\left(x+3\right)\right)-\left(x+3\right)+3-3\right)+4\right)-4\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int \frac{1}{1+x^{2}}\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\int  \frac{1}{1+x^{2}}+\left(3x-2\right)-\left(3x-2\right)\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `effort:add_cancel_linear`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\int  -\left(-\left(\left(\frac{1}{1+x^{2}}+4\right)-4\right)\right)\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\int  \left(-\left(-\frac{-\left(1-x\right)\frac{1}{1+x^{2}}}{-\left(1-x\right)}\right)\right)+4-4\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\int  \left(\left(\left(\frac{1}{1+x^{2}}+\left(3x+2\right)-\left(3x+2\right)\right)+4-4\right)+\left(2x-2\right)\right)-\left(2x-2\right)\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\int \frac{1}{9+x^{2}}\,dx$
- Answer: $\frac{1}{3}\arctan\left(\frac{x}{3}\right)+C$
- From: `form:arctan_a2` · `conceptual:invtrig` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25 · shortfall=4

### C=8 · S=4

- Prompt: $\int  \left(\frac{1}{9+x^{2}}+1\right)-1\,dx$
- Answer: $\frac{1}{3}\arctan\left(\frac{x}{3}\right)+C$
- From: `form:arctan_a2` · `conceptual:invtrig` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=8 · S=4 · amax=25 · shortfall=3

### C=8 · S=8

- Prompt: $\int  \left(\left(-\left(-\frac{1}{9+x^{2}}\right)\right)+3\right)-3\,dx$
- Answer: $\frac{1}{3}\arctan\left(\frac{x}{3}\right)+C$
- From: `form:arctan_a2` · `conceptual:invtrig` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=8 · S=8 · amax=25 · shortfall=2

### C=8 · S=16

- Prompt: $\int  \left(\frac{-\left(2+x\right)\left(\left(\frac{1}{9+x^{2}}+1\right)-1\right)}{-\left(2+x\right)}+\left(-2x-2\right)\right)-\left(-2x-2\right)\,dx$
- Answer: $\frac{1}{3}\arctan\left(\frac{x}{3}\right)+C$
- From: `form:arctan_a2` · `conceptual:invtrig` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=16 · amax=25 · shortfall=1

### C=8 · S=32

- Prompt: $\int  \left(\left(-\left(-\frac{1}{9+x^{2}}\right)\right)+\left(-2x-2\right)-\left(-2x-2\right)+4\right)-4\,dx$
- Answer: $\frac{1}{3}\arctan\left(\frac{x}{3}\right)+C$
- From: `form:arctan_a2` · `conceptual:invtrig` · `effort:double_neg` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=32 · amax=25 · shortfall=1

### C=12 · S=0

- Prompt: $\int \frac{1}{1+x^{2}}\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=12 · S=0 · amax=25 · shortfall=8

### C=12 · S=4

- Prompt: $\int  \frac{4\left(x-2\right)\frac{1}{1+x^{2}}}{4\left(x-2\right)}\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `prereq:cancel_quot_bait`
- Flags: C=12 · S=4 · amax=25 · shortfall=7

### C=12 · S=8

- Prompt: $\int  \left(\left(-\left(-\frac{1}{1+x^{2}}\right)\right)+1\right)-1\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=12 · S=8 · amax=25 · shortfall=6

### C=12 · S=16

- Prompt: $\int  \frac{\left(x+2\right)\left(\left(\frac{1}{1+x^{2}}+\left(2x-2\right)-\left(2x-2\right)\right)+3-3\right)}{x+2}\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=16 · amax=25 · shortfall=5

### C=12 · S=32

- Prompt: $\int  \left(\left(\frac{\left(x+1\right)\frac{1}{1+x^{2}}}{x+1}+6-6\right)+4\right)-4\,dx$
- Answer: $\arctan(x)+C$
- From: `form:arctan_basic` · `conceptual:invtrig` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=12 · S=32 · amax=25 · shortfall=5

### C=16 · S=0

- Prompt: $\int \frac{1}{4+4x^{2}}\,dx$
- Answer: $\frac{1}{4}\arctan\left(\frac{2x}{2}\right)+C$
- From: `form:arctan_scaled` · `conceptual:invtrig` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=12

### C=16 · S=4

- Prompt: $\int  \frac{2\left(x-1\right)\frac{1}{4+4x^{2}}}{2\left(x-1\right)}\,dx$
- Answer: $\frac{1}{4}\arctan\left(\frac{2x}{2}\right)+C$
- From: `form:arctan_scaled` · `conceptual:invtrig` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=16 · S=4 · amax=25 · shortfall=11

### C=16 · S=8

- Prompt: $\int  \frac{4\left(x+2\right)\left(\frac{1}{4+4x^{2}}+\left(x+2\right)-\left(x+2\right)\right)}{4\left(x+2\right)}\,dx$
- Answer: $\frac{1}{4}\arctan\left(\frac{2x}{2}\right)+C$
- From: `form:arctan_scaled` · `conceptual:invtrig` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=16 · S=8 · amax=25 · shortfall=10

### C=16 · S=16

- Prompt: $\int  \left(\left(\frac{\left(x+1\right)\frac{1}{4+4x^{2}}}{x+1}+1-1\right)+\left(2x\right)\right)-\left(2x\right)\,dx$
- Answer: $\frac{1}{4}\arctan\left(\frac{2x}{2}\right)+C$
- From: `form:arctan_scaled` · `conceptual:invtrig` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=16 · amax=25 · shortfall=9

### C=16 · S=32

- Prompt: $\int  \frac{-\left(3+x\right)\left(\left(\frac{1}{4+4x^{2}}+5-5\right)+\left(2x-2\right)\right)-\left(2x-2\right)}{-\left(3+x\right)}\,dx$
- Answer: $\frac{1}{4}\arctan\left(\frac{2x}{2}\right)+C$
- From: `form:arctan_scaled` · `conceptual:invtrig` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=32 · amax=25 · shortfall=9

### C=20 · S=0

- Prompt: $\int \frac{1}{\sqrt{4-x^{2}}}\,dx$
- Answer: $\arcsin\left(\frac{x}{2}\right)+C$
- From: `form:arcsin_a2` · `conceptual:invtrig` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=16

### C=20 · S=4

- Prompt: $\int  -\left(-\frac{1}{\sqrt{4-x^{2}}}\right)\,dx$
- Answer: $\arcsin\left(\frac{x}{2}\right)+C$
- From: `form:arcsin_a2` · `conceptual:invtrig` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=4 · amax=25 · shortfall=15

### C=20 · S=8

- Prompt: $\int  \frac{-\left(1+x\right)\frac{1}{\sqrt{4-x^{2}}}}{-\left(1+x\right)}+\left(2x-2\right)-\left(2x-2\right)\,dx$
- Answer: $\arcsin\left(\frac{x}{2}\right)+C$
- From: `form:arcsin_a2` · `conceptual:invtrig` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=20 · S=8 · amax=25 · shortfall=14

### C=20 · S=16

- Prompt: $\int  \left(\left(\left(\frac{1}{\sqrt{4-x^{2}}}+6\right)-6\right)+\left(3x-2\right)\right)-\left(3x-2\right)+\left(x+3\right)-\left(x+3\right)\,dx$
- Answer: $\arcsin\left(\frac{x}{2}\right)+C$
- From: `form:arcsin_a2` · `conceptual:invtrig` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=20 · S=16 · amax=25 · shortfall=13

### C=20 · S=32

- Prompt: $\int  \left(\frac{-\left(2-x\right)\left(-\left(-\frac{1}{\sqrt{4-x^{2}}}\right)\right)}{-\left(2-x\right)}+\left(-x-1\right)\right)-\left(-x-1\right)\,dx$
- Answer: $\arcsin\left(\frac{x}{2}\right)+C$
- From: `form:arcsin_a2` · `conceptual:invtrig` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=32 · amax=25 · shortfall=13

### C=25 · S=0

- Prompt: $\int \frac{1}{\sqrt{16-16x^{2}}}\,dx$
- Answer: $\frac{1}{4}\arcsin\left(\frac{4x}{4}\right)+C$
- From: `form:arcsin_scaled` · `conceptual:invtrig` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=21

### C=25 · S=4

- Prompt: $\int  \frac{-\left(1-x\right)\frac{1}{\sqrt{16-16x^{2}}}}{-\left(1-x\right)}\,dx$
- Answer: $\frac{1}{4}\arcsin\left(\frac{4x}{4}\right)+C$
- From: `form:arcsin_scaled` · `conceptual:invtrig` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=25 · S=4 · amax=25 · shortfall=20

### C=25 · S=8

- Prompt: $\int  \frac{\left(x+2\right)\left(\frac{1}{\sqrt{16-16x^{2}}}+\left(-x-2\right)-\left(-x-2\right)\right)}{x+2}\,dx$
- Answer: $\frac{1}{4}\arcsin\left(\frac{4x}{4}\right)+C$
- From: `form:arcsin_scaled` · `conceptual:invtrig` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=25 · S=8 · amax=25 · shortfall=19

### C=25 · S=16

- Prompt: $\int  \frac{-\left(3+x\right)\left(\left(\left(\frac{1}{\sqrt{16-16x^{2}}}+4\right)-4\right)+6-6\right)}{-\left(3+x\right)}\,dx$
- Answer: $\frac{1}{4}\arcsin\left(\frac{4x}{4}\right)+C$
- From: `form:arcsin_scaled` · `conceptual:invtrig` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=25 · S=16 · amax=25 · shortfall=18

### C=25 · S=32

- Prompt: $\int  \left(\left(\frac{1}{\sqrt{16-16x^{2}}}+\left(3x+2\right)\right)-\left(3x+2\right)+\left(3x\right)\right)-\left(3x\right)+6-6\,dx$
- Answer: $\frac{1}{4}\arcsin\left(\frac{4x}{4}\right)+C$
- From: `form:arcsin_scaled` · `conceptual:invtrig` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=25 · S=32 · amax=25 · shortfall=18
