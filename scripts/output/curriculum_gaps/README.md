# Curriculum gap findings

Living notes on **topics we could add** to each course, discovered by comparing external curricula / TOCs / standards against our current `lib/curriculum.ts` + `question_engine/catalogs/`.

This is **not** a Ready/scaffolding tracker (see `scripts/output/DEFERRED.md` for UI/diagram deferrals). This folder is for **coverage gaps**: missing topics, unwired generators, and partial coverage worth expanding.

## Courses

| Course id | File | Last updated |
|-----------|------|--------------|
| `grade_6` | [grade_6.md](grade_6.md) | 2026-07-13 |
| `pre_algebra` | [pre_algebra.md](pre_algebra.md) | 2026-07-28 |
| `algebra_1` | [algebra_1.md](algebra_1.md) | 2026-07-16 |
| `geometry` | _(add `geometry.md`)_ | — |
| `algebra_2` | [algebra_2.md](algebra_2.md) | 2026-07-13 |
| `precalculus` | [precalculus.md](precalculus.md) | 2026-07-13 |
| `calculus` | [calculus.md](calculus.md) | 2026-07-13 |

Use the same `course_id` as in catalogs / curriculum when possible (`grade_6`, `pre_algebra`, `algebra_1`, …).

## How to research examples

When mining online exercises to generalize patterns and progressions (EMH vs new topics), follow [`EXAMPLE_MINING.md`](EXAMPLE_MINING.md). Research stops at gap-row updates unless the user asks to implement.

## How to add findings (for agents / humans)

1. Copy [`_TEMPLATE.md`](_TEMPLATE.md) → `<course_id>.md` if the course file does not exist yet.
2. Append rows to **Candidate additions** (do not rewrite unrelated history).
3. Prefer one row per discrete topic or OpenStax/CCSS-style section.
4. Update the **Courses** table above (`Last updated` + link).
5. Set **Status** carefully (see legend below). When a gap is shipped, mark `done` rather than deleting the row.
6. For example-mining captures, use the block in [`EXAMPLE_MINING.md`](EXAMPLE_MINING.md) in Evidence/notes (or a short subsection under the course file).

### Status legend

| Status | Meaning |
|--------|---------|
| `unwired` | Generator / framework already exists; needs catalog + curriculum wiring (and maybe presets). |
| `missing` | No suitable generator yet. |
| `partial` | Related type exists but does not fully cover the named skill. |
| `defer` | Intentionally skipped for now (below grade band, needs heavy UI, etc.). |
| `done` | Shipped / selectable under this course. |

### Effort (rough)

| Effort | Meaning |
|--------|---------|
| `S` | Wire existing generator to catalog/curriculum. |
| `M` | New type on existing framework / light generator work. |
| `L` | New framework, diagrams, or substantial generator design. |

## Source comparisons

When findings come from a specific textbook/TOC/standards pass, note the source in the course file’s **Sources** section (name + date). Multiple sources per course are fine.

For the OpenStax chapter-order reorganization of `lib/curriculum.ts` (and leftover “Other” wiring), see [`OPENSTAX_REORG.md`](OPENSTAX_REORG.md).
