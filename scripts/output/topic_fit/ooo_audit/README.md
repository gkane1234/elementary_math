# Order of operations audit

Samples via the **live continuous-D API path**:

`QUESTION_TYPES` → `handler._generate_for_type` → `primitive_g6.order_of_operations`
→ `build_context` (budget spend) → `sample_ooo_expression`.

This matches WorksheetGenerator / `/generate` for `order_of_operations` and
aliases (`g6_numeric_expressions_and_order_of_operations`, etc.).

## Open

```powershell
start scripts/output/topic_fit/ooo_audit/gallery.html
```

## Regenerate

```powershell
$env:PYTHONPATH='.'
python scripts/build_layer1_primitive_audits.py
# Related by_topic galleries:
python scripts/build_verified_topic_galleries.py --only-ooo
```

## What to look for

- Difficulties **0, 5, 10, 15, 20, 25**
- Metadata: `primitive_engine=ooo`, `spend`, `sample_log`, `upgrades`, `n_ops`
- Variety with D (more addends / ops, grouping, exponents) — not flat EMH-looking stems only
- No bare numbers (see `test_ooo_no_bare_number`)
