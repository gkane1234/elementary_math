# Notes — `calc_diff_chain_rule` (`Chain Rule`)

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_chain_rule`
- **Suggested family:** other (calc limits / Diff)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate a composition with the chain rule. Skeleton is \(f(g(x))\) at low/mid D and \(f(g(h(x)))\) at high D. Each layer is sampled from the leaf’s allowed function classes (trig / exp / ln / algebraic power), not a fixed power-poly production.
- **D=0:** One easy outer of a simple inner — old easy \((ax+b)^n\). Do not jump to \(f(g(h(x)))\).
- **Mid D (≈8):** Still one composition, but rotate unlike OpenStax layers when allows unlock: \(\sin(g)\), \(\tan(ax+b)\), \(e^{ax+b}\), \((\sin x)^n\), \(\cos(x^2)\).
- **High D (≈16–22):** Deeper nest \(f(g(h(x)))\) (occasionally deeper at elite D). Layers unlike when multiple classes are allowed — \(e^{\sin x}\), \(\ln(\cos x)\), \(\sin(e^{3x})\). Not \((({\rm poly})^p)^q\) that exponent laws flatten.
- **Must not:** Bare product without composition; second derivative bleed; `chain_nested_power` as the dominant high-D shape.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live old path: `question_engine.generators.calculus._derivative_chain_rule` (shadowed by `calculus_derivative_rules`; no `use_sample_*` opt-out). Seeded `random.seed` then called the old builder. Band map: D≤4 easy, D≤11 medium, else hard.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\frac{d}{dx}\left(2x + 4\right)^{3}$` | `$6\left(2x + 4\right)^{2}$` | easy: \((ax+b)^n\) |
| 0 | 207 | `$\frac{d}{dx}\left(2x - 2\right)^{2}$` | `$4\left(2x - 2\right)$` | easy: \((ax+b)^n\) |
| 8 | 101 | `$\frac{d}{dx}\left(3x^{2} - 1\right)^{4}$` | `$24x\left(3x^{2} - 1\right)^{3}$` | medium: \((ax^2+c)^n\) |
| 8 | 313 | `$\frac{d}{dx}\left(3x^{2} - 2\right)^{4}$` | `$24x\left(3x^{2} - 2\right)^{3}$` | medium: quadratic power |
| 16 | 101 | `$\frac{d}{dx}\sin\left(3x^{4}\right)$` | `$12x^{3}\cos\left(3x^{4}\right)$` | hard: \(\sin(ax^n)\) — unlike composition |
| 22 | 101 | `$\frac{d}{dx}\sin\left(3x^{4}\right)$` | `$12x^{3}\cos\left(3x^{4}\right)$` | hard: same family as D=16 |

Opt-out flag used: _none — call shadowed `calculus._derivative_chain_rule` directly_

**Pre-fix live skeleton** (same seeds) was algebraic-only: D=0 `(2x)^2`; D=8 `(poly)^3`; D=16/22 `chain_nested_power` towers such as `\left(-8\left(x^{4}+\cdots\right)^{3}\right)^{5}`. Cause: leaf `allow_trig`/`allow_exp`/`allow_log` defaulted off, so the catalog could only pick `chain_power_linear` / `chain_nested_power`.

## OpenStax examples + chapter/section cites

Paraphrase stems; copy shapes, not wording.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.6 The Chain Rule | https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule | \((ax+b)^n\), \(({\rm poly})^n\); \(\sin^n x\); \(\cos(5x^2)\); \(\sin(7x+2)\); \(\tan({\rm poly})\); \(\sec({\rm poly})\) (sec outer deferred — no `sec` Apply); nested unlike \(\cos^4((7x)^2+1)\), \(\sin^6(x^3)\) |
| OpenStax Calculus Volume 1 §3.9 Exp / log derivatives | https://openstax.org/books/calculus-volume-1/pages/3-9-derivatives-of-exponential-and-logarithmic-functions | \(e^{g(x)}\), \(\ln(g(x))\) as chain outers |

Local mining: `scripts/output/example_mining/calculus-volume-1/stage1/3-6-the-chain-rule.md`

Catalog forms wired: `chain_power_linear`, `chain_trig_poly` (sin/cos/tan of inner), `chain_exp_poly`, `chain_ln_poly`, `chain_power_trig` \(({\rm trig})^n\), `chain_nested` (unlike \(f\circ g\circ h\) from the allow pool). `chain_nested_power` stays in the catalog for power/general but is **not** a chain-leaf form.

## Variety notes

Old hard is one Mad-Lib (`sin(a x^n)` only). OpenStax §3.6/§3.9 frames win for story/shape variety at mid/high D; algebra at D=0 still matches old easy.

## Limitations

- **Status:** shipped — Diff `expr_skeleton` + catalog compose forms. Remaining: no `sec`/`csc` outer (AST has `tan` → `sec^2` only); product+chain textbook items such as \((2x+1)^5(3x-2)^7\) are on the **product** leaf (`product_chain_powers`); applied velocity stories not on this leaf.
- **Generator:** `derivative_chain_rule`
- Token `LIMITATIONS` kept for those honest gaps (not for the old nested-power bug).

## Proposed engine (reuse vs new)

**Reuse:** `expr_skeleton` `Diff(Apply(fn,u))` / `Diff(Pow(H,n))` + `derivatives.json` chain forms. Nest slots pick from the allowed function pool; richness nest budget scales \(f(g(x))\) → \(f(g(h(x)))\). No new core; no padded `difficulty_costs`.

- **Shipped:** allow_* defaults on for this leaf; D-unlocks still keep D=0 algebraic; unlike compose forms; nested-power demoted off the chain leaf.

Coverage: Diff algebraic families also cataloged in `scripts/output/diff_skeleton_gallery/` (power, product, quotient, chain, trig, invtrig, ln/exp, general, higher_order).
