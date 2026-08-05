# Literal equations

Primitive-linear audit for `literal_equations` across D=[0.0, 3.0, 6.0, 10.0, 14.0, 20.0].

| D | Prompt | Answer | Upgrades |
|--:|--------|--------|----------|
| 0 | $A = \ell w \quad \text{Solve for } w.$ | $w = \frac{A}{\ell}$ | — |
| 0 | $I = p r t \quad \text{Solve for } r.$ | $r = \frac{I}{p t}$ | — |
| 0 | $I = p r t \quad \text{Solve for } r.$ | $r = \frac{I}{p t}$ | — |
| 3 | $1x + 2y = 2 \quad \text{Solve for } y.$ | $y = \frac{2 - 1x}{2}$ | multi_letter |
| 3 | $2x + 1y = 3 \quad \text{Solve for } y.$ | $y = \frac{3 - 2x}{1}$ | multi_letter |
| 3 | $2x + 3y = 1 \quad \text{Solve for } y.$ | $y = \frac{1 - 2x}{3}$ | multi_letter |
| 6 | $A = \frac{1}{2} b h \quad \text{Solve for } h.$ | $h = \frac{2A}{b}$ | multi_letter, rearrange_hard |
| 6 | $A = \ell w \quad \text{Solve for } w.$ | $w = \frac{A}{\ell}$ | — |
| 6 | $d = r t \quad \text{Solve for } t.$ | $t = \frac{d}{r}$ | — |
| 10 | $V = \ell w h \quad \text{Solve for } w.$ | $w = \frac{V}{\ell h}$ | multi_letter, rearrange_hard |
| 10 | $A = \frac{1}{2} b h \quad \text{Solve for } h.$ | $h = \frac{2A}{b}$ | multi_letter, rearrange_hard |
| 10 | $V = \ell w h \quad \text{Solve for } w.$ | $w = \frac{V}{\ell h}$ | multi_letter, rearrange_hard |
| 14 | $A = \frac{1}{2} b h \quad \text{Solve for } h.$ | $h = \frac{2A}{b}$ | multi_letter, rearrange_hard |
| 14 | $V = \ell w h \quad \text{Solve for } w.$ | $w = \frac{V}{\ell h}$ | multi_letter, rearrange_hard |
| 14 | $y - 0 = 1(x - 2) \quad \text{Solve for } y.$ | $y = x - 2$ | multi_letter, rearrange_hard |
| 20 | $A = \frac{1}{2} b h \quad \text{Solve for } h.$ | $h = \frac{2A}{b}$ | multi_letter, rearrange_hard |
| 20 | $y - 4 = 7(x - 5) \quad \text{Solve for } y.$ | $y = 7x - 31$ | multi_letter, rearrange_hard |
| 20 | $y - 0 = 1(x - 2) \quad \text{Solve for } y.$ | $y = x - 2$ | multi_letter, rearrange_hard |
