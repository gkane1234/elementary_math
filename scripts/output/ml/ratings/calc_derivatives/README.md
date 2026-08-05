# Calc derivatives — hand rating package

Generated for human effort / quality ratings. Machine fields are complete;
human fields start null.

## Files

| File | Role |
|------|------|
| `rater.html` | Open locally (KaTeX). Enter ratings; autosaves to localStorage; export JSON. |
| `items.jsonl` | Full machine rows (θ, Spec snapshot, prompts, metadata). |
| `items.json` | Same rows as a JSON array (loaded by the rater). |
| `calc_derivatives_ratings.json` | Exported / recovered human store (`rating_id` → fields). |
| `ratings_filled.jsonl` | `items.jsonl` merged with human ratings. |
| `CALIBRATION.md` | Coverage + correlation + recalibration summary. |
| `recalibration_linear.json` | Linear maps between rating ↔ `y_effort` / difficulty. |
| `human_forward_effort_model.json` (+ `.pkl`) | Tiny GBR trained on human→effort-mapped targets. |
| `INDEX.json` | Stratification counts + regenerate hints. |
| `COVERAGE.md` | OpenStax form checklist vs generator packs / gaps. |
| `README.md` | This file. |

## How to rate

1. Open `rater.html` in a desktop browser (double-click / file://).
2. Use **Show → Unrated only** (default when any nulls remain) to work through
   unfinished items; switch to **All** or **Rated only** as needed. Prev/Next
   skip items hidden by the filter.
3. For each item, enter **rating 1–5** (effort/quality for ML — see scale below),
   optional **minutes**, and optional **notes**.
4. Existing `calc_derivatives_ratings.json` is embedded (and fetched when served
   over HTTP) as the baseline; **localStorage** overrides merge on top
   (`poly_rating_calc_derivatives`).
5. Click **Export ratings JSON** to download `calc_derivatives_ratings.json`
   (merge of rating_id → human fields). Click **Export full JSONL** to download
   items with ratings filled in.
6. Keep `items.jsonl` immutable as the machine source of truth; store exported
   ratings beside it (e.g. `ratings_filled.jsonl`).

### Suggested 1–5 scale

| Score | Meaning |
|-------|---------|
| 1 | Trivial / under-topic / broken |
| 2 | Easy for the claimed D / thin |
| 3 | On-level |
| 4 | Solid challenge for claimed D |
| 5 | Hard / dense / high cognitive load (still fair) |

Use notes for pedagogy flags (wrong topic, ugly latex, answer suspect, etc.).

## Stratification

- **Items:** 360 (0 generation errors)
- **Difficulties:** [0.0, 3.0, 6.0, 8.0, 12.0, 16.0, 20.0, 25.0]
- **Per pack:** see `INDEX.json`

## Regenerate / join later

Each row carries:

- `type_id`, `generator`, `seed`, continuous `difficulty`
- `theta_full` (resolved allow_*/require_* + Spec-merged exponent knobs)
- `spec_snapshot` when Spec packs ran
- `function_classes`, `methods_used`, `effort_features`, structure inventory

```powershell
$env:PYTHONPATH='.'
python -c "from question_engine.api.handler import _generate_for_type; print(_generate_for_type('TYPE', {'difficulty': D, 'count': 1, 'include_answer_key': True, 'seed': SEED})[0].prompt_latex)"
```

## Later courses

Sibling scaffolds (empty until built):

- `../algebra_1/`
- `../algebra_2/`
- `../precalc_algebraic/`

Rebuild this campaign:

```powershell
$env:PYTHONPATH='.'
python scripts/build_hand_rating_set.py --campaign calc_derivatives
```
