# `g6_classifying_and_naming` — Classifying and naming polyhedra

> RED HEADER: **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** picture of a rectangular prism; name it (multiple choice in metadata).

**High D:** triangular prism, square pyramid, triangular pyramid. Still *name the solid*, not count faces/edges/vertices unless we add that (OpenStax does not emphasize Euler; IM sometimes counts faces).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Classify the polyhedron shown.}$` | `$\text{rectangular prism}$` |
| 8 | `$\text{Classify the polyhedron shown.}$` | `$\text{triangular prism}$` |
| 16 | `$\text{Classify the polyhedron shown.}$` | `$\text{triangular pyramid}$` |
| 22 | `$\text{Classify the polyhedron shown.}$` | `$\text{triangular pyramid}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Classify the polyhedron shown.}$` → `$\text{rectangular prism}$`
- D=22: `$\text{Classify the polyhedron shown.}$` → `$\text{triangular pyramid}$`

## OpenStax examples + chapter/section

**Prealgebra 2e §9.6** names rectangular solids, cubes, spheres, cylinders, cones in the volume section — identification is incidental to formulas.
G6 classify prisms/pyramids: **IM Grade 6 Unit 1** (polyhedra).

OpenStax does not have a “name the polyhedron” exercise bank comparable to this leaf.

## Variety notes

**LOW_VARIETY:** stem always `Classify the polyhedron shown.` D=0 is rectangular prism; high D piles on triangular pyramid. No “how many faces”, no net matching (nets were removed from catalog).

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY:** stem always `Classify the polyhedron shown.` D=0 is rectangular prism; high D piles on triangular pyramid. No “how many faces”, no net matching (nets were removed from catalog).

## Proposed engine (proposal only)

geometry classify-only (existing `g6_classify_polyhedron`). Not a formula engine.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
