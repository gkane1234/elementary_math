# Notes — `calc_indef_int_logarithmic_rule_and_exponentials`

- **Display name:** Logarithmic Rule and Exponentials
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_log_exp`
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Indefinite log-rule / exponential antiderivative \(+C\) (OpenStax §5.6 table).
- **D=0:** Old easy leftover \(\int 1/x\,dx\) or \(\int e^{x}\,dx\).
- **Mid D (≈8):** That leftover still allowed, plus \(\int a/(ax+b)\,dx\), \(\int e^{kx}\,dx\) (\(k\ge 2\)), and \(\int a^{x}\,dx\).
- **High D (≈16):** Lock out `ln` / `exp`. Mid leftover plus `base_a`.
- **Expert (≈22):** `ln_linear` and `base_a` only.
- **Must not:** u-sub chains (those stay on the substitution sibling); \(\int\log_a x\) (parts); padded `difficulty_costs`; new cores (Ex. 5.37 \(e^{-x}\), Ex. 5.38 \(e^{x}\sqrt{1+e^{x}}\)).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Live path is `calculus_integrals` → `_sample_ln_exp`. Ungated five-family mix (`ln` / `ln_linear` / `exp` / `exp_k` / `base_a`) at every D, so D=16 and D=22 were the same pool as D=0. `form_id` / `generator=integral_log_exp` already stamped via `family` fallback on metadata and `spec_snapshot`. 40-seed counts identical at every D: `exp_k` 15 / `base_a` 10 / `ln_linear` 6 / `exp` 5 / `ln` 4.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{3}{3x + 3}\,dx$ | $\ln\lvert 3x + 3\rvert+C$ | `ln_linear` |
| 0 | 207 | $\int 3^{x}\,dx$ | $\frac{3^{x}}{\ln 3}+C$ | `base_a` |
| 8 | 101 | $\int \frac{3}{3x + 3}\,dx$ | $\ln\lvert 3x + 3\rvert+C$ | `ln_linear` leftover |
| 8 | 207 | $\int 3^{x}\,dx$ | $\frac{3^{x}}{\ln 3}+C$ | `base_a` leftover |
| 16 | 101 | $\int \frac{3}{3x + 2}\,dx$ | $\ln\lvert 3x + 2\rvert+C$ | `ln_linear` leftover at D=16 |
| 16 | 207 | $\int 3^{x}\,dx$ | $\frac{3^{x}}{\ln 3}+C$ | `base_a` leftover at D=16 |
| 22 | 101 | $\int \frac{3}{3x - 2}\,dx$ | $\ln\lvert 3x - 2\rvert+C$ | `ln_linear` leftover at expert |
| 22 | 207 | $\int 3^{x}\,dx$ | $\frac{3^{x}}{\ln 3}+C$ | `base_a`; same pool as D=0 |

Opt-out flag used: _(none — live generator is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same five builders. D=0 is table \(\int 1/x\) / \(\int e^{x}\). Gallery seeds 101/207 can collide on one form at mid D; rotation is across seeds. Exclusive bands; `select_form_id` keeps equal D-weights among the band (quality tilt via `live_quality_form_weights`).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{1}{x}\,dx$ | $\ln\lvert x\rvert+C$ | `ln` |
| 0 | 207 | $\int e^{x}\,dx$ | $e^{x}+C$ | `exp` |
| 8 | 101 | $\int \frac{1}{x}\,dx$ | $\ln\lvert x\rvert+C$ | `ln` leftover |
| 8 | 207 | $\int 5^{x}\,dx$ | $\frac{5^{x}}{\ln 5}+C$ | `base_a` |
| 16 | 101 | $\int \frac{3}{3x + 2}\,dx$ | $\ln\lvert 3x + 2\rvert+C$ | `ln_linear` leftover (no `ln` / `exp`) |
| 16 | 207 | $\int 5^{x}\,dx$ | $\frac{5^{x}}{\ln 5}+C$ | `base_a` |
| 22 | 101 | $\int \frac{3}{3x - 2}\,dx$ | $\ln\lvert 3x - 2\rvert+C$ | `ln_linear` only vs `base_a` |
| 22 | 207 | $\int 5^{x}\,dx$ | $\frac{5^{x}}{\ln 5}+C$ | `base_a` |

40-seed counts **after**: D=0 `exp` 22 / `ln` 18; D=8 leftover mix (`base_a` 10 / `ln` 10 / `ln_linear` 9 / `exp` 6 / `exp_k` 5); D=16 `ln_linear` 15 / `base_a` 14 / `exp_k` 11 (no `ln` / `exp`); D=22 `base_a` 22 / `ln_linear` 18.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.6 | https://openstax.org/books/calculus-volume-1/pages/5-6-integrals-involving-exponential-and-logarithmic-functions | Table \(\int e^{x}\), \(\int a^{x}\), \(\int 1/x\). Checkpoint 5.38 \(\int 1/(x+2)\) is the `ln_linear` shape. Ex. 5.37 \(e^{-x}\) / Ex. 5.38 \(e^{x}\sqrt{1+e^{x}}\) / Ex. 5.39 \(3x^{2}e^{2x^{3}}\) are substitution — stay on the u-sub sibling. Ex. 5.47 \(\log_{2} x\) is parts, not this leaf. |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-6). Volume 2 §1.6 is the same table.

## Variety notes

Not a WP. D=0 one easy table form (old). Same-D leftover mix at D=8 (that plus linear-log / scaled-exp / other-base). High D keeps the old `ln_linear` and `base_a` builders (do not invent Ex. 5.37 \(e^{-x}\) or Ex. 5.47 \(\log_a x\)). Five old forms, so D=16 mixes mid leftover + `base_a` and D=22 is `ln_linear` / `base_a` only.

## Limitations

- **Status:** shipped — leftover lockout of D=0 `ln` / `exp`. Remaining `LIMITATIONS`: five frozen old builders (table \(\int 1/x\) / \(\int e^{x}\); \(\int e^{kx}\) with \(k\ge 2\); \(\int a/(ax+b)\); \(\int a^{x}\) for \(a\in\{2,3,5\}\)); no Ex. 5.37 \(e^{-x}\) / Ex. 5.38 \(e^{x}\sqrt{1+e^{x}}\) / Ex. 5.39 cubic-exp (u-sub sibling); no Ex. 5.47 \(\log_a x\) (parts); D=16 can still emit `exp_k` leftover (intentional).
- **Live pairwise:** each item stamps `form_id`, `generator=integral_log_exp`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `integral_log_exp`

## Proposed engine (reuse vs new)

- **Reuse:** existing `_sample_ln_exp` builders in `integrals.py`. Depth = leftover lockout of \(\int 1/x\) / \(\int e^{x}\), not a new substitution / \(\log_a x\) core.
- **Not this pass:** Ex. 5.37 \(e^{-x}\); Ex. 5.38–5.39 substitution; Ex. 5.47 \(\log_a x\).
