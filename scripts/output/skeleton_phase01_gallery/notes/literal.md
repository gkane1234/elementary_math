# Notes — `literal` (`literal_equations`)

Also covers: `literal_equations`

Flags:

- _(none)_

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve a formula for a specified variable.
- **D=0:** One-step isolate: $d=rt$, $A=\ell w$, $C=\pi d$.
- **High D (≈16–22):** Multi-term formulas; fractions; isolate a var that is not already alone.
- **Must not:** Numeric linear equations in one unknown; word-problem stories.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_sample_literal_equation=True`.

- **D=0 seed=101:** $A = \ell w \quad \text{Solve for } w.$ → $w = \frac{A}{\ell}$
- **D=0 seed=207:** $d = r t \quad \text{Solve for } t.$ → $t = \frac{d}{r}$
- **D=8 seed=101:** $A = \frac{1}{2} b h \quad \text{Solve for } h.$ → $h = \frac{2A}{b}$
- **D=8 seed=207:** $V = \ell w h \quad \text{Solve for } w.$ → $w = \frac{V}{\ell h}$
- **D=16 seed=101:** $A = \frac{1}{2} b h \quad \text{Solve for } h.$ → $h = \frac{2A}{b}$
- **D=16 seed=207:** $V = \ell w h \quad \text{Solve for } w.$ → $w = \frac{V}{\ell h}$
- **D=22 seed=101:** $A = \frac{1}{2} b h \quad \text{Solve for } h.$ → $h = \frac{2A}{b}$
- **D=22 seed=207:** $V = \ell w h \quad \text{Solve for } w.$ → $w = \frac{V}{\ell h}$

Opt-out flag used: `use_sample_literal_equation=True`

## Current default (same D/seeds)

- **D=0 seed=101:** $d = r t \quad \text{Solve for } r.$ → $r = \frac{d}{t}$ — form_id=literal_equation, pattern=SolveLiteral
- **D=0 seed=207:** $C = \pi d \quad \text{Solve for } d.$ → $d = \frac{C}{\pi}$ — form_id=literal_equation, pattern=SolveLiteral
- **D=8 seed=101:** $C = \pi d \quad \text{Solve for } d.$ → $d = \frac{C}{\pi}$ — form_id=literal_equation, pattern=SolveLiteral
- **D=8 seed=207:** $P = a + b + c \quad \text{Solve for } a.$ → $a = P - b - c$ — form_id=literal_equation, pattern=SolveLiteral
- **D=16 seed=101:** $P = 2L + 2W \quad \text{Solve for } W.$ → $W = \frac{P - 2L}{2}$ — form_id=literal_equation, pattern=SolveLiteral
- **D=16 seed=207:** $y = 3x + 12 \quad \text{Solve for } x.$ → $x = \frac{y - 12}{3}$ — form_id=literal_equation, pattern=SolveLiteral
- **D=22 seed=101:** $V = L W H \quad \text{Solve for } H.$ → $H = \frac{V}{L W}$ — form_id=literal_equation, pattern=SolveLiteral
- **D=22 seed=207:** $P = 2L + 2W \quad \text{Solve for } W.$ → $W = \frac{P - 2L}{2}$ — form_id=literal_equation, pattern=SolveLiteral

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL. Do not dump copyrighted problem text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §2.6 | https://openstax.org/books/elementary-algebra-2e/pages/2-6-solve-a-formula-for-a-specific-variable | Solve $d=rt$ for $t$; $A=\tfrac12 bh$ for $h$; $P=2L+2W$ for $W$. |

Local HTML (if mined): `textbooks/openstax/html/elementary-algebra-2e/` or `intermediate-algebra-2e/`.

## Variety notes

Not a WP. Old D=0 is $A=\ell w$ / $d=rt$; D≥8 is $A=\tfrac12 bh$ / $V=\ell wh$ and
does not climb further in these seeds. Default unlocks $P=2L+2W$ and $y=mx+b$ isolate
at D≥16 (OpenStax EA §2.6).

## Limitations

- Gallery section slug: `literal` (type_id or alias).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveLiteral / equation_skeleton (already wired). Opt-out: `use_sample_literal_equation`.
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `A1_INDEX.md`: `solve`

_Catalog:_ Algebra 1 — Equations — Literal equations. Generator `literal_equations`.
