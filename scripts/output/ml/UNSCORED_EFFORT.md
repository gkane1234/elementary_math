# Unscored continuous-D effort coverage

**Status: COMPLETE (2026-07-28)** — **0** unscored / **601** scored.

Catalog continuous-D types come from
[`scripts/output/_continuous_d_buckets.json`](_continuous_d_buckets.json)
(601 rows). A type is **scored** when `has_effort_scorer(type_id)` is true.

## Snapshot

| Metric | Count |
|--------|------:|
| Catalog continuous-D types | 601 |
| Catalog types with effort scorers | **601** |
| Catalog types still unscored | **0** |
| Scorer registry size (`EFFORT_SCORERS`) | 611 (includes non-catalog aliases) |

### Unscored by course

| Course | Unscored | Notes |
|--------|---------:|-------|
| geometry | 0 | Constructions + notation scored via `effort_construction` / `effort_geo_notation` |
| grade_6 | 0 | Fraction sides / grid / shaded / isometric scored |
| algebra_1 | 0 | Exp graph / solve-by-graphing / scatter / visualizing scored |
| precalculus | 0 | `pc_vectors_diagrams` uses `vector_diagrams` + `effort_vector_diagram` |
| calculus | 0 | — |
| algebra_2 | 0 | — |
| pre_algebra | 0 | — |

## Final coverage wave (done)

- **A1:** `graphing_exponential_functions`, `quadratic_solve_by_graphing`, `scatter_plots`, `visualizing_data`
- **G6:** fraction rect/tri/prism + grid/shaded polygons + isometric volume/SA
- **Geo:** 8 construction leaves + `geo_basics_geometric_diagrams_and_notation`
- **Precalc:** replaced `scaffold` for `pc_vectors_diagrams` with tip-to-tail `vector_diagrams` generator

A1 re-exported + retrained (**73** labeled types / **6570** rows; forward r≈0.91).
Precalc export list includes `pc_vectors_diagrams`; full JSONL re-export optional
(current labeled file is still 93 types / 8370 rows).

## How to recompute

```powershell
$env:PYTHONPATH='.'
python -c "import json; from pathlib import Path; from collections import Counter; from question_engine.ml.effort import has_effort_scorer, EFFORT_SCORERS; rows=json.loads(Path('scripts/output/_continuous_d_buckets.json').read_text(encoding='utf-8'))['rows']; u=[(r['course'],r['id']) for r in rows if not has_effort_scorer(r['id'])]; print(len(EFFORT_SCORERS), 601-len(u), len(u)); print(dict(Counter(c for c,_ in u)))"
```

See also [`FIGURE_DIVERSITY.md`](FIGURE_DIVERSITY.md).
