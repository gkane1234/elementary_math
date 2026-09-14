# Notes — `calc_limits_at_infinity` (`At infinity`)

- **Course:** Calculus
- **Category:** Calculus — Limits
- **Generator:** `limit_at_infinity`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `limit_at_infinity`
- **Remaining limits:** LimitSpec packs ship. Remaining gaps: form_id metadata sometimes mismatches latex (e.g. `direct_sqrt` stamp on rational plug-in); one-sided / piecewise story variety thinner than OpenStax §2.2–2.4 exercise banks; no dedicated limit-skeleton patterns beyond packs.

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate lim_{x→±∞} (end behavior / compare degrees / growth rates).
- **D=0:** Rational same-degree → horizontal asymptote ratio of leading coefs.
- **High D (≈16–22):** exp ratios, ln/poly, arctan, trig/x — OpenStax §4.6 ladder.
- **Must not:** Finite-a removable / jump; L'Hôpital leaf owns indeterminate ∞/∞ when teaching the rule.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live LimitSpec after flesh fix (2026-08-20).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to \infty} \frac{-4x^{2} - 5x}{5x^{2}}$` | `$-\frac{4}{5}$` | form=`inf_rational` |
| 8 | 101 | `$\lim_{x \to \infty} -4\frac{4+4e^{x}}{2+1e^{x}}$` | `$-16$` | form=`inf_exp_ratio` (a+be^x)/(c+de^x) |
| 16 | 101 | `$\lim_{x \to \infty} 4\frac{4+4e^{x}}{2+1e^{x}}$` | `$16$` | form=`inf_exp_ratio` + dress |
| 22 | 101 | `$\lim_{x \to \infty} 4\frac{4+4e^{x}}{2+1e^{x}}$` | `$16$` | form=`inf_exp_ratio` + dress |

Opt-out flag used: _none found (LimitSpec default)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.6 Limits at Infinity and Asymptotes | https://openstax.org/books/calculus-volume-1/pages/4-6-limits-at-infinity-and-asymptotes | rational end behavior; exp/ln growth |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/4-6-limits-at-infinity-and-asymptotes.md`

## Variety notes / flags

Shipped: `inf_exp_ratio` fleshes (a+be^x)/(c+de^x) per catalog (not e^x/x²). Multi-seed mid D rotates rational / sin/x / arctan / exp / ln.

## Proposed engine (reuse vs new)

**Reuse:** LimitSpec `limit_at_infinity`. Broaden form rotation at mid/high D.
