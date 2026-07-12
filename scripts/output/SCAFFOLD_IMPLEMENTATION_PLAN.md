# Scaffold Implementation Plan (2026-07-11)

## Baseline (session start)
Wired 391 · Scaffold 210 · Ready 354

## Mid-session (after first geometry/advanced wave)
Wired 453 · Scaffold 148 · Ready 445

## Parallel workers (in flight)
| Worker | Scope |
|--------|--------|
| Geometry | frameworks/geometry*, generators/geometry, diagrams, geometry catalog |
| Grade 6 | generators/grade6, frameworks/number, grade_6 catalog |
| Precalc/Calc | generators/precalc+calculus, those catalogs |
| Algebra 2 | generators/algebra2, algebra_2 catalog |
| Stats/Word | statistics + charts, using_statistical_models |

## Orchestrator (this agent)
1. Merge new generator keys into `generator_profiles.py` (and `__init__.py` only if new modules)
2. Resolve catalog/denylist conflicts
3. Run `scripts/audit_ready_types.py` — fix broken generators
4. Document true Tier-3 deferrals
5. **Only then** `scripts/generate_all_types_examples_pdf.py` with E/M/H per Ready type

## PDF gate
No PDF until: scaffold cleared or explicitly deferred + audit pass.

## PDF requirement
Exactly 1 Easy + 1 Medium + 1 Hard per Ready type via `difficulty_tier`.
