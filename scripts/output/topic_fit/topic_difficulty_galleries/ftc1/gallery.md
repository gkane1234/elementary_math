# FTC — first

**type_id:** `calc_def_int_first_fundamental_theorem_of_calculus` · **leaf:** `first_fundamental_theorem`  
Conceptual max (full allow_* kit): **25**  
Conceptual axis: 0, 4, 8, 12, 16, 20, 25  
Spec axis (presentation dress, unbounded): 0, 4, 8, 16, 32  
Allows: `allow_exp`, `allow_roots`, `allow_trig`  
**Generated:** 2026-08-05 19:09 UTC

Open [gallery.html](gallery.html) in a browser for KaTeX.

True **2D grid**: rows = conceptual (calculus method/form), columns = Spec
(algebra presentation: cancel bait / cancel pairs — same answer after simplify).
Spec does not change the calculus method or raise the underlying degree.

## Grid (prompt)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $\int_{0}^{\pi/2} \sin(x)\,dx$ |
| **C=4** | $\int_{0}^{4} x\,dx$ | $\int_{0}^{4} x\,dx$ | $\int_{0}^{4} x\,dx$ | $\int_{0}^{4} x\,dx$ | $\int_{0}^{4} x\,dx$ |
| **C=8** | $\frac{d}{dx}\int_{0}^{2x + 1} x\,dx$ | $\frac{d}{dx}\int_{0}^{2x + 1} x\,dx$ | $\frac{d}{dx}\int_{0}^{2x + 1} x\,dx$ | $\frac{d}{dx}\int_{0}^{2x + 1} x\,dx$ | $\frac{d}{dx}\int_{0}^{2x + 1} x\,dx$ |
| **C=12** | $\frac{d}{dx}\int_{0}^{-x + 1} \sin(x)\,dx$ | $\frac{d}{dx}\int_{0}^{-x + 1} \sin(x)\,dx$ | $\frac{d}{dx}\int_{0}^{-x + 1} \sin(x)\,dx$ | $\frac{d}{dx}\int_{0}^{-x + 1} \sin(x)\,dx$ | $\frac{d}{dx}\int_{0}^{-x + 1} \sin(x)\,dx$ |
| **C=16** | $\frac{d}{dx}\int_{0}^{3x - 1} x\,dx$ | $\frac{d}{dx}\int_{0}^{3x - 1} x\,dx$ | $\frac{d}{dx}\int_{0}^{3x - 1} x\,dx$ | $\frac{d}{dx}\int_{0}^{3x - 1} x\,dx$ | $\frac{d}{dx}\int_{0}^{3x - 1} x\,dx$ |
| **C=20** | $\frac{d}{dx}\int_{0}^{-2x + 2} x^{2}\,dx$ | $\frac{d}{dx}\int_{0}^{-2x + 2} x^{2}\,dx$ | $\frac{d}{dx}\int_{0}^{-2x + 2} x^{2}\,dx$ | $\frac{d}{dx}\int_{0}^{-2x + 2} x^{2}\,dx$ | $\frac{d}{dx}\int_{0}^{-2x + 2} x^{2}\,dx$ |
| **C=25** | $\int_{0}^{2} x^{2}\,dx$ | $\int_{0}^{2} x^{2}\,dx$ | $\int_{0}^{2} x^{2}\,dx$ | $\int_{0}^{2} x^{2}\,dx$ | $\int_{0}^{2} x^{2}\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $1$ | $1$ | $1$ | $1$ | $1$ |
| **C=4** | $8$ | $8$ | $8$ | $8$ | $8$ |
| **C=8** | $2\left(2x + 1\right)$ | $2\left(2x + 1\right)$ | $2\left(2x + 1\right)$ | $2\left(2x + 1\right)$ | $2\left(2x + 1\right)$ |
| **C=12** | $-\sin\left(-x + 1\right)$ | $-\sin\left(-x + 1\right)$ | $-\sin\left(-x + 1\right)$ | $-\sin\left(-x + 1\right)$ | $-\sin\left(-x + 1\right)$ |
| **C=16** | $3\left(3x - 1\right)$ | $3\left(3x - 1\right)$ | $3\left(3x - 1\right)$ | $3\left(3x - 1\right)$ | $3\left(3x - 1\right)$ |
| **C=20** | $-2\left(-2x + 2\right)^{2}$ | $-2\left(-2x + 2\right)^{2}$ | $-2\left(-2x + 2\right)^{2}$ | $-2\left(-2x + 2\right)^{2}$ | $-2\left(-2x + 2\right)^{2}$ |
| **C=25** | $\frac{8}{3}$ | $\frac{8}{3}$ | $\frac{8}{3}$ | $\frac{8}{3}$ | $\frac{8}{3}$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int_{0}^{\pi/2} \sin(x)\,dx$
- Answer: $1$
- From: `form:ftc_sin` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int_{0}^{\pi/2} \sin(x)\,dx$
- Answer: $1$
- From: `form:ftc_sin` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int_{0}^{\pi/2} \sin(x)\,dx$
- Answer: $1$
- From: `form:ftc_sin` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int_{0}^{\pi/2} \sin(x)\,dx$
- Answer: $1$
- From: `form:ftc_sin` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int_{0}^{\pi/2} \sin(x)\,dx$
- Answer: $1$
- From: `form:ftc_sin` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots` · `effort:spec_high`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int_{0}^{4} x\,dx$
- Answer: $8$
- From: `form:ftc_linear` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots`
- Flags: C=4 · S=0 · amax=25 · shortfall=2

### C=4 · S=4

- Prompt: $\int_{0}^{4} x\,dx$
- Answer: $8$
- From: `form:ftc_linear` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots`
- Flags: C=4 · S=4 · amax=25 · shortfall=2

### C=4 · S=8

- Prompt: $\int_{0}^{4} x\,dx$
- Answer: $8$
- From: `form:ftc_linear` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots`
- Flags: C=4 · S=8 · amax=25 · shortfall=2

### C=4 · S=16

- Prompt: $\int_{0}^{4} x\,dx$
- Answer: $8$
- From: `form:ftc_linear` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots`
- Flags: C=4 · S=16 · amax=25 · shortfall=2

### C=4 · S=32

- Prompt: $\int_{0}^{4} x\,dx$
- Answer: $8$
- From: `form:ftc_linear` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots` · `effort:spec_high`
- Flags: C=4 · S=32 · amax=25 · shortfall=2

### C=8 · S=0

- Prompt: $\frac{d}{dx}\int_{0}^{2x + 1} x\,dx$
- Answer: $2\left(2x + 1\right)$
- From: `form:ftc_linear_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25 · shortfall=5

### C=8 · S=4

- Prompt: $\frac{d}{dx}\int_{0}^{2x + 1} x\,dx$
- Answer: $2\left(2x + 1\right)$
- From: `form:ftc_linear_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=8 · S=4 · amax=25 · shortfall=5

### C=8 · S=8

- Prompt: $\frac{d}{dx}\int_{0}^{2x + 1} x\,dx$
- Answer: $2\left(2x + 1\right)$
- From: `form:ftc_linear_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=8 · S=8 · amax=25 · shortfall=5

### C=8 · S=16

- Prompt: $\frac{d}{dx}\int_{0}^{2x + 1} x\,dx$
- Answer: $2\left(2x + 1\right)$
- From: `form:ftc_linear_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=8 · S=16 · amax=25 · shortfall=5

### C=8 · S=32

- Prompt: $\frac{d}{dx}\int_{0}^{2x + 1} x\,dx$
- Answer: $2\left(2x + 1\right)$
- From: `form:ftc_linear_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy` · `effort:spec_high`
- Flags: C=8 · S=32 · amax=25 · shortfall=5

### C=12 · S=0

- Prompt: $\frac{d}{dx}\int_{0}^{-x + 1} \sin(x)\,dx$
- Answer: $-\sin\left(-x + 1\right)$
- From: `form:ftc_sin_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=7.5

### C=12 · S=4

- Prompt: $\frac{d}{dx}\int_{0}^{-x + 1} \sin(x)\,dx$
- Answer: $-\sin\left(-x + 1\right)$
- From: `form:ftc_sin_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=12 · S=4 · amax=25 · shortfall=7.5

### C=12 · S=8

- Prompt: $\frac{d}{dx}\int_{0}^{-x + 1} \sin(x)\,dx$
- Answer: $-\sin\left(-x + 1\right)$
- From: `form:ftc_sin_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=12 · S=8 · amax=25 · shortfall=7.5

### C=12 · S=16

- Prompt: $\frac{d}{dx}\int_{0}^{-x + 1} \sin(x)\,dx$
- Answer: $-\sin\left(-x + 1\right)$
- From: `form:ftc_sin_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=12 · S=16 · amax=25 · shortfall=7.5

### C=12 · S=32

- Prompt: $\frac{d}{dx}\int_{0}^{-x + 1} \sin(x)\,dx$
- Answer: $-\sin\left(-x + 1\right)$
- From: `form:ftc_sin_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy` · `effort:spec_high`
- Flags: C=12 · S=32 · amax=25 · shortfall=7.5

### C=16 · S=0

- Prompt: $\frac{d}{dx}\int_{0}^{3x - 1} x\,dx$
- Answer: $3\left(3x - 1\right)$
- From: `form:ftc_linear_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=13

### C=16 · S=4

- Prompt: $\frac{d}{dx}\int_{0}^{3x - 1} x\,dx$
- Answer: $3\left(3x - 1\right)$
- From: `form:ftc_linear_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=16 · S=4 · amax=25 · shortfall=13

### C=16 · S=8

- Prompt: $\frac{d}{dx}\int_{0}^{3x - 1} x\,dx$
- Answer: $3\left(3x - 1\right)$
- From: `form:ftc_linear_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=16 · S=8 · amax=25 · shortfall=13

### C=16 · S=16

- Prompt: $\frac{d}{dx}\int_{0}^{3x - 1} x\,dx$
- Answer: $3\left(3x - 1\right)$
- From: `form:ftc_linear_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=16 · S=16 · amax=25 · shortfall=13

### C=16 · S=32

- Prompt: $\frac{d}{dx}\int_{0}^{3x - 1} x\,dx$
- Answer: $3\left(3x - 1\right)$
- From: `form:ftc_linear_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy` · `effort:spec_high`
- Flags: C=16 · S=32 · amax=25 · shortfall=13

### C=20 · S=0

- Prompt: $\frac{d}{dx}\int_{0}^{-2x + 2} x^{2}\,dx$
- Answer: $-2\left(-2x + 2\right)^{2}$
- From: `form:ftc_quad_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=17

### C=20 · S=4

- Prompt: $\frac{d}{dx}\int_{0}^{-2x + 2} x^{2}\,dx$
- Answer: $-2\left(-2x + 2\right)^{2}$
- From: `form:ftc_quad_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=20 · S=4 · amax=25 · shortfall=17

### C=20 · S=8

- Prompt: $\frac{d}{dx}\int_{0}^{-2x + 2} x^{2}\,dx$
- Answer: $-2\left(-2x + 2\right)^{2}$
- From: `form:ftc_quad_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=20 · S=8 · amax=25 · shortfall=17

### C=20 · S=16

- Prompt: $\frac{d}{dx}\int_{0}^{-2x + 2} x^{2}\,dx$
- Answer: $-2\left(-2x + 2\right)^{2}$
- From: `form:ftc_quad_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=20 · S=16 · amax=25 · shortfall=17

### C=20 · S=32

- Prompt: $\frac{d}{dx}\int_{0}^{-2x + 2} x^{2}\,dx$
- Answer: $-2\left(-2x + 2\right)^{2}$
- From: `form:ftc_quad_variable_upper` · `conceptual:ftc` · `conceptual:ftc_variable_upper` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy` · `effort:spec_high`
- Flags: C=20 · S=32 · amax=25 · shortfall=17

### C=25 · S=0

- Prompt: $\int_{0}^{2} x^{2}\,dx$
- Answer: $\frac{8}{3}$
- From: `form:ftc_quad` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=23

### C=25 · S=4

- Prompt: $\int_{0}^{2} x^{2}\,dx$
- Answer: $\frac{8}{3}$
- From: `form:ftc_quad` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=25 · S=4 · amax=25 · shortfall=23

### C=25 · S=8

- Prompt: $\int_{0}^{2} x^{2}\,dx$
- Answer: $\frac{8}{3}$
- From: `form:ftc_quad` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=25 · S=8 · amax=25 · shortfall=23

### C=25 · S=16

- Prompt: $\int_{0}^{2} x^{2}\,dx$
- Answer: $\frac{8}{3}$
- From: `form:ftc_quad` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=25 · S=16 · amax=25 · shortfall=23

### C=25 · S=32

- Prompt: $\int_{0}^{2} x^{2}\,dx$
- Answer: $\frac{8}{3}$
- From: `form:ftc_quad` · `conceptual:ftc` · `allow:trig` · `allow:exp` · `allow:roots` · `answer:unkind_or_messy` · `effort:spec_high`
- Flags: C=25 · S=32 · amax=25 · shortfall=23
