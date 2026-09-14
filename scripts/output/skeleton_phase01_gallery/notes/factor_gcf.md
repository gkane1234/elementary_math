# Notes — `factor_gcf` (`polynomial_factoring_common_factor`)

Also covers: `polynomial_factoring_common_factor`, `g6_factor_gcf`, `factor_gcf`

Flags:

- `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Factor a monomial GCF from a sum (binomial at D=0); residual may stay unfactored.
- **D=0:** $6x+9 \to 3(2x+3)$ or $4x+8$.
- **High D (≈16–22):** Larger GCF, more terms, $x^n$ in the GCF — still GCF-only, not trinomials.
- **Must not:** FactorProduct trinomials; same $3x+6$ at every D.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_factor_poly=True`.

- **D=0 seed=101:** $\text{Factor: } 6x + 3$ → $3\left(2x + 1\right)$
- **D=0 seed=207:** $\text{Factor: } 2x + 4$ → $2\left(x + 2\right)$
- **D=8 seed=101:** $\text{Factor: } -12x + 8x^{2}$ → $4x\left(2x - 3\right)$
- **D=8 seed=207:** $\text{Factor: } 3x^{2} + 3x$ → $3x\left(x + 1\right)$
- **D=16 seed=101:** $\text{Factor: } -18x + 12x^{2}$ → $6x\left(2x - 3\right)$
- **D=16 seed=207:** $\text{Factor: } 3x^{2} + 9x$ → $3x\left(x + 3\right)$
- **D=22 seed=101:** $\text{Factor: } -18x + 12x^{2}$ → $6x\left(2x - 3\right)$
- **D=22 seed=207:** $\text{Factor: } 3x^{2} + 9x$ → $3x\left(x + 3\right)$

## Current default (same D/seeds)

- **D=0 seed=101:** $\text{Factor: } 3x + 6$ → $3\left(x + 2\right)$ — form_id=gcf_monomial
- **D=0 seed=207:** $\text{Factor: } 2 + 2x$ → $2\left(x + 1\right)$ — form_id=gcf_monomial
- **D=8 seed=101:** $\text{Factor: } -10x + 5x^{2}$ → $5x\left(x - 2\right)$ — form_id=gcf_monomial, variable_gcf
- **D=8 seed=207:** $\text{Factor: } 6x^{2} - 4x$ → $2x\left(3x - 2\right)$ — form_id=gcf_monomial, variable_gcf
- **D=16 seed=101:** $\text{Factor: } -18x + 9x^{2}$ → $9x\left(x - 2\right)$ — form_id=gcf_monomial, variable_gcf
- **D=16 seed=207:** $\text{Factor: } 4x^{2} - 2x$ → $2x\left(2x - 1\right)$ — form_id=gcf_monomial, variable_gcf
- **D=22 seed=101:** $\text{Factor: } -18x + 9x^{2}$ → $9x\left(x - 2\right)$ — form_id=gcf_monomial, variable_gcf
- **D=22 seed=207:** $\text{Factor: } 4x^{2} - 2x$ → $2x\left(2x - 1\right)$ — form_id=gcf_monomial, variable_gcf

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §7.1 Examples 7.1–7.3** — Find/factor GCF: $4x^2+20$, $5y^3+15y$, $12x^2y+18xy$ — https://openstax.org/books/elementary-algebra-2e/pages/7-1-greatest-common-factor-and-factor-by-grouping

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

**UNCLEAR** — catalog alias `g6_factor_gcf` is **not a live type_id** (`Unknown question type`); live leaf is `polynomial_factoring_common_factor`. Default now climbs with D like old opt-out: D=0 is $3x+6$; D≥8 puts $x$ in the GCF (e.g. $5x(x-2)$, $2x(3x-2)$). OpenStax §7.1 is still richer (two variables).

## Limitations

- UNCLEAR: gold look not fully locked — keep red gallery header; do not invent a new engine.
- Gallery section slug: `factor_gcf` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** FactorGcf / poly_skeleton (wired; D≥8 variable GCF).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `other`
