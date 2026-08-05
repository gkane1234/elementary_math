# Integrals — partial fractions

**type_id:** `calc_indef_int_partial_fractions` · **leaf:** `integration_by_parts`  
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
| **C=0** | $\int \frac{4x + 2}{x^{2} + 2x}\,dx$ | $\int  \frac{-\left(2-x\right)\frac{4x + 2}{x^{2} + 2x}}{-\left(2-x\right)}\,dx$ | $\int  \left(\frac{4x + 2}{x^{2} + 2x}+4-4\right)+\left(3x\right)-\left(3x\right)\,dx$ | $\int  \left(\frac{-\left(1-x\right)\frac{4x + 2}{x^{2} + 2x}}{-\left(1-x\right)}+4-4\right)+4-4\,dx$ | $\int  \left(\left(\left(\frac{4x + 2}{x^{2} + 2x}+\left(3x+3\right)-\left(3x+3\right)\right)+5-5\right)+6\right)-6\,dx$ |
| **C=4** | $\int \frac{-6}{x^{2} - x - 2}\,dx$ | $\int  \frac{3\left(x+2\right)\frac{-6}{x^{2} - x - 2}}{3\left(x+2\right)}\,dx$ | $\int  \left(\left(-\left(-\frac{-6}{x^{2} - x - 2}\right)\right)+\left(-2x+2\right)\right)-\left(-2x+2\right)\,dx$ | $\int  \left(\frac{2\left(x-1\right)\left(\frac{-6}{x^{2} - x - 2}+2-2\right)}{2\left(x-1\right)}+\left(x-1\right)\right)-\left(x-1\right)\,dx$ | $\int  \left(\left(\left(\frac{-6}{x^{2} - x - 2}+\left(x-2\right)-\left(x-2\right)\right)+\left(x-1\right)\right)-\left(x-1\right)+\left(2x+3\right)\right)-\left(2x+3\right)\,dx$ |
| **C=8** | $\int \frac{-2x}{2x^{2} + 2}\,dx$ | $\int  \left(\frac{-2x}{2x^{2} + 2}+6\right)-6\,dx$ | $\int  \left(\frac{-2x}{2x^{2} + 2}+\left(2x+1\right)\right)-\left(2x+1\right)+2-2\,dx$ | $\int  \left(-\left(-\left(\frac{-2x}{2x^{2} + 2}+\left(x+2\right)\right)-\left(x+2\right)\right)\right)+\left(3x-2\right)-\left(3x-2\right)\,dx$ | $\int  \left(\left(\left(\frac{\left(x+2\right)\frac{-2x}{2x^{2} + 2}}{x+2}+6\right)-6\right)+\left(2x-2\right)\right)-\left(2x-2\right)\,dx$ |
| **C=12** | $\int \frac{-4}{x^{2} + 1}\,dx$ | $\int  \frac{-4}{x^{2} + 1}+\left(-2x\right)-\left(-2x\right)\,dx$ | $\int  \frac{\left(x-3\right)\frac{-4}{x^{2} + 1}}{x-3}+\left(2x\right)-\left(2x\right)\,dx$ | $\int  \frac{2\left(x-2\right)\left(\left(\left(-\left(-\frac{-4}{x^{2} + 1}\right)\right)+4\right)-4\right)}{2\left(x-2\right)}\,dx$ | $\int  -\left(-\left(\left(\frac{-4}{x^{2} + 1}+2\right)-2\right)+\left(3x+3\right)-\left(3x+3\right)\right)\,dx$ |
| **C=16** | $\int \frac{-x + 7}{\left(x - 3\right)^{2}}\,dx$ | $\int  \frac{-\left(2-x\right)\frac{-x + 7}{\left(x - 3\right)^{2}}}{-\left(2-x\right)}\,dx$ | $\int  \left(\left(\frac{-x + 7}{\left(x - 3\right)^{2}}+\left(2x\right)\right)-\left(2x\right)+6\right)-6\,dx$ | $\int  \left(\left(\frac{-x + 7}{\left(x - 3\right)^{2}}+3-3\right)+\left(-x+2\right)\right)-\left(-x+2\right)+\left(-x-2\right)-\left(-x-2\right)\,dx$ | $\int  \frac{3\left(x-1\right)\left(\frac{-x + 7}{\left(x - 3\right)^{2}}+\left(-2x-1\right)\right)-\left(-2x-1\right)}{3\left(x-1\right)}+\left(x-2\right)-\left(x-2\right)\,dx$ |
| **C=20** | $\int \frac{4x^{2} + 2x + 28}{x^{3} + x^{2} + 9x + 9}\,dx$ | $\int  \left(\frac{4x^{2} + 2x + 28}{x^{3} + x^{2} + 9x + 9}+\left(3x\right)\right)-\left(3x\right)\,dx$ | $\int  \left(\frac{4x^{2} + 2x + 28}{x^{3} + x^{2} + 9x + 9}+\left(3x\right)\right)-\left(3x\right)+\left(2x\right)-\left(2x\right)\,dx$ | $\int  \left(-\left(-\left(\frac{4x^{2} + 2x + 28}{x^{3} + x^{2} + 9x + 9}+6-6\right)\right)\right)+1-1\,dx$ | $\int  \frac{2\left(x+2\right)\left(-\left(-\frac{4x^{2} + 2x + 28}{x^{3} + x^{2} + 9x + 9}\right)\right)}{2\left(x+2\right)}+1-1\,dx$ |
| **C=25** | $\int \frac{8x^{2} + 2x + 80}{x^{3} + 4x^{2} + 9x + 36}\,dx$ | $\int  \frac{\left(x-3\right)\frac{8x^{2} + 2x + 80}{x^{3} + 4x^{2} + 9x + 36}}{x-3}\,dx$ | $\int  \left(-\left(-\frac{8x^{2} + 2x + 80}{x^{3} + 4x^{2} + 9x + 36}\right)\right)+2-2\,dx$ | $\int  \left(\frac{\left(x+3\right)\frac{8x^{2} + 2x + 80}{x^{3} + 4x^{2} + 9x + 36}}{x+3}+2-2\right)+1-1\,dx$ | $\int  \frac{\left(x-1\right)\left(\left(-\left(-\frac{8x^{2} + 2x + 80}{x^{3} + 4x^{2} + 9x + 36}\right)\right)+\left(-x-1\right)\right)-\left(-x-1\right)}{x-1}\,dx$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $\ln|x|+3\ln|x + 2|+C$ | $\ln|x|+3\ln|x + 2|+C$ | $\ln|x|+3\ln|x + 2|+C$ | $\ln|x|+3\ln|x + 2|+C$ | $\ln|x|+3\ln|x + 2|+C$ |
| **C=4** | $2\ln|x + 1|-2\ln|x - 2|+C$ | $2\ln|x + 1|-2\ln|x - 2|+C$ | $2\ln|x + 1|-2\ln|x - 2|+C$ | $2\ln|x + 1|-2\ln|x - 2|+C$ | $2\ln|x + 1|-2\ln|x - 2|+C$ |
| **C=8** | $-\frac{1}{2}\ln|x^{2}+1|+C$ | $-\frac{1}{2}\ln|x^{2}+1|+C$ | $-\frac{1}{2}\ln|x^{2}+1|+C$ | $-\frac{1}{2}\ln|x^{2}+1|+C$ | $-\frac{1}{2}\ln|x^{2}+1|+C$ |
| **C=12** | $-4\arctan(x)+C$ | $-4\arctan(x)+C$ | $-4\arctan(x)+C$ | $-4\arctan(x)+C$ | $-4\arctan(x)+C$ |
| **C=16** | $-\ln|x - 3|-4\frac{1}{x - 3}+C$ | $-\ln|x - 3|-4\frac{1}{x - 3}+C$ | $-\ln|x - 3|-4\frac{1}{x - 3}+C$ | $-\ln|x - 3|-4\frac{1}{x - 3}+C$ | $-\ln|x - 3|-4\frac{1}{x - 3}+C$ |
| **C=20** | $3\ln|x + 1|+\frac{1}{2}\ln|x^{2}+9|+\frac{1}{3}\arctan(\frac{x}{3})+C$ | $3\ln|x + 1|+\frac{1}{2}\ln|x^{2}+9|+\frac{1}{3}\arctan(\frac{x}{3})+C$ | $3\ln|x + 1|+\frac{1}{2}\ln|x^{2}+9|+\frac{1}{3}\arctan(\frac{x}{3})+C$ | $3\ln|x + 1|+\frac{1}{2}\ln|x^{2}+9|+\frac{1}{3}\arctan(\frac{x}{3})+C$ | $3\ln|x + 1|+\frac{1}{2}\ln|x^{2}+9|+\frac{1}{3}\arctan(\frac{x}{3})+C$ |
| **C=25** | $8\ln|x + 4|+\frac{2}{3}\arctan(\frac{x}{3})+C$ | $8\ln|x + 4|+\frac{2}{3}\arctan(\frac{x}{3})+C$ | $8\ln|x + 4|+\frac{2}{3}\arctan(\frac{x}{3})+C$ | $8\ln|x + 4|+\frac{2}{3}\arctan(\frac{x}{3})+C$ | $8\ln|x + 4|+\frac{2}{3}\arctan(\frac{x}{3})+C$ |

## Cell detail

### C=0 · S=0

- Prompt: $\int \frac{4x + 2}{x^{2} + 2x}\,dx$
- Answer: $\ln|x|+3\ln|x + 2|+C$
- From: `form:distinct_linear_2` · `conceptual:pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\int  \frac{-\left(2-x\right)\frac{4x + 2}{x^{2} + 2x}}{-\left(2-x\right)}\,dx$
- Answer: $\ln|x|+3\ln|x + 2|+C$
- From: `form:distinct_linear_2` · `conceptual:pfd` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\int  \left(\frac{4x + 2}{x^{2} + 2x}+4-4\right)+\left(3x\right)-\left(3x\right)\,dx$
- Answer: $\ln|x|+3\ln|x + 2|+C$
- From: `form:distinct_linear_2` · `conceptual:pfd` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\int  \left(\frac{-\left(1-x\right)\frac{4x + 2}{x^{2} + 2x}}{-\left(1-x\right)}+4-4\right)+4-4\,dx$
- Answer: $\ln|x|+3\ln|x + 2|+C$
- From: `form:distinct_linear_2` · `conceptual:pfd` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\int  \left(\left(\left(\frac{4x + 2}{x^{2} + 2x}+\left(3x+3\right)-\left(3x+3\right)\right)+5-5\right)+6\right)-6\,dx$
- Answer: $\ln|x|+3\ln|x + 2|+C$
- From: `form:distinct_linear_2` · `conceptual:pfd` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\int \frac{-6}{x^{2} - x - 2}\,dx$
- Answer: $2\ln|x + 1|-2\ln|x - 2|+C$
- From: `form:distinct_linear_2` · `conceptual:pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=0 · amax=25 · shortfall=0.5

### C=4 · S=4

- Prompt: $\int  \frac{3\left(x+2\right)\frac{-6}{x^{2} - x - 2}}{3\left(x+2\right)}\,dx$
- Answer: $2\ln|x + 1|-2\ln|x - 2|+C$
- From: `form:distinct_linear_2` · `conceptual:pfd` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=4 · S=4 · amax=25

### C=4 · S=8

- Prompt: $\int  \left(\left(-\left(-\frac{-6}{x^{2} - x - 2}\right)\right)+\left(-2x+2\right)\right)-\left(-2x+2\right)\,dx$
- Answer: $2\ln|x + 1|-2\ln|x - 2|+C$
- From: `form:distinct_linear_2` · `conceptual:pfd` · `effort:double_neg` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=4 · S=8 · amax=25

### C=4 · S=16

- Prompt: $\int  \left(\frac{2\left(x-1\right)\left(\frac{-6}{x^{2} - x - 2}+2-2\right)}{2\left(x-1\right)}+\left(x-1\right)\right)-\left(x-1\right)\,dx$
- Answer: $2\ln|x + 1|-2\ln|x - 2|+C$
- From: `form:distinct_linear_2` · `conceptual:pfd` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=4 · S=16 · amax=25

### C=4 · S=32

- Prompt: $\int  \left(\left(\left(\frac{-6}{x^{2} - x - 2}+\left(x-2\right)-\left(x-2\right)\right)+\left(x-1\right)\right)-\left(x-1\right)+\left(2x+3\right)\right)-\left(2x+3\right)\,dx$
- Answer: $2\ln|x + 1|-2\ln|x - 2|+C$
- From: `form:distinct_linear_2` · `conceptual:pfd` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=4 · S=32 · amax=25

### C=8 · S=0

- Prompt: $\int \frac{-2x}{2x^{2} + 2}\,dx$
- Answer: $-\frac{1}{2}\ln|x^{2}+1|+C$
- From: `form:irreducible_quad_ln` · `conceptual:pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25 · shortfall=2.5

### C=8 · S=4

- Prompt: $\int  \left(\frac{-2x}{2x^{2} + 2}+6\right)-6\,dx$
- Answer: $-\frac{1}{2}\ln|x^{2}+1|+C$
- From: `form:irreducible_quad_ln` · `conceptual:pfd` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_const`
- Flags: C=8 · S=4 · amax=25 · shortfall=1.5

### C=8 · S=8

- Prompt: $\int  \left(\frac{-2x}{2x^{2} + 2}+\left(2x+1\right)\right)-\left(2x+1\right)+2-2\,dx$
- Answer: $-\frac{1}{2}\ln|x^{2}+1|+C$
- From: `form:irreducible_quad_ln` · `conceptual:pfd` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=8 · amax=25 · shortfall=0.5

### C=8 · S=16

- Prompt: $\int  \left(-\left(-\left(\frac{-2x}{2x^{2} + 2}+\left(x+2\right)\right)-\left(x+2\right)\right)\right)+\left(3x-2\right)-\left(3x-2\right)\,dx$
- Answer: $-\frac{1}{2}\ln|x^{2}+1|+C$
- From: `form:irreducible_quad_ln` · `conceptual:pfd` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\int  \left(\left(\left(\frac{\left(x+2\right)\frac{-2x}{2x^{2} + 2}}{x+2}+6\right)-6\right)+\left(2x-2\right)\right)-\left(2x-2\right)\,dx$
- Answer: $-\frac{1}{2}\ln|x^{2}+1|+C$
- From: `form:irreducible_quad_ln` · `conceptual:pfd` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\int \frac{-4}{x^{2} + 1}\,dx$
- Answer: $-4\arctan(x)+C$
- From: `form:irreducible_quad_arctan` · `conceptual:pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=0 · amax=25 · shortfall=6.5

### C=12 · S=4

- Prompt: $\int  \frac{-4}{x^{2} + 1}+\left(-2x\right)-\left(-2x\right)\,dx$
- Answer: $-4\arctan(x)+C$
- From: `form:irreducible_quad_arctan` · `conceptual:pfd` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=12 · S=4 · amax=25 · shortfall=5.5

### C=12 · S=8

- Prompt: $\int  \frac{\left(x-3\right)\frac{-4}{x^{2} + 1}}{x-3}+\left(2x\right)-\left(2x\right)\,dx$
- Answer: $-4\arctan(x)+C$
- From: `form:irreducible_quad_arctan` · `conceptual:pfd` · `prereq:cancel_quot_bait` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=12 · S=8 · amax=25 · shortfall=4.5

### C=12 · S=16

- Prompt: $\int  \frac{2\left(x-2\right)\left(\left(\left(-\left(-\frac{-4}{x^{2} + 1}\right)\right)+4\right)-4\right)}{2\left(x-2\right)}\,dx$
- Answer: $-4\arctan(x)+C$
- From: `form:irreducible_quad_arctan` · `conceptual:pfd` · `effort:double_neg` · `effort:add_cancel_const` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=16 · amax=25 · shortfall=3.5

### C=12 · S=32

- Prompt: $\int  -\left(-\left(\left(\frac{-4}{x^{2} + 1}+2\right)-2\right)+\left(3x+3\right)-\left(3x+3\right)\right)\,dx$
- Answer: $-4\arctan(x)+C$
- From: `form:irreducible_quad_arctan` · `conceptual:pfd` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=12 · S=32 · amax=25 · shortfall=3.5

### C=16 · S=0

- Prompt: $\int \frac{-x + 7}{\left(x - 3\right)^{2}}\,dx$
- Answer: $-\ln|x - 3|-4\frac{1}{x - 3}+C$
- From: `form:repeated_linear_square` · `conceptual:pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=12.5

### C=16 · S=4

- Prompt: $\int  \frac{-\left(2-x\right)\frac{-x + 7}{\left(x - 3\right)^{2}}}{-\left(2-x\right)}\,dx$
- Answer: $-\ln|x - 3|-4\frac{1}{x - 3}+C$
- From: `form:repeated_linear_square` · `conceptual:pfd` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=16 · S=4 · amax=25 · shortfall=11.5

### C=16 · S=8

- Prompt: $\int  \left(\left(\frac{-x + 7}{\left(x - 3\right)^{2}}+\left(2x\right)\right)-\left(2x\right)+6\right)-6\,dx$
- Answer: $-\ln|x - 3|-4\frac{1}{x - 3}+C$
- From: `form:repeated_linear_square` · `conceptual:pfd` · `effort:add_cancel_linear` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=8 · amax=25 · shortfall=10.5

### C=16 · S=16

- Prompt: $\int  \left(\left(\frac{-x + 7}{\left(x - 3\right)^{2}}+3-3\right)+\left(-x+2\right)\right)-\left(-x+2\right)+\left(-x-2\right)-\left(-x-2\right)\,dx$
- Answer: $-\ln|x - 3|-4\frac{1}{x - 3}+C$
- From: `form:repeated_linear_square` · `conceptual:pfd` · `effort:add_cancel_const` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=16 · amax=25 · shortfall=9.5

### C=16 · S=32

- Prompt: $\int  \frac{3\left(x-1\right)\left(\frac{-x + 7}{\left(x - 3\right)^{2}}+\left(-2x-1\right)\right)-\left(-2x-1\right)}{3\left(x-1\right)}+\left(x-2\right)-\left(x-2\right)\,dx$
- Answer: $-\ln|x - 3|-4\frac{1}{x - 3}+C$
- From: `form:repeated_linear_square` · `conceptual:pfd` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=16 · S=32 · amax=25 · shortfall=9.5

### C=20 · S=0

- Prompt: $\int \frac{4x^{2} + 2x + 28}{x^{3} + x^{2} + 9x + 9}\,dx$
- Answer: $3\ln|x + 1|+\frac{1}{2}\ln|x^{2}+9|+\frac{1}{3}\arctan(\frac{x}{3})+C$
- From: `form:mixed_linear_quad` · `conceptual:pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=14.5

### C=20 · S=4

- Prompt: $\int  \left(\frac{4x^{2} + 2x + 28}{x^{3} + x^{2} + 9x + 9}+\left(3x\right)\right)-\left(3x\right)\,dx$
- Answer: $3\ln|x + 1|+\frac{1}{2}\ln|x^{2}+9|+\frac{1}{3}\arctan(\frac{x}{3})+C$
- From: `form:mixed_linear_quad` · `conceptual:pfd` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=20 · S=4 · amax=25 · shortfall=13.5

### C=20 · S=8

- Prompt: $\int  \left(\frac{4x^{2} + 2x + 28}{x^{3} + x^{2} + 9x + 9}+\left(3x\right)\right)-\left(3x\right)+\left(2x\right)-\left(2x\right)\,dx$
- Answer: $3\ln|x + 1|+\frac{1}{2}\ln|x^{2}+9|+\frac{1}{3}\arctan(\frac{x}{3})+C$
- From: `form:mixed_linear_quad` · `conceptual:pfd` · `effort:add_cancel_linear` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `effort:add_cancel_linear`
- Flags: C=20 · S=8 · amax=25 · shortfall=12.5

### C=20 · S=16

- Prompt: $\int  \left(-\left(-\left(\frac{4x^{2} + 2x + 28}{x^{3} + x^{2} + 9x + 9}+6-6\right)\right)\right)+1-1\,dx$
- Answer: $3\ln|x + 1|+\frac{1}{2}\ln|x^{2}+9|+\frac{1}{3}\arctan(\frac{x}{3})+C$
- From: `form:mixed_linear_quad` · `conceptual:pfd` · `effort:add_cancel_const` · `effort:double_neg` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=20 · S=16 · amax=25 · shortfall=11.5

### C=20 · S=32

- Prompt: $\int  \frac{2\left(x+2\right)\left(-\left(-\frac{4x^{2} + 2x + 28}{x^{3} + x^{2} + 9x + 9}\right)\right)}{2\left(x+2\right)}+1-1\,dx$
- Answer: $3\ln|x + 1|+\frac{1}{2}\ln|x^{2}+9|+\frac{1}{3}\arctan(\frac{x}{3})+C$
- From: `form:mixed_linear_quad` · `conceptual:pfd` · `effort:double_neg` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=20 · S=32 · amax=25 · shortfall=11.5

### C=25 · S=0

- Prompt: $\int \frac{8x^{2} + 2x + 80}{x^{3} + 4x^{2} + 9x + 36}\,dx$
- Answer: $8\ln|x + 4|+\frac{2}{3}\arctan(\frac{x}{3})+C$
- From: `form:mixed_linear_quad` · `conceptual:pfd` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=19.5

### C=25 · S=4

- Prompt: $\int  \frac{\left(x-3\right)\frac{8x^{2} + 2x + 80}{x^{3} + 4x^{2} + 9x + 36}}{x-3}\,dx$
- Answer: $8\ln|x + 4|+\frac{2}{3}\arctan(\frac{x}{3})+C$
- From: `form:mixed_linear_quad` · `conceptual:pfd` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy` · `prereq:cancel_quot_bait`
- Flags: C=25 · S=4 · amax=25 · shortfall=18.5

### C=25 · S=8

- Prompt: $\int  \left(-\left(-\frac{8x^{2} + 2x + 80}{x^{3} + 4x^{2} + 9x + 36}\right)\right)+2-2\,dx$
- Answer: $8\ln|x + 4|+\frac{2}{3}\arctan(\frac{x}{3})+C$
- From: `form:mixed_linear_quad` · `conceptual:pfd` · `effort:double_neg` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=8 · amax=25 · shortfall=17.5

### C=25 · S=16

- Prompt: $\int  \left(\frac{\left(x+3\right)\frac{8x^{2} + 2x + 80}{x^{3} + 4x^{2} + 9x + 36}}{x+3}+2-2\right)+1-1\,dx$
- Answer: $8\ln|x + 4|+\frac{2}{3}\arctan(\frac{x}{3})+C$
- From: `form:mixed_linear_quad` · `conceptual:pfd` · `prereq:cancel_quot_bait` · `effort:add_cancel_const` · `allow:trig` · `allow:exp` · `allow:log` · `answer:unkind_or_messy`
- Flags: C=25 · S=16 · amax=25 · shortfall=16.5

### C=25 · S=32

- Prompt: $\int  \frac{\left(x-1\right)\left(\left(-\left(-\frac{8x^{2} + 2x + 80}{x^{3} + 4x^{2} + 9x + 36}\right)\right)+\left(-x-1\right)\right)-\left(-x-1\right)}{x-1}\,dx$
- Answer: $8\ln|x + 4|+\frac{2}{3}\arctan(\frac{x}{3})+C$
- From: `form:mixed_linear_quad` · `conceptual:pfd` · `effort:double_neg` · `effort:add_cancel_linear` · `prereq:cancel_quot_bait` · `allow:trig` · `allow:exp` · `allow:log`
- Flags: C=25 · S=32 · amax=25 · shortfall=16.5
