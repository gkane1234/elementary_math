# Limits — direct evaluation

**type_id:** `calc_limits_by_direct_evaluation` · **leaf:** `limit_direct_evaluation`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_exp`, `allow_invtrig`, `allow_log`, `allow_roots`, `allow_trig`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\lim_{x \to -5} \left(-2\right)$ | $\lim_{x \to -5} \left(-2\right)+\left(-2x-1\right)-\left(-2x-1\right)$ | $\lim_{x \to -5} \left(\left(\left(-2\right)+2\right)-2\right)+\left(x-1\right)-\left(x-1\right)$ | $\lim_{x \to -5} \left(-\left(-\frac{-\left(3-x\right)\left(-2\right)}{-\left(3-x\right)}\right)\right)+3-3$ | $\lim_{x \to -5} \left(\left(-\left(-\left(\left(-2\right)+\left(-x+3\right)\right)-\left(-x+3\right)\right)\right)+\left(3x+1\right)\right)-\left(3x+1\right)$ |
| **C=4** | $\lim_{x \to 3} \frac{6x^{2} + 6x}{4x - 6}$ | $\lim_{x \to 3} \frac{6x^{2} + 6x}{4x - 6}+3-3$ | $\lim_{x \to 3} \frac{\left(x-3\right)\frac{6x^{2} + 6x}{4x - 6}}{x-3}+6-6$ | $\lim_{x \to 3} \left(\frac{4\left(x-3\right)\left(\left(\frac{6x^{2} + 6x}{4x - 6}+1\right)-1\right)}{4\left(x-3\right)}+3\right)-3$ | $\lim_{x \to 3} \frac{\left(x-2\right)\left(-\left(-\frac{6x^{2} + 6x}{4x - 6}\right)\right)}{x-2}+6-6$ |
| **C=8** | $\lim_{x \to 3} \ln e^{3x}$ | $\lim_{x \to 3} \left(\ln e^{3x}+3\right)-3$ | $\lim_{x \to 3} \left(\ln e^{3x}+5-5\right)+\left(-x-1\right)-\left(-x-1\right)$ | $\lim_{x \to 3} \left(\frac{\left(x-2\right)\left(\ln e^{3x}+4-4\right)}{x-2}+\left(-2x-2\right)\right)-\left(-2x-2\right)$ | $\lim_{x \to 3} \left(\ln e^{3x}+\left(-x+3\right)\right)-\left(-x+3\right)+\left(-2x+2\right)-\left(-2x+2\right)+4-4$ |
| **C=12** | $\lim_{x \to 3} \frac{-x^{2} - 6x}{x + 1}$ | $\lim_{x \to 3} -\left(-\frac{-x^{2} - 6x}{x + 1}\right)$ | $\lim_{x \to 3} \frac{-\left(3-x\right)\left(-\left(-\frac{-x^{2} - 6x}{x + 1}\right)\right)}{-\left(3-x\right)}$ | $\lim_{x \to 3} \left(\left(\left(\left(-\left(-\frac{-x^{2} - 6x}{x + 1}\right)\right)+5\right)-5\right)+3\right)-3$ | $\lim_{x \to 3} -\left(-\frac{\left(x-2\right)\left(\frac{-x^{2} - 6x}{x + 1}+\left(-x+3\right)\right)-\left(-x+3\right)}{x-2}\right)$ |
| **C=16** | $\lim_{x \to -5} \left(e^{\arctan(6x)}e^{\left(7x - 7\right)}\right)$ | $\lim_{x \to -5} \left(e^{\arctan(6x)}e^{\left(7x - 7\right)}\right)$ | $\lim_{x \to -5} \left(e^{\arctan(6x)}e^{\left(7x - 7\right)}\right)$ | $\lim_{x \to -5} \left(e^{\arctan(6x)}e^{\left(7x - 7\right)}\right)$ | $\lim_{x \to -5} \left(e^{\arctan(6x)}e^{\left(7x - 7\right)}\right)$ |
| **C=20** | $\lim_{x \to 6} (2x-1)\sqrt{x+4}$ | $\lim_{x \to 6} \frac{\left(x-3\right)\left((2x-1)\sqrt{x+4}\right)}{x-3}$ | $\lim_{x \to 6} \frac{-\left(1-x\right)\left(-\left(-\left((2x-1)\sqrt{x+4}\right)\right)\right)}{-\left(1-x\right)}$ | $\lim_{x \to 6} \left(\left(\left(\left(\left((2x-1)\sqrt{x+4}\right)+5\right)-5\right)+\left(-2x+3\right)\right)-\left(-2x+3\right)+2\right)-2$ | $\lim_{x \to 6} \left(\left(-\left(-\left((2x-1)\sqrt{x+4}\right)\right)\right)+\left(-x+1\right)-\left(-x+1\right)+\left(3x-2\right)\right)-\left(3x-2\right)$ |
| **C=25** | $\lim_{x \to 0} \frac{\sin(2x)}{x}$ | $\lim_{x \to 0} -\left(-\frac{\sin(2x)}{x}\right)$ | $\lim_{x \to 0} \frac{\left(x+1\right)\left(\left(\frac{\sin(2x)}{x}+4\right)-4\right)}{x+1}$ | $\lim_{x \to 0} \left(\left(\frac{\sin(2x)}{x}+\left(3x-1\right)-\left(3x-1\right)\right)+6-6\right)+\left(x+2\right)-\left(x+2\right)$ | $\lim_{x \to 0} -\left(-\left(\left(\frac{-\left(1-x\right)\frac{\sin(2x)}{x}}{-\left(1-x\right)}+4\right)-4\right)\right)$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $-2$ | $-2$ | $-2$ | $-2$ | $-2$ |
| **C=4** | $12$ | $12$ | $12$ | $12$ | $12$ |
| **C=8** | $9$ | $9$ | $9$ | $9$ | $9$ |
| **C=12** | $-\frac{27}{4}$ | $-\frac{27}{4}$ | $-\frac{27}{4}$ | $-\frac{27}{4}$ | $-\frac{27}{4}$ |
| **C=16** | $0$ | $0$ | $0$ | $0$ | $0$ |
| **C=20** | $11\sqrt{10}$ | $11\sqrt{10}$ | $11\sqrt{10}$ | $11\sqrt{10}$ | $11\sqrt{10}$ |
| **C=25** | $2$ | $2$ | $2$ | $2$ | $2$ |

## Cell detail

### C=0 · S=0

- Prompt: $\lim_{x \to -5} \left(-2\right)$
- Answer: $-2$
- From: `form:poly_direct` · `conceptual:direct_eval` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\lim_{x \to -5} \left(-2\right)+\left(-2x-1\right)-\left(-2x-1\right)$
- Answer: $-2$
- From: `form:poly_direct` · `conceptual:direct_eval` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\lim_{x \to -5} \left(\left(\left(-2\right)+2\right)-2\right)+\left(x-1\right)-\left(x-1\right)$
- Answer: $-2$
- From: `form:poly_direct` · `conceptual:direct_eval` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\lim_{x \to -5} \left(-\left(-\frac{-\left(3-x\right)\left(-2\right)}{-\left(3-x\right)}\right)\right)+3-3$
- Answer: $-2$
- From: `form:poly_direct` · `conceptual:direct_eval` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\lim_{x \to -5} \left(\left(-\left(-\left(\left(-2\right)+\left(-x+3\right)\right)-\left(-x+3\right)\right)\right)+\left(3x+1\right)\right)-\left(3x+1\right)$
- Answer: $-2$
- From: `form:poly_direct` · `conceptual:direct_eval` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\lim_{x \to 3} \frac{6x^{2} + 6x}{4x - 6}$
- Answer: $12$
- From: `form:rational_direct` · `conceptual:direct_eval` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=4 · S=0 · amax=25 · shortfall=2

### C=4 · S=4

- Prompt: $\lim_{x \to 3} \frac{6x^{2} + 6x}{4x - 6}+3-3$
- Answer: $12$
- From: `form:rational_direct` · `conceptual:direct_eval` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=4 · S=4 · amax=25 · shortfall=1

### C=4 · S=8

- Prompt: $\lim_{x \to 3} \frac{\left(x-3\right)\frac{6x^{2} + 6x}{4x - 6}}{x-3}+6-6$
- Answer: $12$
- From: `form:rational_direct` · `conceptual:direct_eval` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\lim_{x \to 3} \left(\frac{4\left(x-3\right)\left(\left(\frac{6x^{2} + 6x}{4x - 6}+1\right)-1\right)}{4\left(x-3\right)}+3\right)-3$
- Answer: $12$
- From: `form:rational_direct` · `conceptual:direct_eval` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\lim_{x \to 3} \frac{\left(x-2\right)\left(-\left(-\frac{6x^{2} + 6x}{4x - 6}\right)\right)}{x-2}+6-6$
- Answer: $12$
- From: `form:rational_direct` · `conceptual:direct_eval` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\lim_{x \to 3} \ln e^{3x}$
- Answer: $9$
- From: `form:direct_ln` · `conceptual:direct_eval` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=8 · S=0 · amax=25 · shortfall=1

### C=8 · S=4

- Prompt: $\lim_{x \to 3} \left(\ln e^{3x}+3\right)-3$
- Answer: $9$
- From: `form:direct_ln` · `conceptual:direct_eval` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\lim_{x \to 3} \left(\ln e^{3x}+5-5\right)+\left(-x-1\right)-\left(-x-1\right)$
- Answer: $9$
- From: `form:direct_ln` · `conceptual:direct_eval` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\lim_{x \to 3} \left(\frac{\left(x-2\right)\left(\ln e^{3x}+4-4\right)}{x-2}+\left(-2x-2\right)\right)-\left(-2x-2\right)$
- Answer: $9$
- From: `form:direct_ln` · `conceptual:direct_eval` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\lim_{x \to 3} \left(\ln e^{3x}+\left(-x+3\right)\right)-\left(-x+3\right)+\left(-2x+2\right)-\left(-2x+2\right)+4-4$
- Answer: $9$
- From: `form:direct_ln` · `conceptual:direct_eval` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\lim_{x \to 3} \frac{-x^{2} - 6x}{x + 1}$
- Answer: $-\frac{27}{4}$
- From: `form:rational_direct` · `conceptual:direct_eval` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=10

### C=12 · S=4

- Prompt: $\lim_{x \to 3} -\left(-\frac{-x^{2} - 6x}{x + 1}\right)$
- Answer: $-\frac{27}{4}$
- From: `form:rational_direct` · `conceptual:direct_eval` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=12 · S=4 · amax=25 · shortfall=9

### C=12 · S=8

- Prompt: $\lim_{x \to 3} \frac{-\left(3-x\right)\left(-\left(-\frac{-x^{2} - 6x}{x + 1}\right)\right)}{-\left(3-x\right)}$
- Answer: $-\frac{27}{4}$
- From: `form:rational_direct` · `conceptual:direct_eval` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=12 · S=8 · amax=25 · shortfall=8

### C=12 · S=16

- Prompt: $\lim_{x \to 3} \left(\left(\left(\left(-\left(-\frac{-x^{2} - 6x}{x + 1}\right)\right)+5\right)-5\right)+3\right)-3$
- Answer: $-\frac{27}{4}$
- From: `form:rational_direct` · `conceptual:direct_eval` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=12 · S=16 · amax=25 · shortfall=7

### C=12 · S=32

- Prompt: $\lim_{x \to 3} -\left(-\frac{\left(x-2\right)\left(\frac{-x^{2} - 6x}{x + 1}+\left(-x+3\right)\right)-\left(-x+3\right)}{x-2}\right)$
- Answer: $-\frac{27}{4}$
- From: `form:rational_direct` · `conceptual:direct_eval` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=32 · amax=25 · shortfall=7

### C=16 · S=0

- Prompt: $\lim_{x \to -5} \left(e^{\arctan(6x)}e^{\left(7x - 7\right)}\right)$
- Answer: $0$
- From: `form:direct_exp` · `conceptual:direct_eval` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=16 · S=0 · amax=25 · shortfall=5.5

### C=16 · S=4

- Prompt: $\lim_{x \to -5} \left(e^{\arctan(6x)}e^{\left(7x - 7\right)}\right)$
- Answer: $0$
- From: `form:direct_exp` · `conceptual:direct_eval` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=16 · S=4 · amax=25 · shortfall=5.5

### C=16 · S=8

- Prompt: $\lim_{x \to -5} \left(e^{\arctan(6x)}e^{\left(7x - 7\right)}\right)$
- Answer: $0$
- From: `form:direct_exp` · `conceptual:direct_eval` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=16 · S=8 · amax=25 · shortfall=5.5

### C=16 · S=16

- Prompt: $\lim_{x \to -5} \left(e^{\arctan(6x)}e^{\left(7x - 7\right)}\right)$
- Answer: $0$
- From: `form:direct_exp` · `conceptual:direct_eval` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=16 · S=16 · amax=25 · shortfall=5.5

### C=16 · S=32

- Prompt: $\lim_{x \to -5} \left(e^{\arctan(6x)}e^{\left(7x - 7\right)}\right)$
- Answer: $0$
- From: `form:direct_exp` · `conceptual:direct_eval` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `effort:spec_high`
- Flags: C=16 · S=32 · amax=25 · shortfall=5.5

### C=20 · S=0

- Prompt: $\lim_{x \to 6} (2x-1)\sqrt{x+4}$
- Answer: $11\sqrt{10}$
- From: `form:direct_sqrt` · `conceptual:direct_eval` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=13

### C=20 · S=4

- Prompt: $\lim_{x \to 6} \frac{\left(x-3\right)\left((2x-1)\sqrt{x+4}\right)}{x-3}$
- Answer: $11\sqrt{10}$
- From: `form:direct_sqrt` · `conceptual:direct_eval` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=20 · S=4 · amax=25 · shortfall=12

### C=20 · S=8

- Prompt: $\lim_{x \to 6} \frac{-\left(1-x\right)\left(-\left(-\left((2x-1)\sqrt{x+4}\right)\right)\right)}{-\left(1-x\right)}$
- Answer: $11\sqrt{10}$
- From: `form:direct_sqrt` · `conceptual:direct_eval` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=20 · S=8 · amax=25 · shortfall=11

### C=20 · S=16

- Prompt: $\lim_{x \to 6} \left(\left(\left(\left(\left((2x-1)\sqrt{x+4}\right)+5\right)-5\right)+\left(-2x+3\right)\right)-\left(-2x+3\right)+2\right)-2$
- Answer: $11\sqrt{10}$
- From: `form:direct_sqrt` · `conceptual:direct_eval` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=20 · S=16 · amax=25 · shortfall=10

### C=20 · S=32

- Prompt: $\lim_{x \to 6} \left(\left(-\left(-\left((2x-1)\sqrt{x+4}\right)\right)\right)+\left(-x+1\right)-\left(-x+1\right)+\left(3x-2\right)\right)-\left(3x-2\right)$
- Answer: $11\sqrt{10}$
- From: `form:direct_sqrt` · `conceptual:direct_eval` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=20 · S=32 · amax=25 · shortfall=10

### C=25 · S=0

- Prompt: $\lim_{x \to 0} \frac{\sin(2x)}{x}$
- Answer: $2$
- From: `form:squeeze_sin_over_x` · `conceptual:squeeze_trig` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=0 · amax=25 · shortfall=15.5

### C=25 · S=4

- Prompt: $\lim_{x \to 0} -\left(-\frac{\sin(2x)}{x}\right)$
- Answer: $2$
- From: `form:squeeze_sin_over_x` · `conceptual:squeeze_trig` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=4 · amax=25 · shortfall=14.5

### C=25 · S=8

- Prompt: $\lim_{x \to 0} \frac{\left(x+1\right)\left(\left(\frac{\sin(2x)}{x}+4\right)-4\right)}{x+1}$
- Answer: $2$
- From: `form:squeeze_sin_over_x` · `conceptual:squeeze_trig` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=25 · S=8 · amax=25 · shortfall=13.5

### C=25 · S=16

- Prompt: $\lim_{x \to 0} \left(\left(\frac{\sin(2x)}{x}+\left(3x-1\right)-\left(3x-1\right)\right)+6-6\right)+\left(x+2\right)-\left(x+2\right)$
- Answer: $2$
- From: `form:squeeze_sin_over_x` · `conceptual:squeeze_trig` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=25 · S=16 · amax=25 · shortfall=12.5

### C=25 · S=32

- Prompt: $\lim_{x \to 0} -\left(-\left(\left(\frac{-\left(1-x\right)\frac{\sin(2x)}{x}}{-\left(1-x\right)}+4\right)-4\right)\right)$
- Answer: $2$
- From: `form:squeeze_sin_over_x` · `conceptual:squeeze_trig` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=32 · amax=25 · shortfall=12.5
