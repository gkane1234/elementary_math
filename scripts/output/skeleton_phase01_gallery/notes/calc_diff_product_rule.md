# Notes — `calc_diff_product_rule` (`Product Rule`)

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_product_rule`
- **Suggested family:** other (calc limits / Diff)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate a product \(uv\) with the product rule. Mid/high D may compose **a factor** (product+chain) when `allow_chain` is on; specials (`allow_trig` / `allow_exp` / `allow_log`) use the same function pool as the chain-rule leaf.
- **D=0:** Simple product of two easy factors — old easy \((ax+b)(cx+d)\) / monomials. No required composition; not \(f(g(h(x)))\).
- **Mid D (≈8):** Denser poly×linear **or** one composed factor \(\mathrm{poly}\times(ax+b)^n\). With specials on: \(\sin x\cdot e^{g(x)}\).
- **High D (≈16–22):** OpenStax two-chain product \((ax+b)^n(cx+d)^m\) (Example 3.54) rotates in; one-chain poly\(\times(u)^n\) still allowed. Nest stays 1 on a factor — chain leaf keeps \(f(g(h(x)))\).
- **Must not:** Pure chain without a product; quotient leaf shapes; log-diff \(x^x\) / \((\sin x)^x\); 3-deep nest on this leaf.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live old path: `question_engine.generators.calculus._derivative_product_rule` (shadowed by `calculus_derivative_rules`; no `use_sample_*` opt-out). Seeded `random.seed` then called the old builder. Band map: D≤4 easy, D≤11 medium, else hard.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\frac{d}{dx}\left[\left(2x + 4\right)\left(3x + 3\right)\right]$` | `$12x + 18$` | easy: two linears |
| 0 | 207 | `$\frac{d}{dx}\left[\left(2x - 2\right)\left(x + 1\right)\right]$` | `$4x$` | easy: two linears |
| 8 | 101 | `$\frac{d}{dx}\left[\left(3x^{2} - x + 4\right)\left(3x + 3\right)\right]$` | `$27x^{2} + 12x + 9$` | medium: quadratic × linear |
| 16 | 101 | `$\frac{d}{dx}\left[x^{4}\left(2x + 4\right)\right]$` | `$10x^{4} + 16x^{3}$` | hard: monomial × linear — **no chain** |
| 22 | 101 | `$\frac{d}{dx}\left[x^{4}\left(2x + 4\right)\right]$` | `$10x^{4} + 16x^{3}$` | hard: same family as D=16 |

Opt-out flag used: _none — call shadowed `calculus._derivative_product_rule` directly_

**Pre-fix live skeleton** (seed 101) already had opportunistic one-chain at high D via `product_two_poly` hole fill: D=0 `$x(2x)$`; D=8 poly×linear; D=16/22 `(-2(\mathrm{poly})^3)(\mathrm{poly})`. Missing dedicated OpenStax two-chain \((ax+b)^n(cx+d)^m\) and \(\sin x\cdot e^{g}\).

## OpenStax examples + chapter/section cites

Paraphrase stems; copy shapes, not wording.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.3 Differentiation Rules | https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules | product of two polys / binomials — \( (x^2+2)(3x^3-5x) \), \( 2x^5(4x^2+x) \) |
| OpenStax Calculus Volume 1 §3.6 The Chain Rule — Example 3.54 | https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule | **product of two chains:** \( (2x+1)^5(3x-2)^7 \). Checkpoint 3.37 is a **quotient** \( x/(2x+3)^3 \) — not this leaf. |
| OpenStax Calculus Volume 1 §3.9 Exp / log derivatives | https://openstax.org/books/calculus-volume-1/pages/3-9-derivatives-of-exponential-and-logarithmic-functions | product+chain with one composed exp: \( x e^{2x} \), \( 4x e^{(x^2-1)} \); \(\sin x\cdot e^{g(x)}\) |

Local mining: `scripts/output/example_mining/calculus-volume-1/stage1/3-3-differentiation-rules.md`, `3-6-the-chain-rule.md`. Challenging-integrals bank (`challenging_indefinite_integrals_bc.tex`) is mostly one composed piece times its derivative (u-sub) — product of two composed factors is rare there; do not copy integral shapes onto this leaf.

Catalog forms on this leaf: `product_two_poly` (D=0 core), `product_one_chain`, `product_chain_powers` (Example 3.54), `product_poly_trig` / `product_poly_exp` (specials opt-in), `product_trig_exp_chain` (`allow_trig`+`allow_exp`). Not on `derivative_chain_rule` / `derivative_logarithmic`.

## Variety notes

Old hard is monomial×linear only. OpenStax §3.6/§3.9 frames win for product+chain at mid/high D; D=0 algebra still matches old easy. Specials stay checkbox opt-in (same pool as chain-rule when on).

## Limitations

- **Status:** shipped — Diff `expr_skeleton` + catalog product+chain forms. Remaining `LIMITATIONS`: OpenStax Example 3.54 is a **product of two chains**; we also emit **one-chain** poly\(\times(u)^n\) (milder, and what old high-D skeleton already did). Product of two unlike special compositions (\(\sin(g)\cdot e^{h}\) with both inners composed) is not a default form — rare in the integrals bank and not the §3.54 item. No `sec`/`csc` factors. Log-diff variable-exponent work stays on the log-diff leaf.
- **Generator:** `derivative_product_rule`

## Proposed engine (reuse vs new)

**Reuse:** `expr_skeleton` `Diff(Prod(F,G))` (independent inners) + `derivatives.json` product forms. New form_ids stay on the product leaf; chain leaf remains \(f(g(h(x)))\). No padded `difficulty_costs`.

- **Shipped:** `product_one_chain`, `product_chain_powers`, `product_trig_exp_chain`; D=0 still `product_two_poly`.

Coverage: Diff algebraic families also cataloged in `scripts/output/diff_skeleton_gallery/` (power, product, quotient, chain, trig, invtrig, ln/exp, general, higher_order).
