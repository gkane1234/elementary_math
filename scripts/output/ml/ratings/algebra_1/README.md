# algebra_1 — hand rating package

Generated for human effort / quality ratings. Machine fields are complete;
human fields start null.

Join keys: `rating_id`, `type_id`, `generator`, `seed`, `difficulty`,
`theta_full`, `spec_snapshot` when present.

```powershell
$env:PYTHONPATH='.'
python scripts/build_hand_rating_set.py --campaign algebra_1
```
