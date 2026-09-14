# Notes — `calc_indef_int_trigonometric`

- **Display name:** Trigonometric
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_trigonometric`
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Indefinite trigonometric antiderivative \(+C\) (OpenStax Vol. 1 table + Vol. 2 §3.2).
- **D=0:** Old easy leftover table \(\int\sin(kx)\), \(\int\cos(kx)\), \(\int\sec^{2}(kx)\), \(\int\sec x\tan x\).
- **Mid D (≈8):** That table is already locked by catalog `d_max`. Leftover easy u-sub \(\int\cos^{j}x\sin x\) / \(\int\sin^{j}x\cos x\), plus odd/even powers, \(\int\tan^{2}x\), \(\int\sec^{j}x\tan x\), \(\int\tan^{k}x\sec^{2}x\).
- **High D (≈16):** Lock out `cos_j_sin` / `sin_j_cos`. Mid leftover plus product-to-sum, both-even/odd, BC-bank closed forms, tan/sec mixed parity, \(\int\tan^{4}x\).
- **Expert (≈22):** High catalog only (no D=8 leftover).
- **Must not:** Weierstrass / \(\csc^{5}\) / \(\tan^{4}\sec^{3}\) (deferred, no closed template); trig-sub radicals (sibling leaf); padded `difficulty_costs`; new cores.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Live path is `calculus_integrals` → `_sample_trig` on `trig_integrals`. Catalog `d_min`/`d_max` already kept D=0 as table and locked table at D≥8; from D≥16 the accumulating pool was the same as D=22 (including leftover `cos_j_sin`). `form_id` / `generator=integral_trigonometric` already stamped on metadata and `spec_snapshot`. 40-seed counts: D=0 table 40 (`basic_sec_tan` 14 / `basic_sin_kx` 11 / `basic_sec2` 8 / `basic_cos_kx` 7); D=8 leftover mix (`tan_k_sec2` 7 / `sin_j_cos` 7 / `sin_odd_cos_any` 6 / `sin_even_power` 6 / `tan2` 4 / `sec_j_tan` 3 / `cos_even_power` 3 / `cos_odd_sin_any` 2 / `cos_j_sin` 2); D=16/22 identical (`sin_cos_both_odd` 6 / `cos_odd_sin_any` 5 / `tan_sec_sec_even` 4 / … / `cos_j_sin` 1 / `sin_j_cos` 1).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \sin(3x)\,dx$ | $-\frac{1}{3}\cos(3x)+C$ | `basic_sin_kx` |
| 0 | 207 | $\int \sec(x)\tan(x)\,dx$ | $\sec(x)+C$ | `basic_sec_tan` |
| 8 | 101 | $\int \cos^{2}(x)\sin(x)\,dx$ | $-\frac{1}{3}\cos^{3}(x)+C$ | `cos_j_sin` leftover |
| 8 | 207 | $\int \tan^{4}(x)\sec^{2}(x)\,dx$ | $\frac{1}{5}\tan^{5}(x)+C$ | `tan_k_sec2` |
| 16 | 101 | $\int \cos^{2}(x)\sin(x)\,dx$ | $-\frac{1}{3}\cos^{3}(x)+C$ | `cos_j_sin` leftover at D=16 |
| 16 | 207 | $\int \csc^{3}(x)\cot(x)\,dx$ | $-\frac{1}{3}\csc^{3}(x)+C$ | BC bank `csc_j_cot` leftover at D=16 |
| 22 | 101 | $\int \cos^{2}(x)\sin(x)\,dx$ | $-\frac{1}{3}\cos^{3}(x)+C$ | `cos_j_sin` leftover at expert |
| 22 | 207 | $\int \csc^{3}(x)\cot(x)\,dx$ | $-\frac{1}{3}\csc^{3}(x)+C$ | `csc_j_cot`; same pool as D=16 |

Opt-out flag used: _(none — live generator is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same implemented builders. D=0 is table \(\int\sin/\cos/\sec^{2}/\sec\tan\). Gallery seeds 101/207 can collide on one form at mid D; rotation is across seeds. Catalog `d_min` still unlocks within each exclusive band; `select_form_id` keeps catalog D-weights among the band (quality tilt via `live_quality_form_weights`). Parts-gated `sec3_reduction` / `sec_odd_reduction_n5` stay out unless `allow_parts`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \sin(3x)\,dx$ | $-\frac{1}{3}\cos(3x)+C$ | `basic_sin_kx` |
| 0 | 207 | $\int \sec(x)\tan(x)\,dx$ | $\sec(x)+C$ | `basic_sec_tan` |
| 8 | 101 | $\int \cos^{2}(x)\sin(x)\,dx$ | $-\frac{1}{3}\cos^{3}(x)+C$ | `cos_j_sin` leftover |
| 8 | 207 | $\int \tan^{4}(x)\sec^{2}(x)\,dx$ | $\frac{1}{5}\tan^{5}(x)+C$ | `tan_k_sec2` |
| 16 | 101 | $\int \cos^{2}(x)\sin^{3}(x)\,dx$ | $-\frac{1}{3}\cos^{3}(x)+\frac{1}{5}\cos^{5}(x)+C$ | `sin_odd_cos_any` leftover (no `cos_j_sin`) |
| 16 | 207 | $\int \frac{\sin(x)}{1+\cos^{2}(x)}\,dx$ | $-\arctan(\cos(x))+C$ | BC bank `sin_over_one_plus_cos2` |
| 22 | 101 | $\int \sin^{2}(x)\cos^{2}(x)\,dx$ | $\frac{x}{8}-\frac{1}{32}\sin(4x)+C$ | `sin_cos_both_even` only vs high catalog |
| 22 | 207 | $\int \frac{1}{1+\cos(x)}\,dx$ | $\tan\left(\frac{x}{2}\right)+C$ | `one_over_one_plus_cos` |

40-seed counts **after**: D=0 table 40 (`basic_sec_tan` 14 / `basic_sin_kx` 11 / `basic_sec2` 8 / `basic_cos_kx` 7); D=8 leftover mix (same nine as old); D=16 `sin_cos_both_odd` 6 / `sin_even_power` 5 / `tan_sec_sec_even` 5 / … (no `cos_j_sin` / `sin_j_cos`); D=22 high only (`product_sin_a_cos_b` 7 / `tan_even_reduction` 7 / `sin_over_one_plus_cos2` 6 / `tan_sec_sec_even` 4 / `csc_j_cot` 4 / …).

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.4 | https://openstax.org/books/calculus-volume-1/pages/5-4-integration-formulas-and-the-net-change-theorem | Table \(\int\sin\), \(\int\cos\), \(\int\sec^{2}\), \(\int\sec\tan\). D=0 stays these antiderivatives. |
| OpenStax Calculus Volume 2 §3.2 | https://openstax.org/books/calculus-volume-2/pages/3-2-trigonometric-integrals | Ex. 3.8 \(\int\cos^{j}x\sin x\) is `cos_j_sin` (D=8 leftover). Ex. 3.9 odd-sin save-one; even-power reduction; product-to-sum; tan/sec even/odd; \(\int\sec^{3}\) / \(\int\tan^{4}\) reduction. BC bank closed forms (`csc^{j}\cot\), \(\sin/(1+\cos^{2})\), \(1/(1+\cos)\)) reuse those strategies. |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-2/stage1/` (3-2).

## Variety notes

Not a WP. D=0 table (old). Same-D leftover mix at D=8 (easy u-sub + odd/even + tan/sec). High D keeps the old §3.2 / bank builders (do not invent Weierstrass or \(\csc^{5}\)). Many old forms, so D=16 mixes mid leftover + high and D=22 is high only.

## Limitations

- **Status:** shipped — leftover lockout of D=0 table and of D=8 `cos_j_sin` / `sin_j_cos`. Remaining `LIMITATIONS`: frozen implemented catalog builders (table sin/cos/sec²/sec·tan; easy u-sub \(\cos^{j}\sin\) / \(\sin^{j}\cos\); odd/even powers; \(\tan^{2}\); \(\sec^{j}\tan\) / \(\tan^{k}\sec^{2}\); product-to-sum; both-even/odd; BC-bank `csc^{j}\cot` / \(\sin/(1+\cos^{2})\) / \(1/(1+\sin)\) / \(1/(1+\cos)\); tan/sec mixed parity; \(\int\tan^{4}\)); deferred Weierstrass `1/(a+\sin)`, `csc^5` reduction, `tan^4 sec^3`; `sec^3` / `sec^5` need `allow_parts` (off on this leaf); trig-sub stays on the sibling; D=16 can still emit `sin_even_power` / `tan_k_sec2` leftover (intentional).
- **Live pairwise:** each item stamps `form_id`, `generator=integral_trigonometric`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `integral_trigonometric`

## Proposed engine (reuse vs new)

- **Reuse:** existing `_sample_trig` builders in `integrals.py` + `trig_integrals.json`. Depth = leftover lockout of table / `cos_j_sin`, not a new Weierstrass / reduction core.
- **Not this pass:** Weierstrass; \(\csc^{5}\); \(\tan^{4}\sec^{3}\); parts-gated \(\sec^{3}\) on this leaf; trig-sub sibling.
