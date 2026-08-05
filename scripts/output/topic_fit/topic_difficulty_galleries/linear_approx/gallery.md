# Linear approximations

**type_id:** `calc_app_diff_linear_approximations` · **leaf:** `derivative_power_rule`  
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
| **C=0** | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=3.$ | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=3.$ | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=3.$ | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=3.$ | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=3.$ |
| **C=4** | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ |
| **C=8** | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$ | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$ | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$ | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$ | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$ |
| **C=12** | $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=2\text{ to estimate }f(\frac{21}{10}).$ | $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=2\text{ to estimate }f(\frac{21}{10}).$ | $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=2\text{ to estimate }f(\frac{21}{10}).$ | $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=2\text{ to estimate }f(\frac{21}{10}).$ | $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=2\text{ to estimate }f(\frac{21}{10}).$ |
| **C=16** | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$ | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$ | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$ | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$ | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$ |
| **C=20** | $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$ | $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$ | $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$ | $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$ | $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$ |
| **C=25** | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ |

## Grid (answer)

| C \ S | **S=0** | **S=4** | **S=8** | **S=16** | **S=32** |
|---|---|---|---|---|---|
| **C=0** | $L(x)=9+6(x-3)$ | $L(x)=9+6(x-3)$ | $L(x)=9+6(x-3)$ | $L(x)=9+6(x-3)$ | $L(x)=9+6(x-3)$ |
| **C=4** | $L(x)=4+4(x-2)$ | $L(x)=4+4(x-2)$ | $L(x)=4+4(x-2)$ | $L(x)=4+4(x-2)$ | $L(x)=4+4(x-2)$ |
| **C=8** | $L(x)=3+\frac{1}{6}(x-9)$ | $L(x)=3+\frac{1}{6}(x-9)$ | $L(x)=3+\frac{1}{6}(x-9)$ | $L(x)=3+\frac{1}{6}(x-9)$ | $L(x)=3+\frac{1}{6}(x-9)$ |
| **C=12** | $\frac{22}{5}$ | $\frac{22}{5}$ | $\frac{22}{5}$ | $\frac{22}{5}$ | $\frac{22}{5}$ |
| **C=16** | $L(x)=3+\frac{1}{6}(x-9)$ | $L(x)=3+\frac{1}{6}(x-9)$ | $L(x)=3+\frac{1}{6}(x-9)$ | $L(x)=3+\frac{1}{6}(x-9)$ | $L(x)=3+\frac{1}{6}(x-9)$ |
| **C=20** | $L(x)=1+x$ | $L(x)=1+x$ | $L(x)=1+x$ | $L(x)=1+x$ | $L(x)=1+x$ |
| **C=25** | $L(x)=4+4(x-2)$ | $L(x)=4+4(x-2)$ | $L(x)=4+4(x-2)$ | $L(x)=4+4(x-2)$ | $L(x)=4+4(x-2)$ |

## Cell detail

### C=0 · S=0

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=3.$
- Answer: $L(x)=9+6(x-3)$
- From: —
- Flags: —

### C=0 · S=4

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=3.$
- Answer: $L(x)=9+6(x-3)$
- From: —
- Flags: —

### C=0 · S=8

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=3.$
- Answer: $L(x)=9+6(x-3)$
- From: —
- Flags: —

### C=0 · S=16

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=3.$
- Answer: $L(x)=9+6(x-3)$
- From: —
- Flags: —

### C=0 · S=32

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=3.$
- Answer: $L(x)=9+6(x-3)$
- From: —
- Flags: —

### C=4 · S=0

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$
- Answer: $L(x)=4+4(x-2)$
- From: —
- Flags: —

### C=4 · S=4

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$
- Answer: $L(x)=4+4(x-2)$
- From: —
- Flags: —

### C=4 · S=8

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$
- Answer: $L(x)=4+4(x-2)$
- From: —
- Flags: —

### C=4 · S=16

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$
- Answer: $L(x)=4+4(x-2)$
- From: —
- Flags: —

### C=4 · S=32

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$
- Answer: $L(x)=4+4(x-2)$
- From: —
- Flags: —

### C=8 · S=0

- Prompt: $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$
- Answer: $L(x)=3+\frac{1}{6}(x-9)$
- From: —
- Flags: —

### C=8 · S=4

- Prompt: $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$
- Answer: $L(x)=3+\frac{1}{6}(x-9)$
- From: —
- Flags: —

### C=8 · S=8

- Prompt: $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$
- Answer: $L(x)=3+\frac{1}{6}(x-9)$
- From: —
- Flags: —

### C=8 · S=16

- Prompt: $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$
- Answer: $L(x)=3+\frac{1}{6}(x-9)$
- From: —
- Flags: —

### C=8 · S=32

- Prompt: $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$
- Answer: $L(x)=3+\frac{1}{6}(x-9)$
- From: —
- Flags: —

### C=12 · S=0

- Prompt: $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=2\text{ to estimate }f(\frac{21}{10}).$
- Answer: $\frac{22}{5}$
- From: —
- Flags: —

### C=12 · S=4

- Prompt: $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=2\text{ to estimate }f(\frac{21}{10}).$
- Answer: $\frac{22}{5}$
- From: —
- Flags: —

### C=12 · S=8

- Prompt: $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=2\text{ to estimate }f(\frac{21}{10}).$
- Answer: $\frac{22}{5}$
- From: —
- Flags: —

### C=12 · S=16

- Prompt: $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=2\text{ to estimate }f(\frac{21}{10}).$
- Answer: $\frac{22}{5}$
- From: —
- Flags: —

### C=12 · S=32

- Prompt: $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=2\text{ to estimate }f(\frac{21}{10}).$
- Answer: $\frac{22}{5}$
- From: —
- Flags: —

### C=16 · S=0

- Prompt: $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$
- Answer: $L(x)=3+\frac{1}{6}(x-9)$
- From: —
- Flags: —

### C=16 · S=4

- Prompt: $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$
- Answer: $L(x)=3+\frac{1}{6}(x-9)$
- From: —
- Flags: —

### C=16 · S=8

- Prompt: $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$
- Answer: $L(x)=3+\frac{1}{6}(x-9)$
- From: —
- Flags: —

### C=16 · S=16

- Prompt: $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$
- Answer: $L(x)=3+\frac{1}{6}(x-9)$
- From: —
- Flags: —

### C=16 · S=32

- Prompt: $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$
- Answer: $L(x)=3+\frac{1}{6}(x-9)$
- From: —
- Flags: —

### C=20 · S=0

- Prompt: $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$
- Answer: $L(x)=1+x$
- From: —
- Flags: —

### C=20 · S=4

- Prompt: $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$
- Answer: $L(x)=1+x$
- From: —
- Flags: —

### C=20 · S=8

- Prompt: $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$
- Answer: $L(x)=1+x$
- From: —
- Flags: —

### C=20 · S=16

- Prompt: $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$
- Answer: $L(x)=1+x$
- From: —
- Flags: —

### C=20 · S=32

- Prompt: $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$
- Answer: $L(x)=1+x$
- From: —
- Flags: —

### C=25 · S=0

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$
- Answer: $L(x)=4+4(x-2)$
- From: —
- Flags: —

### C=25 · S=4

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$
- Answer: $L(x)=4+4(x-2)$
- From: —
- Flags: —

### C=25 · S=8

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$
- Answer: $L(x)=4+4(x-2)$
- From: —
- Flags: —

### C=25 · S=16

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$
- Answer: $L(x)=4+4(x-2)$
- From: —
- Flags: —

### C=25 · S=32

- Prompt: $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$
- Answer: $L(x)=4+4(x-2)$
- From: —
- Flags: —
