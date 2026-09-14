# Notes — `calc_app_diff_linear_approximations` (`Linear approximations`)

- **Display name:** Linear approximations
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `linear_approximation`
- **Suggested family:** other (write \(L(x)=f(a)+f'(a)(x-a)\); not differentials \(dy\), not a WP)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Find the linearization \(L(x)\) of \(f\) at a point, or (mid D leftover) use \(L\) of \(x^{2}\) to estimate \(f(a+h)\).
- **D=0:** Easy leftover mix: \(f(x)=x^{2}\) or \(f(x)=\sqrt{x}\) at a nice \(a\) (old easy; OpenStax Ex. 4.5 is \(\sqrt{x}\) at a perfect square).
- **Mid D (≈8):** Easy leftover still allowed, plus estimate-\(x^{2}\), \(1/x\), and \(e^{x}\) at \(0\).
- **High D (≈16):** Lock out \(x^{2}\) leftovers (formula and estimate). \(\sqrt{x}\) leftover plus \(1/x\) and \(e^{x}\).
- **Expert (≈22):** Reciprocal and exp only (no \(\sqrt{x}\) leftover, no \(x^{2}\)).
- **Must not:** Differentials \(dy=f'(x)\,dx\) (other leaf); OpenStax sin / \((1+x)^{n}\) / cube-root invented cores; padded `difficulty_costs`; figure of \(y\) vs \(L(x)\).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Accumulating unlocks: D=0 always \(\sqrt{x}\) / \(x^{2}\) formula; D=8 same plus \(x^{2}\) estimate (\(h\in\{1/10,1/5,1/2\}\)); D≥10 added \(1/x\) and \(e^{x}\) at \(0\) **without locking \(x^{2}\) leftovers**. D=16 and D=22 were the same four-family pool. `form_id` unstamped; top-level `generator` unstamped (only inside `spec_snapshot`). 40-seed counts: D=0 sqrt 19 / quad 21; D=8 sqrt 20 / quad formula 13 / quad estimate 7; D=16 and D=22 identical (exp 10, quad formula 6, reciprocal 10, sqrt 8, quad estimate 6).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=4.$ | $L(x)=2+\frac{1}{4}(x-4)$ | `sqrt` leftover |
| 0 | 207 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $L(x)=4+4(x-2)$ | `quad` leftover |
| 8 | 101 | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=4.$ | $L(x)=2+\frac{1}{4}(x-4)$ | sqrt leftover |
| 8 | 207 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $L(x)=4+4(x-2)$ | quad leftover |
| 16 | 101 | $\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=5.$ | $L(x)=\frac{1}{5}-\frac{1}{25}(x-5)$ | `reciprocal` unlock |
| 16 | 207 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $L(x)=4+4(x-2)$ | \(x^{2}\) leftover at high D |
| 22 | 101 | $\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=5.$ | $L(x)=\frac{1}{5}-\frac{1}{25}(x-5)$ | D=22 == D=16 pool |
| 22 | 207 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $L(x)=4+4(x-2)$ | \(x^{2}\) leftover at expert |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same four family builders (estimate split out as `quad_estimate` for pairwise stamps). D=0 stays the old \(\sqrt{x}\) / \(x^{2}\) mix. Gallery seeds 101/207/313 can collide on one form at a band; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=1.$ | $L(x)=1+\frac{1}{2}(x-1)$ | `sqrt` |
| 0 | 1 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=1.$ | $L(x)=1+2(x-1)$ | `quad` leftover |
| 8 | 101 | $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=2\text{ to estimate }f(\frac{5}{2}).$ | $6$ | `quad_estimate` leftover |
| 8 | 0 | $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$ | $L(x)=1+x$ | `exp` unlock |
| 8 | 1 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=1.$ | $L(x)=1+2(x-1)$ | quad leftover |
| 16 | 101 | $\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=3.$ | $L(x)=\frac{1}{3}-\frac{1}{9}(x-3)$ | `reciprocal`; no \(x^{2}\) |
| 16 | 1 | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=1.$ | $L(x)=1+\frac{1}{2}(x-1)$ | sqrt leftover (intentional) |
| 22 | 101 | $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$ | $L(x)=1+x$ | `exp` only + reciprocal |
| 22 | 1 | $\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=2.$ | $L(x)=\frac{1}{2}-\frac{1}{4}(x-2)$ | no \(\sqrt{x}\) leftover |

40-seed counts **after**: D=0 sqrt 21 / quad 19; D=8 leftover easy + estimate 10 / reciprocal 8 / exp 6; D=16 sqrt 14 / reciprocal 15 / exp 11 (no quad); D=22 exp 21 / reciprocal 19 only.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.2 | https://openstax.org/books/calculus-volume-1/pages/4-2-linear-approximations-and-differentials | \(L(x)=f(a)+f'(a)(x-a)\). Ex. 4.5: linearize \(\sqrt{x}\) at a perfect square and estimate a nearby root (old path has the \(L(x)\) stem, not the estimate). Ex. 4.6: linearize \(\sin x\) at \(\pi/3\) and estimate a degree argument — not in old path (LIMITATIONS). |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/4-2-linear-approximations-and-differentials.md`.

## Variety notes

Not a WP. Algebra/technique shapes follow old path (\(x^{2}\), \(\sqrt{x}\) at \(\{1,4,9\}\), \(1/x\) at \(a\in\{2,\ldots,5\}\), \(e^{x}\) at \(0\), estimate only on leftover \(x^{2}\)). Do not invent sin / cube-root / \((1+x)^{n}\) cores this pass.

## Limitations

**Status:** shipped — leftover lockout of D=0 \(x^{2}\) (formula + estimate). Remaining `LIMITATIONS`: no Ex. 4.5 estimate-\(\sqrt{x}\) (old estimate was \(x^{2}\) only); no Ex. 4.6 \(\sin x\) at \(\pi/3\) / degree conversion; no Checkpoint 4.5 cube root; no Ex. 4.7 \((1+x)^{n}\) at \(0\); D=16 can still emit \(\sqrt{x}\) leftover (intentional); D=22 \(e^{x}\) is frozen at \(a=0\); no diagram of \(y\) vs \(L(x)\).

## Proposed engine (reuse vs new)

- **Reuse:** existing four family builders (now in `calc_app_diff.py`; estimate is `quad_estimate` for `select_form_id` / `live_quality_form_weights`). Depth = real structure (lock out \(x^{2}\); mix leftover at D=8 / D=16; D=22 reciprocal/exp only) — not padded `difficulty_costs`.
- **New:** not this pass. Sin / cube-root / binomial linearizations stay LIMITATIONS until an honest extra builder is wanted.
- **Stamps:** `form_id` + `generator=linear_approximation`.
