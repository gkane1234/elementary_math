# Notes — `g6_distributive_property_area_diagrams_numeric` (`g6_distributive_property_area_diagrams_numeric`)

- **Display name:** Distributive property with area diagrams, numeric
- **Catalog chapter:** Grade 6 — Numeric Expressions, Exponents, and the Order of Operations
- **Generator key:** `g6_distributive_property_area_diagrams_numeric` (registry → `PRIM_DISTRIBUTIVE`; live path currently wrong)
- **Already on skeleton:** no
- **Flags:** `UNCLEAR`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Use an area model to expand / evaluate a **numeric** distributive product $a(b+c)$.
- **D=0:** small integers with a 1×2 area diagram.
- **High D:** larger integers / more addends; still numeric (no $x$).
- **Must not:** divisibility Yes/No; algebraic area model (sibling leaf); bare arithmetic with no diagram.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `include_answer_key=True`, seed 101.

**Pre-fix (catalog miswire to `g6_divisibility`):** Yes/No divisibility stems at every D — wrong topic.

**Post-fix:** should match `g6_distributive_property_numeric` shapes (distribute rewrite) with area-model metadata. Re-sample in gallery after regen.

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Prealgebra 2e **§7.3** | https://openstax.org/books/prealgebra-2e/pages/7-3-distributive-property | Area / model distribution + numeric expand |

## Variety notes / UNCLEAR flag

**UNCLEAR:** gold is numeric area-model distribute. Catalog miswire to divisibility is **fixed**; live prompts now match the numeric distributive sibling. Still UNCLEAR on rewrite-vs-evaluate keys, and area SVG was missing in a D=0 spot-check.

## Limitations

- Flags: **UNCLEAR**.
- Token: **LIMITATIONS**.
- **Miswire fixed in catalog:** was `generator=g6_divisibility`; now `distributive_property` + area_model family (same core as numeric sibling).
- Gold still UNCLEAR on rewrite-vs-evaluate (uncombined product keys), same as the non-diagram sibling.
- Diagram-named leaf: live sample at D=0 still had **no** `diagram_svg` after the wiring fix — confirm area SVG attachment.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** `sample_distributive_numeric` + area-model presentation. No new skeleton.
- **New:** none.
- **Not this pass:** no further generator redesign until rewrite-vs-evaluate gold is locked; also verify SVG path.

Suggested family: **affine**.
