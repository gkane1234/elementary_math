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
