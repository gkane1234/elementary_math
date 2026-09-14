# Notes — `calc_diff_instantaneous_rates_of_change` (`Instantaneous rates of change`)

- **Display name:** Instantaneous rates of change
- **Category:** Calculus — Differentiation
- **Generator:** `instantaneous_rate_of_change` (shared with `pc_instantaneous_rates_of_change`)
- **Suggested family:** diff / other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Compute \(f'(a)\) for a named \(f\) (instantaneous rate, not \(\frac{f(b)-f(a)}{b-a}\)).
- **D=0:** Easy leftover — monomial \(f(x)=x^{n}\) at a point (old easy).
- **Mid D (≈8):** Easy leftover still allowed, plus \(px^{2}+q\), \(\sqrt{x}\), and \(1/x\).
- **High D (≈16):** Lock out bare \(x^{n}\). Medium leftover plus cubic \(px^{3}+qx\), \(\sin x/\cos x\), and \(e^{kx}\).
- **Expert (≈22):** Cubic / trig / exp only.
- **Must not:** Average-rate interval stems (that leaf); padded `difficulty_costs`; a new free-fall \(s(t)=-16t^{2}\) / table / graph core.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. `_pick_family` accumulated easy+medium+hard+trig/exp once `unlock_hard` (D≥10), so D=16 and D=22 were the same 7-family pool. `form_id` unstamped (`family` / `structure_id` only). 40-seed counts: D=0 `power` 40; D=8 leftover mix (`power` 11 / `sqrt` 11 / `poly` 10 / `reciprocal` 8); D=16 and D=22 identical (`exp` 8, `cubic` 7, `sqrt` 7, `reciprocal` 6, `trig` 5, `power` 4, `poly` 3).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the instantaneous rate of change of }f(x)=x^{3}\text{ at }x=1.$ | $3$ | `power` |
| 0 | 207 | $\text{Find the instantaneous rate of change of }f(x)=x^{2}\text{ at }x=1.$ | $2$ | `power` |
| 8 | 101 | $\text{Find the instantaneous rate of change of }f(x)=\sqrt{x}\text{ at }x=4.$ | $\frac{1}{4}$ | leftover `sqrt` |
| 8 | 207 | $\text{Find the instantaneous rate of change of }f(x)=x^{2} + 1\text{ at }x=2.$ | $4$ | `poly` |
| 8 | 313 | $\text{Find the instantaneous rate of change of }f(x)=\frac{1}{x}\text{ at }x=4.$ | $-\frac{1}{16}$ | `reciprocal` |
| 16 | 101 | $\text{Find the instantaneous rate of change of }f(x)=2x^{3} - 3x\text{ at }x=2.$ | $21$ | leftover `cubic`; same pool as D=22 |
| 16 | 207 | $\text{Find the instantaneous rate of change of }f(x)=\sin(x)\text{ at }x=0.$ | $1$ | leftover `trig`; same pool as D=22 |
| 16 | 2 | $\text{Find the instantaneous rate of change of }f(x)=x^{2}\text{ at }x=1.$ | $2$ | leftover `power`; same pool as D=22 |
| 22 | 101 | $\text{Find the instantaneous rate of change of }f(x)=2x^{3} - 3x\text{ at }x=2.$ | $21$ | frozen identical to D=16 |
| 22 | 207 | $\text{Find the instantaneous rate of change of }f(x)=\sin(x)\text{ at }x=0.$ | $1$ | frozen identical to D=16 |
| 22 | 2 | $\text{Find the instantaneous rate of change of }f(x)=x^{2}\text{ at }x=1.$ | $2$ | leftover `power`; frozen identical to D=16 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same seven builders. D=0 stays old \(x^{n}\). Gallery seeds 101/207/313 can collide on one form at a given D; rotation is across seeds. `select_form_id` consumes RNG, so D=0 seed 101 is now \(x^{4}\) not the pre-lockout \(x^{3}\).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the instantaneous rate of change of }f(x)=x^{4}\text{ at }x=1.$ | $4$ | `power` |
| 0 | 207 | $\text{Find the instantaneous rate of change of }f(x)=x^{2}\text{ at }x=1.$ | $2$ | `power` |
| 8 | 2 | $\text{Find the instantaneous rate of change of }f(x)=x^{3}\text{ at }x=1.$ | $3$ | leftover `power` |
| 8 | 207 | $\text{Find the instantaneous rate of change of }f(x)=x^{1/2}\text{ at }x=1.$ | $\frac{1}{2}$ | `sqrt` |
| 8 | 101 | $\text{Find the instantaneous rate of change of }f(x)=x^{-1}\text{ at }x=3.$ | $-\frac{1}{9}$ | `reciprocal` |
| 16 | 2 | $\text{Find the instantaneous rate of change of }f(x)=2x^{2} - 2\text{ at }x=1.$ | $4$ | leftover `poly` (no bare \(x^{n}\)) |
| 16 | 207 | $\text{Find the instantaneous rate of change of }f(x)=\sin(x)\text{ at }x=0.$ | $1$ | `trig` |
| 16 | 101 | $\text{Find the instantaneous rate of change of }f(x)=e^{3x}\text{ at }x=0.$ | $3$ | `exp` |
| 22 | 2 | $\text{Find the instantaneous rate of change of }f(x)=2x^{3} + 3x\text{ at }x=1.$ | $9$ | `cubic` only |
| 22 | 1 | $\text{Find the instantaneous rate of change of }f(x)=\sin(x)\text{ at }x=0.$ | $1$ | `trig` only |
| 22 | 101 | $\text{Find the instantaneous rate of change of }f(x)=e^{3x}\text{ at }x=0.$ | $3$ | `exp` only |

40-seed counts **after**: D=0 `power` 40; D=8 leftover easy + poly / sqrt / reciprocal (5+13+11+11); D=16 medium leftover + hard (no `power`); D=22 `cubic`/`trig`/`exp` only (10+16+14).

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.4 | https://openstax.org/books/calculus-volume-1/pages/3-4-derivatives-as-rates-of-change | Instantaneous \(f'(a)\) vs average \(\frac{f(b)-f(a)}{b-a}\); keep the formula stem, not Ex. 3.34 free-fall story |
| OpenStax Precalculus 2e §12.3 | https://openstax.org/books/precalculus-2e/pages/12-3-derivatives | Derivative at a point from a formula — matches the old \(f(x)=\ldots\) at \(x=a\) prompt |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (3-4). Average-rate wording stays on `calc_diff_average_rates_of_change`; Precalc `pc_instantaneous_rates_of_change` shares this generator.

## Variety notes

Not a WP. D=0 is the single old easy \(x^{n}\) builder (\(n\in\{2,3,4\}\); evaluation point rotates). Same-D rotation at mid D: leftover \(x^{n}\) vs \(px^{2}+q\) / \(\sqrt{x}\) / \(1/x\). High D keeps the old cubic / trig-at-0 / \(e^{kx}\) builders (do not invent \(s(t)=-16t^{2}\) / table / graph). Seven old forms, so D=16 mixes medium leftover + hard and D=22 is hard-only.

## Limitations

- **Status:** shipped — leftover lockout of D=0 \(x^{n}\). Remaining `LIMITATIONS`: seven frozen old builders (no Ex. 3.34 free-fall \(s(t)=-16t^{2}\); no table/graph instantaneous rate; trig is still \(\sin x/\cos x\) at 0 only; exp is still \(e^{kx}\) at 0); D=16 can still emit \(px^{2}+q\) / \(\sqrt{x}\) / \(1/x\) leftover (intentional); cubic is still \(px^{3}+qx\), not a free cubic; shared generator also leftover-locks `pc_instantaneous_rates_of_change`.
- **Live pairwise:** each item stamps `form_id` (= family), shared `generator=instantaneous_rate_of_change`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `instantaneous_rate_of_change`

## Proposed engine (reuse vs new)

- **Reuse:** existing `calculus_derivative_rules._instantaneous_rate_of_change` builders. Depth = real structure (lock out easy \(x^{n}\); mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** free-fall story / mixed \(x^{2}-1/x\); a second independent generator for the Precalc sibling.
