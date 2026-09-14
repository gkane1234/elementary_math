# Notes — `a2_direct_and_inverse_variation_direct_and_inverse_variation`

> **LIMITATIONS** — Live `variation_packaging` rotates direct/inverse; OpenStax joint/cost frames still thin.

- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Direct and Inverse Variation
- **Generator:** `direct_inverse_variation`
- **Suggested family:** `other`
- **Gallery slug:** `direct_inverse_variation` (engine `variation_packaging`; A2 alias on type_id)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Write $y=kx$ or $y=k/x$; find $k$; short direct-rate stories.
- **D=0:** Given-$k$ inverse or point→equation.
- **High D (≈16–22):** Mix direct point, inverse point, direct-rate story frames (OpenStax EA §8.9).
- **Must not:** Inverse-only Mad-Lib at every D (legacy path).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `none (hand generator)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{If } y \text{ varies inversely with } x \text{ and } y = \frac{5}{6} \text{ when } x = 6, \text{ write the equation.}$ | $y = \frac{5}{x}$ |  |
| 0 | 207 | $\text{Write an inverse variation equation with } k = 12.$ | $y = \frac{12}{x}$ |  |
| 8 | 101 | $\text{If } y \text{ varies inversely with } x \text{ and } y = \frac{5}{6} \text{ when } x = 6, \text{ write the equation.}$ | $y = \frac{5}{x}$ |  |
| 8 | 207 | $\text{Write an inverse variation equation with } k = 12.$ | $y = \frac{12}{x}$ |  |
| 16 | 101 | $\text{If } y \text{ varies inversely with } x \text{ and } y = \frac{5}{6} \text{ when } x = 6, \text{ write the equation.}$ | $y = \frac{5}{x}$ |  |
| 16 | 207 | $\text{Write an inverse variation equation with } k = 12.$ | $y = \frac{12}{x}$ |  |
| 22 | 101 | $\text{If } y \text{ varies inversely with } x \text{ and } y = \frac{5}{6} \text{ when } x = 6, \text{ write the equation.}$ | $y = \frac{5}{x}$ |  |
| 22 | 207 | $\text{Write an inverse variation equation with } k = 12.$ | $y = \frac{12}{x}$ |  |

Opt-out flag used: `none (hand generator)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §8.9 | https://openstax.org/books/elementary-algebra-2e/pages/8-9-use-direct-and-inverse-variation | Direct, inverse, joint; story contexts |

## Variety notes / UNCLEAR flag

Legacy hand path (table above) was **inverse-only** and D-flat. Live default now uses `variation_packaging` (opt out `use_legacy_variation=True`) and rotates `var_inverse_k` / `var_inverse_point` / `var_direct_point` / `var_direct_rate` in the gallery.

## Limitations

Flags for gallery red header: `LIMITATIONS`.

- **Variety (residual):** Direct + inverse + rate are present live; still missing OpenStax-style **joint** variation and richer cost/work frames from EA §8.9.
- **Difficulty scaling:** Legacy samples in this file are D-flat — trust gallery `direct_inverse_variation` live ladder, not the inverse-only table above.
- **OpenStax:** EA §8.9 cite is correct; expand frames toward joint / application stems before clearing `LIMITATIONS`.
- **Shipped?** Algebraic packaging yes; story-bank incomplete vs OpenStax.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** `variation_packaging` (already wired in gallery).
- **New:** not needed for core algebra; extend frames only.
- **This pass:** Limitations audit only — no new engine.
