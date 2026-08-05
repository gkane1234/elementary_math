# Difficulty sweep gallery (continuous difficulty only)

Generated: `2026-07-19T01:42:10.598719+00:00`

Five samples at each difficulty **0, 5, 10, 15, 20, 25, 50** for Ready catalog types that expose a **continuous numeric `difficulty`** setting (int/float/range) — the same field that drives the worksheet difficulty slider.

Excluded: Ready types with only `difficulty_tier` (easy/medium/hard), select-style discrete `difficulty`, missing difficulty fields, scaffolds, or not-ready demotions.

## Open

- [index.html](index.html) — TOC + summary
- [gallery.html](gallery.html) — full KaTeX gallery
- [by_course/](by_course/) — per-course HTML slices
- [samples.jsonl](samples.jsonl) — full (untruncated) prompts/answers
- [summary.json](summary.json) — machine-readable counts
- [failed.jsonl](failed.jsonl) — failures
- [excluded.jsonl](excluded.jsonl) — Ready types excluded (not continuous)

## Counts

| Continuous-difficulty types included | 29 |
| Unique generators among included | 18 |
| Ready types excluded (no continuous D) | 556 |
| Fully succeeded (all D) | 29 |
| Partial (some D failed) | 0 |
| Fully failed | 0 |
| Skipped before generate | 0 |
| Elapsed | 5.1s |

### Exclude reasons

- difficulty_tier only (easy/medium/hard): **531**
- discrete difficulty field (type=select): **24**
- no difficulty / difficulty_tier field: **1**

## Regenerate

```powershell
$env:PYTHONPATH='.'
python scripts/build_difficulty_sweep_gallery.py
# optional: python scripts/build_difficulty_sweep_gallery.py --timeout 45 --limit 0
```

## High-D notes

- `a2_equations_and_inequalities_multi_step_equations`: grows sharply by D=50 (len≈626 vs D=0≈59)
- `geo_review_multi_step_equations`: grows sharply by D=50 (len≈600 vs D=0≈59)
- `pa_equations_multi_step_equations`: grows sharply by D=50 (len≈733 vs D=0≈68)
