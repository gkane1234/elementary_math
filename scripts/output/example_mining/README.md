# Example mining outputs

Generated from local OpenStax HTML under `textbooks/openstax/html/`.

## Stages

| Stage | Goal | Status |
|-------|------|--------|
| **1_inventory** | Extract examples / checkpoints / exercises with MathML→LaTeX prompts | Calc Vol 1 chs 2–6; Vol 2–3 pilots (+ §3.2–3.3); Precalculus 2e chs 1,4–7; Prealgebra 2e Ch 3–6; Elementary Algebra 2e Ch 2, 4–10 |
| **1b_form_catalog** | Explicit textbook form taxonomy (`form_id`) driving Spec samplers | Trig integrals + **A1** `algebra1_*` + **Precalc** `precalculus_*` (function ops / exp-log / trig / PFD); see `openstax_form_catalogs/` + `scripts/output/ml/OPENSTAX_FORM_CATALOG.md` |
| **2_families** | Tag *each mined item* with form_id + within-family EMH | Not started (catalog exists; per-item classification of stage1 dumps does not) |
| **3_progression** | Prerequisite DAG + reading order across sections | G6 → PreAlg → Alg1 + Calc Vol 1 |

## Stage 1 command

```powershell
$env:PYTHONPATH='.'
python scripts/mine_openstax_section.py --book calculus-volume-1 --chapter 2 --sections 1-3
python scripts/mine_openstax_section.py --book prealgebra-2e --chapter 3 --sections 1-5
python scripts/mine_openstax_section.py --book elementary-algebra-2e --chapter 2 --sections 1-7
```

Inspect: `scripts/output/example_mining/calculus-volume-1/stage1/`, `scripts/output/example_mining/prealgebra-2e/stage1/`, `scripts/output/example_mining/elementary-algebra-2e/stage1/`

User Calc BC indefinite-integral drill bank (extra form families, not OpenStax): `challenging_indefinite_integrals_bc.tex` + mapping `challenging_indefinite_integrals_bc.md`.

## Cross-section progression graph

Two views in each output file:

1. **Prerequisite DAG** — curated actual dependencies (`scripts/example_mining/prerequisites/<book>.json`). Rendered **left-to-right** (`flowchart LR`): prerequisites on the left, dependents on the right. Sibling topics (e.g. L'Hôpital vs optimization) share prerequisites but are not chained by textbook order. Cross-course edges link Foundations → Grade 6 → Prealgebra → Algebra 1 → Geometry → Algebra 2 → Precalculus → Calculus.
2. **Reading order** — textbook chapter/section sequence for reference.

Chapter intros and motivational sections appear in reading order only. Grade 6 / Foundations / Geometry use curriculum units. Algebra 1 Foundations (Ch 1) is omitted from the DAG — real prerequisites point at Prealgebra instead.

```powershell
$env:PYTHONPATH='.'
python scripts/build_progression.py --preset full --name full_spine
python scripts/export_prerequisite_browser.py
python scripts/build_progression.py --preset g6-prealg-alg1 --name g6_prealg_alg1
python scripts/build_progression.py --books calculus-volume-1
```

Output: `scripts/output/example_mining/progression/` — `<name>.md` / `<name>.json`.
Topic picker index: `lib/data/prerequisite-index.json`.

Prerequisite maps live under `scripts/example_mining/prerequisites/`.
- **Section maps** (`<book>.json`): OpenStax section → section edges (textbook DAG).
- **Topic leaves** (`topic_leaves.json`): curriculum `type_id` → `type_id` skill deps for intra-chapter cases the chapter export drops (e.g. trig derivatives → power/product/chain). Re-run `export_prerequisite_browser.py` after edits.
