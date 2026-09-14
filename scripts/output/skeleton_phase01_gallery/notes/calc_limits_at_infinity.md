# Notes — `calc_limits_at_infinity` (`At infinity`)

- **Course:** Calculus
- **Category:** Calculus — Limits
- **Generator:** `limit_at_infinity`
- **Suggested family:** other (calc limits / Diff)
- **Precalc alias:** `pc_limits_at_infinity` (same generator)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate \(\lim_{x\to\pm\infty}\) (end behavior / compare degrees / growth rates).
- **D=0:** Rational same- or nearby-degree at \(\pm\infty\) — old Mad-Lib easy.
- **Mid D (≈8):** Leftover rational plus \(\sin x/x\), \(\arctan x\), \((a+be^{x})/(c+de^{x})\), \(\ln x/x^{k}\).
- **High D (≈16–22):** Exp / ln / arctan / bounded-over-\(x^{n}\) — OpenStax §4.6 ladder, not leftover rational.
- **Must not:** Finite-\(a\) removable / jump; L'Hôpital leaf owns indeterminate \(\infty/\infty\) when teaching the rule.

## What old / live path actually produced (real latex, D=0/8/16/22)

**Old Mad-Lib** (`calculus.py` `_limit_at_infinity`, overridden by LimitSpec): always rational \(P/Q\) at \(\pm\infty\) (degree compare). No D ladder of families — higher D only grows degree/coefs. No opt-out flag — live catalog **is** the old LimitSpec path.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to \infty} \frac{3x - 1}{2}$` | `$\infty$` | old Mad-Lib rational |
| 8 | 101 | `$\lim_{x \to -\infty} \frac{-x^{2} - 2}{2x^{2}}$` | `$-\frac{1}{2}$` | still rational |
| 16 | 101 | `$\lim_{x \to \infty} \frac{-x^{4} - 5x^{2}}{9x^{2}}$` | `$-\infty$` | still rational, higher degree |
| 22 | 101 | `$\lim_{x \to \infty} \frac{2x^{4} + x^{2}}{10x^{4}}$` | `$\frac{1}{5}$` | still rational |

**Before this leftover pass** (`_generate_for_type`): D=0 `inf_rational` only; D=8 leftover mix including `inf_rational` (8/40); D=16 and D=22 the same mix, still including leftover `inf_rational` (7/40). Metadata already stamped `form_id` + `generator=limit_at_infinity` on `spec_snapshot`.

Opt-out flag used: _none — LimitSpec `limit_at_infinity` / `limits.json` is the live default_

## What live path produces now (real latex)

Leftover lockout of D=0 rational at \(\pm\infty\) at D≥16 (`d_max=10` on `inf_rational`). Sampler else-branch cannot silently emit leftover rational when catalog fid is empty. Stamps `form_id` + `generator=limit_at_infinity` on metadata and `spec_snapshot`. 40-seed counts: D=0 `inf_rational` 40; D=8 leftover mix (`inf_exp_ratio` 10 / `inf_arctan` 10 / `inf_rational` 8 / `inf_ln_over_poly` 8 / `inf_sin_over_x` 4); D=16/22 `inf_exp_ratio` 11 / `inf_ln_over_poly` 11 / `inf_sin_over_x` 9 / `inf_arctan` 9 (no `inf_rational`).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to \infty} \frac{3x^{2} - 3x}{5x^{2}}$` | `$\frac{3}{5}$` | `inf_rational` |
| 0 | 0 | `$\lim_{x \to \infty} \frac{6x - 6}{5x}$` | `$\frac{6}{5}$` | same form |
| 8 | 0 | `$\lim_{x \to \infty} 4\frac{6x - 6}{5x}$` | `$\frac{24}{5}$` | leftover `inf_rational` + scale |
| 8 | 1 | `$\lim_{x \to -\infty} 3\frac{3+3e^{x}}{1+1e^{x}}$` | `$9$` | `inf_exp_ratio` |
| 8 | 11 | `$\lim_{x \to \infty} -3\arctan(x)$` | `$-3\frac{\pi}{2}$` | `inf_arctan` |
| 16 | 0 | `$\lim_{x \to \infty} -2\frac{\cos(x)}{x^{1}}$` | `$0$` | `inf_sin_over_x` (no leftover rational) |
| 16 | 1 | `$\lim_{x \to -\infty} 3\frac{3+3e^{x}}{1+1e^{x}}$` | `$9$` | `inf_exp_ratio` |
| 16 | 2 | `$\lim_{x \to \infty} -6\frac{\ln(x)}{x^{3}}$` | `$0$` | `inf_ln_over_poly` |
| 22 | 11 | `$\lim_{x \to \infty} 6\arctan(x)$` | `$6\frac{\pi}{2}$` | `inf_arctan` |

Opt-out flag used: _none — live catalog on `limits.py` / `limits.json`_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.6 Limits at Infinity and Asymptotes | https://openstax.org/books/calculus-volume-1/pages/4-6-limits-at-infinity-and-asymptotes | rational end behavior; Ex. 4.21 \(5-2/x^{2}\), \(\sin x/x\), \(\arctan x\); exp/ln growth |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/4-6-limits-at-infinity-and-asymptotes.md`; form catalog `limits.json` `inf_*`

## Variety notes

D=0 stays one easy form (`inf_rational`). D=8 leftover rational + §4.6 specials. High D cannot emit leftover rational. Not a WP. Shared generator also leftover-locks `pc_limits_at_infinity`.

## Limitations

- **Status:** leftover lockout of D=0 rational shipped. Remaining `LIMITATIONS`: D=16 and D=22 are the same exp/ln/arctan/trig mix; D=8 can still emit leftover `inf_rational` (intentional); frozen closed specials (same \(\sin x/x\) or \(\cos x/x^{n}\), \(\arctan x\), \((a+be^{x})/(c+de^{x})\), \(\ln x/x^{k}\)); sampler `e^{x}/x^{k}` family is not a catalog form; Spec scale dress can look like \(k\frac{\cdots}{\cdots}\) or \(k\arctan x\); no oblique-asymptote / ε–δ / figure-bank cores.
- **Live pairwise:** each item stamps `form_id`, `generator=limit_at_infinity`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt inside the leftover band.
- **Generator:** `limit_at_infinity`

## Proposed engine (reuse vs new)

- **Reuse:** LimitSpec `_sample_infinity` + generator `limit_at_infinity` + `limits.json`. Catalog `d_max=10` on leftover rational. No padded `difficulty_costs`. Did not invent an \(e^{x}/x^{k}\) catalog form / oblique-asymptote / ε–δ / figure-bank core.
- **Shipped this pass:** leftover lockout of D=0 rational at D≥16; sampler cannot silently emit leftover rational when catalog fid is empty; `form_id` + `generator` on `spec_snapshot`.
