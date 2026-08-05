# Expression generator plan (polynomial-first via derivatives)

**Date:** 2026-07-29  
**Status:** Phases 0–3 implemented (derivatives wedge)  
**Intent:** Expose a **single expression sampler** (ops, paren/assoc, nesting, structure) driven by **constraints**. Derivative topic leaves become **constraint packs** on top. Do **not** require G6→… unification now; keep the door open for that end-state.

### Implementation status (2026-07-29)

| Phase | Status | Notes |
|-------|--------|-------|
| 0 — Extract poly helpers | **Done** | `frameworks/primitives/poly_expression.py`: `sample_poly_atom`, `compose_power`, `product_pair`, `quotient_pair`; `derivatives.py` wrappers |
| 1 — ExpressionSpec + AST | **Done** | Frozen `ExpressionSpec`, poly `ExprAST`, `sample_expression`, AST→AST `differentiate`, `render_latex`; packs for power / product / alg-chain; algebraic paths via Spec |
| 2 — Inventory + paren policy | **Done** | `structure_inventory` (`shape_id`, ops, nest, degrees); `paren_style` minimal / always_factors / always_powers; metadata wired on samples |
| 3 — Elementary Fn nodes | **Done** | `Fn` AST + Spec `allowed_functions`; trig / ln-exp / invtrig framework leaves Spec-driven; legacy `calculus.py` poly builders documented as shadowed |
| 4+ — Full packs / cleanup | Not started | Implicit / log-diff / quotient Spec; delete shadowed calculus paths optional |

**Verify:** `test_poly_expression.py`, `test_calc_derivative_function_knobs.py`, `test_calculus_derivative_rules.py`; live generate power/product/chain + trig/ln-exp/invtrig.

---

## 1. Why this wedge

Full bottom-up unification of every arithmetic / algebra expression path is too ambitious. Derivatives already:

- Sample **algebraic atoms** (`_atom_poly`, `_atom_linear`) and compose them with product / quotient / power-chain.
- Gate structure with **topic allow/require packs** (`_TOPIC_DEFAULTS`) + continuous-D upgrades.
- Emit **topic-fit metadata** (`methods_used`, `function_classes`, `structure_id`).

That is the right shape for “one generator + constraint packs,” but today expression shape and differentiation are **fused** inside `question_engine/frameworks/primitives/derivatives.py` as latex string pairs (`DerivativeExpr.body_latex` / `deriv_latex`). There is no reusable AST, and poly sampling is a private helper rather than a Spec-driven API.

**Strategy:** Extract **polynomial expression sampling** first (the common core of power / product / sum-of-powers / algebraic chain). Keep differentiation as a **consumer**. Grow Spec fields until derivative leaves are thin packs. Elementary function nodes and full non-poly packs come later.

---

## 2. Current code map (ground truth)

| Piece | Role today | Relation to plan |
|-------|------------|------------------|
| `frameworks/primitives/derivatives.py` | Continuous-D sampler; `_TOPIC_DEFAULTS`; `_atom_poly` / product / quotient / compose; `sample_derivative_expression` | **Source to extract from**; keep as derivative façade |
| `generators/calculus_derivative_rules.py` | Thin `_framework_generator` for power/product/quotient/chain/trig/ln-exp/invtrig | Stays thin; packs call Spec |
| `generators/calculus.py` | Legacy poly `d/dx` builders (`_random_poly_terms`, product/quotient/chain madlibs); **overridden** in `GENERATORS` merge by derivative_rules for shared keys | Do **not** revive; optional later delete / redirect |
| `expression_structure.py` | Binary tree + paren/assoc for **numeric OOO** and **affine** algebraic | **Reference only** (paren policy, D leaf/nest curves) — do not merge yet |
| `poly_compose.py` / constructive | Value-preserving inflate toward a **target** poly | Different invariant (target coeffs); reuse ideas/helpers, not the API |
| `poly_helpers.sample_poly_coeffs` | Sparse coeff maps for algebra primitives | Useful leaf sampler for poly Spec |
| Precalc `pc_power_rule_for_differentiation` | Same generator key `derivative_power_rule` | Shared pack risk — see §6 |

Existing allow keys (`allow_*` / `require_*`) already behave like constraint packs. End-state maps them onto `ExpressionSpec` (+ a thin `DerivativeSpec` for prompt framing / answer mode).

---

## 3. End-state API sketch

Polynomial-first subset is enough for early phases; later fields are sketched so packs can grow without renaming.

```python
# Conceptual API — not implemented yet

@dataclass(frozen=True)
class ExpressionSpec:
    """Constraints for sampling one univariate expression tree."""

    variable: str = "x"

    # --- Polynomial-first (Phase 0–2) ---
    allowed_ops: frozenset[str] = frozenset({"+", "*", "^"})  # later: "/", compose, fn
    degree_min: int = 1
    degree_max: int = 4
    term_count_min: int = 1
    term_count_max: int = 3
    coef_abs_max: int = 5
    allow_negative_coefs: bool = True
    allow_constant_term: bool = True
    require_leading: bool = True

    # Structure shape (derivative methods become these)
    require_product: bool = False
    require_sum: bool = False          # ≥2 addends (sum-of-powers / poly)
    require_power_of_poly: bool = False  # (ax+b)^n or (poly)^n
    forbid_product: bool = False
    forbid_quotient: bool = True       # poly-first default
    max_nesting: int = 1
    max_factors: int = 2               # for product of polys

    # Presentation (optional; may stay latex-policy until Phase 2)
    paren_style: Literal["minimal", "always_factors", "always_powers"] = "always_factors"
    assoc_bias: Literal["left", "right", "balanced", "flat"] | None = None

    # Budget
    d_spend: float = 6.0               # continuous D; upgrades buy terms/powers/nest
    seed: int | None = None

    # --- Later (Phase 3+) — reserved, unused early ---
    # allowed_functions: frozenset[str] = frozenset()  # sin, exp, ln, ...
    # allow_rational_powers: bool = False
    # allow_quotient: bool = False


@dataclass(frozen=True)
class ExprAST:
    """Opaque tree: Var, Const, Add, Mul, Pow, later Fn / Quotient."""
    # Implementation detail: dataclass nodes or tagged unions.
    # Must support: render_latex, structure_inventory, differentiate (poly subset).


def sample_expression(spec: ExpressionSpec, *, rng: random.Random | None = None) -> ExprAST: ...

def render_latex(expr: ExprAST, *, paren_style: str | None = None) -> str: ...

def differentiate(expr: ExprAST, var: str = "x") -> ExprAST: ...  # symbolic AST → AST

def structure_inventory(expr: ExprAST) -> dict[str, Any]:
    """Topic-fit / gallery: ops, degrees, nest, product/sum flags, shape_id."""
    ...


# Derivative topics = Spec packs + framing
def pack_power_rule(d: float, **overrides) -> ExpressionSpec: ...
def pack_product_rule(d: float, **overrides) -> ExpressionSpec: ...
# ...

def sample_derivative_from_spec(spec: ExpressionSpec, *, frame: str = "d_dx") -> DerivativeSample:
    expr = sample_expression(spec)
    d_expr = differentiate(expr, spec.variable)
    return DerivativeSample(
        prompt_latex=frame_derivative(render_latex(expr), spec.variable, frame),
        answer_latex=render_latex(d_expr),
        metadata=structure_inventory(expr),
        ...
    )
```

### Mapping today’s defaults → Spec packs

| Topic / generator | Spec essence (poly era) |
|-------------------|-------------------------|
| `derivative_power_rule` | `allowed_ops={+,^}`; `require_sum` optional via D; no product/quotient; roots later as `^` with rational |
| `derivative_product_rule` | `require_product=True`; factors algebraic polys / linears |
| `derivative_chain_rule` (alg) | `require_power_of_poly=True`; inner linear→quad by D |
| `derivative_higher_order` | Same poly Spec + `differentiate` applied *n* times (still out of early PR) |
| Trig / exp / log leaves | Phase 3+: `allowed_functions` + method requires |

Worksheet settings (`allow_*` / `require_*` / `difficulty`) continue to merge into Spec the way `resolve_derivative_allows` + `structure_knobs_from_d` do today.

---

## 4. Phases (0–N) and exit criteria

### Phase 0 — Extract & stabilize poly sampling (no behavior change)

**Work**

- Split **poly atom + algebraic product / sum / `(·)^n`** construction out of `derivatives.py` into a focused module, e.g. `frameworks/primitives/poly_expression.py` (name TBD).
- Public surface: something like `sample_poly_expression_latex(...)` **or** early AST with latex parity — prefer **minimal AST** if it stays small; otherwise extract string builders first and introduce AST in Phase 1.
- `derivatives._atom_poly` / algebraic branches of product & chain call the new module.
- Keep `DerivativeExpr` / `sample_derivative_expression` signatures and metadata stable.
- Document Spec fields that already exist implicitly (`coef_hi`, `power_max`, `term_budget`, force product/chain).

**Exit criteria**

- Existing tests: `test_calc_derivative_function_knobs.py`, `test_calculus_derivative_rules.py`, power/product/chain smoke paths — **pass unchanged**.
- Spot-check: regenerate `derivative_power_rule` / `derivative_product_rule` at fixed seeds; latex distribution within prior families.
- No new worksheet UI; no catalog changes.

### Phase 1 — `ExpressionSpec` (polynomial subset) + packs for power / product / sum-of-powers

**Work**

- Introduce frozen `ExpressionSpec` + `sample_expression(spec) -> ExprAST` for **poly-only** trees: monomials, sums of powers, products of polys/linears, `(linear|poly)^n`.
- Implement `differentiate` for that subset (power, sum, product, chain-on-power) producing AST (or latex if AST diff is deferred one phase — prefer AST→AST).
- Replace algebraic paths in `sample_derivative_expression` for:
  - `derivative_power_rule`
  - `derivative_product_rule`
  - algebraic-only `derivative_chain_rule` when no specials purchased
- Topic defaults become **named pack constructors** that return `ExpressionSpec` (wrappers around today’s `_TOPIC_DEFAULTS` + D spans).

**Exit criteria**

- Power / product / algebraic chain **only** go through Spec packs (no private `_atom_poly` fork).
- Metadata still includes `methods_used` / `structure_id`; inventory fields may gain `degree`, `n_terms`, `n_factors`.
- Knobs / allow flags for those leaves still work (settings override pack).

### Phase 2 — Structure inventory + paren policy

**Work**

- Formalize `structure_inventory(expr)` for topic-fit QA / gallery (`shape_id`, ops multiset, nest depth, require flags satisfied).
- Align paren/assoc with a **small explicit policy** (borrow ideas from `expression_structure` assoc biases; do not import the whole engine).
- Optional: wire inventory into Mad-Libs leftovers (`higher_order`, other-base) only if cheap.

**Exit criteria**

- QA / sampling scripts can filter or report poly derivative shapes without parsing latex.
- No “unreadable” default paren explosion on easy power-rule items (see Risks).

### Phase 3 — Elementary function nodes (still Spec-driven)

**Work**

- Extend AST: `Fn(sin|cos|tan|exp|ln|…, arg)`, optional `Quotient`.
- Extend Spec: `allowed_functions`, unlock costs (reuse `difficulty_knobs` → `derivatives`).
- Migrate trig / ln-exp / invtrig / mixed product+special off string atoms onto Spec.

**Exit criteria**

- Remaining `_framework_generator` leaves for specials call Spec; `_TOPIC_DEFAULTS` fully expressed as packs.
- Integrals still out of scope.

### Phase 4 — Full derivative packs + cleanup (optional stretch)

**Work**

- Implicit / logarithmic differentiation as packs (may stay specialized builders longer).
- Delete or stub dead poly paths in `calculus.py` that are shadowed by `calculus_derivative_rules`.
- Document how a future non-calc consumer (e.g. expand/factor) could call `sample_expression` with a different pack — **without** forcing G6 migration.

**Exit criteria**

- One documented entrypoint for “sample expression under constraints”; derivatives are the primary consumer; other courses may adopt packs later.

### Phase N (explicit non-goal for this program)

- Unify OOO / `expression_structure` / `poly_compose` into one global grammar.
- Rebuild entire arithmetic stack from elementary up.

---

## 5. What stays out (for now)

| Out of scope | Why |
|--------------|-----|
| Limits, MVT, related rates, definition-of-derivative tables | Different prompts; not expression-AST consumers yet |
| `derivative_from_tables`, Riemann / FTC / integrals | Separate generators; integrals must not drive Spec design |
| Full G6→PA→A1 expression unification | Too large; Spec design only **allows** later sharing |
| Merging `expression_structure` or `poly_compose` into derivatives | Different invariants (affine OOO / target poly); reference only |
| Implicit / log-diff / other-base enrichment | Keep madlibs until Phase 3–4 |
| Changing worksheet UX beyond existing allow_* knobs | Packs map to current settings |

---

## 6. Risks

1. **Duplicate grammars**  
   Poly latex in `derivatives`, sparse coeffs in `poly_helpers`, inflate trees in `poly_compose`, binary trees in `expression_structure`. Mitigation: Phase 0 extract **one** poly sampler for derivative consumers; reuse `sample_poly_coeffs` / `format_polynomial_latex` only; do not fork a third coeff API.

2. **Unreadable paren rules**  
   Today products always wrap `\left(u\right)\left(v\right)` and powers use `\left(inner\right)^{n}`. A naïve “always paren” Spec makes easy power-rule worksheets noisy. Mitigation: `paren_style` with **minimal** default for pure sums-of-monomials; force wrappers only for product/chain packs.

3. **Precalc ↔ Calc shared `derivative_power_rule`**  
   Catalog: `pc_power_rule_for_differentiation` and Calc power-rule both use the same generator. Spec/pack changes affect both. Mitigation: pack constructors may take `course=` or keep PC on a conservative Spec subset; regression-sample both catalogs before merging Phase 1.

4. **Answer-key drift**  
   Moving from hand-built `deriv_latex` strings to `differentiate(AST)` can change simplification (e.g. `2\cdot 1` vs `2`). Mitigation: phase gate with golden seed snapshots; normalize latex in tests or accept documented simplification rules.

5. **D-upgrade double spend**  
   Spec `d_spend` plus existing `select_upgrades` could apply twice if not careful. Mitigation: single budget consumer — either Spec absorbs upgrade selection, or packs pre-resolve knobs then pass concrete bounds (degree_max, term_count_max) into Spec.

6. **Scope creep into specials**  
   Temptation to migrate trig before poly Spec is solid. Mitigation: Phase 1 exit criteria are poly-only; specials stay string atoms until Phase 3.

---

## 7. First PR-sized slice (after plan approval)

**Smallest useful change:** Phase 0 extract only.

1. Add `question_engine/frameworks/primitives/poly_expression.py` with:
   - `sample_poly_atom(rng, var, coef_hi, power_max, *, extra_term) -> PolyExpr` (latex body + deriv latex **or** tiny AST with both renders)
   - helpers for algebraic product of two poly atoms and `(inner)^n` used by chain — **only** what `_atom_poly` / algebraic chain need
2. Point `derivatives._atom_poly` (and algebraic-only call sites if trivial) at that module.
3. Add a short unit test: fixed seed → stable body/deriv latex; optional import-path test that power-rule generator still returns questions.
4. No Spec dataclass yet; no catalog/UI changes; no deletion of `calculus.py` legacy.

**Verify:** `pytest` on `test_calc_derivative_function_knobs.py` + `test_calculus_derivative_rules.py` (or focused subset); one live generate call for `derivative_power_rule` at D≈3 and D≈12.

**Follow-up PR (not this slice):** introduce `ExpressionSpec` + pack for `derivative_power_rule` only.

---

## 8. Design principles (carry through all phases)

1. **Sample expression once; differentiate / render as separate steps** — even if early extract still returns paired latex for parity.
2. **Topics are packs, not forked generators** — keep `_framework_generator` thin.
3. **Polynomial-first Spec is real API**, not a throwaway — later fields extend, don’t replace.
4. **Metadata is first-class** — structure inventory must support topic-fit without latex archaeology.
5. **No forced cross-course rewrite** — expression module may later serve PA/A1; derivatives do not wait on that.

---

## 9. Suggested file touch list (future, not now)

| Path | Likely phases |
|------|----------------|
| `frameworks/primitives/poly_expression.py` | 0–2 (new) |
| `frameworks/primitives/expression_spec.py` or same module | 1 |
| `frameworks/primitives/derivatives.py` | 0–3 (façade + packs) |
| `generators/calculus_derivative_rules.py` | 1 (unchanged shape; packs) |
| `tests/test_poly_expression.py` | 0+ |
| `scripts/output/ml/EXPRESSION_GENERATOR_PLAN.md` | this doc |

---

## 10. One-line verdict

**Use derivatives as the wedge:** extract poly expression sampling → Spec/AST → topic packs; leave limits/integrals/full arithmetic unification out until poly Spec is the single source for power/product/algebraic-chain leaves.
