# Notes — `calc_indef_int_power_rule`

- **Display name:** Power Rule
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_power_rule`
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Indefinite power-rule antiderivative \(+C\) (OpenStax §4.10 / §5.4).
- **D=0:** Old easy leftover \(\int c\,dx\) / \(\int \sum c_k x^k\) or frozen \(\int\sqrt{x}\,dx\).
- **Mid D (≈8):** That leftover still allowed, plus \(1/\sqrt{x}\), \(x\sqrt{x}\), \(k/x^n\) (\(n\ge 2\)), and rewrite \(\int(x^2+c\sqrt[3]{x})/x\).
- **High D (≈16):** Lock out `poly_sum` / \(\sqrt{x}\). Mid leftover plus rewrite / neg-power.
- **Expert (≈22):** Rewrite and neg-power only.
- **Must not:** Trig / \(e^x\) / \(1/x\) (other leaves); u-sub; padded `difficulty_costs`; new cores (Ex. 4.50 \(\cos x\) / \(e^x\), Ex. 5.23 \(\sqrt{t}(1+t)\)).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Live path is `calculus_integrals` → `_sample_power` on `basic_power_integrals`. Accumulating catalog pool (`poly_sum`/`sqrt_x` at D=0; all six from D≥6), so D=16 and D=22 were the same six-family pool as D=8. `form_id` / `generator=integral_power_rule` already stamped on metadata and `spec_snapshot`. 40-seed counts: D=0 `poly_sum` 24 / `sqrt_x` 16; D=8 leftover mix (`rewrite` 11 / `x_sqrt_x` 9 / `poly_sum` 7 / `sqrt_x` 7 / `neg_power` 4 / `one_over_sqrt_x` 2); D=16/22 identical (`rewrite` 13 / `poly_sum` 7 / `x_sqrt_x` 7 / `sqrt_x` 5 / `one_over_sqrt` 4 / `neg_power` 4).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int 3 \, dx$ | $3x+C$ | `poly_sum` |
| 0 | 207 | $\int \sqrt{x}\,dx$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | `sqrt_x` |
| 8 | 101 | $\int -3x^{4} + 3 \, dx$ | $3x-\frac{3}{5}x^{5}+C$ | `poly_sum` leftover |
| 8 | 207 | $\int \frac{x^{2}+5\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+15x^{\frac{1}{3}}+C$ | `rewrite_over_x` |
| 16 | 101 | $\int 6x^{4} + 2 \, dx$ | $2x+\frac{6}{5}x^{5}+C$ | `poly_sum` leftover at D=16 |
| 16 | 207 | $\int \frac{x^{2}+5\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+15x^{\frac{1}{3}}+C$ | `rewrite_over_x` |
| 22 | 101 | $\int 3x^{4} - 2 \, dx$ | $-2x+\frac{3}{5}x^{5}+C$ | `poly_sum` leftover at expert |
| 22 | 207 | $\int \frac{x^{2}+5\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+15x^{\frac{1}{3}}+C$ | `rewrite_over_x`; same pool as D=16 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same six builders. D=0 stays old `poly_sum` / \(\sqrt{x}\). Gallery seeds 101/207 can collide on one form at mid D; rotation is across seeds. Catalog `d_max` plus exclusive bands; `select_form_id` keeps catalog D-weights among the band.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int 3 \, dx$ | $3x+C$ | `poly_sum` |
| 0 | 207 | $\int \sqrt{x}\,dx$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | `sqrt_x` |
| 8 | 101 | $\int -3x^{4} + 3 \, dx$ | $3x-\frac{3}{5}x^{5}+C$ | `poly_sum` leftover |
| 8 | 207 | $\int \frac{x^{2}+5\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+15x^{\frac{1}{3}}+C$ | `rewrite_over_x` |
| 16 | 101 | $\int \frac{1}{\sqrt{x}}\,dx$ | $2\sqrt{x}+C$ | `one_over_sqrt_x` leftover (no `poly_sum`) |
| 16 | 207 | $\int \frac{x^{2}+5\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+15x^{\frac{1}{3}}+C$ | `rewrite_over_x` |
| 22 | 101 | $\int \frac{1}{x^{3}}\,dx$ | $-\frac{1}{2}x^{-2}+C$ | `neg_power` only vs rewrite |
| 22 | 207 | $\int \frac{x^{2}+5\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+15x^{\frac{1}{3}}+C$ | `rewrite_over_x` |

40-seed counts **after**: D=0 `poly_sum` 24 / `sqrt_x` 16; D=8 leftover mix (same six as old); D=16 `rewrite` 14 / `one_over_sqrt` 10 / `neg_power` 10 / `x_sqrt_x` 6 (no `poly_sum` / `sqrt_x`); D=22 `rewrite` 24 / `neg_power` 16.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.10 Antiderivatives | https://openstax.org/books/calculus-volume-1/pages/4-10-antiderivatives | \(\int x^n\,dx\) power rule \(+C\). Ex. 4.50 also has \(1/x\), \(\cos x\), \(e^x\) — those stay on log/exp / trig leaves, not this power leaf |
| OpenStax Calculus Volume 1 §5.4 Integration Formulas | https://openstax.org/books/calculus-volume-1/pages/5-4-integration-formulas-and-the-net-change-theorem | Power-rule rewrite (Ex. 5.23 \(\sqrt{t}(1+t)\)); old path is frozen \((x^2+c\sqrt[3]{x})/x\), not that product |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (4-10, 5-4).

## Variety notes

Not a WP. D=0 one easy poly-or-root (old). Same-D leftover mix at D=8 (that plus rewrite / neg-power / other roots). High D keeps the old rewrite and \(k/x^n\) builders (do not invent Ex. 4.50 trig/exp or Ex. 5.23 \(\sqrt{t}(1+t)\)). Six old forms, so D=16 mixes mid leftover + rewrite/neg-power and D=22 is rewrite / neg-power only.

## Limitations

- **Status:** shipped — leftover lockout of D=0 `poly_sum` / \(\sqrt{x}\). Remaining `LIMITATIONS`: six frozen old builders (`poly_sum` term mix; frozen \(\sqrt{x}\) / \(1/\sqrt{x}\) / \(x\sqrt{x}\); frozen rewrite \((x^2+c\sqrt[3]{x})/x\); \(k/x^n\) with \(n\in\{2,3,4\}\)); no Ex. 4.50 \(1/x\) / \(\cos x\) / \(e^x\) (other leaves); no Ex. 5.23 \(\sqrt{t}(1+t)\); D=16 can still emit \(1/\sqrt{x}\) / \(x\sqrt{x}\) leftover (intentional); shared generator also leftover-locks `pc_indefinite_integrals`.
- **Live pairwise:** each item stamps `form_id`, `generator=integral_power_rule`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `integral_power_rule`

## Proposed engine (reuse vs new)

- **Reuse:** existing `_sample_power` builders in `integrals.py` + `basic_power_integrals.json`. Depth = leftover lockout of `poly_sum` / \(\sqrt{x}\), not a new trig/exp/rewrite-product core.
- **Not this pass:** Ex. 4.50 non-power table; Ex. 5.23 \(\sqrt{t}(1+t)\); logarithmic \(1/x\).
