# Consistency / consolidation sweep

## Scope
Full audit of all Ready types after scaffold implementations. Conflicting catalog wirings: **0**.

## Unified

### Shared settings profiles (59 generators newly mapped)
- Precalc/calc foundations → `algebra_expression` / `derivatives`
- Geometry circle / construction / triangle families → matching `geometry_*` profiles
- G6 nets, area, hanger/tape → `geometry_basic` / `equation` / `inequality`
- Matrices / systems / radicals / logs / trig graphing → sibling profiles (`algebra_expression`, `systems`, `radical`, `logarithm`, `trigonometry`)

### Difficulty presets added for families
`logarithm`, `exponential`, `trigonometry`, `limits`, `derivatives`, `integrals`, `statistics`, `algebra_expression`

### Instruction / header consistency
- `_pc` / `_calc` helpers now use `resolve_instruction_latex` / `resolve_instruction_text` (same as geometry/grade 6)
- Fixed wrong “Solve.” defaults: `pc_continuity`, `calc_diff_eq_introduction`, `geo_review_multi_step_equations` → “Solve for x.”

### Graphing consolidation
- `graphing_trig_functions` now emits blank `graph_spec` + `answer_graph_spec` (origin-centered), matching other graphing types
- `pc_graphing_trig_functions` wired to the same canonical generator as Algebra 2

### Readiness denylists (unchanged, verified)
Still demoted (correct): drawing UIs, scatter stand-in, isometric, vector diagrams, composite rhombus/kite trig.
`INCORRECT_IMPLEMENTATION` remains empty.

### Bugfix enabling clean audit
- `rational.py` LCD factor `randint` empty-range clamp when `target_degree_max` is small

## Deferred (Coming soon)
See `scripts/output/DEFERRED.md` (13 `REQUIRES_DIAGRAM` ids).
