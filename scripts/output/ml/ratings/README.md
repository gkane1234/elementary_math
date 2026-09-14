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

## Live adaptive rater (pairwise Bayesian utility)

Default loop: under-sampled **generator** → type → D (cold) or UCB /
informative pair (ready) → generate **A and B** → choose A better / B better /
tie → Bayesian linear utility **refits on every submit**. Absolute 1–5 is
optional / legacy. Works for every Ready type with a numeric `difficulty`
setting (WIP leaves included). A generator used by several topics is updated by
ratings from **any** of them (`generator` is a model feature).

Once `model_ready`, the posterior **changes generation**: Thompson / UCB
reweights `form_id` in `select_form_id` (`live_quality_form_weights`) and the
next pair is chosen for uncertainty / comparison information. This is a sampling
tilt, not difficulty-cost padding.

**Campaigns**

| Campaign | What it covers | Default session folder |
|----------|----------------|------------------------|
| **`all_topics`** (UI default) | All Ready continuous-D topics | `live/all_topics/` |
| `skeleton_deriv` | `calc_diff_*` skeleton-path subset | `live/skeleton_deriv/` |
| single `type_id` | One leaf | `live/<type_id>/` |

Until **8 pairs** or **20** absolute 1–5 ratings (not broken/skipped) on the
**current** generation fingerprint, `model_ready=false` and `predicted_rating`
is n/a.

**Generation-process reset.** Each live row stamps `engine_rev` (git HEAD plus
a short hash of uncommitted `question_engine` generation-path diffs, or
`POLY_ENGINE_REV`). If that fingerprint changes, the live `ratings.jsonl` is
moved to `live/<session>/history/ratings.<old_rev>.<timestamp>.jsonl` and the
model cold-starts. Old labels stay on disk; they do not train the new process.

```powershell
$env:PYTHONPATH='.'
python scripts/live_rating_server.py
# open http://127.0.0.1:8777/
# Campaign dropdown: all_topics (default), skeleton_deriv, or single type_id
# Load next → A better / B better / Tie (keys a/b/t) → optional flags/notes → Submit & next

# CLI smoke — all-topics campaign (pairwise)
python scripts/live_rating_server.py --next --campaign all_topics --session smoke_all
python scripts/live_rating_server.py --submit --campaign all_topics --session smoke_all --winner a
python scripts/live_rating_server.py --coverage --campaign all_topics --session smoke_all

# Named subset
python scripts/live_rating_server.py --next --campaign skeleton_deriv --session smoke_skel

# Single-item (legacy --rating)
python scripts/live_rating_server.py --list-types
python scripts/live_rating_server.py --next --single --type-id g6_introduction_to_ratios --session smoke_g6
python scripts/live_rating_server.py --submit --type-id g6_introduction_to_ratios --session smoke_g6 --rating 3 --notes fake
```

Ratings land in `live/<session>/ratings.jsonl` with `session.json` + optional
`pending.json`. Pair rows use `record_kind=pair`, `pair_id`, `left`, `right`,
`winner`, plus `engine_rev` / generators / form_ids. Legacy single-item rows
(`rating_1_to_5`) still load. `/api/next` returns a `pair` (default) with
`predicted_rating`, `predicted_std`, `n_train`, `n_pairs`, `model_ready`.

Cold-start thresholds: `MIN_PAIRS = 8`, `MIN_TRAIN = 20` in
`question_engine/ml/rating_regressor.py`.

## Rating schema (all campaigns)

| Field | Type | Role |
|-------|------|------|
| `winner` | `a` \| `b` \| `tie` \| null | Primary pairwise label |
| `rating_1_to_5` | int \| null | Optional / legacy absolute label |
| `minutes` | float \| null | Optional solve time |
| `notes` | string \| null | Pedagogy / latex flags |

Open `calc_derivatives/rater.html` to rate offline packs; export JSON / JSONL when done.
Use the live server above for the adaptive loop.
