# Notes — `calc_app_diff_rolles_theorem` (`Rolle's Theorem`)

- **Display name:** Rolle's Theorem
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `rolles_theorem`
- **Suggested family:** other (find \(c\) with \(f'(c)=0\) when \(f(a)=f(b)\))

---

## What the question should look like (D=0 vs high D)

- **Skill:** Find the Rolle point(s) \(c\) on \([a,b]\) for an explicit \(f\) with \(f(a)=f(b)\).
- **D=0:** Even quadratic \(f(x)=x^{2}-n^{2}\) on \([-n,n]\) (old easy) — \(c=0\).
- **Mid D (≈8):** Even-quad leftover still allowed, plus two-root quadratics \(f=(x-a)(x-b)\) on \([a,b]\) with midpoint \(c\neq 0\) (Ex. 4.14 first: \(x^{2}+2x\) on \([-2,0]\)).
- **High D (≈16):** Lock out the even-quad \(c=0\). Two-root leftover plus odd cubic \(x^{3}-n^{2}x\) on \([-n,n]\) (Ex. 4.14 second; \(c=\pm n/\sqrt{3}\)).
- **Expert (≈22):** Lock out the two-root leftover. Odd cubic only.
- **Must not:** Hypothesis-only true/false with no \(c\); padded `difficulty_costs`; even-quad \(c=0\) at high D; two-root lookalikes whose midpoint is 0 (same leftover).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**. Families accumulated (`_pick_family`), so high D still emitted even-quad \(c=0\) on \([-n,n]\). No `form_id` / `generator` stamp.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{2}-4\text{ on }[-2,2].$ | $0$ | even-quad |
| 0 | 207 | $\text{Find }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{2}-4\text{ on }[-2,2].$ | $0$ | same |
| 8 | 101 | $\text{Find }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{2}-4\text{ on }[-2,2].$ | $0$ | leftover even-quad |
| 8 | 207 | $\text{Find }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{2} + 2x\text{ on }[-2,0].$ | $-1$ | two-root (Ex. 4.14 first) |
| 16 | 101 | $\text{Find }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{2}-4\text{ on }[-2,2].$ | $0$ | even-quad leftover at high D |
| 16 | 207 | $\text{Find }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{2} - 5x\text{ on }[0,5].$ | $\frac{5}{2}$ | two-root |
| 22 | 101 | $\text{Find }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{2}-25\text{ on }[-5,5].$ | $0$ | still even-quad |
| 22 | 207 | $\text{Find }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{2} + 3x\text{ on }[-3,0].$ | $-\frac{3}{2}$ | two-root, not cubic |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the existing even-quad / two-root / odd-cubic core. Two-root sampling rejects \(a+b=0\) so it cannot emit the even-quad leftover.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{2} - 9\text{ on }[-3,3].$ | $0$ | `rolles_even_quad` |
| 8 | 7 | $\text{Find }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{2} - 9\text{ on }[-3,3].$ | $0$ | even-quad leftover |
| 8 | 101 | $\text{Find }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{2} + 2x - 3\text{ on }[-3,1].$ | $-1$ | `rolles_two_roots` |
| 16 | 7 | $\text{Find }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{2} + x - 6\text{ on }[-3,2].$ | $-\frac{1}{2}$ | two-root leftover |
| 16 | 101 | $\text{Find all }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{3} - 4x\text{ on }[-2,2].$ | $c=\pm\frac{2}{\sqrt{3}}$ | `rolles_cubic_odd` (Ex. 4.14) |
| 22 | 101 | $\text{Find all }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{3} - 4x\text{ on }[-2,2].$ | $c=\pm\frac{2}{\sqrt{3}}$ | cubic only |
| 22 | 207 | $\text{Find all }c\text{ guaranteed by Rolle's Theorem for }f(x)=x^{3} - 16x\text{ on }[-4,4].$ | $c=\pm\frac{4}{\sqrt{3}}$ | \(c=\pm n/\sqrt{3}\) |

40-seed counts **after**: D=0 even-quad-only; D=8 even-quad/two-root; D=16 two-root leftover + cubic (0/40 with \(c=0\)); D=22 cubic only (0/40 with \(c=0\)).

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.4 | https://openstax.org/books/calculus-volume-1/pages/4-4-the-mean-value-theorem | Ex. 4.14 \(x^{2}+2x\) on \([-2,0]\) and \(x^{3}-4x\) on \([-2,2]\); find \(c\) with \(f'(c)=0\) |
| Checkpoint 4.14 | same | scaled \(2x^{2}-8x+6\) on \([1,3]\) — not on the monic two-root core |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/4-4-the-mean-value-theorem.md`.

## Variety notes

Not a WP. D=0 one easy even-quad. Same-D rotation at mid D: even-quad leftover vs two-root (midpoint \(c\neq 0\)). High D odd cubic already on the old core (Ex. 4.14 second). Algebra stays closed-form (\(c=0\), midpoint, \(\pm n/\sqrt{3}\)).

## Limitations

- **Status:** shipped — leftover lockout of even-quad \(c=0\). Remaining `LIMITATIONS`: no scaled Checkpoint 4.14 quadratic (\(2x^{2}-8x+6\)); no trig/exp Rolle; no hypothesis-verify stem (old path is find-\(c\) only); D=16 can still emit the two-root leftover (intentional).
- **Live pairwise:** each item stamps `form_id`, shared `generator=rolles_theorem`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `rolles_theorem`

## Proposed engine (reuse vs new)

- **Reuse:** existing Rolle closed forms (even-quad + two-root + odd cubic) moved onto the calc_app_diff constructive core. Depth = real structure (lock out even-quad \(c=0\); keep Ex. 4.14 cubic) — not padded `difficulty_costs`.
- **Not this pass:** scaled Checkpoint 4.14; hypothesis-only true/false.
