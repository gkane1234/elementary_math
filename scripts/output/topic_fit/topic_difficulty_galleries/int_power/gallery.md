# Integrals — power rule

**type_id:** `calc_indef_int_power_rule` · **leaf:** `integral_power_rule`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_roots`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\int 3x \, dx$ | $\int  \frac{3\left(x-1\right)3x}{3\left(x-1\right)}\, dx$ | $\int  -\left(-\left(2x + x\right)\right)\, dx$ | $\int  \left(\left(\frac{2\left(x-1\right)3x}{2\left(x-1\right)}+\left(-x+2\right)\right)-\left(-x+2\right)+\left(2x-1\right)\right)-\left(2x-1\right)\, dx$ | $\int  \frac{\left(x-2\right)\left(\left(3x+2-2\right)+\left(x\right)\right)-\left(x\right)}{x-2}\, dx$ |
| **C=4** | $\int \sqrt{x}\,dx$ | $\int  \left(\sqrt{x}+2\right)-2\,dx$ | $\int  \left(\left(\left(\sqrt{x}+4\right)-4\right)+1\right)-1\,dx$ | $\int  \left(-\left(-\frac{-\left(3-x\right)\sqrt{x}}{-\left(3-x\right)}\right)\right)+1-1\,dx$ | $\int  \left(\left(-\left(-\frac{2\left(x-1\right)\sqrt{x}}{2\left(x-1\right)}\right)\right)+1\right)-1\,dx$ |
| **C=8** | $\int \frac{1}{\sqrt{x}}\,dx$ | $\int  -\left(-\frac{1}{\sqrt{x}}\right)\,dx$ | $\int  \left(\left(-\left(-\frac{1}{\sqrt{x}}\right)\right)+1\right)-1\,dx$ | $\int  \left(\left(\left(\left(-\left(-\frac{1}{\sqrt{x}}\right)\right)+3\right)-3\right)+6\right)-6\,dx$ | $\int  -\left(-\frac{3\left(x-1\right)\left(\frac{1}{\sqrt{x}}+\left(-2x-1\right)\right)-\left(-2x-1\right)}{3\left(x-1\right)}\right)\,dx$ |
| **C=12** | $\int -3x^{5} \, dx$ | $\int  3\left(-x^{5}\right)\, dx$ | $\int  -\left(-\left(\left(-3x^{5}\right)+6-6\right)\right)\, dx$ | $\int  \frac{\left(x-3\right)\left(\left(\left(\left(\left(-3x^{5}\right)+6\right)-6\right)+3\right)-3\right)}{x-3}\, dx$ | $\int  -\left(-\frac{-\left(2-x\right)\left(3\left(-x^{5}\right)\right)}{-\left(2-x\right)}\right)\, dx$ |
| **C=16** | $\int \frac{4}{x^{2}}\,dx$ | $\int  \frac{4\left(x-2\right)\frac{4}{x^{2}}}{4\left(x-2\right)}\,dx$ | $\int  -\left(-\left(\left(\frac{4}{x^{2}}+4\right)-4\right)\right)\,dx$ | $\int  \left(\frac{4\left(x+2\right)\frac{4}{x^{2}}}{4\left(x+2\right)}+\left(-x\right)-\left(-x\right)\right)+1-1\,dx$ | $\int  \left(\left(-\left(-\frac{4}{x^{2}}\right)\right)+6-6\right)+\left(x+1\right)-\left(x+1\right)\,dx$ |
| **C=20** | $\int \frac{1}{x^{3}}\,dx$ | $\int  -\left(-\frac{1}{x^{3}}\right)\,dx$ | $\int  -\left(-\left(\left(\frac{1}{x^{3}}+3\right)-3\right)\right)\,dx$ | $\int  \left(\left(\left(\left(\frac{1}{x^{3}}+3\right)-3\right)+\left(-2x+2\right)\right)-\left(-2x+2\right)+5\right)-5\,dx$ | $\int  \left(\left(\frac{2\left(x-1\right)\frac{1}{x^{3}}}{2\left(x-1\right)}+2\right)-2\right)+\left(2x+2\right)-\left(2x+2\right)\,dx$ |
| **C=25** | $\int x\sqrt{x}\,dx$ | $\int  \frac{\left(x-2\right)x\sqrt{x}}{x-2}\,dx$ | $\int  -\left(-\frac{\left(x+3\right)x\sqrt{x}}{x+3}\right)\,dx$ | $\int  -\left(-\left(\frac{4\left(x-3\right)x\sqrt{x}}{4\left(x-3\right)}+\left(2x+3\right)-\left(2x+3\right)\right)\right)\,dx$ | $\int  \frac{-\left(3+x\right)\left(x\sqrt{x}+5-5\right)}{-\left(3+x\right)}+6-6\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\frac{3}{2}x^{2}+C$ | $\frac{3}{2}x^{2}+C$ | $\frac{3}{2}x^{2}+C$ | $\frac{3}{2}x^{2}+C$ | $\frac{3}{2}x^{2}+C$ |
| **C=4** | $\frac{2}{3}x^{\frac{3}{2}}+C$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ |
| **C=8** | $2\sqrt{x}+C$ | $2\sqrt{x}+C$ | $2\sqrt{x}+C$ | $2\sqrt{x}+C$ | $2\sqrt{x}+C$ |
| **C=12** | $-\frac{1}{2}x^{6}+C$ | $-\frac{1}{2}x^{6}+C$ | $-\frac{1}{2}x^{6}+C$ | $-\frac{1}{2}x^{6}+C$ | $-\frac{1}{2}x^{6}+C$ |
| **C=16** | $-4x^{-1}+C$ | $-4x^{-1}+C$ | $-4x^{-1}+C$ | $-4x^{-1}+C$ | $-4x^{-1}+C$ |
| **C=20** | $-\frac{1}{2}x^{-2}+C$ | $-\frac{1}{2}x^{-2}+C$ | $-\frac{1}{2}x^{-2}+C$ | $-\frac{1}{2}x^{-2}+C$ | $-\frac{1}{2}x^{-2}+C$ |
| **C=25** | $\frac{2}{5}x^{\frac{5}{2}}+C$ | $\frac{2}{5}x^{\frac{5}{2}}+C$ | $\frac{2}{5}x^{\frac{5}{2}}+C$ | $\frac{2}{5}x^{\frac{5}{2}}+C$ | $\frac{2}{5}x^{\frac{5}{2}}+C$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int 3x \, dx$
- Answer: $\frac{3}{2}x^{2}+C$
- From: `form:poly_sum` · `conceptual:power` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int  \frac{3\left(x-1\right)3x}{3\left(x-1\right)}\, dx$
- Answer: $\frac{3}{2}x^{2}+C$
- From: `form:poly_sum` · `conceptual:power` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int  -\left(-\left(2x + x\right)\right)\, dx$
- Answer: $\frac{3}{2}x^{2}+C$
- From: `form:poly_sum` · `conceptual:power` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `effort:poly_inflate` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int  \left(\left(\frac{2\left(x-1\right)3x}{2\left(x-1\right)}+\left(-x+2\right)\right)-\left(-x+2\right)+\left(2x-1\right)\right)-\left(2x-1\right)\, dx$
- Answer: $\frac{3}{2}x^{2}+C$
- From: `form:poly_sum` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int  \frac{\left(x-2\right)\left(\left(3x+2-2\right)+\left(x\right)\right)-\left(x\right)}{x-2}\, dx$
- Answer: $\frac{3}{2}x^{2}+C$
- From: `form:poly_sum` · `conceptual:power` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int \sqrt{x}\,dx$
- Answer: $\frac{2}{3}x^{\frac{3}{2}}+C$
- From: `form:sqrt_x` · `conceptual:power` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25 · shortfall=3

### C=4 · S=4

- Prompt: $\int  \left(\sqrt{x}+2\right)-2\,dx$
- Answer: $\frac{2}{3}x^{\frac{3}{2}}+C$
- From: `form:sqrt_x` · `conceptual:power` · `effort:add_cancel_const` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=4 · S=4 · amax=25 · shortfall=2

### C=4 · S=8

- Prompt: $\int  \left(\left(\left(\sqrt{x}+4\right)-4\right)+1\right)-1\,dx$
- Answer: $\frac{2}{3}x^{\frac{3}{2}}+C$
- From: `form:sqrt_x` · `conceptual:power` · `effort:add_cancel_const` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:add_cancel_const` · `effort:spec_answer_preserved`
- Flags: C=4 · S=8 · amax=25 · shortfall=1

### C=4 · S=16

- Prompt: $\int  \left(-\left(-\frac{-\left(3-x\right)\sqrt{x}}{-\left(3-x\right)}\right)\right)+1-1\,dx$
- Answer: $\frac{2}{3}x^{\frac{3}{2}}+C$
- From: `form:sqrt_x` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\int  \left(\left(-\left(-\frac{2\left(x-1\right)\sqrt{x}}{2\left(x-1\right)}\right)\right)+1\right)-1\,dx$
- Answer: $\frac{2}{3}x^{\frac{3}{2}}+C$
- From: `form:sqrt_x` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\int \frac{1}{\sqrt{x}}\,dx$
- Answer: $2\sqrt{x}+C$
- From: `form:one_over_sqrt_x` · `conceptual:power` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25 · shortfall=6.5

### C=8 · S=4

- Prompt: $\int  -\left(-\frac{1}{\sqrt{x}}\right)\,dx$
- Answer: $2\sqrt{x}+C$
- From: `form:one_over_sqrt_x` · `conceptual:power` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=8 · S=4 · amax=25 · shortfall=5.5

### C=8 · S=8

- Prompt: $\int  \left(\left(-\left(-\frac{1}{\sqrt{x}}\right)\right)+1\right)-1\,dx$
- Answer: $2\sqrt{x}+C$
- From: `form:one_over_sqrt_x` · `conceptual:power` · `effort:double_neg` · `effort:add_cancel_const` · `allow:roots` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:add_cancel_const`
- Flags: C=8 · S=8 · amax=25 · shortfall=4.5

### C=8 · S=16

- Prompt: $\int  \left(\left(\left(\left(-\left(-\frac{1}{\sqrt{x}}\right)\right)+3\right)-3\right)+6\right)-6\,dx$
- Answer: $2\sqrt{x}+C$
- From: `form:one_over_sqrt_x` · `conceptual:power` · `effort:double_neg` · `effort:add_cancel_const` · `allow:roots` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:add_cancel_const`
- Flags: C=8 · S=16 · amax=25 · shortfall=3.5

### C=8 · S=32

- Prompt: $\int  -\left(-\frac{3\left(x-1\right)\left(\frac{1}{\sqrt{x}}+\left(-2x-1\right)\right)-\left(-2x-1\right)}{3\left(x-1\right)}\right)\,dx$
- Answer: $2\sqrt{x}+C$
- From: `form:one_over_sqrt_x` · `conceptual:power` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=8 · S=32 · amax=25 · shortfall=3.5

### C=12 · S=0

- Prompt: $\int -3x^{5} \, dx$
- Answer: $-\frac{1}{2}x^{6}+C$
- From: `form:poly_sum` · `conceptual:power` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=11.5

### C=12 · S=4

- Prompt: $\int  3\left(-x^{5}\right)\, dx$
- Answer: $-\frac{1}{2}x^{6}+C$
- From: `form:poly_sum` · `conceptual:power` · `allow:roots` · `answer:unkind_or_messy` · `effort:poly_inflate` · `effort:spec_answer_preserved`
- Flags: C=12 · S=4 · amax=25 · shortfall=10.5

### C=12 · S=8

- Prompt: $\int  -\left(-\left(\left(-3x^{5}\right)+6-6\right)\right)\, dx$
- Answer: $-\frac{1}{2}x^{6}+C$
- From: `form:poly_sum` · `conceptual:power` · `effort:add_cancel_const` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:double_neg`
- Flags: C=12 · S=8 · amax=25 · shortfall=9.5

### C=12 · S=16

- Prompt: $\int  \frac{\left(x-3\right)\left(\left(\left(\left(\left(-3x^{5}\right)+6\right)-6\right)+3\right)-3\right)}{x-3}\, dx$
- Answer: $-\frac{1}{2}x^{6}+C$
- From: `form:poly_sum` · `conceptual:power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:add_cancel_const`
- Flags: C=12 · S=16 · amax=25 · shortfall=8.5

### C=12 · S=32

- Prompt: $\int  -\left(-\frac{-\left(2-x\right)\left(3\left(-x^{5}\right)\right)}{-\left(2-x\right)}\right)\, dx$
- Answer: $-\frac{1}{2}x^{6}+C$
- From: `form:poly_sum` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `effort:poly_inflate` · `prereq:cancel_quot_bait`
- Flags: C=12 · S=32 · amax=25 · shortfall=8.5

### C=16 · S=0

- Prompt: $\int \frac{4}{x^{2}}\,dx$
- Answer: $-4x^{-1}+C$
- From: `form:neg_power` · `conceptual:power` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=14

### C=16 · S=4

- Prompt: $\int  \frac{4\left(x-2\right)\frac{4}{x^{2}}}{4\left(x-2\right)}\,dx$
- Answer: $-4x^{-1}+C$
- From: `form:neg_power` · `conceptual:power` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=16 · S=4 · amax=25 · shortfall=13

### C=16 · S=8

- Prompt: $\int  -\left(-\left(\left(\frac{4}{x^{2}}+4\right)-4\right)\right)\,dx$
- Answer: $-4x^{-1}+C$
- From: `form:neg_power` · `conceptual:power` · `effort:add_cancel_const` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:double_neg`
- Flags: C=16 · S=8 · amax=25 · shortfall=12

### C=16 · S=16

- Prompt: $\int  \left(\frac{4\left(x+2\right)\frac{4}{x^{2}}}{4\left(x+2\right)}+\left(-x\right)-\left(-x\right)\right)+1-1\,dx$
- Answer: $-4x^{-1}+C$
- From: `form:neg_power` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=16 · S=16 · amax=25 · shortfall=11

### C=16 · S=32

- Prompt: $\int  \left(\left(-\left(-\frac{4}{x^{2}}\right)\right)+6-6\right)+\left(x+1\right)-\left(x+1\right)\,dx$
- Answer: $-4x^{-1}+C$
- From: `form:neg_power` · `conceptual:power` · `effort:double_neg` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:roots` · `answer:unkind_or_messy` · `effort:double_neg`
- Flags: C=16 · S=32 · amax=25 · shortfall=11

### C=20 · S=0

- Prompt: $\int \frac{1}{x^{3}}\,dx$
- Answer: $-\frac{1}{2}x^{-2}+C$
- From: `form:neg_power` · `conceptual:power` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=18

### C=20 · S=4

- Prompt: $\int  -\left(-\frac{1}{x^{3}}\right)\,dx$
- Answer: $-\frac{1}{2}x^{-2}+C$
- From: `form:neg_power` · `conceptual:power` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `effort:double_neg` · `effort:spec_answer_preserved`
- Flags: C=20 · S=4 · amax=25 · shortfall=17

### C=20 · S=8

- Prompt: $\int  -\left(-\left(\left(\frac{1}{x^{3}}+3\right)-3\right)\right)\,dx$
- Answer: $-\frac{1}{2}x^{-2}+C$
- From: `form:neg_power` · `conceptual:power` · `effort:add_cancel_const` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:double_neg`
- Flags: C=20 · S=8 · amax=25 · shortfall=16

### C=20 · S=16

- Prompt: $\int  \left(\left(\left(\left(\frac{1}{x^{3}}+3\right)-3\right)+\left(-2x+2\right)\right)-\left(-2x+2\right)+5\right)-5\,dx$
- Answer: $-\frac{1}{2}x^{-2}+C$
- From: `form:neg_power` · `conceptual:power` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `effort:add_cancel_linear`
- Flags: C=20 · S=16 · amax=25 · shortfall=15

### C=20 · S=32

- Prompt: $\int  \left(\left(\frac{2\left(x-1\right)\frac{1}{x^{3}}}{2\left(x-1\right)}+2\right)-2\right)+\left(2x+2\right)-\left(2x+2\right)\,dx$
- Answer: $-\frac{1}{2}x^{-2}+C$
- From: `form:neg_power` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=20 · S=32 · amax=25 · shortfall=15

### C=25 · S=0

- Prompt: $\int x\sqrt{x}\,dx$
- Answer: $\frac{2}{5}x^{\frac{5}{2}}+C$
- From: `form:x_sqrt_x` · `conceptual:power` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=23

### C=25 · S=4

- Prompt: $\int  \frac{\left(x-2\right)x\sqrt{x}}{x-2}\,dx$
- Answer: $\frac{2}{5}x^{\frac{5}{2}}+C$
- From: `form:x_sqrt_x` · `conceptual:power` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:spec_answer_preserved`
- Flags: C=25 · S=4 · amax=25 · shortfall=22

### C=25 · S=8

- Prompt: $\int  -\left(-\frac{\left(x+3\right)x\sqrt{x}}{x+3}\right)\,dx$
- Answer: $\frac{2}{5}x^{\frac{5}{2}}+C$
- From: `form:x_sqrt_x` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait` · `effort:double_neg`
- Flags: C=25 · S=8 · amax=25 · shortfall=21

### C=25 · S=16

- Prompt: $\int  -\left(-\left(\frac{4\left(x-3\right)x\sqrt{x}}{4\left(x-3\right)}+\left(2x+3\right)-\left(2x+3\right)\right)\right)\,dx$
- Answer: $\frac{2}{5}x^{\frac{5}{2}}+C$
- From: `form:x_sqrt_x` · `conceptual:power` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:roots` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=25 · S=16 · amax=25 · shortfall=20

### C=25 · S=32

- Prompt: $\int  \frac{-\left(3+x\right)\left(x\sqrt{x}+5-5\right)}{-\left(3+x\right)}+6-6\,dx$
- Answer: $\frac{2}{5}x^{\frac{5}{2}}+C$
- From: `form:x_sqrt_x` · `conceptual:power` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:roots` · `answer:unkind_or_messy` · `effort:add_cancel_const` · `prereq:cancel_quot_bait`
- Flags: C=25 · S=32 · amax=25 · shortfall=20
