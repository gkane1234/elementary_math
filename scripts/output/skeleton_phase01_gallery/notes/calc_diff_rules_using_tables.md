# Notes — `calc_diff_rules_using_tables`

- **Display name:** Rules, using tables
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_from_tables`
- **Suggested family:** diff / other

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `derivative_from_tables`
- **Remaining limits:** Dedicated constructive / Mad-Lib-meta generators (not expr_skeleton gallery topics). Gaps: table/figure UX still text-only; logarithmic / inverse-function depth vs OpenStax §3.8–3.9 limited; implicit remains Mad-Lib (see that leaf).

## What the question should look like (D=0 vs high D)

- **Skill:** Rules, using tables — match OpenStax shape below.
- **D=0:** As simple as live easy samples.
- **High D (≈16–22):** Numeric / structure unlocks via continuous D (not metadata pads).
- **Must not:** Wrong-topic dump; Diff skeleton on non-Diff leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` (default path).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $f(1)=4,\ f'(1)=-1,\ g(1)=-4,\ g'(1)=5.\quad\text{Find }(fg)'(1).$ | $24$ | — |
| 0 | 207 | $f(1)=-6,\ f'(1)=-1,\ g(1)=-1,\ g'(1)=-4.\quad\text{Find }(fg)'(1).$ | $25$ | — |
| 8 | 101 | $f(1)=-1,\ f'(1)=3,\ g(1)=1,\ g'(1)=-3.\quad\text{Find }\left(\frac{f}{g}\right)'(1).$ | $0$ | — |
| 8 | 207 | $f(4)=-3,\ f'(4)=2,\ g(4)=-4,\ g'(4)=-5.\quad\text{Find }\left(\frac{f}{g}\right)'(4).$ | $-\frac{23}{16}$ | — |
| 16 | 101 | $f(1)=2,\ f'(1)=6,\ g(1)=-4,\ g'(1)=5.\quad\text{Find }(fg)'(1).$ | $-14$ | — |
| 16 | 207 | $f'(-2)=-3,\ g(3)=-2,\ g'(3)=1.\quad\text{Find }(f\circ g)'(3).$ | $-3$ | — |
| 22 | 101 | $f(4)=-2,\ f'(4)=-6,\ g(4)=-1,\ g'(4)=3.\quad\text{Find }\left(\frac{f}{g}\right)'(4).$ | $12$ | — |
| 22 | 207 | $f(3)=4,\ f'(3)=-1,\ g(3)=-1,\ g'(3)=5.\quad\text{Find }\left(\frac{f}{g}\right)'(3).$ | $-19$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.3 | https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules | product/quotient/chain from table |

Local HTML / mine: `scripts/output/example_mining/calculus-volume-1/stage1/`

## Variety notes

Shapes follow live samples; OpenStax frames win for story variety when applicable.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** current catalog generator `derivative_from_tables`.
- **Not this pass:** gallery stub + Limitations; flesh only if gold locked.
