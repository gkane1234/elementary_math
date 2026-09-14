# Notes — `calc_continuity_determining_and_classifying` (`Determining and classifying`)

- **Course:** Calculus
- **Category:** Calculus — Continuity
- **Generator:** `limit_continuity`
- **Suggested family:** other (calc limits / Diff)
- **Precalc alias:** `pc_continuity` (same generator)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Classify continuity at a point (continuous / removable / jump / essential).
- **D=0:** Linear poly continuous, or removable hole \((x^{2}-a^{2})/(x-a)\) — old easy.
- **Mid D (≈8):** Leftover continuous / removable plus piecewise jump (const\|\|const or linear\|\|const).
- **High D (≈16–22):** Jump (linear\|\|const) and essential \(1/(x-a)\) — not leftover linear-continuous or rem_diff_sq.
- **Must not:** Only evaluate a numeric limit without classifying; invent a figure-bank / ε–δ core.

## What old / live path actually produced (real latex, D=0/8/16/22)

**Before this leftover pass** (`_generate_for_type`): D=0 `continuity_classify_continuous` 20 / `continuity_classify_removable` 20; D=8 leftover mix (`jump` 18 / `removable` 12 / `continuous` 10); D=16 and D=22 the **same** mix, still including leftover continuous/removable (`jump` 13 / `removable` 13 / `essential` 7 / `continuous` 7). Metadata already stamped `form_id` + `generator=limit_continuity` on `spec_snapshot`. No opt-out flag — live catalog **is** the old LimitSpec path.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Classify the continuity of }f(x)=3x - 3\text{ at }x=4.$` | `$\text{continuous}$` | leftover continuous |
| 8 | 101 | `$\text{Classify the continuity of }f(x)=3x - 3\text{ at }x=4.$` | `$\text{continuous}$` | leftover continuous |
| 16 | 101 | `$\text{Classify the continuity of }f(x)=\frac{1}{x-4}\text{ at }x=4.$` | `$\text{essential discontinuity}$` | essential |
| 22 | 101 | `$\text{Classify the continuity of }f(x)=\frac{1}{x-4}\text{ at }x=4.$` | `$\text{essential discontinuity}$` | essential |

Opt-out flag used: _none — LimitSpec `limit_continuity` / `limits.json` is the live default_

## What live path produces now (real latex)

Leftover lockout of D=0 linear-continuous / rem_diff_sq at D≥16 (`d_max=10` on those catalog forms). Sampler else-branch cannot silently emit leftover when catalog fid is empty or leftover. High-D jump uses the existing linear-left core (no leftover const\|\|const). Stamps `form_id` + `generator=limit_continuity` on metadata and `spec_snapshot`. 40-seed counts: D=0 `continuous` 20 / `removable` 20; D=8 leftover mix (`jump` 20 / `continuous` 10 / `removable` 10); D=16/22 `jump` 20 / `essential` 20 (no leftover; jump `left_kind=linear`).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 0 | `$\text{Classify the continuity of }f(x)=6x\text{ at }x=-5.$` | `$\text{continuous}$` | leftover continuous |
| 0 | 1 | `$\text{Classify the continuity of }f(x)=\frac{x^{2}-1}{x+1}\text{ at }x=-1.$` | `$\text{removable discontinuity}$` | leftover rem_diff_sq |
| 8 | 0 | `$\text{Classify the continuity of }f(x)=6x\text{ at }x=-5.$` | `$\text{continuous}$` | leftover continuous |
| 8 | 1 | `$\text{Classify the continuity of }f(x)=\begin{cases}-4&x<-1\\-1&x\ge -1\end{cases}\text{ at }x=-1.$` | `$\text{jump discontinuity}$` | leftover jump const |
| 8 | 11 | `$\text{Classify the continuity of }f(x)=\frac{x^{2}-25}{x-5}\text{ at }x=5.$` | `$\text{removable discontinuity}$` | leftover rem_diff_sq |
| 16 | 0 | `$\text{Classify the continuity of }f(x)=\begin{cases}5x + 31&x<-5\\5&x\ge -5\end{cases}\text{ at }x=-5.$` | `$\text{jump discontinuity}$` | linear jump (no leftover) |
| 16 | 1 | `$\text{Classify the continuity of }f(x)=\frac{1}{x+1}\text{ at }x=-1.$` | `$\text{essential discontinuity}$` | essential \(1/(x-a)\) |
| 22 | 0 | `$\text{Classify the continuity of }f(x)=\begin{cases}-7x - 31&x<-5\\9&x\ge -5\end{cases}\text{ at }x=-5.$` | `$\text{jump discontinuity}$` | linear jump |

Opt-out flag used: _none — live catalog on `limits.py` / `limits.json`_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §2.4 Continuity | https://openstax.org/books/calculus-volume-1/pages/2-4-continuity | types of discontinuity; continuity checklist; piecewise jump vs hole vs VA |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/2-4-continuity.md`; form catalog `limits.json` `continuity_classify_*`

## Variety notes

D=0 stays the two old-easy kinds (continuous linear / rem_diff_sq). D=8 leftover mix + jump. High D cannot emit leftover continuous or removable. Not a WP. Shared generator also leftover-locks `pc_continuity`.

## Limitations

- **Status:** leftover lockout of D=0 linear-continuous / rem_diff_sq shipped. Remaining `LIMITATIONS`: D=16 and D=22 are the same jump/essential mix; D=8 can still emit leftover continuous/removable (intentional); essential is frozen \(1/(x-a)\) (no osc / tan / higher-power VA on this leaf); jump right piece is always const; quadratic-poly continuous was a 40% variant of leftover continuous and is locked out with it (no separate harder-continuous form); no figure-bank piecewise / ε–δ / IVT-on-an-interval cores.
- **Live pairwise:** each item stamps `form_id`, `generator=limit_continuity`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt inside the leftover band.
- **Generator:** `limit_continuity`

## Proposed engine (reuse vs new)

- **Reuse:** LimitSpec `_sample_continuity` + generator `limit_continuity` + `limits.json`. Catalog `d_max=10` on leftover continuous/removable. No padded `difficulty_costs`. Did not invent an expanded-cancel classify / osc-essential / figure-bank core.
- **Shipped this pass:** leftover lockout of D=0 continuous/removable at D≥16; sampler cannot silently emit leftover when catalog fid is empty; high-D jump is linear-left; `form_id` + `generator` on `spec_snapshot`.
