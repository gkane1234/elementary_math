# Notes — `calc_app_diff_limits_in_form_of_definition_of_derivative` (`Limits in form of definition of derivative`)

- **Display name:** Limits in form of definition of derivative
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `definition_of_derivative` (shared with `calc_diff_definition_of_the_derivative` / `pc_definition_of_the_derivative`)
- **Suggested family:** other (text \(x\to a\) / \(h\to 0\) stems; no figure)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Recognize a canceling difference quotient as \(f'(a)\) and evaluate it from the definition (not power rule).
- **D=0:** Easy leftover — \(\lim_{x\to a}\frac{x^{2}-a^{2}}{x-a}\) or \(\lim_{h\to 0}\frac{(a+h)^{2}-a^{2}}{h}\) (old easy).
- **Mid D (≈8):** Easy leftover still allowed, plus cube, \(k(a+h)^{2}\), and named \(f(x)=kx^{2}\).
- **High D (≈16):** Lock out bare \(x^{2}\) limits. Medium leftover plus reciprocal / \(\sqrt{\,\cdot\,}\) / named \(px^{2}+q\).
- **Expert (≈22):** Reciprocal / square-root / named-poly only.
- **Must not:** Pure power-rule “find \(f'\)” without a limit / definition stem; padded `difficulty_costs`; a general \(f\) AST.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. `_pick_family` accumulated easy+medium+hard once `unlock_hard` (D≥10), so D=16 and D=22 were the same 8-family pool. `form_id` unstamped (`family` / `structure_id` only). 40-seed counts: D=0 `limit_x` 19 / `limit_h` 21; D=8 leftover mix; D=16 and D=22 identical (`limit_x` 8, `named` 8, `cube` 5, `limit_h` 4, `linear_coef` 4, `sqrt` 4, `reciprocal` 4, `poly` 3).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\lim_{x\to 1}\frac{x^{2}-1}{x-1}$ | $2$ | `limit_x` |
| 0 | 207 | $\lim_{h\to 0}\frac{(1+h)^{2}-1}{h}$ | $2$ | `limit_h` |
| 8 | 101 | $\text{Use the definition to find }f'(2)\text{ for }f(x)=3x^{2}.$ | $12$ | `named` |
| 8 | 207 | $\lim_{x\to 2}\frac{x^{2}-4}{x-2}$ | $4$ | leftover `limit_x` |
| 8 | 313 | $\lim_{h\to 0}\frac{3(2+h)^{2}-12}{h}$ | $12$ | `linear_coef` |
| 16 | 101 | $\lim_{h\to 0}\frac{4(5+h)^{2}-100}{h}$ | $40$ | `linear_coef`; same pool as D=22 |
| 16 | 207 | $\lim_{h\to 0}\frac{4(5+h)^{2}-100}{h}$ | $40$ | identical to D=22 seed=207 |
| 16 | 313 | $\lim_{h\to 0}\frac{(5+h)^{3}-125}{h}$ | $75$ | `cube` |
| 22 | 101 | $\lim_{h\to 0}\frac{4(5+h)^{2}-100}{h}$ | $40$ | frozen identical to D=16 |
| 22 | 207 | $\lim_{h\to 0}\frac{4(5+h)^{2}-100}{h}$ | $40$ | frozen identical to D=16 |
| 22 | 313 | $\lim_{h\to 0}\frac{(5+h)^{3}-125}{h}$ | $75$ | frozen identical to D=16 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same eight builders. D=0 stays old \(x^{2}\) limits. Gallery seeds 101/207/313 can collide on one form at a given D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\lim_{x\to 1}\frac{x^{2}-1}{x-1}$ | $2$ | `limit_x` |
| 0 | 2 | $\lim_{h\to 0}\frac{(1+h)^{2}-1}{h}$ | $2$ | `limit_h` |
| 8 | 2 | $\lim_{h\to 0}\frac{(1+h)^{2}-1}{h}$ | $2$ | leftover `limit_h` |
| 8 | 101 | $\text{Use the definition to find }f'(2)\text{ for }f(x)=4x^{2}.$ | $16$ | `named` |
| 16 | 313 | $\lim_{h\to 0}\frac{(5+h)^{3}-125}{h}$ | $75$ | leftover `cube` |
| 16 | 0 | $\lim_{h\to 0}\frac{\sqrt{4+h}-\sqrt{4}}{h}$ | $\frac{1}{4}$ | `sqrt` (no \(x^{2}\) leftover) |
| 22 | 101 | $\text{Use the definition to find }f'(5)\text{ for }f(x)=-1 + 3x^{2}.$ | $30$ | `poly` only |
| 22 | 207 | $\lim_{h\to 0}\frac{\sqrt{9+h}-\sqrt{9}}{h}$ | $\frac{1}{6}$ | `sqrt` only |

40-seed counts **after**: D=0 `limit_x` 22 / `limit_h` 18; D=8 leftover easy + cube / linear_coef / named (4+8+9+12+7); D=16 medium leftover + hard (no `limit_h`/`limit_x`); D=22 `poly`/`sqrt`/`reciprocal` only.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.1 Defining the Derivative | https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative | Two equivalent limits: \(\lim_{h\to 0}\frac{f(a+h)-f(a)}{h}\) and \(\lim_{x\to a}\frac{f(x)-f(a)}{x-a}\) |
| OpenStax Calculus Volume 1 §3.1 (square-root / reciprocal) | https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative | High-D builders already on this leaf: \(\sqrt{x}\) and \(1/x\) difference quotients — not a new core |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (3-1). Instantaneous-rate wording stays on `calc_diff_instantaneous_rates_of_change`; the Differentiation sibling `calc_diff_definition_of_the_derivative` shares this generator.

## Variety notes

Not a WP. D=0 rotates the two easy stems (\(x\to a\) vs \(h\to 0\)). Same-D rotation at mid D: leftover easy vs cube / \(k x^{2}\) / named. High D keeps the old reciprocal / sqrt / named-poly builders (do not invent a general \(f\)). Eight old forms, so D=16 mixes medium leftover + hard and D=22 is hard-only.

## Limitations

- **Status:** shipped — leftover lockout of D=0 \(x^{2}\) limits. Remaining `LIMITATIONS`: eight frozen old builders (no general \(f\); no trig / exp definition limits; no piecewise / one-sided); D=16 can still emit cube / \(k(a+h)^{2}\) / named leftover (intentional); named-poly is still \(px^{2}+q\), not a cubic; shared generator also leftover-locks `calc_diff_definition_of_the_derivative` / `pc_definition_of_the_derivative`.
- **Live pairwise:** each item stamps `form_id` (= family), shared `generator=definition_of_derivative`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `definition_of_derivative`

## Proposed engine (reuse vs new)

- **Reuse:** existing `calculus_derivative_rules._definition_of_derivative` builders. Depth = real structure (lock out easy \(x^{2}\) limits; mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** general \(f\) AST; trig / exp / piecewise definition limits; a second independent generator for the Differentiation sibling.
