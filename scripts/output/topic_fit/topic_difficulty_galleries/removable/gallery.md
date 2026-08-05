# Limits — removable discontinuities

**type_id:** `calc_limits_at_removable_discontinuities` · **leaf:** `limit_removable`  
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
| **C=0** | $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$ | $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$ | $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$ | $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$ | $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$ |
| **C=4** | $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$ | $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$ | $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$ | $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$ | $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$ |
| **C=8** | $\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}$ | $\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}$ | $\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}$ | $\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}$ | $\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}$ |
| **C=12** | $\lim_{x \to 1} \frac{x^{2} - 1}{x-1}$ | $\lim_{x \to 1} \frac{x^{2} - 1}{x-1}$ | $\lim_{x \to 1} \frac{x^{2} - 1}{x-1}$ | $\lim_{x \to 1} \frac{x^{2} - 1}{x-1}$ | $\lim_{x \to 1} \frac{x^{2} - 1}{x-1}$ |
| **C=16** | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ |
| **C=20** | $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$ | $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$ | $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$ | $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$ | $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$ |
| **C=25** | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $4$ | $4$ | $4$ | $4$ | $4$ |
| **C=4** | $4$ | $4$ | $4$ | $4$ | $4$ |
| **C=8** | $\frac{1}{2\sqrt{3}}$ | $\frac{1}{2\sqrt{3}}$ | $\frac{1}{2\sqrt{3}}$ | $\frac{1}{2\sqrt{3}}$ | $\frac{1}{2\sqrt{3}}$ |
| **C=12** | $2$ | $2$ | $2$ | $2$ | $2$ |
| **C=16** | $\frac{1}{2\sqrt{4}}$ | $\frac{1}{2\sqrt{4}}$ | $\frac{1}{2\sqrt{4}}$ | $\frac{1}{2\sqrt{4}}$ | $\frac{1}{2\sqrt{4}}$ |
| **C=20** | $\frac{1}{2\sqrt{2}}$ | $\frac{1}{2\sqrt{2}}$ | $\frac{1}{2\sqrt{2}}$ | $\frac{1}{2\sqrt{2}}$ | $\frac{1}{2\sqrt{2}}$ |
| **C=25** | $\frac{1}{2\sqrt{4}}$ | $\frac{1}{2\sqrt{4}}$ | $\frac{1}{2\sqrt{4}}$ | $\frac{1}{2\sqrt{4}}$ | $\frac{1}{2\sqrt{4}}$ |

## Cell detail

### C=0 · S=0

- Prompt: $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$
- Answer: $4$
- From: `form:removable_diff_sq` · `conceptual:factor_cancel` · `allow:roots`
- Flags: C=0 · S=0 · amax=25

### C=0 · S=4

- Prompt: $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$
- Answer: $4$
- From: `form:removable_diff_sq` · `conceptual:factor_cancel` · `allow:roots`
- Flags: C=0 · S=4 · amax=25

### C=0 · S=8

- Prompt: $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$
- Answer: $4$
- From: `form:removable_diff_sq` · `conceptual:factor_cancel` · `allow:roots`
- Flags: C=0 · S=8 · amax=25

### C=0 · S=16

- Prompt: $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$
- Answer: $4$
- From: `form:removable_diff_sq` · `conceptual:factor_cancel` · `allow:roots`
- Flags: C=0 · S=16 · amax=25

### C=0 · S=32

- Prompt: $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$
- Answer: $4$
- From: `form:removable_diff_sq` · `conceptual:factor_cancel` · `allow:roots` · `effort:spec_high`
- Flags: C=0 · S=32 · amax=25

### C=4 · S=0

- Prompt: $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$
- Answer: $4$
- From: `form:removable_diff_sq` · `conceptual:factor_cancel` · `allow:roots`
- Flags: C=4 · S=0 · amax=25 · shortfall=1

### C=4 · S=4

- Prompt: $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$
- Answer: $4$
- From: `form:removable_diff_sq` · `conceptual:factor_cancel` · `allow:roots`
- Flags: C=4 · S=4 · amax=25 · shortfall=1

### C=4 · S=8

- Prompt: $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$
- Answer: $4$
- From: `form:removable_diff_sq` · `conceptual:factor_cancel` · `allow:roots`
- Flags: C=4 · S=8 · amax=25 · shortfall=1

### C=4 · S=16

- Prompt: $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$
- Answer: $4$
- From: `form:removable_diff_sq` · `conceptual:factor_cancel` · `allow:roots`
- Flags: C=4 · S=16 · amax=25 · shortfall=1

### C=4 · S=32

- Prompt: $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$
- Answer: $4$
- From: `form:removable_diff_sq` · `conceptual:factor_cancel` · `allow:roots` · `effort:spec_high`
- Flags: C=4 · S=32 · amax=25 · shortfall=1

### C=8 · S=0

- Prompt: $\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}$
- Answer: $\frac{1}{2\sqrt{3}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=8 · S=0 · amax=25

### C=8 · S=4

- Prompt: $\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}$
- Answer: $\frac{1}{2\sqrt{3}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=8 · S=4 · amax=25

### C=8 · S=8

- Prompt: $\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}$
- Answer: $\frac{1}{2\sqrt{3}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=8 · S=8 · amax=25

### C=8 · S=16

- Prompt: $\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}$
- Answer: $\frac{1}{2\sqrt{3}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=8 · S=16 · amax=25

### C=8 · S=32

- Prompt: $\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}$
- Answer: $\frac{1}{2\sqrt{3}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy` · `effort:spec_high`
- Flags: C=8 · S=32 · amax=25

### C=12 · S=0

- Prompt: $\lim_{x \to 1} \frac{x^{2} - 1}{x-1}$
- Answer: $2$
- From: `form:removable_quad_shared` · `conceptual:factor_cancel` · `allow:roots`
- Flags: C=12 · S=0 · amax=25 · shortfall=6

### C=12 · S=4

- Prompt: $\lim_{x \to 1} \frac{x^{2} - 1}{x-1}$
- Answer: $2$
- From: `form:removable_quad_shared` · `conceptual:factor_cancel` · `allow:roots`
- Flags: C=12 · S=4 · amax=25 · shortfall=6

### C=12 · S=8

- Prompt: $\lim_{x \to 1} \frac{x^{2} - 1}{x-1}$
- Answer: $2$
- From: `form:removable_quad_shared` · `conceptual:factor_cancel` · `allow:roots`
- Flags: C=12 · S=8 · amax=25 · shortfall=6

### C=12 · S=16

- Prompt: $\lim_{x \to 1} \frac{x^{2} - 1}{x-1}$
- Answer: $2$
- From: `form:removable_quad_shared` · `conceptual:factor_cancel` · `allow:roots`
- Flags: C=12 · S=16 · amax=25 · shortfall=6

### C=12 · S=32

- Prompt: $\lim_{x \to 1} \frac{x^{2} - 1}{x-1}$
- Answer: $2$
- From: `form:removable_quad_shared` · `conceptual:factor_cancel` · `allow:roots` · `effort:spec_high`
- Flags: C=12 · S=32 · amax=25 · shortfall=6

### C=16 · S=0

- Prompt: $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$
- Answer: $\frac{1}{2\sqrt{4}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=16 · S=0 · amax=25 · shortfall=12

### C=16 · S=4

- Prompt: $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$
- Answer: $\frac{1}{2\sqrt{4}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=16 · S=4 · amax=25 · shortfall=12

### C=16 · S=8

- Prompt: $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$
- Answer: $\frac{1}{2\sqrt{4}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=16 · S=8 · amax=25 · shortfall=12

### C=16 · S=16

- Prompt: $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$
- Answer: $\frac{1}{2\sqrt{4}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=16 · S=16 · amax=25 · shortfall=12

### C=16 · S=32

- Prompt: $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$
- Answer: $\frac{1}{2\sqrt{4}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy` · `effort:spec_high`
- Flags: C=16 · S=32 · amax=25 · shortfall=12

### C=20 · S=0

- Prompt: $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$
- Answer: $\frac{1}{2\sqrt{2}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=20 · S=0 · amax=25 · shortfall=11

### C=20 · S=4

- Prompt: $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$
- Answer: $\frac{1}{2\sqrt{2}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=20 · S=4 · amax=25 · shortfall=11

### C=20 · S=8

- Prompt: $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$
- Answer: $\frac{1}{2\sqrt{2}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=20 · S=8 · amax=25 · shortfall=11

### C=20 · S=16

- Prompt: $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$
- Answer: $\frac{1}{2\sqrt{2}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=20 · S=16 · amax=25 · shortfall=11

### C=20 · S=32

- Prompt: $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$
- Answer: $\frac{1}{2\sqrt{2}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy` · `effort:spec_high`
- Flags: C=20 · S=32 · amax=25 · shortfall=11

### C=25 · S=0

- Prompt: $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$
- Answer: $\frac{1}{2\sqrt{4}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=25 · S=0 · amax=25 · shortfall=16

### C=25 · S=4

- Prompt: $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$
- Answer: $\frac{1}{2\sqrt{4}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=25 · S=4 · amax=25 · shortfall=16

### C=25 · S=8

- Prompt: $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$
- Answer: $\frac{1}{2\sqrt{4}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=25 · S=8 · amax=25 · shortfall=16

### C=25 · S=16

- Prompt: $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$
- Answer: $\frac{1}{2\sqrt{4}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy`
- Flags: C=25 · S=16 · amax=25 · shortfall=16

### C=25 · S=32

- Prompt: $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$
- Answer: $\frac{1}{2\sqrt{4}}$
- From: `form:removable_rationalize` · `conceptual:rationalize` · `allow:roots` · `answer:unkind_or_messy` · `effort:spec_high`
- Flags: C=25 · S=32 · amax=25 · shortfall=16
