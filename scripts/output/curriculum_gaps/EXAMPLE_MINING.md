# Example mining playbook

Research online exercises and worked sequences so we can **generalize** problem patterns and **progressions**, then record findings as gap rows. This phase stops at documentation — do **not** implement generators, presets, or curriculum leaves unless the user explicitly asks.

Related: [README.md](README.md) (gap status legend), [`question_engine/FRAMEWORK.md`](../../question_engine/FRAMEWORK.md) (implementation hand-off later).

## Purpose

1. Find open / citation-friendly sources of exercises or skill sequences.
2. Extract a **generalizable pattern** (structure + parameters + constraints).
3. Separate **within-topic difficulty** (EMH) from **new topics** (next curriculum leaf).
4. Append or refine a **Candidate additions** row in `scripts/output/curriculum_gaps/<course_id>.md`.

## Preferred sources

Prefer open or clearly attributable curricula first:

| Source | Use for |
|--------|---------|
| OpenStax (Elementary Algebra, Intermediate Algebra, Prealgebra, Calculus, …) | TOC sections + exercise sets; primary comparison source for many gap files |
| Local OpenStax HTML mirror (`textbooks/openstax/html/`) | Offline mining with MathML preserved — see [`textbooks/README.md`](../../../textbooks/README.md) and `scripts/mirror_openstax.py` |
| Illustrative Mathematics | Task sequences and grade-band progressions |
| EngageNY / Eureka Math | Lesson progressions within a module |
| CK-12 | Skill pages and practice sets |
| Khan Academy | **Skill titles and order only** (exercise lists as progressions) — do not paste proprietary item text |
| CCSS / state cluster progressions | Ordering of skills across grades, not individual stems |

### Mirroring OpenStax HTML (recommended before mining)

```powershell
$env:PYTHONPATH='.'
python scripts/mirror_openstax.py --book calculus-volume-1 --chapter 2
python scripts/mirror_openstax.py --book elementary-algebra-2e --chapter 7
```

Pages land under `textbooks/openstax/html/<book>/` (gitignored). Prefer mining from these files over live scrapes so math stays as MathML.

Multiple sources per skill are fine. Always record name, section/id, URL (if any), and date consulted in the course file **Sources** table and in the capture block.

## What to capture vs not

**Do**

- Cite source + section + URL + date.
- **Paraphrase** 2–3 example stems that show the pattern (change numbers/names; keep structure).
- Write the shared structure, parameters, constraints, and answer form.
- Sketch Easy / Medium / Hard knobs for the **same** skill.
- Name `progression_next` when the source sequence moves to a different method or skill.

**Do not**

- Dump copyrighted problem text wholesale into the repo.
- Treat “Hard” as a different topic (e.g. Hard factoring ≠ quadratic formula).
- Implement frameworks, catalog entries, or `lib/curriculum.ts` leaves in a research-only pass.
- Put Ready / UI / diagram blockers here — use `scripts/output/DEFERRED.md`.

## Two progression kinds (hard rule)

| Kind | Meaning | Where it lives later |
|------|---------|----------------------|
| **EMH** | Same named skill; harder parameters (coeffs, steps, constraints, distractors) | Difficulty presets for one `type_id` |
| **New topic** | Different method or skill (new technique, new application type) | Separate gap row → eventual catalog type + curriculum leaf |

If a textbook section “builds” by introducing a new technique, that is `progression_next`, not Hard of the previous skill.

## Generalization checklist

Before writing the gap row, answer:

1. **Stem template** — What does the student see? (equation form, figure, narrative slots)
2. **Answer form** — Expression, number, choice, graph, ordered pair, …
3. **Parameters** — What varies across instances? (integers, leading coeff, GCF present, …)
4. **Constraints** — What must stay true for the skill to stay on-topic?
5. **Forbidden drifts** — Wrong methods or topics that must not appear under this type name

If you cannot fill (1)–(4), keep researching or mark the gap `defer` with a reason.

## Capture block (copy into Evidence / notes)

Paste a filled version into the gap row’s **Evidence / notes** cell, or under a short subsection in the course file if the table cell would be unreadable. Keep paraphrases short.

```markdown
### Example mining — <skill short name>
- **Source:** <name>, §<section> (<URL>); consulted YYYY-MM-DD
- **Paraphrased stems:**
  1. …
  2. …
  3. …
- **Pattern:** <structure>; params: <list>; constraints: <list>
- **Answer form:** …
- **EMH sketch:**
  - Easy: …
  - Medium: …
  - Hard: …
- **progression_next:** <next skill name or “—”>
- **Suggested:** status=`missing|partial|unwired`; effort=`S|M|L`; chapter=<…>
- **Forbidden drifts:** …
```

Then update the Candidate additions row: set **Status** / **Effort** / **Suggested catalog chapter** to match, and point Evidence/notes at this capture (or inline a one-line summary plus “see Example mining subsection below”).

## When research is done

1. Append a new Candidate additions row, or refine an existing one — do not delete history; mark `done` when shipped later.
2. Add or update the **Sources** table in that course file.
3. Update **Last updated** on the course file and the Courses table in [README.md](README.md).
4. Stop. Implementation is a separate request.

## Hand-off to implementation (Option 2/3 later)

When asked to build the skill (not during Option 1 research):

1. Domain settings + `QuestionFramework.build_prompt` (prefer `question_engine/frameworks/`)
2. Expose a generator key via `framework_generators` / `GENERATORS`
3. EMH presets from the capture’s EMH sketch
4. Catalog `entry(...)` + curriculum leaf under the suggested chapter
5. Topic-fit sample (`scripts/topic_fit_sample.py`) before marking the gap `done`

Option 2 can lift these capture blocks into a dedicated `example_mining/` stash without changing the research rules above.
