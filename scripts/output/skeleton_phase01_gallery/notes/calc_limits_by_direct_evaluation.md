# Notes — `calc_limits_by_direct_evaluation` (`By direct evaluation`)

- **Course:** Calculus
- **Category:** Calculus — Limits
- **Generator:** `limit_direct_evaluation`
- **Suggested family:** other (calc limits / Diff)
- **Precalc alias:** `pc_limits_by_direct_evaluation` (same generator)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate a two-sided limit at a finite point by plugging in (poly / rational / specials).
- **D=0:** Polynomial plug-in only — old Mad-Lib easy, e.g. \(\lim_{x\to a}(ax^{2}+bx+c)\).
- **Mid D (≈8):** Leftover poly plus rational (nonzero den) and unlocked specials (trig / exp / ln / √ / arctan / squeeze).
- **High D (≈16–22):** Direct plug-ins that are not leftover poly — rational and specials. Still direct, not removable / indet.
- **Must not:** 0/0 cancel as the skill, jump piecewise, \(\infty\), L'Hôpital — those are other leaves.

## What old / live path actually produced (real latex, D=0/8/16/22)

**Old Mad-Lib** (`calculus.py` `_limit_direct_evaluation`, overridden by LimitSpec): poly plug-in only. Degree/coefs scale with D. No opt-out flag — live catalog **is** the old LimitSpec path.

**Before this leftover pass** (`_generate_for_type`): D=0 `poly_direct` only; D=8 leftover mix including poly (5/40) but catalog often stamped `direct_sqrt` / `direct_ln` / `poly_direct` on rational latex (`form == "rational_direct"` beat the catalog pick); D=16 and D=22 the same mix, still including leftover poly (5/40). Metadata already stamped `form_id` + `generator=limit_direct_evaluation` on `spec_snapshot`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 1} \left(2x^{2} - 3x + 3\right)$` | `$2$` | form=`poly_direct` |
| 8 | 101 | `$\lim_{x \to 4} \frac{3x^{3} - 3x}{2x - 1}$` | `$\frac{180}{7}$` | stamped `direct_sqrt`; latex is rational |
| 16 | 101 | `$\lim_{x \to 4} 3\frac{2x^{3} + 6x}{-4x + 7}$` | `$-\frac{152}{3}$` | same stamp mismatch + dress |
| 22 | 101 | `$\lim_{x \to 4} 3\frac{-2x^{3} + 3x}{6x - 7}$` | `$-\frac{348}{17}$` | leftover poly still in the old pool |

Opt-out flag used: _none — LimitSpec `limit_direct` / `limits.json` is the live default_

## What live path produces now (real latex)

Leftover lockout of D=0 poly plug-in at D≥16 (`d_max=10` on `poly_direct`). Catalog pick wins over `_pick_form`; `_sample_rational_direct` stamps `rational_direct`. Stamps `form_id` + `generator=limit_direct_evaluation` on metadata and `spec_snapshot`. 40-seed counts: D=0 `poly_direct` 40; D=8 leftover mix (`direct_exp` 7 / `direct_sqrt` 6 / `squeeze_sin_over_x` 6 / `poly_direct` 5 / `direct_arctan` 5 / `direct_sin_shift` 4 / `rational_direct` 4 / `direct_ln` 3); D=16/22 identical specials/rational mix (no `poly_direct`).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 1} \left(2x^{2} - 3x + 3\right)$` | `$2$` | `poly_direct` |
| 0 | 1 | `$\lim_{x \to 0} \left(-4x^{2} + 3\right)$` | `$3$` | same form |
| 8 | 0 | `$\lim_{x \to -5} -2\left(6x^{2}\right)$` | `$-300$` | leftover `poly_direct` + dress |
| 8 | 101 | `$\lim_{x \to 6} -\left((2x-1)\sqrt{x+4}\right)$` | `$-11\sqrt{10}$` | `direct_sqrt` (stamp matches) |
| 8 | 12 | `$\lim_{x \to 6} (2x-1)\sqrt{x+4}$` | `$11\sqrt{10}$` | `direct_sqrt` |
| 16 | 0 | `$\lim_{x \to -5} -2\frac{6x^{2} - 1}{5x + 7}$` | `$\frac{149}{9}$` | `rational_direct` |
| 16 | 7 | `$\lim_{x \to 0} -3\arctan(x)$` | `$0$` | `direct_arctan` |
| 16 | 17 | `$\lim_{x \to 2} -e^{x}$` | `$-e^{2}$` | `direct_exp` |
| 22 | 2 | `$\lim_{x \to 0} -3\frac{\sin(x)}{x}$` | `$-3$` | `squeeze_sin_over_x` |

Opt-out flag used: _none — live catalog on `limits.py` / `limits.json`_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §2.3 The Limit Laws | https://openstax.org/books/calculus-volume-1/pages/2-3-the-limit-laws | direct plug-in poly / rational / trig / exp / ln / roots |
| OpenStax Calculus Volume 1 §2.2 The Limit of a Function | https://openstax.org/books/calculus-volume-1/pages/2-2-the-limit-of-a-function | limit-at-a-point language |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/2-3-the-limit-laws.md`; form catalog `limits.json`

## Variety notes

D=0 stays one easy form (`poly_direct`). D=8 leftover poly + rational/specials. High D cannot emit leftover poly. Not a WP. Shared generator also leftover-locks `pc_limits_by_direct_evaluation`. Multi-seed spans poly (mid only), rational, sin/cos, exp, ln, √, arctan, squeeze.

## Limitations

- **Status:** leftover lockout of D=0 poly shipped. Remaining `LIMITATIONS`: D=16 and D=22 are the same specials/rational mix; D=8 can still emit leftover poly (intentional); specials are frozen closed families (same \((2x-1)\sqrt{x+4}\) at \(x\to 6\); same \(\arctan(x)\) at 0); `squeeze_sin_over_x` is a known-limit / 0/0 identity on a plug-in leaf; no ε–δ; dress can wrap a simple core (`-3\arctan(x)`).
- **Live pairwise:** each item stamps `form_id`, `generator=limit_direct_evaluation`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt inside the leftover band.
- **Generator:** `limit_direct_evaluation`

## Proposed engine (reuse vs new)

- **Reuse:** LimitSpec `_sample_poly_direct` / `_sample_rational_direct` / `_sample_expr_direct` + generator `limit_direct_evaluation` + `limits.json`. Catalog `d_max=10` on leftover poly. No padded `difficulty_costs`. Did not invent ε–δ / piecewise / removable cores.
- **Shipped this pass:** leftover lockout of D=0 poly at D≥16; catalog pick honored so `form_id` matches latex; `form_id` + `generator` on `spec_snapshot`.
