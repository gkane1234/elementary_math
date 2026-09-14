# Notes — `calc_diff_average_rates_of_change` (`Average rates of change`)

- **Display name:** Average rates of change
- **Category:** Calculus — Differentiation
- **Generator:** `average_rate_of_change` (shared with `pc_average_rates_of_change`)
- **Suggested family:** diff / other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Compute \(\frac{f(b)-f(a)}{b-a}\) for a named \(f\) on a closed interval (not \(f'(a)\)).
- **D=0:** Easy leftover — \(f(x)=x^{2}\) on \([a,b]\) (old easy).
- **Mid D (≈8):** Easy leftover still allowed, plus cubic \(kx^{3}\), \(px^{2}+q\), and linear \(mx+c\).
- **High D (≈16):** Lock out bare \(x^{2}\). Medium leftover plus \(px^{2}+qx+r\), \(x^{3}+x\), and \(1/x\).
- **Expert (≈22):** Poly / shifted cubic / reciprocal only.
- **Must not:** Instantaneous-rate \(f'(a)\) stems (that leaf); padded `difficulty_costs`; a new \(\sqrt{x}\) / trig / story \(s(t)\) core.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. `_pick_family` accumulated easy+medium+hard once `unlock_hard` (D≥10), so D=16 and D=22 were the same 7-family pool. `form_id` unstamped (`family` / `structure_id` only). 40-seed counts: D=0 `quad` 40; D=8 leftover mix (`quad_const` 13 / `cubic` 10 / `quad` 9 / `linear` 8); D=16 and D=22 identical (`shifted` 8, `poly` 7, `quad` 6, `quad_const` 6, `reciprocal` 6, `cubic` 5, `linear` 2).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,3].$ | $4$ | `quad` |
| 0 | 207 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,2].$ | $3$ | `quad` |
| 8 | 101 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,5].$ | $6$ | leftover `quad` |
| 8 | 207 | $\text{Find the average rate of change of }f(x)=x^{2} + 3\text{ on }[1,2].$ | $3$ | `quad_const` |
| 8 | 313 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,5].$ | $6$ | leftover `quad` |
| 16 | 101 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,5].$ | $6$ | leftover `quad`; same pool as D=22 |
| 16 | 207 | $\text{Find the average rate of change of }f(x)=x^{3}+x\text{ on }[1,2].$ | $8$ | `shifted` |
| 16 | 313 | $\text{Find the average rate of change of }f(x)=\frac{1}{x}\text{ on }[1,2].$ | $-\frac{1}{2}$ | `reciprocal` |
| 22 | 101 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,5].$ | $6$ | frozen identical to D=16 |
| 22 | 207 | $\text{Find the average rate of change of }f(x)=x^{3}+x\text{ on }[1,2].$ | $8$ | frozen identical to D=16 |
| 22 | 313 | $\text{Find the average rate of change of }f(x)=\frac{1}{x}\text{ on }[1,2].$ | $-\frac{1}{2}$ | frozen identical to D=16 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same seven builders. D=0 stays old \(x^{2}\). Gallery seeds 101/207/313 can collide on one form at a given D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,3].$ | $4$ | `quad` |
| 0 | 2 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[0,1].$ | $1$ | `quad` |
| 8 | 101 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,5].$ | $6$ | leftover `quad` |
| 8 | 313 | $\text{Find the average rate of change of }f(x)=-2x + 3\text{ on }[1,5].$ | $-2$ | `linear` |
| 8 | 0 | $\text{Find the average rate of change of }f(x)=3x^{3}\text{ on }[3,4].$ | $111$ | `cubic` |
| 16 | 0 | $\text{Find the average rate of change of }f(x)=3 + 3x^{2}\text{ on }[3,4].$ | $21$ | leftover `quad_const` (no bare \(x^{2}\)) |
| 16 | 207 | $\text{Find the average rate of change of }f(x)=x^{3}+x\text{ on }[1,2].$ | $8$ | `shifted` |
| 16 | 313 | $\text{Find the average rate of change of }f(x)=\frac{1}{x}\text{ on }[1,2].$ | $-\frac{1}{2}$ | `reciprocal` |
| 22 | 101 | $\text{Find the average rate of change of }f(x)=-1 + x + x^{2}\text{ on }[1,5].$ | $7$ | `poly` only |
| 22 | 207 | $\text{Find the average rate of change of }f(x)=x^{-1}\text{ on }[2,3].$ | $-\frac{1}{6}$ | `reciprocal` only |
| 22 | 2 | $\text{Find the average rate of change of }f(x)=x^{3}+x\text{ on }[0,1].$ | $2$ | `shifted` only |

40-seed counts **after**: D=0 `quad` 40; D=8 leftover easy + cubic / linear / quad_const (11+9+10+10); D=16 medium leftover + hard (no `quad`); D=22 `poly`/`shifted`/`reciprocal` only (13+15+12).

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.4 | https://openstax.org/books/calculus-volume-1/pages/3-4-derivatives-as-rates-of-change | Average \(\frac{f(b)-f(a)}{b-a}\) vs instantaneous \(f'(a)\); keep the formula stem, not Ex. 3.34 free-fall story |
| OpenStax Precalculus 2e §1.3 | https://openstax.org/books/precalculus-2e/pages/1-3-rates-of-change-and-behavior-of-graphs | Average rate of a formula on \([a,b]\) — matches the old \(f(x)=\ldots\) on \([a,b]\) prompt |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (3-4). Instantaneous-rate wording stays on `calc_diff_instantaneous_rates_of_change`; Precalc `pc_average_rates_of_change` shares this generator.

## Variety notes

Not a WP. D=0 is the single old easy \(x^{2}\) builder (interval endpoints rotate). Same-D rotation at mid D: leftover \(x^{2}\) vs cubic / \(px^{2}+q\) / linear. High D keeps the old poly / \(x^{3}+x\) / \(1/x\) builders (do not invent \(\sqrt{x}\) / trig / \(s(t)=-16t^{2}\)). Seven old forms, so D=16 mixes medium leftover + hard and D=22 is hard-only.

## Limitations

- **Status:** shipped — leftover lockout of D=0 \(x^{2}\). Remaining `LIMITATIONS`: seven frozen old builders (no \(\sqrt{x}\) / trig / exp; no Ex. 3.34 free-fall story; no table/graph average rate); D=16 can still emit cubic / \(px^{2}+q\) / linear leftover (intentional); shifted is still \(x^{3}+x\), not a free cubic; shared generator also leftover-locks `pc_average_rates_of_change`.
- **Live pairwise:** each item stamps `form_id` (= family), shared `generator=average_rate_of_change`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `average_rate_of_change`

## Proposed engine (reuse vs new)

- **Reuse:** existing `calculus_derivative_rules._average_rate_of_change` builders. Depth = real structure (lock out easy \(x^{2}\); mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** \(\sqrt{x}\) / mixed \(x^{2}-1/x\) (Precalc §1.3 formula); trig / story \(s(t)\); a second independent generator for the Precalc sibling.
