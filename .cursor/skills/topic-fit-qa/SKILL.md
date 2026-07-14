---
name: topic-fit-qa
description: >-
  Sample and review generated math questions for topic appropriateness (correct
  skill, method, and within-topic difficulty), not answer-key correctness. Use
  when the user asks to QA questions, check topic fit, review a question family,
  audit generators for wrong-topic wiring, or run topic-fit sampling.
---

# Topic-fit question QA

## Goal

Verify questions **match the curriculum topic** — not that answers are mathematically correct.

Catch: wrong generator / miswire, wrong method under a named technique, hard that changes topic instead of getting harder, scaffold/stub under Ready types.

Do **not** spend effort verifying answer keys unless a wrong answer is incidental evidence of wrong topic. Exception: identify-property types (`g6_properties_of_addition_and_multiplication`) — auto heuristics flag keys that are bare operation names or numeric products (miswire signal).

## Workflow

1. Sample a pack for the requested family or types.
2. Read `gallery.md` (+ `auto_flags.json` as pre-flags only).
3. Score each type with the rubric below.
4. Write `scripts/output/topic_fit/<family>_REPORT.md` from `_TEMPLATE.md`.
5. Prefer fixing generator / presets / catalog wiring over documenting-and-moving-on when fails are clear.

### Generate a sample pack

```powershell
$env:PYTHONPATH='.'
python scripts/topic_fit_sample.py --family poly_quad --n 3
python scripts/topic_fit_sample.py --type-id quadratic_factoring --n 5
python scripts/topic_fit_sample.py --prefix radical_ --n 2
```

Families: `poly_quad`, `a1_equations`, `radical_rational`, `graphing_linear`.

Outputs under `scripts/output/topic_fit/<run_id>/`:
- `samples.jsonl`
- `gallery.md`
- `auto_flags.json`

### Hand path

1. Run the CLI above.
2. Open `gallery.md`.
3. Copy `scripts/output/topic_fit/_TEMPLATE.md` → `<family>_REPORT.md`.
4. Fill the table; list failures with evidence; fix or defer.

### Agent path

Same artifacts and rubric. Auto flags are heuristics — still judge prompts yourself. See [reference.md](reference.md) for miswire patterns and pack schema.

## Rubric

| Criterion | Pass when |
|-----------|-----------|
| **Topic?** | Prompt asks for the skill named by the type |
| **Method?** | Technique matches type name / catalog intent |
| **Hard harder?** | Hard is harder *within the same topic* |
| **Ready integrity?** | No scaffold/stub/placeholder under Ready types |
| **Wiring?** | Generator is not an obvious wrong-topic alias |

## Report location

Write: `scripts/output/topic_fit/<family>_REPORT.md` (or `<type_id>_REPORT.md` for deep dives).

Use the columns: Type | E/M/H samples | Topic? | Method? | Hard harder? | Status.
