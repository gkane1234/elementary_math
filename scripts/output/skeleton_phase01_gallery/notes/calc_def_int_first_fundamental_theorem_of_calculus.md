# Notes — `calc_def_int_first_fundamental_theorem_of_calculus` (`First Fundamental Theorem of Calculus`)

- **Display name:** First Fundamental Theorem of Calculus
- **Category:** Calculus — Definite Integration
- **Generator:** `first_fundamental_theorem`
- **Suggested family:** integral (OpenStax FTC Part 2: evaluate \(\int_a^b f=F(b)-F(a)\); catalog name is “first”)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate a definite integral by an antiderivative (FTC Part 2). Not \(\frac{d}{dx}\int_a^{g(x)}\) — that is the second-FTC leaf.
- **D=0:** Old easy mix: \(\int_0^b x\,dx\) leftover and \(\int_0^b kx^{2}\,dx\) (\(k\ge 1\)).
- **Mid D (≈8):** Those leftovers still allowed, plus \(\int_0^b(px^{2}+q)\,dx\).
- **High D (≈16):** Lock out \(\int x\) / \(\int kx^{2}\). Quad-const leftover plus \(\int_0^b\sqrt{x}\,dx\) / \(\int_0^{\pi/2}\sin x\,dx\).
- **Expert (≈22):** \(\sqrt{x}\) and \(\sin x\) only.
- **Must not:** Derivative-of-integral stems; padded `difficulty_costs`; new cores (Ex. 5.20 \(t^{2}-4\) on \([-2,2]\), Ex. 5.21 \(\frac{x-1}{\sqrt{x}}\) on \([1,9]\), start at \(a\neq 0\) except the frozen \(\sin\) limits).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Live path is `calculus_integrals` → `_sample_ftc` (shadowed `calculus.py` `_pick_family` is not live). Accumulating pool, so high D still mixed \(\int x\,dx\). `form_id` was coarse `linear`/`quad`/…; `spec_snapshot.generator` unstamped. 40-seed counts: D=0 `quad` 24 / `linear` 16; D=8 leftover `quad_const` 17 / `quad` 17 / `linear` 6; D=12–22 all five (`linear` 5 / `quad` 5 / `quad_const` 7 / `sin` 11 / `sqrt` 12).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 0 | $\int_{0}^{3} 4x^{2}\,dx$ | $36$ | `quad` |
| 0 | 101 | $\int_{0}^{2} x\,dx$ | $2$ | `linear` |
| 8 | 0 | $\int_{0}^{3} \left(3x^{2} + 2\right)\,dx$ | $33$ | `quad_const` |
| 8 | 207 | $\int_{0}^{4} x\,dx$ | $8$ | linear leftover |
| 16 | 1 | $\int_{0}^{2} x\,dx$ | $2$ | linear leftover at D=16 |
| 16 | 7 | $\int_{0}^{4} \sqrt{x}\,dx$ | $\frac{16}{3}$ | `sqrt` |
| 22 | 1 | $\int_{0}^{2} x\,dx$ | $2$ | linear leftover at expert |
| 22 | 7 | $\int_{0}^{16} \sqrt{x}\,dx$ | $\frac{128}{3}$ | `sqrt` |
| 22 | 101 | $\int_{0}^{2} 3x^{2}\,dx$ | $8$ | `quad` leftover at expert |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same five builders. D=0 stays old linear/quad mix. Gallery seeds 101/207/313 can collide on one form at mid D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int_{0}^{4} x\,dx$ | $8$ | `ftc1_linear` |
| 0 | 0 | $\int_{0}^{3} 6x^{2}\,dx$ | $54$ | `ftc1_quad` |
| 8 | 101 | $\int_{0}^{4} x\,dx$ | $8$ | linear leftover |
| 8 | 2 | $\int_{0}^{3} 5x^{2}\,dx$ | $45$ | `ftc1_quad` leftover |
| 8 | 0 | $\int_{0}^{3} \left(3x^{2} + 2\right)\,dx$ | $33$ | `ftc1_quad_const` |
| 16 | 101 | $\int_{0}^{4} \left(x^{2} - 1\right)\,dx$ | $\frac{52}{3}$ | quad-const leftover (no \(\int x\)) |
| 16 | 2 | $\int_{0}^{9} \sqrt{x}\,dx$ | $18$ | `ftc1_sqrt` |
| 16 | 0 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc1_sin` |
| 22 | 101 | $\int_{0}^{9} \sqrt{x}\,dx$ | $18$ | `ftc1_sqrt` only (sqrt/sin) |
| 22 | 0 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc1_sin` only |

40-seed counts **after**: D=0 `ftc1_quad` 22 / `ftc1_linear` 18; D=8 leftover `ftc1_linear` 15 / `ftc1_quad` 11 / `ftc1_quad_const` 14; D=16 leftover `ftc1_quad_const` 15 + `ftc1_sin` 14 / `ftc1_sqrt` 11 (no linear/quad); D=22 `ftc1_sin` 22 / `ftc1_sqrt` 18.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.3 The Fundamental Theorem of Calculus | https://openstax.org/books/calculus-volume-1/pages/5-3-the-fundamental-theorem-of-calculus | FTC Part 2 (obj. 5.3.4–5.3.5): evaluate \(\int_a^b f=F(b)-F(a)\). Ex. 5.20 \(\int_{-2}^{2}(t^{2}-4)\,dt\); Ex. 5.21 \(\int_1^9\frac{x-1}{\sqrt{x}}\,dx\); Checkpoint 5.19 \(\int_1^2 x^{-4}\,dx\) — old path is frozen \(\int_0^b x / kx^{2} / (px^{2}+q) / \sqrt{x}\) and \(\int_0^{\pi/2}\sin x\), not these |
| OpenStax Calculus Volume 1 §5.3 (Part 1, other leaf) | https://openstax.org/books/calculus-volume-1/pages/5-3-the-fundamental-theorem-of-calculus | \(\frac{d}{dx}\int_a^{g(x)} f\) stays on `calc_def_int_second_fundamental_theorem_of_calculus` (Ex. 5.17–5.19) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-3).

## Variety notes

Not a WP. D=0 rotates old easy \(\int x\) vs \(\int kx^{2}\). Same-D leftover mix at D=8 (those plus \(px^{2}+q\)). High D keeps the old \(\sqrt{x}\) / \(\sin x\) builders (do not invent Ex. 5.20 / 5.21). Five old forms, so D=16 mixes quad-const leftover + sqrt/sin and D=22 is sqrt/sin-only.

## Limitations

- **Status:** shipped — leftover lockout of D=0 \(\int x\) / \(\int kx^{2}\). Remaining `LIMITATIONS`: five frozen old builders (always \(a=0\) except frozen \(\sin\) on \([0,\pi/2]\); no Ex. 5.20 \(t^{2}-4\) on \([-2,2]\), no Ex. 5.21 \(\frac{x-1}{\sqrt{x}}\), no \(x^{-4}\)); D=16 can still emit quad-const leftover (intentional); catalog name “first” is OpenStax Part 2 (evaluate), not Part 1.
- **Live pairwise:** each item stamps `form_id`, `generator=first_fundamental_theorem`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `first_fundamental_theorem`

## Proposed engine (reuse vs new)

- **Reuse:** existing linear / quad / quad-const / sqrt / sin builders in `integrals.py` `_sample_ftc`. Depth = real structure (lock out \(\int x\) / \(\int kx^{2}\); mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** Ex. 5.20 / 5.21 / Checkpoint 5.19; derivative-of-integral (second leaf); start at \(a\neq 0\) on the poly/sqrt builders.
