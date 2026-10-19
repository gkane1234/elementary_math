# Development directions

A place to keep product ideas that are not the current task. Each direction says what it is, what already exists, and what it is not.

## Showcase build

The near-term goal is a build that shows the project working: varied questions, ordinary math, figures where the topic has them, and an honest split between topics that are ready to teach with and topics that are not.

Sort topics into four buckets. The buckets are about utility as a learning tool, not about whether the generator returns a string.

| Bucket | Meaning | What to do in a showcase |
|--------|---------|--------------------------|
| **Ready** | The prompt, the answer, and any figure change across draws, and the skill matches the topic name. | Include on the demo worksheet and in the gallery without a caveat. |
| **Thin** | The generator runs, but two draws are the same problem, or several topic names share one sentence. | Show one example and say the pool has one question at this difficulty. |
| **Unclear** | The words do not say what the student is supposed to do, or the figure the topic promises is missing. Older notes marked these `UNCLEAR`. | Keep out of the demo until the prompt or the figure is fixed. |
| **Low variety** | A figure or a number changes, but the task is one Mad-Lib. Older notes marked these `LOW_VARIETY`. | Usable for practice inside a unit. Weak as a showcase of range. |

The older flags live in `scripts/output/skeleton_phase01_gallery/notes/`. Of 588 notes, about 100 open with `UNCLEAR` and about 119 with `LOW_VARIETY` (about 35 carry both). Examples of unclear: graphing topics whose gold standard has no graph, polynomial naming that only says “quadratic,” word-problem stubs that print an equation with no story. Examples of low variety: one trig equation repeated, one scatter-plot story, precalculus limits that repeat one rational at a fixed seed.

## Duplicate questions

Two checks, both at difficulty 6 with no seed.

**Inside one topic.** Two independent draws had the same prompt for 43 of 604 ready topics. Many of those are a fixed sentence (“Find the area of the parallelogram,” “Find the area of the triangle,” a single trig equation). A later gallery pass compared prompt, answer, and figure, retried up to twelve times, and also refused a prompt already used by another topic in the same chapter. After that, 7 topics still had only one distinct question.

**Across topics in one chapter.** Six pairs in the same catalog category produced the same prompt on the first draw:

- Grade 6 polygons: “Parallelograms, understanding area formula” and “Parallelograms.”
- Pre-algebra plane figures: “Quadrilaterals” and “Area of triangles and quadrilaterals” (both a trapezoid).
- Geometry quadrilaterals: “Trapezoids” and “Area of triangles and quadrilaterals.”
- Geometry similarity: “Similar triangles” and “Similar right triangles.”
- Geometry probability: the word-problem leaf and the plain leaf (both a coin and a die).
- Precalculus trigonometry: “Equations with factoring and fundamental identities” and “Equations and multiple-angle identities” (both \(2\sin^2\theta-\sin\theta=0\)).

The all-topics gallery drops a second card when it is the same problem. It does not yet give those topics a larger pool.

## How a worksheet includes topics

There are two modes.

**Chosen sections.** The worksheet is a list of sections. Each section is one `type_id`, a count, and that topic’s settings. `POST /api/generate` walks the sections and generates each one on its own. Nothing is added that the user did not put in the list. This is the ordinary generator: the teacher picks Power Rule, then Quotient Rule, and gets only those.

**Progressive practice.** The user picks a seed topic, a count, and a difficulty range. `question_engine/progressive.py` expands the seed before any question is written:

1. Keep the seed if it is registered and not demoted.
2. Add earlier topics listed as prerequisites in `scripts/example_mining/prerequisites/topic_leaves.json`.
3. Add neighbors in the same catalog chapter, preferring ids that share a skill word.
4. Add topics that list the seed as their prerequisite.
5. If that is still short, fill from the rest of the chapter.

The default cap is 4 topics. Question \(i\) of \(N\) gets a difficulty linearly between `d_min` and `d_max`. Early questions lean toward the prerequisites. Details and the level presets are in [`scripts/output/ml/PROGRESSIVE_WORKSHEET.md`](scripts/output/ml/PROGRESSIVE_WORKSHEET.md).

Progressive practice is one worksheet that mixes related topics at rising difficulty. It does not remember what a class finished last week.

## Spaced review of topics

A different idea from progressive practice. A class sequence is an ordered list, for example topic \(x\), then \(y\), then \(z\). A worksheet whose target is \(z\) would also include a few questions on \(x\) and \(y\), and sometimes one harder question whose main skill is \(x\) but whose expression also uses something from \(y\) or \(z\).

What exists now can supply the earlier topics: `topic_leaves.json` already names prerequisites, and progressive mode already inserts them at the low end of one difficulty ramp. What does not exist is a class memory. Nothing records “this class has finished \(x\) and \(y\) and is now on \(z\).” Nothing schedules a review gap (a topic last practiced \(n\) worksheets ago). Nothing builds a synthesis item that is graded as skill \(x\) while containing a sub-expression from \(y\) or \(z\).

A first version can stay inside the section model: given a target topic and a list of already-taught topics, emit sections for a few review counts plus the target count, using the prerequisite list as the default “already taught” set when the teacher does not pass one. The synthesis item is a later step. It needs the expression tree, so that a derivative or an equation can be wrapped in a skill from an earlier topic without becoming a different topic’s question.

## Other directions

**Form quality, separate from difficulty.** Topic-fit ratings tilt which catalog form is sampled. Effort stays on the forward and inverse models. See [Two learning loops](README.md#two-learning-loops).

**Edits after the form is chosen.** Derivatives already apply a small edit catalog to an expression tree. Limits, integrals, algebra, and figures have named OpenStax moves in `question_engine/frameworks/primitives/openstax_edit_catalogs.py`. Most of those families still write a finished string, so the edit list is not applied yet. The direction is: build the expression or the figure as parts first, then run the family’s edit list.

**Trees for every topic kind.** An expression, a figure, and a data list are different trees. One edit catalog does not cover all three. Expression topics that already have an OpenStax form catalog (limits, integrals, algebra) are the next place to reuse the derivative edit machinery.

**Showcase gallery.** `scripts/output/topic_fit/expression_edits_gallery/gallery.html` has two draws for each ready topic, with figures when the generator produced one. It is a review surface for the four buckets above, not a curriculum sequence.
