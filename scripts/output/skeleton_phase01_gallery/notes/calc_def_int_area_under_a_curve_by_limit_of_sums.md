# Notes — `calc_def_int_area_under_a_curve_by_limit_of_sums` (`Area under a curve by limit of sums`)

- **Display name:** Area under a curve by limit of sums
- **Category:** Calculus — Definite Integration
- **Generator:** `area_under_curve` (shared with `calc_app_int_area_under_a_curve`)
- **Suggested family:** other (OpenStax §5.2 definition / \(\lim\sum\); live stem is FTC area)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate a definite integral from the **definition** (right-endpoint Riemann sum, then \(n\to\infty\)). Not FTC “find the area under \(y=f\)”.
- **D=0:** As simple as old easy: still FTC \(y=x\) on \([0,b]\) — that is the live path, not gold.
- **High D (≈16–22):** Gold would be a \(\lim_{n\to\infty}\sum f(x_i^*)\Delta x\) / definition setup (OpenStax Ex. 5.7). Live high D is leftover-locked \(y=kx^{2}\) FTC area.
- **Must not:** Invent a new Riemann-limit core; rewire onto finite-\(n\) `riemann_approximate_area` (that is the approximating sibling) or table `riemann_sum_tables`.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**. Catalog generator is `area_under_curve` (FTC area stem). Leftover lockout of \(y=x\) already ships on that shared core (`calc_app_int_area_under_a_curve`). No \(\sum\), \(\lim\), or “Riemann” in any sampled prompt. 40-seed counts: D=0 `auc_linear` 40; D=8 leftover `auc_quad` 21 / `auc_linear` 19; D=16 leftover `auc_quad_coef` 21 / `auc_quad` 19 (no `auc_linear`); D=22 `auc_quad_coef` 40.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the area under }y=x\text{ from }x=0\text{ to }x=2.$ | $2$ | `auc_linear` — FTC area, not \(\lim\sum\) |
| 0 | 0 | $\text{Find the area under }y=x\text{ from }x=0\text{ to }x=3.$ | $\frac{9}{2}$ | old easy \(y=x\) |
| 8 | 1 | $\text{Find the area under }y=x\text{ from }x=0\text{ to }x=2.$ | $2$ | \(y=x\) leftover |
| 8 | 101 | $\text{Find the area under }y=x^{2}\text{ from }x=0\text{ to }x=3.$ | $9$ | `auc_quad` |
| 16 | 1 | $\text{Find the area under }y=x^{2}\text{ from }x=0\text{ to }x=2.$ | $\frac{8}{3}$ | \(x^{2}\) leftover |
| 16 | 101 | $\text{Find the area under }y=4x^{2}\text{ from }x=0\text{ to }x=3.$ | $36$ | no \(y=x\); still FTC wording |
| 22 | 101 | $\text{Find the area under }y=4x^{2}\text{ from }x=0\text{ to }x=3.$ | $36$ | `auc_quad_coef` only |
| 22 | 207 | $\text{Find the area under }y=2x^{2}\text{ from }x=0\text{ to }x=6.$ | $144$ | still “Find the area under”, not a definition sum |

Opt-out flag used: _(none — live catalog is the old path)_

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.2 The Definite Integral | https://openstax.org/books/calculus-volume-1/pages/5-2-the-definite-integral | Ex. 5.7: use the **definition** to evaluate \(\int_0^2 x^{2}\,dx\) (right-endpoint Riemann sum, then \(n\to\infty\)). Checkpoint 5.7: same for \(\int_0^3(2x-1)\,dx\). Exercises 60–63: identify \(\lim_{n\to\infty}\sum f(x_i^*)\Delta x\) as a definite integral |
| OpenStax Calculus Volume 1 §5.1 Approximating Areas | https://openstax.org/books/calculus-volume-1/pages/5-1-approximating-areas | Finite L/R/mid sums stay on `calc_def_int_approximating_area_under_a_curve`; tables stay on `calc_def_int_riemann_sum_tables` |
| OpenStax Calculus Volume 1 §5.3 / §6.1 | https://openstax.org/books/calculus-volume-1/pages/5-3-the-fundamental-theorem-of-calculus | FTC “area under \(y=f\)” stays on `calc_app_int_area_under_a_curve` |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-2).

## Variety notes / UNCLEAR flag

UNCLEAR — gold look is OpenStax definition / \(\lim\sum\); live path is the FTC area sibling. Not a WP. Leftover lockout on `area_under_curve` is real structure for the **wrong** skill (D=22 \(y=kx^{2}\) only). Do not leftover-lock this leaf further as if it were limit-of-sums.

## Limitations

- **Status:** skipped — `UNCLEAR` / `LIMITATIONS` / `NOT_IMPLEMENTED`. Live generator is shared FTC `area_under_curve` (“Find the area under \(y=\ldots\)”). OpenStax Ex. 5.7 definition (right-endpoint sum \(\to n\to\infty\)) has **no existing core**. Finite-\(n\) `riemann_approximate_area` and table `riemann_sum_tables` are other leaves. Did not invent a \(\lim\sum\) core.
- **Wrong skill:** leftover lockout of \(y=x\) already ships on the shared generator; D=22 is \(y=kx^{2}\) FTC area, not a harder definition-sum.
- **Live pairwise:** stamps `form_id` / `generator=area_under_curve` (sibling metadata) — not a limit-of-sums `form_id`.
- **Generator:** `area_under_curve`

## Proposed engine (reuse vs new)

- **Reuse:** none honestly. `area_under_curve` is FTC area. `riemann_approximate_area` is finite \(n\) (“approximate”). `riemann_sum_tables` is table values.
- **New:** a definition / \(\lim\sum\) core would be required to match Ex. 5.7. **Not this pass** — do not invent cores (`benchmark-old-path` skip).
- **Leave the leaf** until a limit-of-sums core exists.
