# Notes — `calc_app_diff_slope_tangent_and_normal_lines` (`Slope, tangent, and normal lines`)

- **Display name:** Slope, tangent, and normal lines
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `tangent_normal_line`
- **Suggested family:** other (point-slope tangent / normal from \(f'(a)\); not linearization \(L(x)\), not a WP)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Find the tangent line (and, from mid D, sometimes the normal) to \(y=f(x)\) at a given \(x=a\).
- **D=0:** Easy leftover mix: \(x^n\), quadratic, \(\sin x/\cos x\) at \(0\), \(e^{kx}\) at \(0\), \(\ln x/\ln(x^{2})/\ln(2x)\) (old easy; OpenStax Ex. 3.1 is \(x^{2}\)). Always tangent.
- **Mid D (≈8):** Easy leftover still allowed, plus \(1/x\) (Ex. 3.3) and \(\sqrt{ax+b}\) (Checkpoint 3.1). Normals begin.
- **High D (≈16):** Lock out D=0 poly/trig/exp/ln leftovers. Reciprocal/radical leftover plus cubic \(Ax^{3}+Bx\), \((x+p)/(x+q)\), \(\sin(kx)/\cos(kx)/\sin(x^{2})\).
- **Expert (≈22):** Cubic and nested only (no reciprocal/radical leftover, no D=0 mix).
- **Must not:** Linearization \(L(x)\) (other leaf); implicit/folium normals; padded `difficulty_costs`; a new figure bank of the actual \(f\) (generic `function_sketch` overlay is pre-existing, not a match-the-graph leaf).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Accumulating unlocks: D=0 always poly_mono / poly_quad / trig / exp / ln; D=8 added reciprocal/radical; D≥10 added poly_cubic and (D≥14) nested **without locking easy leftovers**. D=16 and D=22 were the same 10-family pool. `form_id` unstamped; top-level `generator` unstamped (only `structure_id=tangent_normal_line:<family>`). 40-seed counts: D=0 exp 8 / poly_quad 11 / poly_mono 6 / ln 10 / trig 5; D=8 same plus reciprocal 4 / radical 4; D=16 and D=22 identical (exp 4, reciprocal 5, poly_mono 3, radical 6, trig_chain 5, poly_cubic 3, ln 4, trig 2, poly_quad 3, rational_linear 5).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the tangent line to }y=\ln(2x)\text{ at }x=1.$ | $y-\ln(2)=1\left(x-1\right)$ | `ln` leftover |
| 0 | 2 | $\text{Find the tangent line to }y=x^{2}\text{ at }x=1.$ | $y-1=2\left(x-1\right)$ | `poly_mono`; OpenStax Ex. 3.1 |
| 0 | 7 | $\text{Find the tangent line to }y=\sin(x)\text{ at }x=0.$ | $y-0=1\left(x-0\right)$ | `trig` |
| 8 | 7 | $\text{Find the normal line to }y=x^{-1}\text{ at }x=2.$ | $y-\frac{1}{2}=4\left(x-2\right)$ | `reciprocal` unlock; Ex. 3.3 |
| 8 | 11 | $\text{Find the tangent line to }y=\sqrt{9x + 12}\text{ at }x=0.$ | $y-3=\frac{3}{2}\left(x-0\right)$ | `radical` |
| 16 | 2 | $\text{Find the normal line to }y=x^{2}\text{ at }x=1.$ | $y-1=-\frac{1}{2}\left(x-1\right)$ | poly_mono leftover at high D |
| 16 | 207 | $\text{Find the tangent line to }y=\frac{x+3}{x+2}\text{ at }x=0.$ | $y-\frac{3}{2}=-\frac{1}{4}\left(x-0\right)$ | `rational_linear` nested |
| 22 | 2 | $\text{Find the normal line to }y=x^{2}\text{ at }x=1.$ | $y-1=-\frac{1}{2}\left(x-1\right)$ | \(x^{2}\) leftover at expert |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same ten family builders. D=0 stays the old five-family easy mix (always tangent). Gallery seeds 101/207/313 can collide on one form at a band; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the tangent line to }y=\sin(x)\text{ at }x=0.$ | $y-0=1\left(x-0\right)$ | `trig` |
| 0 | 1 | $\text{Find the tangent line to }y=x^{2}\text{ at }x=3.$ | $y-9=6\left(x-3\right)$ | `poly_mono`; Ex. 3.1 |
| 0 | 0 | $\text{Find the tangent line to }y=\ln(x)\text{ at }x=2.$ | $y-\ln(2)=\frac{1}{2}\left(x-2\right)$ | `ln` leftover |
| 8 | 0 | $\text{Find the tangent line to }y=\frac{1}{x}\text{ at }x=4.$ | $y-\frac{1}{4}=-\frac{1}{16}\left(x-4\right)$ | `reciprocal`; Ex. 3.3 |
| 8 | 2 | $\text{Find the tangent line to }y=\sqrt{1x}\text{ at }x=1.$ | $y-1=\frac{1}{2}\left(x-1\right)$ | `radical` leftover display |
| 8 | 7 | $\text{Find the normal line to }y=\sin(x)\text{ at }x=0.$ | $y-0=-1\left(x-0\right)$ | normal overlay |
| 16 | 1 | $\text{Find the normal line to }y=\frac{1}{x}\text{ at }x=3.$ | $y-\frac{1}{3}=9\left(x-3\right)$ | reciprocal leftover (no \(x^{2}\)/ln) |
| 16 | 101 | $\text{Find the normal line to }y=2x^{3} + x\text{ at }x=1.$ | $y-3=-\frac{1}{7}\left(x-1\right)$ | `poly_cubic` |
| 22 | 207 | $\text{Find the tangent line to }y=\frac{x+3}{x+2}\text{ at }x=0.$ | $y-\frac{3}{2}=-\frac{1}{4}\left(x-0\right)$ | `rational_linear` nested only |
| 22 | 1 | $\text{Find the normal line to }y=-3x + 2x^{3}\text{ at }x=2.$ | $y-10=-\frac{1}{21}\left(x-2\right)$ | `poly_cubic`; no radical leftover |

40-seed counts **after**: D=0 ln 6 / poly_mono 7 / poly_quad 9 / exp 8 / trig 10; D=8 leftover easy + reciprocal 3 / radical 5; D=16 trig_chain 6 / reciprocal 7 / radical 9 / rational_linear 8 / poly_cubic 10 (no poly/trig/exp/ln); D=22 trig_chain 11 / poly_cubic 14 / rational_linear 15 only.

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.1 Example 3.1 | https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative | Tangent to \(f(x)=x^{2}\) at \(x=3\) — old D=0 `poly_mono`. |
| Same §3.1 Example 3.3 | same | Tangent to \(f(x)=1/x\) at \(x=2\) — old mid `reciprocal` (also \(x^{-1}\) display). |
| Same §3.1 Checkpoint 3.1 | same | Slope of tangent to \(\sqrt{x}\) at \(x=4\) — old mid `radical` is \(\sqrt{ax+b}\) at a perfect-square inside (full line, not slope-only). |
| §3.6 / §3.8 / §3.9 exercises | https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule | Normal line as an exercise (e.g. \(\sin^{2}(\pi\theta)\), folium, \(x\cdot 5^{x}\)) — **not this pass**. |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/3-1-defining-the-derivative.md`.

## Variety notes

Not a WP. Same-D rotation at D=0: power vs quad vs trig vs exp vs ln (old mix — do not shrink D=0). Mid D adds reciprocal/radical. High D keeps old cubic / nested builders — do not invent implicit-folium or \(\pi/6\) trig cores. Normal vs tangent is a D-gated overlay on the same families (D=0 always tangent), not a new core.

## Limitations

- **Status:** shipped — leftover lockout of D=0 poly/trig/exp/ln. Remaining `LIMITATIONS`: no OpenStax implicit/folium normal; no \(x\cdot 5^{x}\) normal; trig evaluation frozen at \(0\) (no \(\pi/6\)); `rational_linear` never asks for a normal (old builder); D=16 can still emit reciprocal/radical leftover (intentional); radical can render \(\sqrt{1x}\); attached SVG is a generic `function_sketch`, not the computed tangent of the given \(f\).
- **Live pairwise:** each item stamps `form_id`, shared `generator=tangent_normal_line`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `tangent_normal_line`

## Proposed engine (reuse vs new)

- **Reuse:** existing ten family builders (now in `calc_app_diff.py`). Depth = real structure (lock out easy poly/trig/exp/ln; mix leftover at D=8 / D=16; D=22 cubic/nested only) — not padded `difficulty_costs`.
- **Not this pass:** implicit normals; true tangent overlay of the sampled \(f\); \(\pi/6\) trig points; linearization (other leaf).
- **Stamps:** `form_id` + `generator=tangent_normal_line`.
