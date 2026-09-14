# Notes — `calc_diff_implicit` (`Implicit`)

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_implicit`
- **Suggested family:** other (calc limits / Diff)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate an \(F(x,y)=c\) relation implicitly and solve for \(dy/dx\).
- **D=0:** Circle \(x^2+y^2=c\) only (old easy).
- **Mid D (≈8):** OpenStax §3.8 algebraic mix — ellipse \(ax^2+y^2=c\), product \(x^2+xy=c\), \(xy=c\). Not circle leftovers.
- **High D (≈16–22):** Cubes, trig of \(y\), \(e^y\), folium \(x^3+y^3=cxy\). At elite D, scale trig args and two-exponential relations.
- **Must not:** Explicit \(y=f(x)\) only; dump without solving for \(y'\).

## What old / live path actually produced (real latex, D=0/8/16/22)

**Old (pre-catalog routing), seed 101:** D=0 circle; D=8 ellipse; D=16/22 cubes — all stamped `form_id=implicit_basic`. Circle still eligible at D=8.

**Live now** (`_generate_for_type`):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Differentiate implicitly: }y^{2}+x^{2}=1.\text{ Solve for }\frac{dy}{dx}.$` | `$\frac{dy}{dx}=-\frac{x}{y}$` | form=`implicit_basic` |
| 0 | 207 | `$\text{Differentiate implicitly: }x^{2}+y^{2}=3.\text{ Solve for }\frac{dy}{dx}.$` | `$\frac{dy}{dx}=-\frac{x}{y}$` | circle only |
| 8 | 101 | `$\text{Differentiate implicitly: }xy+x^{2}=2.\text{ Solve for }\frac{dy}{dx}.$` | `$\frac{dy}{dx}=-\frac{2x+y}{x}$` | form=`implicit_xy` |
| 8 | 3 | `$\text{Differentiate implicitly: }4x^{2}+y^{2}=2.\text{ Solve for }\frac{dy}{dx}.$` | `$\frac{dy}{dx}=-\frac{8x}{y}$` | form=`implicit_ellipse` |
| 16 | 3 | `$\text{Differentiate implicitly: }\sin(y)=x.\text{ Solve for }\frac{dy}{dx}.$` | `$\frac{dy}{dx}=\frac{1}{\cos(y)}$` | form=`implicit_trig` |
| 16 | 101 | `$\text{Differentiate implicitly: }e^{y}+x=2.\text{ Solve for }\frac{dy}{dx}.$` | `$\frac{dy}{dx}=-e^{-y}$` | form=`implicit_exp` |
| 22 | 3 | `$\text{Differentiate implicitly: }\sin(3x)+\cos(y)=0.\text{ Solve for }\frac{dy}{dx}.$` | `$\frac{dy}{dx}=\frac{3\cos(3x)}{\sin(y)}$` | scaled trig |
| 22 | 44 | `$\text{Differentiate implicitly: }e^{y}+e^{x}=1.\text{ Solve for }\frac{dy}{dx}.$` | `$\frac{dy}{dx}=-e^{x-y}$` | two-exp |
| 22 | 0 | `$\text{Differentiate implicitly: }x^{3}+y^{3}=3xy.\text{ Solve for }\frac{dy}{dx}.$` | `$\frac{dy}{dx}=\frac{x^{2}-y}{x-y^{2}}$` | form=`implicit_folium` |

Opt-out flag used: _none — structured catalog on the existing Mad-Lib builders_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.8 Implicit Differentiation | https://openstax.org/books/calculus-volume-1/pages/3-8-implicit-differentiation | Circle; ellipse; \(xy\) product; cubes; \(\sin y\); \(e^y\); folium \(x^3+y^3=axy\) |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/3-8-implicit-differentiation.md`

Catalog forms: `implicit_basic`, `implicit_ellipse`, `implicit_xy`, `implicit_product`, `implicit_cubes`, `implicit_trig`, `implicit_exp`, `implicit_folium`.

## Variety notes

D=0 stays one easy frame (circle). Mid/high D rotate several §3.8 algebraic / trig / exp / folium shapes. Not a WP.

## Limitations

- **Status:** shipped — catalog-routed closed-form families. Remaining `LIMITATIONS`: not a general \(F(x,y)\) AST / `expr_skeleton` relation sampler; templates cover listed OpenStax shapes only (no arbitrary mixed trig-poly products).
- **Generator:** `derivative_implicit`

## Proposed engine (reuse vs new)

**Reuse:** existing structured implicit builders + `derivatives.json` form_ids with `d_min`/`d_max` (same pattern as parts / trig integrals). No padded costs. Product+chain textbook items stay on the product leaf.

- **Shipped this pass:** catalog routing; D=0 circle-only; high D cannot emit `implicit_basic`.
