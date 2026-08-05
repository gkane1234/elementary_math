# Integrals — trigonometric

**type_id:** `calc_indef_int_trigonometric` · **leaf:** `integral_trigonometric`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_trig`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\int \sec^{2}(x)\,dx$ | $\int  \frac{-\left(3+x\right)\sec^{2}(x)}{-\left(3+x\right)}\,dx$ | $\int  \left(\left(-\left(-\sec^{2}(x)\right)\right)+6\right)-6\,dx$ | $\int  -\left(-\left(\left(\frac{-\left(2+x\right)\sec^{2}(x)}{-\left(2+x\right)}+5\right)-5\right)\right)\,dx$ | $\int  \frac{-\left(2+x\right)\left(-\left(-\sec^{2}(x)\right)\right)}{-\left(2+x\right)}+\left(3x+2\right)-\left(3x+2\right)\,dx$ |
| **C=4** | $\int \sin^{4}(x)\cos(x)\,dx$ | $\int  \left(\sin^{4}(x)\cos(x)+\left(3x-1\right)\right)-\left(3x-1\right)\,dx$ | $\int  -\left(-\frac{4\left(x+1\right)\sin^{4}(x)\cos(x)}{4\left(x+1\right)}\right)\,dx$ | $\int  \left(\left(\frac{-\left(1-x\right)\sin^{4}(x)\cos(x)}{-\left(1-x\right)}+\left(-x+2\right)\right)-\left(-x+2\right)+\left(3x+3\right)\right)-\left(3x+3\right)\,dx$ | $\int  \left(\frac{3\left(x+3\right)\left(\sin^{4}(x)\cos(x)+3-3\right)}{3\left(x+3\right)}+\left(-2x\right)\right)-\left(-2x\right)\,dx$ |
| **C=8** | $\int \tan^{2}(x)\,dx$ | $\int  \left(\tan^{2}(x)+4\right)-4\,dx$ | $\int  -\left(-\frac{\left(x+2\right)\tan^{2}(x)}{x+2}\right)\,dx$ | $\int  \left(\left(-\left(-\frac{\left(x-2\right)\tan^{2}(x)}{x-2}\right)\right)+\left(3x+3\right)\right)-\left(3x+3\right)\,dx$ | $\int  \left(\left(\left(-\left(-\tan^{2}(x)\right)\right)+4-4\right)+6\right)-6\,dx$ |
| **C=12** | $\int \sin^{2}(x)\cos^{2}(x)\,dx$ | $\int  \frac{-\left(1+x\right)\sin^{2}(x)\cos^{2}(x)}{-\left(1+x\right)}\,dx$ | $\int  \left(\frac{4\left(x+2\right)\sin^{2}(x)\cos^{2}(x)}{4\left(x+2\right)}+\left(2x-1\right)\right)-\left(2x-1\right)\,dx$ | $\int  -\left(-\frac{\left(x+3\right)\left(\sin^{2}(x)\cos^{2}(x)+5-5\right)}{x+3}\right)\,dx$ | $\int  \frac{\left(x+2\right)\left(\left(\left(-\left(-\sin^{2}(x)\cos^{2}(x)\right)\right)+1\right)-1\right)}{x+2}\,dx$ |
| **C=16** | $\int \tan^{4}(x)\,dx$ | $\int  \left(\tan^{4}(x)+\left(3x-1\right)\right)-\left(3x-1\right)\,dx$ | $\int  \frac{\left(x-3\right)\left(-\left(-\tan^{4}(x)\right)\right)}{x-3}\,dx$ | $\int  \left(\left(\left(\tan^{4}(x)+\left(3x-2\right)-\left(3x-2\right)\right)+2\right)-2\right)+3-3\,dx$ | $\int  -\left(-\left(\left(\left(\tan^{4}(x)+\left(x\right)\right)-\left(x\right)+3\right)-3\right)\right)\,dx$ |
| **C=20** | $\int \tan^{2}(x)\,dx$ | $\int  \left(\tan^{2}(x)+\left(x\right)\right)-\left(x\right)\,dx$ | $\int  \frac{3\left(x+2\right)\left(-\left(-\tan^{2}(x)\right)\right)}{3\left(x+2\right)}\,dx$ | $\int  \left(-\left(-\frac{-\left(1-x\right)\tan^{2}(x)}{-\left(1-x\right)}\right)\right)+\left(-2x+3\right)-\left(-2x+3\right)\,dx$ | $\int  \frac{-\left(1+x\right)\left(\left(\tan^{2}(x)+\left(3x+1\right)\right)-\left(3x+1\right)+1-1\right)}{-\left(1+x\right)}\,dx$ |
| **C=25** | $\int \cos(6x)\cos(5x)\,dx$ | $\int  \frac{-\left(1-x\right)\cos(6x)\cos(5x)}{-\left(1-x\right)}\,dx$ | $\int  -\left(-\frac{-\left(3-x\right)\cos(6x)\cos(5x)}{-\left(3-x\right)}\right)\,dx$ | $\int  \frac{2\left(x+1\right)\left(\cos(6x)\cos(5x)+\left(-x-2\right)\right)-\left(-x-2\right)}{2\left(x+1\right)}+4-4\,dx$ | $\int  \left(\left(-\left(-\left(\left(\cos(6x)\cos(5x)+3\right)-3\right)\right)\right)+3\right)-3\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\tan(x)+C$ | $\tan(x)+C$ | $\tan(x)+C$ | $\tan(x)+C$ | $\tan(x)+C$ |
| **C=4** | $\frac{1}{5}\sin^{5}(x)+C$ | $\frac{1}{5}\sin^{5}(x)+C$ | $\frac{1}{5}\sin^{5}(x)+C$ | $\frac{1}{5}\sin^{5}(x)+C$ | $\frac{1}{5}\sin^{5}(x)+C$ |
| **C=8** | $\tan(x)-x+C$ | $\tan(x)-x+C$ | $\tan(x)-x+C$ | $\tan(x)-x+C$ | $\tan(x)-x+C$ |
| **C=12** | $\frac{x}{8}-\frac{1}{32}\sin(4x)+C$ | $\frac{x}{8}-\frac{1}{32}\sin(4x)+C$ | $\frac{x}{8}-\frac{1}{32}\sin(4x)+C$ | $\frac{x}{8}-\frac{1}{32}\sin(4x)+C$ | $\frac{x}{8}-\frac{1}{32}\sin(4x)+C$ |
| **C=16** | $\frac{1}{3}\tan^{3}(x)-\tan(x)+x+C$ | $\frac{1}{3}\tan^{3}(x)-\tan(x)+x+C$ | $\frac{1}{3}\tan^{3}(x)-\tan(x)+x+C$ | $\frac{1}{3}\tan^{3}(x)-\tan(x)+x+C$ | $\frac{1}{3}\tan^{3}(x)-\tan(x)+x+C$ |
| **C=20** | $\tan(x)-x+C$ | $\tan(x)-x+C$ | $\tan(x)-x+C$ | $\tan(x)-x+C$ | $\tan(x)-x+C$ |
| **C=25** | $\frac{1}{22}\sin(11x)+\frac{1}{2}\sin(1x)+C$ | $\frac{1}{22}\sin(11x)+\frac{1}{2}\sin(1x)+C$ | $\frac{1}{22}\sin(11x)+\frac{1}{2}\sin(1x)+C$ | $\frac{1}{22}\sin(11x)+\frac{1}{2}\sin(1x)+C$ | $\frac{1}{22}\sin(11x)+\frac{1}{2}\sin(1x)+C$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int \sec^{2}(x)\,dx$
- Answer: $\tan(x)+C$
- From: `form:basic_sec2` · `conceptual:trig` · `allow:trig`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int  \frac{-\left(3+x\right)\sec^{2}(x)}{-\left(3+x\right)}\,dx$
- Answer: $\tan(x)+C$
- From: `form:basic_sec2` · `conceptual:trig` · `prereq:cancel_quot_bait` · `allow:trig` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int  \left(\left(-\left(-\sec^{2}(x)\right)\right)+6\right)-6\,dx$
- Answer: $\tan(x)+C$
- From: `form:basic_sec2` · `conceptual:trig` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `effort:double_neg` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int  -\left(-\left(\left(\frac{-\left(2+x\right)\sec^{2}(x)}{-\left(2+x\right)}+5\right)-5\right)\right)\,dx$
- Answer: $\tan(x)+C$
- From: `form:basic_sec2` · `conceptual:trig` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `prereq:cancel_quot_bait` · `effort:add_cancel_const`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int  \frac{-\left(2+x\right)\left(-\left(-\sec^{2}(x)\right)\right)}{-\left(2+x\right)}+\left(3x+2\right)-\left(3x+2\right)\,dx$
- Answer: $\tan(x)+C$
- From: `form:basic_sec2` · `conceptual:trig` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `effort:double_neg` · `prereq:cancel_quot_bait`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int \sin^{4}(x)\cos(x)\,dx$
- Answer: $\frac{1}{5}\sin^{5}(x)+C$
- From: `form:sin_j_cos` · `conceptual:trig+u_sub` · `allow:trig` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25 · shortfall=0.5

### C=4 · S=4

- Prompt: $\int  \left(\sin^{4}(x)\cos(x)+\left(3x-1\right)\right)-\left(3x-1\right)\,dx$
- Answer: $\frac{1}{5}\sin^{5}(x)+C$
- From: `form:sin_j_cos` · `conceptual:trig+u_sub` · `effort:add_cancel_linear` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\int  -\left(-\frac{4\left(x+1\right)\sin^{4}(x)\cos(x)}{4\left(x+1\right)}\right)\,dx$
- Answer: $\frac{1}{5}\sin^{5}(x)+C$
- From: `form:sin_j_cos` · `conceptual:trig+u_sub` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:double_neg`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\int  \left(\left(\frac{-\left(1-x\right)\sin^{4}(x)\cos(x)}{-\left(1-x\right)}+\left(-x+2\right)\right)-\left(-x+2\right)+\left(3x+3\right)\right)-\left(3x+3\right)\,dx$
- Answer: $\frac{1}{5}\sin^{5}(x)+C$
- From: `form:sin_j_cos` · `conceptual:trig+u_sub` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\int  \left(\frac{3\left(x+3\right)\left(\sin^{4}(x)\cos(x)+3-3\right)}{3\left(x+3\right)}+\left(-2x\right)\right)-\left(-2x\right)\,dx$
- Answer: $\frac{1}{5}\sin^{5}(x)+C$
- From: `form:sin_j_cos` · `conceptual:trig+u_sub` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\int \tan^{2}(x)\,dx$
- Answer: $\tan(x)-x+C$
- From: `form:tan2` · `conceptual:trig` · `allow:trig`
- Flags: C=8 · S=0 · amax=25 · shortfall=4.5

### C=8 · S=4

- Prompt: $\int  \left(\tan^{2}(x)+4\right)-4\,dx$
- Answer: $\tan(x)-x+C$
- From: `form:tan2` · `conceptual:trig` · `effort:add_cancel_const` · `allow:trig` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=8 · S=4 · amax=25 · shortfall=3.5

### C=8 · S=8

- Prompt: $\int  -\left(-\frac{\left(x+2\right)\tan^{2}(x)}{x+2}\right)\,dx$
- Answer: $\tan(x)-x+C$
- From: `form:tan2` · `conceptual:trig` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=8 · S=8 · amax=25 · shortfall=2.5

### C=8 · S=16

- Prompt: $\int  \left(\left(-\left(-\frac{\left(x-2\right)\tan^{2}(x)}{x-2}\right)\right)+\left(3x+3\right)\right)-\left(3x+3\right)\,dx$
- Answer: $\tan(x)-x+C$
- From: `form:tan2` · `conceptual:trig` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `prereq:cancel_quot_bait` · `effort:double_neg`
- Flags: C=8 · S=16 · amax=25 · shortfall=1.5

### C=8 · S=32

- Prompt: $\int  \left(\left(\left(-\left(-\tan^{2}(x)\right)\right)+4-4\right)+6\right)-6\,dx$
- Answer: $\tan(x)-x+C$
- From: `form:tan2` · `conceptual:trig` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `effort:double_neg` · `effort:add_cancel_const` · `effort:add_cancel_const`
- Flags: C=8 · S=32 · amax=25 · shortfall=1.5

### C=12 · S=0

- Prompt: $\int \sin^{2}(x)\cos^{2}(x)\,dx$
- Answer: $\frac{x}{8}-\frac{1}{32}\sin(4x)+C$
- From: `form:sin_cos_both_even` · `conceptual:trig` · `allow:trig` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=8.5

### C=12 · S=4

- Prompt: $\int  \frac{-\left(1+x\right)\sin^{2}(x)\cos^{2}(x)}{-\left(1+x\right)}\,dx$
- Answer: $\frac{x}{8}-\frac{1}{32}\sin(4x)+C$
- From: `form:sin_cos_both_even` · `conceptual:trig` · `prereq:cancel_quot_bait` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=12 · S=4 · amax=25 · shortfall=7.5

### C=12 · S=8

- Prompt: $\int  \left(\frac{4\left(x+2\right)\sin^{2}(x)\cos^{2}(x)}{4\left(x+2\right)}+\left(2x-1\right)\right)-\left(2x-1\right)\,dx$
- Answer: $\frac{x}{8}-\frac{1}{32}\sin(4x)+C$
- From: `form:sin_cos_both_even` · `conceptual:trig` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear`
- Flags: C=12 · S=8 · amax=25 · shortfall=6.5

### C=12 · S=16

- Prompt: $\int  -\left(-\frac{\left(x+3\right)\left(\sin^{2}(x)\cos^{2}(x)+5-5\right)}{x+3}\right)\,dx$
- Answer: $\frac{x}{8}-\frac{1}{32}\sin(4x)+C$
- From: `form:sin_cos_both_even` · `conceptual:trig` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=12 · S=16 · amax=25 · shortfall=5.5

### C=12 · S=32

- Prompt: $\int  \frac{\left(x+2\right)\left(\left(\left(-\left(-\sin^{2}(x)\cos^{2}(x)\right)\right)+1\right)-1\right)}{x+2}\,dx$
- Answer: $\frac{x}{8}-\frac{1}{32}\sin(4x)+C$
- From: `form:sin_cos_both_even` · `conceptual:trig` · `effort:double_neg` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=12 · S=32 · amax=25 · shortfall=5.5

### C=16 · S=0

- Prompt: $\int \tan^{4}(x)\,dx$
- Answer: $\frac{1}{3}\tan^{3}(x)-\tan(x)+x+C$
- From: `form:tan_even_reduction` · `conceptual:trig` · `allow:trig` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=12.5

### C=16 · S=4

- Prompt: $\int  \left(\tan^{4}(x)+\left(3x-1\right)\right)-\left(3x-1\right)\,dx$
- Answer: $\frac{1}{3}\tan^{3}(x)-\tan(x)+x+C$
- From: `form:tan_even_reduction` · `conceptual:trig` · `effort:add_cancel_linear` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=16 · S=4 · amax=25 · shortfall=11.5

### C=16 · S=8

- Prompt: $\int  \frac{\left(x-3\right)\left(-\left(-\tan^{4}(x)\right)\right)}{x-3}\,dx$
- Answer: $\frac{1}{3}\tan^{3}(x)-\tan(x)+x+C$
- From: `form:tan_even_reduction` · `conceptual:trig` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `answer:unkind_or_messy` · `effort:double_neg` · `prereq:cancel_quot_bait`
- Flags: C=16 · S=8 · amax=25 · shortfall=10.5

### C=16 · S=16

- Prompt: $\int  \left(\left(\left(\tan^{4}(x)+\left(3x-2\right)-\left(3x-2\right)\right)+2\right)-2\right)+3-3\,dx$
- Answer: $\frac{1}{3}\tan^{3}(x)-\tan(x)+x+C$
- From: `form:tan_even_reduction` · `conceptual:trig` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear` · `effort:add_cancel_const`
- Flags: C=16 · S=16 · amax=25 · shortfall=9.5

### C=16 · S=32

- Prompt: $\int  -\left(-\left(\left(\left(\tan^{4}(x)+\left(x\right)\right)-\left(x\right)+3\right)-3\right)\right)\,dx$
- Answer: $\frac{1}{3}\tan^{3}(x)-\tan(x)+x+C$
- From: `form:tan_even_reduction` · `conceptual:trig` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=16 · S=32 · amax=25 · shortfall=9.5

### C=20 · S=0

- Prompt: $\int \tan^{2}(x)\,dx$
- Answer: $\tan(x)-x+C$
- From: `form:tan2` · `conceptual:trig` · `allow:trig`
- Flags: C=20 · S=0 · amax=25 · shortfall=16.5

### C=20 · S=4

- Prompt: $\int  \left(\tan^{2}(x)+\left(x\right)\right)-\left(x\right)\,dx$
- Answer: $\tan(x)-x+C$
- From: `form:tan2` · `conceptual:trig` · `effort:add_cancel_linear` · `allow:trig` · `effort:add_cancel_linear` · `effort:spec_answer_preserved`
- Flags: C=20 · S=4 · amax=25 · shortfall=15.5

### C=20 · S=8

- Prompt: $\int  \frac{3\left(x+2\right)\left(-\left(-\tan^{2}(x)\right)\right)}{3\left(x+2\right)}\,dx$
- Answer: $\tan(x)-x+C$
- From: `form:tan2` · `conceptual:trig` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=20 · S=8 · amax=25 · shortfall=14.5

### C=20 · S=16

- Prompt: $\int  \left(-\left(-\frac{-\left(1-x\right)\tan^{2}(x)}{-\left(1-x\right)}\right)\right)+\left(-2x+3\right)-\left(-2x+3\right)\,dx$
- Answer: $\tan(x)-x+C$
- From: `form:tan2` · `conceptual:trig` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `prereq:cancel_quot_bait` · `effort:double_neg`
- Flags: C=20 · S=16 · amax=25 · shortfall=13.5

### C=20 · S=32

- Prompt: $\int  \frac{-\left(1+x\right)\left(\left(\tan^{2}(x)+\left(3x+1\right)\right)-\left(3x+1\right)+1-1\right)}{-\left(1+x\right)}\,dx$
- Answer: $\tan(x)-x+C$
- From: `form:tan2` · `conceptual:trig` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `effort:add_cancel_linear` · `effort:add_cancel_const`
- Flags: C=20 · S=32 · amax=25 · shortfall=13.5

### C=25 · S=0

- Prompt: $\int \cos(6x)\cos(5x)\,dx$
- Answer: $\frac{1}{22}\sin(11x)+\frac{1}{2}\sin(1x)+C$
- From: `form:product_cos_a_cos_b` · `conceptual:trig` · `allow:trig` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=18.5

### C=25 · S=4

- Prompt: $\int  \frac{-\left(1-x\right)\cos(6x)\cos(5x)}{-\left(1-x\right)}\,dx$
- Answer: $\frac{1}{22}\sin(11x)+\frac{1}{2}\sin(1x)+C$
- From: `form:product_cos_a_cos_b` · `conceptual:trig` · `prereq:cancel_quot_bait` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=25 · S=4 · amax=25 · shortfall=17.5

### C=25 · S=8

- Prompt: $\int  -\left(-\frac{-\left(3-x\right)\cos(6x)\cos(5x)}{-\left(3-x\right)}\right)\,dx$
- Answer: $\frac{1}{22}\sin(11x)+\frac{1}{2}\sin(1x)+C$
- From: `form:product_cos_a_cos_b` · `conceptual:trig` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:double_neg`
- Flags: C=25 · S=8 · amax=25 · shortfall=16.5

### C=25 · S=16

- Prompt: $\int  \frac{2\left(x+1\right)\left(\cos(6x)\cos(5x)+\left(-x-2\right)\right)-\left(-x-2\right)}{2\left(x+1\right)}+4-4\,dx$
- Answer: $\frac{1}{22}\sin(11x)+\frac{1}{2}\sin(1x)+C$
- From: `form:product_cos_a_cos_b` · `conceptual:trig` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=25 · S=16 · amax=25 · shortfall=15.5

### C=25 · S=32

- Prompt: $\int  \left(\left(-\left(-\left(\left(\cos(6x)\cos(5x)+3\right)-3\right)\right)\right)+3\right)-3\,dx$
- Answer: $\frac{1}{22}\sin(11x)+\frac{1}{2}\sin(1x)+C$
- From: `form:product_cos_a_cos_b` · `conceptual:trig` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:double_neg`
- Flags: C=25 · S=32 · amax=25 · shortfall=15.5
