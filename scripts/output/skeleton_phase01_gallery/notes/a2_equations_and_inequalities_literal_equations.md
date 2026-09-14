# Notes — `a2_equations_and_inequalities_literal_equations`


- **Course:** Algebra 2 (A2 catalog)
- **Category:** Algebra 2 — Equations and Inequalities
- **Generator:** `literal_equations`
- **Suggested family:** `solve`

---

## What the question should look like (D=0 vs high D)

- **Skill:** One-step isolate a named variable ($d=rt$ for $t$, $A=\ell w$ for $w$).
- **D=0:** One-step isolate a named variable ($d=rt$ for $t$, $A=\ell w$ for $w$).
- **High D (≈16–22):** Two-step / fraction formulas ($A=\frac12 bh$, $V=\ell wh$).
- **Must not:** Multi-step linear in $x$ only; WP dump.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out: `use_sample_literal_equation=True`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $A = \ell w \quad \text{Solve for } w.$ | $w = \frac{A}{\ell}$ |  |
| 0 | 207 | $d = r t \quad \text{Solve for } t.$ | $t = \frac{d}{r}$ |  |
| 8 | 101 | $A = \frac{1}{2} b h \quad \text{Solve for } h.$ | $h = \frac{2A}{b}$ |  |
| 8 | 207 | $V = \ell w h \quad \text{Solve for } w.$ | $w = \frac{V}{\ell h}$ |  |
| 16 | 101 | $A = \frac{1}{2} b h \quad \text{Solve for } h.$ | $h = \frac{2A}{b}$ |  |
| 16 | 207 | $V = \ell w h \quad \text{Solve for } w.$ | $w = \frac{V}{\ell h}$ |  |
| 22 | 101 | $A = \frac{1}{2} b h \quad \text{Solve for } h.$ | $h = \frac{2A}{b}$ |  |
| 22 | 207 | $V = \ell w h \quad \text{Solve for } w.$ | $w = \frac{V}{\ell h}$ |  |

Opt-out flag used: `use_sample_literal_equation=True`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Elementary Algebra 2e §2.6 | https://openstax.org/books/elementary-algebra-2e/pages/2-6-solve-a-formula-for-a-specific-variable | Geometry formulas; solve for indicated variable |
| OpenStax Intermediate Algebra 2e §2.2 | https://openstax.org/books/intermediate-algebra-2e/pages/2-2-use-a-general-strategy-to-solve-equations | Literal equations in applications chapter |

## Variety notes / UNCLEAR flag

Old path shapes recorded above; OpenStax frames win for WP stories.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SolveLiteral (equation_skeleton) — alias of `literal_equations`.
- **New:** only if no honest match (see benchmark-old-path skip).
- **Not this pass:** notes only — no generator implementation.
