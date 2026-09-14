# Notes — `calc_limits_by_direct_evaluation` (`By direct evaluation`)

- **Course:** Calculus
- **Category:** Calculus — Limits
- **Generator:** `limit_direct_evaluation`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `limit_direct_evaluation`
- **Remaining limits:** LimitSpec packs ship. Remaining gaps: form_id metadata sometimes mismatches latex (e.g. `direct_sqrt` stamp on rational plug-in); one-sided / piecewise story variety thinner than OpenStax §2.2–2.4 exercise banks; no dedicated limit-skeleton patterns beyond packs.

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate a two-sided limit at a finite point by plugging in (poly / rational / specials).
- **D=0:** Polynomial plug-in, e.g. lim_{x→a}(ax²+bx+c).
- **High D (≈16–22):** Richer direct plug-ins (rational with nonzero den, roots/trig/exp/log when unlocked) — still direct, not removable/indet.
- **Must not:** 0/0 cancel, jump piecewise, ∞, L'Hôpital — those are other leaves.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path (Diff leaves → `expr_skeleton` when form maps; limits → LimitSpec packs). No `use_sample_*` / Mad-Lib opt-out found for these generators.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 1} \left(2x^{2} - 3x + 3\right)$` | `$2$` | form=`poly_direct`; skel=`—`; pack=`limit_direct` |
| 8 | 101 | `$\lim_{x \to 4} \frac{3x^{3} - 3x}{2x - 1}$` | `$\frac{180}{7}$` | form=`direct_sqrt`; skel=`—`; pack=`limit_direct` |
| 16 | 101 | `$\lim_{x \to 4} \frac{2x^{3} + 6x}{-4x + 7}$` | `$-\frac{152}{9}$` | form=`direct_sqrt`; skel=`—`; pack=`limit_direct` |
| 22 | 101 | `$\lim_{x \to 4} \frac{-2x^{3} + 3x}{6x - 7}$` | `$-\frac{116}{17}$` | form=`direct_sqrt`; skel=`—`; pack=`limit_direct` |

Opt-out flag used: _none found (LimitSpec / form catalog is the live default; no `use_sample_*` opt-out)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §2.3 The Limit Laws | https://openstax.org/books/calculus-volume-1/pages/2-3-the-limit-laws | direct plug-in poly / rational / trig / exp |
| OpenStax Calculus Volume 1 §2.2 The Limit of a Function | https://openstax.org/books/calculus-volume-1/pages/2-2-the-limit-of-a-function | limit-at-a-point language |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/2-3-the-limit-laws.md; form catalog limits.json`

## Variety notes / flags

Live LimitSpec packs (`limit_direct`). form_id at D≥8 often stamped `direct_sqrt` while latex is still rational plug-in — metadata mismatch; shapes themselves escalate coefs ok. No Diff skeleton.

## Proposed engine (reuse vs new) — proposal only

**Reuse:** `question_engine/frameworks/primitives/limits.py` LimitSpec + form catalog `limits.json` (`poly_direct`, `rational_direct`, …). **Not** `expr_skeleton` Diff. Optional future: dedicated limit-skeleton patterns if pack variety stalls.

- **Not this pass:** notes only — no generator changes.

Coverage: Diff algebraic families also cataloged in `scripts/output/diff_skeleton_gallery/` (power, product, quotient, chain, trig, invtrig, ln/exp, general, higher_order).
