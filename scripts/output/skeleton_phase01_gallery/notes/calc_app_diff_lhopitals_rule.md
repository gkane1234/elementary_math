# Notes — `calc_app_diff_lhopitals_rule` (`L'Hôpital's Rule`)

- **Course:** Calculus
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `lhopitals_rule`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `lhopitals_rule`
- **Remaining limits:** LimitSpec packs ship. Remaining gaps: form_id metadata sometimes mismatches latex (e.g. `direct_sqrt` stamp on rational plug-in); one-sided / piecewise story variety thinner than OpenStax §2.2–2.4 exercise banks; no dedicated limit-skeleton patterns beyond packs.

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate indeterminate limits (0/0, ∞/∞, …) via L'Hôpital when appropriate.
- **D=0:** Simple 0/0 like (e^{kx}−1)/x, sin(kx)/x, or (x²−a²)/(x−a).
- **High D (≈16–22):** ∞/∞ rationals, multipass, exp/poly, 0·∞ / 1^∞ after rewrite — OpenStax §4.8.
- **Must not:** Direct plug-in that is already determinate; dump non-indet cancel as if L'Hôpital were required.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live LimitSpec after form→flesh fix (2026-08-20). OpenStax §4.8 gold locked.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 2} \frac{x^{2}-4}{x-2}$` | `$4$` | form=`lhopital_0_0_poly`; 0/0 |
| 8 | 101 | `$\lim_{x \to \infty} x^{1} e^{-x}$` | `$0$` | form=`lhopital_0_inf_product`; 0·∞ |
| 16 | 101 | `$\lim_{x \to 0^{+}} 3x^{1/x}$` | `$0$` | form=`lhopital_0_inf_power`; 0^∞ |
| 22 | 101 | `$\lim_{x \to 0^{+}} 16x^{2/x}$` | `$0$` | form=`lhopital_0_inf_power` + dress |

Opt-out flag used: _none found (LimitSpec default)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.8 L'Hôpital's Rule | https://openstax.org/books/calculus-volume-1/pages/4-8-lhopitals-rule | 0/0 and ∞/∞; other forms after algebra |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/4-8-lhopitals-rule.md; limits.json lhopital_*`

## Variety notes / flags

Shipped: form_id matches latex for rewrite/exp/multipass catalog forms. Multi-seed spans 0/0, ∞/∞, 0·∞, ∞−∞, 0^0, ∞^0, 1^∞, 0^∞.

## Proposed engine (reuse vs new)

**Reuse:** LimitSpec `limit_lhopital` / generator `lhopitals_rule`. Keep as limit pack (not Diff skeleton).
