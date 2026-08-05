# Limits — at infinity

**type_id:** `calc_limits_at_infinity` · **leaf:** `limit_at_infinity`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_exp`, `allow_invtrig`, `allow_log`, `allow_trig`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\lim_{x \to \infty} \frac{-5x - 5}{6x}$ | $\lim_{x \to \infty} \left(\frac{-5x - 5}{6x}+5\right)-5$ | $\lim_{x \to \infty} \frac{\left(x+2\right)\left(\left(\frac{-5x - 5}{6x}+2\right)-2\right)}{x+2}$ | $\lim_{x \to \infty} -\left(-\frac{\left(x+2\right)\left(\frac{-5x - 5}{6x}+5-5\right)}{x+2}\right)$ | $\lim_{x \to \infty} -\left(-\left(\left(\frac{-5x - 5}{6x}+2\right)-2\right)+\left(x-2\right)-\left(x-2\right)\right)$ |
| **C=4** | $\lim_{x \to -\infty} \frac{5x + 4}{x}$ | $\lim_{x \to -\infty} \left(\frac{5x + 4}{x}+\left(2x+3\right)\right)-\left(2x+3\right)$ | $\lim_{x \to -\infty} -\left(-\frac{4\left(x-3\right)\frac{5x + 4}{x}}{4\left(x-3\right)}\right)$ | $\lim_{x \to -\infty} \left(-\left(-\frac{4\left(x-2\right)\frac{5x + 4}{x}}{4\left(x-2\right)}\right)\right)+2-2$ | $\lim_{x \to -\infty} \frac{3\left(x+3\right)\left(\frac{5x + 4}{x}+\left(-x+3\right)\right)-\left(-x+3\right)}{3\left(x+3\right)}+2-2$ |
| **C=8** | $\lim_{x \to -\infty} \frac{-2x + 4}{3}$ | $\lim_{x \to -\infty} \left(\frac{-2x + 4}{3}+\left(3x+1\right)\right)-\left(3x+1\right)$ | $\lim_{x \to -\infty} \left(\left(\frac{-2x + 4}{3}+4\right)-4\right)+5-5$ | $\lim_{x \to -\infty} \left(\frac{3\left(x+1\right)\frac{-2x + 4}{3}}{3\left(x+1\right)}+2-2\right)+\left(3x-1\right)-\left(3x-1\right)$ | $\lim_{x \to -\infty} \left(\frac{\left(x+2\right)\left(\frac{-2x + 4}{3}+\left(-x+1\right)-\left(-x+1\right)\right)}{x+2}+\left(3x-2\right)\right)-\left(3x-2\right)$ |
| **C=12** | $\lim_{x \to -\infty} \arctan(x)$ | $\lim_{x \to -\infty} \left(\arctan(x)+6\right)-6$ | $\lim_{x \to -\infty} \left(\left(\left(\arctan(x)+2\right)-2\right)+\left(3x+2\right)\right)-\left(3x+2\right)$ | $\lim_{x \to -\infty} \left(\left(\frac{-\left(3-x\right)\arctan(x)}{-\left(3-x\right)}+\left(3x-2\right)-\left(3x-2\right)\right)+5\right)-5$ | $\lim_{x \to -\infty} -\left(-\left(\frac{-\left(3-x\right)\arctan(x)}{-\left(3-x\right)}+\left(3x-1\right)-\left(3x-1\right)\right)\right)$ |
| **C=16** | $\lim_{x \to \infty} \frac{\cos(x)}{x^{2}}$ | $\lim_{x \to \infty} \left(\frac{\cos(x)}{x^{2}}+\left(-2x+1\right)\right)-\left(-2x+1\right)$ | $\lim_{x \to \infty} \left(\frac{\cos(x)}{x^{2}}+\left(3x-2\right)-\left(3x-2\right)\right)+\left(2x+1\right)-\left(2x+1\right)$ | $\lim_{x \to \infty} \left(\frac{2\left(x+3\right)\left(-\left(-\frac{\cos(x)}{x^{2}}\right)\right)}{2\left(x+3\right)}+\left(-2x-2\right)\right)-\left(-2x-2\right)$ | $\lim_{x \to \infty} -\left(-\left(\frac{2\left(x-3\right)\frac{\cos(x)}{x^{2}}}{2\left(x-3\right)}+\left(-x+3\right)\right)-\left(-x+3\right)\right)$ |
| **C=20** | $\lim_{x \to -\infty} \frac{\cos(x)}{x^{2}}$ | $\lim_{x \to -\infty} \left(\frac{\cos(x)}{x^{2}}+\left(2x-1\right)\right)-\left(2x-1\right)$ | $\lim_{x \to -\infty} \left(-\left(-\frac{\cos(x)}{x^{2}}\right)\right)+4-4$ | $\lim_{x \to -\infty} \left(\left(\left(\frac{\cos(x)}{x^{2}}+\left(3x+1\right)\right)-\left(3x+1\right)+5\right)-5\right)+\left(3x+2\right)-\left(3x+2\right)$ | $\lim_{x \to -\infty} \left(-\left(-\left(\frac{\cos(x)}{x^{2}}+\left(-2x-1\right)-\left(-2x-1\right)\right)\right)\right)+\left(-2x+2\right)-\left(-2x+2\right)$ |
| **C=25** | $\lim_{x \to \infty} \frac{-2x^{2} + 7x}{x}$ | $\lim_{x \to \infty} \frac{4\left(x-1\right)\frac{-2x^{2} + 7x}{x}}{4\left(x-1\right)}$ | $\lim_{x \to \infty} \frac{-\left(3+x\right)\left(-\left(-\frac{-2x^{2} + 7x}{x}\right)\right)}{-\left(3+x\right)}$ | $\lim_{x \to \infty} \left(\left(\left(\frac{-2x^{2} + 7x}{x}+\left(-2x-1\right)-\left(-2x-1\right)\right)+5-5\right)+\left(-2x+1\right)\right)-\left(-2x+1\right)$ | $\lim_{x \to \infty} -\left(-\left(\frac{-\left(1-x\right)\frac{-2x^{2} + 7x}{x}}{-\left(1-x\right)}+\left(-2x\right)-\left(-2x\right)\right)\right)$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $-\frac{5}{6}$ | $-\frac{5}{6}$ | $-\frac{5}{6}$ | $-\frac{5}{6}$ | $-\frac{5}{6}$ |
| **C=4** | $5$ | $5$ | $5$ | $5$ | $5$ |
| **C=8** | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ |
| **C=12** | $-\frac{\pi}{2}$ | $-\frac{\pi}{2}$ | $-\frac{\pi}{2}$ | $-\frac{\pi}{2}$ | $-\frac{\pi}{2}$ |
| **C=16** | $0$ | $0$ | $0$ | $0$ | $0$ |
| **C=20** | $0$ | $0$ | $0$ | $0$ | $0$ |
| **C=25** | $-\infty$ | $-\infty$ | $-\infty$ | $-\infty$ | $-\infty$ |

## Cell detail

### C=0 · S=0

- Prompt: $\lim_{x \to \infty} \frac{-5x - 5}{6x}$
- Answer: $-\frac{5}{6}$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\lim_{x \to \infty} \left(\frac{-5x - 5}{6x}+5\right)-5$
- Answer: $-\frac{5}{6}$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\lim_{x \to \infty} \frac{\left(x+2\right)\left(\left(\frac{-5x - 5}{6x}+2\right)-2\right)}{x+2}$
- Answer: $-\frac{5}{6}$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\lim_{x \to \infty} -\left(-\frac{\left(x+2\right)\left(\frac{-5x - 5}{6x}+5-5\right)}{x+2}\right)$
- Answer: $-\frac{5}{6}$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\lim_{x \to \infty} -\left(-\left(\left(\frac{-5x - 5}{6x}+2\right)-2\right)+\left(x-2\right)-\left(x-2\right)\right)$
- Answer: $-\frac{5}{6}$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\lim_{x \to -\infty} \frac{5x + 4}{x}$
- Answer: $5$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\lim_{x \to -\infty} \left(\frac{5x + 4}{x}+\left(2x+3\right)\right)-\left(2x+3\right)$
- Answer: $5$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\lim_{x \to -\infty} -\left(-\frac{4\left(x-3\right)\frac{5x + 4}{x}}{4\left(x-3\right)}\right)$
- Answer: $5$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `prereq:cancel_quot_bait` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\lim_{x \to -\infty} \left(-\left(-\frac{4\left(x-2\right)\frac{5x + 4}{x}}{4\left(x-2\right)}\right)\right)+2-2$
- Answer: $5$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `prereq:cancel_quot_bait` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\lim_{x \to -\infty} \frac{3\left(x+3\right)\left(\frac{5x + 4}{x}+\left(-x+3\right)\right)-\left(-x+3\right)}{3\left(x+3\right)}+2-2$
- Answer: $5$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\lim_{x \to -\infty} \frac{-2x + 4}{3}$
- Answer: $\infty$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=8 · S=0 · amax=25 · shortfall=3

### C=8 · S=4

- Prompt: $\lim_{x \to -\infty} \left(\frac{-2x + 4}{3}+\left(3x+1\right)\right)-\left(3x+1\right)$
- Answer: $\infty$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=8 · S=4 · amax=25 · shortfall=2

### C=8 · S=8

- Prompt: $\lim_{x \to -\infty} \left(\left(\frac{-2x + 4}{3}+4\right)-4\right)+5-5$
- Answer: $\infty$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=8 · S=8 · amax=25 · shortfall=1

### C=8 · S=16

- Prompt: $\lim_{x \to -\infty} \left(\frac{3\left(x+1\right)\frac{-2x + 4}{3}}{3\left(x+1\right)}+2-2\right)+\left(3x-1\right)-\left(3x-1\right)$
- Answer: $\infty$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\lim_{x \to -\infty} \left(\frac{\left(x+2\right)\left(\frac{-2x + 4}{3}+\left(-x+1\right)-\left(-x+1\right)\right)}{x+2}+\left(3x-2\right)\right)-\left(3x-2\right)$
- Answer: $\infty$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\lim_{x \to -\infty} \arctan(x)$
- Answer: $-\frac{\pi}{2}$
- From: `form:inf_arctan` · `conceptual:end_behavior` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=4

### C=12 · S=4

- Prompt: $\lim_{x \to -\infty} \left(\arctan(x)+6\right)-6$
- Answer: $-\frac{\pi}{2}$
- From: `form:inf_arctan` · `conceptual:end_behavior` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=12 · S=4 · amax=25 · shortfall=3

### C=12 · S=8

- Prompt: $\lim_{x \to -\infty} \left(\left(\left(\arctan(x)+2\right)-2\right)+\left(3x+2\right)\right)-\left(3x+2\right)$
- Answer: $-\frac{\pi}{2}$
- From: `form:inf_arctan` · `conceptual:end_behavior` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=12 · S=8 · amax=25 · shortfall=2

### C=12 · S=16

- Prompt: $\lim_{x \to -\infty} \left(\left(\frac{-\left(3-x\right)\arctan(x)}{-\left(3-x\right)}+\left(3x-2\right)-\left(3x-2\right)\right)+5\right)-5$
- Answer: $-\frac{\pi}{2}$
- From: `form:inf_arctan` · `conceptual:end_behavior` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=16 · amax=25 · shortfall=1

### C=12 · S=32

- Prompt: $\lim_{x \to -\infty} -\left(-\left(\frac{-\left(3-x\right)\arctan(x)}{-\left(3-x\right)}+\left(3x-1\right)-\left(3x-1\right)\right)\right)$
- Answer: $-\frac{\pi}{2}$
- From: `form:inf_arctan` · `conceptual:end_behavior` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=32 · amax=25 · shortfall=1

### C=16 · S=0

- Prompt: $\lim_{x \to \infty} \frac{\cos(x)}{x^{2}}$
- Answer: $0$
- From: `form:inf_sin_over_x` · `conceptual:end_behavior` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=16 · S=0 · amax=25 · shortfall=8.5

### C=16 · S=4

- Prompt: $\lim_{x \to \infty} \left(\frac{\cos(x)}{x^{2}}+\left(-2x+1\right)\right)-\left(-2x+1\right)$
- Answer: $0$
- From: `form:inf_sin_over_x` · `conceptual:end_behavior` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=16 · S=4 · amax=25 · shortfall=7.5

### C=16 · S=8

- Prompt: $\lim_{x \to \infty} \left(\frac{\cos(x)}{x^{2}}+\left(3x-2\right)-\left(3x-2\right)\right)+\left(2x+1\right)-\left(2x+1\right)$
- Answer: $0$
- From: `form:inf_sin_over_x` · `conceptual:end_behavior` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=16 · S=8 · amax=25 · shortfall=6.5

### C=16 · S=16

- Prompt: $\lim_{x \to \infty} \left(\frac{2\left(x+3\right)\left(-\left(-\frac{\cos(x)}{x^{2}}\right)\right)}{2\left(x+3\right)}+\left(-2x-2\right)\right)-\left(-2x-2\right)$
- Answer: $0$
- From: `form:inf_sin_over_x` · `conceptual:end_behavior` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=16 · amax=25 · shortfall=5.5

### C=16 · S=32

- Prompt: $\lim_{x \to \infty} -\left(-\left(\frac{2\left(x-3\right)\frac{\cos(x)}{x^{2}}}{2\left(x-3\right)}+\left(-x+3\right)\right)-\left(-x+3\right)\right)$
- Answer: $0$
- From: `form:inf_sin_over_x` · `conceptual:end_behavior` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=32 · amax=25 · shortfall=5.5

### C=20 · S=0

- Prompt: $\lim_{x \to -\infty} \frac{\cos(x)}{x^{2}}$
- Answer: $0$
- From: `form:inf_sin_over_x` · `conceptual:end_behavior` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=20 · S=0 · amax=25 · shortfall=12.5

### C=20 · S=4

- Prompt: $\lim_{x \to -\infty} \left(\frac{\cos(x)}{x^{2}}+\left(2x-1\right)\right)-\left(2x-1\right)$
- Answer: $0$
- From: `form:inf_sin_over_x` · `conceptual:end_behavior` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=20 · S=4 · amax=25 · shortfall=11.5

### C=20 · S=8

- Prompt: $\lim_{x \to -\infty} \left(-\left(-\frac{\cos(x)}{x^{2}}\right)\right)+4-4$
- Answer: $0$
- From: `form:inf_sin_over_x` · `conceptual:end_behavior` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=20 · S=8 · amax=25 · shortfall=10.5

### C=20 · S=16

- Prompt: $\lim_{x \to -\infty} \left(\left(\left(\frac{\cos(x)}{x^{2}}+\left(3x+1\right)\right)-\left(3x+1\right)+5\right)-5\right)+\left(3x+2\right)-\left(3x+2\right)$
- Answer: $0$
- From: `form:inf_sin_over_x` · `conceptual:end_behavior` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=20 · S=16 · amax=25 · shortfall=9.5

### C=20 · S=32

- Prompt: $\lim_{x \to -\infty} \left(-\left(-\left(\frac{\cos(x)}{x^{2}}+\left(-2x-1\right)-\left(-2x-1\right)\right)\right)\right)+\left(-2x+2\right)-\left(-2x+2\right)$
- Answer: $0$
- From: `form:inf_sin_over_x` · `conceptual:end_behavior` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=20 · S=32 · amax=25 · shortfall=9.5

### C=25 · S=0

- Prompt: $\lim_{x \to \infty} \frac{-2x^{2} + 7x}{x}$
- Answer: $-\infty$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=0 · amax=25 · shortfall=20

### C=25 · S=4

- Prompt: $\lim_{x \to \infty} \frac{4\left(x-1\right)\frac{-2x^{2} + 7x}{x}}{4\left(x-1\right)}$
- Answer: $-\infty$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:invtrig`
- Flags: C=25 · S=4 · amax=25 · shortfall=19

### C=25 · S=8

- Prompt: $\lim_{x \to \infty} \frac{-\left(3+x\right)\left(-\left(-\frac{-2x^{2} + 7x}{x}\right)\right)}{-\left(3+x\right)}$
- Answer: $-\infty$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `effort:double_neg` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=25 · S=8 · amax=25 · shortfall=18

### C=25 · S=16

- Prompt: $\lim_{x \to \infty} \left(\left(\left(\frac{-2x^{2} + 7x}{x}+\left(-2x-1\right)-\left(-2x-1\right)\right)+5-5\right)+\left(-2x+1\right)\right)-\left(-2x+1\right)$
- Answer: $-\infty$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=25 · S=16 · amax=25 · shortfall=17

### C=25 · S=32

- Prompt: $\lim_{x \to \infty} -\left(-\left(\frac{-\left(1-x\right)\frac{-2x^{2} + 7x}{x}}{-\left(1-x\right)}+\left(-2x\right)-\left(-2x\right)\right)\right)$
- Answer: $-\infty$
- From: `form:inf_rational` · `conceptual:compare_degrees` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=32 · amax=25 · shortfall=17
