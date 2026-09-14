# Notes — `calc_limits_at_removable_discontinuities` (`At removable discontinuities`)

- **Course:** Calculus
- **Category:** Calculus — Limits
- **Generator:** `limit_removable`
- **Suggested family:** other (calc limits / Diff)
- **Precalc alias:** `pc_limits_at_removable_discontinuities` (same generator)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate 0/0 limits by canceling a common factor (or rationalizing) at a hole.
- **D=0:** Difference of squares cancel only — old Mad-Lib easy, e.g. \(\lim_{x\to a}\frac{x^{2}-a^{2}}{x-a}\).
- **Mid D (≈8):** Leftover diff-sq plus expanded linear cancel and rationalize \(\frac{\sqrt{x}-\sqrt{a}}{x-a}\).
- **High D (≈16–22):** Expanded cancel / rationalize — not leftover \((x^{2}-a^{2})/(x-a)\).
- **Must not:** Direct plug-in with nonzero den; L'Hôpital as first method on this leaf; jump piecewise.

## What old / live path actually produced (real latex, D=0/8/16/22)

**Old Mad-Lib** (`advanced.py` `_limit_removable`, overridden by LimitSpec): always \(\lim_{x\to a}\frac{x^{2}-a^{2}}{x-a}=2a\). \(a\) only changes with seed — no D ladder. No opt-out flag — live catalog **is** the old LimitSpec path.

**Before this leftover pass** (`_generate_for_type`): D=0 `removable_diff_sq` only; D=8 leftover mix including rem_diff_sq (9/40) but `removable_quad_shared` could stamp rem_diff_sq latex (`\(\frac{x^{2}-9}{x-3}\)`); D=16 and D=22 the same mix, still including leftover rem_diff_sq (8/40). Metadata already stamped `form_id` + `generator=limit_removable` on `spec_snapshot`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 2} \frac{x^{2}-4}{x-2}$` | `$4$` | form=`removable_diff_sq` |
| 8 | 101 | `$\lim_{x \to 2} \frac{x^{2}-5x+6}{x-2}$` | `$-1$` | form=`removable_quad_shared` |
| 16 | 0 | `$\lim_{x \to 1} \frac{x^{2}-1}{x-1}$` | `$2$` | leftover rem_diff_sq still in the old pool |
| 22 | 0 | `$\lim_{x \to 1} \frac{x^{2}-1}{x-1}$` | `$2$` | leftover rem_diff_sq still in the old pool |

Old Mad-Lib seed 101: D=0 `$\lim_{x \to 2} \frac{x^{2} - 4}{x - 2}$` → `$4$`; D=8 `$\lim_{x \to 1} \frac{x^{2} - 1}{x - 1}$` → `$2$`; D=16/22 same as D=0.

Opt-out flag used: _none — LimitSpec `limit_removable` / `limits.json` is the live default_

## What live path produces now (real latex)

Leftover lockout of D=0 \((x^{2}-a^{2})/(x-a)\) at D≥16 (`d_max=10` on `removable_diff_sq`). Expanded linear/quad cancel cannot collapse to leftover rem_diff_sq latex. Stamps `form_id` + `generator=limit_removable` on metadata and `spec_snapshot`. 40-seed counts: D=0 `removable_diff_sq` 40; D=8 leftover mix (`removable_rationalize` 15 / `removable_diff_sq` 9 / `removable_quad_shared` 8 / `removable_linear_factor` 8); D=16/22 `removable_rationalize` 18 / `removable_quad_shared` 12 / `removable_linear_factor` 10 (no rem_diff_sq).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 2} \frac{x^{2}-4}{x-2}$` | `$4$` | `removable_diff_sq` |
| 0 | 1 | `$\lim_{x \to 3} \frac{x^{2}-9}{x-3}$` | `$6$` | same form |
| 8 | 0 | `$\lim_{x \to 1} \frac{x^{2}-1}{x-1}$` | `$2$` | leftover `removable_diff_sq` |
| 8 | 101 | `$\lim_{x \to 2} \frac{x^{2}+1x-6}{x-2}$` | `$5$` | `removable_quad_shared` |
| 8 | 7 | `$\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$` | `$\frac{1}{2\sqrt{4}}$` | `removable_rationalize` |
| 16 | 0 | `$\lim_{x \to 1} \frac{x^{2}+5x-6}{x-1}$` | `$7$` | `removable_linear_factor` (no leftover rem_diff_sq) |
| 16 | 101 | `$\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$` | `$\frac{1}{2\sqrt{2}}$` | `removable_rationalize` |
| 22 | 101 | `$\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$` | `$\frac{1}{2\sqrt{2}}$` | `removable_rationalize` |

Opt-out flag used: _none — live catalog on `limits.py` / `limits.json`_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §2.3 The Limit Laws | https://openstax.org/books/calculus-volume-1/pages/2-3-the-limit-laws | algebraic cancel / factor for 0/0 |
| OpenStax Calculus Volume 1 §2.4 Continuity | https://openstax.org/books/calculus-volume-1/pages/2-4-continuity | removable discontinuity / redefine at hole |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/2-3-the-limit-laws.md`; form catalog `limits.json` `removable_*`

## Variety notes

D=0 stays one easy form (`removable_diff_sq`). D=8 leftover rem_diff_sq + expanded cancel / rationalize. High D cannot emit leftover rem_diff_sq. Not a WP. Shared generator also leftover-locks `pc_limits_at_removable_discontinuities`.

## Limitations

- **Status:** leftover lockout of D=0 rem_diff_sq shipped. Remaining `LIMITATIONS`: D=16 and D=22 are the same expanded/rationalize mix; D=8 can still emit leftover rem_diff_sq (intentional); `removable_linear_factor` and `removable_quad_shared` are the same expanded \((x-a)(x+c)/(x-a)\) shape (no true shared-quadratic core); `removable_rationalize` is a frozen closed family (always \((\sqrt{x}-\sqrt{a})/(x-a)\)); no ε–δ; L'Hôpital stays on its sibling.
- **Live pairwise:** each item stamps `form_id`, `generator=limit_removable`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt inside the leftover band.
- **Generator:** `limit_removable`

## Proposed engine (reuse vs new)

- **Reuse:** LimitSpec `_sample_removable_factor` / `_sample_removable_rationalize` + generator `limit_removable` + `limits.json`. Catalog `d_max=10` on leftover rem_diff_sq. No padded `difficulty_costs`. Did not invent a true shared-quadratic / conjugate-pair / ε–δ core.
- **Shipped this pass:** leftover lockout of D=0 rem_diff_sq at D≥16; expanded cancel cannot collapse to rem_diff_sq latex; `form_id` + `generator` on `spec_snapshot`.
