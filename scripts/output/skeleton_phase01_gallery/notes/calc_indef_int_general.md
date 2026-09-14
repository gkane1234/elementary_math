# Notes — `calc_indef_int_general` (`calc_indef_int_general`)

Mixed-technique indefinite integral leaf, analogous to `calc_diff_general`.
Teacher `allow_*` checkboxes drop catalog forms whose `requires_allows` /
`tricks` are not all on. OpenStax table/power at low D; BC-bank families and
parts/PFD/trig-sub unlock mid/high D.

- **Display name:** General indefinite integrals
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_general`
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Choose and apply an allowed antiderivative technique.
- **D=0:** Old easy leftover is table/power/ln-exp — \(\int\sqrt{x}\), \(\int x^n\), \(\int\sin(kx)\), \(\int\sec\tan\), \(\int 1/x\), \(\int e^x\).
- **Mid D (≈8):** Leftover table/power plus u-sub / parts / PFD / invtrig. Table trig leftover still allowed when the planner picks trig.
- **High D (≈16–22):** No D=0 power leftover; no table trig. Parts / PFD / trig-sub / u-sub / leftover mid-trig / ln-exp / invtrig. D=22 trig is high-catalog only when trig is picked.
- **Must not:** Invent Weierstrass / \(x^4+1\) / three-trick cores; padded `difficulty_costs`; stamp a sub-sampler as the leaf generator.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` **before** leftover lockout. No opt-out (new mixed leaf). Seed 101 at D=8/16/22 stayed on power `rewrite_over_x`. D=0 seed 207 was table \(\int\sec\tan\). Shared `_sample_trig` already dropped table at D≥8 (catalog `d_max=4`); high D could still pick power.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \sqrt{x}\,dx$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | `sqrt_x` leftover |
| 0 | 207 | $\int \sec(x)\tan(x)\,dx$ | $\sec(x)+C$ | table trig leftover |
| 0 | 313 | $\int \sin(6x)\,dx$ | $-\frac{1}{6}\cos(6x)+C$ | table `basic_sin_kx` |
| 8 | 101 | $\int \frac{x^{2}+1\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+3x^{\frac{1}{3}}+C$ | power leftover |
| 8 | 207 | $\int x\cos(3x)\,dx$ | $\frac{1}{3}x\sin(3x)+\frac{1}{9}\cos(3x)+C$ | parts |
| 16 | 101 | $\int \frac{x^{2}+1\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+3x^{\frac{1}{3}}+C$ | power leftover at high D |
| 16 | 207 | $\int \frac{-4x + 4}{\left(x - 2\right)^{2}}\,dx$ | $-4\ln\|x - 2\|+4\frac{1}{x - 2}+C$ | PFD |
| 16 | 313 | $\int \frac{x^{2}}{\sqrt{x^{2}+4}}\,dx$ | $\frac{1}{2}x\sqrt{x^{2}+4}-2\ln\left\|x+\sqrt{x^{2}+4}\right\|+C$ | trig-sub |
| 22 | 101 | $\int \frac{x^{2}+1\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+3x^{\frac{1}{3}}+C$ | same power leftover |

Opt-out flag used: none (this is a new mixed leaf; technique leaves still have old-path flags).

## What live path produces now (real latex)

Leftover lockout of D=0 table trig / power on the existing mixed core. Planner drops power at D≥16. When trig is picked, `general_trig_forms_for_difficulty` keeps table leftover at D=8 and drops table at D≥16 (equal `d_min`/`d_weight` inside the leftover band so catalog `d_max=4` cannot starve table). Stamps `form_id` + `generator=integral_general` on metadata and `spec_snapshot`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \sqrt{x}\,dx$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | `sqrt_x` leftover |
| 0 | 207 | $\int \tan(x)\,dx$ | $-\ln\|\cos(x)\|+C$ | table `basic_tan` |
| 0 | 313 | $\int \sin(6x)\,dx$ | $-\frac{1}{6}\cos(6x)+C$ | table `basic_sin_kx` |
| 8 | 101 | $\int \frac{x^{2}+1\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+3x^{\frac{1}{3}}+C$ | power leftover |
| 8 | 207 | $\int x\cos(3x)\,dx$ | $\frac{1}{3}x\sin(3x)+\frac{1}{9}\cos(3x)+C$ | parts |
| 8 | 313 | $\int \ln(3x)\,dx$ | $x\ln(3x)-x+C$ | parts leftover |
| 16 | 101 | $\int \sin^{3}(x)\cos^{3}(x)\,dx$ | $\frac{1}{4}\sin^{4}(x)-\frac{1}{6}\sin^{6}(x)+C$ | no power leftover |
| 16 | 207 | $\int \frac{-4x + 4}{\left(x - 2\right)^{2}}\,dx$ | $-4\ln\|x - 2\|+4\frac{1}{x - 2}+C$ | PFD |
| 16 | 313 | $\int \frac{x^{2}}{\sqrt{x^{2}+4}}\,dx$ | $\frac{1}{2}x\sqrt{x^{2}+4}-2\ln\left\|x+\sqrt{x^{2}+4}\right\|+C$ | trig-sub |
| 22 | 101 | $\int \frac{\cos(x)}{1+\sin^{2}(x)}\,dx$ | $\arctan(\sin(x))+C$ | high trig; no table |
| 22 | 207 | $\int \frac{-4x + 4}{\left(x - 2\right)^{2}}\,dx$ | $-4\ln\|x - 2\|+4\frac{1}{x - 2}+C$ | PFD |

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1/2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.10 | https://openstax.org/books/calculus-volume-1/pages/4-10-antiderivatives | D=0 power / table \(\int\sin\), \(\int\sec\tan\), \(\int\sqrt{x}\) |
| OpenStax Calculus Volume 1 §5.5 | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | u-sub families |
| OpenStax Calculus Volume 2 §3.1–3.4 | https://openstax.org/books/calculus-volume-2/pages/3-1-integration-by-parts | parts / trig / PFD / trig-sub |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `textbooks/openstax/html/calculus-volume-2/`.

## Variety notes

Not a WP. D=0 one easy mix (table/power/ln-exp). D=8 leftover table + unlocks. High D cannot emit table trig or power rewrite. Toggles: `allow_parts` off → no `cyclic_exp_*` / tabular parts. `allow_pfd` off → no distinct-linear / mixed PFD. `allow_trig` off → no trig catalog or trig u-sub bank families.

## Limitations

- **Status:** leftover lockout of D=0 table trig / power shipped. Remaining `LIMITATIONS`: D=0 majority is still `sqrt_x` / `poly_sum` (table is rare); D=8 can still emit power `rewrite_over_x` leftover; D=16 can still emit leftover mid-trig (`sin_j_cos`, `sec_j_tan`) / `arcsin_basic` / `exp_k`; D=16 and D=22 share the same planner trick band (trig form band splits); reverse-chain u-sub may appear when substitution is on; deferred bank items (`x^4+1`, Weierstrass, `ln(cos x)`) are not invented.
- **Live pairwise:** each item stamps `form_id`, `generator=integral_general`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Trig pick uses `select_form_id` so `live_quality_form_weights` can tilt inside the leftover band.
- **Generator:** `integral_general`

## Proposed engine (reuse vs new)

- **Reuse:** existing `_plan_general_pipeline` + `_sample_trig` / power / ln-exp / parts / PFD / trig-sub cores. Exclusive trick bands + general-only trig leftover bands. No padded `difficulty_costs`.
- **Shipped this pass:** leftover lockout of D=0 table trig / power; `general_tricks_for_difficulty` / `general_trig_forms_for_difficulty`; leaf `generator` stamp on `spec_snapshot`.
- **Not this pass:** inventing Weierstrass / \(x^4+1\) / three-trick cores; a fourth EMH named preset (this leaf has no named form preset).
