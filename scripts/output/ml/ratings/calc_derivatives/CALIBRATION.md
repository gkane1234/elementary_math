# Calc derivatives — calibration report

Recovered ratings from Cursor browser localStorage → `calc_derivatives_ratings.json`.

## Coverage

- Items: **360**
- Rated (1–5): **292** (81.1%)
- Unrated / null: **68**
- Score histogram: `{1: 51, 2: 173, 3: 45, 4: 19, 5: 4}`

Unrated by pack:

- `chain`: 24
- `trig`: 20
- `ln_exp`: 20
- `invtrig`: 4

## Human vs machine

- Pearson(rating, y_effort): **0.526**
- Spearman(rating, y_effort): **0.410**
- Pearson(rating, difficulty): **0.337**
- Spearman(rating, difficulty): **0.303**

### Linear recalibration

- `rating ≈ 0.0843 * y_effort + 0.9818` (r=0.526, MAE=0.563)
- `y_effort ≈ 3.2801 * rating + 6.8040` (r=0.526)

Artifacts: `recalibration_linear.json`, filled rows `ratings_filled.jsonl`.

### Packs with most disagreement (z-score |human − y_effort|)

- **quotient** n=40 mean_rating=2.10 mean_y_effort=15.59 r(y_effort)=-0.05038351318126773 z_disagree=1.267
- **higher_order** n=32 mean_rating=1.84 mean_y_effort=11.58 r(y_effort)=-0.028588573549026403 z_disagree=1.265
- **power** n=48 mean_rating=1.88 mean_y_effort=8.13 r(y_effort)=0.046369461585882246 z_disagree=0.894
- **invtrig** n=28 mean_rating=2.11 mean_y_effort=15.28 r(y_effort)=0.43836691514972004 z_disagree=0.886
- **trig** n=20 mean_rating=1.65 mean_y_effort=16.46 r(y_effort)=0.7142913566533239 z_disagree=0.654

### Tiny forward model (human→effort-mapped target)

- kind: `gbr`
- metrics: `{'n_train': 219.0, 'n_test': 73.0, 'rmse': 1.0321022531064126, 'pearson_r': 0.9067267904981987}`
- saved: `human_forward_effort_model.json`

## Next steps

1. **Finish the 68 nulls** — reopen `rater.html`, filter Unrated, export JSON to `calc_derivatives_ratings.json` (or re-run extract from browser storage).
2. **OpenStax rating pass** — use `COVERAGE.md` checklist; rate textbook-aligned forms the generator under-covers (especially packs that disagree most).
3. **Expand campaigns** — build/rate `algebra_1`, `algebra_2`, `precalc_algebraic` with the same rater pipeline.
4. **Apply recalibration** — use `y_effort_from_rating` to supervise effort scorers, or fold the human forward model into inverse-D pilots for calc derivative packs.
