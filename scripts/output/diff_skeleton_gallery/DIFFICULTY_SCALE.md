# Differentiation skeleton — conceptual difficulty scale
Conceptual difficulty (`conceptual_difficulty` / C) elaborates **holes** inside
an OpenStax form’s skeleton pattern. It does **not** change the pattern itself
(e.g. C never swaps `Diff(Prod(F,G)(u))` for `Diff(Prod(F,G))`).
Pattern choice comes from the form map in `expr_skeleton.FORM_PATTERNS`.
## Bands
| Band | C (approx) | Inner `u` | Hole F / G / powers | Nest |
|------|------------|-----------|---------------------|------|
| **Low** | 0–4 | Var / Affine | Apply / simple poly of x | 0 |
| **Mid** | 4–12 | Affine → **Poly** unlock | poly-of-u; `power_min` rises | 0 (poly is the unlock) |
| **High** | 12–20 | Poly; **forced nest ≥1** | higher exponents | 1 (Apply or algebraic compose) |
| **Elite** | 20+ | Deeper nest | richest exponents / coefs | 2 |
When the pattern’s atom pool is **poly-only**, nest spends as algebraic compose
(poly / power of a sub-inner) rather than Apply — so C still densifies latex.
## Debug fields (gallery)
Each sample records:
- **Identity:** `form_id`, `skeleton_pattern`, `skeleton_kind`, `productions`, seed
- **Richness knobs:** band, nest_budget, force_min_nest, allow/prefer_poly_u,
  power_min/max, poly_degree_min, coef_abs_max, atomFN candidates
- **Cost / spend (honest):** inner_kind, nest_depth_expr, chain_depth, degree_max,
  n_applies, n_terms — measured from the generated AST, not padded
## Pattern kinds (form-owned)
| Pattern | Meaning | Typical forms |
|---------|---------|---------------|
| `Diff(Pow(H,n))` | Power / chain-power | `power_*`, `chain_power_linear`, higher-order |
| `Diff(Apply(fn,u))` | Named outer | `trig_basic`, `ln_basic`, `exp_basic`, chain/invtrig |
| `Diff(Prod(F,G))` | Product, **independent** inners | `product_two_poly`, `product_poly_trig`, `product_poly_exp` |
| `Diff(Prod(F,G)(u))` | Product, **shared** u | `trig_product_chain`, `ln_exp_product` |
| `Diff(Quot(F,G))` | Quotient, independent inners | `quotient_*` textbook cases |
| `Diff(F(u))` | Loose | `general_mixed` |
## Spec axis
Spec difficulty only spends identity extras (`expression_flesh`), not skeleton
richness. See module docs on `expr_skeleton` / `expression_flesh`.
