# Notes — `calc_def_int_second_fundamental_theorem_of_calculus` (`Second Fundamental Theorem of Calculus`)

- **Display name:** Second Fundamental Theorem of Calculus
- **Category:** Calculus — Definite Integration
- **Generator:** `second_fundamental_theorem`
- **Suggested family:** integral (OpenStax FTC Part 1: \(\frac{d}{dx}\int_a^{g(x)} f=f(g(x))g'(x)\); catalog name is “second”)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate an integral with a variable upper limit (OpenStax FTC Part 1). Not evaluate-\(\int_a^b\) — that is the first-FTC leaf.
- **D=0:** Old easy leftover \(\frac{d}{dx}\int_a^{x} t^{2}\,dt \to x^{2}\) (\(a\in\{0,1,2,3\}\)).
- **Mid D (≈8):** That leftover still allowed, plus \(\frac{d}{dx}\int_a^{x}\sin(t)\,dt \to \sin(x)\).
- **High D (≈16):** Lock out \(t^{2}\). Trig leftover plus chain \(\frac{d}{dx}\int_a^{kx} e^{t}\,dt \to k e^{kx}\) (\(k\ge 2\)).
- **Expert (≈22):** Chain \(g(x)=kx\) only.
- **Must not:** Plain evaluate-\(\int_a^b\) stems; padded `difficulty_costs`; new cores (Ex. 5.17 \(1/(t^{3}+1)\), Ex. 5.18 \(\sqrt{x}\) upper, Ex. 5.19 two variable limits, Checkpoint 5.16 \(\sqrt{x^{2}+4}\)).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Live path is `calculus_integrals` → `_sample_ftc2`. Accumulating pool (`poly`; `+trig` at D≥8; `+chain` at D≥14), so high D still mixed \(t^{2}\). `form_id` was already `ftc2_poly`/`ftc2_trig`/`ftc2_chain`; `spec_snapshot.generator` already copied. 40-seed counts: D=0 `ftc2_poly` 40; D=8 leftover `ftc2_trig` 24 / `ftc2_poly` 16; D=12 same as D=8; D=14–22 all three (`ftc2_chain` 17 / `ftc2_trig` 17 / `ftc2_poly` 6).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 0 | $\frac{d}{dx}\int_{1}^{x} t^{2}\,dt$ | $x^{2}$ | `ftc2_poly` |
| 0 | 101 | $\frac{d}{dx}\int_{0}^{x} t^{2}\,dt$ | $x^{2}$ | `ftc2_poly` |
| 8 | 0 | $\frac{d}{dx}\int_{1}^{x} \sin(t)\,dt$ | $\sin(x)$ | `ftc2_trig` |
| 8 | 101 | $\frac{d}{dx}\int_{0}^{x} t^{2}\,dt$ | $x^{2}$ | poly leftover |
| 16 | 0 | $\frac{d}{dx}\int_{1}^{4x} e^{t}\,dt$ | $4e^{4x}$ | `ftc2_chain` |
| 16 | 101 | $\frac{d}{dx}\int_{0}^{x} t^{2}\,dt$ | $x^{2}$ | poly leftover at D=16 |
| 22 | 0 | $\frac{d}{dx}\int_{1}^{4x} e^{t}\,dt$ | $4e^{4x}$ | `ftc2_chain` |
| 22 | 101 | $\frac{d}{dx}\int_{0}^{x} t^{2}\,dt$ | $x^{2}$ | `ftc2_poly` leftover at expert |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same three builders. D=0 stays old \(t^{2}\). Gallery seeds 101/207/313 can collide on one form at mid D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\frac{d}{dx}\int_{2}^{x} t^{2}\,dt$ | $x^{2}$ | `ftc2_poly` |
| 0 | 0 | $\frac{d}{dx}\int_{1}^{x} t^{2}\,dt$ | $x^{2}$ | `ftc2_poly` |
| 8 | 101 | $\frac{d}{dx}\int_{2}^{x} t^{2}\,dt$ | $x^{2}$ | poly leftover |
| 8 | 0 | $\frac{d}{dx}\int_{1}^{x} \sin(t)\,dt$ | $\sin(x)$ | `ftc2_trig` |
| 16 | 101 | $\frac{d}{dx}\int_{2}^{x} \sin(t)\,dt$ | $\sin(x)$ | trig leftover (no \(t^{2}\)) |
| 16 | 0 | $\frac{d}{dx}\int_{1}^{4x} e^{t}\,dt$ | $4e^{4x}$ | `ftc2_chain` |
| 22 | 101 | $\frac{d}{dx}\int_{2}^{2x} e^{t}\,dt$ | $2e^{2x}$ | `ftc2_chain` only |
| 22 | 0 | $\frac{d}{dx}\int_{1}^{4x} e^{t}\,dt$ | $4e^{4x}$ | `ftc2_chain` only |

40-seed counts **after**: D=0 `ftc2_poly` 40; D=8 leftover `ftc2_trig` 22 / `ftc2_poly` 18; D=16 leftover `ftc2_chain` 22 / `ftc2_trig` 18 (no poly); D=22 `ftc2_chain` 40.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.3 The Fundamental Theorem of Calculus | https://openstax.org/books/calculus-volume-1/pages/5-3-the-fundamental-theorem-of-calculus | FTC Part 1 (obj. 5.3.2–5.3.3): \(\frac{d}{dx}\int_a^{g(x)} f=f(g(x))g'(x)\). Ex. 5.17 \(g(x)=\int_1^x 1/(t^{3}+1)\,dt\); Ex. 5.18 \(\int_1^{\sqrt{x}}\sin t\,dt\); Ex. 5.19 two limits \(\int_x^{2x} t^{3}\,dt\); Checkpoint 5.16 \(\int_0^r\sqrt{x^{2}+4}\,dx\); Checkpoint 5.17 \(\int_1^{x^{3}}\cos t\,dt\) — old path is frozen \(t^{2}\) / \(\sin t\) / \(e^{t}\) with \(g(x)=x\) or \(kx\), not these |
| OpenStax Calculus Volume 1 §5.3 (Part 2, other leaf) | https://openstax.org/books/calculus-volume-1/pages/5-3-the-fundamental-theorem-of-calculus | evaluate \(\int_a^b f=F(b)-F(a)\) stays on `calc_def_int_first_fundamental_theorem_of_calculus` (Ex. 5.20–5.21) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-3).

## Variety notes

Not a WP. D=0 one easy \(t^{2}\) (old). Same-D leftover mix at D=8 (that plus \(\sin t\)). High D keeps the old chain \(g(x)=kx\) builder (do not invent \(\sqrt{x}\) / \(x^{3}\) uppers or two variable limits). Three old forms, so D=16 mixes trig leftover + chain and D=22 is chain-only.

## Limitations

- **Status:** shipped — leftover lockout of D=0 \(t^{2}\). Remaining `LIMITATIONS`: three frozen old builders (always dummy lower \(a\in\{0,1,2,3\}\); integrand frozen \(t^{2}\) / \(\sin t\) / \(e^{t}\); chain upper is only \(kx\), never \(\sqrt{x}\) / \(x^{3}\)); no Ex. 5.17 \(1/(t^{3}+1)\), no Ex. 5.18 \(\sqrt{x}\) upper, no Ex. 5.19 two variable limits; D=16 can still emit trig leftover (intentional); catalog name “second” is OpenStax Part 1 (derivative of integral), not Part 2.
- **Live pairwise:** each item stamps `form_id`, `generator=second_fundamental_theorem`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `second_fundamental_theorem`

## Proposed engine (reuse vs new)

- **Reuse:** existing poly / trig / chain builders in `integrals.py` `_sample_ftc2`. Depth = real structure (lock out \(t^{2}\); mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** Ex. 5.17 / 5.18 / 5.19 / Checkpoints 5.16–5.18; evaluate-\(\int_a^b\) (first leaf).
