# Notes — `calc_indef_int_inverse_trigonometric`

- **Display name:** Inverse trigonometric
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_inverse_trig`
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Indefinite inverse-trig antiderivative \(+C\) (OpenStax §5.7 table).
- **D=0:** Old easy leftover \(\int 1/(1+x^{2})\,dx\).
- **Mid D (≈8):** That leftover still allowed, plus \(\int 1/(a^{2}+x^{2})\), \(\int 1/\sqrt{1-x^{2}}\), \(\int 1/\sqrt{a^{2}-x^{2}}\), and scaled \(a^{2}+b^{2}x^{2}\) / \(a^{2}-b^{2}x^{2}\).
- **High D (≈16):** Lock out `arctan_basic`. Mid leftover plus scaled.
- **Expert (≈22):** `arctan_scaled` and `arcsin_scaled` only.
- **Must not:** u-sub chains (those stay on the substitution sibling); definite Ex. 5.49; padded `difficulty_costs`; new cores (arcsec, \(\int 1/(x\sqrt{x^{2}-a^{2}})\)).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Live path is `calculus_integrals` → `_sample_invtrig` on `invtrig_integrals`. Catalog `d_min` already kept D=0 as `arctan_basic` only; from D≥8 the accumulating pool was all six forms, so D=16 and D=22 were the same mix as D=8 (including leftover `arctan_basic`). `form_id` / `generator=integral_inverse_trig` already stamped on metadata and `spec_snapshot`. 40-seed counts: D=0 `arctan_basic` 40; D=8 leftover mix (`arctan_a2` 10 / `arcsin_basic` 8 / `arcsin_a2` 7 / `arcsin_scaled` 7 / `arctan_basic` 5 / `arctan_scaled` 3); D=16/22 identical (`arcsin_scaled` 10 / `arctan_a2` 9 / `arcsin_basic` 7 / `arcsin_a2` 5 / `arctan_scaled` 5 / `arctan_basic` 4).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | `arctan_basic` |
| 0 | 207 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | `arctan_basic` |
| 8 | 101 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | `arctan_basic` leftover |
| 8 | 207 | $\int \frac{1}{\sqrt{16-4x^{2}}}\,dx$ | $\frac{1}{2}\arcsin\left(\frac{2x}{4}\right)+C$ | `arcsin_scaled` |
| 16 | 101 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | `arctan_basic` leftover at D=16 |
| 16 | 207 | $\int \frac{1}{\sqrt{16-4x^{2}}}\,dx$ | $\frac{1}{2}\arcsin\left(\frac{2x}{4}\right)+C$ | `arcsin_scaled` leftover at D=16 |
| 22 | 101 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | `arctan_basic` leftover at expert |
| 22 | 207 | $\int \frac{1}{\sqrt{16-4x^{2}}}\,dx$ | $\frac{1}{2}\arcsin\left(\frac{2x}{4}\right)+C$ | `arcsin_scaled`; same pool as D=16 |

Opt-out flag used: _(none — live generator is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same six builders. D=0 is table \(\int 1/(1+x^{2})\). Gallery seeds 101/207 can collide on one form at mid D; rotation is across seeds. Catalog `d_max` plus exclusive bands; `select_form_id` keeps catalog D-weights among the band (quality tilt via `live_quality_form_weights`).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | `arctan_basic` |
| 0 | 207 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | `arctan_basic` |
| 8 | 101 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | `arctan_basic` leftover |
| 8 | 207 | $\int \frac{1}{\sqrt{16-4x^{2}}}\,dx$ | $\frac{1}{2}\arcsin\left(\frac{2x}{4}\right)+C$ | `arcsin_scaled` |
| 16 | 101 | $\int \frac{1}{16+x^{2}}\,dx$ | $\frac{1}{4}\arctan\left(\frac{x}{4}\right)+C$ | `arctan_a2` leftover (no `arctan_basic`) |
| 16 | 207 | $\int \frac{1}{\sqrt{16-4x^{2}}}\,dx$ | $\frac{1}{2}\arcsin\left(\frac{2x}{4}\right)+C$ | `arcsin_scaled` |
| 22 | 101 | $\int \frac{1}{16+4x^{2}}\,dx$ | $\frac{1}{8}\arctan\left(\frac{2x}{4}\right)+C$ | `arctan_scaled` only vs `arcsin_scaled` |
| 22 | 207 | $\int \frac{1}{\sqrt{16-4x^{2}}}\,dx$ | $\frac{1}{2}\arcsin\left(\frac{2x}{4}\right)+C$ | `arcsin_scaled` |

40-seed counts **after**: D=0 `arctan_basic` 40; D=8 leftover mix (same six as old); D=16 `arcsin_scaled` 11 / `arctan_a2` 9 / `arcsin_basic` 8 / `arctan_scaled` 7 / `arcsin_a2` 5 (no `arctan_basic`); D=22 `arcsin_scaled` 22 / `arctan_scaled` 18.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.7 | https://openstax.org/books/calculus-volume-1/pages/5-7-integrals-resulting-in-inverse-trigonometric-functions | Table \(\int 1/(a^{2}+u^{2})\), \(\int 1/\sqrt{a^{2}-u^{2}}\). Ex. 5.50 \(\int dx/\sqrt{4-9x^{2}}\) is the `arcsin_scaled` shape. Ex. 5.49 is definite \(\int_{0}^{1/2} dx/\sqrt{1-x^{2}}\) — stays off this indefinite leaf. Substitution into these table forms stays on the u-sub sibling. |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (5-7).

## Variety notes

Not a WP. D=0 one easy table form (old). Same-D leftover mix at D=8 (that plus \(a^{2}\) / scaled). High D keeps the old scaled builders (do not invent arcsec or a definite core). Six old forms, so D=16 mixes mid leftover + scaled and D=22 is scaled only.

## Limitations

- **Status:** shipped — leftover lockout of D=0 `arctan_basic`. Remaining `LIMITATIONS`: six frozen old builders (table \(\int 1/(1+x^{2})\); \(\int 1/(a^{2}+x^{2})\) / \(\int 1/\sqrt{1-x^{2}}\) / \(\int 1/\sqrt{a^{2}-x^{2}}\) with \(a\ge 2\); scaled \(a^{2}+b^{2}x^{2}\) / \(a^{2}-b^{2}x^{2}\) with \(a,b\ge 2\)); no Ex. 5.49 definite; no arcsec; substitution stays on the u-sub sibling; D=16 can still emit `arcsin_basic` leftover (intentional).
- **Live pairwise:** each item stamps `form_id`, `generator=integral_inverse_trig`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `integral_inverse_trig`

## Proposed engine (reuse vs new)

- **Reuse:** existing `_sample_invtrig` builders in `integrals.py` + `invtrig_integrals.json`. Depth = leftover lockout of \(\int 1/(1+x^{2})\), not a new arcsec / definite core.
- **Not this pass:** Ex. 5.49 definite; arcsec; u-sub into invtrig (sibling leaf).
