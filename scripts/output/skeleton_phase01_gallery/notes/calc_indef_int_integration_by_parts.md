# Notes — `calc_indef_int_integration_by_parts`

- **Display name:** Integration by parts
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integration_by_parts`
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate an indefinite integral with integration by parts (LIATE).
- **D=0:** One parts step, coefficient 1 — rotate OpenStax easy shapes: \(\int \ln x\,dx\), \(\int x e^x\,dx\), \(\int x\sin x\,dx\), \(\int x\cos x\,dx\).
- **Mid D (≈8):** Same one-step families with real inner scale: \(\ln(ax)\), \(x e^{kx}\), \(x\sin(kx)\).
- **High D (≈16–22):** Tabular \(x^n e^{kx}\) / \(x^n\sin/cos\) (n≤3), \((\ln(ax))^{2,3}\), cyclic \(e^{ax}\sin/cos(bx)\), \(x\arctan\), \(x\arcsin\). Named preset `parts_form_preset=bc_bank`. Not \(\int \ln x\) again.
- **Must not:** u-sub-only power chains; PFD rationals; derivative prompts; frozen bank LaTeX.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` **before** this pass. Frozen templates; seed 101 stayed \(\int\ln x\) at every D.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \ln(x)\,dx$ | $x\ln(x)-x+C$ | form=`ln_alone` — only D=0 form |
| 0 | 207 | $\int \ln(x)\,dx$ | $x\ln(x)-x+C$ | same |
| 8 | 101 | $\int \ln(x)\,dx$ | $x\ln(x)-x+C$ | still `ln_alone` |
| 8 | 207 | $\int x\cos(x)\,dx$ | $x\sin(x)+\cos(x)+C$ | form=`poly1_cos`, k=1 |
| 16 | 101 | $\int \ln(x)\,dx$ | $x\ln(x)-x+C$ | high D still easy leftover |
| 16 | 207 | $\int e^{x}\cos(x)\,dx$ | $\frac{1}{2}e^{x}(\sin(x)+\cos(x))+C$ | form=`cyclic_exp_cos` |
| 22 | 101 | $\int \ln(x)\,dx$ | $x\ln(x)-x+C$ | no numeric hardness |
| 22 | 207 | $\int e^{x}\cos(x)\,dx$ | $\frac{1}{2}e^{x}(\sin(x)+\cos(x))+C$ | same as D=16 |

Opt-out flag used: `(none — live default is old path)`

## What live path produces now (real latex)

Live `_generate_for_type` after BC bank §2 lookalikes. EMH-hard at D≥16 stamps `parts_form_preset=bc_bank`. `ln_alone` still has `d_max=8`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \ln(x)\,dx$ | $x\ln(x)-x+C$ | `ln_alone`, k=1 |
| 0 | 207 | $\int x\cos(x)\,dx$ | $x\sin(x)+\cos(x)+C$ | `poly1_cos` |
| 0 | 44 | $\int x\sin(x)\,dx$ | $-x\cos(x)+\sin(x)+C$ | `poly1_sin` |
| 8 | 101 | $\int \ln(2x)\,dx$ | $x\ln(2x)-x+C$ | same family, scaled inner |
| 8 | 207 | $\int x\cos(4x)\,dx$ | $\frac{1}{4}x\sin(4x)+\frac{1}{16}\cos(4x)+C$ | k=4 |
| 8 | 44 | $\int xe^{4x}\,dx$ | $\frac{1}{16}e^{4x}(4x-1)+C$ | `poly1_exp` |
| 16 | 101 | $\int x^{2}e^{3x}\,dx$ | $\frac{1}{27}e^{3x}(9x^{2}-6x+2)+C$ | tabular `poly2_exp` |
| 16 | 207 | $\int e^{2x}\cos(x)\,dx$ | $\frac{e^{2x}(2\cos(x)+\sin(x))}{5}+C$ | cyclic; bank preset |
| 16 | 44 | $\int (\ln(3x))^{3}\,dx$ | $x(\ln(3x))^{3}-3x(\ln(3x))^{2}+6x\ln(3x)-6x+C$ | `ln_power_3` lookalike |
| 22 | 207 | $\int e^{2x}\cos(x)\,dx$ | $\frac{e^{2x}(2\cos(x)+\sin(x))}{5}+C$ | cyclic, not \(\int\ln x\) |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 2 §3.1 | https://openstax.org/books/calculus-volume-2/pages/3-1-integration-by-parts | ∫ u dv = uv − ∫ v du; LIATE: ln, x e^x, x sin/cos, tabular x² e^x, cyclic e^{ax}sin(bx), arctan |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-2/` · `scripts/output/example_mining/calculus-volume-2/form_catalogs/integration_by_parts.json`.

## Variety notes

Not a WP. D=0 rotates several one-step LIATE frames (old path was ln-only). High D uses catalog `d_max` so `ln_alone` cannot dominate. EMH-hard is named `parts_form_preset=bc_bank`.

## Live now — skip further leftover lockout

Already rich enough: leftover mix + stamps. Live `_generate_for_type` already stamps `form_id` + `generator=integration_by_parts` on metadata and `spec_snapshot` (40/40). Easy `ln_alone` has catalog `d_max=8`. D=8 leftover mix is `ln_alone` / `poly1_ln` / scaled `poly1_exp|sin|cos`. D=16–22 is named `bc_bank` (no `ln_alone`, no `poly1_exp|sin|cos`). Exclusive leftover bands on `auto` would not change live at D≥16 (named preset). Lockout *under* `bc_bank` would empty `parts_preset_bc_bank`. Did not invent `poly_exp_trig` / `poly1_arccos` / `poly2_ln_quad` cores.

## Limitations

- **Status:** skipped further leftover lockout — live already stamps `form_id` + `generator=integration_by_parts`; catalog `d_max=8` + EMH `bc_bank` already drop `ln_alone` at D≥16. Remaining `LIMITATIONS`: \(\int x e^{ax}\sin(bx)\) (`poly_exp_trig`) deferred — no honest tabular/cyclic answer template; \(\int x\arccos x\) deferred as a duplicate of \(x\arcsin\); \(\int x^{2}\ln(x^{2}+a^{2})\) deferred; \(\sec^3\) owned by the trig-integrals leaf; no definite-parts evaluation on this indefinite leaf; D=16 and D=22 are the same `bc_bank` mix.
- **Live pairwise:** each item stamps `form_id`, `generator=integration_by_parts`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `integration_by_parts`

## Proposed engine (reuse vs new)

- **Reuse:** `integrals.py` `_sample_parts` + `integration_by_parts.json`. Numeric hardness is inner \(k\) / \(a,b\) / polynomial degree, not padded `difficulty_costs`. Depth = document skip, not a new exclusive-band overlay on named presets.
- **Not this pass:** exclusive leftover bands; locking `ln_power_*` / cyclic leftovers out of `bc_bank` (that *is* the named mix); inventing a closed template for `poly_exp_trig`.
