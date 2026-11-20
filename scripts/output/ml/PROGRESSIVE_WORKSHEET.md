# Progressive practice worksheets

Ship a **Progressive practice** mode that expands a seed topic into a small
coherent set and generates questions with a **global continuous-D ramp**.

## How to use (UI)

1. Open the worksheet app.
2. In **Worksheet settings → Mode**, choose **Progressive practice**.
3. Pick a **seed topic** (continuous-difficulty types only), set question count
   and `D min` / `D max`, and optionally **Include related topics**.
4. Click **Generate progressive worksheet**.
5. Or click a topic in the curriculum browser while in progressive mode to set
   the seed.

## How to use (API)

`POST /api/generate` with a `progressive` body (no `sections` needed):

```json
{
  "title": "Progressive Practice",
  "progressive": {
    "seed": "g6_introduction_to_ratios",
    "count": 10,
    "d_min": 0,
    "d_max": 18,
    "include_related": true,
    "max_topics": 4
  }
}
```

Also accepted: `seeds: ["pa_simplifying_fractions", ...]`.

- Set `"plan_only": true` to return the expanded `sections` / topic plan without
  generating questions.
- Response includes `progressive` (topics + difficulties) and `sections`
  (count=1 per question with rising `difficulty`).

Python helper:

```python
from question_engine.progressive import select_coherent_topics, build_progressive_sections
from question_engine.api.handler import handle_generate

topics = select_coherent_topics("pa_simplifying_fractions", n=4)
built = build_progressive_sections(seed="pa_simplifying_fractions", count=10)
status, _, body = handle_generate({"progressive": {"seed": "g6_introduction_to_ratios", "count": 8}})
```

## Worksheet templates (Grade 6 and Geometry)

Grade 6 and Geometry are the first courses on the template planner. A worksheet
is a template: scope, checked topics, pairing, and difficulty shape are choices.
Generating fills the questions from that template. Every other course still uses
`select_coherent_topics` below.

There is no generator that fuses two `type_id`s into one question. The harder
ending is the next adjacent leaf at high D.

### Request fields

| Field | Values | Default |
|-------|--------|---------|
| `pairing` | `lesson`, `drill`, `spiral` | `lesson` |
| `scope` | `topic`, `unit`, `adjacent` | `topic` |
| `topics` | checked type ids | omitted (planner chooses) |
| `style` | `ramp` (easy to hard), `straight` (flat) | `ramp` |
| `ramp_each_topic` | bool | false |
| `include_related` | bool | true. `false` drops warm-up and stretch |
| `max_topics` | int | 4. Caps auto warm-up and stretch. When `topics` is omitted the total topic list stays ≤ `max_topics`. Checked topics are kept even when there are more than four. |

`spiral` is never the default. When the unit is not the first unit in the course,
`spiral_suggestion` names the previous unit. The UI shows that as a hint. Choosing
spiral is still explicit. Spiral review uses earlier units in the **same** course
only, weighted to the previous unit.

Flat difficulty (`style: "straight"`) is a customization: one D, the midpoint of
`d_min` and `d_max`, checked topics only.

### Page order (easy to hard)

Warm-up, then selected topics in curriculum order, then a short procedure-drill
block of those topics, then one follow-on skill.

- Lesson, one topic: up to two earlier leaves in the unit (or `topic_leaves.json`
  `requires` when that type has them), then the seed, then a drill of that seed,
  then the next leaf in the unit or the first leaf of the next unit.
- Lesson, unit or adjacent: up to two leaves from the end of the same-course
  prerequisite unit, then the checked leaves, then the first eligible leaf of the
  following unit.
- Procedure drill: no warm-up and no follow-on. One topic expands to the seed plus
  the previous and next leaf in the unit. Unit or adjacent uses the checked leaves.
- Spiral: up to two leaves from the end of the previous unit, then the selected
  topics, then the first leaf of the next unit when there is one.

Difficulty on a ramp is one monotone schedule from `d_min` to `d_max` across the
page. Warm-up is about 20% (at least one question when count ≥ 4), stretch about
15% (at least one when count ≥ 6), drill about 20% of what remains, and the rest
is the selected topics. `ramp_each_topic` only groups the focus slice so each
selected topic sits in its own band of that ramp.

If `count` is smaller than the number of focus topics, the earlier ones are
placed and the rest are listed as `omitted_topics`.

Grade 6 is not an OpenStax book. Lesson order is the Illustrative-style unit
order in `lib/curriculum.ts` (`grade_6_math`). Unit prerequisites are
`scripts/example_mining/prerequisites/grade_6_math.json`. Geometry uses the same
template shape with `geometry.plan_topics` and `config/worksheet-gallery-geometry.json`.

Calls that omit `pairing`, `scope`, and `style` still default to lesson + ramp +
scope `topic` for Grade 6 and Geometry seeds.

### `plan_topics` signature

Both course modules use:

```python
def plan_topics(
    seeds,
    *,
    pairing="lesson",
    scope="topic",
    topics=None,
    max_topics=4,
    include_related=True,
) -> dict:
    # focus, warmup, drill, stretch, omitted, spiral_suggestion, course_id
```

`question_engine.worksheet_courses.base.plan_topics_for_seeds` returns that dict
when every seed is in `grade_6_math` or `geometry`, and `None` otherwise (the
old expander runs). If `geometry.py` cannot be imported, Geometry seeds use the
old expander and Grade 6 still plans.

## Coherence rules (`select_coherent_topics`)

Given seed type_id(s), build up to `n` topics (default 4):

1. Keep eligible seeds (registered, not demoted, continuous-D when required).
2. Add direct `topic_leaves.json` prerequisites (curriculum-earlier first).
3. Add same-catalog-category neighbors (closest index first).
4. Add immediate topic_leaves postrequisites.
5. If still short, fill from the rest of the same category.

**Continuous-D only by default:** related topics without a numeric `difficulty`
setting are skipped.

Topic order for the worksheet: prereqs → seeds → neighbors → postreqs so early
questions bias easier / prerequisite skills.

## Difficulty ramp

Question `i` of `N` gets:

`D = lerp(d_min, d_max, i / (N - 1))`

### Worksheet-level difficulty

Prefer setting `worksheet_difficulty` instead of raw `d_min`/`d_max`:

| Level   | d_min | d_max | schedule |
|---------|-------|-------|----------|
| level-0 | 0     | 3     | intro    |
| level-1 | 0     | 8     | gentle   |
| level-2 | 3     | 20    | moderate |
| level-3 | 8     | 25    | steep    |
| level-4 | 20    | 25    | intense  |

UI labels are **Level 0–4** (optional `D min–max` secondary). Legacy `easy`/`medium`/`hard`
and prior `d0-8`/`d4-14`/`d10-22` still resolve as aliases. A numeric value in `[0, 24]`
interpolates between level-0 and level-4. No Level 5 (only five ranges specified).
Implemented in `question_engine/worksheet_difficulty.py` and `lib/worksheet-difficulty.ts`.
Example gallery: `/gallery` (config in `config/worksheet-gallery.json`).

Topics rotate with a growing prefix of the coherent list (early indices stick
to earlier topics). Implemented as N sections of `count=1` so the existing
multi-section generate path works unchanged.

## Files

| Path | Role |
|------|------|
| `question_engine/progressive.py` | Selection + ramp helpers |
| `question_engine/api/handler.py` | `progressive` body support |
| `lib/api.ts` / `lib/progressive.ts` | Client helpers |
| `components/WorksheetGenerator.tsx` | Mode UI |
| `question_engine/tests/test_progressive_worksheet.py` | Coherence + D tests |

## Smoke examples

- Seed `g6_introduction_to_ratios` → related ratio family topics, D 0→12.
- Seed `pa_simplifying_fractions` → related PA fraction/decimal family, D 2→14.
