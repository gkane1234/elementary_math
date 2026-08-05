# L'Hôpital's rule

**type_id:** `calc_app_diff_lhopitals_rule` · **leaf:** `lhopitals_rule`  
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
| **C=0** | $\lim_{x \to 1} \frac{x^{2}-1}{x-1}$ | $\lim_{x \to 1} -\left(-\frac{x^{2}-1}{x-1}\right)$ | $\lim_{x \to 1} -\left(-\left(\left(\frac{x^{2}-1}{x-1}+1\right)-1\right)\right)$ | $\lim_{x \to 1} \left(\left(\left(\left(\frac{x^{2}-1}{x-1}+\left(x-2\right)\right)-\left(x-2\right)+1\right)-1\right)+\left(x\right)\right)-\left(x\right)$ | $\lim_{x \to 1} -\left(-\left(\left(\left(\frac{x^{2}-1}{x-1}+3-3\right)+2\right)-2\right)\right)$ |
| **C=4** | $\lim_{x \to 0} \frac{\sin(5x)}{x}$ | $\lim_{x \to 0} -\left(-\frac{\sin(5x)}{x}\right)$ | $\lim_{x \to 0} -\left(-\left(\frac{\sin(5x)}{x}+3-3\right)\right)$ | $\lim_{x \to 0} \left(\left(\left(-\left(-\frac{\sin(5x)}{x}\right)\right)+\left(-2x+2\right)\right)-\left(-2x+2\right)+3\right)-3$ | $\lim_{x \to 0} \left(\left(-\left(-\left(\frac{\sin(5x)}{x}+1-1\right)\right)\right)+\left(x-1\right)\right)-\left(x-1\right)$ |
| **C=8** | $\lim_{x \to 1} \frac{x^{2}-1}{x-1}$ | $\lim_{x \to 1} -\left(-\frac{x^{2}-1}{x-1}\right)$ | $\lim_{x \to 1} \left(\left(\frac{x^{2}-1}{x-1}+\left(-x\right)-\left(-x\right)\right)+6\right)-6$ | $\lim_{x \to 1} \left(\left(\left(\frac{x^{2}-1}{x-1}+\left(-2x-1\right)\right)-\left(-2x-1\right)+6-6\right)+\left(-x+1\right)\right)-\left(-x+1\right)$ | $\lim_{x \to 1} \left(\left(\left(\left(\frac{x^{2}-1}{x-1}+\left(-2x+1\right)\right)-\left(-2x+1\right)+4\right)-4\right)+\left(3x+3\right)\right)-\left(3x+3\right)$ |
| **C=12** | $\lim_{x \to 0^{+}} \left(\frac{1}{x}-\frac{1}{\sin(x)}\right)$ | $\lim_{x \to 0^{+}} -\left(-\left(\frac{1}{x}-\frac{1}{\sin(x)}\right)\right)$ | $\lim_{x \to 0^{+}} \left(\left(-\left(-\left(\frac{1}{x}-\frac{1}{\sin(x)}\right)\right)\right)+\left(x-1\right)\right)-\left(x-1\right)$ | $\lim_{x \to 0^{+}} -\left(-\left(\left(\frac{1}{x}-\frac{1}{\sin(x)}\right)+\left(2x-2\right)-\left(2x-2\right)+\left(2x+2\right)\right)-\left(2x+2\right)\right)$ | $\lim_{x \to 0^{+}} -\left(-\left(\left(\left(\frac{1}{x}-\frac{1}{\sin(x)}\right)+1\right)-1\right)+\left(-2x-1\right)-\left(-2x-1\right)\right)$ |
| **C=16** | $\lim_{x \to \infty} \frac{6x^{2}-1}{3x^{2}+1}$ | $\lim_{x \to \infty} \frac{6x^{2}-1}{3x^{2}+1}+1-1$ | $\lim_{x \to \infty} \left(\frac{6x^{2}-1}{3x^{2}+1}+6-6\right)+\left(x-1\right)-\left(x-1\right)$ | $\lim_{x \to \infty} \left(\left(-\left(-\frac{6x^{2}-1}{3x^{2}+1}\right)\right)+\left(3x\right)\right)-\left(3x\right)+5-5$ | $\lim_{x \to \infty} -\left(-\left(\left(\left(\frac{6x^{2}-1}{3x^{2}+1}+1\right)-1\right)+\left(-2x\right)\right)-\left(-2x\right)\right)$ |
| **C=20** | $\lim_{x \to \infty} \left(\frac{1}{x}\right)^{x}$ | $\lim_{x \to \infty} \left(\frac{1}{x}\right)^{x}+\left(2x\right)-\left(2x\right)$ | $\lim_{x \to \infty} \left(\left(\left(\frac{1}{x}\right)^{x}+6-6\right)+3\right)-3$ | $\lim_{x \to \infty} \left(-\left(-\left(\frac{1}{x}\right)^{x}+\left(-x+1\right)-\left(-x+1\right)\right)\right)+3-3$ | $\lim_{x \to \infty} \left(\left(\left(\left(\frac{1}{x}\right)^{x}+4\right)-4\right)+\left(x+1\right)\right)-\left(x+1\right)+6-6$ |
| **C=25** | $\lim_{x \to 0} \frac{\sin(3x)}{x}$ | $\lim_{x \to 0} \left(\frac{\sin(3x)}{x}+6\right)-6$ | $\lim_{x \to 0} -\left(-\left(\frac{\sin(3x)}{x}+\left(-2x+2\right)\right)-\left(-2x+2\right)\right)$ | $\lim_{x \to 0} \left(\left(-\left(-\frac{\sin(3x)}{x}\right)\right)+\left(2x-2\right)\right)-\left(2x-2\right)+\left(3x+1\right)-\left(3x+1\right)$ | $\lim_{x \to 0} \left(\left(\left(\left(-\left(-\frac{\sin(3x)}{x}\right)\right)+4\right)-4\right)+5\right)-5$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $2$ | $2$ | $2$ | $2$ | $2$ |
| **C=4** | $5$ | $5$ | $5$ | $5$ | $5$ |
| **C=8** | $2$ | $2$ | $2$ | $2$ | $2$ |
| **C=12** | $-\frac{1}{6}$ | $-\frac{1}{6}$ | $-\frac{1}{6}$ | $-\frac{1}{6}$ | $-\frac{1}{6}$ |
| **C=16** | $2$ | $2$ | $2$ | $2$ | $2$ |
| **C=20** | $0$ | $0$ | $0$ | $0$ | $0$ |
| **C=25** | $3$ | $3$ | $3$ | $3$ | $3$ |

## Cell detail

### C=0 · S=0

- Prompt: $\lim_{x \to 1} \frac{x^{2}-1}{x-1}$
- Answer: $2$
- From: `form:lhopital_0_0_poly` · `conceptual:lhopital` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\lim_{x \to 1} -\left(-\frac{x^{2}-1}{x-1}\right)$
- Answer: $2$
- From: `form:lhopital_0_0_poly` · `conceptual:lhopital` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\lim_{x \to 1} -\left(-\left(\left(\frac{x^{2}-1}{x-1}+1\right)-1\right)\right)$
- Answer: $2$
- From: `form:lhopital_0_0_poly` · `conceptual:lhopital` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\lim_{x \to 1} \left(\left(\left(\left(\frac{x^{2}-1}{x-1}+\left(x-2\right)\right)-\left(x-2\right)+1\right)-1\right)+\left(x\right)\right)-\left(x\right)$
- Answer: $2$
- From: `form:lhopital_0_0_poly` · `conceptual:lhopital` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\lim_{x \to 1} -\left(-\left(\left(\left(\frac{x^{2}-1}{x-1}+3-3\right)+2\right)-2\right)\right)$
- Answer: $2$
- From: `form:lhopital_0_0_poly` · `conceptual:lhopital` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\lim_{x \to 0} \frac{\sin(5x)}{x}$
- Answer: $5$
- From: `form:lhopital_0_0_trig` · `conceptual:lhopital` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\lim_{x \to 0} -\left(-\frac{\sin(5x)}{x}\right)$
- Answer: $5$
- From: `form:lhopital_0_0_trig` · `conceptual:lhopital` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\lim_{x \to 0} -\left(-\left(\frac{\sin(5x)}{x}+3-3\right)\right)$
- Answer: $5$
- From: `form:lhopital_0_0_trig` · `conceptual:lhopital` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\lim_{x \to 0} \left(\left(\left(-\left(-\frac{\sin(5x)}{x}\right)\right)+\left(-2x+2\right)\right)-\left(-2x+2\right)+3\right)-3$
- Answer: $5$
- From: `form:lhopital_0_0_trig` · `conceptual:lhopital` · `effort:double_neg` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\lim_{x \to 0} \left(\left(-\left(-\left(\frac{\sin(5x)}{x}+1-1\right)\right)\right)+\left(x-1\right)\right)-\left(x-1\right)$
- Answer: $5$
- From: `form:lhopital_0_0_trig` · `conceptual:lhopital` · `effort:add_cancel_const` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\lim_{x \to 1} \frac{x^{2}-1}{x-1}$
- Answer: $2$
- From: `form:lhopital_0_0_poly` · `conceptual:lhopital` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=8 · S=0 · amax=25 · shortfall=1

### C=8 · S=4

- Prompt: $\lim_{x \to 1} -\left(-\frac{x^{2}-1}{x-1}\right)$
- Answer: $2$
- From: `form:lhopital_0_0_poly` · `conceptual:lhopital` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\lim_{x \to 1} \left(\left(\frac{x^{2}-1}{x-1}+\left(-x\right)-\left(-x\right)\right)+6\right)-6$
- Answer: $2$
- From: `form:lhopital_0_0_poly` · `conceptual:lhopital` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\lim_{x \to 1} \left(\left(\left(\frac{x^{2}-1}{x-1}+\left(-2x-1\right)\right)-\left(-2x-1\right)+6-6\right)+\left(-x+1\right)\right)-\left(-x+1\right)$
- Answer: $2$
- From: `form:lhopital_0_0_poly` · `conceptual:lhopital` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\lim_{x \to 1} \left(\left(\left(\left(\frac{x^{2}-1}{x-1}+\left(-2x+1\right)\right)-\left(-2x+1\right)+4\right)-4\right)+\left(3x+3\right)\right)-\left(3x+3\right)$
- Answer: $2$
- From: `form:lhopital_0_0_poly` · `conceptual:lhopital` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\lim_{x \to 0^{+}} \left(\frac{1}{x}-\frac{1}{\sin(x)}\right)$
- Answer: $-\frac{1}{6}$
- From: `form:lhopital_inf_minus_inf` · `conceptual:lhopital` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25

### C=12 · S=4

- Prompt: $\lim_{x \to 0^{+}} -\left(-\left(\frac{1}{x}-\frac{1}{\sin(x)}\right)\right)$
- Answer: $-\frac{1}{6}$
- From: `form:lhopital_inf_minus_inf` · `conceptual:lhopital` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=12 · S=4 · amax=25

### C=12 · S=8

- Prompt: $\lim_{x \to 0^{+}} \left(\left(-\left(-\left(\frac{1}{x}-\frac{1}{\sin(x)}\right)\right)\right)+\left(x-1\right)\right)-\left(x-1\right)$
- Answer: $-\frac{1}{6}$
- From: `form:lhopital_inf_minus_inf` · `conceptual:lhopital` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=12 · S=8 · amax=25

### C=12 · S=16

- Prompt: $\lim_{x \to 0^{+}} -\left(-\left(\left(\frac{1}{x}-\frac{1}{\sin(x)}\right)+\left(2x-2\right)-\left(2x-2\right)+\left(2x+2\right)\right)-\left(2x+2\right)\right)$
- Answer: $-\frac{1}{6}$
- From: `form:lhopital_inf_minus_inf` · `conceptual:lhopital` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=12 · S=16 · amax=25

### C=12 · S=32

- Prompt: $\lim_{x \to 0^{+}} -\left(-\left(\left(\left(\frac{1}{x}-\frac{1}{\sin(x)}\right)+1\right)-1\right)+\left(-2x-1\right)-\left(-2x-1\right)\right)$
- Answer: $-\frac{1}{6}$
- From: `form:lhopital_inf_minus_inf` · `conceptual:lhopital` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=32 · amax=25

### C=16 · S=0

- Prompt: $\lim_{x \to \infty} \frac{6x^{2}-1}{3x^{2}+1}$
- Answer: $2$
- From: `form:lhopital_inf_inf_poly` · `conceptual:lhopital` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=16 · S=0 · amax=25 · shortfall=5

### C=16 · S=4

- Prompt: $\lim_{x \to \infty} \frac{6x^{2}-1}{3x^{2}+1}+1-1$
- Answer: $2$
- From: `form:lhopital_inf_inf_poly` · `conceptual:lhopital` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=16 · S=4 · amax=25 · shortfall=4

### C=16 · S=8

- Prompt: $\lim_{x \to \infty} \left(\frac{6x^{2}-1}{3x^{2}+1}+6-6\right)+\left(x-1\right)-\left(x-1\right)$
- Answer: $2$
- From: `form:lhopital_inf_inf_poly` · `conceptual:lhopital` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=16 · S=8 · amax=25 · shortfall=3

### C=16 · S=16

- Prompt: $\lim_{x \to \infty} \left(\left(-\left(-\frac{6x^{2}-1}{3x^{2}+1}\right)\right)+\left(3x\right)\right)-\left(3x\right)+5-5$
- Answer: $2$
- From: `form:lhopital_inf_inf_poly` · `conceptual:lhopital` · `effort:double_neg` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=16 · amax=25 · shortfall=2

### C=16 · S=32

- Prompt: $\lim_{x \to \infty} -\left(-\left(\left(\left(\frac{6x^{2}-1}{3x^{2}+1}+1\right)-1\right)+\left(-2x\right)\right)-\left(-2x\right)\right)$
- Answer: $2$
- From: `form:lhopital_inf_inf_poly` · `conceptual:lhopital` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=16 · S=32 · amax=25 · shortfall=2

### C=20 · S=0

- Prompt: $\lim_{x \to \infty} \left(\frac{1}{x}\right)^{x}$
- Answer: $0$
- From: `form:lhopital_0_inf_power` · `conceptual:lhopital` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=20 · S=0 · amax=25 · shortfall=1

### C=20 · S=4

- Prompt: $\lim_{x \to \infty} \left(\frac{1}{x}\right)^{x}+\left(2x\right)-\left(2x\right)$
- Answer: $0$
- From: `form:lhopital_0_inf_power` · `conceptual:lhopital` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=20 · S=4 · amax=25

### C=20 · S=8

- Prompt: $\lim_{x \to \infty} \left(\left(\left(\frac{1}{x}\right)^{x}+6-6\right)+3\right)-3$
- Answer: $0$
- From: `form:lhopital_0_inf_power` · `conceptual:lhopital` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=20 · S=8 · amax=25

### C=20 · S=16

- Prompt: $\lim_{x \to \infty} \left(-\left(-\left(\frac{1}{x}\right)^{x}+\left(-x+1\right)-\left(-x+1\right)\right)\right)+3-3$
- Answer: $0$
- From: `form:lhopital_0_inf_power` · `conceptual:lhopital` · `effort:add_cancel_linear` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=16 · amax=25

### C=20 · S=32

- Prompt: $\lim_{x \to \infty} \left(\left(\left(\left(\frac{1}{x}\right)^{x}+4\right)-4\right)+\left(x+1\right)\right)-\left(x+1\right)+6-6$
- Answer: $0$
- From: `form:lhopital_0_inf_power` · `conceptual:lhopital` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=20 · S=32 · amax=25

### C=25 · S=0

- Prompt: $\lim_{x \to 0} \frac{\sin(3x)}{x}$
- Answer: $3$
- From: `form:lhopital_0_0_trig` · `conceptual:lhopital` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=25 · S=0 · amax=25 · shortfall=16.5

### C=25 · S=4

- Prompt: $\lim_{x \to 0} \left(\frac{\sin(3x)}{x}+6\right)-6$
- Answer: $3$
- From: `form:lhopital_0_0_trig` · `conceptual:lhopital` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig` · `allow:one_sided`
- Flags: C=25 · S=4 · amax=25 · shortfall=15.5

### C=25 · S=8

- Prompt: $\lim_{x \to 0} -\left(-\left(\frac{\sin(3x)}{x}+\left(-2x+2\right)\right)-\left(-2x+2\right)\right)$
- Answer: $3$
- From: `form:lhopital_0_0_trig` · `conceptual:lhopital` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=25 · S=8 · amax=25 · shortfall=14.5

### C=25 · S=16

- Prompt: $\lim_{x \to 0} \left(\left(-\left(-\frac{\sin(3x)}{x}\right)\right)+\left(2x-2\right)\right)-\left(2x-2\right)+\left(3x+1\right)-\left(3x+1\right)$
- Answer: $3$
- From: `form:lhopital_0_0_trig` · `conceptual:lhopital` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=25 · S=16 · amax=25 · shortfall=13.5

### C=25 · S=32

- Prompt: $\lim_{x \to 0} \left(\left(\left(\left(-\left(-\frac{\sin(3x)}{x}\right)\right)+4\right)-4\right)+5\right)-5$
- Answer: $3$
- From: `form:lhopital_0_0_trig` · `conceptual:lhopital` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `allow:invtrig`
- Flags: C=25 · S=32 · amax=25 · shortfall=13.5
