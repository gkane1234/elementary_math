# Notes — `calc_app_diff_newtons_method` (`Newton's Method`)

- **Display name:** Newton's Method
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `newtons_method`
- **Suggested family:** other (constructive Newton iterates on \(x^{2}-a\) / \(x^{3}-a\))

---

## What the question should look like (D=0 vs high D)

- **Skill:** Perform one or more Newton iterations \(x_{n+1}=x_n-f(x_n)/f'(x_n)\) and report the next \(x\).
- **D=0:** One step on \(f(x)=x^{2}-a\) from \(x_0\in\{1,2\}\) (old easy; OpenStax square-root shape).
- **Mid D (≈8):** One-quad leftover still allowed, plus one cubic step on \(f(x)=x^{3}-a\).
- **High D (≈16):** Lock out \(x^{2}-a\). One-cubic leftover plus two cubic steps.
- **Expert (≈22):** Lock out all one-step leftovers. Two cubic steps only.
- **Must not:** Generic \(\frac{d}{dx}\) dump; padded `difficulty_costs`; Ex. 4.46 \(x^{3}-3x+1\) five-iterate stems this pass; failure-of-Newton (Ex. 4.48); two-step quadratic as a new form.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Cliff at D=10 (one cubic) then D=16 (two cubic). D=8 was **identical** to D=0 (`newton_one_quad` only). `generator` was unstamped on the `_framework` wrapper. No `spec_snapshot`. 40-seed counts: D=0/8 all one-quad; D=10/12 all one-cubic; D=16/22 all two-cubic.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Use one Newton step for }f(x)=x^{2}-3\text{ from }x_0=2.$ | $x_1=\frac{7}{4}$ | `newton_one_quad` |
| 0 | 207 | $\text{Use one Newton step for }f(x)=x^{2}-3\text{ from }x_0=1.$ | $x_1=2$ | same quadratic |
| 8 | 101 | $\text{Use one Newton step for }f(x)=x^{2}-3\text{ from }x_0=2.$ | $x_1=\frac{7}{4}$ | D=8 == D=0 leftover |
| 8 | 207 | $\text{Use one Newton step for }f(x)=x^{2}-3\text{ from }x_0=1.$ | $x_1=2$ | still \(x^{2}-a\) |
| 16 | 101 | $\text{Use two Newton steps for }f(x)=x^{3}-10\text{ from }x_0=1.$ | $x_2=\frac{23}{8}$ | `newton_two_cubic` |
| 22 | 101 | $\text{Use two Newton steps for }f(x)=x^{3}-10\text{ from }x_0=1.$ | $x_2=\frac{23}{8}$ | same as D=16 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same \(x^{2}-a\) / \(x^{3}-a\) core. D=0 stays old one-quad. Gallery seeds 101/207/313 can collide on one form; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Use one Newton step for }f(x)=x^{2}-3\text{ from }x_0=2.$ | $x_1=\frac{7}{4}$ | `newton_one_quad` |
| 0 | 207 | $\text{Use one Newton step for }f(x)=x^{2}-3\text{ from }x_0=1.$ | $x_1=2$ | old easy quadratic |
| 8 | 1 | $\text{Use one Newton step for }f(x)=x^{2}-2\text{ from }x_0=2.$ | $x_1=\frac{3}{2}$ | one-quad leftover |
| 8 | 101 | $\text{Use one Newton step for }f(x)=x^{3}-3\text{ from }x_0=2.$ | $x_1=\frac{19}{12}$ | one cubic |
| 16 | 1 | $\text{Use one Newton step for }f(x)=x^{3}-2\text{ from }x_0=2.$ | $x_1=\frac{3}{2}$ | one-cubic leftover |
| 16 | 101 | $\text{Use two Newton steps for }f(x)=x^{3}-3\text{ from }x_0=2.$ | $x_2=\frac{9451}{6498}$ | two cubic |
| 22 | 0 | $\text{Use two Newton steps for }f(x)=x^{3}-7\text{ from }x_0=1.$ | $x_2=\frac{61}{27}$ | two cubic |
| 22 | 101 | $\text{Use two Newton steps for }f(x)=x^{3}-3\text{ from }x_0=2.$ | $x_2=\frac{9451}{6498}$ | two cubic only |
| 22 | 207 | $\text{Use two Newton steps for }f(x)=x^{3}-10\text{ from }x_0=1.$ | $x_2=\frac{23}{8}$ | two cubic |

40-seed counts **after**: D=0 one-quad only; D=8 one-quad leftover + one-cubic; D=16 one-cubic leftover + two-cubic (no quad); D=22 two-cubic only.

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.9 Example 4.47 / Checkpoint 4.46 | https://openstax.org/books/calculus-volume-1/pages/4-9-newtons-method | Square-root via \(f(x)=x^{2}-a\); D=0 is one iterate (old easy), not the five-iterate stem |
| OpenStax Calculus Volume 1 §4.9 Example 4.46 | same | Cubic \(x^{3}-3x+1\) with many iterates — **not this pass** (messy rationals; leave on LIMITATIONS) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/4-9-newtons-method.md`.

## Variety notes

Not a WP. D=0 one easy one-quad (old). Same-D rotation at mid D: leftover \(x^{2}-a\) vs one cubic step. High D cubics keep integer \(a\in\{2,3,5,7,10\}\) and \(x_0\in\{1,2\}\) from the old builder.

## Limitations

- **Status:** shipped — leftover lockout of one-quad. Remaining `LIMITATIONS`: no Ex. 4.46 \(x^{3}-3x+1\) (five iterates); no failure-of-Newton (Ex. 4.48 \(x^{3}-2x+2\)); no two-step quadratic (Checkpoint 4.46 asks \(x_1\) and \(x_2\)); no trig/exp Newton; D=16 can still emit one-cubic leftover (intentional).
- **Live pairwise:** each item stamps `form_id`, shared `generator=newtons_method`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `newtons_method`

## Proposed engine (reuse vs new)

- **Reuse:** existing one-quad / one-cubic / two-cubic builders in `calc_app_diff.py`. Depth = real structure (lock out \(x^{2}-a\); unlock two cubic steps) — not padded `difficulty_costs`.
- **Not this pass:** Ex. 4.46 shifted cubic; failure cases; two-step quadratic; figure for the tangent-line picture.
