# Notes — `calc_app_diff_lhopitals_rule` (`L'Hôpital's Rule`)

- **Course:** Calculus
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `lhopitals_rule`
- **Suggested family:** other (calc limits / Diff)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate indeterminate limits (0/0, ∞/∞, rewrite 0·∞ / 1^∞ / …) via L'Hôpital when appropriate.
- **D=0:** Simple 0/0 only — \((x^{2}-a^{2})/(x-a)\) or \((e^{kx}-1)/x\) (old easy on the LimitSpec core).
- **Mid D (≈8):** Leftover one-pass 0/0 plus \(\sin(kx)/x\), ∞/∞ rationals, 0·∞ rewrite, ∞−∞ rewrite.
- **High D (≈16–22):** Multipass, exp/poly, 0^0 / ∞^0 / 1^∞ / 0^∞ after ln rewrite. Not leftover \((x^{2}-a^{2})/(x-a)\) or \(\sin(kx)/x\).
- **Must not:** Direct plug-in that is already determinate; dump non-indet cancel as if L'Hôpital were required; invent ε–δ / table cores.

## What old / live path actually produced (real latex, D=0/8/16/22)

**Old Mad-Lib** (`advanced.py` `_lhopitals_rule`, overridden by LimitSpec): only \(\lim_{x\to 0}\sin(ax)/x\). No opt-out flag — live catalog **is** the old LimitSpec path.

**Before this leftover pass** (`_generate_for_type`): D=0 `lhopital_0_0_poly` only; D=8 leftover mix including 0/0 poly (8/40) and \(\sin(kx)/x\) (4/40); D=16 and D=22 the same 12-form pool, still including leftover 0/0 poly (2/40) and trig (4/40). Metadata already stamped `form_id` + `generator=lhopitals_rule`; `spec_snapshot` had neither.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 2} \frac{x^{2}-4}{x-2}$` | `$4$` | form=`lhopital_0_0_poly`; 0/0 |
| 0 | 1 | `$\lim_{x \to 0} \frac{e^{1x}-1}{x}$` | `$1$` | same form; exp 0/0 variant |
| 8 | 101 | `$\lim_{x \to \infty} x^{1} e^{-x}$` | `$0$` | form=`lhopital_0_inf_product`; 0·∞ |
| 8 | 0 | `$\lim_{x \to 3} -2\frac{x^{2}-9}{x-3}$` | `$-12$` | leftover `lhopital_0_0_poly` |
| 8 | 8 | `$\lim_{x \to 0} -\frac{\sin(2x)}{x}$` | `$-2$` | leftover `lhopital_0_0_trig` |
| 16 | 101 | `$\lim_{x \to 0^{+}} 3x^{1/x}$` | `$0$` | form=`lhopital_0_inf_power`; 0^∞ |
| 22 | 101 | `$\lim_{x \to 0^{+}} 16x^{2/x}$` | `$0$` | same form + dress; leftover 0/0 still in the old pool |

Opt-out flag used: _none — LimitSpec `limit_lhopital` / `limits.json` is the live default_

## What live path produces now (real latex)

Leftover lockout of D=0 0/0 poly and of old Mad-Lib \(\sin(kx)/x\) at D≥16 (`d_max=10` on `lhopital_0_0_poly` / `lhopital_0_0_trig`). Stamps `form_id` + `generator=lhopitals_rule` on metadata and `spec_snapshot`. 40-seed counts: D=0 `lhopital_0_0_poly` 40; D=8 leftover mix (`0_inf_product` 10 / `inf_minus_inf` 9 / `inf_inf_poly` 9 / `0_0_poly` 8 / `0_0_trig` 4); D=16/22 identical rewrite/multipass/exp mix (no `0_0_poly`, no `0_0_trig`).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 2} \frac{x^{2}-4}{x-2}$` | `$4$` | `lhopital_0_0_poly` |
| 0 | 1 | `$\lim_{x \to 0} \frac{e^{1x}-1}{x}$` | `$1$` | same form; exp variant |
| 8 | 101 | `$\lim_{x \to \infty} x^{1} e^{-x}$` | `$0$` | `lhopital_0_inf_product` |
| 8 | 0 | `$\lim_{x \to 3} -2\frac{x^{2}-9}{x-3}$` | `$-12$` | leftover 0/0 poly |
| 8 | 8 | `$\lim_{x \to 0} -\frac{\sin(2x)}{x}$` | `$-2$` | leftover \(\sin(kx)/x\) |
| 16 | 101 | `$\lim_{x \to 0^{+}} 3x^{1/x}$` | `$0$` | `lhopital_0_inf_power` |
| 16 | 207 | `$\lim_{x \to 0} 8\frac{\sin(x)-x}{x^{3}}$` | `$-\frac{4}{3}$` | `lhopital_multipass_trig` |
| 16 | 2 | `$\lim_{x \to \infty} -4\frac{x^{2}}{e^{x}}$` | `$0$` | `lhopital_poly_over_exp` |
| 22 | 101 | `$\lim_{x \to 0^{+}} 16x^{2/x}$` | `$0$` | same mix as D=16 + dress |

Opt-out flag used: _none — live catalog on `limits.py` / `limits.json`_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.8 L'Hôpital's Rule | https://openstax.org/books/calculus-volume-1/pages/4-8-lhopitals-rule | Ex. 4.38 0/0 (incl. \((\sin x-x)/x^{2}\)); Ex. 4.39 ∞/∞; Ex. 4.41 0·∞; Ex. 4.42 ∞−∞; Ex. 4.43–4.44 powers; Ex. 4.45 \(x^{k}/e^{x}\) |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/4-8-lhopitals-rule.md`; catalog `limits.json` `lhopital_*`.

## Variety notes

D=0 stays one easy form (`lhopital_0_0_poly`, poly or \((e^{kx}-1)/x\)). D=8 leftover 0/0 + rewrite/∞/∞. High D cannot emit leftover 0/0 poly or \(\sin(kx)/x\). Not a WP. Multi-seed spans 0/0 (multipass), ∞/∞, 0·∞, ∞−∞, 0^0, ∞^0, 1^∞, 0^∞.

## Limitations

- **Status:** leftover lockout of D=0 0/0 poly and of \(\sin(kx)/x\) shipped. Remaining `LIMITATIONS`: D=16 and D=22 are the same rewrite/multipass/exp mix; D=8 can still emit leftover 0/0 (intentional); no Ex. 4.40 “L'Hôpital does not apply” stem; no \(\ln x/\cot x\) / \(\ln x/(5x)\) catalog forms; no ε–δ; dress can wrap a simple core (`8(\sin x-x)/x^{3}`).
- **Live pairwise:** each item stamps `form_id`, `generator=lhopitals_rule`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt inside the leftover band.
- **Generator:** `lhopitals_rule`

## Proposed engine (reuse vs new)

- **Reuse:** LimitSpec `_sample_lhopital` / generator `lhopitals_rule` + `limits.json`. Catalog `d_max=10` on leftover 0/0. No padded `difficulty_costs`. Did not invent Ex. 4.40 / \(\ln x/\cot x\) / ε–δ cores.
- **Shipped this pass:** leftover lockout of D=0 0/0 poly and of \(\sin(kx)/x\) at D≥16; `form_id` + `generator` on `spec_snapshot`.
