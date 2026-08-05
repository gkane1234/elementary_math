# Limits — jump discontinuities / kinks

**type_id:** `calc_limits_at_jump_discontinuities_and_kinks` · **leaf:** `limit_jump`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_exp`, `allow_log`, `allow_one_sided`, `allow_roots`, `allow_trig`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\lim_{x \to -5} f(x)\text{ where }f(x)=\begin{cases}3&x<-5\\-6&x\ge -5\end{cases}$ | $\lim_{x \to -5} f(x)\text{ where }f(x)=\begin{cases}3&x<-5\\-6&x\ge -5\end{cases}$ | $\lim_{x \to -5} f(x)\text{ where }f(x)=\begin{cases}3&x<-5\\-6&x\ge -5\end{cases}$ | $\lim_{x \to -5} f(x)\text{ where }f(x)=\begin{cases}3&x<-5\\-6&x\ge -5\end{cases}$ | $\lim_{x \to -5} f(x)\text{ where }f(x)=\begin{cases}3&x<-5\\-6&x\ge -5\end{cases}$ |
| **C=4** | $\lim_{x \to 1} f(x)\text{ where }f(x)=\begin{cases}6&x<1\\-4x - 4&x\ge 1\end{cases}$ | $\lim_{x \to 1} f(x)\text{ where }f(x)=\begin{cases}6&x<1\\-4x - 4&x\ge 1\end{cases}$ | $\lim_{x \to 1} f(x)\text{ where }f(x)=\begin{cases}6&x<1\\-4x - 4&x\ge 1\end{cases}$ | $\lim_{x \to 1} f(x)\text{ where }f(x)=\begin{cases}6&x<1\\-4x - 4&x\ge 1\end{cases}$ | $\lim_{x \to 1} f(x)\text{ where }f(x)=\begin{cases}6&x<1\\-4x - 4&x\ge 1\end{cases}$ |
| **C=8** | $\lim_{x \to -5^{+}} f(x)\text{ where }f(x)=\begin{cases}4x^{2} - 4x&x<-5\\x - 2&x\ge -5\end{cases}$ | $\lim_{x \to -5^{+}} f(x)\text{ where }f(x)=\begin{cases}4x^{2} - 4x&x<-5\\x - 2&x\ge -5\end{cases}$ | $\lim_{x \to -5^{+}} f(x)\text{ where }f(x)=\begin{cases}4x^{2} - 4x&x<-5\\x - 2&x\ge -5\end{cases}$ | $\lim_{x \to -5^{+}} f(x)\text{ where }f(x)=\begin{cases}4x^{2} - 4x&x<-5\\x - 2&x\ge -5\end{cases}$ | $\lim_{x \to -5^{+}} f(x)\text{ where }f(x)=\begin{cases}4x^{2} - 4x&x<-5\\x - 2&x\ge -5\end{cases}$ |
| **C=12** | $\lim_{x \to 1^{+}} f(x)\text{ where }f(x)=\begin{cases}-x^{2} - 3x - 2&x<1\\-5&x=1\\-2x^{2} + 4x + 1&x>1\end{cases}$ | $\lim_{x \to 1^{+}} f(x)\text{ where }f(x)=\begin{cases}-x^{2} - 3x - 2&x<1\\-5&x=1\\-2x^{2} + 4x + 1&x>1\end{cases}$ | $\lim_{x \to 1^{+}} f(x)\text{ where }f(x)=\begin{cases}-x^{2} - 3x - 2&x<1\\-5&x=1\\-2x^{2} + 4x + 1&x>1\end{cases}$ | $\lim_{x \to 1^{+}} f(x)\text{ where }f(x)=\begin{cases}-x^{2} - 3x - 2&x<1\\-5&x=1\\-2x^{2} + 4x + 1&x>1\end{cases}$ | $\lim_{x \to 1^{+}} f(x)\text{ where }f(x)=\begin{cases}-x^{2} - 3x - 2&x<1\\-5&x=1\\-2x^{2} + 4x + 1&x>1\end{cases}$ |
| **C=16** | $\lim_{x \to 1^{-}} f(x)\text{ where }f(x)=\begin{cases}\left(-2x - 6\right)\left(-5x + 1\right)&x<1\\28&x=1\\2x^{2} + 2x - 4&x>1\end{cases}$ | $\lim_{x \to 1^{-}} f(x)\text{ where }f(x)=\begin{cases}\left(-2x - 6\right)\left(-5x + 1\right)&x<1\\28&x=1\\2x^{2} + 2x - 4&x>1\end{cases}$ | $\lim_{x \to 1^{-}} f(x)\text{ where }f(x)=\begin{cases}\left(-2x - 6\right)\left(-5x + 1\right)&x<1\\28&x=1\\2x^{2} + 2x - 4&x>1\end{cases}$ | $\lim_{x \to 1^{-}} f(x)\text{ where }f(x)=\begin{cases}\left(-2x - 6\right)\left(-5x + 1\right)&x<1\\28&x=1\\2x^{2} + 2x - 4&x>1\end{cases}$ | $\lim_{x \to 1^{-}} f(x)\text{ where }f(x)=\begin{cases}\left(-2x - 6\right)\left(-5x + 1\right)&x<1\\28&x=1\\2x^{2} + 2x - 4&x>1\end{cases}$ |
| **C=20** | $\lim_{x \to -2} f(x)\text{ where }f(x)=\begin{cases}\ln\left(x + 3\right)-4&x<-2\\-4&x=-2\\-e^{x + 2}&x>-2\end{cases}$ | $\lim_{x \to -2} f(x)\text{ where }f(x)=\begin{cases}\ln\left(x + 3\right)-4&x<-2\\-4&x=-2\\-e^{x + 2}&x>-2\end{cases}$ | $\lim_{x \to -2} f(x)\text{ where }f(x)=\begin{cases}\ln\left(x + 3\right)-4&x<-2\\-4&x=-2\\-e^{x + 2}&x>-2\end{cases}$ | $\lim_{x \to -2} f(x)\text{ where }f(x)=\begin{cases}\ln\left(x + 3\right)-4&x<-2\\-4&x=-2\\-e^{x + 2}&x>-2\end{cases}$ | $\lim_{x \to -2} f(x)\text{ where }f(x)=\begin{cases}\ln\left(x + 3\right)-4&x<-2\\-4&x=-2\\-e^{x + 2}&x>-2\end{cases}$ |
| **C=25** | $\lim_{x \to 3^{-}} f(x)\text{ where }f(x)=\begin{cases}5x^{3} - x^{2} - x - 3&x<3\\114&x=3\\\left(-6x + 2\right)\left(-x\right)&x>3\end{cases}$ | $\lim_{x \to 3^{-}} f(x)\text{ where }f(x)=\begin{cases}5x^{3} - x^{2} - x - 3&x<3\\114&x=3\\\left(-6x + 2\right)\left(-x\right)&x>3\end{cases}$ | $\lim_{x \to 3^{-}} f(x)\text{ where }f(x)=\begin{cases}5x^{3} - x^{2} - x - 3&x<3\\114&x=3\\\left(-6x + 2\right)\left(-x\right)&x>3\end{cases}$ | $\lim_{x \to 3^{-}} f(x)\text{ where }f(x)=\begin{cases}5x^{3} - x^{2} - x - 3&x<3\\114&x=3\\\left(-6x + 2\right)\left(-x\right)&x>3\end{cases}$ | $\lim_{x \to 3^{-}} f(x)\text{ where }f(x)=\begin{cases}5x^{3} - x^{2} - x - 3&x<3\\114&x=3\\\left(-6x + 2\right)\left(-x\right)&x>3\end{cases}$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ |
| **C=4** | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ |
| **C=8** | $-7$ | $-7$ | $-7$ | $-7$ | $-7$ |
| **C=12** | $3$ | $3$ | $3$ | $3$ | $3$ |
| **C=16** | $32$ | $32$ | $32$ | $32$ | $32$ |
| **C=20** | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ | $\text{DNE}$ |
| **C=25** | $120$ | $120$ | $120$ | $120$ | $120$ |

## Cell detail

### C=0 · S=0

- Prompt: $\lim_{x \to -5} f(x)\text{ where }f(x)=\begin{cases}3&x<-5\\-6&x\ge -5\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump` · `conceptual:two_sided_compare` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\lim_{x \to -5} f(x)\text{ where }f(x)=\begin{cases}3&x<-5\\-6&x\ge -5\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump` · `conceptual:two_sided_compare` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\lim_{x \to -5} f(x)\text{ where }f(x)=\begin{cases}3&x<-5\\-6&x\ge -5\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump` · `conceptual:two_sided_compare` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\lim_{x \to -5} f(x)\text{ where }f(x)=\begin{cases}3&x<-5\\-6&x\ge -5\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump` · `conceptual:two_sided_compare` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\lim_{x \to -5} f(x)\text{ where }f(x)=\begin{cases}3&x<-5\\-6&x\ge -5\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump` · `conceptual:two_sided_compare` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided` · `effort:spec_high`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\lim_{x \to 1} f(x)\text{ where }f(x)=\begin{cases}6&x<1\\-4x - 4&x\ge 1\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump_linear` · `conceptual:two_sided_compare` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=4 · S=0 · amax=25

### C=4 · S=4

- Prompt: $\lim_{x \to 1} f(x)\text{ where }f(x)=\begin{cases}6&x<1\\-4x - 4&x\ge 1\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump_linear` · `conceptual:two_sided_compare` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\lim_{x \to 1} f(x)\text{ where }f(x)=\begin{cases}6&x<1\\-4x - 4&x\ge 1\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump_linear` · `conceptual:two_sided_compare` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\lim_{x \to 1} f(x)\text{ where }f(x)=\begin{cases}6&x<1\\-4x - 4&x\ge 1\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump_linear` · `conceptual:two_sided_compare` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\lim_{x \to 1} f(x)\text{ where }f(x)=\begin{cases}6&x<1\\-4x - 4&x\ge 1\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump_linear` · `conceptual:two_sided_compare` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided` · `effort:spec_high`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\lim_{x \to -5^{+}} f(x)\text{ where }f(x)=\begin{cases}4x^{2} - 4x&x<-5\\x - 2&x\ge -5\end{cases}$
- Answer: $-7$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=8 · S=0 · amax=25

### C=8 · S=4

- Prompt: $\lim_{x \to -5^{+}} f(x)\text{ where }f(x)=\begin{cases}4x^{2} - 4x&x<-5\\x - 2&x\ge -5\end{cases}$
- Answer: $-7$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\lim_{x \to -5^{+}} f(x)\text{ where }f(x)=\begin{cases}4x^{2} - 4x&x<-5\\x - 2&x\ge -5\end{cases}$
- Answer: $-7$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\lim_{x \to -5^{+}} f(x)\text{ where }f(x)=\begin{cases}4x^{2} - 4x&x<-5\\x - 2&x\ge -5\end{cases}$
- Answer: $-7$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\lim_{x \to -5^{+}} f(x)\text{ where }f(x)=\begin{cases}4x^{2} - 4x&x<-5\\x - 2&x\ge -5\end{cases}$
- Answer: $-7$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided` · `effort:spec_high`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\lim_{x \to 1^{+}} f(x)\text{ where }f(x)=\begin{cases}-x^{2} - 3x - 2&x<1\\-5&x=1\\-2x^{2} + 4x + 1&x>1\end{cases}$
- Answer: $3$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=12 · S=0 · amax=25

### C=12 · S=4

- Prompt: $\lim_{x \to 1^{+}} f(x)\text{ where }f(x)=\begin{cases}-x^{2} - 3x - 2&x<1\\-5&x=1\\-2x^{2} + 4x + 1&x>1\end{cases}$
- Answer: $3$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=12 · S=4 · amax=25

### C=12 · S=8

- Prompt: $\lim_{x \to 1^{+}} f(x)\text{ where }f(x)=\begin{cases}-x^{2} - 3x - 2&x<1\\-5&x=1\\-2x^{2} + 4x + 1&x>1\end{cases}$
- Answer: $3$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=12 · S=8 · amax=25

### C=12 · S=16

- Prompt: $\lim_{x \to 1^{+}} f(x)\text{ where }f(x)=\begin{cases}-x^{2} - 3x - 2&x<1\\-5&x=1\\-2x^{2} + 4x + 1&x>1\end{cases}$
- Answer: $3$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=12 · S=16 · amax=25

### C=12 · S=32

- Prompt: $\lim_{x \to 1^{+}} f(x)\text{ where }f(x)=\begin{cases}-x^{2} - 3x - 2&x<1\\-5&x=1\\-2x^{2} + 4x + 1&x>1\end{cases}$
- Answer: $3$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots` · `allow:one_sided`
- Flags: C=12 · S=32 · amax=25

### C=16 · S=0

- Prompt: $\lim_{x \to 1^{-}} f(x)\text{ where }f(x)=\begin{cases}\left(-2x - 6\right)\left(-5x + 1\right)&x<1\\28&x=1\\2x^{2} + 2x - 4&x>1\end{cases}$
- Answer: $32$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `effort:awkward_factors` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=16 · S=0 · amax=25

### C=16 · S=4

- Prompt: $\lim_{x \to 1^{-}} f(x)\text{ where }f(x)=\begin{cases}\left(-2x - 6\right)\left(-5x + 1\right)&x<1\\28&x=1\\2x^{2} + 2x - 4&x>1\end{cases}$
- Answer: $32$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `effort:awkward_factors` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=16 · S=4 · amax=25

### C=16 · S=8

- Prompt: $\lim_{x \to 1^{-}} f(x)\text{ where }f(x)=\begin{cases}\left(-2x - 6\right)\left(-5x + 1\right)&x<1\\28&x=1\\2x^{2} + 2x - 4&x>1\end{cases}$
- Answer: $32$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `effort:awkward_factors` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=16 · S=8 · amax=25

### C=16 · S=16

- Prompt: $\lim_{x \to 1^{-}} f(x)\text{ where }f(x)=\begin{cases}\left(-2x - 6\right)\left(-5x + 1\right)&x<1\\28&x=1\\2x^{2} + 2x - 4&x>1\end{cases}$
- Answer: $32$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `effort:awkward_factors` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=16 · S=16 · amax=25

### C=16 · S=32

- Prompt: $\lim_{x \to 1^{-}} f(x)\text{ where }f(x)=\begin{cases}\left(-2x - 6\right)\left(-5x + 1\right)&x<1\\28&x=1\\2x^{2} + 2x - 4&x>1\end{cases}$
- Answer: $32$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `effort:awkward_factors` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log` · `allow:roots`
- Flags: C=16 · S=32 · amax=25

### C=20 · S=0

- Prompt: $\lim_{x \to -2} f(x)\text{ where }f(x)=\begin{cases}\ln\left(x + 3\right)-4&x<-2\\-4&x=-2\\-e^{x + 2}&x>-2\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump_poly` · `conceptual:two_sided_compare` · `allow:log_side` · `allow:exp_side` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=0 · amax=25

### C=20 · S=4

- Prompt: $\lim_{x \to -2} f(x)\text{ where }f(x)=\begin{cases}\ln\left(x + 3\right)-4&x<-2\\-4&x=-2\\-e^{x + 2}&x>-2\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump_poly` · `conceptual:two_sided_compare` · `allow:log_side` · `allow:exp_side` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=4 · amax=25

### C=20 · S=8

- Prompt: $\lim_{x \to -2} f(x)\text{ where }f(x)=\begin{cases}\ln\left(x + 3\right)-4&x<-2\\-4&x=-2\\-e^{x + 2}&x>-2\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump_poly` · `conceptual:two_sided_compare` · `allow:log_side` · `allow:exp_side` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=8 · amax=25

### C=20 · S=16

- Prompt: $\lim_{x \to -2} f(x)\text{ where }f(x)=\begin{cases}\ln\left(x + 3\right)-4&x<-2\\-4&x=-2\\-e^{x + 2}&x>-2\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump_poly` · `conceptual:two_sided_compare` · `allow:log_side` · `allow:exp_side` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=16 · amax=25

### C=20 · S=32

- Prompt: $\lim_{x \to -2} f(x)\text{ where }f(x)=\begin{cases}\ln\left(x + 3\right)-4&x<-2\\-4&x=-2\\-e^{x + 2}&x>-2\end{cases}$
- Answer: $\text{DNE}$
- From: `form:piecewise_jump_poly` · `conceptual:two_sided_compare` · `allow:log_side` · `allow:exp_side` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=32 · amax=25

### C=25 · S=0

- Prompt: $\lim_{x \to 3^{-}} f(x)\text{ where }f(x)=\begin{cases}5x^{3} - x^{2} - x - 3&x<3\\114&x=3\\\left(-6x + 2\right)\left(-x\right)&x>3\end{cases}$
- Answer: $120$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `effort:cubic_side` · `effort:awkward_factors` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=0 · amax=25 · shortfall=3

### C=25 · S=4

- Prompt: $\lim_{x \to 3^{-}} f(x)\text{ where }f(x)=\begin{cases}5x^{3} - x^{2} - x - 3&x<3\\114&x=3\\\left(-6x + 2\right)\left(-x\right)&x>3\end{cases}$
- Answer: $120$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `effort:cubic_side` · `effort:awkward_factors` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=4 · amax=25 · shortfall=3

### C=25 · S=8

- Prompt: $\lim_{x \to 3^{-}} f(x)\text{ where }f(x)=\begin{cases}5x^{3} - x^{2} - x - 3&x<3\\114&x=3\\\left(-6x + 2\right)\left(-x\right)&x>3\end{cases}$
- Answer: $120$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `effort:cubic_side` · `effort:awkward_factors` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=8 · amax=25 · shortfall=3

### C=25 · S=16

- Prompt: $\lim_{x \to 3^{-}} f(x)\text{ where }f(x)=\begin{cases}5x^{3} - x^{2} - x - 3&x<3\\114&x=3\\\left(-6x + 2\right)\left(-x\right)&x>3\end{cases}$
- Answer: $120$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `effort:cubic_side` · `effort:awkward_factors` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=16 · amax=25 · shortfall=3

### C=25 · S=32

- Prompt: $\lim_{x \to 3^{-}} f(x)\text{ where }f(x)=\begin{cases}5x^{3} - x^{2} - x - 3&x<3\\114&x=3\\\left(-6x + 2\right)\left(-x\right)&x>3\end{cases}$
- Answer: $120$
- From: `form:piecewise_jump_poly` · `conceptual:one_sided` · `effort:cubic_side` · `effort:awkward_factors` · `conceptual:three_piece` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=32 · amax=25 · shortfall=3
