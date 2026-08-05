# Continuous-D TODO (EMH leftovers)

Updated: 2026-07-29 (pass: B UI/gallery EMH labels → D ranges)

Audit of remaining easy/medium/hard (EMH) surfaces vs continuous numeric
`difficulty`. Companion to [`CONTINUOUS_D_FULL_MIGRATION.md`](CONTINUOUS_D_FULL_MIGRATION.md)
and [`CONTINUOUS_D_LADDER_DEEPENING.md`](CONTINUOUS_D_LADDER_DEEPENING.md).
Raw counts: [`_audit_emh_vs_continuous.json`](_audit_emh_vs_continuous.json),
[`_audit_emh_generation.json`](_audit_emh_generation.json).

## Verdict (schema)

| Metric | Count |
|--------|------:|
| Catalog types (`QUESTION_TYPES`) | **610** |
| Continuous numeric `difficulty` in settings schema | **610** |
| EMH-only schema (`difficulty_tier` without continuous `difficulty`) | **0** |

Every catalog type exposes continuous D. Legacy `difficulty_tier` remains on most
schemas for presets; the UI hides it when `difficulty` is present
(`TopicSettingsFields`).

---

## Categories

| Cat | Meaning |
|-----|---------|
| **A** | Generation still discrete EMH (not fine continuous). Todo below. |
| **B** | ~~UI/gallery Easy/Medium/Hard labels~~ — **cleared** (Level 0–4 presets). |
| **C** | Schema continuous + generator uses continuous knobs / fine D ladders (or neutral structure with no EMH branch). |

API note: `apply_difficulty_presets` maps numeric `difficulty` → EMH band →
profile presets. That makes many “tier-only” generators *API-capable at 3 bands*
even when the generator body never reads `difficulty`. Those still count as **A**
(not continuous generation).

---

## Fixed this pass (moved toward C)

| Bucket | type_ids / notes |
|--------|------------------|
| **A0** | `geo_quadrilaterals_rhombuses` → wired `geo_rhombus_area` (`RhombusAreaFramework`; base×height → diagonals with D) |
| **A1** | `calc_app_diff_differentials`, `calc_app_diff_slope_tangent_and_normal_lines`, `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` — pilot `_difficulty_tier` → `settings_difficulty_band` + family unlocks via `derivative_rule_structure` |
| **A2 calc/PC** | `calc_diff_power_rule`, `calc_diff_product_rule`, `calc_diff_chain_rule`, `pc_power_rule_for_differentiation` — `sample_derivative_expression` / function-class knobs (do not duplicate) |
| **A2 radicals** | `radical_add_subtract`, `radical_multiply`, `radical_divide` (+ A2/geo review mirrors) via `apply_radical_expression_continuous_knobs` |
| **A2 other** | `a2_rational_expressions_complex_fractions`, `pc_compound_interest`, `geo_trig_trigonometry_and_area` |
| **Already C** | `g6_solutions_to_equations` (`check_equation_solution` already maps numeric D → structure) |
| **CDR deepen** | quotient/trig/invtrig/ln_exp framework generators; other_base / higher_order / implicit / rates / definition / inverse / log-diff use `_rule_structure` + allow gates |
| **A3 calc/PC** | All ~29 listed A3 types → `calc_topic_structure_from_continuous` + `pick_unlocked_families` (D-gated family unlocks + continuous knobs; no EMH structure collapse). Precalc: `pc_definition_of_the_derivative`, `pc_approximating_area_under_a_curve`, `pc_area_under_a_curve_by_limit_of_sums`. Calc: rates / definition / higher-order / tables / other-base / log-diff / implicit / inverse / Rolle / MVT / limits-as-definition / area / indef+def integrals / Riemann / FTC / slope fields |

Tests: `question_engine/tests/test_continuous_d_todo_fixes.py` (D=0 vs D=20 structure).

---

## A — Still not continuous generation

### A3. Continuous-capable only as **3 EMH bands** (`settings_difficulty_band`)

**Cleared this pass.** Former A3 list (~29 type_ids) now spends numeric D via
`calc_topic_structure_from_continuous` / CDR `_rule_structure` unlock gates.

**A3 count:** **0** (was ~29).

### A4. Broader coarse-ladder debt (families, not re-listed type-by-type)

Already tracked in [`CONTINUOUS_D_LADDER_DEEPENING.md`](CONTINUOUS_D_LADDER_DEEPENING.md)
§ “Still coarse”:

- Geometry: right-triangle application leaves; some circle-segment / secant paths;
  construction surfaces still identify-only.
- Algebra 2: complex polar; radical-exponent clusters; 3D systems / planes spans;
  non-conic graphing wrappers.
- Precalc: polynomial zeros / rational inequalities; polar conics beyond identify;
  induction stubs; vectors (now wired but thin).
- Calc: series / many app-diff & definite-integral variants; Newton / motion /
  richer Riemann UX still thin (structure now continuous; content depth TBD).

Also: `frameworks/linear.py` `_slope_difficulty_tier` still prefers string EMH /
stringified `difficulty` without `settings_difficulty_band` (slope / more-on-slope
paths). `frameworks/equation.py` still has EMH solution picks.

Legacy `tier == easy|medium|hard` branches remain in some `calculus.py` helpers
that are **overridden** by `calculus_derivative_rules` / framework samplers
(product/quotient/chain/trig duplicates) — not live A3 paths.

### A — summary counts

| Bucket | Approx. type_ids |
|--------|-----------------:|
| A0 missing | **0** (was 1) |
| A1 broken pilot | **0** (was 3) |
| A2 tier-only / EMH helpers | **0** listed (was ~20) |
| A3 coarse band (listed) | **0** (was ~29) |
| **A listed unique (A0–A3)** | **0** (was ~55) |
| A4 family debt | see ladder deepening (many more leaves) |

---

## B — UI / gallery Easy / Medium / Hard labels — **DONE**

Continuous worksheet D ramps (`d_min`/`d_max`) are labeled **Level 0–4** (with optional
`D min–max` secondary text). Legacy EMH and prior `d0-8`/`d4-14`/`d10-22` strings still
resolve as API aliases; they are never shown as UI copy. No Level 5 (only five ranges).

| Surface | Status |
|---------|--------|
| `lib/worksheet-difficulty.ts` | Presets `level-0`…`level-4` with labels **Level 0–4**; option text `Level N (D …)`; slider label `D N` |
| `question_engine/worksheet_difficulty.py` | Same; EMH + prior D-range aliases input-only |
| `components/WorksheetGenerator.tsx` | Progressive select uses Level presets |
| `components/WorksheetGallery.tsx` | Badges, filter, mapping table use Levels + D secondary |
| `components/GalleryExampleViewer.tsx` | Badge from Level label / D range |
| `config/worksheet-gallery.json` | Entries use `worksheetDifficulty` `level-N`; ids `*-level-N` |
| `public/gallery/index.json` + snapshots | Regenerated with level ids |
| `scripts/build_worksheet_gallery.py` | INDEX emits Level labels |

**Rename target (met):** Levels 0–4 — no Easy/Medium/Hard or bare “D 0–8” as primary UI label.

Per-topic settings UI is continuous-first (`TopicSettingsFields` hides
`difficulty_tier` when `difficulty` exists; leftover tier options label as D ~3/8/14).

Curriculum names that contain the word “hard” (e.g. `pc_logarithmic_equations_hard`)
are **topic titles**, not difficulty controls — leave unless product wants rename.

---

## C — Already continuous (schema + generation)

- **Schema:** 610 / 610.
- **Fine ladders:** types wired through `apply_*_continuous_knobs` /
  `*_structure_from_continuous` / `*_params_from_settings` (see ladder deepening
  “Wired” sections: geo angles/proofs, A2 conics/matrices/sequences, PC trig/
  piecewise, many calc limits/volumes/DE/opt, G6/PA number ladders, etc.).
- **Calc derivative rules:** `frameworks/primitives/derivatives.py` sampler +
  allow/unlock knobs (`derivative_rule_structure`); pilots reuse the same structure.
- **Calc topic EMH→continuous:** `calc_topic_structure_from_continuous` +
  `pick_unlocked_families` for integrals / theorems / Riemann / area / slope fields /
  CDR dedicated builders (rates, definition, implicit, log-diff, …).
- **Effort scorers:** 601+ catalog types scored (`UNSCORED_EFFORT.md` — complete).

---

## Docs / scripts that still emit EMH

| Path | Role |
|------|------|
| `question_engine/settings/presets.py` | EMH preset tables; seeds `difficulty` 3/8/14 for tier clients |
| `lib/difficulty-presets.ts` | Frontend EMH preset maps (legacy; hidden when continuous D shown) |
| `scripts/output/ml/CONTINUOUS_D_*.md` | Historical migration notes (keep) |
| Topic-fit / QA reports under `scripts/output/topic_fit/**` | Many still sample/report easy/medium/hard bands |
| Tests (`test_*`) | Still parametrize EMH tiers for regression — OK as legacy coverage |

---

## Verification

```text
pytest question_engine/tests/test_continuous_d_todo_fixes.py -q
→ 11 passed (prior fixes + A3 calc/PC D=0 vs D=20)

pytest question_engine/tests/test_calculus_derivative_rules.py \
       question_engine/tests/test_calc_derivative_function_knobs.py \
       question_engine/tests/test_continuous_d_ladder_deepening.py -q
→ 70 passed

Live generate (29 former A3 type_ids × D∈{0,8,20}, seed batches):
→ 0 failures; D=0 vs D=20 prompt sets differ

Generator strategy (post-fix):
→ A0–A3 listed unique = 0
→ Remaining work: A4 family deepening (B UI/gallery EMH labels cleared)
```

Recompute generation buckets: `scripts/output/ml/_audit_emh_vs_continuous.py`
(refreshed 2026-07-29: `TOTAL_A_TYPES 0` for module tier-only).
`_audit_emh_generation.json` A0–A3 lists cleared to match TODO.
