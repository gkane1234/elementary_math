# Notes — `calc_def_int_second_fundamental_theorem_of_calculus`

- **Display name:** Second Fundamental Theorem of Calculus
- **Category:** Calculus — Definite Integration
- **Generator:** `second_fundamental_theorem`
- **Suggested family:** `integral`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `second_fundamental_theorem`
- **Remaining limits:** Reuse `integrals.py` / FTC / Riemann constructive cores. Gaps: curve families still thin vs OpenStax §5–6 (mostly poly); trig-sub / PFD / multi-trick are catalog-shaped but not full textbook exercise breadth.

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate an integral with variable upper limit (OpenStax FTC Part 1).
- **D=0:** $\frac{d}{dx}\int_a^x t^2\,dt \to x^2$.
- **High D:** unlock trig integrand and chain upper limit $g(x)=kx$.
- **Must not:** Plain evaluate-$\int_a^b$ (that is FTC1 / first leaf).

## What live path actually produced (real latex, D=0/8/16/22)

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\frac{d}{dx}\int_{0}^{x} t^{2}\,dt$ | $x^{2}$ | form=`ftc2_poly` |
| 0 | 207 | $\frac{d}{dx}\int_{2}^{x} t^{2}\,dt$ | $x^{2}$ | form=`ftc2_poly` |
| 8 | 101 | $\frac{d}{dx}\int_{0}^{x} t^{2}\,dt$ | $x^{2}$ | form=`ftc2_poly` |
| 8 | 207 | $\frac{d}{dx}\int_{2}^{x} t^{2}\,dt$ | $x^{2}$ | form=`ftc2_poly` |
| 16 | 101 | $\frac{d}{dx}\int_{0}^{x} t^{2}\,dt$ | $x^{2}$ | form=`ftc2_poly` (trig/chain across other seeds) |
| 16 | 207 | $\frac{d}{dx}\int_{2}^{x} t^{2}\,dt$ | $x^{2}$ | form=`ftc2_poly` |
| 22 | 101 | $\frac{d}{dx}\int_{0}^{x} t^{2}\,dt$ | $x^{2}$ | form=`ftc2_poly` |
| 22 | 207 | $\frac{d}{dx}\int_{2}^{x} t^{2}\,dt$ | $x^{2}$ | form=`ftc2_poly` |

Opt-out flag used: `(none)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.3 | https://openstax.org/books/calculus-volume-1/pages/5-3-the-fundamental-theorem-of-calculus | FTC Part 1: $\frac{d}{dx}\int_a^{g(x)} f = f(g(x))g'(x)$ |

## Variety notes

Clear gold: derivative-of-integral skill restored (was wrongly aliased to evaluate-∫ after integrals Spec override).

## Proposed engine (reuse vs new)

- **Proposal:** Reuse `integrals.py` `_sample_ftc2` (pack `integral_ftc2`).
- **New Integral skeleton?** no — shared Spec API already covers this.
- **Shipped:** FTC2 sampler + gallery.

_Catalog generator `second_fundamental_theorem`._
