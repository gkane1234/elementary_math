# Notes — `calc_limits_at_essential_discontinuities` (`At essential discontinuities`)

- **Course:** Calculus
- **Category:** Calculus — Limits
- **Generator:** `limit_essential`
- **Suggested family:** other (calc limits / Diff)
- **Precalc alias:** `pc_limits_at_essential_discontinuities` (same generator)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Recognize limits that DNE (or go to \(\pm\infty\)) at vertical asymptotes / wild oscillation (essential).
- **D=0:** Bare \(\lim_{x\to 0} 1/x\) → DNE — old Mad-Lib easy.
- **Mid D (≈8):** Leftover \(1/x\) plus \(1/x^{2}\), rational VA, \(\sin(1/x)\), \(\cos(1/x)\), \(\tan x\) as \(x\to\pi/2\).
- **High D (≈16–22):** Oscillating / even-power / rational-VA / tan — not leftover \(\lim_{x\to 0} 1/x\). Spec dress (shift / scale / cancel).
- **Must not:** Removable cancel that exists; ordinary rational plug-in; jump piecewise.

## What old / live path actually produced (real latex, D=0/8/16/22)

**Old Mad-Lib** (`precalc.py` essential branch, overridden by LimitSpec): always \(\lim_{x\to 0} 1/x^{p}\) with \(p\in\{1,2\}\), answer `\text{does not exist}`. No D ladder. Seed 101: `$\lim_{x\to0}\frac{1}{x^{1}}$`; seed 0: `$\lim_{x\to0}\frac{1}{x^{2}}$`. No opt-out flag — live catalog **is** the old LimitSpec path.

**Before this leftover pass** (`_generate_for_type`): D=0 `essential_1_over_x` only; D=8 leftover mix including `essential_1_over_x` (7/40, 2/40 still bare leftover latex); D=16 and D=22 the same mix, still including leftover `essential_1_over_x` (6/40), including sign-only `$\lim_{x \to 0} -\frac{1}{x}$`. Metadata already stamped `form_id` + `generator=limit_essential` on `spec_snapshot`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 0} \frac{1}{x}$` | `$\text{DNE}$` | form=`essential_1_over_x` |
| 8 | 101 | `$\lim_{x \to -4} \cos\left(\frac{1}{(x+4)}\right)$` | `$\text{DNE}$` | form=`essential_cos_1_over_x`; wrap=shift |
| 16 | 0 | `$\lim_{x \to 0} -\frac{1}{x}$` | `$\text{DNE}$` | leftover `essential_1_over_x` + sign |
| 22 | 0 | `$\lim_{x \to 0} -\frac{1}{x}$` | `$\text{DNE}$` | leftover `essential_1_over_x` still in the old pool |

Opt-out flag used: _none — LimitSpec `limit_essential` / `limits.json` is the live default_

## What live path produces now (real latex)

Leftover lockout of D=0 \(\lim 1/x\) at D≥16 (`d_max=10` on `essential_1_over_x`). Sampler else-branch cannot silently emit leftover \(1/x\) when catalog fid is empty. Stamps `form_id` + `generator=limit_essential` on metadata and `spec_snapshot`. 40-seed counts: D=0 `essential_1_over_x` 40; D=8 leftover mix (`essential_rational_va` 9 / `essential_tan_asymptote` 8 / `essential_cos_1_over_x` 8 / `essential_1_over_x` 7 / `essential_sin_1_over_x` 5 / `essential_1_over_x_sq` 3); D=16/22 `essential_tan_asymptote` 9 / `essential_1_over_x_sq` 8 / `essential_cos_1_over_x` 8 / `essential_sin_1_over_x` 8 / `essential_rational_va` 7 (no `essential_1_over_x`).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 0} \frac{1}{x}$` | `$\text{DNE}$` | `essential_1_over_x` |
| 0 | 1 | `$\lim_{x \to 0} \frac{1}{x}$` | `$\text{DNE}$` | same form |
| 8 | 0 | `$\lim_{x \to 0} \frac{1}{x}$` | `$\text{DNE}$` | leftover `essential_1_over_x` |
| 8 | 1 | `$\lim_{x \to 4} \sin\left(\frac{1}{(x-4)}\right)$` | `$\text{DNE}$` | `essential_sin_1_over_x` |
| 8 | 2 | `$\lim_{x \to \frac{\pi}{2}} \tan(x)$` | `$\text{DNE}$` | `essential_tan_asymptote` |
| 8 | 101 | `$\lim_{x \to -4} \cos\left(\frac{1}{(x+4)}\right)$` | `$\text{DNE}$` | `essential_cos_1_over_x` |
| 16 | 0 | `$\lim_{x \to 0} -\frac{1}{x^{2}}$` | `$-\infty$` | `essential_1_over_x_sq` (no leftover 1/x) |
| 16 | 4 | `$\lim_{x \to -5} \frac{1}{(x+5)^{2}}$` | `$\infty$` | `essential_1_over_x_sq` + shift |
| 16 | 7 | `$\lim_{x \to \frac{\pi}{2}} -\tan(x)$` | `$\text{DNE}$` | `essential_tan_asymptote` |
| 22 | 11 | `$\lim_{x \to 0} -\sin\left(\frac{1}{x}\right)$` | `$\text{DNE}$` | `essential_sin_1_over_x` |

Opt-out flag used: _none — live catalog on `limits.py` / `limits.json`_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §2.2 The Limit of a Function | https://openstax.org/books/calculus-volume-1/pages/2-2-the-limit-of-a-function | infinite / oscillating behavior near asymptotes; VA \(1/(x+3)^{4}\), \(1/(x-2)^{3}\) |
| OpenStax Calculus Volume 1 §2.4 Continuity | https://openstax.org/books/calculus-volume-1/pages/2-4-continuity | essential discontinuity classification; \(\sin(1/x)\) oscillation |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/2-4-continuity.md`; form catalog `limits.json` `essential_*`

## Variety notes

D=0 stays one easy form (`essential_1_over_x`). D=8 leftover \(1/x\) + VA / osc / tan. High D cannot emit leftover \(1/x\). Not a WP. Shared generator also leftover-locks `pc_limits_at_essential_discontinuities`.

## Limitations

- **Status:** leftover lockout of D=0 \(1/x\) shipped. Remaining `LIMITATIONS`: D=16 and D=22 are the same osc/VA/tan mix; D=8 can still emit leftover \(1/x\) (intentional); `essential_tan_asymptote` is a frozen closed family (always \(\tan x\) as \(x\to\pi/2\)); `essential_rational_va` power \(n=1\) can look like shifted \(1/x\); cancel/unfactored dress can look messy (`\(\frac{x}{x^{2}}\)`, `\(\frac{(x+2)}{x^{2}+2x}\)`) or like a hole rather than a VA; old Mad-Lib also had \(1/x^{2}\) (live D=0 is \(1/x\) only; \(1/x^{2}\) stays mid/high); no figure-bank graphs; no ε–δ.
- **Live pairwise:** each item stamps `form_id`, `generator=limit_essential`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt inside the leftover band.
- **Generator:** `limit_essential`

## Proposed engine (reuse vs new)

- **Reuse:** LimitSpec `_sample_essential` + generator `limit_essential` + `limits.json`. Catalog `d_max=10` on leftover \(1/x\). No padded `difficulty_costs`. Did not invent a figure-bank / ε–δ / \(x\sin(1/x)\) core.
- **Shipped this pass:** leftover lockout of D=0 \(1/x\) at D≥16; sampler cannot silently emit leftover \(1/x\) when catalog fid is empty; `form_id` + `generator` on `spec_snapshot`.
