# Notes — `calc_diff_rules_using_tables` (`Rules, using tables`)

- **Display name:** Rules, using tables
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_from_tables`
- **Suggested family:** diff / other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Apply product / quotient / chain at a point from tabulated \(f,f',g,g'\) (text values, not a figure).
- **D=0:** Easy leftover — product \((fg)'(a)\) from four values (old easy).
- **Mid D (≈8):** Easy leftover still allowed, plus quotient \(\bigl(\frac{f}{g}\bigr)'(a)\).
- **High D (≈16):** Lock out product. Quotient leftover plus compose \((f\circ g)'(a)=f'(g(a))g'(a)\).
- **Expert (≈22):** Compose only.
- **Must not:** Formula product/quotient/chain (those Diff-skeleton leaves); a figure-bank table; padded `difficulty_costs`; a new sum+product / three-function core.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Accumulating pool (`product`; `+quotient` at D≥6; `+compose` at D≥12), so D=16 and D=22 were the same three-family pool. `form_id` / `generator` unstamped (`generation_settings` / `instruction_latex` only). 40-seed counts: D=0 `product` 40; D=8 leftover mix (`product` 25 / `quotient` 15); D=12 `product` 13 / `quotient` 15 / `compose` 12; D=16 and D=22 the same mix (D=16 `compose` 15 / `product` 14 / `quotient` 11; D=22 `product` 17 / `compose` 13 / `quotient` 10).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $f(3)=4,\ f'(3)=5,\ g(3)=-5,\ g'(3)=-4.\quad\text{Find }(fg)'(3).$ | $-41$ | `product` |
| 0 | 207 | $f(4)=2,\ f'(4)=4,\ g(4)=6,\ g'(4)=-4.\quad\text{Find }(fg)'(4).$ | $16$ | `product` |
| 8 | 101 | $f(3)=0,\ f'(3)=-2,\ g(3)=-4,\ g'(3)=6.\quad\text{Find }\left(\frac{f}{g}\right)'(3).$ | $\frac{1}{2}$ | leftover `quotient` |
| 8 | 207 | $f(3)=1,\ f'(3)=-4,\ g(3)=-3,\ g'(3)=5.\quad\text{Find }(fg)'(3).$ | $17$ | leftover `product` |
| 16 | 101 | $f(3)=-2,\ f'(3)=-5,\ g(3)=-2,\ g'(3)=-2.\quad\text{Find }(fg)'(3).$ | $14$ | leftover `product`; same pool as D=22 |
| 16 | 2 | $f(2)=6,\ f'(2)=2,\ g(2)=-3,\ g'(2)=-3.\quad\text{Find }\left(\frac{f}{g}\right)'(2).$ | $\frac{4}{3}$ | leftover `quotient`; same pool as D=22 |
| 12 | 0 | $f'(-4)=4,\ g(2)=-4,\ g'(2)=-2.\quad\text{Find }(f\circ g)'(2).$ | $-8$ | leftover `compose` (compose unlocks D≥12) |
| 22 | 101 | $f(1)=-1,\ f'(1)=-1,\ g(1)=6,\ g'(1)=-3.\quad\text{Find }(fg)'(1).$ | $-3$ | leftover `product`; frozen identical pool to D=16 |
| 22 | 313 | $f(2)=0,\ f'(2)=4,\ g(2)=-5,\ g'(2)=6.\quad\text{Find }\left(\frac{f}{g}\right)'(2).$ | $-\frac{4}{5}$ | leftover `quotient`; frozen identical pool to D=16 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same three builders. D=0 stays old \((fg)'\). Gallery seeds 101/207/313 can collide on one form at a given D; rotation is across seeds. `select_form_id` consumes RNG, so D=0 seed 101 is now \(a=2\) not the pre-lockout \(a=3\).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $f(2)=2,\ f'(2)=-1,\ g(2)=1,\ g'(2)=-6.\quad\text{Find }(fg)'(2).$ | $-13$ | `product` |
| 0 | 207 | $f(2)=5,\ f'(2)=-4,\ g(2)=-6,\ g'(2)=4.\quad\text{Find }(fg)'(2).$ | $44$ | `product` |
| 8 | 1 | $f(2)=3,\ f'(2)=6,\ g(2)=6,\ g'(2)=-5.\quad\text{Find }(fg)'(2).$ | $21$ | leftover `product` |
| 8 | 101 | $f(2)=2,\ f'(2)=-1,\ g(2)=1,\ g'(2)=-6.\quad\text{Find }\left(\frac{f}{g}\right)'(2).$ | $11$ | `quotient` |
| 16 | 1 | $f(2)=3,\ f'(2)=6,\ g(2)=6,\ g'(2)=-5.\quad\text{Find }\left(\frac{f}{g}\right)'(2).$ | $\frac{17}{12}$ | leftover `quotient` (no product) |
| 16 | 101 | $f'(1)=-2,\ g(2)=1,\ g'(2)=-6.\quad\text{Find }(f\circ g)'(2).$ | $12$ | `compose` |
| 22 | 101 | $f'(1)=-2,\ g(2)=1,\ g'(2)=-6.\quad\text{Find }(f\circ g)'(2).$ | $12$ | `compose` only |
| 22 | 1 | $f'(6)=2,\ g(2)=6,\ g'(2)=-5.\quad\text{Find }(f\circ g)'(2).$ | $-10$ | `compose` only |

40-seed counts **after**: D=0 `product` 40; D=8 leftover product + quotient (23+17); D=16 quotient leftover + compose (23+17, no `product`); D=22 `compose` 40.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.3 Example 3.23 | https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules | Product at a point from \(f(a),f'(a),g(a),g'(a)\) — keep the four-value stem, not a binomial product |
| OpenStax Calculus Volume 1 §3.3 | https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules | Quotient rule; old path evaluates \(\bigl(\frac{f}{g}\bigr)'(a)\) from the same four values |
| OpenStax Calculus Volume 1 §3.6 | https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule | Chain \((f\circ g)'(a)=f'(g(a))g'(a)\) from tabulated \(f',g,g'\) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (3-3, 3-6). Formula product/quotient/chain stay on the Diff-skeleton siblings.

## Variety notes

Not a WP. D=0 is the single old easy product builder (evaluation point and integers rotate). Same-D rotation at mid D: leftover product vs quotient. High D keeps the old quotient / compose builders (do not invent a figure-bank table, three-function product, or \(f+g\) / \(f-g\) cores). Three old forms, so D=16 mixes quotient leftover + compose and D=22 is compose-only.

## Limitations

- **Status:** shipped — leftover lockout of D=0 \((fg)'\). Remaining `LIMITATIONS`: three frozen old builders (text values only, no OpenStax table figure; no Ex. 3.23 \(j=fg\) naming; no three-function product / combined quotient+product; compose still omits \(f(a)\) and uses a fresh \(f'(g(a))\); integers \(\pm 1\ldots 6\) only); D=16 can still emit quotient leftover (intentional).
- **Live pairwise:** each item stamps `form_id` (= family), shared `generator=derivative_from_tables`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `derivative_from_tables`

## Proposed engine (reuse vs new)

- **Reuse:** existing `derivative_from_tables` four-value / compose builders. Depth = leftover lockout of product, not a new table-figure core.
- **Not this pass:** figure-bank table; sum of products; \(h=f+g\) from values.
