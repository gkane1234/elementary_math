# Notes — `calc_indef_int_multi_trick`

- **Display name:** Multi-technique (u-sub then PFD)
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_multi_trick`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `integral_multi_trick`
- **Remaining limits:** Reuse `integrals.py` / FTC / Riemann constructive cores. Gaps: curve families still thin vs OpenStax §5–6 (mostly poly); trig-sub / PFD / multi-trick are catalog-shaped but not full textbook exercise breadth.

## What the question should look like (D=0 vs high D)

- **Skill:** Integrate with a multi-step technique pipeline (e.g. u-sub then PFD).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{3\left(\cos(2x)\right)-1}{\left(\cos(2x)\right)\left(\cos(2x)-1\right)}\left(-2\sin(2x)\right)\,dx$ | $\ln|\left(\cos(2x)\right)|+2\ln|\left(\cos(2x)-1\right)|+C$ | pattern=u_sub+pfd, form=u_sub_then_pfd_trig |
| 0 | 207 | $\int \frac{0\left(\sin(x)\right)+1}{\left(\sin(x)-1\right)\left(\sin(x)-2\right)}\cdot \cos(x)\,dx$ | $-\ln|\left(\sin(x)-1\right)|+\ln|\left(\sin(x)-2\right)|+C$ | pattern=u_sub+pfd, form=u_sub_then_pfd_trig |
| 8 | 101 | $\int \frac{2\left(\ln|3x + 3|\right)+3}{\left(\ln|3x + 3|\right)^{2}+9}\frac{3}{3x + 3}\,dx$ | $\ln|\ln|3x + 3| - 2|+\ln|\ln|3x + 3|^{2}+9|+\arctan(\frac{\ln|3x + 3|}{3})+C$ | pattern=u_sub+pfd, form=u_sub_then_pfd_log |
| 8 | 207 | $\int \frac{-7}{\left(\ln|2x + 2|\right)^{2}+9}\frac{2}{2x + 2}\,dx$ | $-2\ln|\ln|2x + 2| - 1|-\frac{7}{3}\arctan(\frac{\ln|2x + 2|}{3})+C$ | pattern=u_sub+pfd, form=u_sub_then_pfd_log |
| 16 | 101 | $\int \frac{-2\left(\ln|x + 2|\right)+6}{\left(\ln|x + 2|\right)^{2}+9}\frac{1}{x + 2}\,dx$ | $3\ln|\ln|x + 2| - 2|-\ln|\ln|x + 2|^{2}+9|+2\arctan(\frac{\ln|x + 2|}{3})+C$ | pattern=u_sub+pfd, form=u_sub_then_pfd_log |
| 16 | 207 | $\int \frac{2}{\left(\ln|2x + 1|\right)^{2}+4}\frac{2}{2x + 1}\,dx$ | $-2\ln|\ln|2x + 1| - 4|+\arctan(\frac{\ln|2x + 1|}{2})+C$ | pattern=u_sub+pfd, form=u_sub_then_pfd_log |
| 22 | 101 | $\int \frac{3}{\left(\ln|3x - 2|\right)^{2}+9}\frac{3}{3x - 2}\,dx$ | $2\ln|\ln|3x - 2| - 2|+\arctan(\frac{\ln|3x - 2|}{3})+C$ | pattern=u_sub+pfd, form=u_sub_then_pfd_log |
| 22 | 207 | $\int \frac{2\left(\cos(x)\right)-7}{\left(\cos(x)\right)^{2}+16}\left(-\sin(x)\right)\,dx$ | $14\ln|\cos(x) + 13|+\ln|\cos(x)^{2}+16|-\frac{7}{4}\arctan(\frac{\cos(x)}{4})+C$ | pattern=u_sub+pfd, form=u_sub_then_pfd_trig |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.5 | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | u-sub then PFD / parts mix — e.g. Example 5.30: Using Substitution to Find an Antiderivative Use substitution to find the antiderivative $\int 6 x \left(\right. 3 x^{2} + 4 \left.\right)^{4} d x .$; Example 5.31: Using Substitution with Alteration Use substitution to find $\int z \sqrt{z^{2} - 5} d z .$ |
| OpenStax Calculus Volume 2 §3.4 | https://openstax.org/books/calculus-volume-2/pages/3-4-partial-fractions | multi-technique pipelines |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Reuse `integrals.py` multi-trick path; keep form catalogs.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `integral_multi_trick`; limits/differentiation owned by other agent._
