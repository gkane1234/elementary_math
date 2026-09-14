# Notes — `calc_diff_average_rates_of_change`

- **Display name:** Average rates of change
- **Category:** Calculus — Differentiation
- **Generator:** `average_rate_of_change`
- **Suggested family:** diff / other

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `average_rate_of_change`
- **Remaining limits:** Dedicated constructive / Mad-Lib-meta generators (not expr_skeleton gallery topics). Gaps: table/figure UX still text-only; logarithmic / inverse-function depth vs OpenStax §3.8–3.9 limited; implicit remains Mad-Lib (see that leaf).

## What the question should look like (D=0 vs high D)

- **Skill:** Average rates of change — match OpenStax shape below.
- **D=0:** As simple as live easy samples.
- **High D (≈16–22):** Numeric / structure unlocks via continuous D (not metadata pads).
- **Must not:** Wrong-topic dump; Diff skeleton on non-Diff leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` (default path).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,3].$ | $4$ | Diff(structured_average_rate_of_change) |
| 0 | 207 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,2].$ | $3$ | Diff(structured_average_rate_of_change) |
| 8 | 101 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,5].$ | $6$ | Diff(structured_average_rate_of_change) |
| 8 | 207 | $\text{Find the average rate of change of }f(x)=x^{2} + 3\text{ on }[1,2].$ | $3$ | Diff(structured_average_rate_of_change) |
| 16 | 101 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,5].$ | $6$ | Diff(structured_average_rate_of_change) |
| 16 | 207 | $\text{Find the average rate of change of }f(x)=x^{3}+x\text{ on }[1,2].$ | $8$ | Diff(structured_average_rate_of_change) |
| 22 | 101 | $\text{Find the average rate of change of }f(x)=x^{2}\text{ on }[1,5].$ | $6$ | Diff(structured_average_rate_of_change) |
| 22 | 207 | $\text{Find the average rate of change of }f(x)=x^{3}+x\text{ on }[1,2].$ | $8$ | Diff(structured_average_rate_of_change) |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.4 | https://openstax.org/books/calculus-volume-1/pages/3-4-derivatives-as-rates-of-change | avg rate [a,b] |

Local HTML / mine: `scripts/output/example_mining/calculus-volume-1/stage1/`

## Variety notes

Shapes follow live samples; OpenStax frames win for story variety when applicable.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** current catalog generator `average_rate_of_change`.
- **Not this pass:** gallery stub + Limitations; flesh only if gold locked.
