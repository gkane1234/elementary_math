# Notes — `calc_def_int_substitution_with_change_of_variables`

- **Display name:** Substitution with change of variables
- **Category:** Calculus — Definite Integration
- **Generator:** `integral_definite_substitution`
- **Suggested family:** `integral`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Definite u-sub with changed limits (not indefinite +C).
- **D=0:** Old easy leftover \(\int_0^b p(px+q)^n\,dx\) linear \(u\).
- **Mid D (≈8):** That leftover still allowed, plus \(\int_0^a 2x(x^{2}+1)^n\,dx\).
- **High D (≈16):** Lock out linear. Quad leftover plus \(\int_0^a \frac{2x}{x^{2}+1}\,dx=\ln(a^{2}+1)\).
- **Expert (≈22):** \(du/u\) only.
- **Must not:** Indefinite-only prompts on this leaf (see `calc_indef_int_power_rule_with_substitution`); padded `difficulty_costs`; new cores (Ex. 5.31 \(\sin^2\theta\cos\theta\), Ex. 5.32 \(e^{\sqrt{x}}/\sqrt{x}\), reverse limits).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Live path is `calculus_integrals` → `_sample_definite_u_sub`. Accumulating pool (`linear`; `+quad` at D≥8; `+du/u` at D≥12), so D=16 and D=22 were the same three-family pool as D=12. `form_id` / `generator=integral_definite_substitution` already stamped on metadata and `spec_snapshot`. 40-seed counts: D=0 `definite_power_linear_du` 40; D=8 leftover mix (`linear` 25 / `quad` 15); D=12/16/22 identical (`du_over_u` 15 / `linear` 16 / `quad` 9).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int_{0}^{3} 2\left(2x + 2\right)^{2}\,dx$ | $168$ | `definite_power_linear_du` |
| 0 | 207 | $\int_{0}^{1} 2\left(2x\right)^{2}\,dx$ | $\frac{8}{3}$ | `definite_power_linear_du` |
| 8 | 101 | $\int_{0}^{3} 2\left(2x + 2\right)^{2}\,dx$ | $168$ | linear leftover |
| 8 | 207 | $\int_{0}^{1} 2x\left(x^{2}+1\right)^{2}\,dx$ | $\frac{7}{3}$ | `definite_power_quad_x_du` |
| 16 | 101 | $\int_{0}^{3} 2\left(2x + 2\right)^{2}\,dx$ | $168$ | linear leftover at D=16 |
| 16 | 207 | $\int_{0}^{3} \frac{2x}{x^{2}+1}\,dx$ | $\ln(10)$ | `definite_du_over_u` |
| 22 | 101 | $\int_{0}^{3} 2\left(2x + 2\right)^{2}\,dx$ | $168$ | `definite_power_linear_du` leftover at expert |
| 22 | 207 | $\int_{0}^{3} \frac{2x}{x^{2}+1}\,dx$ | $\ln(10)$ | `definite_du_over_u`; same pool as D=16 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same three builders. D=0 stays old linear \(u\). Gallery seeds 101/207/313 can collide on one form at mid D; rotation is across seeds. `select_form_id` consumes RNG, so same seed is not bitwise-identical to the accumulating `rng.choice` path.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int_{0}^{2} 3\left(3x\right)^{2}\,dx$ | $72$ | `definite_power_linear_du` |
| 0 | 0 | $\int_{0}^{1} 2\left(2x + 2\right)^{3}\,dx$ | $60$ | `definite_power_linear_du` |
| 8 | 101 | $\int_{0}^{2} 3\left(3x\right)^{2}\,dx$ | $72$ | linear leftover |
| 8 | 0 | $\int_{0}^{1} 2x\left(x^{2}+1\right)^{2}\,dx$ | $\frac{7}{3}$ | `definite_power_quad_x_du` |
| 16 | 101 | $\int_{0}^{2} 2x\left(x^{2}+1\right)^{2}\,dx$ | $\frac{124}{3}$ | quad leftover (no linear) |
| 16 | 0 | $\int_{0}^{1} \frac{2x}{x^{2}+1}\,dx$ | $\ln(2)$ | `definite_du_over_u` |
| 22 | 101 | $\int_{0}^{2} \frac{2x}{x^{2}+1}\,dx$ | $\ln(5)$ | `definite_du_over_u` only |
| 22 | 0 | $\int_{0}^{1} \frac{2x}{x^{2}+1}\,dx$ | $\ln(2)$ | `definite_du_over_u` only |

40-seed counts **after**: D=0 `definite_power_linear_du` 40; D=8 leftover `quad` 22 / `linear` 18; D=16 leftover `du_over_u` 22 / `quad` 18 (no linear); D=22 `definite_du_over_u` 40.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.5 Substitution | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | Definite substitution; change limits with \(u\) (obj. 5.5.2). Ex. 5.31 \(\int_0^{\pi/2}\sin^2\theta\cos\theta\,d\theta\); Ex. 5.32 \(\int_1^4 e^{\sqrt{x}}/\sqrt{x}\,dx\); Checkpoint 5.30 reverse limits — old path is frozen linear \(p(px+q)^n\) / \(2x(x^{2}+1)^n\) / \(2x/(x^{2}+1)\) on \([0,b]\), not these |
| OpenStax Calculus Volume 1 §5.5 (indefinite sibling) | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | Indefinite \(+C\) u-sub stays on `calc_indef_int_power_rule_with_substitution` |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-5).

## Variety notes

Not a WP. D=0 one easy linear changed-limits (old). Same-D leftover mix at D=8 (that plus quad inner). High D keeps the old \(du/u\) builder (do not invent trig/exp definite or reverse limits). Three old forms, so D=16 mixes quad leftover + \(du/u\) and D=22 is \(du/u\)-only.

## Limitations

- **Status:** shipped — leftover lockout of D=0 linear \(u\). Remaining `LIMITATIONS`: three frozen old builders (always \(a=0\); linear is \(p(px+q)^n\); quad is frozen \(2x(x^{2}+1)^n\); \(du/u\) is frozen \(2x/(x^{2}+1)\)); no Ex. 5.31 \(\sin^2\theta\cos\theta\), no Ex. 5.32 \(e^{\sqrt{x}}/\sqrt{x}\), no reverse limits; D=16 can still emit quad leftover (intentional); named EMH presets on this leaf lock power/challenging families that the definite sampler does not consume.
- **Live pairwise:** each item stamps `form_id`, `generator=integral_definite_substitution`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `integral_definite_substitution`

## Proposed engine (reuse vs new)

- **Reuse:** existing linear / quad / \(du/u\) builders in `integrals.py` `_sample_definite_u_sub`. Depth = leftover lockout of linear, not a new definite-trig/exp core.
- **Not this pass:** Ex. 5.31 / 5.32 / Checkpoint 5.30; indefinite \(+C\) (power-with-substitution leaf); wiring named EMH `u_sub_form_preset` into the definite sampler.
