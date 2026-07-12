# Topic-fit QA report — TEMPLATE

Scope: _family or type list_

Generated sample pack: `scripts/output/topic_fit/<run_id>/`

## Rubric

Score each type for **topic appropriateness**, not answer-key correctness.

| Criterion | Pass when |
|-----------|-----------|
| Topic? | Prompt asks for the skill named by the type |
| Method? | Technique matches the type (GCF stays GCF; grouping looks like grouping) |
| Hard harder? | Hard is meaningfully harder *within the same topic* |
| Ready integrity? | No scaffold / stub / placeholder under Ready types |
| Wiring? | Generator is not an obvious wrong-topic alias |

Optional note only if noticed: incidental wrong answers that reveal wrong topic.

## Verification table

| Type | E sample | M sample | H sample | Topic? | Method? | Hard harder? | Status |
|------|----------|----------|----------|--------|---------|--------------|--------|
| `type_id` | … | … | … | Y/N | Y/N | Y/N | Pass / Fail / Deferred |

## Failures found

### `type_id` — short title

- Evidence: sample prompt(s)
- Why it fails topic-fit
- Likely fix location (generator / presets / catalog wiring)

## Deferred

| Item | Evidence | Why deferred |
|------|----------|--------------|
| … | … | … |

## Files to touch

- …
