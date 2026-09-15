# Notes — `calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime` (`Graphical comparison of f, f', and f''`)

- **Display name:** Graphical comparison of f, f', and f''
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `graphical_f_fp`
- **Suggested family:** other (sign of an explicit \(f'\); no figure bank)

---

## What the question should look like (D=0 vs high D)

- **Skill:** From an explicit \(f'\), say on which interval(s) \(f\) is increasing or decreasing.
- **D=0:** Linear leftover \(f'(x)=x-c\), decreasing on \((-\infty,c)\) (old easy).
- **Mid / high / expert (≈8–22):** Lock out linear leftover. Quadratic \(f'(x)=x^{2}-a^{2}\), increasing on \((-\infty,-a)\cup(a,\infty)\). Exclusive cliff already (`d<8` linear, else quadratic) — D=8, D=16, and D=22 are the same quadratic builder.
- **Must not:** Graph-match figures of \(f\) / \(f'\) / \(f''\) (OpenStax §4.5 gold — no figure bank); padded `difficulty_costs`; a cubic \(f'\) / \(f''\) core.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before generator stamps. Exclusive cliff already (`d<8` linear, else quadratic). `form_id` was present; `generator` / `spec_snapshot` unstamped. 40-seed counts: D=0 all `fp_linear_sign`; D=8/16/22 all `fp_quadratic_sign` (no linear leftover at D=16).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $f'(x)=x-5.\text{ On which interval is }f\text{ decreasing?}$ | $(-\infty,5)$ | linear leftover |
| 0 | 0 | $f'(x)=x-4.\text{ On which interval is }f\text{ decreasing?}$ | $(-\infty,4)$ | frozen old easy |
| 8 | 101 | $f'(x)=x^{2}-4.\text{ On which intervals is }f\text{ increasing?}$ | $(-\infty,-2)\cup(2,\infty)$ | quadratic (no leftover mix) |
| 16 | 101 | $f'(x)=x^{2}-4.\text{ On which intervals is }f\text{ increasing?}$ | $(-\infty,-2)\cup(2,\infty)$ | same quadratic |
| 22 | 207 | $f'(x)=x^{2}-4.\text{ On which intervals is }f\text{ increasing?}$ | $(-\infty,-2)\cup(2,\infty)$ | D=16===D=22 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout made explicit on the same two builders (`select_form_id` exclusive bands). Same live algebra; stamps `form_id` + `generator=graphical_f_fp` on metadata and `spec_snapshot`. `select_form_id` consumes RNG, so seed 101 D=0 is now \(c=2\) not \(c=5\).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $f'(x)=x-2.\text{ On which interval is }f\text{ decreasing?}$ | $(-\infty,2)$ | `fp_linear_sign` |
| 0 | 207 | $f'(x)=x-5.\text{ On which interval is }f\text{ decreasing?}$ | $(-\infty,5)$ | old easy \(c\) |
| 8 | 0 | $f'(x)=x^{2}-16.\text{ On which intervals is }f\text{ increasing?}$ | $(-\infty,-4)\cup(4,\infty)$ | `fp_quadratic_sign` |
| 8 | 101 | $f'(x)=x^{2}-4.\text{ On which intervals is }f\text{ increasing?}$ | $(-\infty,-2)\cup(2,\infty)$ | no linear leftover |
| 16 | 101 | $f'(x)=x^{2}-4.\text{ On which intervals is }f\text{ increasing?}$ | $(-\infty,-2)\cup(2,\infty)$ | same quadratic |
| 22 | 0 | $f'(x)=x^{2}-16.\text{ On which intervals is }f\text{ increasing?}$ | $(-\infty,-4)\cup(4,\infty)$ | D=8===D=16===D=22 |

40-seed counts **after**: D=0 `fp_linear_sign` 40; D=8/16/22 `fp_quadratic_sign` 40 (all `generator=graphical_f_fp`).

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.5 Derivatives and the Shape of a Graph | https://openstax.org/books/calculus-volume-1/pages/4-5-derivatives-and-the-shape-of-a-graph | Sign of \(f'\) → increase/decrease. Gold is graph-match of \(f\) / \(f'\) / \(f''\) figures — **no** existing figure bank |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (4-5).

## Variety notes

Not a WP. D=0 one easy linear \(f'\). Exclusive cliff already: D≥8 is the quadratic builder only (do not invent a D=8 leftover mix that reintroduces linear). Two frozen forms, so D=8===D=16===D=22. Gold graph-match stays skipped.

## Limitations

- **Status:** shipped — leftover lockout of D=0 linear \(f'\) (exclusive cliff already) plus `form_id` / `generator` stamps. Remaining `LIMITATIONS`: no graph-match figure bank (OpenStax §4.5 figures); two frozen old builders (linear decreasing \(x-c\); quadratic increasing \(x^{2}-a^{2}\)); D=8===D=16===D=22 quadratic only; no cubic \(f'\) / \(f''\) stem.
- **Live pairwise:** each item stamps `form_id`, `generator=graphical_f_fp`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt (exclusive bands are one form each).
- **Generator:** `graphical_f_fp`

## Proposed engine (reuse vs new)

- **Reuse:** existing linear / quadratic sign-of-\(f'\) builders in `calc_app_diff.py`. Depth = real structure (lock out linear leftover) — not padded `difficulty_costs`.
- **Not this pass:** figure bank; graph-match of \(f\) / \(f'\) / \(f''\); cubic \(f'\).
