# Notes — `calc_indef_int_trigonometric`

- **Display name:** Trigonometric
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_trigonometric`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `integral_trigonometric`
- **Remaining limits:** OpenStax §3.2 catalog plus BC bank closed forms (`sin_cos_both_odd`, `csc_j_cot`, `sin_over_one_plus_cos2`, `one_over_one_plus_cos/sin`). Deferred: Weierstrass `1/(a+sin)`, `csc^5` reduction, `tan^4 sec^3` mixed parity. D=0 stays table sin/cos/sec².

## What the question should look like (D=0 vs high D)

- **Skill:** Practice trigonometric.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \sin(3x)\,dx$ | $-\frac{1}{3}\cos(3x)+C$ | pattern=trig, form=basic_sin_kx |
| 0 | 207 | $\int \sec(x)\tan(x)\,dx$ | $\sec(x)+C$ | pattern=trig, form=basic_sec_tan |
| 8 | 101 | $\int \cos^{2}(x)\sin(x)\,dx$ | $-\frac{1}{3}\cos^{3}(x)+C$ | pattern=trig+u_sub, form=cos_j_sin |
| 8 | 207 | $\int \tan^{4}(x)\sec^{2}(x)\,dx$ | $\frac{1}{5}\tan^{5}(x)+C$ | pattern=trig+u_sub, form=tan_k_sec2 |
| 16 | 101 | $\int \cos^{2}(x)\sin(x)\,dx$ | $-\frac{1}{3}\cos^{3}(x)+C$ | pattern=trig+u_sub, form=cos_j_sin |
| 16 | 207 | $\int \csc^{3}(x)\cot(x)\,dx$ | $-\frac{1}{3}\csc^{3}(x)+C$ | BC bank `csc_j_cot` |
| 22 | 101 | $\int \cos^{2}(x)\sin(x)\,dx$ | $-\frac{1}{3}\cos^{3}(x)+C$ | pattern=trig+u_sub, form=cos_j_sin |
| 22 | 207 | $\int \csc^{3}(x)\cot(x)\,dx$ | $-\frac{1}{3}\csc^{3}(x)+C$ | BC bank `csc_j_cot` |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.4 | https://openstax.org/books/calculus-volume-1/pages/5-4-integration-formulas-and-the-net-change-theorem | basic trig antiderivatives — e.g. Example 5.23: Integrating a Function Using the Power Rule Use the power rule to integrate the function $\int_{1}^{4} \sqrt{t} (1 + t) d t .$; Example 5.24: Finding Net Displacement Given a velocity function $v (t) = 3 t - 5$ (in meters per second) for a particle in motion from time $t = 0$ to time $t = 3 ,$ find the net displacemen… |
| OpenStax Calculus Volume 2 §3.2 | https://openstax.org/books/calculus-volume-2/pages/3-2-trigonometric-integrals | powers of sin/cos (Calc 2) — e.g. Example 3.8: Integrating $\int \cos^{j} x \sin x d x$ Evaluate $\int \cos^{3} x \sin x d x .$; Example 3.9: A Preliminary Example: Integrating $\int \cos^{j} x \sin^{k} x d x$ Where k is Odd Evaluate $\int \cos^{2} x \sin^{3} x d x .$ |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Reuse `question_engine/frameworks/primitives/integrals.py` + OpenStax form catalogs; harden difficulty via real technique structure (not Diff).
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `integral_trigonometric`; limits/differentiation owned by other agent._
