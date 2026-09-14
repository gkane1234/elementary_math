# Notes — `calc_limits_at_jump_discontinuities_and_kinks` (`At jump discontinuities and kinks`)

- **Course:** Calculus
- **Category:** Calculus — Limits
- **Generator:** `limit_jump`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `limit_jump`
- **Remaining limits:** LimitSpec packs ship. Remaining gaps: form_id metadata sometimes mismatches latex (e.g. `direct_sqrt` stamp on rational plug-in); one-sided / piecewise story variety thinner than OpenStax §2.2–2.4 exercise banks; no dedicated limit-skeleton patterns beyond packs.

## What the question should look like (D=0 vs high D)

- **Skill:** Decide whether a two-sided limit exists for a piecewise jump (one-sided values disagree) — OpenStax one-sided / jump story.
- **D=0:** Constant-vs-constant piecewise at the kink; answer DNE.
- **High D (≈16–22):** Linear/poly pieces meeting with unequal one-sided limits; optionally ask one-sided lim x→a± explicitly.
- **Must not:** Removable holes, essential 1/x oscillation, infinity limits.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` / LimitSpec after flesh fix (2026-08-20).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 5} f(x)\text{ where }f(x)=\begin{cases}-1&x<5\\6&x\ge 5\end{cases}$` | `$\text{DNE}$` | form=`piecewise_jump`; const\|\|const |
| 8 | 101 | `$\lim_{x \to 5} f(x)\text{ where }f(x)=\begin{cases}-6x + 5&x<5\\4&x\ge 5\end{cases}$` | `$\text{DNE}$` | form=`piecewise_jump_linear`; linear\|\|const |
| 16 | 101 | `$\lim_{x \to 5^{+}} f(x)\text{ where }f(x)=\begin{cases}2x^{2} + 4&x<5\\2&x\ge 5\end{cases}$` | `$2$` | form=`piecewise_jump_poly`; one-sided + quad |
| 22 | 101 | `$\lim_{x \to 5^{+}} f(x)\text{ where }f(x)=\begin{cases}2x^{2} + x + 6&x<5\\-6&x\ge 5\end{cases}$` | `$-6$` | form=`piecewise_jump_poly` |

Opt-out flag used: _none found (LimitSpec default)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §2.2 The Limit of a Function | https://openstax.org/books/calculus-volume-1/pages/2-2-the-limit-of-a-function | one-sided limits; jump where lim− ≠ lim+ |
| OpenStax Calculus Volume 1 §2.4 Continuity | https://openstax.org/books/calculus-volume-1/pages/2-4-continuity | piecewise jump / kink continuity |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/2-2-the-limit-of-a-function.md; 2-4-continuity.md`

## Variety notes / flags

Shipped: form_id matches flesh (const → linear → poly); occasional one-sided prompts at mid/high D. Structural `jump_side_*` wraps — no whole-prompt scale.

## Proposed engine (reuse vs new)

**Reuse:** LimitSpec `limit_jump` pack. Flesh linear/poly pieces to match form_ids; one-sided prompts. No Diff skeleton.
