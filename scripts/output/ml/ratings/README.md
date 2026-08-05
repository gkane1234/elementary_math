# Hand-rating campaigns

Human effort / quality labels for difficulty learning. Machine fields
(`type_id`, `generator`, `seed`, continuous `difficulty`, `theta_full`, Spec
snapshot / structure metadata) ship with each item; human fields start null.

| Campaign | Status | Path |
|----------|--------|------|
| **calc_derivatives** | 292/360 rated; calibrated — see [`CALIBRATION.md`](calc_derivatives/CALIBRATION.md) | [`calc_derivatives/`](calc_derivatives/) |
| calc_diff_gaps | Ready to build (other_base / log-diff / implicit) | [`calc_diff_gaps/`](calc_diff_gaps/) |
| algebra_1 | Packs in `CAMPAIGN.json`; not yet rated | [`algebra_1/`](algebra_1/) |
| algebra_2 | Packs in `CAMPAIGN.json`; not yet rated | [`algebra_2/`](algebra_2/) |
| precalc_algebraic | Packs in `CAMPAIGN.json`; not yet rated | [`precalc_algebraic/`](precalc_algebraic/) |

Course-level plumbing status: [`../ML_TRAINING_READINESS.md`](../ML_TRAINING_READINESS.md).

## Build / rebuild (offline packs)

```powershell
$env:PYTHONPATH='.'
python scripts/build_hand_rating_set.py --campaign calc_derivatives
# Do not overwrite rated calc_derivatives when adding gaps:
python scripts/build_hand_rating_set.py --campaign calc_diff_gaps --smoke
python scripts/build_hand_rating_set.py --campaign algebra_1 --smoke
```

## Live adaptive rater (v1)

Stratified continuous-`difficulty` loop: pick under-sampled D bin → live
generate → rate → append JSONL → next. Works for any Ready type with a
numeric `difficulty` setting. No GP / BO / multi-knob uncertainty yet (v2).

```powershell
$env:PYTHONPATH='.'
python scripts/live_rating_server.py
# open http://127.0.0.1:8777/

# CLI smoke
python scripts/live_rating_server.py --list-types
python scripts/live_rating_server.py --next --type-id g6_introduction_to_ratios --session smoke_g6
python scripts/live_rating_server.py --submit --type-id g6_introduction_to_ratios --session smoke_g6 --rating 3 --notes fake
python scripts/live_rating_server.py --coverage --type-id g6_introduction_to_ratios --session smoke_g6
```

Ratings land in `live/<session_or_type_id>/ratings.jsonl` with
`session.json` + optional `pending.json`. Each row stores `type_id`, `seed`,
`theta_requested`, `theta_full`, `rating_1_to_5`, `minutes`, `notes`, optional
`topic_fit_ok` / `latex_ok` / `broken`, `rated_at`, and `engine_rev` when
available.

## Rating schema (all campaigns)

| Field | Type | Role |
|-------|------|------|
| `rating_1_to_5` | int \| null | Primary human label |
| `minutes` | float \| null | Optional solve time |
| `notes` | string \| null | Pedagogy / latex flags |

Open `calc_derivatives/rater.html` to rate offline packs; export JSON / JSONL when done.
Use the live server above for the adaptive loop.
